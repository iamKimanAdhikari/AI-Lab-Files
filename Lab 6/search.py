import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import colors
from collections import deque
import time

# Define the maze from the lab
maze = [
    ['S', 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'G'],
]

# Convert maze to numerical grid
def to_numeric_grid(maze):
    grid = np.zeros((len(maze), len(maze[0])), dtype=int)
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == 'S':
                grid[r, c] = 2
            elif cell == 'G':
                grid[r, c] = 3
            elif cell == 0:
                grid[r, c] = 0
            elif cell == 1:
                grid[r, c] = 1
    return grid

# Find position of a specific value in grid
def find_pos(grid, value):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == value:
                return (r, c)
    return None

# Get valid neighbors for a cell
def get_neighbors(grid, r, c):
    rows, cols = grid.shape
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    neighbors = []
    
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr, nc] != 1:  # Not a wall
                neighbors.append((nr, nc))
    return neighbors

# Solve maze with BFS or DFS
def solve_maze(grid, algorithm):
    start = find_pos(grid, 2)
    goal = find_pos(grid, 3)
    if not start or not goal:
        return None, None, 0, 0
    
    visited = set()
    parent = {}
    visit_order = []
    
    # Initialize frontier
    if algorithm == 'bfs':
        frontier = deque([start])
    else:  # dfs
        frontier = [start]
    
    visited.add(start)
    visit_order.append(start)
    start_time = time.time()
    path_found = False
    
    while frontier:
        # Get next node based on algorithm
        if algorithm == 'bfs':
            r, c = frontier.popleft()
        else:  # dfs
            r, c = frontier.pop()
        
        # Check if goal reached
        if (r, c) == goal:
            path_found = True
            break
        
        # Explore neighbors
        for nr, nc in get_neighbors(grid, r, c):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                visit_order.append((nr, nc))
                parent[(nr, nc)] = (r, c)
                if algorithm == 'bfs':
                    frontier.append((nr, nc))
                else:  # dfs
                    frontier.append((nr, nc))
    
    end_time = time.time()
    exec_time = end_time - start_time
    
    # Reconstruct path
    path = []
    if path_found:
        node = goal
        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)
        path.reverse()
    
    return path, visit_order, len(path), exec_time

# Create colormap for visualization
maze_cmap = colors.ListedColormap(['white', 'black', 'orange', 'red', 'green', 'blue'])
maze_norm = colors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5], maze_cmap.N)

# Animate search process with final frame hold
def animate_search(grid, start, goal, visit_order, path, algorithm):
    fig, ax = plt.subplots(figsize=(10, 10))
    vis_grid = np.copy(grid)
    
    # Initialize visualization grid
    vis_grid[start] = 2  # Start
    vis_grid[goal] = 3   # Goal
    
    img = ax.imshow(vis_grid, cmap=maze_cmap, norm=maze_norm)
    ax.set_title(f"Maze Solving with {algorithm.upper()}")
    
    # Close figure when 'q' is pressed
    def on_key(event):
        if event.key == 'q':
            plt.close(fig)
    fig.canvas.mpl_connect('key_press_event', on_key)
    
    # Calculate extra frames for final hold (2 seconds at 50ms/frame = 40 frames)
    hold_frames = 40
    total_frames = len(visit_order) + len(path) + hold_frames
    
    # Animation update function
    def update(frame):
        nonlocal vis_grid
        
        # Phase 1: Show visited nodes
        if frame < len(visit_order):
            r, c = visit_order[frame]
            if (r, c) != start and (r, c) != goal:
                vis_grid[r, c] = 4  # Mark visited
                
        # Phase 2: Show path being built
        elif frame < len(visit_order) + len(path):
            path_idx = frame - len(visit_order)
            r, c = path[path_idx]
            if (r, c) != start and (r, c) != goal:
                vis_grid[r, c] = 5  # Mark path
                
        # Phase 3: Hold final frame (no changes)
        else:
            pass  # Maintain current state
        
        img.set_data(vis_grid)
        return [img]
    
    anim = FuncAnimation(fig, update, frames=total_frames, interval=50, blit=True)
    plt.show()

# Main program
if __name__ == "__main__":
    # Convert maze to numerical grid
    grid = to_numeric_grid(maze)
    start = find_pos(grid, 2)
    goal = find_pos(grid, 3)
    
    # Visualize initial maze
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap=maze_cmap, norm=maze_norm)
    plt.title("Initial Maze")
    plt.show()
    
    # Prompt user for algorithm choice
    algorithm = input("Choose algorithm (BFS or DFS): ").strip().lower()
    while algorithm not in ['bfs', 'dfs']:
        print("Invalid choice. Please enter 'bfs' or 'dfs'.")
        algorithm = input("Choose algorithm (BFS or DFS): ").strip().lower()
    
    # Solve maze and get results
    path, visit_order, path_length, exec_time = solve_maze(grid, algorithm)
    
    # Print results
    print(f"\nAlgorithm: {algorithm.upper()}")
    print(f"Execution time: {exec_time:.4f} seconds")
    print(f"Visited nodes: {len(visit_order)}")
    if path:
        print(f"Path length: {path_length} steps")
    else:
        print("No path found!")
    
    # Animate search process with final frame hold
    if path:
        animate_search(grid, start, goal, visit_order, path, algorithm)