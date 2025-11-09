import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
from src.models import Solution


def plot_solution(solution: Solution, title: str = "VRP Solution", save_path: Optional[str] = None, show: bool = False):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9))
    
    depot = solution.depot
    colors = plt.cm.tab20(np.linspace(0, 1, len(solution.vehicles)))
    
    # Graphique 1: Routes spatiales
    ax1.scatter(depot.x, depot.y, c='red', s=400, marker='s', 
               label='Dépôt', zorder=5, edgecolors='black', linewidth=2)
    
    for idx, vehicle in enumerate(solution.vehicles):
        if len(vehicle.route) == 0:
            continue
        
        route_x = [depot.x] + [client.x for client in vehicle.route] + [depot.x]
        route_y = [depot.y] + [client.y for client in vehicle.route] + [depot.y]
        
        ax1.plot(route_x, route_y, c=colors[idx], linewidth=2.5, alpha=0.7, 
                label=f'V{vehicle.id + 1} ({vehicle.load}/{vehicle.capacity})')
        
        arrival_times, waiting_times, feasible = solution.calculate_route_times(vehicle)
        
        for i, client in enumerate(vehicle.route):
            marker_color = colors[idx] if feasible else 'red'
            ax1.scatter(client.x, client.y, c=[marker_color], s=150, 
                       zorder=3, edgecolors='black', linewidth=0.5)
            
            label_text = f'{client.id}'
            if arrival_times and i < len(arrival_times):
                label_text += f'\n[{client.ready_time:.0f},{client.due_time:.0f}]'
                label_text += f'\nA:{arrival_times[i]:.0f}'
                if i < len(waiting_times) and waiting_times[i] > 0:
                    label_text += f'\nW:{waiting_times[i]:.0f}'
            
            ax1.annotate(label_text, (client.x, client.y), 
                        fontsize=7, ha='center', va='center', fontweight='bold')
    
    ax1.set_title(f'{title}\nDistance: {solution.cost:.2f} | Véhicules: {solution.get_num_vehicles_used()} | Faisable: {solution.is_feasible()}', 
                 fontsize=14, fontweight='bold')
    ax1.set_xlabel('X', fontsize=12)
    ax1.set_ylabel('Y', fontsize=12)
    ax1.legend(loc='best', fontsize=9, ncol=2)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Graphique 2: Diagramme temporel
    y_position = 0
    route_details = solution.get_route_details()
    
    for route in route_details:
        if route['time_feasible']:
            arrival_times = route['arrival_times']
            waiting_times = route['waiting_times']
            vehicle = solution.vehicles[route['vehicle_id'] - 1]
            
            current_time = depot.ready_time
            prev_x = depot.x
            prev_y = depot.y
            
            ax2.plot([depot.ready_time, depot.ready_time], [y_position - 0.3, y_position + 0.3], 
                    'rs', markersize=10, label='Départ' if y_position == 0 else '')
            
            for i, client in enumerate(vehicle.route):
                travel_time = np.sqrt((client.x - prev_x)**2 + (client.y - prev_y)**2)
                arrival = arrival_times[i]
                waiting = waiting_times[i]
                service_start = max(arrival, client.ready_time)
                service_end = service_start + client.service_time
                
                # Trajet (ligne pointillée)
                ax2.plot([current_time, arrival], [y_position, y_position], 
                        'k--', alpha=0.3, linewidth=1)
                
                # Attente (rouge)
                if waiting > 0:
                    ax2.plot([arrival, service_start], [y_position, y_position], 
                            'r-', linewidth=4, alpha=0.6, label='Attente' if y_position == 0 and i == 0 else '')
                
                # Fenêtre temporelle (zone grisée)
                ax2.axvspan(client.ready_time, client.due_time, 
                           ymin=(y_position - 0.4 + 5) / 10, 
                           ymax=(y_position + 0.4 + 5) / 10,
                           alpha=0.1, color='blue')
                
                # Service (barre verte)
                ax2.plot([service_start, service_end], [y_position, y_position], 
                        color=colors[route['vehicle_id'] - 1], linewidth=6, 
                        solid_capstyle='round')
                
                # Annotation
                ax2.annotate(f'C{client.id}', (service_start, y_position), 
                           fontsize=8, ha='center', va='bottom', fontweight='bold')
                
                current_time = service_end
                prev_x, prev_y = client.x, client.y
            
            # Retour au dépôt
            return_time = current_time + np.sqrt((depot.x - prev_x)**2 + (depot.y - prev_y)**2)
            ax2.plot([current_time, return_time], [y_position, y_position], 
                    'k--', alpha=0.3, linewidth=1)
            ax2.plot([return_time, return_time], [y_position - 0.3, y_position + 0.3], 
                    'rs', markersize=10)
            
            # Label du véhicule
            ax2.text(-20, y_position, f'V{route["vehicle_id"]}', 
                    fontsize=10, va='center', fontweight='bold')
            
            y_position += 1
    
    ax2.set_xlabel('Temps', fontsize=12)
    ax2.set_ylabel('Véhicules', fontsize=12)
    ax2.set_title('Diagramme de Gantt - Fenêtres Temporelles', fontsize=14, fontweight='bold')
    ax2.set_yticks(range(len(route_details)))
    ax2.set_yticklabels([f'V{r["vehicle_id"]}' for r in route_details])
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.legend(loc='upper right', fontsize=9)
    
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
    print(f"SOLUTION CVRPTW - DÉTAILS")
    print("="*70)
    print(f"Distance Totale: {solution.cost:.2f}")
    print(f"Véhicules Utilisés: {solution.get_num_vehicles_used()}/{len(solution.vehicles)}")
    print(f"Faisable (Capacité): {all(v.load <= v.capacity for v in solution.vehicles)}")
    print(f"Faisable (Temps): {solution.is_feasible()}")
    print("\n" + "-"*70)
    print("ROUTES ET HORAIRES:")
    print("-"*70)
    
    routes = solution.get_route_details()
    for route in routes:
        print(f"\n🚛 Véhicule {route['vehicle_id']}:")
        print(f"  Clients: {route['clients']}")
        print(f"  Charge: {route['load']}/{route['capacity']} ({route['load']/route['capacity']*100:.1f}%)")
        print(f"  Nombre de clients: {route['num_clients']}")
        print(f"  Temps total: {route['total_time']:.2f}")
        print(f"  Faisabilité temporelle: {'✅' if route['time_feasible'] else '❌'}")
        
        if route['time_feasible'] and route['arrival_times']:
            print(f"\n  Horaires détaillés:")
            vehicle = solution.vehicles[route['vehicle_id'] - 1]
            for i, client in enumerate(vehicle.route):
                arrival = route['arrival_times'][i]
                waiting = route['waiting_times'][i]
                service_start = max(arrival, client.ready_time)
                service_end = service_start + client.service_time
                
                status = '⏰' if waiting > 0 else '✅'
                print(f"    {status} Client {client.id}: TW=[{client.ready_time:.0f},{client.due_time:.0f}] "
                      f"Arrivée={arrival:.1f} Attente={waiting:.1f} Service=[{service_start:.1f},{service_end:.1f}]")
    
    print("\n" + "="*70)


def export_solution(solution: Solution, filename: str):
    with open(filename, 'w') as f:
        f.write(f"Cost: {solution.cost:.2f}\n")
        f.write(f"Vehicles used: {solution.get_num_vehicles_used()}\n\n")
        
        routes = solution.get_route_details()
        for route in routes:
            f.write(f"Route {route['vehicle_id']}: ")
            f.write(" -> ".join([str(solution.depot.id)] + [str(c) for c in route['clients']] + [str(solution.depot.id)]))
            f.write(f" (Load: {route['load']}/{route['capacity']})\n")
    
    print(f"Solution exported to {filename}")
