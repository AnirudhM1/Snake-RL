import random
import numpy as np
import gym
from gym import spaces
import pygame
import time
class Snake(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}
    initial_length = 2

    def __init__(self, grid_size):
        self.length = 2
        pygame.init()
        self.surface = pygame.display.set_mode((grid_size*10,grid_size*10))
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
        self.snake = []
    def step(self, action: int):
        head_j = self.head % self.grid_size
        head_i = (self.head // self.grid_size) % self.grid_size
        tail_i, tail_j = self._findTail()
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
            self.state[head_i][head_j] = 1
            self.state[point[0]][point[1]] = 2
            self.snake = [self.head] + self.snake
            if self.head == self.food:  # Snake has eaten the food
                self.food = self._getRandomFoodLocation()  # Updating the food location
                self.state[self.food // self.grid_size][self.food % self.grid_size] = 3
                self.length+=1
            else:  # Snake has not eaten the food
                self.snake = self.snake[:-1]
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
    def _findTail(self):
        return self.snake[-1] // self.grid_size, self.snake[-1] % self.grid_size

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

    # Get random start location for the game
    def _getRandomHeadLocation(self):
        return (self.grid_size * self.grid_size) // 2

    def reset(self):
        self.surface.fill((0, 0, 0))
        self.state = np.zeros(shape=(self.grid_size, self.grid_size), dtype=int)
        self.head = self._getRandomHeadLocation()
        self.state[self.head // self.grid_size][self.head % self.grid_size] = 2
        self.state[(self.head // self.grid_size) + 1][self.head % self.grid_size] = 1
        self.snake = [self.head, self.head + self.grid_size]
        self.food = self._getRandomFoodLocation()
        self.state[self.food // self.grid_size][self.food % self.grid_size] = 3
        return self.state

    def render(self, mode="human"):
        pass


snake = Snake(grid_size=10)
snake.reset()
while True:
    snake.surface.fill((0, 0, 0))
    for event in pygame.event.get():
           
          # Condition becomes true when keyboard is pressed   
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DOWN:
                action = 1

            if event.key == pygame.K_UP:
                action = 0

            if event.key == pygame.K_LEFT:
                action = 2

            if event.key == pygame.K_RIGHT:
                action = 3
            _,_,done,_ = snake.step(action)
            if done:
                snake.reset()
        if event.type == pygame.QUIT:
            pygame.quit()
    for i in range(snake.grid_size):
        for j in range(snake.grid_size):
            if snake.state[j][i] == 1:
                pygame.draw.rect(snake.surface, (0,255,0), (i*10,j*10,10,10))
            elif snake.state[j][i] == 2:
                pygame.draw.rect(snake.surface, (255,255,51), (i*10,j*10,10,10))
            elif snake.state[j][i] == 3:
                pygame.draw.rect(snake.surface, (255,0,0), (i*10,j*10,10,10))
    pygame.display.update()