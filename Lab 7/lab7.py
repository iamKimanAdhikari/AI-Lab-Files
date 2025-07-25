import numpy as np
import heapq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from matplotlib import colors
from matplotlib.patches import Patch

maze_cmap = colors.ListedColormap(["white","black","green","blue","yellow","red"])
maze_norm = colors.BoundaryNorm([0,1,2,3,4,5,6], maze_cmap.N)

def generate_maze(rows, cols):
    if rows%2==0: rows+=1
    if cols%2==0: cols+=1
    maze = np.ones((rows,cols),dtype=int)
    
    sr, sc = rows//2, cols//2
    maze[sr,sc]=0
    walls = [(sr,sc,sr+dr,sc+dc) 
             for dr,dc in [(-2,0),(2,0),(0,-2),(0,2)]
             if 0<=sr+dr<rows and 0<=sc+dc<cols]
    while walls:
        i = np.random.randint(len(walls))
        r1,c1,r2,c2 = walls.pop(i)
        if maze[r2,c2]==1:
            maze[(r1+r2)//2,(c1+c2)//2] = 0
            maze[r2,c2] = 0
            for dr,dc in [(-2,0),(2,0),(0,-2),(0,2)]:
                nr, nc = r2+dr, c2+dc
                if 0<=nr<rows and 0<=nc<cols and maze[nr,nc]==1:
                    walls.append((r2,c2,nr,nc))
    return maze

def place_start_goal(maze):
    r,c = maze.shape
    start = (1,1)
    goal  = (r-2,c-2)
    maze[start]=0
    maze[goal]=0
    return maze, start, goal

def plot_maze(maze, start, goal, title="Maze"):
    disp = maze.copy()
    disp[start]=4
    disp[goal]=5
    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(disp, cmap=maze_cmap, norm=maze_norm)
    ax.set_title(title)
    ax.axis("on")
    patches = [
        Patch(color="white",  label="Passage"),
        Patch(color="black",  label="Wall"),
        Patch(color="yellow", label="Start"),
        Patch(color="red",    label="Goal"),
    ]
    ax.legend(
        handles=patches,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        bbox_transform=ax.transAxes,
        borderaxespad=0
    )
    plt.tight_layout()
    plt.show()

def get_neighbors(maze, r, c):
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0<=nr<maze.shape[0] and 0<=nc<maze.shape[1] and maze[nr,nc]!=1:
            yield (nr, nc)

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(maze, start, goal):
    open_set = [(manhattan(start,goal), 0, start)]
    came_from = {start: None}
    g_score = {start: 0}
    visited = []
    closed = set()
    while open_set:
        _, g, cur = heapq.heappop(open_set)
        if cur in closed:
            continue
        closed.add(cur)
        visited.append(cur)
        if cur == goal:
            path = []
            while cur:
                path.append(cur)
                cur = came_from[cur]
            return path[::-1], visited
        for nbr in get_neighbors(maze, *cur):
            tg = g+1
            if nbr not in g_score or tg<g_score[nbr]:
                g_score[nbr]=tg
                came_from[nbr]=cur
                f = tg + manhattan(nbr, goal)
                heapq.heappush(open_set, (f, tg, nbr))
    return None, visited

def animate_search(maze, start, goal, visit_order, path):
    fig, ax = plt.subplots(figsize=(6,6))
    vis = maze.copy()
    vis[start]=4
    vis[goal]=5
    img = ax.imshow(vis, cmap=maze_cmap, norm=maze_norm)
    ax.set_title("A* Search")
    ax.axis("on")
    legend_patches = [
        Patch(color="green",  label="Visited"),
        Patch(color="blue",   label="Shortest Path"),
        Patch(color="yellow", label="Start"),
        Patch(color="red",    label="Goal"),
    ]
    ax.legend(
        handles=legend_patches,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        bbox_transform=ax.transAxes,
        borderaxespad=0
    )
    total_frames = len(visit_order) + (len(path) if path else 0) + 50

    def update(i):
        if i < len(visit_order):
            r,c = visit_order[i]
            if (r,c) not in (start, goal):
                vis[r,c] = 2
        elif path and i < len(visit_order) + len(path):
            pr = i - len(visit_order)
            r,c = path[pr]
            if (r,c) not in (start, goal):
                vis[r,c] = 3
        img.set_data(vis)
        return [img]

    anim = FuncAnimation(fig, update, frames=total_frames, interval=50, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()
    return anim 

if __name__ == "__main__":
    np.random.seed(42)
    maze = generate_maze(21,21)
    maze, start, goal = place_start_goal(maze)
    plot_maze(maze, start, goal, "Generated Maze")

    print("Running A*...")
    t0 = time.time()
    path, visited = astar(maze, start, goal)
    t1 = time.time()
    if path is None:
        print("No path found")
    else:
        print(f"Path Found in {t1-t0:.4f}s.")
        print(f"Path Length = {len(path)}.")
        print(f"Nodes Visited = {len(visited)}.")
        animate_search(maze, start, goal, visited, path)
