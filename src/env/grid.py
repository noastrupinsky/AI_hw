import random
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from block import Block
import sys

class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(101)] for _ in range(101)]
        self.unblocked = deque()

    def display_grid(self):
        # for row in self.grid:
        #     print(' '.join(map(str, row)))
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.axis('off')  # Turn off the axis
        plt.show()

    def init_start(self):
        x_start = random.randint(0,len(self.grid) - 1)
        y_start = random.randint(0,len(self.grid) - 1)
        start_block = Block(x_start, y_start)
        self.grid[x_start][y_start] = 1
        self.unblocked.append(start_block)
        return start_block
    
    def create_maze(self):
        start = self.init_start()
        visited = set()
        self.dfs(start, visited)

    def dfs(self, start_block, visited):
        if (start_block in visited) or (start_block.x <0) or (start_block.y <0) or (start_block.x > len(self.grid) - 1) or  (start_block.y > len(self.grid) - 1):
            return
      
        visited.add(start_block)

        blockedness = random.choices([0,1], weights = [0.7, 0.3])[0]

        self.grid[start_block.x][start_block.y] = blockedness

        if blockedness == 0:
            self.unblocked.append(start_block)

        nswe = [(1,0), (0,1), (0,-1), (-1,0)]
        random.shuffle(nswe)

        for change_x, change_y in nswe:
            self.dfs(Block(start_block.x+change_x, start_block.y+change_y), visited)
        
if __name__ == "__main__":
    sys.setrecursionlimit(10201)
    grid = Grid()
    grid.create_maze()            
    grid.display_grid()    



