from dataclasses import dataclass
import math
from pathlib import Path
from typing import List, Tuple

# Usage: container for problem data (coords, dist matrix) consumed by GA and plotting
@dataclass
class TSPProblem:
    name: str
    coords: List[Tuple[float, float]]
    dist: List[List[float]]
    @property
    def n_cities(self) -> int:
        return len(self.coords)
    
# Usage: helper to compute straight-line distance for the dist matrix
def _euclidean(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.dist(a, b)

# Usage: parse TSPLIB .tsp and return a ready TSPProblem with precomputed distances
class TSPLIBParser:
    # Usage: load coordinates from NODE_COORD_SECTION and build symmetric dist matrix
    @staticmethod
    def from_file(path: str) -> TSPProblem:
        path = Path(path)
        name = path.stem
        coords: List[Tuple[float, float]] = []
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            in_section = False
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("NAME"):
                    parts = line.split(":")
                    if len(parts) >= 2:
                        name = parts[1].strip()
                if "NODE_COORD_SECTION" in line:
                    in_section = True
                    continue
                if "EOF" in line:
                    break
                if in_section:
                    parts = line.split()
                    if len(parts) >= 3:
                        x, y = float(parts[1]), float(parts[2])
                        coords.append((x, y))
        n = len(coords)
        dist = [[0.0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                d = _euclidean(coords[i], coords[j])
                dist[i][j] = d
                dist[j][i] = d
        return TSPProblem(name=name, coords=coords, dist=dist)
