#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import numpy as np
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
import logging
from datetime import datetime

# Import our custom RecSim environment
from recSim_environment import RecommendationEnv

# Set up logging
def setup_logger():
    log_dir = "logs/"
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/training_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

logger = setup_logger()

def make_env():
    """
    Create and wrap the recommendation environment
    """
    def _init():
        # Initialize the environment with appropriate parameters
        env = RecommendationEnv()
        # Wrap the environment with Monitor for logging
        env = Monitor(env)
        return env
    return _init

def train_ppo_model(total_timesteps=100000, save_freq=10000, eval_freq=10000):
    """
    Train a PPO model on the recommendation environment
    
    Args:
        total_timesteps (int): Total number of timesteps to train for
        save_freq (int): Frequency (in timesteps) to save model checkpoints
        eval_freq (int): Frequency (in timesteps) to evaluate the model
    
    Returns:
        model: The trained PPO model
    """
    logger.info("Starting PPO model training")
    
    # Create log and model directories
    log_dir = "logs/"
    model_dir = "models/"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    
    # Create the vectorized environment
    env = DummyVecEnv([make_env()])
    
    # Normalize the environment for better training stability
    env = VecNormalize(env, norm_obs=True, norm_reward=True, clip_obs=10.)
    
    # Define callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=save_freq,
        save_path=f"{model_dir}/checkpoints/",
        name_prefix="ppo_recommendation_model",
        save_vecnormalize=True
    )
    
    # Create a separate environment for evaluation
    eval_env = DummyVecEnv([make_env()])
    eval_env = VecNormalize(
        eval_env,
        norm_obs=True,
        norm_reward=True,
        clip_obs=10.,
        training=False
    )
    
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=f"{model_dir}/best/",
        log_path=log_dir,
        eval_freq=eval_freq,
        deterministic=True,
        render=False
    )
    
    # PPO hyperparameters
    # These can be tuned based on performance
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        clip_range_vf=None,
        ent_coef=0.01,
        vf_coef=0.5,
        max_grad_norm=0.5,
        use_sde=False,
        sde_sample_freq=-1,
        target_kl=None,
        tensorboard_log=f"{log_dir}/tensorboard/",
        verbose=1
    )
    
    # Train the model
    start_time = time.time()
    logger.info(f"Starting training for {total_timesteps} timesteps")
    
    model.learn(
        total_timesteps=total_timesteps,
        callback=[checkpoint_callback, eval_callback]
    )
    
    training_time = time.time() - start_time
    logger.info(f"Training completed in {training_time:.2f} seconds")
    
    # Save the final model
    final_model_path = f"{model_dir}/ppo_recommendation.zip"
    model.save(final_model_path)
    logger.info(f"Final model saved to {final_model_path}")
    
    # Save the VecNormalize statistics
    env_stats_path = f"{model_dir}/vec_normalize_stats.pkl"
    env.save(env_stats_path)
    logger.info(f"Environment normalization statistics saved to {env_stats_path}")
    
    return model, env

def evaluate_model(model, env, n_eval_episodes=10):
    """
    Evaluate the trained model
    
    Args:
        model: Trained PPO model
        env: Environment to evaluate on
        n_eval_episodes: Number of episodes to evaluate
    
    Returns:
        mean_reward: Mean reward across evaluation episodes
        std_reward: Standard deviation of rewards
    """
    logger.info(f"Evaluating model over {n_eval_episodes} episodes")
    
    mean_reward, std_reward = evaluate_policy(
        model, 
        env,
        n_eval_episodes=n_eval_episodes,
        deterministic=True
    )
    
    logger.info(f"Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")
    return mean_reward, std_reward

if __name__ == "__main__":
    # Train the model
    model, env = train_ppo_model(
        total_timesteps=500000,  # Adjust based on your computational resources
        save_freq=50000,
        eval_freq=50000
    )
    
    # Evaluate the trained model
    evaluate_model(model, env, n_eval_episodes=20)
    
    logger.info("Training and evaluation complete!")