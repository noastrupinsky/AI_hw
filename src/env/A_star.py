from block import Block
from grid import Grid
import heapq
from collections import deque
from tiebreaker import TieBreaker
import sys
import random

expanded_nodes = 0

class A_star:
    h_lookup_table = {}
    lookup_table = {}
    
    def a_star(self, temp_grid, start_node, goal_node, adaptive):
        TieBreaker().reset()
        self.clear_lookup_table()
        if adaptive == False:
            self.clear_h_lookup_table()
        open_list = [] 
        closed_list = deque()

        heapq.heappush(open_list, start_node) #add start to open list

        if adaptive and start_node in A_star.h_lookup_table:
            start_node_h = A_star.h_lookup_table[start_node]
        else:
            start_node_h = start_node.getManhattanDistance(goal_node)
        
        start_node.f = start_node_h
           
        A_star.lookup_table[start_node] = start_node.f, 0
        
        while open_list:
            current_node = heapq.heappop(open_list) #pop off min value from the heap

            global expanded_nodes
            expanded_nodes += 1 #to count the number of expanded nodes
            
            closed_list.append(current_node) #add to path

            if current_node == goal_node:
                break
            neighbors, _ = current_node.get_adjacent_nodes(temp_grid) #pass in the grid size so that we can check that we arent "overflowing"

            #the neighbors only include possible actions (already pruned)
            for neighbor in neighbors:
                neighbor.parent = current_node
                
                _, g_current = A_star.lookup_table[current_node]

                if adaptive and neighbor in A_star.h_lookup_table:
                    neighbor_h = A_star.h_lookup_table[neighbor]
                else:
                    neighbor_h = neighbor.getManhattanDistance(goal_node)

                neighbor.g = g_current + 1 
                neighbor.f = neighbor.g + neighbor_h
                
                TieBreaker().updateMaxG(neighbor.g)

                if neighbor in open_list:
                    if A_star.lookup_table[neighbor][0] > neighbor.f:
                        open_list.remove(neighbor)
                        heapq.heapify(open_list)
                    else:
                        if A_star.lookup_table[neighbor][0] < neighbor.f:
                            continue
                        else:
                            if TieBreaker().tieBreaker(A_star.lookup_table[neighbor], (neighbor.f, neighbor.g)):
                                continue
                            else: 
                                open_list.remove(neighbor)
                                heapq.heapify(open_list)
                        
                if neighbor in closed_list:
                    if A_star.lookup_table[neighbor][0] > neighbor.f:
                        closed_list.remove(neighbor)
                    else:
                        if A_star.lookup_table[neighbor][0] < neighbor.f:
                            continue
                        else:
                            if TieBreaker().tieBreaker(A_star.lookup_table[neighbor], (neighbor.f, neighbor.g)):
                                continue
                            else: 
                                closed_list.remove(neighbor)
                       
                
                heapq.heappush(open_list, neighbor)
                A_star.lookup_table[neighbor] = (neighbor.f, neighbor.g)
                
        return closed_list

    def repeated_forward_a_star(self, grid, current_node, goal_node):
        tempGrid = [[0 for _ in range(len(grid.grid))] for _ in range(len(grid.grid))] #create tempGrid
        final_path = deque()
        final_path.append(current_node)
        while current_node is not goal_node: #while we have not reached the goal
            _, blocked = current_node.get_adjacent_nodes(grid.grid)
            for coordinate in blocked: #identify in the tempGrid the neighbors that we know are blocked
                tempGrid[coordinate.x][coordinate.y] = 1
                
            path = self.a_star(tempGrid, current_node, goal_node, False) #do A* with the info we have

            if goal_node not in path: #if there's no path we have no answer
                print("No path")
                return path
            
            endNode = path.pop()
            
            reversedPath = deque()
            while endNode:
                # print(endNode.location.x, endNode.location.y)
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
                if(block.location.x == 26 and block.location.y == 32):
                    print("HERE")
                if grid.grid[block.location.x][block.location.y] == 1: #if the path encounters an impediment
                    current_node = reversedPath[index] #set the node that we will do A* on in the next iteration to be the one before the blocked one on the path
                    reversedPath.clear()
                    break
                if block != current_node:
                    _, blocked_neighbor = block.get_adjacent_nodes(grid.grid) #I added this so that the grid is updated even when the agent doesn't bump into stuff
                    for coordinate in blocked_neighbor: #identify in the tempGrid the neighbors that we know are blocked
                        tempGrid[coordinate.x][coordinate.y] = 1
                    final_path.append(block)
                index-=1

        return final_path
    
    def repeated_backward_a_star(self, grid, current_node, goal_node):
        tempGrid = [[0 for _ in range(len(grid.grid))] for _ in range(len(grid.grid))] #create tempGrid
        final_path = deque()
        final_path.append(current_node)
        while current_node is not goal_node: #while we have not reached the goal
            unblocked, blocked = current_node.get_adjacent_nodes(grid.grid)
            for coordinate in blocked: #identify in the tempGrid the neighbors that we know are blocked
                tempGrid[coordinate.x][coordinate.y] = 1
            path = self.a_star(tempGrid, goal_node, current_node, False) #do A* with the info we have

            if current_node not in path: #if there's no path we have no answer
                print("No path")
                return path
            
            endNode = path.pop()
            
            reversedPath = deque()
            while endNode:
                # print(endNode.location.x, endNode.location.y)
                reversedPath.append(endNode)
                temp_node = endNode.parent
                endNode.parent = None
                endNode = temp_node
           
                
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
                    _, blocked_neighbor = block.get_adjacent_nodes(grid.grid) #I added this so that the grid is updated even when the agent doesn't bump into stuff
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
          

        print("Forward average")
        print(forwards_count/10)
        print("Backward Average")
        print(backwards_count/10)

    def update_h(self, path, goal_node):
        num = 0
        for current_node in path:
            _, g_goal = A_star.lookup_table[goal_node]
            _, g_node = A_star.lookup_table[current_node]

            A_star.h_lookup_table[current_node] = g_goal-g_node


    def adaptive_a_star(self, grid, start_node, goal_node):
        tempGrid = [[0 for _ in range(len(grid.grid))] for _ in range(len(grid.grid))] #create tempGrid
        
        final_path = deque()
        final_path.append(start_node)
        
        current_node = start_node
        
        while current_node is not goal_node: #while we have not reached the goal
            _, blocked = current_node.get_adjacent_nodes(grid.grid)
            for coordinate in blocked: #identify in the tempGrid the neighbors that we know are blocked
                tempGrid[coordinate.x][coordinate.y] = 1
            
            path = self.a_star(tempGrid, current_node, goal_node, True) #do A* with the info we have

            if goal_node not in path: #if there's no path we have no answer
                print("No path")
                return path
            
            node = path.pop()
            
            reversedPath = deque()
            while node:
                reversedPath.append(node)
                temp_node = node.parent
                node.parent = None
                node = temp_node
                
                
            index = len(reversedPath)
            while index > 0: #traverse the path that A* gave us in the right direction
                block = reversedPath[index-1]
                
                if block == goal_node:
                    final_path.append(block)
                    return final_path
                if(block.location.x == 25 and block.location.y == 32):
                    print("HERE")
                if grid.grid[block.location.x][block.location.y] == 1: #if the path encounters an impediment
                    current_node = reversedPath[index] #set the node that we will do A* on in the next iteration to be the one before the blocked one on the path
                    self.update_h(path, goal_node)
                    reversedPath.clear()
                    break
                
                if block != current_node:
                    _, blocked_neighbor = block.get_adjacent_nodes(grid.grid) #I added this so that the grid is updated even when the agent doesn't bump into stuff
                    for coordinate in blocked_neighbor: #identify in the tempGrid the neighbors that we know are blocked
                        tempGrid[coordinate.x][coordinate.y] = 1
                    final_path.append(block)
                    
                index-=1

        return final_path
                
    def clear_lookup_table(self):
        A_star.lookup_table = {}
    
    def clear_h_lookup_table(self):
        A_star.h_lookup_table = {}
    
    def perform_search(self, grid, generate_new_grids, x):
        global expanded_nodes
        if generate_new_grids:
            for i in range(50):
                grid.create_maze()
                grid.save_grid(i)
                
        print(f"Grid: {x}" ) 
        grid.get_grid(x)
        grid.create_start_and_goal()
        
        # grid.start = Block(38, 48)
        # grid.target = Block(26, 0)
        
        print(f"Start: ({grid.start.location.x}, {grid.start.location.y})")
        print(f"target: ({grid.target.location.x}, {grid.target.location.y})")
        expanded_nodes = 0
        A_star().clear_lookup_table()
        
        TieBreaker().set_prioritization(True)
        
        print("Starting Adaptive")
        adaptivePath = astar.adaptive_a_star(grid, grid.start, grid.target)
        adaptiveNodes = expanded_nodes
        expanded_nodes = 0
        A_star().clear_lookup_table()
        
        print("Starting repeated forward")
        repeatedForwardPath = astar.repeated_forward_a_star(grid, grid.start, grid.target)
        repeatedForwardNodes = expanded_nodes
        expanded_nodes = 0
        A_star().clear_lookup_table()
 
        print("Starting repeated backwards")
        repeatedBackwardsPath = astar.repeated_backward_a_star(grid, grid.start, grid.target)
        repeatedBackwardsNodes = expanded_nodes
        paths_large_g = [
            (adaptivePath, adaptiveNodes),
            (repeatedForwardPath, repeatedForwardNodes),
            (repeatedBackwardsPath, repeatedBackwardsNodes)
        ]

        # All same tests but with prioritizing small g
        TieBreaker().set_prioritization(False)
        print("Starting Adaptive")
        expanded_nodes = 0
        A_star().clear_lookup_table()
        adaptivePath = astar.adaptive_a_star(grid, grid.start, grid.target)
        adaptiveNodes = expanded_nodes
        
        print("Starting repeated forward")
        expanded_nodes = 0
        A_star().clear_lookup_table()
        repeatedForwardPath = astar.repeated_forward_a_star(grid, grid.start, grid.target)
        repeatedForwardNodes = expanded_nodes
        
        print("Starting repeated backwards")
        expanded_nodes = 0
        A_star().clear_lookup_table()
        repeatedBackwardsPath = astar.repeated_backward_a_star(grid, grid.start, grid.target)
        repeatedBackwardsNodes = expanded_nodes
        
        paths_small_g = [
            (adaptivePath, adaptiveNodes),
            (repeatedForwardPath, repeatedForwardNodes),
            (repeatedBackwardsPath, repeatedBackwardsNodes)
        ]
        
        
        titles_large_g = [
            "Adaptive Path (Large G)",
            "Repeated Forward Path (Large G)",
            "Repeated Backward Path (Large G)"
        ]

        titles_small_g = [
            "Adaptive Path (Small G)",
            "Repeated Forward Path (Small G)",
            "Repeated Backward Path (Small G)"
        ]
        
        grid.color_paths_in_two_sections(paths_large_g, paths_small_g, titles_large_g, titles_small_g, grid.start, grid.target)


    

if __name__ == "__main__":

    grid = Grid()
    astar = A_star()
    sys.setrecursionlimit(10300)
    
    random_number = random.randint(0, 49)
    astar.perform_search(grid, False, random_number)