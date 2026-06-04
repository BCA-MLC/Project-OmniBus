# Host this competition on Codabench (organizer checklist)

## 1. Build the bundle

```bash
conda activate base
cd OmniMan
pip install -r requirements.txt
python scripts/precompute_competition_data.py
python scripts/build_codabench_bundle.py
```

Upload **`dist/hackensack_sbrp_competition.zip`** to [Codabench](https://www.codabench.org) → **Benchmark → Management → Upload**.

## 2. Edit before publishing

In `codabench/competition.yaml` (rebuild after edits):

- `contact_email`
- Phase `start` / `end` dates
- `title` / descriptions

Set **Publish** in the competition editor when ready.

## 3. Compute worker (required for real traffic)

Public shared queues are unreliable for many school teams. Run your own worker:

1. Competition editor → **Queue Management** → create a queue → copy **Broker URL**
2. On a Linux VM (≈100 GB disk, Docker installed), follow [Compute Worker Setup](https://docs.codabench.org/latest/Organizers/Running_a_benchmark/Compute-Worker-Management---Setup/)
3. In `competition.yaml`, set `queue:` to your queue **Vhost** (from queue details)

## 4. Docker image

Default `codalab/codalab-legacy:py37` is enough (numpy is preinstalled; graph is cached in input data).

For `stable-baselines3` in *organizer* tests only, use a custom image — participants should not need SB3 on the server if they only submit `agent.py` with hand-written logic.

## 5. Distribute to students

Send **`dist/participant_starter_kit.zip`** — not the full competition bundle.

Point them to **`HOW_TO_SUBMIT.md`** inside that zip.

## 6. Test a submission

1. Upload `dist/example_solution.zip` under **My Submissions** on your competition
2. Confirm **Results** shows a numeric score

Local dry-run:

```bash
python participant_starter/run_submission.py
```

## 7. Files participants upload

```
TeamName.zip
├── agent.py      ← required
└── model.zip     ← optional
```

Nothing else.
