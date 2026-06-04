"""
Test your submission locally before uploading to Codabench.

Run from the OmniMan repo root:
  python participant_starter/run_submission.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent import Agent
from sbrp_env.eval_runner import evaluate_agent, load_seeds

CACHE = ROOT / "competition_data" / "graph_cache"
SEEDS = ROOT / "competition_data" / "seeds" / "dev_seeds.json"
CONFIG = ROOT / "competition_data" / "env_config.json"


def main():
    if not CACHE.exists():
        print("Missing graph cache. Run: python scripts/precompute_competition_data.py")
        sys.exit(1)

    import json

    with open(CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)

    seeds = load_seeds(SEEDS)
    agent = Agent()
    results = evaluate_agent(
        agent,
        seeds,
        cache_dir=CACHE,
        num_stops=cfg["num_stops"],
        num_schools=cfg["num_schools"],
        num_buses=cfg["num_buses"],
    )
    print(f"Episodes: {results['num_episodes']}")
    print(f"Mean reward: {results['mean_reward']:.2f}")
    print("(Higher is better — closer to 0 means fewer penalties.)")


if __name__ == "__main__":
    main()
