import math
from typing import List, Optional
from copy import deepcopy


class Client:
    def __init__(self, id: int, x: float, y: float, demand: int):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
    
    def __repr__(self):
        return f"Client({self.id}, demand={self.demand})"


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
    
    def is_feasible(self) -> bool:
        for vehicle in self.vehicles:
            if vehicle.load > vehicle.capacity:
                return False
        return True
    
    def get_num_vehicles_used(self) -> int:
        return sum(1 for v in self.vehicles if len(v.route) > 0)
    
    def copy(self):
        return deepcopy(self)
    
    def __repr__(self):
        return f"Solution(cost={self.cost:.2f}, vehicles_used={self.get_num_vehicles_used()}/{len(self.vehicles)})"


def euclidean_distance(node1: Client, node2: Client) -> float:
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

