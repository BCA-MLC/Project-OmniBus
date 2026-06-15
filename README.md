# NJ Hackensack School Bus Routing Challenge (Project OmniBus)

Welcome to Project OmniBus; a Hackensack School Bus Routing Challenge. In this competition, high school students will build a routing agent for school buses on a real Hackensack, New Jersey road network from OpenStreetMap.

Your agent decides which stop or school each bus should visit next. The simulator handles travel times, bus capacity, student pickup and dropoff, school start times, random road disruptions, and fairness penalties for long or unequal ride times.

You can build either:

- A rule-based agent, such as a nearest-stop or capacity-aware routing strategy
- A reinforcement learning agent trained from simulation experience
- A hybrid agent that combines hand-written rules with a trained model

## AI Tools Are Encouraged

We fully encourage participants to use AI tools, including generative AI, large language models, coding assistants, chatbots, and AI-powered development tools.

You may use AI to help you:

- Understand the starter code
- Learn Python, reinforcement learning, and routing strategies
- Brainstorm agent designs
- Write, edit, and debug `agent.py`
- Interpret error messages
- Compare rule-based and machine learning approaches
- Learn how to train and load models

Using AI effectively is part of modern programming and machine learning. Treat AI as a learning partner: ask it questions, test its suggestions, and make sure your final submission runs correctly.

## Who Can Join

- Any high school student in the United States, ages 14 to 18
- No prior reinforcement learning experience required
- Beginners can start with the provided starter `agent.py`

To be eligible for prizes, fill out the official prize eligibility form:

**[Prize Eligibility Form](https://forms.gle/woD4Tzpib9aafzK36)**

You can also find competition information on the website:

**[Competition Website](https://competition.bcamlc.com/)**

## Getting the Competition Files

There are two ways to get started.

### Option 1: Download the Starter Kit

If you only need the files required to build and submit an agent:

1. Open the **Releases** section on the right side of this GitHub repository.
2. Download **`participant_starter_kit.zip`** from the latest release.
3. Extract the zip file.
4. Begin editing `agent.py`.

The starter kit contains:

- `agent.py`
- `HOW_TO_SUBMIT.md`
- Local testing utilities

This is the recommended path if you want the simplest setup.

### Option 2: Clone the Full Repository

If you want access to the simulator, training scripts, baselines, and development tools, clone the full repository and follow the setup instructions below.

```bash
git clone https://github.com/BCA-MLC/Project-OmniBus.git
cd Project-OmniBus
pip install -r requirements.txt
```

We recommend running these commands inside a virtual environment, such as `venv` or `conda`, to avoid package conflicts.

## Quick Start Guide

### Step 1: Precompute the Road Network Cache

Before local training or full-repository testing, run the precompute script once:

```bash
python scripts/precompute_competition_data.py
```

This downloads the Hackensack drivable road network and precomputes travel-time data. The cached files are saved locally so future runs do not need to download the map again.

Participants do not need to include raw OpenStreetMap files or graph cache files in their Codabench submission. The scoring server already has the needed competition data.

### Step 2: Implement Your Agent

Open `participant_starter/agent.py` in your editor. For most participants, this is the only file you need to modify.

Your file must define an `Agent` class with an `act` method:

```python
class Agent:
    def act(self, obs, action_mask, info) -> int:
        # Return an integer action index for the next stop or school to visit.
        ...
```

Your agent should return a valid integer action. Use `action_mask` to avoid choosing illegal actions.

### Step 3: Test Your Agent Locally

Run the local test harness:

```bash
python participant_starter/run_submission.py
```

The script evaluates your current agent on public development scenarios and prints your mean reward. Higher scores are better.

## Observation Format

Your agent receives three inputs:

```python
def act(self, obs, action_mask, info) -> int:
    ...
```

The `obs` object contains the current simulator state.

| Key | Shape | Meaning |
|-----|-------|---------|
| `bus_states` | `(num_buses, 4)` | Bus location, time, passenger count, and target school |
| `stop_states` | `(num_stops, 2)` | Waiting students and target school for each stop |
| `global_time` | `(1,)` | Current simulation clock |
| `current_bus` | `(1,)` | Which bus is currently choosing an action |

The `action_mask` lists which destination indices are currently legal.

## Training a Reinforcement Learning Model (Optional)

You do not need reinforcement learning to participate. A strong rule-based agent is a great place to start.

If you want to train a neural network, the full repository includes training tools that use Stable-Baselines3 and `sb3-contrib` MaskablePPO.

Train a model:

```bash
python train.py --train --timesteps 20000
```

This trains an RL agent on the competition environment and saves model weights.

Evaluate or render a trained model:

```bash
python train.py --render
```

If your trained model is saved as `sbrp_agent.zip`, rename or copy it to `model.zip` before submitting.

## Reference Baselines

To compare against a simple heuristic baseline, run:

```bash
python baselines.py
```

Use the baseline score as a benchmark to beat.

## Recommended Development Path

1. Run the starter agent locally.
2. Make a simple rule-based improvement, such as choosing the nearest valid stop.
3. Add capacity-aware behavior, such as going to school when the bus is full.
4. Consider fairness by avoiding extremely long student ride times.
5. Compare your score against previous versions.
6. Try reinforcement learning only after your basic agent works reliably.

## Learning Resources

### Reinforcement Learning

- **OpenAI Spinning Up: Introduction to RL**  
  https://spinningup.openai.com/en/latest/spinningup/rl_intro.html

- **Hugging Face Deep RL Course**  
  https://huggingface.co/learn/deep-rl-course/unit0/introduction

- **Sutton and Barto Reinforcement Learning Book**  
  http://incompleteideas.net/book/the-book-2nd.html

- **David Silver's Reinforcement Learning Course**  
  https://www.davidsilver.uk/teaching/

### Python and Machine Learning

- **Python Tutorial**  
  https://docs.python.org/3/tutorial/

- **NumPy Quickstart**  
  https://numpy.org/doc/stable/user/quickstart.html

- **PyTorch Tutorials**  
  https://docs.pytorch.org/tutorials/

- **Stable-Baselines3 Documentation**  
  https://stable-baselines3.readthedocs.io/

### AI-Assisted Coding

- **ChatGPT**  
  https://chatgpt.com/

- **Claude**  
  https://claude.ai/

- **Google Gemini**  
  https://gemini.google.com/

- **GitHub Copilot**  
  https://github.com/features/copilot

- **Cursor**  
  https://cursor.com/

Good prompts to try:

- "Explain this `agent.py` file like I am new to reinforcement learning."
- "Help me design a school bus routing heuristic."
- "How should I use `action_mask` to avoid illegal actions?"
- "Why might my routing agent get a low reward?"
- "Help me compare a nearest-stop strategy with a capacity-aware strategy."

## How to Submit

Once your agent is ready, prepare a zip file to upload to Codabench.

Your zip file should contain only:

- `agent.py` - required
- `model.zip` - optional, only if your agent loads a trained model

The files must be at the root level of the zip file.

Correct:

```text
submission.zip
├── agent.py
└── model.zip
```

Incorrect:

```text
submission.zip
└── participant_starter/
    ├── agent.py
    └── model.zip
```

Important rules:

- Do not include `run_submission.py`, `train.py`, `baselines.py`, or other repository files in your submission.
- Do not include raw map data or graph cache files.
- Do not download external data inside `agent.py` during evaluation.
- Keep your submission zip under 50 MB.
- Make sure `agent.py` imports and runs without errors.

Upload your zip file on the **My Submissions** tab of the Codabench competition page.

## Documentation

For more details, check:

- `HOW_TO_SUBMIT.md` inside the `participant_starter` folder
- The Overview, Evaluation, Data, and Terms tabs on the Codabench competition page

## Contact

Email `machinelearningclubbca@gmail.com` with questions.
