import gym
from gym import spaces
import pygame
import numpy as np
from . import main_fun
from typing import TYPE_CHECKING, Optional

class DangerousDaveEnv(gym.Env):
    def __init__(self, render_mode: Optional[str] = None):
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, 5 - 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, 5 - 1, shape=(2,), dtype=int),
            }
        )

        # We have 4 actions, corresponding to "right", "up", "left", "down", "right"
        self.action_space = spaces.Discrete(4)
    
    def reset(self, seed=None, options=None):
        pass
    def step(self, action):
        pass
    def render(self):
        #if self.render_mode == "human":
        main_fun.main()
    def close(self):
        pass     
