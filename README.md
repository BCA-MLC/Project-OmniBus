# OmniMan — NJ Hackensack School Bus Routing (RL Competition)

Gymnasium environment for the **School Bus Routing Problem** on a real **Hackensack, NJ** OpenStreetMap network, packaged for **[Codabench](https://www.codabench.org)** hosting.

## Quick links

| Audience | Document / artifact |
|----------|---------------------|
| **Participants** | `participant_starter/HOW_TO_SUBMIT.md` and `dist/participant_starter_kit.zip` |
| **Organizers** | `codabench/HOST_ON_CODABENCH.md` and `dist/hackensack_sbrp_competition.zip` |

## Organizer — publish on Codabench

```bash
conda activate base
pip install -r requirements.txt
python scripts/precompute_competition_data.py
python scripts/build_codabench_bundle.py
```

Upload `dist/hackensack_sbrp_competition.zip` to Codabench (**Benchmark → Management → Upload**). See `codabench/HOST_ON_CODABENCH.md` for compute workers and go-live checklist.

## Participant — develop and test

1. Get `participant_starter_kit.zip` from your teacher.
2. Clone this repo and install deps.
3. Edit `participant_starter/agent.py`.
4. Run `python participant_starter/run_submission.py` from the repo root.
5. Zip **only** `agent.py` (+ optional `model.zip`) and upload on Codabench.

## Project layout

```
sbrp_env/              # Simulator (env, road network, eval runner)
participant_starter/   # What students edit + HOW_TO_SUBMIT.md
codabench/             # competition.yaml, ingestion, scoring, docs
competition_data/      # Cached graph + eval seeds (generated)
scripts/               # precompute, build bundle
dist/                  # Built zips (after build script)
```

## Training (optional)

```bash
python train.py --train --timesteps 20000
python train.py  # evaluate saved model
python baselines.py
```
