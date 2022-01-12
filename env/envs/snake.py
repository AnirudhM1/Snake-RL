import random
import gym
from gym import spaces


class Snake(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.action_space = spaces.Discrete(4)  # Snake has only 4 possible moves. One in each direction
        # coordinate_space = spaces.Discrete(grid_size * grid_size)  # The space for food and head
        # grid_space = spaces.MultiBinary([grid_size, grid_size])  # The space for the snake body
        # observation_space = {
        #     "snake": grid_space,
        #     "head": coordinate_space,
        #     "food": coordinate_space,
        #     "tail": coordinate_space
        # }
        # self.observation_space = spaces.Dict(observation_space)

        self.observation_space = spaces.Box(low=0, high=4, shape=(grid_size, grid_size),
                                            dtype=int)  # nothing = 0,snake = 1,head = 2, fruit = 3
        self.head = None
        self.tail = None
        self.food = None
        self.state = None

    def step(self, action):
        head_j = self.head % self.grid_size
        head_i = (self.head // self.grid_size) % self.grid_size
        tail_i, tail_j = self._findTail([-1, -1], [head_i, head_j])
        self.tail = tail_i * self.grid_size + tail_j

        if action == 0:  # up
            point = [head_i - 1, head_j]
            self.head = self.head - self.grid_size
        elif action == 1:  # down
            point = [head_i + 1, head_j]
            self.head = self.head + self.grid_size
        elif action == 2:  # left
            point = [head_i, head_j - 1]
            self.head = self.head - 1
        elif action == 3:  # right
            point = [head_i, head_j + 1]
            self.head = self.head + 1
        else:
            raise Exception(f'Invalid action: {action}')

        done = self._isGameOver(point)
        reward = self._getReward()

        if not done:  # Update the state
            self.state[point[0]][point[1]] = 2
            self.state[head_i][head_j] = 1
            if self.head == self.food:  # Snake has eaten the food
                self.food = self._getRandomFoodLocation()  # Updating the food location
            else:  # Snake has not eaten the food
                self.state[tail_i][tail_j] = 0

        return self.state, reward, done, {}

    # Reward model
    def _getReward(self):
        if self.head == self.food:
            return 1
        else:
            return 0

    # Check crash
    def _isGameOver(self, point):
        # check crash against the wall
        if not self._check(point):
            return True
        # check crash against body
        if self.head != self.tail:
            if self.state[point[0]][point[1]] == 1:
                return True
        return False

    # Find the tail of the snake
    def _findTail(self, prev, current):
        up = [current[0]-1, current[1]]
        down = [current[0]+1, current[1]]
        left = [current[0], current[1]-1]
        right = [current[0], current[1]+1]

        for next_sqr in [up, down, left, right]:
            if (next_sqr != prev) and self._check(next_sqr) and self.state[next_sqr[0]][next_sqr[1]] == 1:
                return self._findTail(current, next_sqr)
        return current

    # Checks if the coordinate is within the grid
    def _check(self, coords):
        return 0 <= coords[0] < self.grid_size and 0 <= coords[1] < self.grid_size

    def _getRandomFoodLocation(self):
        snake = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.state[i][j] == 1 != 0:
                    snake.append(i*self.grid_size + j)
        return random.choice(list(set([x for x in range(0, self.grid_size*self.grid_size)]) - set(snake)))

    def reset(self):
        pass

    def render(self, mode="human"):
        pass
