import random
from typing import List
from individual import Individual

# Usage: pick best among k random contenders (pressure via k)
class TournamentSelection:
    def __init__(self, k: int = 5):
        self.k = k

    # Usage: sample k individuals and return the lowest-fitness one
    def choose(self, population: List[Individual]) -> Individual:
        contenders = random.sample(population, self.k)
        return min(contenders, key=lambda ind: ind.fitness)
    
# Usage: probability ∝ 1/fitness; favors shorter tours while keeping diversity
class RouletteSelection:
    def __init__(self, epsilon: float = 1e-9):
        self.eps = epsilon

    # Usage: draw one parent by roulette wheel on inverse-fitness weights
    def choose(self, population: List[Individual]) -> Individual:
        weights = [1.0 / (self.eps + ind.fitness) for ind in population]
        total = sum(weights)
        r = random.random() * total
        c = 0.0
        for ind, w in zip(population, weights):
            c += w
            if c >= r:
                return ind
        return population[-1]
