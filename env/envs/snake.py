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
            "food": coordinate_space,
            "tail": coordinate_space
        }
        self.table = spaces.Box(low=0, high = 4, shape=(grid_size, grid_size), dtype=int) #nothing = 0,snake = 1,head = 2, fruit = 3
        self.observation_space = spaces.Dict(observation_space)

    def step(self, action):
        done = False
        head_j = self.observation_space["head"]%self.grid_size
        head_i = (self.observation_space["head"]//self.grid_size)%self.grid_size
        tail_j = self.observation_space["tail"]%self.grid_size
        tail_i = (self.observation_space["tail"]//self.grid_size)%self.grid_size
        if action == 0:   #up
            point = [head_i-1, head_j]
            self.observation_space["head"] = self.observation_space["head"] - self.grid_size
        if action == 1:  #down
            point = [head_i+1, head_j]
            self.observation_space["head"] = self.observation_space["head"] + self.grid_size
        if action == 2:  #left
            point = self.table[head_i, head_j-1]
            self.observation_space["head"] = self.observation_space["head"] - 1
        if action == 3:  #right
            point = self.table[head_i, head_j+1]
            self.observation_space["head"] = self.observation_space["head"] + 1
        self.table[head_i, head_j] = 1
        prev = self.table[point[0], point[1]]
        state = prev-2
        if state == 1:
            reward = 2
            fruit_loc_init()
        else:
            self.table[tail_i,tail_j] = 0
            if state == -2:
                reward = 0
            if state == -1:
                reward = -1
                done = True
        self.table[point[0], point[1]] = 2

        if done:
            self.reset()
        info = {}
        return self.table, reward, info

    def reset(self):
        pass

    def render(self, mode="human"):
        pass
