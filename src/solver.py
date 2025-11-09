import random
import math
from typing import Callable, List
from copy import deepcopy
from src.models import Solution, Client, euclidean_distance


def swap_move(solution: Solution) -> Solution:
    new_solution = solution.copy()
    non_empty_vehicles = [v for v in new_solution.vehicles if len(v.route) > 0]
    
    if len(non_empty_vehicles) < 2:
        return new_solution
    
    v1, v2 = random.sample(non_empty_vehicles, 2)
    if len(v1.route) > 0 and len(v2.route) > 0:
        i1 = random.randint(0, len(v1.route) - 1)
        i2 = random.randint(0, len(v2.route) - 1)
        
        c1, c2 = v1.route[i1], v2.route[i2]
        
        if (v1.load - c1.demand + c2.demand <= v1.capacity and 
            v2.load - c2.demand + c1.demand <= v2.capacity):
            v1.route[i1] = c2
            v2.route[i2] = c1
            v1.load = v1.load - c1.demand + c2.demand
            v2.load = v2.load - c2.demand + c1.demand
            
            if not new_solution.is_route_time_feasible(v1) or not new_solution.is_route_time_feasible(v2):
                v1.route[i1] = c1
                v2.route[i2] = c2
                v1.load = v1.load + c1.demand - c2.demand
                v2.load = v2.load + c2.demand - c1.demand
    
    new_solution.calculate_cost()
    return new_solution


def relocate_move(solution: Solution) -> Solution:
    new_solution = solution.copy()
    non_empty_vehicles = [v for v in new_solution.vehicles if len(v.route) > 0]
    
    if len(non_empty_vehicles) < 1:
        return new_solution
    
    v1 = random.choice(non_empty_vehicles)
    v2 = random.choice(new_solution.vehicles)
    
    if len(v1.route) > 0:
        i1 = random.randint(0, len(v1.route) - 1)
        client = v1.route[i1]
        
        if v2.load + client.demand <= v2.capacity:
            v1.route.pop(i1)
            v1.load -= client.demand
            
            if len(v2.route) > 0:
                i2 = random.randint(0, len(v2.route))
                v2.route.insert(i2, client)
            else:
                v2.route.append(client)
            v2.load += client.demand
            
            if not new_solution.is_route_time_feasible(v1) or not new_solution.is_route_time_feasible(v2):
                v2.route.remove(client)
                v2.load -= client.demand
                v1.route.insert(i1, client)
                v1.load += client.demand
    
    new_solution.calculate_cost()
    return new_solution


def two_opt_move(solution: Solution) -> Solution:
    new_solution = solution.copy()
    non_empty_vehicles = [v for v in new_solution.vehicles if len(v.route) > 0]
    
    if len(non_empty_vehicles) < 1:
        return new_solution
    
    vehicle = random.choice(non_empty_vehicles)
    route = vehicle.route
    
    if len(route) > 3:
        i = random.randint(0, len(route) - 2)
        j = random.randint(i + 1, len(route) - 1)
        original_segment = vehicle.route[i:j+1].copy()
        vehicle.route[i:j+1] = list(reversed(vehicle.route[i:j+1]))
        
        if not new_solution.is_route_time_feasible(vehicle):
            vehicle.route[i:j+1] = original_segment
    
    new_solution.calculate_cost()
    return new_solution


def or_opt_move(solution: Solution) -> Solution:
    new_solution = solution.copy()
    non_empty_vehicles = [v for v in new_solution.vehicles if len(v.route) > 0]
    
    if len(non_empty_vehicles) < 1:
        return new_solution
    
    v1 = random.choice(non_empty_vehicles)
    
    if len(v1.route) > 2:
        length = random.randint(1, min(3, len(v1.route) - 1))
        i = random.randint(0, len(v1.route) - length)
        segment = v1.route[i:i+length]
        
        remaining = v1.route[:i] + v1.route[i+length:]
        if len(remaining) > 0:
            insert_pos = random.randint(0, len(remaining))
            v1.route = remaining[:insert_pos] + segment + remaining[insert_pos:]
    
    new_solution.calculate_cost()
    return new_solution


def cross_exchange_move(solution: Solution) -> Solution:
    new_solution = solution.copy()
    non_empty_vehicles = [v for v in new_solution.vehicles if len(v.route) > 0]
    
    if len(non_empty_vehicles) < 2:
        return new_solution
    
    v1, v2 = random.sample(non_empty_vehicles, 2)
    
    if len(v1.route) > 1 and len(v2.route) > 1:
        len1 = random.randint(1, min(2, len(v1.route)))
        len2 = random.randint(1, min(2, len(v2.route)))
        
        i1 = random.randint(0, len(v1.route) - len1)
        i2 = random.randint(0, len(v2.route) - len2)
        
        seg1 = v1.route[i1:i1+len1]
        seg2 = v2.route[i2:i2+len2]
        
        demand1 = sum(c.demand for c in seg1)
        demand2 = sum(c.demand for c in seg2)
        
        new_load1 = v1.load - demand1 + demand2
        new_load2 = v2.load - demand2 + demand1
        
        if new_load1 <= v1.capacity and new_load2 <= v2.capacity:
            v1.route = v1.route[:i1] + seg2 + v1.route[i1+len1:]
            v2.route = v2.route[:i2] + seg1 + v2.route[i2+len2:]
            v1.load = new_load1
            v2.load = new_load2
    
    new_solution.calculate_cost()
    return new_solution


def generate_neighbor(solution: Solution, operators: List[Callable] = None) -> Solution:
    if operators is None:
        operators = [swap_move, relocate_move, two_opt_move, or_opt_move, cross_exchange_move]
    
    operator = random.choice(operators)
    return operator(solution)


def local_search(solution: Solution, max_iterations: int = 100) -> Solution:
    current = solution.copy()
    improved = True
    iteration = 0
    
    while improved and iteration < max_iterations:
        improved = False
        best_neighbor = current
        
        for _ in range(10):
            neighbor = generate_neighbor(current)
            if neighbor.cost < best_neighbor.cost:
                best_neighbor = neighbor
                improved = True
        
        if improved:
            current = best_neighbor
        
        iteration += 1
    
    return current


def acceptance_probability(current_cost: float, new_cost: float, temperature: float) -> float:
    if new_cost < current_cost:
        return 1.0
    if temperature <= 0:
        return 0.0
    return math.exp((current_cost - new_cost) / temperature)


def simulated_annealing(
    initial_solution: Solution,
    initial_temp: float = 1000,
    cooling_rate: float = 0.995,
    max_iter: int = 10000,
    min_temp: float = 0.1,
    verbose: bool = False
) -> Solution:
    current_solution = initial_solution.copy()
    best_solution = current_solution.copy()
    
    temperature = initial_temp
    iteration = 0
    stagnation_counter = 0
    last_improvement = 0
    
    while iteration < max_iter and temperature > min_temp:
        neighbor = generate_neighbor(current_solution)
        
        current_cost = current_solution.cost
        neighbor_cost = neighbor.cost
        
        if acceptance_probability(current_cost, neighbor_cost, temperature) > random.random():
            current_solution = neighbor
            
            if current_solution.cost < best_solution.cost:
                best_solution = current_solution.copy()
                last_improvement = iteration
                stagnation_counter = 0
                if verbose and iteration % 500 == 0:
                    print(f"Iteration {iteration}: New best = {best_solution.cost:.2f}")
            else:
                stagnation_counter += 1
        
        if stagnation_counter > 1000:
            current_solution = generate_neighbor(best_solution)
            current_solution = generate_neighbor(current_solution)
            stagnation_counter = 0
        
        temperature *= cooling_rate
        iteration += 1
    
    if verbose:
        print(f"Optimization completed. Best cost: {best_solution.cost:.2f}")
        print(f"Last improvement at iteration: {last_improvement}")
    
    return best_solution
