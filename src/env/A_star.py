from block import Block
from grid import Grid
import heapq
from collections import deque
from tiebreaker import TieBreaker
import sys

expanded_nodes = 0

class A_star:
    f_lookup_table = {}
    
    def a_star(self, temp_grid, start_node, goal_node):
        
        open_list = [] 
        closed_list = deque()

    
        heapq.heappush(open_list, start_node) #add start to open list
        start_node_h = A_star.f_lookup_table[start_node][2] if A_star.f_lookup_table[start_node]  else start_node.getManhattanDistance(goal_node)
        A_star.f_lookup_table[start_node] = (start_node_h, 0, start_node_h)
        start_node.f = start_node_h
        
        while open_list:
            current_node = heapq.heappop(open_list) #pop off min value from the heap
            global expanded_nodes
            expanded_nodes+=1 #to count the number of expanded nodes
            closed_list.append(current_node) #add to path

            if current_node == goal_node:
                break

            
            neighbors, blocked_neighbors = current_node.get_adjacent_nodes(temp_grid) #pass in the grid size so that we can check that we arent "overflowing"

            #the neighbors only include possible actions (already pruned)
            for neighbor in neighbors:
                neighbor.parent = current_node
                f_current, g_current, h_current = A_star.f_lookup_table[current_node]

                neighbor_h =  A_star.f_lookup_table[neighbor][2] if A_star.f_lookup_table[neighbor]  else neighbor.getManhattanDistance(goal_node)  #set huristic
                neighbor.g = g_current + 1 
                TieBreaker().updateMaxG(neighbor.g)
                neighbor.f = neighbor.g + neighbor_h


                if neighbor in open_list:
                    if A_star.f_lookup_table[neighbor][0] <= neighbor.f:
                        continue
                    else:
                        open_list.remove(neighbor)
                        
                if neighbor in closed_list:
                   if A_star.f_lookup_table[neighbor][0] <= neighbor.f:
                    continue
                   else:
                    closed_list.remove(neighbor)
                
                
                heapq.heappush(open_list, neighbor)
                A_star.f_lookup_table[neighbor] = (neighbor.f, neighbor.g, neighbor_h)

        return closed_list

    def repeated_forward_a_star(self, grid, start_node, goal_node):
        tempGrid = [[0 for _ in range(len(grid.grid))] for _ in range(len(grid.grid))] #create tempGrid
        final_path = deque()
        final_path.append(start_node)
        current_node = start_node
        while current_node is not goal_node: #while we have not reached the goal
            unblocked, blocked = current_node.get_adjacent_nodes(grid.grid)
            for coordinate in blocked: #identify in the tempGrid the neighbors that we know are blocked
                tempGrid[coordinate.x][coordinate.y] = 1
                
            path = self.a_star(tempGrid, current_node, goal_node) #do A* with the info we have

            if goal_node not in path: #if there's no path we have no answer
                print("No path")
                return
            
            endNode = path.pop()
            
            reversedPath = deque()
            while endNode:
                reversedPath.append(endNode)
                endNode = endNode.parent
        
            for node in path:
                node.parent = None
                
            index = len(reversedPath)
            while index > 0: #traverse the path that A* gave us in the right direction
                block = reversedPath[index-1]
                if block == goal_node:
                    final_path.append(block)
                    return final_path
                if grid.grid[block.location.x][block.location.y] == 1: #if the path encounters an impediment
                    current_node = reversedPath[index] #set the node that we will do A* on in the next iteration to be the one before the blocked one on the path
                    reversedPath.clear()
                    break
                if block != current_node:
                    unblocked_neighbor, blocked_neighbor = block.get_adjacent_nodes(grid.grid) #I added this so that the grid is updated even when the agent doesn't bump into stuff
                    for coordinate in blocked_neighbor: #identify in the tempGrid the neighbors that we know are blocked
                        tempGrid[coordinate.x][coordinate.y] = 1
                    final_path.append(block)
                index-=1

        return final_path
    
    def repeated_backward_a_star(self, grid, start_node, goal_node):
        tempGrid = [[0 for _ in range(len(grid.grid))] for _ in range(len(grid.grid))] #create tempGrid
        final_path = deque()
        final_path.append(start_node)
        current_node = start_node
        while current_node is not goal_node: #while we have not reached the goal
            unblocked, blocked = current_node.get_adjacent_nodes(grid.grid)
            for coordinate in blocked: #identify in the tempGrid the neighbors that we know are blocked
                tempGrid[coordinate.x][coordinate.y] = 1
            path = self.a_star(tempGrid, goal_node, current_node) #do A* with the info we have

            if current_node not in path: #if there's no path we have no answer
                print("No path")
                return
            
            endNode = path.pop()
            
            reversedPath = deque()
            while endNode:
                reversedPath.append(endNode)
                endNode = endNode.parent
        
            for node in path:
                node.parent = None
                
            index = 0 
            end = len(reversedPath)
            while index < end: #traverse the path that A* gave us in the right direction
                block = reversedPath[index]
                if block == goal_node:
                    final_path.append(block)
                    return final_path
                if grid.grid[block.location.x][block.location.y] == 1: #if the path encounters an impediment
                    current_node = reversedPath[index-1] #set the node that we will do A* on in the next iteration to be the one before the blocked one on the path
                    reversedPath.clear()
                    break
                if block != current_node:
                    unblocked_neighbor, blocked_neighbor = block.get_adjacent_nodes(grid.grid) #I added this so that the grid is updated even when the agent doesn't bump into stuff
                    for coordinate in blocked_neighbor: #identify in the tempGrid the neighbors that we know are blocked
                        tempGrid[coordinate.x][coordinate.y] = 1
                    final_path.append(block)
                index+=1

        return final_path

    def compare_forward_backward(self): #counts the number of expanded nodes in forwards and backwards a start for a bunch mazes and calculates the avg
        sys.setrecursionlimit(10300)
        astar = A_star()
        forwards_count = 0
        backwards_count = 0
        global expanded_nodes
        for i in range(10):
            grid = Grid()
            grid.create_maze()
            grid.create_start_and_goal()
            astar.repeated_forward_a_star(grid, grid.start, grid.target)
            forwards_count+=expanded_nodes
            print(expanded_nodes)
            expanded_nodes = 0
            astar.repeated_backward_a_star(grid, grid.start, grid.target)
            backwards_count+=expanded_nodes
            print(expanded_nodes)
            expanded_nodes = 0
            print("Next")
            print()

        print("Forward average")
        print(forwards_count/10)
        print("Backward Average")
        print(backwards_count/10)

    def adaptive_astar(self, grid, start_node, goal_node):
        path = deque()
        current_max_g = 0

        if len(path) is not 0:
            for node in path:
                node.g = current_max_g - node.g
                
    def clear_lookup_table(self):
        A_star.f_lookup_table = {}
        
        


if __name__ == "__main__":
    grid1 = [
       [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 0, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
        
    start_node = Block(0, 0)
    goal_node = Block(8, 9)

    grid = Grid()
    astar = A_star()

    astar.compare_forward_backward()

    #testing A* plain:
    # path = astar.a_star(grid, start_node, goal_node)
    # endNode = path.pop()
    
    # reversedPath = deque()
    # while endNode:
    #     reversedPath.append(endNode)
    #     endNode = endNode.parent
    
    #testing using grid1:
    # grid.grid =  grid1      
    # grid.start = start_node
    # grid.target = goal_node
    # reversedPath = astar.repeated_backward_a_star(grid, grid.start, grid.target)
    # if reversedPath: 
    #     grid.color_path(reversedPath)
    #     while reversedPath:
    #         node = reversedPath.pop()
    #         print(node.location.x, node.location.y)  

    #testing using a generated grid:
    sys.setrecursionlimit(10300)
    grid.create_maze()
    grid.save_grid(2)
    # grid.get_grid(2)
    grid.create_start_and_goal()
    TieBreaker().set_prioritization(True)
    reversedPath = astar.repeated_forward_a_star(grid, grid.start, grid.target)
    # if reversedPath: 
    #     grid.color_path(reversedPath)
        # while reversedPath:
        #     node = reversedPath.pop()
            # print(node.location.x, node.location.y)
    
    TieBreaker().set_prioritization(False)
    reversedPath2 = astar.repeated_forward_a_star(grid, grid.start, grid.target)
    # if reversedPath: 
    #     grid.color_path(reversedPath)
        # while reversedPath:
        #     node = reversedPath.pop()
        
    if reversedPath and reversedPath2:
        grid.color_paths(reversedPath, reversedPath2)




        

        
        
