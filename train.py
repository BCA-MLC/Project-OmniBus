import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import argparse
from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableMultiInputActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sbrp_env.env import HackensackSBRPOptimizationEnv

def mask_fn(env: HackensackSBRPOptimizationEnv):
    return env.valid_action_mask()

def make_env(render_mode=None):
    env = HackensackSBRPOptimizationEnv(render_mode=render_mode)
    env = ActionMasker(env, mask_fn)
    return env

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true", help="Train the model")
    parser.add_argument("--timesteps", type=int, default=10000, help="Timesteps to train")
    parser.add_argument("--render", action="store_true", help="Render the environment during execution")
    parser.add_argument("--model-path", type=str, default="sbrp_agent.zip", help="Path to save/load model")
    args = parser.parse_args()

    render_mode = "human" if args.render else None

    if args.train:
        print("Initializing environment for training...")
        env = make_env(render_mode=render_mode)
        
        print("Initializing MaskablePPO agent...")
        model = MaskablePPO(MaskableMultiInputActorCriticPolicy, env, verbose=1, learning_rate=3e-4)
        
        print(f"Training for {args.timesteps} timesteps...")
        model.learn(total_timesteps=args.timesteps)
        
        model.save(args.model_path)
        print(f"Model saved to {args.model_path}")
        env.close()
    else:
        print("Loading model for inference...")
        if not os.path.exists(args.model_path):
            print(f"Error: Model file {args.model_path} not found. Please train first.")
            exit(1)
            
        env = make_env(render_mode=render_mode)
        model = MaskablePPO.load(args.model_path, env=env)
        
        obs, info = env.reset()
        done = False
        total_reward = 0
        steps = 0
        
        print("Starting evaluation...")
        while not done:
            action, _states = model.predict(obs, action_masks=env.unwrapped.valid_action_mask(), deterministic=True)
            obs, reward, done, truncated, info = env.step(action)
            total_reward += reward
            steps += 1
            
        print(f"Episode finished in {steps} steps with total reward: {total_reward}")
        env.close()
