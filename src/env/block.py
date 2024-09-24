
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = self.g + self.h

    def __eq__(self, other):
        return isinstance(other, Block) and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))