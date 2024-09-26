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
        heapq.heappush(open_list, start_node)
        
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
               heapq.heappush(open_list, neighbor)
        return closed_list

    def repeated_forward_a_star(self, grid, start_node, goal_node):
        tempGrid = [[0 for _ in range(len(grid))] for _ in range(len(grid))] #create tempGrid
        final_path = deque()
        current_node = start_node
        while current_node is not goal_node: #while we have not reached the goal
            unblocked, blocked = current_node.get_adjacent_nodes(grid)
            for coordinate in blocked: #identify in the tempGrid the neighbors that we know are blocked
                tempGrid[coordinate.location.x][coordinate.location.y] = 1
            a_star_path_end_to_start = self.a_star(tempGrid, current_node, goal_node) #do A* with the info we have

            if not a_star_path_end_to_start: #if there's no path we have no answer
                return
            
            a_star_path_start_to_end = deque() #walk up the tree so that I know what all the nodes are
            while a_star_path_end_to_start:
                a_star_path_start_to_end.append(a_star_path_end_to_start)
                a_star_path_end_to_start = a_star_path_end_to_start.parent
                
            index = len(a_star_path_start_to_end)
            while index > 0: #traverse the path that A* gave us in the right direction
                block = a_star_path_start_to_end[index]
                if block is goal_node:
                    final_path.append(block)
                    return
                if grid[block.location.x][block.location.y] == 1: #if the path encounters an impediment
                    current_node = a_star_path_start_to_end[-1] #set the node that we will do A* on in the next iteration to be the one before the blocked one on the path
                    break
                final_path.append(block)
                index+=1

        return final_path
    
    def repeated_backward_a_star(self, grid, start_node, goal_node):
        tempGrid = [[0 for _ in range(len(grid))] for _ in range(len(grid))] #create tempGrid
        final_path = deque()
        current_node = goal_node
        while current_node is not start_node: #while we have not reached the goal
            unblocked, blocked = current_node.get_adjacent_nodes(grid)
            for coordinate in blocked: #identify in the tempGrid the neighbors that we know are blocked
                tempGrid[coordinate.location.x][coordinate.location.y] = 1
            a_star_path_end_to_start = self.a_star(tempGrid, goal_node, current_node) #do A* with the info we have

            if not a_star_path_end_to_start: #if there's no path we have no answer
                return
            
            while a_star_path_end_to_start:
                if block is start_node:
                    return
                final_path.append(a_star_path_end_to_start)
                a_star_path_end_to_start = a_star_path_end_to_start.parent
            
                #traverse the path that A* gave us
                if current_node is start_node: #first checks the first node independently of the rest. this way we can check the rest in terms of current_node.next so if i find an impediment i know which block comes before it
                    final_path.append(current_node)
                    return
                final_path.append(current_node)
                while current_node.parent: 
                    if grid[current_node.parent.location.x][current_node.parent.location.y] == 1: #if the path encounters an impediment
                        break
                final_path.append(current_node.parent)
                current_node = current_node.parent

        return final_path
        
if __name__ == "__main__":
    grid = [[0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]]
    
    start_node = Block(0, 0)
    goal_node = Block(4, 4)

    astar = A_star()

    tempGrid = [[0 for _ in range(5)] for _ in range(5)]
    path = astar.repeated_forward_a_star(grid, start_node, goal_node)

    for block in path:
        print(block.location.x, block.location.y)
                





        

        
        
