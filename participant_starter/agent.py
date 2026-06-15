"""
Your routing agent - edit this file only.

At each step the simulator asks: "Which stop or school should the active bus visit next?"
Return one integer action index.
"""


class Agent:
    def __init__(self):
        # Optional: load a trained PyTorch model here.
        # TensorFlow is not available in the Codabench scoring image.
        pass

    def act(self, obs, action_mask, info):
        num_schools = info["num_schools"]
        current_bus_idx = int(obs["current_bus"][0])
        bus = obs["bus_states"][current_bus_idx]
        current_loc = int(bus[0])
        passengers = float(bus[2])
        target_school = int(bus[3])
        time_matrix = info["time_matrix"]

        # If the bus is full, go straight to the school.
        if passengers >= 30 and target_school >= 0 and action_mask[target_school]:
            return target_school

        # Score valid stops by nearby demand. This is still simple, but it is
        # smarter than always picking the biggest stop across town.
        best_action = current_loc
        best_score = -1.0
        for stop_idx in range(obs["stop_states"].shape[0]):
            action = num_schools + stop_idx
            if not action_mask[action]:
                continue

            demand = float(obs["stop_states"][stop_idx, 0])
            if demand <= 0:
                continue

            travel_minutes = float(time_matrix[current_loc][action]) / 60.0
            score = demand / (travel_minutes + 1.0)
            if score > best_score:
                best_score = score
                best_action = action

        if best_score > 0:
            return int(best_action)

        # No pickup is possible, so drop off if possible.
        if passengers > 0 and target_school >= 0 and action_mask[target_school]:
            return target_school

        # Last resort: pick the first valid action.
        for action, is_valid in enumerate(action_mask):
            if is_valid:
                return int(action)
        return current_loc
