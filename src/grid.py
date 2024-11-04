from collections import deque
import matplotlib.pyplot as plt
import numpy as np
class Grid:
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def __init__(self):
        self.target = (6, 6)
        self.bull = (0, 0)
        self.robot = (12, 12)
        
    def displayGrid(self):
        fig, ax = plt.subplots()
        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (i, j) == self.bull:
                    color = 'red'  # bull location
                elif (i, j) == self.robot:
                    color = 'blue'  # robot location
                elif (i, j) == self.target:
                    color = 'green'  # target location
                elif self.grid[i][j] == 1:
                    color = 'black'  # obstacles
                else:
                    color = 'white'  # empty space
                
                rect = plt.Rectangle((j, len(self.grid) - i - 1), 1, 1, facecolor=color)
                ax.add_patch(rect)
                
        ax.set_xlim(0, len(self.grid[0]))
        ax.set_ylim(0, len(self.grid))
        ax.set_xticks(np.arange(0, len(self.grid[0]), 1))
        ax.set_yticks(np.arange(0, len(self.grid), 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(True)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
            
if __name__ == "__main__":
    grid = Grid()
    grid.displayGrid()


