"""
Example usage of VRP Solver
Demonstrates programmatic usage without CLI
"""

from src.parser import load_instance
from src.heuristics import (
    generate_random_solution,
    generate_nearest_neighbor_solution,
    generate_clarke_wright_solution
)
from src.solver import simulated_annealing, local_search
from src.visualization import plot_solution, print_solution_details, export_solution


def example_basic():
    """Basic usage example"""
    print("="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    clients, depot, capacity = load_instance("instance/VRPLIB/tests/data/A-n32-k5.vrp")
    
    initial = generate_clarke_wright_solution(clients, depot, capacity)
    print(f"Initial solution: {initial.cost:.2f}")
    
    best = simulated_annealing(initial, verbose=False)
    print(f"Optimized solution: {best.cost:.2f}")
    
    print_solution_details(best)
    plot_solution(best, title="Example Basic Solution")


def example_compare_methods():
    """Compare different initial solution methods"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Comparing Initial Solution Methods")
    print("="*60)
    
    clients, depot, capacity = load_instance("instance/VRPLIB/tests/data/A-n32-k5.vrp")
    num_vehicles = 5
    
    methods = {
        'Random': lambda: generate_random_solution(clients, depot, num_vehicles, capacity),
        'Nearest Neighbor': lambda: generate_nearest_neighbor_solution(clients, depot, num_vehicles, capacity),
        'Clarke-Wright': lambda: generate_clarke_wright_solution(clients, depot, capacity)
    }
    
    results = {}
    for name, method in methods.items():
        solution = method()
        results[name] = solution.cost
        print(f"{name:20s}: {solution.cost:8.2f}")
    
    best_method = min(results, key=results.get)
    print(f"\nBest initial method: {best_method}")


def example_with_local_search():
    """Using simulated annealing with local search"""
    print("\n" + "="*60)
    print("EXAMPLE 3: SA + Local Search")
    print("="*60)
    
    clients, depot, capacity = load_instance("instance/VRPLIB/tests/data/A-n32-k5.vrp")
    
    initial = generate_clarke_wright_solution(clients, depot, capacity)
    print(f"Initial: {initial.cost:.2f}")
    
    after_sa = simulated_annealing(initial, max_iter=20000, verbose=False)
    print(f"After SA: {after_sa.cost:.2f}")
    
    final = local_search(after_sa, max_iterations=100)
    print(f"After Local Search: {final.cost:.2f}")
    
    improvement = ((initial.cost - final.cost) / initial.cost) * 100
    print(f"Total improvement: {improvement:.1f}%")


def example_custom_parameters():
    """Using custom SA parameters"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Parameters")
    print("="*60)
    
    clients, depot, capacity = load_instance("instance/VRPLIB/tests/data/E-n13-k4.vrp")
    
    initial = generate_clarke_wright_solution(clients, depot, capacity)
    
    configs = [
        {'temp': 1000, 'cooling': 0.99, 'iter': 10000, 'name': 'Fast'},
        {'temp': 2000, 'cooling': 0.999, 'iter': 30000, 'name': 'Balanced'},
        {'temp': 3000, 'cooling': 0.9995, 'iter': 50000, 'name': 'Thorough'},
    ]
    
    for config in configs:
        solution = simulated_annealing(
            initial.copy(),
            initial_temp=config['temp'],
            cooling_rate=config['cooling'],
            max_iter=config['iter'],
            verbose=False
        )
        print(f"{config['name']:12s}: {solution.cost:8.2f} (T={config['temp']}, α={config['cooling']})")


def example_multiple_instances():
    """Process multiple instances"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Multiple Instances")
    print("="*60)
    
    instances = [
        "instance/VRPLIB/tests/data/E-n13-k4.vrp",
        "instance/VRPLIB/tests/data/A-n32-k5.vrp",
        "instance/VRPLIB/tests/data/P-n16-k8.vrp",
    ]
    
    for instance_path in instances:
        try:
            clients, depot, capacity = load_instance(instance_path)
            initial = generate_clarke_wright_solution(clients, depot, capacity)
            best = simulated_annealing(initial, max_iter=20000, verbose=False)
            
            instance_name = instance_path.split('/')[-1].replace('.vrp', '')
            print(f"{instance_name:15s}: {best.cost:8.2f} ({best.get_num_vehicles_used()} vehicles)")
        except Exception as e:
            print(f"Error processing {instance_path}: {e}")


if __name__ == "__main__":
    example_basic()
    example_compare_methods()
    example_with_local_search()
    example_custom_parameters()
    example_multiple_instances()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)
