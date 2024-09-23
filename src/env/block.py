
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0 #unblocked
    
    def setStatus(self, status):
        self.status = status
