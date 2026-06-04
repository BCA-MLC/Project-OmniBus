"""
Codabench ingestion: run each participant's agent.py on hidden eval seeds.
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

PROGRAM_DIR = Path("/app/program")
INGESTED_DIR = Path("/app/ingested_program")
INPUT_DIR = Path("/app/input_data")
OUTPUT_DIR = Path("/app/output")

sys.path.insert(0, str(PROGRAM_DIR))
sys.path.insert(0, str(INGESTED_DIR))

from sbrp_env.eval_runner import evaluate_agent, load_seeds  # noqa: E402


def load_participant_agent():
    agent_path = INGESTED_DIR / "agent.py"
    if not agent_path.exists():
        raise FileNotFoundError(
            "Submission must include agent.py at the top level of the zip."
        )
    spec = importlib.util.spec_from_file_location("participant_agent", agent_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "Agent"):
        raise AttributeError("agent.py must define a class named Agent with act().")
    return module.Agent()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(INPUT_DIR / "env_config.json", encoding="utf-8") as f:
        env_cfg = json.load(f)

    seeds_path = INPUT_DIR / "eval_seeds.json"
    seeds = load_seeds(seeds_path)
    cache_dir = INPUT_DIR / "graph_cache"

    agent = load_participant_agent()
    results = evaluate_agent(
        agent(),
        seeds,
        cache_dir=cache_dir,
        num_stops=env_cfg["num_stops"],
        num_schools=env_cfg["num_schools"],
        num_buses=env_cfg["num_buses"],
    )

    out_path = OUTPUT_DIR / "results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Wrote {out_path} — mean_reward={results['mean_reward']:.4f}")


if __name__ == "__main__":
    main()
