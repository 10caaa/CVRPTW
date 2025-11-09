from typing import Dict, List, Tuple
from src.models import Client


def parse_vrplib(file_path: str) -> Dict:
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    data = {
        'name': '',
        'comment': '',
        'type': '',
        'dimension': 0,
        'capacity': 0,
        'edge_weight_type': '',
        'nodes': [],
        'demands': [],
        'depot': 1,
        'num_vehicles': None
    }
    
    section = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('NAME'):
            data['name'] = line.split(':')[1].strip()
        elif line.startswith('COMMENT'):
            data['comment'] = line.split(':')[1].strip()
        elif line.startswith('TYPE'):
            data['type'] = line.split(':')[1].strip()
        elif line.startswith('DIMENSION'):
            data['dimension'] = int(line.split(':')[1].strip())
        elif line.startswith('CAPACITY'):
            data['capacity'] = int(line.split(':')[1].strip())
        elif line.startswith('EDGE_WEIGHT_TYPE'):
            data['edge_weight_type'] = line.split(':')[1].strip()
        elif line.startswith('NODE_COORD_SECTION'):
            section = 'nodes'
        elif line.startswith('DEMAND_SECTION'):
            section = 'demands'
        elif line.startswith('DEPOT_SECTION'):
            section = 'depot'
        elif line.startswith('EOF'):
            break
        elif section == 'nodes':
            parts = line.split()
            if len(parts) == 3:
                node_id, x, y = int(parts[0]), float(parts[1]), float(parts[2])
                data['nodes'].append((node_id, x, y))
        elif section == 'demands':
            parts = line.split()
            if len(parts) == 2:
                node_id, demand = int(parts[0]), int(parts[1])
                data['demands'].append((node_id, demand))
        elif section == 'depot':
            if line != '-1':
                data['depot'] = int(line)
    
    return data


def create_clients_and_depot(data: Dict) -> Tuple[List[Client], Client]:
    clients = []
    depot = None
    
    if len(data['nodes']) == 0 and len(data['demands']) > 0:
        for node_id, demand in data['demands']:
            x, y = 0.0, 0.0
            
            if node_id == data['depot']:
                depot = Client(node_id, x, y, 0)
            else:
                clients.append(Client(node_id, x, y, demand))
    else:
        for node in data['nodes']:
            node_id, x, y = node
            demand = next((d[1] for d in data['demands'] if d[0] == node_id), 0)
            
            if node_id == data['depot']:
                depot = Client(node_id, x, y, 0)
            else:
                clients.append(Client(node_id, x, y, demand))
    
    if depot is None:
        depot_demand = next((d for d in data['demands'] if d[0] == data['depot']), None)
        if depot_demand:
            depot = Client(data['depot'], 0.0, 0.0, 0)
        else:
            raise ValueError("Depot not found in instance data")
    
    return clients, depot


def load_instance(file_path: str) -> Tuple[List[Client], Client, int]:
    data = parse_vrplib(file_path)
    clients, depot = create_clients_and_depot(data)
    capacity = data['capacity']
    
    return clients, depot, capacity

