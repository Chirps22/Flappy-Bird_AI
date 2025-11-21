from stable_baselines3 import PPO
from flappybird_env import FlappyBirdEnv
import time

env = FlappyBirdEnv(render=True)

model = PPO.load("models/PPO/PPO_flappy_2500000")

obs = env.reset()
done = False

while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    time.sleep(0.02)

env.close()