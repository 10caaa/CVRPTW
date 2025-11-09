# Architecture du Projet VRP Solver

## Vue d'ensemble

Le projet suit une architecture modulaire en couches pour faciliter la maintenance, l'extensibilité et les tests.

## Diagramme d'Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Interface Utilisateur                   │
│                        (main.py)                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   Couche Configuration                       │
│                     (config.py)                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Couche Métier                             │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐          │
│  │  Parser    │  │ Heuristics │  │   Solver     │          │
│  │ (parser.py)│  │(heuristics)│  │ (solver.py)  │          │
│  └────────────┘  └────────────┘  └──────────────┘          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Couche Données                            │
│                    (models.py)                               │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  Couche Présentation                         │
│                (visualization.py)                            │
└──────────────────────────────────────────────────────────────┘
```

## Modules Détaillés

### 1. models.py - Modèle de Données
**Responsabilité** : Définir les structures de données fondamentales

**Classes** :
- `Client` : Représente un client/nœud
- `Vehicle` : Représente un véhicule avec capacité
- `Solution` : Ensemble complet de routes

**Fonctions** :
- `euclidean_distance()` : Calcul de distance

### 2. parser.py - Lecture d'Instances
**Responsabilité** : Charger et parser les fichiers VRPLIB

**Fonctions** :
- `parse_vrplib()` : Parser format VRPLIB
- `create_clients_and_depot()` : Créer objets Client
- `load_instance()` : Interface simplifiée

### 3. heuristics.py - Solutions Initiales
**Responsabilité** : Générer solutions de départ

**Algorithmes** :
- `generate_random_solution()` : Assignation aléatoire
- `generate_nearest_neighbor_solution()` : Plus proche voisin
- `generate_clarke_wright_solution()` : Économies de fusion

### 4. solver.py - Optimisation
**Responsabilité** : Métaheuristiques et opérateurs

**Opérateurs de voisinage** :
- `swap_move()` : Échange inter-routes
- `relocate_move()` : Relocalisation
- `two_opt_move()` : Optimisation intra-route
- `or_opt_move()` : Déplacement de séquences
- `cross_exchange_move()` : Échange de segments

**Algorithmes** :
- `simulated_annealing()` : Recuit simulé
- `local_search()` : Recherche locale
- `acceptance_probability()` : Critère de Metropolis

### 5. visualization.py - Présentation
**Responsabilité** : Affichage et export

**Fonctions** :
- `plot_solution()` : Graphique des routes
- `plot_convergence()` : Évolution du coût
- `print_solution_details()` : Statistiques
- `export_solution()` : Export fichier texte

### 6. config.py - Configuration
**Responsabilité** : Gestion paramètres

**Classe** :
- `Config` : Chargement YAML et accès paramètres

### 7. main.py - Point d'Entrée
**Responsabilité** : Orchestration et CLI

**Fonctionnalités** :
- Parsing arguments ligne de commande
- Orchestration du workflow complet
- Affichage des résultats

## Flux d'Exécution

```
1. main.py
   ↓
2. Charger configuration (config.py)
   ↓
3. Parser instance (parser.py)
   ↓
4. Générer solution initiale (heuristics.py)
   ↓
5. Optimiser (solver.py)
   ↓
6. Recherche locale optionnelle (solver.py)
   ↓
7. Visualiser/Exporter (visualization.py)
```

## Principes de Design

### SOLID

1. **Single Responsibility** : Chaque module une responsabilité
2. **Open/Closed** : Extensible sans modification
3. **Liskov Substitution** : Classes interchangeables
4. **Interface Segregation** : Interfaces minimales
5. **Dependency Inversion** : Dépendances vers abstractions

### Patterns Utilisés

- **Strategy Pattern** : Multiples heuristiques/opérateurs
- **Factory Pattern** : Création de solutions
- **Template Method** : Structure métaheuristique
- **Observer Pattern** : Logging/monitoring

## Extensibilité

### Ajouter un Nouvel Opérateur

```python
# Dans solver.py
def my_new_operator(solution: Solution) -> Solution:
    new_solution = solution.copy()
    # ... logique de l'opérateur
    new_solution.calculate_cost()
    return new_solution
```

### Ajouter une Nouvelle Heuristique

```python
# Dans heuristics.py
def my_heuristic(clients, depot, capacity):
    # ... logique constructive
    return Solution(vehicles, depot)
```

### Ajouter une Nouvelle Métaheuristique

```python
# Dans solver.py
def genetic_algorithm(population_size, generations):
    # ... logique AG
    return best_solution
```

## Tests

```
tests/
├── test_models.py       # Tests structures données
├── test_parser.py       # Tests parsing
├── test_heuristics.py   # Tests solutions initiales
└── test_solver.py       # Tests optimisation
```

## Dépendances

```
numpy        → Calculs numériques
matplotlib   → Visualisation
PyYAML       → Configuration
```

## Performance

| Opération | Complexité | Temps (n=100) |
|-----------|-----------|---------------|
| Parser | O(n) | < 0.1s |
| Clarke-Wright | O(n²) | ~0.5s |
| SA (10k iter) | O(iter × n) | ~2-3s |
| Visualisation | O(n) | ~0.2s |

## Évolutivité Future

### Version 3.0 Planifiée

- [ ] Support CVRPTW (fenêtres temporelles)
- [ ] Algorithme génétique
- [ ] Recherche taboue
- [ ] Interface web Flask
- [ ] Parallélisation multi-thread
- [ ] Export JSON/CSV
- [ ] Dashboard interactif
- [ ] API REST
