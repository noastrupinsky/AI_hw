from collections import deque
from tiebreaker import TieBreaker
import random
class Block:
 
    def __init__(self, x = 0, y = 0):
        self.location = Location(x,y)
        self.f = 0
        self.g = 0
        self.parent = None

    def __eq__(self, other):
        return isinstance(other, Block) and self.location.x == other.location.x and self.location.y == other.location.y
    
    def __lt__(self, other):
        if isinstance(other, Block):
            if(self.f == other.f):
                result = TieBreaker().tieBreaker((self.f, self.g), (other.f, other.g))
                return result
            return self.f < other.f
        return NotImplemented
    
    def __hash__(self):
        return hash((self.location.x, self.location.x))
    
    def get_adjacent_nodes(self, grid):
        x = self.location.x
        y = self.location.y
        grid_size = len(grid)

        neighbors = deque()
        blocked_neighbors = deque()

        if x-1 > -1:
            if grid[x-1][y] == 0:
                 neighbors.append(Block(x-1, y))
            else:   
                blocked_neighbors.append(Location(x-1, y))
        if x+1 < grid_size:
            if grid[x+1][y] == 0:
                neighbors.append(Block(x+1, y))
            else: 
                blocked_neighbors.append(Location(x+1, y))
        if y-1 > -1:
            if grid[x][y-1] == 0:
                neighbors.append(Block(x, y-1))
            else: 
                blocked_neighbors.append(Location(x, y-1))
        if(y+1 < grid_size):
            if grid[x][y+1] == 0:
                neighbors.append(Block(x, y+1))
            else: 
                blocked_neighbors.append(Location(x, y+1))

        random.shuffle(list(neighbors))
        return (deque(neighbors), blocked_neighbors)
    
    def getManhattanDistance(self, target):
        xDiff = abs(self.location.x - target.location.x)
        yDiff = abs(self.location.y - target.location.y)

        return xDiff + yDiff
    


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y