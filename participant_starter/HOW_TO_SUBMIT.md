# How to Submit

This is the short guide for the Hackensack School Bus Routing Challenge.

You only edit one file: `agent.py`.

Your final submission is a small `.zip` file. It should not contain the whole
Project OmniBus repo.

---

## Step 1 - Get The Files

Use one of these options.

### Easiest option: download the starter kit

1. Go to the Project OmniBus GitHub page:
   https://github.com/BCA-MLC/Project-OmniBus
2. Open **Releases** on the right side of the page.
3. Download `participant_starter_kit.zip`.
4. Unzip it.

You should see:

```text
agent.py
run_submission.py
HOW_TO_SUBMIT.md
```

### Better for local testing: clone the full repo

If you are comfortable using a terminal, run:

```bash
git clone https://github.com/BCA-MLC/Project-OmniBus.git
cd Project-OmniBus
pip install -r requirements.txt
```

The GitHub repo already includes the small competition cache files used by
`run_submission.py`, so you should not need to download map data.

If `pip` or `python` is not found, install Python 3.11 or use Anaconda Prompt.
On Windows with Anaconda, open **Anaconda Prompt**, then run the same commands.

---

## Step 2 - Edit `agent.py`

Open `participant_starter/agent.py` in VS Code, IDLE, Notepad, or any editor.

The evaluator will call:

```python
agent.act(obs, action_mask, info)
```

Your job is to return one valid action number.

Important:

- `action_mask[action]` tells you whether an action is legal.
- `info["time_matrix"]` tells you the travel time between places.
- Higher scores are better. Scores are usually negative, so closer to `0` is
  better.

You can make a good first improvement without machine learning. For example,
try choosing a nearby stop with many waiting students instead of a random stop.

### Optional machine learning

The Codabench scoring image supports the competition environment, Gymnasium,
NumPy, and PyTorch-based tools such as Stable-Baselines3. TensorFlow is not
available in the scoring image, so do not submit TensorFlow/Keras code.

If you train a model, save the model file next to `agent.py` and include it in
your zip. Keep the zip under the Codabench size limit.

---

## Step 3 - Test Before You Submit

From the full `Project-OmniBus` folder, run:

```bash
python participant_starter/run_submission.py
```

You should see something like:

```text
Episodes: 10
Mean reward: -123.45
```

If you see `ModuleNotFoundError`, install the requirements:

```bash
pip install -r requirements.txt
```

If you are using Anaconda on Windows, run the commands in **Anaconda Prompt**.

---

## Step 4 - Make The Zip File

Your zip must contain `agent.py` at the top level.

Correct:

```text
TeamHawks.zip
  agent.py
```

Also correct if you trained a model:

```text
TeamHawks.zip
  agent.py
  model.zip
```

Wrong:

```text
TeamHawks.zip
  TeamHawks/
    agent.py
```

Wrong:

```text
TeamHawks.zip
  agent.py
  run_submission.py
  train.py
  competition_data/
```

### Windows

Open a terminal in the folder that contains `agent.py`, then run:

```powershell
Compress-Archive -Path .\agent.py -DestinationPath .\TeamHawks.zip -Force
```

If you also have `model.zip`, run:

```powershell
Compress-Archive -Path .\agent.py, .\model.zip -DestinationPath .\TeamHawks.zip -Force
```

### Mac

Open a terminal in the folder that contains `agent.py`, then run:

```bash
zip TeamHawks.zip agent.py
```

If you also have `model.zip`, run:

```bash
zip TeamHawks.zip agent.py model.zip
```

---

## Step 5 - Upload On Codabench

1. Go to https://www.codabench.org/competitions/16945/ and sign in.
2. Click **My Submissions**.
3. If Codabench asks you to register, check the terms box and click
   **Register**.
4. Under **Submission upload**, keep **Submit as: Yourself**.
5. Click the paperclip upload button.
6. Choose your zip file, such as `TeamHawks.zip`.
7. Wait for the upload and scoring run to finish. This can take several
   minutes.
8. Check the **Status**, **Score**, and logs.
9. When the run finishes successfully, click the small green button in the
   **Actions** column to add that submission to the leaderboard. This lets the
   competition organizers see it in the official results table.

If the status says failed, click the log/error action in the row and read the
message. The most common mistake is a zip that contains a folder instead of
putting `agent.py` directly at the top level.

---

## Rules

- Submit one zip file.
- Include `agent.py`.
- Include a model file only if your code loads it.
- Do not include the whole repo.
- Do not use TensorFlow/Keras; the scoring image is built for PyTorch/Gymnasium.
- Do not download files from the internet inside `agent.py` during scoring.
- Make sure you are registered before the deadline.

Need help? Email `machinelearningclubbca@gmail.com`.
