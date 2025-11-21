import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from flappybird_env import FlappyBirdEnv

models_dir = "models/PPO"
log_dir = "logs"
os.makedirs(models_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

def make_env():
    return FlappyBirdEnv(render=False)

env = DummyVecEnv([make_env])

model = PPO(
    policy="MlpPolicy",
    env=env,
    verbose=1,
    tensorboard_log=log_dir,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
)

TIMESTEPS = 500_000
for i in range(1, 6):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_dir}/PPO_flappy_{i * TIMESTEPS}")

env.close()
print("Training finished.")