from collections import deque
import sys
from grid import Location

class Game:
    
    def __init__(self) -> None:
        pass

    def tStar(self, posB, posC):
   
        if posB == (6,6):
            return 0
 
        cNextIdeas = self.getCNextIdeas(posC, posB)
        minTStar = max

        for cNext in cNextIdeas:
            bNextIdeas = self.getBNextIdeas(posB, cNext) #bNext returns [probability, action]
            tStarForThisCNext = 1
            for bNext in bNextIdeas:
                tStarForThisCNext += self.tStar(bNext, cNext) #potentially prune away rounds of tStar when the probability is 0 anyways
            if tStarForThisCNext < minTStar: #
                minTStar = tStarForThisCNext
       
        return minTStar
    
    def getCNextIdeas(self, posC, posB):
        #check if all 8 movements are possible - not walls etc and that the bull isn't in the way
        cNextIdeas = [Location(posC.x, posC.y-1), Location(posC.x-1, posC.y), Location(posC.x+1, posC.y), Location(posC.x, posC.y+1), Location(posC.x+1, posC.y+1), Location(posC.x-1, posC.y-1), Location(posC.x+1, posC.y-1), Location(posC.x-1, posC.y+1)]
        cNextToReturn = deque()
        for idea in cNextIdeas:
            if Location.spotAllowed(idea) & ~(idea.x == posB.x and idea.y == posB.y):
                cNextToReturn.append(idea)
        return cNextToReturn
    
    def getBNextIdeas(self,posB, posC):
        bNextIdeas = [Location(posB.x, posB.y-1), Location(posB.x-1, posB.y), Location(posB.x+1, posB.y), Location(posB.x, posB.y+1)]
        in5x5Status = Location.inThe5by5(posB, posC)
        # currentDisance = 0
        if in5x5Status:
            currentDistance = Location.manhattanDistance(posB, posC)
            
        potentialIdeas = deque()
        bNextToReturn = deque()
        
        #WIP why do we return ideas that are prob zero - wont that make the recursion tree larger?
        for idea in bNextIdeas:
            if Location.spotAllowed(idea):
                if in5x5Status:
                    if Location.manhattanDistance(idea, posC) < currentDistance:
                        bNextToReturn.append(idea)
                else:
                    bNextToReturn.append(idea)
    
        if len(bNextToReturn) == 0:
            bNextToReturn.append(posB)
        
        #figure out if we're in the 5x5
        #If in 5x5:
            #get manhattanDistanec to posC
            #any place the bull is not allowed to go has probability 0
            #if there are 2 possible places to go, they each get probability 0.5
            #if there is 1 possible place to go it gets probability 1
            #If there's nowhere for the bull to go (likely bc the robot is in the way) then return the current location with a probability of 1.
        
        #If not in 5x5:
            #Any move that isn't hitting the wall or the robot gets equal prob. Those things get prob 0.
        return bNextToReturn
    
if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    game = Game()
    result = game.tStar(Location(0, 0), Location(12, 12))
    print(result)
        