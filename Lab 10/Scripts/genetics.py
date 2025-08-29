from typing import List, Tuple, Dict
from tsp_parser import TSPProblem
from individual import Individual
from selection import TournamentSelection, RouletteSelection
from crossover import OrderCrossover
from mutation import Mutator

# Usage: wire selection/crossover/mutation; run evolution with elitism & patience
class GeneticAlgorithm:
    def __init__(
        self,
        problem: TSPProblem,
        pop_size: int = 200,
        selection_method: str = "tournament",
        tournament_k: int = 5,
        crossover_rate: float = 0.9,
        mutation_rate: float = 0.15,
        elitism: int = 2,
        max_generations: int = 800,
        patience: int = 80
    ):
        self.problem = problem
        self.pop_size = pop_size
        self.elitism = max(0, elitism)
        self.max_generations = max_generations
        self.patience = patience

        if selection_method == "tournament":
            self.selector = TournamentSelection(k=tournament_k)
        else:
            self.selector = RouletteSelection()
        self.crosser = OrderCrossover(rate=crossover_rate)
        self.mutator = Mutator(rate=mutation_rate)

    # Usage: create initial random population of size pop_size
    def _init_population(self) -> List[Individual]:
        return [Individual.random(self.problem) for _ in range(self.pop_size)]
    
    # Usage: elitism carry-over, then breed via select→crossover→mutation to refill
    def _next_generation(self, population: List[Individual]) -> List[Individual]:
        population.sort(key=lambda ind: ind.fitness)
        new_pop: List[Individual] = [population[i].copy() for i in range(self.elitism)]

        while len(new_pop) < self.pop_size:
            mom = self.selector.choose(population)
            dad = self.selector.choose(population)
            c1, c2 = self.crosser.crossover(mom, dad, self.problem)
            c1 = self.mutator.mutate(c1)
            if len(new_pop) < self.pop_size:
                new_pop.append(c1)
            c2 = self.mutator.mutate(c2)
            if len(new_pop) < self.pop_size:
                new_pop.append(c2)
        return new_pop

    # Usage: main loop; track best/avg and stop on max_generations or no-improvement
    def run(self) -> Tuple[Individual, Dict[str, List[float]]]:
        population = self._init_population()
        best = min(population, key=lambda ind: ind.fitness).copy()

        fitnesses = [ind.fitness for ind in population]
        history = {
            "best": [],
            "avg": [],
            "init_best": best.fitness,
            "init_avg": sum(fitnesses) / len(fitnesses),
            "init_route": best.genes[:] 
        }

        best_streak = 0
        for _ in range(1, self.max_generations + 1):
            fitnesses = [ind.fitness for ind in population]
            gen_best = min(population, key=lambda ind: ind.fitness)
            if gen_best.fitness < best.fitness:
                best = gen_best.copy()
                best_streak = 0
            else:
                best_streak += 1

            history["best"].append(best.fitness)
            history["avg"].append(sum(fitnesses) / len(fitnesses))

            if self.patience and best_streak >= self.patience:
                break

            population = self._next_generation(population)

        return best, history

