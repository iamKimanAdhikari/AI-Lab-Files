import argparse
from pathlib import Path
from tsp_parser import TSPLIBParser
from genetics import GeneticAlgorithm
from visualize import Visualizer
from utils import set_seed

# Usage: expose CLI flags for data/hyperparams/paths suitable for berlin52 defaults
def parse_args():
    p = argparse.ArgumentParser(description="GA for TSP (Lab 10)")
    p.add_argument("--data", type=str, default=str(Path(__file__).parent.parent / "Dataset" / "berlin52.tsp"),
                   help="Path to TSPLIB .tsp file")
    p.add_argument("--pop_size", type=int, default=200)
    p.add_argument("--generations", type=int, default=800)
    p.add_argument("--selection", type=str, default="tournament", choices=["tournament", "roulette"])
    p.add_argument("--tournament_k", type=int, default=5)
    p.add_argument("--crossover_rate", type=float, default=0.9)
    p.add_argument("--mutation_rate", type=float, default=0.15)
    p.add_argument("--elitism", type=int, default=2, help="Number of best individuals to carry over")
    p.add_argument("--patience", type=int, default=80, help="Early stop if no improvement for N generations")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--outdir", type=str, default=str(Path(__file__).parent / "outputs"))
    return p.parse_args()

# Usage: end-to-end run: seed → parse data → GA → SVG plots → print summary
def main():
    args = parse_args()
    set_seed(args.seed)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    problem = TSPLIBParser.from_file(args.data)

    # Runningt Genetic ALgorithm
    ga = GeneticAlgorithm(
        problem=problem,
        pop_size=args.pop_size,
        selection_method=args.selection,
        tournament_k=args.tournament_k,
        crossover_rate=args.crossover_rate,
        mutation_rate=args.mutation_rate,
        elitism=args.elitism,
        max_generations=args.generations,
        patience=args.patience
    )

    best, history = ga.run()

    viz = Visualizer(problem)
    # NEW: save initial state (generation 0)
    if "init_route" in history:
        viz.plot_initial_route(history["init_route"], outdir / "initial_route.svg")
    
    viz.plot_convergence(history, outdir / "convergence.svg")
    viz.plot_route(best.genes, outdir / "best_route.svg")

    print("\nRESULTS:")
    print(f"Best tour length: {best.fitness:.4f}")
    print(f"Best route (0-based city indices): {best.genes}")
    print(f"Convergence plot saved to: {outdir / 'convergence.svg'}")
    print(f"Best route plot saved to: {outdir / 'best_route.svg'}")

if __name__ == "__main__":
    main()
