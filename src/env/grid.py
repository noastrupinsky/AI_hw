import random
from collections import deque
from block import Block

class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(5)] for _ in range(5)]
        self.unblocked = deque()


    def init_start(self):
        x_start = random.randint(0,5)
        y_start = random.randint(0,5)
        start_block = Block(x_start, y_start)
        self.grid[x_start][y_start] = 1
        self.unblocked.append(start_block)
        return start_block
    
    def create_maze(self):
        start = self.init_start()
        visited = deque()
        print(f"start: ({start.x}, {start.y})")
        self.dfs(start, visited)
        # for row in self.grid:
        #     print(' '.join(map(str, row)))

    def dfs(self, start_block, visited):

        if (start_block in visited) or (start_block.x <0) or (start_block.y <0) or (start_block.x > 100) or  (start_block.y > 100):
            return
        if start_block in visited:
            print(f"here")
            print(start_block.x, start_block.y)
        
        print(f"Visiting: ({start_block.x}, {start_block.y})")
        visited.append(start_block)
        # for bl in visited:
        #     print(bl.x, bl.y)

        blockedness = random.choices([0,1], weights = [0.7, 0.3])[0]

        self.grid[start_block.x][start_block.y] = blockedness

        if blockedness == 0:
            self.unblocked.append(start_block)

        nswe = [(1,0), (0,1), (0,-1), (-1,0)]
        random.shuffle(nswe)

        for change_x, change_y in nswe:
            self.dfs(Block(start_block.x+change_x, start_block.y+change_y), visited)
        
if __name__ == "__main__":
    grid = Grid()
    grid.create_maze()            
        



