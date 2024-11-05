from game import Location
from collections import deque

class Game:
    
    def __init__(self) -> None:
        pass

    def tStar(self, posB, posC):
        lastMoveBounds = {
        (2, 6), (2, 7), (2, 8), (2, 9),
        (3, 6), (3, 7), (3, 8), (3, 9),
        (4, 6), (4, 7), (4, 8), (4, 9),
        (5, 8), (5, 9), (6, 8), (6, 9),
        (7, 8), (7, 9), (8, 6), (8, 7),
        (8, 8), (8, 9), (9, 6), (9, 7),
        (9, 8), (9, 9), (10, 6), (10, 7),
        (10, 8), (10, 9)
        }
        if posB == (6,6):
            return 0
        if posB == (5,6) & (posC in lastMoveBounds ):
            return 1
        if posB == (4,6) & (posC == (8,6)):
            return 2
        
        cNextIdeas = self.getCNextIdeas(posC, posB)
        minTStar = max

        for cNext in cNextIdeas:
            bNextIdeas = self.getBNextIdeas(posB, cNext) #bNext returns [probability, action]
            tStarForThisCNext = 1
            for bNext in bNextIdeas:
                tStarForThisCNext += bNext[0] * self.tStar(bNext[1], cNext) #potentially prune away rounds of tStar when the probability is 0 anyways
            if tStarForThisCNext < minTStar: #
                minTStar = tStarForThisCNext
       
        return minTStar
    
    def getCNextIdeas(self, posB, posC):
        #check if all 8 movements are possible - not walls etc and that the bull isn't in the way
        cNextIdeas = [Location(posC.x, posC.y-1), Location(posC.x-1, posC.y), Location(posC.x+1, posC.y), Location(posC.x, posC.y+1), Location(posC.x+1, posC.y+1), Location(posC.x-1, posC.y-1), Location(posC.x+1, posC.y-1), Location(posC.x-1, posC.y+1)]
        cNextToReturn = deque()
        for idea in cNextIdeas:
            if (Location.spotAllowed(idea) == 1) & ~(idea.x == posB.x & idea.y == posB.y):
                cNextToReturn.append(idea)
        return cNextToReturn
    
    def getBNextIdeas(self,posB, posC):
        bNextIdeas = [Location(posB.x, posB.y-1), Location(posB.x-1, posB.y), Location(posB.x+1, posB.y)]
        in5x5Status = Location.inThe5by5(posB, posC)
        currentDisance = 0
        if in5x5Status == 1:
            currentDistance = Location.manhattanDistance(posB, posC)
        bNextToReturn = deque()
        
        for idea in bNextIdeas:
            if Location.spotAllowed(idea) == 0:
                bNextToReturn.append([idea, 0])
            elif in5x5Status == 1:
                if Location.manhattanDistance(idea, posC) > currentDistance:
                    bNextToReturn.append([idea, 0])



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
    

        