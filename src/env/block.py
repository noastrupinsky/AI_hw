
class Block:
    def __init__(self, x, y):
        self.location = Location(x,y)
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return isinstance(other, Block) and self.location.x == other.location.x and self.location.y == other.location.y
    
    def __hash__(self):
        return hash((self.location.x, self.location.x))

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y