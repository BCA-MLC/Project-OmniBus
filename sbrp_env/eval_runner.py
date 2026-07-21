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
    """Run one episode and return per-episode metrics.

    Security contract
    -----------------
    * The agent receives read-only copies of observations and info (enforced
      by the env's ``_frozen`` helper).  Any attempted in-place mutation
      raises ``ValueError`` inside the agent process rather than corrupting
      the harness's internal state.
    * ``reward`` is the scalar returned *directly* by ``env.step()`` — it is
      computed inside the env from ``self.rn.get_time()`` (the judge's own
      copy), never from anything that passed through the agent's hands.
    * ``info`` returned by ``env.step()`` is likewise a fresh read-only copy;
      we do **not** use it for scoring — it is only forwarded to the agent
      on the next call so the agent can plan.
    * As an independent cross-check, the returned dict also includes
      ``env_total_reward`` taken from ``env.total_reward`` (accumulated
      inside the env) so the judge can verify the harness-side accumulation
      matches the env-side accumulation.
    """
    obs, info = env.reset(seed=seed)
    total_reward = 0.0
    steps = 0
    done = False

    while not done:
        mask = env.valid_action_mask()
        action = int(agent.act(obs, mask, info))
        # reward is the raw float from env.step() — computed inside the env
        # from the env's own internal time_matrix, NOT from info.
        obs, reward, done, _truncated, info = env.step(action)
        total_reward += float(reward)
        steps += 1

    # env.total_reward is the env's own running accumulation — an independent
    # check against our harness-side total_reward.  They should match.
    env_side_total = float(env.total_reward)

    return {
        "seed": seed,
        "reward": total_reward,
        "env_reward": env_side_total,
        "steps": steps,
    }


def evaluate_agent(
    agent: RoutingAgent,
    seeds: list[int],
    *,
    cache_dir: str | Path | None = None,
    num_stops: int = 20,
    num_schools: int = 3,
    num_buses: int = 4,
) -> dict:
    """Evaluate *agent* over *seeds* and return aggregate metrics.

    Tamper detection
    ----------------
    Each episode records both the harness-side reward accumulation
    (``reward``) and the env-side accumulation (``env_reward``).  If they
    diverge by more than floating-point epsilon, it indicates that the agent
    managed to influence the reward signal from outside the env — which
    should be structurally impossible given the read-only copy protections,
    but is worth checking explicitly.  A ``tampering_detected`` flag is
    included in the returned dict so Codabench ingestion can reject the
    submission.
    """
    env = HackensackSBRPOptimizationEnv(
        num_stops=num_stops,
        num_schools=num_schools,
        num_buses=num_buses,
        cache_dir=cache_dir,
    )
    episodes = [run_episode(env, agent, seed) for seed in seeds]
    env.close()
    rewards = [e["reward"] for e in episodes]

    # Cross-check: harness reward vs. env-internal reward.  Should match
    # to within normal float accumulation error.
    tamper_flags = []
    for ep in episodes:
        delta = abs(ep["reward"] - ep["env_reward"])
        if delta > 1e-3:  # larger than any plausible fp rounding gap
            import warnings
            warnings.warn(
                f"Reward divergence detected on seed {ep['seed']}: "
                f"harness={ep['reward']:.4f}, env={ep['env_reward']:.4f}, "
                f"delta={delta:.6f}.  Possible reward tampering.",
                stacklevel=2,
            )
            tamper_flags.append(ep["seed"])

    return {
        "episodes": episodes,
        "mean_reward": float(np.mean(rewards)),
        "std_reward": float(np.std(rewards)) if len(rewards) > 1 else 0.0,
        "num_episodes": len(seeds),
        "tampering_detected": bool(tamper_flags),
        "tampered_seeds": tamper_flags,
    }


def load_seeds(path: str | Path) -> list[int]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        return list(data["seeds"])
    return list(data)
