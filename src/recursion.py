from collections import deque
import sys
from grid import Location

class Game:
    
    def __init__(self) -> None:
        self.hash_table = {}
        self.visited = set()
        # self.options = set()
        # pass
    def insertTStar(self, coord1, coord2, value):
        # Use a tuple of tuples as the key
        self.hash_table[(coord1, coord2)] = value
    
    def isKnownTStar(self, coord1, coord2):
        return (coord1, coord2) in self.hash_table
    
    def getStoredTStar(self, coord1, coord2):
        return self.hash_table.get((coord1, coord2), None)
    
    def insertVisited(self, coord1, coord2):
        self.visited.add((coord1, coord2))
        
    def isVisited(self, coord1, coord2):
        return (coord1, coord2) in self.visited
    
    # def insertOption(self, value):
    #     self.options.add(value)
    
    # def resetOptions(self):
    #     self.options.clear()
    
    # def findMin(self):
    #     return min(self.options)

    def tStar(self, posB, posC):
   
        if posB.x == 6 and posB.y == 6:
            return 0
        
        self.insertVisited((posC.x, posC.y),(posB.x, posB.y))
 
        cNextIdeas = self.getCNextIdeas(posC, posB)
        # self.resetOptions()
        options = set()
        options.add(sys.maxsize)
        for cNext in cNextIdeas:
            bNextIdeas = self.getBNextIdeas(posB, cNext) 
            for bNext in bNextIdeas:
                tStarValue = 0
                
                if self.isVisited((cNext.x, cNext.y),(bNext.x, bNext.y)):
                    continue
                if(cNext.x == bNext.x and cNext.y == bNext.y):
                    continue
                
                if(self.isKnownTStar((cNext.x, cNext.y),(bNext.x, bNext.y))):
                    tStarValue = self.getStoredTStar((cNext.x, cNext.y),(bNext.x, bNext.y))
                else:
                    tStarValue = self.tStar(bNext, cNext)
                    self.insertTStar((cNext.x, cNext.y),(bNext.x, bNext.y), tStarValue)
                    
                # print(tStarValue)
                options.add(tStarValue)
       
        return 1 + min(options)
    
    def getCNextIdeas(self, posC, posB):
        #check if all 8 movements are possible - not walls etc and that the bull isn't in the way
        cNextIdeas = [Location(posC.x, posC.y-1), Location(posC.x-1, posC.y), Location(posC.x+1, posC.y), Location(posC.x, posC.y+1), Location(posC.x+1, posC.y+1), Location(posC.x-1, posC.y-1), Location(posC.x+1, posC.y-1), Location(posC.x-1, posC.y+1)]
        cNextToReturn = deque()
        for idea in cNextIdeas:
            if Location.spotAllowed(idea) and not (idea.x == posB.x and idea.y == posB.y):
                cNextToReturn.append(idea)
        return cNextToReturn
    
    def getBNextIdeas(self,posB, posC):
        bNextIdeas = [Location(posB.x, posB.y-1), Location(posB.x-1, posB.y), Location(posB.x+1, posB.y), Location(posB.x, posB.y+1)]
        in5x5Status = Location.inThe5by5(posB, posC)
        # currentDisance = 0
        if in5x5Status:
            currentDistance = Location.manhattanDistance(posB, posC)
            
        # potentialIdeas = deque()
        bNextToReturn = deque()
        
        #WIP why do we return ideas that are prob zero - wont that make the recursion tree larger?
        for idea in bNextIdeas:
            if Location.spotAllowed(idea):
                if in5x5Status:
                    distFromRobot = Location.manhattanDistance(idea, posC)
                    if distFromRobot <= currentDistance:
                        bNextToReturn.append(idea)
                else:
                    bNextToReturn.append(idea)
    
        if len(bNextToReturn) == 0:
            bNextToReturn.append(posB)

        return bNextToReturn
    
if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    game = Game()
    result = game.tStar(Location(0, 0), Location(12, 12))
    print(result)
        