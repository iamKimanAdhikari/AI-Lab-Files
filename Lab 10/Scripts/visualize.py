from pathlib import Path
from typing import Dict, List
import matplotlib.pyplot as plt
from tsp_parser import TSPProblem

# Usage: plot convergence and routes for report-quality SVGs
class Visualizer:
    def __init__(self, problem: TSPProblem):
        self.problem = problem

    # Usage: line plot of best vs avg fitness across generations (SVG)
    def plot_convergence(self, history: Dict[str, List[float]], outpath: Path):
        plt.figure()
        best = history.get("best", [])
        avg = history.get("avg", [])
        if "init_best" in history and "init_avg" in history:
            best = [history["init_best"]] + best
            avg = [history["init_avg"]] + avg
        plt.plot(best, label="Best")
        plt.plot(avg, label="Average")
        plt.title(f"GA Convergence — {self.problem.name}")
        plt.xlabel("Generation (0 = initial)")
        plt.ylabel("Tour Length")
        plt.legend()
        plt.tight_layout()
        plt.savefig(outpath, format="svg")
        plt.close()

    # Usage: draw the initial route with markers/step numbers (SVG)
    def plot_initial_route(self, route: List[int], outpath: Path):
        self._plot_route_common(route, outpath, title=f"Initial Route — {self.problem.name}")

    # Usage: draw the best-found route with markers/step numbers (SVG)
    def plot_route(self, route: List[int], outpath: Path):
        self._plot_route_common(route, outpath, title=f"Best Route — {self.problem.name}")

    # Usage: shared polyline/markers/annotations helper used by route plotters
    def _plot_route_common(self, route: List[int], outpath: Path, title: str):
        coords = self.problem.coords
        xs = [coords[i][0] for i in route] + [coords[route[0]][0]]
        ys = [coords[i][1] for i in route] + [coords[route[0]][1]]
        plt.figure()
        plt.plot(xs, ys, marker="o", linewidth=1.2)
        for step, city in enumerate(route, start=1):
            x, y = coords[city]
            plt.annotate(str(step), (x, y), textcoords="offset points", xytext=(6, 6), fontsize=8)
        start_city = route[0]
        end_city = route[-1]
        sx, sy = coords[start_city]
        ex, ey = coords[end_city]
        plt.scatter([sx], [sy], marker="*", s=150, label=f"START (city {start_city})")
        plt.scatter([ex], [ey], marker="s",  s=80,  label=f"END (city {end_city})")
        plt.title(title)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.tight_layout()
        plt.savefig(outpath, format="svg")
        plt.close()
