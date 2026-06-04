# Evaluation

## Submission format

Upload a `.zip` with **`agent.py` at the top level** (not inside a subfolder).

Your file must define:

```python
class Agent:
    def act(self, obs, action_mask, info) -> int:
        ...
```

## Scoring

Codabench runs your agent on several random **morning scenarios** (fixed seeds, not shown to you).

| Metric | Meaning |
|--------|---------|
| **score** | Mean episode reward (higher is better) |
| **mean_reward** | Same value |
| **episodes** | Number of mornings simulated |

Reward includes:

- Negative travel time (minutes)
- Penalties for late school arrivals
- Penalties for long / unequal student ride times
- Random road slowdowns during the route

## Phases

| Phase | Seeds | Purpose |
|-------|-------|---------|
| **Development** | 10 scenarios | Practice and leaderboard feedback |
| **Final** | 30 hidden scenarios | Official ranking |

## Time limits

- Development: 20 minutes per submission
- Final: 30 minutes per submission

## What is *not* allowed

- Submitting precomputed score files instead of `agent.py`
- Downloading new map data during evaluation
- Zip files larger than 50 MB
