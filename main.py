import argparse
import os
import time
from datetime import datetime
from src.parser import load_instance
from src.heuristics import generate_random_solution, generate_nearest_neighbor_solution, generate_clarke_wright_solution
from src.solver import simulated_annealing, local_search
from src.visualization import plot_solution, print_solution_details, export_solution
from src.config import Config


def main():
    parser = argparse.ArgumentParser(description='VRP Solver using Metaheuristics')
    parser.add_argument('instance', type=str, help='Path to VRP instance file')
    parser.add_argument('--method', type=str, default='clarke_wright', 
                       choices=['random', 'nearest_neighbor', 'clarke_wright'],
                       help='Initial solution generation method')
    parser.add_argument('--vehicles', type=int, default=None, 
                       help='Number of vehicles (auto-detected if not specified)')
    parser.add_argument('--temp', type=float, default=2000, 
                       help='Initial temperature for simulated annealing')
    parser.add_argument('--cooling', type=float, default=0.999, 
                       help='Cooling rate')
    parser.add_argument('--iterations', type=int, default=50000, 
                       help='Maximum iterations')
    parser.add_argument('--local-search', action='store_true', 
                       help='Apply local search after SA')
    parser.add_argument('--no-plot', action='store_true', 
                       help='Disable visualization')
    parser.add_argument('--save', action='store_true', 
                       help='Save results and plots')
    parser.add_argument('--verbose', action='store_true', 
                       help='Verbose output')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("VRP SOLVER - Vehicle Routing Problem Optimizer")
    print("="*70)
    
    print(f"\nLoading instance: {args.instance}")
    clients, depot, capacity = load_instance(args.instance)
    print(f"✓ Loaded {len(clients)} clients, capacity: {capacity}")
    
    if args.vehicles:
        num_vehicles = args.vehicles
    else:
        total_demand = sum(c.demand for c in clients)
        num_vehicles = max(5, (total_demand + capacity - 1) // capacity)
    
    print(f"✓ Using {num_vehicles} vehicles\n")
    
    print(f"Generating initial solution using: {args.method}")
    start_time = time.time()
    
    if args.method == 'random':
        initial_solution = generate_random_solution(clients, depot, num_vehicles, capacity)
    elif args.method == 'nearest_neighbor':
        initial_solution = generate_nearest_neighbor_solution(clients, depot, num_vehicles, capacity)
    else:
        initial_solution = generate_clarke_wright_solution(clients, depot, capacity)
    
    init_time = time.time() - start_time
    print(f"✓ Initial solution cost: {initial_solution.cost:.2f} (in {init_time:.2f}s)")
    
    print(f"\nRunning Simulated Annealing...")
    print(f"  Temperature: {args.temp} → {0.1}")
    print(f"  Cooling rate: {args.cooling}")
    print(f"  Max iterations: {args.iterations}")
    
    sa_start = time.time()
    best_solution = simulated_annealing(
        initial_solution,
        initial_temp=args.temp,
        cooling_rate=args.cooling,
        max_iter=args.iterations,
        min_temp=0.1,
        verbose=args.verbose
    )
    sa_time = time.time() - sa_start
    
    print(f"✓ Simulated annealing completed in {sa_time:.2f}s")
    print(f"✓ Best solution cost: {best_solution.cost:.2f}")
    
    improvement = ((initial_solution.cost - best_solution.cost) / initial_solution.cost) * 100
    print(f"✓ Improvement: {improvement:.1f}%")
    
    if args.local_search:
        print(f"\nApplying local search...")
        ls_start = time.time()
        best_solution = local_search(best_solution, max_iterations=100)
        ls_time = time.time() - ls_start
        print(f"✓ Local search completed in {ls_time:.2f}s")
        print(f"✓ Final cost: {best_solution.cost:.2f}")
    
    print_solution_details(best_solution)
    
    if args.save:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        instance_name = os.path.splitext(os.path.basename(args.instance))[0]
        
        os.makedirs("results", exist_ok=True)
        os.makedirs("results/plots", exist_ok=True)
        
        result_file = f"results/{instance_name}_{timestamp}.txt"
        plot_file = f"results/plots/{instance_name}_{timestamp}.png"
        
        export_solution(best_solution, result_file)
        plot_solution(best_solution, 
                     title=f"{instance_name} - {args.method}", 
                     save_path=plot_file, 
                     show=not args.no_plot)
    elif not args.no_plot:
        plot_solution(best_solution, 
                     title=f"{os.path.basename(args.instance)} - {args.method}")
    
    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time:.2f}s")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
