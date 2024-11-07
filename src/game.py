from collections import deque
import sys
from itertools import permutations
from grid import Location

class Game:
    
    def __init__(self) -> None:
        self.minMoves= {}

    def insertMinMoves(self, bull, robot, value):
        # Use a tuple of tuples as the key
        self.minMoves[(bull, robot)] = value
    
    def getStoredMinMoves(self, bull, robot):
        if self.minMoves.get((bull, robot)) == None:
            print("WHY")
        return self.minMoves.get((bull, robot))

    
    def converge(self):
        curr = self.getStoredMinMoves(Location(6, 5), Location(4, 6))
        new = -1
        i = 1
        while not curr == new:
            print(f"iteration: {i}")
            curr = new
            for (bull, robot) in (self.minMoves.keys()):
                # if(bull == Location(6,5) and robot == Location(4,6)):
                self.insertMinMoves(bull, robot, self.tStar(bull, robot))
            new = self.getStoredMinMoves(Location(6, 5), Location(4, 6))
            
            print(self.getStoredMinMoves(Location(6, 5), Location(4, 6)))
            print(" ")
            i = i + 1
            
    
    def initStates(self):   
        states = deque()
        for i in range(13):
            for j in range(13):
                if Location.spotAllowed(Location(i, j)):
                    states.append(Location(i, j))
        
        for bull, robot in permutations(states, 2):
            if (robot == Location(6, 6) and bull == Location(6, 5)) or (robot == Location(6, 5) and bull == Location(6, 4)):
                continue
            if bull != robot:
                self.insertMinMoves(bull, robot, 0)
      


    def tStar(self, posB, posC):
        
        if posB == Location(6, 6):
            return 0

        if (posC == Location(6, 6) and posB == Location(6, 5)) or (posC == Location(6, 5) and posB == Location(6, 4)):
            return sys.maxsize

        robotMoves = self.potentialRobotMoves(posC, posB)
        options = set()
        
        for robotMove in robotMoves:
            
            bullMoves = self.potentialBullMoves(posB, robotMove) 
            
            for bullMove in bullMoves:
                if robotMove == bullMove:
                    continue
                options.add(self.getStoredMinMoves(bullMove, robotMove))
        return 1 + sum(options) / len(options)
            
    
    def potentialRobotMoves(self, posC, posB):

        moves = [Location(posC.x, posC.y-1), Location(posC.x-1, posC.y), Location(posC.x+1, posC.y), Location(posC.x, posC.y+1), Location(posC.x+1, posC.y+1), Location(posC.x-1, posC.y-1), Location(posC.x+1, posC.y-1), Location(posC.x-1, posC.y+1)]
        
        possibleMoves = deque()
        
        for move in moves:
            if Location.spotAllowed(move) and not (move.x == posB.x and move.y == posB.y):
                possibleMoves.append(move)
                
        return possibleMoves
    
    def potentialBullMoves(self, currBull, currRobot):
        moves = [Location(currBull.x, currBull.y-1), Location(currBull.x-1, currBull.y), Location(currBull.x+1, currBull.y), Location(currBull.x, currBull.y+1)]
        
        in5x5Status = Location.inThe5by5(currBull, currRobot)
        
        if in5x5Status:
            currentDistance = Location.manhattanDistance(currBull, currRobot)
            
        possibleMoves = deque()
        
        for move in moves:
            if Location.spotAllowed(move) and Location.comboAllowed(currRobot, move):
                if in5x5Status:
                    distFromRobot = Location.manhattanDistance(move, currRobot)
                    if distFromRobot <= currentDistance:
                        possibleMoves.append(move)
                else:
                    possibleMoves.append(move)
    
        if len(possibleMoves) == 0:
            possibleMoves.append(currBull)

        return possibleMoves
    
if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    game = Game()
    game.initStates()
    game.converge()
    # print(result)
        