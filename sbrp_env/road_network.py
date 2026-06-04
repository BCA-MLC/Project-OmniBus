import json
import random
from pathlib import Path

import networkx as nx
import numpy as np

try:
    import osmnx as ox
except ImportError:
    ox = None


class RoadNetwork:
    def __init__(
        self,
        place_name="Hackensack, New Jersey, USA",
        num_stops=20,
        num_schools=5,
        poi_seed=None,
        cache_dir=None,
    ):
        self.place_name = place_name
        self.num_stops = num_stops
        self.num_schools = num_schools
        self.G = None

        if cache_dir is not None:
            self._load_cache(cache_dir)
            return

        if ox is None:
            raise ImportError("osmnx is required unless cache_dir is provided.")

        print(f"Downloading road network for {self.place_name}...")
        self.G = ox.graph_from_place(self.place_name, network_type="drive")
        self.G = ox.add_edge_speeds(self.G)
        self.G = ox.add_edge_travel_times(self.G)

        self.nodes = list(self.G.nodes)
        print("Selecting schools and stops...")
        self._select_locations(poi_seed=poi_seed)
        print("Calculating distance and time matrices...")
        self._calculate_matrices()

    def _largest_component_nodes(self):
        if self.G is None:
            return self.nodes
        undirected = self.G.to_undirected()
        components = list(nx.connected_components(undirected))
        largest = max(components, key=len)
        return list(largest)

    def _select_locations(self, poi_seed=None):
        rng = random.Random(poi_seed) if poi_seed is not None else random
        pool = self._largest_component_nodes()
        n = self.num_schools + self.num_stops
        if len(pool) < n:
            raise ValueError(f"Need {n} POIs but largest road component has only {len(pool)} nodes.")
        selected = rng.sample(pool, n)
        self.school_nodes = selected[: self.num_schools]
        self.stop_nodes = selected[self.num_schools :]
        self.poi_nodes = self.school_nodes + self.stop_nodes

    def _calculate_matrices(self):
        n = len(self.poi_nodes)
        self.time_matrix = np.zeros((n, n), dtype=np.float32)
        # Undirected travel times so every POI in the main component can reach every other
        travel_g = self.G.to_undirected()
        for u, v, data in travel_g.edges(data=True):
            t = data.get("travel_time")
            if t is None or t <= 0:
                length = data.get("length", 1.0)
                speed = data.get("speed_kph", 30.0)
                t = length / max(speed, 1.0) * 3.6
            data["travel_time"] = float(t)

        for i, origin in enumerate(self.poi_nodes):
            lengths = nx.single_source_dijkstra_path_length(
                travel_g, origin, weight="travel_time"
            )
            for j, dest in enumerate(self.poi_nodes):
                self.time_matrix[i, j] = lengths.get(dest, 1e6)
        self.base_time_matrix = self.time_matrix.copy()

    def save_cache(self, cache_dir: str | Path):
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        config = {
            "place_name": self.place_name,
            "num_stops": self.num_stops,
            "num_schools": self.num_schools,
            "school_nodes": self.school_nodes,
            "stop_nodes": self.stop_nodes,
            "poi_nodes": self.poi_nodes,
        }
        with open(cache_dir / "poi_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f)
        np.save(cache_dir / "time_matrix.npy", self.time_matrix)
        np.save(cache_dir / "base_time_matrix.npy", self.base_time_matrix)

    def _load_cache(self, cache_dir: str | Path):
        cache_dir = Path(cache_dir)
        with open(cache_dir / "poi_config.json", encoding="utf-8") as f:
            config = json.load(f)
        self.place_name = config["place_name"]
        self.num_stops = config["num_stops"]
        self.num_schools = config["num_schools"]
        self.school_nodes = config["school_nodes"]
        self.stop_nodes = config["stop_nodes"]
        self.poi_nodes = config["poi_nodes"]
        self.time_matrix = np.load(cache_dir / "time_matrix.npy")
        self.base_time_matrix = np.load(cache_dir / "base_time_matrix.npy")

    def get_time(self, origin_idx, dest_idx):
        return self.time_matrix[origin_idx, dest_idx]

    def trigger_disruption(self):
        self.time_matrix = self.base_time_matrix.copy()
        idx1 = random.randint(0, len(self.poi_nodes) - 1)
        idx2 = random.randint(0, len(self.poi_nodes) - 1)
        if idx1 != idx2:
            multiplier = random.uniform(2.0, 5.0)
            self.time_matrix[idx1, :] *= multiplier
            self.time_matrix[:, idx1] *= multiplier

    def reset_disruptions(self):
        self.time_matrix = self.base_time_matrix.copy()


if __name__ == "__main__":
    rn = RoadNetwork(num_stops=5, num_schools=2, poi_seed=0)
    print("Network initialized successfully.")
    print("Time matrix shape:", rn.time_matrix.shape)
