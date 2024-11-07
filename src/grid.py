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
        self.target = Location(6, 6)
        self.bull = Location(0, 0)
        self.robot = Location(12, 12)
        
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
class Location:
    def __init__(self, x, y):
         self.x = x
         self.y = y
    
    @staticmethod
    def spotAllowed(pos):
        if pos.x > 12 | pos.x < 0 | pos.y > 12 | pos.y < 0:
            return False
        if (pos.x, pos.y) == (5,5) or (pos.x, pos.y) == (5,6) or (pos.x, pos.y) == (5,7) or (pos.x, pos.y) == (6,7) or (pos.x, pos.y) == (7,7) or (pos.x, pos.y) == (7,6) or (pos.x, pos.y) == (7,5): #supposed to be the corrall but idk if i got the locations cortect
            return False
        return True
    
    @staticmethod
    def inThe5by5(posB, posC):
        row = abs(posB.x-posC.x)
        col = abs(posB.y-posC.y)
        if (row <= 5) & (col <= 5):
            return True
        return False
    
    @staticmethod
    def manhattanDistance(posB, posC):
        return abs(posB.x-posC.x) + abs(posB.y-posC.y)
    



