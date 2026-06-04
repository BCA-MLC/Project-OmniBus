# Data

## What organizers provide

- Precomputed **Hackensack drivable road network** travel times between bus stops and schools
- **Scenario seeds** (student demand, school start times, attendance) — hidden during scoring

Participants do **not** receive raw OSM files in the submission zip. The graph is bundled on the scoring server.

## What participants download

1. **participant_starter_kit.zip** — `agent.py`, `HOW_TO_SUBMIT.md`, local test script
2. **Project-OmniBus repository** (optional) — for local development and ML training

Before local testing, run once:

```bash
pip install -r requirements.txt
python scripts/precompute_competition_data.py
```

## Observation format (`obs`)

| Key | Shape | Meaning |
|-----|-------|---------|
| `bus_states` | (num_buses, 4) | location, time, passengers, target school |
| `stop_states` | (num_stops, 2) | waiting students, target school |
| `global_time` | (1,) | simulation clock |
| `current_bus` | (1,) | which bus is deciding now |

`action_mask` lists which destination indices are legal.
