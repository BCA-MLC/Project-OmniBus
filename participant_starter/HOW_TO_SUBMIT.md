# How to Submit (Hackensack School Bus Routing)

## What you are building

You edit **one file**: `agent.py`.  
It tells each school bus which stop or school to visit next.

You do **not** upload your whole project. You upload a small **zip file**.

---

## Step 1 — Get the files

Download **participant_starter** from the competition page (or your club leader).

You also need the full **OmniMan** repo once, to test locally:

```text
git clone 
cd OmniMan
pip install -r requirements.txt
python scripts/precompute_competition_data.py
```

(Your teacher may give you a USB copy instead of git.)

---

## Step 2 — Edit your agent

Open `participant_starter/agent.py` in any editor.

Change the `act(...)` method to make smarter routing decisions.

**Optional — machine learning**

1. Train on your computer (ask your club leader for `train.py` help).
2. Save weights as `model.zip` in the same folder as `agent.py`.
3. Load them inside `Agent.__init__` in `agent.py`.

---

## Step 3 — Test before you submit

From the **OmniMan** folder (not inside participant_starter):

```bash
python participant_starter/run_submission.py
```

You should see a line like:

```text
Mean reward: -123.45
```

If you see an error, fix it before uploading.

---

## Step 4 — Make the zip file

Create a folder named with your team name, e.g. `TeamHawks`.

Put **only** these inside:

| File | Required? |
|------|-----------|
| `agent.py` | **Yes** — your code |
| `model.zip` | Only if you trained a model |

**Do not** include `run_submission.py`, `train.py`, or the whole repo.

### Windows

1. Select `agent.py` (and `model.zip` if you have it).
2. Right-click → **Send to** → **Compressed (zipped) folder**.
3. Rename to `TeamHawks.zip`.

### Mac

1. Select the files → right-click → **Compress**.
2. Rename to `TeamHawks.zip`.

The zip must list `agent.py` at the **top level** (not inside another folder).  
Wrong: `TeamHawks.zip` → `TeamHawks` → `agent.py`  
Right: `TeamHawks.zip` → `agent.py`

---

## Step 5 — Upload on Codabench

1. Go to [codabench.org](https://www.codabench.org) and sign in.
2. Open **NJ School Bus Routing** (your competition).
3. Click **My Submissions**.
4. Click the **paperclip** / upload button.
5. Choose your `TeamHawks.zip`.
6. Wait until status says finished (may take a few minutes).
7. Open the **Results** tab to see your score.

---

## What the score means

- **Higher is better** (less negative is better).
- The score is the average reward over several morning scenarios.
- Penalties include long bus rides, late arrivals, and unfair ride times.

---

## Rules (short)

- One zip per submission.
- Max zip size: **50 MB** (check competition page).
- Do not try to download the internet inside `agent.py` during scoring.
- Be registered on Codabench before the deadline.

---

## Need help?

Ask your club leader or email the address on the competition overview page.
