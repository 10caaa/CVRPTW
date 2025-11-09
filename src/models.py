import math
from typing import List, Optional
from copy import deepcopy


class Client:
    def __init__(self, id: int, x: float, y: float, demand: int, 
                 ready_time: float = 0, due_time: float = float('inf'), 
                 service_time: float = 0):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.ready_time = ready_time  # a_i : début de la fenêtre temporelle
        self.due_time = due_time      # b_i : fin de la fenêtre temporelle
        self.service_time = service_time  # s_i : temps de service
    
    def __repr__(self):
        return f"Client({self.id}, demand={self.demand}, tw=[{self.ready_time}, {self.due_time}])"


class Vehicle:
    def __init__(self, capacity: int, id: int = 0):
        self.id = id
        self.capacity = capacity
        self.route: List[Client] = []
        self.load = 0
    
    def add_client(self, client: Client) -> bool:
        if self.load + client.demand <= self.capacity:
            self.route.append(client)
            self.load += client.demand
            return True
        return False
    
    def remove_client(self, client: Client):
        if client in self.route:
            self.route.remove(client)
            self.load -= client.demand
    
    def insert_client(self, client: Client, position: int) -> bool:
        if self.load + client.demand <= self.capacity:
            self.route.insert(position, client)
            self.load += client.demand
            return True
        return False
    
    def clear(self):
        self.route = []
        self.load = 0
    
    def __repr__(self):
        return f"Vehicle({self.id}, load={self.load}/{self.capacity}, clients={len(self.route)})"


class Solution:
    def __init__(self, vehicles: List[Vehicle], depot: Client):
        self.vehicles = vehicles
        self.depot = depot
        self.cost = 0.0
        self.calculate_cost()
    
    def calculate_cost(self) -> float:
        total_distance = 0.0
        for vehicle in self.vehicles:
            if len(vehicle.route) == 0:
                continue
            route_distance = euclidean_distance(self.depot, vehicle.route[0])
            for i in range(len(vehicle.route) - 1):
                route_distance += euclidean_distance(vehicle.route[i], vehicle.route[i + 1])
            route_distance += euclidean_distance(vehicle.route[-1], self.depot)
            total_distance += route_distance
        self.cost = total_distance
        return total_distance
    
    def calculate_route_times(self, vehicle: Vehicle) -> tuple[List[float], List[float], bool]:
        """
        Calcule les temps d'arrivée et d'attente pour une route.
        Returns: (arrival_times, waiting_times, is_feasible)
        """
        if len(vehicle.route) == 0:
            return [], [], True
        
        arrival_times = []
        waiting_times = []
        current_time = 0.0
        current_location = self.depot
        
        for client in vehicle.route:
            travel_time = euclidean_distance(current_location, client)
            arrival_time = current_time + travel_time
            
            if arrival_time > client.due_time:
                return arrival_times, waiting_times, False
            
            waiting_time = max(0, client.ready_time - arrival_time)
            service_start = max(arrival_time, client.ready_time)
            
            arrival_times.append(arrival_time)
            waiting_times.append(waiting_time)
            
            current_time = service_start + client.service_time
            current_location = client
        
        return arrival_times, waiting_times, True
    
    def is_feasible(self) -> bool:
        for vehicle in self.vehicles:
            if vehicle.load > vehicle.capacity:
                return False
            _, _, time_feasible = self.calculate_route_times(vehicle)
            if not time_feasible:
                return False
        return True
    
    def is_route_time_feasible(self, vehicle: Vehicle) -> bool:
        _, _, feasible = self.calculate_route_times(vehicle)
        return feasible
    
    def get_num_vehicles_used(self) -> int:
        return sum(1 for v in self.vehicles if len(v.route) > 0)
    
    def copy(self):
        return deepcopy(self)
    
    def get_route_details(self) -> List[dict]:
        routes = []
        for idx, vehicle in enumerate(self.vehicles):
            if len(vehicle.route) > 0:
                arrival_times, waiting_times, feasible = self.calculate_route_times(vehicle)
                total_time = 0
                if len(vehicle.route) > 0:
                    last_client = vehicle.route[-1]
                    total_time = arrival_times[-1] + last_client.service_time + euclidean_distance(last_client, self.depot)
                
                routes.append({
                    'vehicle_id': idx + 1,
                    'clients': [c.id for c in vehicle.route],
                    'load': vehicle.load,
                    'capacity': vehicle.capacity,
                    'num_clients': len(vehicle.route),
                    'arrival_times': arrival_times,
                    'waiting_times': waiting_times,
                    'total_time': total_time,
                    'time_feasible': feasible
                })
        return routes
    
    def __repr__(self):
        return f"Solution(cost={self.cost:.2f}, vehicles_used={self.get_num_vehicles_used()}/{len(self.vehicles)})"


def euclidean_distance(node1: Client, node2: Client) -> float:
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)
