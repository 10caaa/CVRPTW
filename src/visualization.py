import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
from src.models import Solution


def plot_solution(solution: Solution, title: str = "VRP Solution", save_path: Optional[str] = None, show: bool = False):
    fig, ax = plt.subplots(figsize=(12, 9))
    
    depot = solution.depot
    colors = plt.cm.tab20(np.linspace(0, 1, len(solution.vehicles)))
    
    # Dépôt
    ax.scatter(depot.x, depot.y, c='red', s=400, marker='s', 
               label='Dépôt', zorder=5, edgecolors='black', linewidth=2)
    
    # Routes
    for idx, vehicle in enumerate(solution.vehicles):
        if len(vehicle.route) == 0:
            continue
        
        route_x = [depot.x] + [client.x for client in vehicle.route] + [depot.x]
        route_y = [depot.y] + [client.y for client in vehicle.route] + [depot.y]
        
        ax.plot(route_x, route_y, c=colors[idx], linewidth=2.5, alpha=0.7, 
                label=f'V{vehicle.id + 1} ({vehicle.load}/{vehicle.capacity})')
        
        for client in vehicle.route:
            ax.scatter(client.x, client.y, c=[colors[idx]], s=150, 
                       zorder=3, edgecolors='black', linewidth=0.5)
            ax.annotate(str(client.id), (client.x, client.y), 
                        fontsize=9, ha='center', va='center', fontweight='bold')
    
    ax.set_title(f'{title}\nDistance: {solution.cost:.2f} | Véhicules: {solution.get_num_vehicles_used()}', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.legend(loc='best', fontsize=9, ncol=2)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_convergence(costs: List[float], title: str = "Convergence", save_path: Optional[str] = None):
    plt.figure(figsize=(12, 6))
    
    iterations = range(len(costs))
    plt.plot(iterations, costs, linewidth=2, color='blue', alpha=0.7, label='Coût actuel')
    
    best_costs = [min(costs[:i+1]) for i in range(len(costs))]
    plt.plot(iterations, best_costs, linewidth=2.5, color='red', label='Meilleur coût')
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Itérations', fontsize=12)
    plt.ylabel('Coût', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def print_solution_details(solution: Solution):
    print("\n" + "="*70)
    print(f"SOLUTION VRP - DÉTAILS")
    print("="*70)
    print(f"Distance Totale: {solution.cost:.2f}")
    print(f"Véhicules Utilisés: {solution.get_num_vehicles_used()}/{len(solution.vehicles)}")
    print(f"Faisable (Capacité): {all(v.load <= v.capacity for v in solution.vehicles)}")
    print("\n" + "-"*70)
    print("ROUTES:")
    print("-"*70)
    
    for idx, vehicle in enumerate(solution.vehicles):
        if len(vehicle.route) > 0:
            print(f"\n🚛 Véhicule {idx + 1}:")
            print(f"  Clients: {[c.id for c in vehicle.route]}")
            print(f"  Charge: {vehicle.load}/{vehicle.capacity} ({vehicle.load/vehicle.capacity*100:.1f}%)")
            print(f"  Nombre de clients: {len(vehicle.route)}")
    
    print("\n" + "="*70)


def export_solution(solution: Solution, filename: str):
    with open(filename, 'w') as f:
        f.write(f"Cost: {solution.cost:.2f}\n")
        f.write(f"Vehicles used: {solution.get_num_vehicles_used()}\n\n")
        
        for idx, vehicle in enumerate(solution.vehicles):
            if len(vehicle.route) > 0:
                f.write(f"Route {idx + 1}: ")
                f.write(" -> ".join([str(solution.depot.id)] + [str(c.id) for c in vehicle.route] + [str(solution.depot.id)]))
                f.write(f" (Load: {vehicle.load}/{vehicle.capacity})\n")
    
    print(f"Solution exported to {filename}")

