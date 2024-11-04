

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
                tStarForThisCNext += bNext[0] * self.tStar(bNext[1], cNext)
            if tStarForThisCNext < minTStar:
                minTStar = tStarForThisCNext
       
        return minTStar
    
    def getCNextIdeas(self, posB, posC):
        #check if all 8 movements are possible - not walls etc
        cNextIdeas = []
        return cNextIdeas
    
    def getBNextIdeas(self,posB, posC):
        bNextIdeas = []
        #figure out if we're in the 5x5
        #If in 5x5:
            #get manhattanDistanec to posC
            #any place the bull is not allowed to go has probability 0
            #if there are 2 possible places to go, they each get probability 0.5
            #if there is 1 possible place to go it gets probability 1
        
        #If not in 5x5:
            #Any move that isn't hitting the wall or the robot gets equal prob. Those things get prob 0.

        return bNextIdeas