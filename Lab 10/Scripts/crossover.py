import random
from typing import Tuple, List
from individual import Individual
from tsp_parser import TSPProblem

# Usage: permutation-preserving OX recombination with configurable probability
class OrderCrossover:
    def __init__(self, rate: float = 0.9):
        self.rate = rate

    # Usage: OX child = slice from p1 + remaining p2 cities in order (no dups)
    def _ox_pair(self, p1: List[int], p2: List[int]) -> List[int]:
        n = len(p1)
        a, b = sorted(random.sample(range(n), 2))
        child = [None] * n
        child[a:b+1] = p1[a:b+1]
        p2_iter = (g for g in p2 if g not in child)
        for i in list(range(b+1, n)) + list(range(0, a)):
            child[i] = next(p2_iter)
        return child
    
    # Usage: return two children via OX with rate; else pass through parents
    def crossover(self, mom: Individual, dad: Individual, problem: TSPProblem) -> Tuple[Individual, Individual]:
        if random.random() > self.rate:
            return mom.copy(), dad.copy()
        c1 = self._ox_pair(mom.genes, dad.genes)
        c2 = self._ox_pair(dad.genes, mom.genes)
        return Individual(c1, problem), Individual(c2, problem)
