from env.block import Block
import heapq
from collections import deque

class A_star:
    def __init__(self):
        self.max_g = 0
        self.c = 1
    
    def updateMaxG(self, curr_g):
        self.max_g = max(self.max_g, curr_g)
        self.c = self.max_g + 1

    def getManhattanDistance(self, currPos, target):
        xDiff = abs(currPos.x - target.x)
        yDiff = abs(currPos.y - target.y)

        return xDiff + yDiff
    
    # def tieBreaker(self, sucessor1, sucessor2):
        f1, g1 = sucessor1
        f2, g2 = sucessor2

        priorityA = (self.c * f1) - g1
        priorityB = (self.c * f2) - g2

        if priorityA > priorityB:
            return sucessor1
        else:    
            return sucessor2

    def get_adjacent_nodes(self, current_node):
        x = current_node.x
        y = current_node.y

        return 

    def a_star(self, grid, start_node, goal_node):
        open_list = []
        closed_list = deque()
        heapq.heappush(open_list, start_node)
        
        while not (not open_list):
            current_node = heapq.heappop(open_list)
            if current_node == goal_node:
                    break
            closed_list.append(current_node) #whenever claculating g, call updateMaxG for tie breaking


        

        
        
