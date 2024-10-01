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
        self.grid = [[0 for _ in range(50)] for _ in range(50)]
        self.unblocked = deque()
        self.start = Block()
        self.target = Block()

    def display_grid(self):
        plt.ioff() 
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.axis('off')  # Turn off the axis
        plt.show()
    

    def color_path(self, reversedPath):
        plt.ioff()
        
        color_grid = np.array(self.grid) 

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
                color_grid[node.location.x, node.location.y] = 2  # Change cell value to 3 for green (first node)
            elif node is last_node:
                color_grid[node.location.x, node.location.y] = 0  # Change cell value to 3 for green (last node)
            else:
                color_grid[node.location.x, node.location.y] = 0  # Change cell value to 2 for red (middle nodes)


    def color_multiple_paths(self, path_infos):
        """
        Visualize multiple paths on the grid, coloring:
        - Red for the path
        - Green for the start
        - Yellow for the target
        - Purple for the path
        - Black for blocked
        - White for unblocked

        Args:
        path_infos: List of tuples, where each tuple contains the path and the number of expanded nodes
        Example: [(path1, expanded_nodes1), (path2, expanded_nodes2), ...]
        """
        plt.ioff()  # Turn off interactive mode

        color_grid = np.array(self.grid) 
    
    def color_paths_in_two_sections(self, paths_large_g, paths_small_g, titles_large_g, titles_small_g):
        """
        Visualize multiple paths in two sections:
        - One section for prioritizing large G
        - Another for prioritizing small G
        
        Args:
        paths_large_g: List of tuples (path, expanded_nodes) for large G prioritization.
        paths_small_g: List of tuples (path, expanded_nodes) for small G prioritization.
        titles_large_g: List of titles for each subplot in the large G section.
        titles_small_g: List of titles for each subplot in the small G section.
        """
        plt.ioff()  # Turn off interactive mode

        # Number of paths for each section
        num_large_g = len(paths_large_g)
        num_small_g = len(paths_small_g)

        # Create a figure with subplots: 2 rows for 2 sections
        fig, axes = plt.subplots(2, max(num_large_g, num_small_g), figsize=(12, 10))

        # Set main titles for each section
        fig.suptitle("Path Visualizations", fontsize=16)
        
        # Helper function to color the grid based on a single path
        def color_grid_with_path(color_grid, path):
            """Helper function to color the grid based on the given path."""
            if not path:
                print("No path to color.")
                return color_grid

            # Color the path (excluding the start and end nodes)
            for node in list(path)[1:-1]:  # Everything except the first and last nodes
                color_grid[node.location.x, node.location.y] = 2  # Red for path

            # Mark the start and target points after coloring the path
            start_node = path[0]  # Start node
            end_node = path[-1]   # End node
            color_grid[start_node.location.x, start_node.location.y] = 3  # Green for start
            color_grid[end_node.location.x, end_node.location.y] = 4      # Yellow for target

            return color_grid

        # Loop over paths for large G prioritization
        for i, (path, expanded_nodes) in enumerate(paths_large_g):
            color_grid = np.array(self.grid)  # Copy of the grid for each path
            color_grid = color_grid_with_path(color_grid, path)

            # Define a custom colormap
            cmap = plt.cm.colors.ListedColormap(['white', 'black', 'red', 'green', 'yellow'])

            # Plot the grid for the current path in the first section
            im = axes[0, i].imshow(color_grid, cmap=cmap, interpolation='nearest')
            axes[0, i].axis('off')  # Hide axes

            # Create title with expanded nodes count
            axes[0, i].set_title(f"{titles_large_g[i]}\nExpanded Nodes: {expanded_nodes}", fontsize=12)

            # Optional: Add a colorbar for each subplot
            fig.colorbar(im, ax=axes[0, i], ticks=[0, 1, 2, 3, 4], label='Grid Color Scheme')

        # Set main title for large G section
        axes[0, 0].set_ylabel("Prioritize Large G", fontsize=14)

        # Loop over paths for small G prioritization
        for i, (path, expanded_nodes) in enumerate(paths_small_g):
            color_grid = np.array(self.grid)  # Copy of the grid for each path
            color_grid = color_grid_with_path(color_grid, path)

            # Define a custom colormap
            cmap = plt.cm.colors.ListedColormap(['white', 'black', 'red', 'green', 'yellow'])

            # Plot the grid for the current path in the second section
            im = axes[1, i].imshow(color_grid, cmap=cmap, interpolation='nearest')
            axes[1, i].axis('off')  # Hide axes

            # Create title with expanded nodes count
            axes[1, i].set_title(f"{titles_small_g[i]}\nExpanded Nodes: {expanded_nodes}", fontsize=12)

            # Optional: Add a colorbar for each subplot
            fig.colorbar(im, ax=axes[1, i], ticks=[0, 1, 2, 3, 4], label='Grid Color Scheme')

        # Set main title for small G section
        axes[1, 0].set_ylabel("Prioritize Small G", fontsize=14)

        # Adjust layout for the figure
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Make room for the main title
        plt.show()
        
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
        self.grid = []
        with open(file_path, 'r') as file:
            for index_x, line in enumerate(file):
                # Strip whitespace from the line and check if it's not empty
                stripped_line = line.strip()
                if stripped_line:  # Only process non-empty lines
                    # Split the line into integers and append it as a new row to the grid
                    row = list(map(int, stripped_line.split()))
                    for index_y, block in enumerate(row):
                        if block == 0:
                            self.unblocked.append(Block(index_x, index_y))
                    self.grid.append(row)
        


# if __name__ == "__main__":
#     sys.setrecursionlimit(10300)
#     grid = Grid()
#     grid.create_maze() 
#     grid.display_grid()
#     grid.save_grid(1)
    # grid2 = Grid()
    # grid2.get_grid(1)
    # grid2.display_grid() #when i display it after i take it out of the text file it's weirdly shrunken but same pattern

      



