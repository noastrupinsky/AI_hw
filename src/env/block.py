
class Block:
    def __init__(self, x, y):
        self.location = Location(x,y)
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent

    def __eq__(self, other):
        return isinstance(other, Block) and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y