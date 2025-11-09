import random
from typing import List
from src.models import Client, Vehicle, Solution, euclidean_distance


def generate_random_solution(clients: List[Client], depot: Client, num_vehicles: int, vehicle_capacity: int) -> Solution:
    vehicles = [Vehicle(vehicle_capacity, i) for i in range(num_vehicles)]
    unassigned_clients = clients[:]
    random.shuffle(unassigned_clients)
    
    current_vehicle_idx = 0
    for client in unassigned_clients:
        assigned = False
        attempts = 0
        while not assigned and attempts < num_vehicles:
            if vehicles[current_vehicle_idx].add_client(client):
                assigned = True
            else:
                current_vehicle_idx = (current_vehicle_idx + 1) % num_vehicles
                attempts += 1
        
        if not assigned:
            new_vehicle = Vehicle(vehicle_capacity, len(vehicles))
            vehicles.append(new_vehicle)
            vehicles[-1].add_client(client)
    
    return Solution(vehicles, depot)


def generate_nearest_neighbor_solution(clients: List[Client], depot: Client, num_vehicles: int, vehicle_capacity: int) -> Solution:
    vehicles = [Vehicle(vehicle_capacity, i) for i in range(num_vehicles)]
    unassigned = set(clients)
    current_vehicle_idx = 0
    
    while unassigned:
        vehicle = vehicles[current_vehicle_idx]
        
        if len(vehicle.route) == 0:
            current_position = depot
            current_time = depot.ready_time
        else:
            current_position = vehicle.route[-1]
            solution_temp = Solution([vehicle], depot)
            arrival_times, _, feasible = solution_temp.calculate_route_times(vehicle)
            if arrival_times:
                current_time = arrival_times[-1] + current_position.service_time
            else:
                current_time = depot.ready_time
        
        best_client = None
        best_distance = float('inf')
        
        for client in unassigned:
            if vehicle.load + client.demand <= vehicle.capacity:
                travel_time = euclidean_distance(current_position, client)
                arrival_time = current_time + travel_time
                
                if arrival_time <= client.due_time:
                    if travel_time < best_distance:
                        best_distance = travel_time
                        best_client = client
        
        if best_client:
            vehicle.add_client(best_client)
            unassigned.remove(best_client)
        else:
            current_vehicle_idx += 1
            if current_vehicle_idx >= len(vehicles):
                new_vehicle = Vehicle(vehicle_capacity, len(vehicles))
                vehicles.append(new_vehicle)
    
    return Solution(vehicles, depot)


def generate_clarke_wright_solution(clients: List[Client], depot: Client, vehicle_capacity: int) -> Solution:
    savings = []
    
    for i, client_i in enumerate(clients):
        for j, client_j in enumerate(clients[i+1:], i+1):
            saving = (euclidean_distance(depot, client_i) + 
                     euclidean_distance(depot, client_j) - 
                     euclidean_distance(client_i, client_j))
            savings.append((saving, client_i, client_j))
    
    savings.sort(reverse=True, key=lambda x: x[0])
    
    routes = {client: [client] for client in clients}
    loads = {client: client.demand for client in clients}
    
    for saving_value, client_i, client_j in savings:
        route_i = routes[client_i]
        route_j = routes[client_j]
        
        if route_i == route_j:
            continue
        
        if client_i != route_i[0] and client_i != route_i[-1]:
            continue
        if client_j != route_j[0] and client_j != route_j[-1]:
            continue
        
        combined_load = loads[client_i] + loads[client_j]
        if combined_load > vehicle_capacity:
            continue
        
        if client_i == route_i[-1] and client_j == route_j[0]:
            new_route = route_i + route_j
        elif client_i == route_i[0] and client_j == route_j[-1]:
            new_route = route_j + route_i
        elif client_i == route_i[-1] and client_j == route_j[-1]:
            new_route = route_i + route_j[::-1]
        elif client_i == route_i[0] and client_j == route_j[0]:
            new_route = route_i[::-1] + route_j
        else:
            continue
        
        for client in new_route:
            routes[client] = new_route
            loads[client] = combined_load
    
    unique_routes = []
    seen = set()
    for route in routes.values():
        route_id = id(route)
        if route_id not in seen:
            seen.add(route_id)
            unique_routes.append(route)
    
    vehicles = []
    for idx, route in enumerate(unique_routes):
        vehicle = Vehicle(vehicle_capacity, idx)
        for client in route:
            vehicle.add_client(client)
        vehicles.append(vehicle)
    
    return Solution(vehicles, depot)
