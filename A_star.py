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
    
    def tieBreaker(self, sucessor1, sucessor2):
        f1, g1 = sucessor1
        f2, g2 = sucessor2

        priorityA = (self.c * f1) - g1
        priorityB = (self.c * f2) - g2

        if priorityA > priorityB:
            return sucessor1
        else:    
            return sucessor2

    def a_star(self, grid, start_node, goal_node):
        open_list = []
        closed_list = set()
        heapq.heappush(open_list, (0, start_node))
        
        while not (not open_list):
            current_node = heapq.heappop(open_list)
            current_node = current_node[1]
            if current_node == goal_node:
                    break
            closed_list.add(current_node) #whenever claculating g, call updateMaxG for tie breaking
            neighbors = current_node.get_adjacent_nodes(grid)
            for neighbor in neighbors:
               if neighbor in closed_list:
                   continue
               if grid[neighbor.location.x][neighbor.location.y] == 1:
                   neighbor.h = float('inf')
                   continue
               else:
                    neighbor.h = neighbor.getManhattanDistance(goal_node)
               neighbor.g = current_node.g + 1 #not sure if this is correct
               neighbor.f = neighbor.g + neighbor.h
               if neighbor.location in [already_exists[1].location for already_exists in open_list]:
                    existing_block = next(already_exists for already_exists in open_list if already_exists.y.location == neighbor.location)
                    if neighbor.f >= existing_block[1].f :
                        continue
               if neighbor.location in [already_exists.location for already_exists in closed_list]:
                    existing_block = next(node for node in open_list if node.position == neighbor.location)
                    if neighbor.f >= existing_block.f :
                        continue
               heapq.heappush(open_list, (neighbor.f, neighbor))

        return closed_list

if __name__ == "__main__":
    grid = [[0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]]
    
    start_node = Block(0, 0)
    goal_node = Block(4, 4)

    astar = A_star()
    path = astar.a_star(grid, start_node, goal_node)

    for block in path:
        print(block.location.x, block.location.y)
                





        

        
        
