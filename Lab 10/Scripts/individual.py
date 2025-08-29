import random
from typing import List
from tsp_parser import TSPProblem

# Usage: permutation chromosome with cached tour length as fitness
class Individual:
    def __init__(self, genes: List[int], problem: TSPProblem):
        self.genes = genes[:]
        self.problem = problem
        self.fitness = self._evaluate()

    # Usage: compute cyclic tour length using problem.dist (lower is better)
    def _evaluate(self) -> float:
        dmat = self.problem.dist
        g = self.genes
        total = 0.0
        for i in range(len(g)):
            a = g[i]
            b = g[(i+1) % len(g)]
            total += dmat[a][b]
        return total
    
    # Usage: duplicate chromosome without recomputing fitness
    def copy(self) -> "Individual":
        clone = Individual(self.genes, self.problem)
        clone.fitness = self.fitness
        return clone
    
    # Usage: create a random valid permutation over all cities
    @staticmethod
    def random(problem: TSPProblem) -> "Individual":
        genes = list(range(problem.n_cities))
        random.shuffle(genes)
        return Individual(genes, problem)
