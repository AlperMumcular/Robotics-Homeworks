import gym
from gym import spaces
import pygame
import numpy as np
from . import main_fun
from typing import TYPE_CHECKING, Optional
from .classes import *
from .functional import *


#x, y = Player.updateLocation()

class Action(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3
    JETPACK = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8
    IDLE = 9

class DangerousDaveEnv(gym.Env):
    def __init__(self, render_mode: Optional[str] = None):

        self.agent = Player()
        self._agent_location = np.array([0.0, 0.0]).astype(np.float32)


        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(np.array([0.0, 0.0]), np.array([SCREEN_WIDTH-1*1.0, SCREEN_HEIGHT-1*1.0]), shape=(2,), dtype=np.float32),
                "target": spaces.Box(np.array([0.0, 0.0]), np.array([SCREEN_WIDTH-1*1.0, SCREEN_HEIGHT-1*1.0]), shape=(2,), dtype=np.float32),
                "trophy": spaces.Box(np.array([0.0, 0.0]), np.array([SCREEN_WIDTH-1*1.0, SCREEN_HEIGHT-1*1.0]), shape=(2,), dtype=np.float32),
                "trophy_taken": spaces.Box(-0.0, 1.0, shape=(2,), dtype=np.float32),
                "jetpack_taken": spaces.Box(-0.0, 1.0, shape=(2,), dtype=np.float32),
                "jetpack_duration": spaces.Box(-0.0, 1.0, shape=(2,), dtype=np.float32),
            }
        )

        # We have 4 actions, corresponding to "right", "up", "left", "down", "right"
        self.action_space = spaces.Discrete(10)

        
    
    def reset(self, seed=None, options=None):
        pass
    def step(self, action):
        #print(  )
        pass
    def render(self):
        #if self.render_mode == "human":        
        main_fun.main()
        
    def close(self):
        pass     
