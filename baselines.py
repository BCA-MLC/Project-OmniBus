"""Nearest-neighbor baseline using the competition eval harness."""
import json
import sys
from pathlib import Path

import numpy as np

from sbrp_env.eval_runner import evaluate_agent, load_seeds

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "competition_data" / "graph_cache"
SEEDS = ROOT / "competition_data" / "seeds" / "dev_seeds.json"
CONFIG = ROOT / "competition_data" / "env_config.json"


class NearestNeighborAgent:
    def __init__(self, env):
        self.env = env

    def act(self, obs, action_mask, info):
        current_bus_idx = int(obs["current_bus"][0])
        bus = obs["bus_states"][current_bus_idx]
        current_loc = int(bus[0])

        best_action = current_loc
        min_time = float("inf")
        for action in range(len(action_mask)):
            if not action_mask[action]:
                continue
            travel_time = self.env.rn.get_time(current_loc, action)
            if travel_time < min_time:
                min_time = travel_time
                best_action = action
        return int(best_action)


def evaluate_baseline():
    with open(CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)
    seeds = load_seeds(SEEDS)

    from sbrp_env.env import HackensackSBRPOptimizationEnv

    env = HackensackSBRPOptimizationEnv(
        num_stops=cfg["num_stops"],
        num_schools=cfg["num_schools"],
        num_buses=cfg["num_buses"],
        cache_dir=CACHE,
    )
    agent = NearestNeighborAgent(env)

    episodes = []
    for seed in seeds:
        obs, info = env.reset(seed=seed)
        total_reward = 0.0
        done = False
        while not done:
            mask = env.valid_action_mask()
            action = agent.act(obs, mask, info)
            obs, reward, done, _t, info = env.step(action)
            total_reward += float(reward)
        episodes.append(total_reward)
    env.close()
    return float(np.mean(episodes)), len(episodes)


if __name__ == "__main__":
    mean_r, n = evaluate_baseline()
    print(f"Nearest-neighbor baseline: mean reward = {mean_r:.2f} over {n} episodes")
