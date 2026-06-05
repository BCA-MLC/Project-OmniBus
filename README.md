# NJ Hackensack School Bus Routing Challenge (Project OmniBus)

Welcome to the Hackensack School Bus Routing Challenge! In this competition, you will design a reinforcement learning or rule-based routing agent to navigate school buses through a real-world OpenStreetMap road network of Hackensack, New Jersey.

Your agent's goal is to decide which stop or school each bus should visit next to pick up waiting students and deliver them to their assigned schools before the morning deadlines—all while minimizing travel times, late arrivals, and ride-time inequality (unfairness).

## 📦 Getting the Competition Files

There are two ways to get started:

### Option 1: Download the Starter Kit

If you only need the files required to build and submit an agent:

1. Open the **Releases** section on the right side of this GitHub repository.
2. Download **`participant_starter_kit.zip`** from the latest release.
3. Extract the ZIP file and begin editing `agent.py`.

The starter kit contains:

* `agent.py`
* `HOW_TO_SUBMIT.md`
* Local testing utilities

### Option 2: Clone the Full Repository

If you want access to the simulator, training scripts, baselines, and development tools, clone the full repository and follow the setup instructions below.

🚀 Quick Start Guide

### Step 1: Clone the Repository & Install Dependencies

First, clone this repository to your local machine and install the required Python packages:

```bash
git clone https://github.com/your-username/Project-OmniBus.git
cd Project-OmniBus
pip install -r requirements.txt
```

> **Note**
>
> We recommend running these commands inside a virtual environment (like conda or venv) to prevent package version conflicts.

### Step 2: Precompute the Road Network Cache

To avoid downloading large map databases from the internet during training and testing, run the precompute script once:

```bash
python scripts/precompute_competition_data.py
```

This downloads the Hackensack drivable road network and precomputes the travel-time matrices, saving them locally under `competition_data/graph_cache/`.

### Step 3: Implement Your Agent

Open `participant_starter/agent.py` in your editor. This is the only file you need to modify.

Complete the `act` method:

```python
class Agent:
    def act(self, obs, action_mask, info):
        # Your routing logic here!
        # Return an integer action index representing the next school or stop to visit.
        ...
```

### Step 4: Test Your Agent Locally

Run the local test harness to evaluate your current agent on 10 public development scenarios:

```bash
python participant_starter/run_submission.py
```

You will see output showing the number of completed episodes and your Mean Reward (a higher score closer to 0 is better).

## 🤖 Training a Reinforcement Learning Model (Optional)

If you want to train a neural network using reinforcement learning (RL) rather than hand-writing rules, you can use the provided training script:

### Train a Model

We use Stable-Baselines3 and sb3-contrib's MaskablePPO to learn to route buses directly from experience:

```bash
python train.py --train --timesteps 20000
```

This trains an RL agent on the correct competition environment settings using the precomputed graph cache and saves the model weights to `sbrp_agent.zip`.

### Evaluate the Trained Model

To check how your trained model performs visually, run it with the rendering flag:

```bash
python train.py --render
```

### Reference Baselines

To see how a simple nearest-neighbor heuristic performs on this task, run:

```bash
python baselines.py
```

Use this score as a benchmark to beat!

## 📦 How to Submit

Once your agent is ready, prepare a ZIP file to upload to Codabench:

1. Select only the following files from your `participant_starter` folder:

   * `agent.py` (required)
   * `model.zip` (optional; if you trained an RL model, rename `sbrp_agent.zip` to `model.zip` and place it here)
2. Compress them into a ZIP file (e.g., `TeamName.zip`). Ensure these files are at the root level of the ZIP file, not nested inside a folder.
3. Upload your ZIP file on the **My Submissions** tab of the Codabench Competition Page.

> **Important**
>
> * Do not include `run_submission.py`, `train.py`, or any other repository files in your submission.
> * Max submission size is 50 MB.
> * Do not try to download external data inside `agent.py` during evaluation.

## 📚 Documentation

For more details, check out:

* `HOW_TO_SUBMIT.md` inside the `participant_starter` folder.
* The Evaluation, Data, and Terms tabs on the Codabench competition website.
