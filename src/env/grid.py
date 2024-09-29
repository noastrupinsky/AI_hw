import random
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from block import Block
import sys
import os
import numpy as np

class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(101)] for _ in range(101)]
        self.unblocked = deque()
        self.start = Block()
        self.target = Block()

    def display_grid(self):
        plt.ioff() 
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.axis('off')  # Turn off the axis
        plt.show()

    def color_path(self, reversedPath):
        plt.ioff()  # Turn off interactive mode
        # Create a copy of the grid to modify for coloring
        color_grid = np.array(self.grid)  # Convert your grid to a NumPy array for easy manipulation

        # Check if reversedPath has nodes
        path_length = len(reversedPath)
        if path_length == 0:
            print("No path to color.")
            return

        # Get the first and last node
        first_node = reversedPath[0]
        last_node = reversedPath[-1]

        # Loop through the reversed path to change the cells
        for index, node in enumerate(reversedPath):
            if node is first_node:
                color_grid[node.location.x, node.location.y] = 3  # Change cell value to 3 for green (first node)
            elif node is last_node:
                color_grid[node.location.x, node.location.y] = 3  # Change cell value to 3 for green (last node)
            else:
                color_grid[node.location.x, node.location.y] = 2  # Change cell value to 2 for red (middle nodes)

        # Define a custom colormap
        cmap = plt.cm.colors.ListedColormap(['white', 'black', 'green', 'red'])  # White for 0, Black for 1, Green for 3, Red for 2

        plt.imshow(color_grid, cmap=cmap, interpolation='nearest')  # Display the modified grid
        plt.axis('off')  # Hide the axis
        plt.colorbar(ticks=[0, 1, 2, 3], label='Cell Values')  # Optional: show a color bar
        plt.show()

        for index, node in enumerate(reversedPath): #done for testing purposes
            if node is first_node:
                color_grid[node.location.x, node.location.y] = 0  # Change cell value to 3 for green (first node)
            elif node is last_node:
                color_grid[node.location.x, node.location.y] = 0  # Change cell value to 3 for green (last node)
            else:
                color_grid[node.location.x, node.location.y] = 0  # Change cell value to 2 for red (middle nodes)


    def init_start(self):
        x_start = random.randint(0,len(self.grid) - 1)
        y_start = random.randint(0,len(self.grid) - 1)
        start_block = Block(x_start, y_start)
        self.grid[x_start][y_start] = 1
        self.unblocked.append(start_block)
        return start_block
    
    def create_maze(self):
        self.start = self.init_start()
        visited = set()
        self.dfs(self.start, visited)
        

    def create_start_and_goal(self):
        start_and_end = random.sample(self.unblocked, 2)
        self.start = start_and_end[0]
        self.target = start_and_end[1]

    def dfs(self, start_block, visited):
        if (start_block in visited) or (start_block.location.x <0) or (start_block.location.y <0) or (start_block.location.x > len(self.grid) - 1) or  (start_block.location.y > len(self.grid) - 1):
            return
      
        visited.add(start_block)

        blockedness = random.choices([0,1], weights = [0.7, 0.3])[0]

        self.grid[start_block.location.x][start_block.location.y] = blockedness

        if blockedness == 0:
            self.unblocked.append(start_block)

        nswe = [(1,0), (0,1), (0,-1), (-1,0)]
        random.shuffle(nswe)

        for change_x, change_y in nswe:
            self.dfs(Block(start_block.location.x+change_x, start_block.location.y+change_y), visited)
        
    def save_grid(self, x):
        folder = "grid_worlds"
        os.makedirs(folder, exist_ok=True)
        file_name = f'grid_{x}.txt'
        file_path = os.path.join(folder, file_name)
        with open(file_path, 'w') as file:
            for row in self.grid:
                file.write(' '.join(map(str, row)) + '\n')

    def get_grid(self, x):
        folder = "grid_worlds"
        file_name = f'grid_{x}.txt'
        file_path = os.path.join(folder, file_name)
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace from the line and check if it's not empty
                stripped_line = line.strip()
                if stripped_line:  # Only process non-empty lines
                    # Split the line into integers and append it as a new row to the grid
                    row = list(map(int, stripped_line.split()))
                    self.grid.append(row)


if __name__ == "__main__":
    sys.setrecursionlimit(10300)
    grid = Grid()
    grid.create_maze() 
    grid.display_grid()
    grid.save_grid(1)
    # grid2 = Grid()
    # grid2.get_grid(1)
    # grid2.display_grid() #when i display it after i take it out of the text file it's weirdly shrunken but same pattern

      



