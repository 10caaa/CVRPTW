# VRP Solver

A Vehicle Routing Problem solver using simulated annealing and multiple construction heuristics.

## Features

- VRPLIB format parser
- Multiple construction heuristics (Random, Nearest Neighbor, Clarke-Wright)
- Simulated annealing with 5 neighborhood operators
- Local search optimization
- Visualization with matplotlib
- YAML configuration
- Results export

## Project Structure

```
CVRPTW/
├── src/                       # Code source principal
│   ├── __init__.py
│   ├── models.py             # Classes Client, Vehicle, Solution
│   ├── parser.py             # Parser VRPLIB
│   ├── heuristics.py         # Heuristiques constructives
│   ├── solver.py             # Recuit simulé + opérateurs
│   ├── visualization.py      # Graphiques et export
│   └── config.py             # Gestion configuration
├── config/
│   └── config.yaml           # Paramètres du solveur
├── data/                     # Instances VRP
├── instance/VRPLIB/          # Benchmark VRPLIB
├── tests/                    # Tests unitaires
│   └── test_models.py
├── results/                  # Résultats et graphiques
│   └── plots/
├── main.py                   # Script principal
├── requirements.txt          # Dépendances Python
└── README.md
```

## Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
python -m unittest tests/test_models.py
```

## Usage

Basic usage:

```bash
python main.py data/A-n32-k5.vrp
```

With options:

```bash
python main.py data/A-n32-k5.vrp --method clarke_wright --temp 2000 --cooling 0.999 --iterations 50000 --local-search --save --verbose
```

Available parameters:

| Option | Description | Défaut |
|--------|-------------|--------|
| `--method` | Méthode initiale (random/nearest_neighbor/clarke_wright) | clarke_wright |
| `--vehicles` | Nombre de véhicules (auto si omis) | auto |
| `--temp` | Température initiale | 2000 |
| `--cooling` | Taux de refroidissement | 0.999 |
| `--iterations` | Nombre max d'itérations | 50000 |
| `--local-search` | Apply local search | False |
| `--save` | Save results | False |
| `--verbose` | Verbose output | False |
| `--no-plot` | Disable visualization | False |

## Results

Instance A-n32-k5 (32 clients, 5 vehicles):
- Initial solution (Clarke-Wright): ~850
- Final solution (SA + Local Search): ~800
- Gap from optimal (784): 2-5%

## Tests

```bash
python -m unittest discover tests
```

## Configuration

Edit `config/config.yaml` to adjust parameters:

```yaml
solver:
  initial_temperature: 2000
  cooling_rate: 0.999
  max_iterations: 50000
  
heuristics:
  initial_solution_method: "clarke_wright"
```

## Programmatic Usage

```python
from src.parser import load_instance
from src.heuristics import generate_clarke_wright_solution
from src.solver import simulated_annealing
from src.visualization import plot_solution

clients, depot, capacity = load_instance("data/A-n32-k5.vrp")
initial = generate_clarke_wright_solution(clients, depot, capacity)
best = simulated_annealing(initial, initial_temp=2000, verbose=True)
plot_solution(best, title="VRP Solution")
```

## Algorithm

The solver uses:
1. Clarke-Wright savings algorithm for initial solution
2. Simulated annealing with 5 operators (swap, relocate, 2-opt, or-opt, cross-exchange)
3. Optional local search for refinement

## License

MIT

## References

- Clarke & Wright (1964) - Scheduling of Vehicles from a Central Depot
- Kirkpatrick et al. (1983) - Optimization by Simulated Annealing
