from block import Block
import heapq
from collections import deque
from tiebreaker import TieBreaker

class A_star:
    def a_star(self, temp_grid, start_node, goal_node):
        f_lookup_table = {}
        open_list = [] 
        closed_list = deque()

    
        heapq.heappush(open_list, start_node) #add start to open list
        start_node_h = start_node.getManhattanDistance(goal_node)
        f_lookup_table[start_node] = (start_node_h, 0)
        start_node.f = start_node_h
        
        while open_list:
            current_node = heapq.heappop(open_list) #pop off min value from the heap
            closed_list.append(current_node) #add to path

            if current_node == goal_node:
                print("found goal")
                break
            
            neighbors, blocked_neighbors = current_node.get_adjacent_nodes(temp_grid) #pass in the grid size so that we can check that we arent "overflowing"

            #the neighbors only include possible actions (already pruned)
            for neighbor in neighbors:
                neighbor.parent = current_node
                f_current, g_current = f_lookup_table[current_node]

                neighbor_h = neighbor.getManhattanDistance(goal_node)  #set huristic
                neighbor.g = g_current + 1 
                TieBreaker().updateMaxG(neighbor.g)
                neighbor.f = neighbor.g + neighbor_h


                if neighbor in open_list:
                    if f_lookup_table[neighbor][0] <= neighbor.f:
                        continue
                    else:
                        open_list.remove(neighbor)
                        
                if neighbor in closed_list:
                   if f_lookup_table[neighbor][0] <= neighbor.f:
                    continue
                   else:
                    closed_list.remove(neighbor)
                
                
                heapq.heappush(open_list, neighbor)
                f_lookup_table[neighbor] = (neighbor.f, neighbor.g)
        
        return closed_list

    def repeated_forward_a_star(self, grid, start_node, goal_node):
        tempGrid = [[0 for _ in range(len(grid))] for _ in range(len(grid))]
        current_node = start_node
        while current_node is not goal_node:
            a_star_path = self.a_star(tempGrid, current_node, goal_node)
            
            if not a_star_path:
                return #no answer
            for block in a_star_path:
                if block is goal_node:
                    return
                if grid[block.location.x][block.location.y] == 1:
                    block.f = float('inf')
                    tempGrid[block.location.x][block.location.y] = 1
                    current_node = block
                    break 
        return a_star_path
    
        
if __name__ == "__main__":
    grid = [[0, 1, 0, 0, 0],
            [1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]]
        
    start_node = Block(0, 0)
    goal_node = Block(4, 4)

    astar = A_star()

    tempGrid = [[0 for _ in range(5)] for _ in range(5)]
    path = astar.a_star(grid, start_node, goal_node)
    endNode = path.pop()
    
    reversedPath = deque()
    while endNode:
        reversedPath.append(endNode)
        endNode = endNode.parent
           
    while reversedPath:
        node = reversedPath.pop()
        print(node.location.x, node.location.y)     





        

        
        
