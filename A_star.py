from env.block import Block
import heapq
from collections import deque

class A_star:

    def getManhattanDistance(self, currPos, target):
        xDiff = abs(currPos.x - target.x)
        yDiff = abs(currPos.y - target.y)

        return xDiff + yDiff
    
    # def calculateF(self, grid, currPos, target):

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


        

        
        
