from env.block import Block

class A_star:

    def getManhattanDistance(self, currPos, target):
        xDiff = abs(currPos.x - target.x)
        yDiff = abs(currPos.y - target.y)

        return xDiff + yDiff
    
    def calculateF(self, grid, currPos, target):
        

        
        
