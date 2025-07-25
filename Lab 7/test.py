import numpy as np
import heapq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from matplotlib import colors

# Define colormap for maze visualization
maze_cmap = colors.ListedColormap(['white', 'black', 'green', 'red', 'yellow', 'blue'])
maze_norm = colors.BoundaryNorm([0, 1, 2, 3, 4, 5], maze_cmap.N)

def generate_maze(rows, cols):
    # Ensure dimensions are odd
    if rows % 2 == 0: rows += 1
    if cols % 2 == 0: cols += 1
    maze = np.ones((rows, cols), dtype=int)  # Start with all walls (1)
    
    # Start from center
    start_row, start_col = rows // 2, cols // 2
    start = (start_row, start_col)
    maze[start] = 0  # Carve out start position
    
    walls = []
    for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        r2, c2 = start_row + dr, start_col + dc
        if 0 <= r2 < rows and 0 <= c2 < cols:
            walls.append((start_row, start_col, r2, c2))
    
    while walls:
        idx = np.random.randint(len(walls))
        r1, c1, r2, c2 = walls[idx]
        del walls[idx]
        
        if maze[r2, c2] == 1:  # If unvisited
            # Carve passage
            maze[(r1 + r2) // 2, (c1 + c2) // 2] = 0
            maze[r2, c2] = 0
            
            # Add new walls
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = r2 + dr, c2 + dc
                if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 1:
                    walls.append((r2, c2, nr, nc))
                    
    return maze

def place_start_goal(maze):
    rows, cols = maze.shape
    # Place start at top-left, goal at bottom-right
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    
    # Ensure start/goal positions are passages
    if maze[start] == 1:
        maze[start] = 0
    if maze[goal] == 1:
        maze[goal] = 0
    
    return maze, start, goal

def plot_maze(maze, start, end, title="Maze"):
    plt.figure(figsize=(8, 8))
    plt.imshow(maze, cmap=maze_cmap, norm=maze_norm)
    plt.scatter(start[1], start[0], c = "green", s=150, label="Start(S)")
    plt.scatter(end[1], end[0], c = "red", s=150, label="Goal(G)")
    plt.title(title)
    plt.legend()
    # plt.axis('off')
    plt.show()

    

def get_neighbors(maze, r, c):
    rows, cols = maze.shape
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if maze[nr, nc] != 1:  # Not a wall
                neighbors.append((nr, nc))
    
    return neighbors

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze, start, end):
    open_set = []
    heapq.heappush(open_set, (0 + manhattan(start, end), 0, start))
    
    came_from = {start: None}
    g_score = {start: 0}
    visited = set()
    visit_order = []
    
    while open_set:
        _, g, current = heapq.heappop(open_set)
        
        if current in visited:
            continue
            
        visited.add(current)
        visit_order.append(current)
        
        if current == end:
            # Reconstruct path
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, visit_order
        
        for neighbor in get_neighbors(maze, *current):
            new_g = g + 1
            # Only consider this new path if it's better
            if neighbor not in g_score or new_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = new_g
                f_score = new_g + manhattan(neighbor, end)
                heapq.heappush(open_set, (f_score, new_g, neighbor))
    
    return None, visit_order  # No path found

def animate_search(maze, start, end, visit_order, path):
    fig, ax = plt.subplots(figsize=(8, 8))
    vis_maze = np.array(maze)  # Working copy
    
    # Create a special visualization array with:
    # 0 = passage (white)
    # 1 = wall (black)
    # 2 = start (green)
    # 3 = end (red)
    # 4 = visited (yellow)
    # 5 = path (blue)
    
    # Mark start and end
    vis_maze[start] = 2
    vis_maze[end] = 3
    
    img = ax.imshow(vis_maze, cmap=maze_cmap, norm=maze_norm)
    ax.set_title("A* Pathfinding")
    ax.axis('off')
    
    def update(frame):
        if frame < len(visit_order):
            # Mark visited cells (yellow)
            r, c = visit_order[frame]
            if (r, c) not in (start, end):  # Don't overwrite start/goal
                vis_maze[r, c] = 4
        else:
            # Draw path (blue)
            path_idx = frame - len(visit_order)
            if path_idx < len(path):
                r, c = path[path_idx]
                if (r, c) not in (start, end):  # Don't overwrite start/goal
                    vis_maze[r, c] = 5
        
        img.set_data(vis_maze)
        return [img]
    
    total_frames = len(visit_order) + len(path)
    anim = FuncAnimation(fig, update, frames=total_frames, 
                         interval=50, blit=True, repeat=False)
    plt.show()

if __name__ == "__main__":
    np.random.seed(42)
    rows, cols = 21, 21

    # Generate and show maze
    print("Generating maze...")
    maze = generate_maze(rows, cols)
    maze, start, end = place_start_goal(maze)
    plot_maze(maze, start, end, "Generated Maze")

    # Run A* algorithm
    print("Running A* search...")
    t0 = time.time()
    path, visited = astar(maze, start, end)
    t1 = time.time()
    
    if path is None:
        print("No path found!")
    else:
        print(f"Path found in {t1-t0:.4f} seconds")
        print(f"Path length: {len(path)} nodes")
        print(f"Nodes visited: {len(visited)}")
        
        # Create visualization
        print("Animating search...")
        animate_search(maze, start, end, visited, path)