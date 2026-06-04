"""
Build fixed Hackensack graph cache + eval seed lists for Codabench.

Run from repo root (requires network once for OSMnx):
  python scripts/precompute_competition_data.py
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sbrp_env.road_network import RoadNetwork  # noqa: E402

# Smaller instance = faster Codabench scoring; same rules, less compute.
NUM_STOPS = 20
NUM_SCHOOLS = 3
POI_SEED = 42

DEV_SEEDS = list(range(1000, 1010))
FINAL_SEEDS = list(range(2000, 2030))


def main():
    cache_dir = ROOT / "competition_data" / "graph_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    print("Building road network (one-time OSM download)...")
    rn = RoadNetwork(
        num_stops=NUM_STOPS,
        num_schools=NUM_SCHOOLS,
        poi_seed=POI_SEED,
    )
    rn.save_cache(cache_dir)

    seeds_dir = ROOT / "competition_data" / "seeds"
    seeds_dir.mkdir(parents=True, exist_ok=True)

    for name, seeds in [("dev_seeds.json", DEV_SEEDS), ("final_seeds.json", FINAL_SEEDS)]:
        path = seeds_dir / name
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"seeds": seeds, "num_stops": NUM_STOPS, "num_schools": NUM_SCHOOLS}, f, indent=2)
        print(f"Wrote {path} ({len(seeds)} seeds)")

    meta = {
        "num_stops": NUM_STOPS,
        "num_schools": NUM_SCHOOLS,
        "num_buses": 4,
        "bus_capacity": 30,
        "poi_seed": POI_SEED,
    }
    with open(ROOT / "competition_data" / "env_config.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print("Done.")


if __name__ == "__main__":
    main()
