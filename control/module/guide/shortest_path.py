from collections import deque
import numpy as np
from numpy import inf

# Constants
STAIR_ELEVATOR = 3
EMPTY = 0
WALL = 2

def create_3d_adjacency_matrix(mymap, goal):
    """
    Create a 3D adjacency matrix for the university map.
    Each node is represented as (floor, row, column).
    """
    nb_floors = len(mymap)
    nb_rows = len(mymap[0])
    nb_columns = len(mymap[0][0])
    
    # Total number of nodes in the 3D matrix
    nb_nodes = nb_floors * nb_rows * nb_columns
    
    # Initialize adjacency matrix with infinity
    adjacency_matrix = [[inf for _ in range(nb_nodes)] for _ in range(nb_nodes)]
    
    # Iterate through each floor, row, and column
    for floor in range(nb_floors):
        for row in range(nb_rows):
            for col in range(nb_columns):
                current_node = floor * (nb_rows * nb_columns) + row * nb_columns + col
                
                # Connect to adjacent cells in the same floor
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < nb_rows and 0 <= new_col < nb_columns:
                        # Allow the goal position to be connected, even if it's a wall
                        if (new_row == goal[1] and new_col == goal[2] and floor == goal[0]):
                            neighbor_node = floor * (nb_rows * nb_columns) + new_row * nb_columns + new_col
                            adjacency_matrix[current_node][neighbor_node] = 1
                        elif mymap[floor][new_row][new_col] == EMPTY or mymap[floor][new_row][new_col] == STAIR_ELEVATOR:
                            neighbor_node = floor * (nb_rows * nb_columns) + new_row * nb_columns + new_col
                            adjacency_matrix[current_node][neighbor_node] = 1
                
                # Connect to stairs or elevators on other floors
                if mymap[floor][row][col] == STAIR_ELEVATOR:
                    for other_floor in range(nb_floors):
                        if other_floor != floor:
                            neighbor_node = other_floor * (nb_rows * nb_columns) + row * nb_columns + col
                            adjacency_matrix[current_node][neighbor_node] = 1
    
    return adjacency_matrix

def bfs(mymap, start, goal):
    """
    Find the shortest path in a 3D matrix using BFS.
    """
    nb_floors = len(mymap)
    nb_rows = len(mymap[0])
    nb_columns = len(mymap[0][0])
    
    # Convert (floor, row, col) to node index
    start_node = start[0] * (nb_rows * nb_columns) + start[1] * nb_columns + start[2]
    goal_node = goal[0] * (nb_rows * nb_columns) + goal[1] * nb_columns + goal[2]
    
    # Create adjacency matrix
    adjacency_matrix = create_3d_adjacency_matrix(mymap, goal)
    
    # BFS setup
    queue = deque()
    queue.append((start_node, [start]))
    
    visited = set()
    visited.add(start_node)
    
    while queue:
        current_node, path = queue.popleft()
        
        # Check if goal is reached
        if current_node == goal_node:
            return path
        
        # Explore neighbors
        for neighbor in range(len(adjacency_matrix)):
            if adjacency_matrix[current_node][neighbor] == 1 and neighbor not in visited:
                visited.add(neighbor)
                # Convert node index back to (floor, row, col)
                floor = neighbor // (nb_rows * nb_columns)
                row = (neighbor % (nb_rows * nb_columns)) // nb_columns
                col = neighbor % nb_columns
                queue.append((neighbor, path + [(floor, row, col)]))
    
    return None  # No path found

# # Example university matrix (3D)
# university_matrix = [
#     [
#         [0, 2, 2, 0, 1, 3],
#         [0, 0, 0, 0, 1, 0],
#         [0, 1, 0, 0, 0, 2],
#         [0, 0, 0, 0, 2, 0],
#         [3, 1, 0, 1, 1, 2]
#     ],
#     [
#         [2, 0, 1, 2, 1, 3],
#         [0, 2, 0, 0, 1, 2],
#         [1, 0, 2, 1, 1, 0],
#         [2, 0, 0, 0, 0, 1],
#         [3, 0, 1, 2, 0, 2]
#     ]
# ]

# # Example start and goal positions
# start = (0, 0, 0)  # Floor 0, Row 0, Column 0
# goal = (1, 4, 5)   # Floor 1, Row 3, Column 3

# # Find the shortest path
# shortest_path = bfs(university_matrix, start, goal)
# if shortest_path:
#     print("Shortest Path:", shortest_path)
# else:
#     print("No path found.")