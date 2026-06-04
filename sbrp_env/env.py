import gymnasium as gym
from gymnasium import spaces
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
from .road_network import RoadNetwork
from .scenario_generator import ScenarioGenerator

class HackensackSBRPOptimizationEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(
        self,
        render_mode=None,
        num_stops=40,
        num_schools=5,
        num_buses=8,
        bus_capacity=30,
        cache_dir=None,
    ):
        super().__init__()
        self.render_mode = render_mode
        self.num_stops = num_stops
        self.num_schools = num_schools
        self.num_buses = num_buses
        self.bus_capacity = bus_capacity

        self.rn = RoadNetwork(
            num_stops=self.num_stops,
            num_schools=self.num_schools,
            cache_dir=cache_dir,
        )
        self.sg = ScenarioGenerator(num_stops=self.num_stops, num_schools=self.num_schools)
        
        # Action space: select next POI (0 to num_schools-1 are schools, the rest are stops)
        self.action_space = spaces.Discrete(self.num_schools + self.num_stops)
        
        # Observation space
        self.observation_space = spaces.Dict({
            "bus_states": spaces.Box(low=0, high=1000, shape=(self.num_buses, 4), dtype=np.float32), 
            # [location_idx, available_time, passengers_on_board, school_target]
            "stop_states": spaces.Box(low=0, high=100, shape=(self.num_stops, 2), dtype=np.float32),
            # [waiting_students, school_target_idx]
            "global_time": spaces.Box(low=0, high=1000, shape=(1,), dtype=np.float32),
            "current_bus": spaces.Box(low=0, high=self.num_buses, shape=(1,), dtype=np.float32)
        })
        
        self.fig, self.ax = None, None
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.rn.reset_disruptions()
        demands, school_assignments, start_times = self.sg.generate_morning_scenario()
        
        self.stop_states = np.zeros((self.num_stops, 2), dtype=np.float32)
        self.stop_states[:, 0] = demands
        self.stop_states[:, 1] = school_assignments
        
        self.school_start_times = start_times
        
        self.bus_states = np.zeros((self.num_buses, 4), dtype=np.float32)
        # All buses start at school 0 (acting as depot) at time 0
        self.bus_states[:, 0] = 0
        self.bus_states[:, 1] = 0 # available_time
        self.bus_states[:, 2] = 0 # passengers
        self.bus_states[:, 3] = -1 # no target school yet
        
        self.global_time = 0.0
        self.current_bus_idx = 0
        self.total_reward = 0.0
        
        self.ride_times = [] # for equity penalty
        
        return self._get_obs(), self._get_info()
        
    def _get_obs(self):
        return {
            "bus_states": self.bus_states,
            "stop_states": self.stop_states,
            "global_time": np.array([self.global_time], dtype=np.float32),
            "current_bus": np.array([self.current_bus_idx], dtype=np.float32)
        }
        
    def _get_info(self):
        return {
            "num_schools": self.num_schools,
            "num_stops": self.num_stops,
            "num_buses": self.num_buses,
        }
        
    def valid_action_mask(self):
        mask = np.zeros(self.action_space.n, dtype=np.int8)
        bus = self.bus_states[self.current_bus_idx]
        current_loc = int(bus[0])
        passengers = bus[2]
        target_school = int(bus[3])
        
        # Can drop off at school if we have passengers
        if passengers > 0 and target_school != -1:
            mask[target_school] = 1
        
        # If no passengers or not full, can visit stops that have waiting students
        if passengers < self.bus_capacity:
            for i in range(self.num_stops):
                if self.stop_states[i, 0] > 0:
                    stop_school_target = int(self.stop_states[i, 1])
                    # Ensure bus only picks up kids for the same school
                    if target_school == -1 or target_school == stop_school_target:
                        mask[self.num_schools + i] = 1
                        
        # If mask is entirely 0, the bus has nothing to do, can just stay at its current location
        if np.sum(mask) == 0:
            mask[current_loc] = 1
            
        return mask

    def step(self, action):
        bus = self.bus_states[self.current_bus_idx]
        current_loc = int(bus[0])
        action = int(action)
        
        reward = 0
        done = False
        
        if current_loc != action:
            # Calculate travel time
            # Travel time is in seconds, convert to minutes
            travel_time_sec = self.rn.get_time(current_loc, action)
            travel_time_min = travel_time_sec / 60.0
            
            # Apply time
            self.bus_states[self.current_bus_idx, 1] += travel_time_min
            self.bus_states[self.current_bus_idx, 0] = action
            reward -= travel_time_min # Penalty for travel time
            
            # If arriving at a school
            if action < self.num_schools:
                if bus[2] > 0 and int(bus[3]) == action:
                    # Drop off students
                    students_dropped = bus[2]
                    self.bus_states[self.current_bus_idx, 2] = 0
                    self.bus_states[self.current_bus_idx, 3] = -1
                    
                    # Lateness penalty
                    arrival_time = self.bus_states[self.current_bus_idx, 1]
                    deadline = self.school_start_times[action]
                    if arrival_time > deadline:
                        reward -= (arrival_time - deadline) * students_dropped * 0.5
            
            # If arriving at a stop
            else:
                stop_idx = action - self.num_schools
                waiting = self.stop_states[stop_idx, 0]
                if waiting > 0:
                    school_target = self.stop_states[stop_idx, 1]
                    
                    # Check capacity
                    available_space = self.bus_capacity - bus[2]
                    pickup = min(waiting, available_space)
                    
                    self.stop_states[stop_idx, 0] -= pickup
                    self.bus_states[self.current_bus_idx, 2] += pickup
                    self.bus_states[self.current_bus_idx, 3] = school_target
                    
                    # Record for equity penalty later (simplified)
                    self.ride_times.append(self.bus_states[self.current_bus_idx, 1])
        else:
            # If the bus decides to stay put / wait, advance its time by 1 minute
            self.bus_states[self.current_bus_idx, 1] += 1.0
            reward -= 0.1 # Small penalty for waiting

        # Random disruption
        if np.random.rand() < 0.05:
            self.rn.trigger_disruption()
            
        # Find next bus to make a decision
        self.current_bus_idx = np.argmin(self.bus_states[:, 1])
        self.global_time = self.bus_states[self.current_bus_idx, 1]
        
        # Check termination (all stops empty and all buses empty)
        all_stops_empty = np.sum(self.stop_states[:, 0]) == 0
        all_buses_empty = np.sum(self.bus_states[:, 2]) == 0
        
        if all_stops_empty and all_buses_empty:
            done = True
            
            # Equity penalty
            if len(self.ride_times) > 1:
                std_ride = np.std(self.ride_times)
                if std_ride > 15: # threshold
                    reward -= std_ride * 2

        if self.global_time > 200: # max episode length in minutes
            done = True
            
        self.total_reward += reward
        
        if self.render_mode == "human":
            self.render()
            
        return self._get_obs(), reward, done, False, self._get_info()
        
    def render(self):
        if self.rn.G is None:
            return
        if self.fig is None:
            plt.ion()
            self.fig, self.ax = plt.subplots(figsize=(8, 8))
            
        self.ax.clear()
        
        # Plot schools
        sx = [self.rn.G.nodes[n]['x'] for n in self.rn.school_nodes]
        sy = [self.rn.G.nodes[n]['y'] for n in self.rn.school_nodes]
        self.ax.scatter(sx, sy, c='red', s=200, marker='*', label='Schools')
        
        # Plot stops
        stx = [self.rn.G.nodes[n]['x'] for n in self.rn.stop_nodes]
        sty = [self.rn.G.nodes[n]['y'] for n in self.rn.stop_nodes]
        
        sizes = self.stop_states[:, 0] * 10
        self.ax.scatter(stx, sty, c='blue', s=sizes, alpha=0.5, label='Stops (size=demand)')
        
        # Plot buses
        bx, by = [], []
        for i in range(self.num_buses):
            loc_idx = int(self.bus_states[i, 0])
            node_id = self.rn.poi_nodes[loc_idx]
            bx.append(self.rn.G.nodes[node_id]['x'])
            by.append(self.rn.G.nodes[node_id]['y'])
        self.ax.scatter(bx, by, c='green', s=100, marker='s', label='Buses')
        
        self.ax.set_title(f"Time: {self.global_time:.1f} mins | Active Bus: {self.current_bus_idx}")
        self.ax.legend()
        plt.pause(0.01)
        
    def close(self):
        if self.fig is not None:
            plt.close(self.fig)
