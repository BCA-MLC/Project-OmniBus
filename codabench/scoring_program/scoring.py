"""
Codabench scoring: read ingestion results and write scores.json for the leaderboard.
"""
import json
import os
from pathlib import Path

OUTPUT_DIR = Path("/app/output")


def find_predictions() -> Path:
    candidates = [
        Path("/app/input") / "res" / "results.json",
        Path("/app/output") / "results.json",
        Path("/app/input") / "results.json",
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Missing results.json from ingestion. Tried: " + ", ".join(str(p) for p in candidates)
    )


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    predictions_path = find_predictions()

    with open(predictions_path, encoding="utf-8") as f:
        results = json.load(f)

    mean_reward = float(results["mean_reward"])
    num_episodes = int(results["num_episodes"])

    scores = {
        "score": mean_reward,
        "mean_reward": mean_reward,
        "episodes": num_episodes,
    }

    with open(OUTPUT_DIR / "scores.json", "w", encoding="utf-8") as f:
        json.dump(scores, f)

    print("scores.json:", scores)


if __name__ == "__main__":
    main()
