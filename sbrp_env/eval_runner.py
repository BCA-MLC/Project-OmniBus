"""Shared evaluation loop for local tests, Codabench ingestion, and baselines."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Protocol

import numpy as np

from .env import HackensackSBRPOptimizationEnv


class RoutingAgent(Protocol):
    def act(self, obs: dict, action_mask: np.ndarray, info: dict) -> int:
        ...


def run_episode(env: HackensackSBRPOptimizationEnv, agent: RoutingAgent, seed: int) -> dict:
    obs, info = env.reset(seed=seed)
    total_reward = 0.0
    steps = 0
    done = False

    while not done:
        mask = env.valid_action_mask()
        action = int(agent.act(obs, mask, info))
        obs, reward, done, _truncated, info = env.step(action)
        total_reward += float(reward)
        steps += 1

    return {"seed": seed, "reward": total_reward, "steps": steps}


def evaluate_agent(
    agent: RoutingAgent,
    seeds: list[int],
    *,
    cache_dir: str | Path | None = None,
    num_stops: int = 20,
    num_schools: int = 3,
    num_buses: int = 4,
) -> dict:
    env = HackensackSBRPOptimizationEnv(
        num_stops=num_stops,
        num_schools=num_schools,
        num_buses=num_buses,
        cache_dir=cache_dir,
    )
    episodes = [run_episode(env, agent, seed) for seed in seeds]
    env.close()
    rewards = [e["reward"] for e in episodes]
    return {
        "episodes": episodes,
        "mean_reward": float(np.mean(rewards)),
        "std_reward": float(np.std(rewards)) if len(rewards) > 1 else 0.0,
        "num_episodes": len(seeds),
    }


def load_seeds(path: str | Path) -> list[int]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        return list(data["seeds"])
    return list(data)
