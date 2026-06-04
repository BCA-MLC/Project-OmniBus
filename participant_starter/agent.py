"""
Your routing agent — edit this file only.

At each step the simulator asks: "Which stop or school should the active bus visit next?"
Return one integer action index.
"""
import numpy as np


class Agent:
    def __init__(self):
        # Optional: load a trained model here, e.g.:
        # from stable_baselines3 import PPO
        # self.model = PPO.load("model.zip")
        pass

    def act(self, obs, action_mask, info):
        num_schools = info["num_schools"]
        current_bus_idx = int(obs["current_bus"][0])
        bus = obs["bus_states"][current_bus_idx]
        current_loc = int(bus[0])
        passengers = float(bus[2])
        target_school = int(bus[3])

        # Drop off at the target school when possible
        if passengers > 0 and target_school >= 0 and action_mask[target_school]:
            return target_school

        # Otherwise visit the valid stop with the most waiting students
        best_action = current_loc
        best_demand = -1.0
        for stop_idx in range(obs["stop_states"].shape[0]):
            action = num_schools + stop_idx
            if not action_mask[action]:
                continue
            demand = float(obs["stop_states"][stop_idx, 0])
            if demand > best_demand:
                best_demand = demand
                best_action = action

        if best_demand > 0:
            return int(best_action)

        # No good move — pick any valid action
        valid = np.where(action_mask)[0]
        return int(valid[0]) if len(valid) else current_loc
