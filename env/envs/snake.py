import gym
from gym import spaces


class Snake(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.action_space = spaces.Discrete(4)  # Snake has only 4 possible moves. One in each direction
        coordinate_space = spaces.Discrete(grid_size * grid_size)  # The space for food and head
        grid_space = spaces.MultiBinary([grid_size, grid_size])  # The space for the snake body
        observation_space = {
            "snake": grid_space,
            "head": coordinate_space,
            "food": coordinate_space
        }
        self.observation_space = spaces.Dict(observation_space)

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode="human"):
        pass
