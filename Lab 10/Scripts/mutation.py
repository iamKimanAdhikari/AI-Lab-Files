import random
from typing import List
from individual import Individual
from tsp_parser import TSPProblem

# Usage: swap/inversion mutation for TSP tours with overall mutation probability
class Mutator:
    def __init__(self, rate: float = 0.15, swap_prob: float = 0.5):
        self.rate = rate
        self.swap_prob = swap_prob

    # Usage: swap two positions to make a small local perturbation
    def _swap(self, genes: List[int]):
        i, j = random.sample(range(len(genes)), 2)
        genes[i], genes[j] = genes[j], genes[i]

    # Usage: reverse a slice to improve subsequence orientation
    def _inversion(self, genes: List[int]):
        i, j = sorted(random.sample(range(len(genes)), 2))
        genes[i:j+1] = reversed(genes[i:j+1])

    # Usage: apply swap or inversion with rate; return new re-evaluated Individual
    def mutate(self, ind: Individual) -> Individual:
        genes = ind.genes[:]
        if random.random() < self.rate:
            if random.random() < self.swap_prob:
                self._swap(genes)
            else:
                self._inversion(genes)
        return Individual(genes, ind.problem)
