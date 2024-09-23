import random

class Grid:
    def _init_(self):
     self.grid = [[0 for _ in range(100)] for _ in range(100)]

    def fill_grid(self):
       x_start = random.randint(0,100)
       y_start = random.randint(0,100)