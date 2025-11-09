from src.parser import load_instance
from src.heuristics import generate_nearest_neighbor_solution
from src.solver import simulated_annealing
from src.visualization import plot_solution, print_solution_details
import matplotlib
matplotlib.use('Agg')

# Solutions optimales connues (Solomon benchmark)
SOLOMON_BEST_KNOWN = {
    'C101': {'distance': 828.94, 'vehicles': 10},
    'C102': {'distance': 828.94, 'vehicles': 10},
    'C201': {'distance': 591.56, 'vehicles': 3},
    'R101': {'distance': 1650.80, 'vehicles': 19},
    'R201': {'distance': 1252.37, 'vehicles': 4},
    'RC101': {'distance': 1696.95, 'vehicles': 14},
    'RC201': {'distance': 1406.94, 'vehicles': 4},
}

print("="*70)
print("TEST CVRPTW SOLVER - Instance Solomon C101")
print("="*70)

# Charger instance
clients, depot, capacity = load_instance('instance/VRPLIB/tests/data/C101.txt')
print(f"\n[OK] Instance chargee: {len(clients)} clients, capacite={capacity}")
print(f"[OK] Depot: fenetre temporelle [{depot.ready_time}, {depot.due_time}]")
print(f"[OK] Premier client: {clients[0]}")

optimal = SOLOMON_BEST_KNOWN.get('C101', {})
if optimal:
    print(f"[OK] Optimal connu: distance={optimal['distance']}, vehicules={optimal['vehicles']}")

# Générer solution initiale
print("\n[*] Generation solution initiale (Nearest Neighbor avec TW)...")
num_vehicles = 25
initial_solution = generate_nearest_neighbor_solution(clients, depot, num_vehicles, capacity)
print(f"[OK] Solution initiale: distance={initial_solution.cost:.2f}, faisable={initial_solution.is_feasible()}")

# Optimiser
print("\n[*] Optimisation par Recuit Simule...")
best_solution = simulated_annealing(
    initial_solution,
    initial_temp=1000,
    cooling_rate=0.998,
    max_iter=10000,
    min_temp=0.1,
    verbose=True
)

print(f"\n[RESULTAT] Optimisation terminee!")
print(f"Distance finale: {best_solution.cost:.2f}")
print(f"Vehicules utilises: {best_solution.get_num_vehicles_used()}")
print(f"Faisabilite: {best_solution.is_feasible()}")

if optimal:
    gap_distance = ((best_solution.cost - optimal['distance']) / optimal['distance']) * 100
    gap_vehicles = best_solution.get_num_vehicles_used() - optimal['vehicles']
    print(f"\n[GAP] Performance vs Optimal:")
    print(f"  Distance: {gap_distance:+.2f}% (optimal={optimal['distance']:.2f})")
    print(f"  Vehicules: {gap_vehicles:+d} (optimal={optimal['vehicles']})")

# Afficher détails
print_solution_details(best_solution)

# Visualiser (sans affichage interactif)
print("\n[*] Generation de la visualisation...")
plot_solution(best_solution, title="CVRPTW - Solomon C101", save_path="results/cvrptw_c101_test.png")
print("[OK] Visualisation sauvegardee dans results/cvrptw_c101_test.png")

print("\n" + "="*70)
print("Test termine!")
print("="*70)
print("="*70)
