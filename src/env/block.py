from collections import deque
class Block:
 
    def __init__(self, x = 0, y = 0):
        self.location = Location(x,y)
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return isinstance(other, Block) and self.location.x == other.location.x and self.location.y == other.location.y
    
    def __lt__(self, other):
        if isinstance(other, Block):
            return self.f < other.f
        return NotImplemented
    
    def __hash__(self):
        return hash((self.location.x, self.location.x))
    
    def get_adjacent_nodes(self, grid):
        x = self.location.x
        y = self.location.y
        neighbors = deque()
        if(x-1 > 0):
            neighbors.append(Block(x-1, y))
        if(x+1<len(grid) - 1):
            neighbors.append(Block(x+1, y))
        if(y-1 > 0):
            neighbors.append(Block(x, y-1))
        if(y+1<len(grid) - 1):
            neighbors.append(Block(x, y+1))
        return neighbors
    
    def getManhattanDistance(self, target):
        xDiff = abs(self.location.x - target.location.x)
        yDiff = abs(self.location.y - target.location.y)

        return xDiff + yDiff

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y