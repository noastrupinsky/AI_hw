from src.env.block import Block
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
        xDiff = abs(currPos.location.x - target.location.x)
        yDiff = abs(currPos.location.y - target.location.y)

        return xDiff + yDiff
    
    def tieBreaker(self, sucessor1, sucessor2):
        f1, g1 = sucessor1
        f2, g2 = sucessor2

        priorityA = (self.c * f1) - g1
        priorityB = (self.c * f2) - g2

        if priorityA > priorityB:
            return sucessor1
        else:    
            return sucessor2

    def get_adjacent_nodes(self, grid, current_node):
        x = current_node.location.x
        y = current_node.location.y
        neighbors = deque()
        if(x-1 > 0):
            neighbors.append(Block(x-1, y))
        if(x+1<len(grid) - 1):
            neighbors.append(Block(x+1, y))
        if(y-1 > 0):
            neighbors.append(Block(x, y-1))
        if(y+1<len(grid) - 1):
            neighbors.append(Block(x, y-1))
        return neighbors

    def a_star(self, grid, start_node, goal_node):
        open_list = []
        closed_list = deque()
        heapq.heappush(open_list, (0, start_node))
        
        while not (not open_list):
            current_node = heapq.heappop(open_list)
            if current_node == goal_node:
                    break
            closed_list.append(current_node) #whenever claculating g, call updateMaxG for tie breaking
            print(closed_list)
            neighbors = current_node.get_adjacent_nodes(grid)
            for neighbor in neighbors:
               if neighbor in closed_list:
                   continue
               if grid[neighbor.location.x][neighbor.location.y] == 1:
                   neighbor.h = float('inf') 
               else:
                    neighbor.h = neighbor.getManhattanDistance(goal_node)
               neighbor.g = current_node.g + 1 #not sure if this is correct
               if neighbor.location in [already_exists.location for already_exists in open_list]:
                    existing_block = next(node for node in open_list if node.position == neighbor.location)
                    if neighbor.f >= existing_block.f :
                        continue
               if neighbor.location in [already_exists.location for already_exists in closed_list]:
                    existing_block = next(node for node in open_list if node.position == neighbor.location)
                    if neighbor.f >= existing_block.f :
                        continue
               heapq.heappush(open_list, (neighbor.f, neighbor))
                





        

        
        
