from grid import Grid
from A_star import A_star
from collections import deque
import sys
import os


class Compare_Forward_Backward:
    sys.setrecursionlimit(10300)

    def same_grid(self):
        path_lengths_forward = 0
        path_lengths_backward = 0
        astar = A_star()
        for i in range(10):
            grid = Grid()
            grid.create_maze()
            grid.create_start_and_goal()
            reversedPath = astar.repeated_forward_a_star(grid, grid.start, grid.target)
            path_lengths_forward += len(reversedPath)
            reversedPath = astar.repeated_backward_a_star(grid, grid.start, grid.target)
            path_lengths_backward += len(reversedPath)

        print("Forward average")
        print(path_lengths_forward/10)
        print("Backward Average")
        print(path_lengths_backward/10)



