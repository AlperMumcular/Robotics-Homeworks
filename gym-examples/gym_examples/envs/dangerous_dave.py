import gym
from gym import spaces
import pygame
import numpy as np
# from . import main_fun
from typing import TYPE_CHECKING, Optional
from .classes import *
from .functional import *
#x, y = Player.updateLocation()

class DangerousDaveEnv(gym.Env):
    def __init__(self, step_limit, render_mode = None):

        # self.agent = Player()
        # self._agent_location = np.array([0.0, 0.0]).astype(np.float32)

        self.observation_space = spaces.Dict(
            {
                "agent_x": spaces.Box(0,288, shape=(1,), dtype=np.float32),
                "agent_y": spaces.Box(32,144, shape=(1,), dtype=np.float32),
                "trophy_x": spaces.Box(176,176, shape=(1,), dtype=np.float32),
                "trophy_y": spaces.Box(48,48, shape=(1,), dtype=np.float32),
                "door_x": spaces.Box(192,192, shape=(1,), dtype=np.float32),
                "door_y": spaces.Box(144,144, shape=(1,), dtype=np.float32),
            }
        )

        #self.observation_space = spaces.Dict(
        #    {
        #        "agent": spaces.Box(np.array([0.0, 0.0]), np.array([SCREEN_WIDTH-1*1.0, SCREEN_HEIGHT-1*1.0]), shape=(2,), dtype=np.float32),
        #        "target": spaces.Box(np.array([0.0, 0.0]), np.array([SCREEN_WIDTH-1*1.0, SCREEN_HEIGHT-1*1.0]), shape=(2,), dtype=np.float32),
        #        "trophy": spaces.Box(np.array([0.0, 0.0]), np.array([SCREEN_WIDTH-1*1.0, SCREEN_HEIGHT-1*1.0]), shape=(2,), dtype=np.float32),
        #        "trophy_taken": spaces.Box(-0.0, 1.0, shape=(2,), dtype=np.float32),
        #        "jetpack_taken": spaces.Box(-0.0, 1.0, shape=(2,), dtype=np.float32),
        #        "jetpack_duration": spaces.Box(-0.0, 1.0, shape=(2,), dtype=np.float32),
        #    }
        #)

        # We have 4 actions, corresponding to "right", "up", "left", "down", "right"
        self.action_space = spaces.Discrete(10)

        # env constructor variables
        self.render_mode = render_mode
        self.step_limit = step_limit
        self.steps = 0

        # Init tiles
        self.tileset, self.ui_tileset = None, None
        self.game_open = True
        self.game_screen = None

        # Init a player
        self.GamePlayer = Player()

        # Init level and spawner
        self.current_level_number = 1
        self.current_spawner_id = 0

        # Available Keys
        self.movement_keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]
        self.inv_keys = [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT]

        # Game processing
        self.ended_game = False
        self.ended_level = False
        self.Level = Map(self.current_level_number)
        (self.player_position_x, self.player_position_y) = self.Level.initPlayerPositions(self.current_spawner_id, self.GamePlayer)
        self.clock = None
        self.jetpack_ui = False
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        ##Init a player
        self.GamePlayer = Player()

        self.ended_game = False
        self.ended_level = False
        self.Level = Map(self.current_level_number)
        (self.player_position_x, self.player_position_y) = self.Level.initPlayerPositions(self.current_spawner_id, self.GamePlayer)
        self.clock = None

        self.steps = 0
        self.jetpack_ui = False

        observation = {
                "agent_x": 32,
                "agent_y": 144,
                "trophy_x": 176,
                "trophy_y": 48,
                "door_x": 192,
                "door_y": 144,
        }

        info = dict()

        return observation, info

    def step(self, action):
        self.steps+=1
        terminated = False
        oldScore = self.GamePlayer.getScore()
        
        if action == 0: # idle
            key_map = [0, 0, 0, 0]
            self.GamePlayer.movementInput(key_map)
            # print(self.GamePlayer.getCurrentState(), self.GamePlayer.getDirectionX())

        elif action == 1: # up
            key_map = [1, 0, 0, 0]
            self.GamePlayer.movementInput(key_map)
            # print(self.GamePlayer.getCurrentState(), self.GamePlayer.getDirectionX())

        elif action == 2: # left
            key_map = [0, 1, 0, 0]
            self.GamePlayer.movementInput(key_map)
            # print(self.GamePlayer.getCurrentState(), self.GamePlayer.getDirectionX())

        elif action == 3: # right
            key_map = [0, 0, 1, 0]
            self.GamePlayer.movementInput(key_map)
            # print(self.GamePlayer.getCurrentState(), self.GamePlayer.getDirectionX())

        elif action == 4: # down
            key_map = [0, 0, 0, 1]
            self.GamePlayer.movementInput(key_map)
            # print(self.GamePlayer.getCurrentState(), self.GamePlayer.getDirectionX())
            
        elif action == 5: # use jetpack
            if self.jetpack_ui == False and self.GamePlayer.inventory["jetpack"] > 0:
                self.jetpack_ui == True
            else:
                self.jetpack_ui == False

            self.GamePlayer.inventoryInput(0)
            # print(self.GamePlayer.getCurrentState(), self.GamePlayer.getDirectionX())

        
        if self.render_mode == "human":
            self.render()
        else:
            (self.player_position_x, self.player_position_y) = self.GamePlayer.updatePosition(self.player_position_x,
                                                                                    self.player_position_y, self.Level,
                                                                                    SCREEN_HEIGHT)
        
        if self.GamePlayer.getCurrentState() == STATE.ENDMAP:
            terminated = True

        observation = {
                "agent_x": self.player_position_x,
                "agent_y": self.player_position_y,
                "trophy_x": 176,
                "trophy_y": 48,
                "door_x": 192,
                "door_y": 144,
        }

        newScore = self.GamePlayer.getScore()
        reward = newScore - oldScore
        return observation, reward, terminated, self.steps==self.step_limit, dict()

    def render(self):
        if self.game_screen is None:
            pygame.init()
            self.game_screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)

            ##Init tiles
            self.tileset, self.ui_tileset = load_all_tiles()
            self.game_open = True

        if self.clock is None:
            self.clock = pygame.time.Clock()

        if self.game_open:
            # self.GamePlayer = Player()

            ##Init level and spawner
            self.current_level_number = 1
            self.current_spawner_id = 0

            pygame.display.update()
                
            if self.GamePlayer.getCurrentState() != STATE.DESTROY:
                (self.player_position_x, self.player_position_y) = self.GamePlayer.updatePosition(self.player_position_x,
                                                                                    self.player_position_y, self.Level,
                                                                                    self.game_screen.getUnscaledHeight())
                                                                                    

            spawner_pos_x = self.Level.getPlayerSpawnerPosition(self.current_spawner_id)[0]
            self.game_screen.setXPosition(spawner_pos_x - 10, self.Level.getWidth())

            self.game_screen.printMap(self.Level, self.tileset)
            self.game_screen.printPlayer(self.GamePlayer,
                                        self.player_position_x - self.game_screen.getXPositionInPixelsUnscaled(),
                                        self.player_position_y, self.tileset)
            self.game_screen.printOverlays(self.ui_tileset)
            self.game_screen.printUi(self.ui_tileset, self.GamePlayer, self.current_level_number)

            if self.GamePlayer.inventory["jetpack"] > 0 or self.jetpack_ui :
                self.game_screen.updateUiJetpack(self.ui_tileset, self.GamePlayer.inventory["jetpack"])
                
            if self.GamePlayer.inventory["trophy"] == 1:
                self.game_screen.updateUiTrophy(self.ui_tileset)

            self.clock.tick(200)

    def close(self):
        if self.game_screen is not None:
            print("called close :D")
            pygame.quit()
            quit()
