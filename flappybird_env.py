import gym
from gym import spaces
import numpy as np
import random
import pygame


class FlappyBirdEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render=False):
        super().__init__()

        self.gravity = 0.5
        self.jump_strength = -8
        self.pipe_gap = 150
        self.pipe_width = 80
        self.pipe_distance = 200
        self.render_enabled = render

        self.screen_width = 400
        self.screen_height = 600

        # Bird state
        self.bird_x = 60
        self.bird_y = self.screen_height / 2
        self.bird_velocity = 0

        # Pipe state
        self.pipe_x = self.screen_width
        self.pipe_height = random.randint(100, 400)

        self.action_space = spaces.Discrete(2)

        low = np.array([0, -20, 0, 0], dtype=np.float32)
        high = np.array([self.screen_height, 20, self.screen_width, self.screen_height], dtype=np.float32)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        # Rendering
        self.win = None
        self.clock = pygame.time.Clock()

        self.score = 0

    def reset(self):
        self.bird_y = self.screen_height / 2
        self.bird_velocity = 0
        self.pipe_x = self.screen_width
        self.pipe_height = random.randint(100, 400)
        self.score = 0

        return np.array([self.bird_y, self.bird_velocity, self.pipe_x, self.pipe_height], dtype=np.float32)

    def step(self, action):
        # Jump
        if action == 1:
            self.bird_velocity = self.jump_strength

        # Physics
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity
        self.pipe_x -= 3

        reward = 0.1
        done = False

        # Passed pipe
        if self.pipe_x < -self.pipe_width:
            self.pipe_x = self.screen_width
            self.pipe_height = random.randint(100, 400)
            self.score += 1
            reward += 1.0

        # Collision
        collided = (
            self.bird_y < 0
            or self.bird_y > self.screen_height
            or (
                self.pipe_x < self.bird_x + 25 < self.pipe_x + self.pipe_width
                and not (self.pipe_height < self.bird_y < self.pipe_height + self.pipe_gap)
            )
        )

        if collided:
            done = True
            reward = -5

        obs = np.array([self.bird_y, self.bird_velocity, self.pipe_x, self.pipe_height], dtype=np.float32)
        return obs, reward, done, {}

    def render(self):
        if not self.render_enabled:
            return

        if self.win is None:
            pygame.init()
            self.win = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.win.fill((135, 206, 235))

        pygame.draw.rect(self.win, (255, 255, 0), (self.bird_x, self.bird_y, 40, 30))
        pygame.draw.rect(self.win, (0, 200, 0), (self.pipe_x, 0, self.pipe_width, self.pipe_height))
        pygame.draw.rect(
            self.win, (0, 200, 0),
            (self.pipe_x, self.pipe_height + self.pipe_gap, self.pipe_width,
             self.screen_height - (self.pipe_height + self.pipe_gap))
        )

        pygame.display.update()
        self.clock.tick(30)

    def close(self):
        if self.win:
            pygame.quit()