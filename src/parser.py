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
        'time_windows': [],
        'service_times': [],
        'depot': 1,
        'num_vehicles': None
    }
    
    if file_path.endswith('.txt'):
        return parse_solomon_format(file_path, data)
    
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


def parse_solomon_format(file_path: str, data: Dict) -> Dict:
    """Parse Solomon format (.txt) files with time windows"""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    data['name'] = lines[0].strip()
    data['type'] = 'CVRPTW'
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('VEHICLE'):
            i += 2  
            parts = lines[i].split()
            if len(parts) >= 2:
                data['num_vehicles'] = int(parts[0])
                data['capacity'] = int(parts[1])
            i += 1
        
        elif line.startswith('CUSTOMER'):
            i += 3  
            while i < len(lines):
                line_data = lines[i].strip()
                if not line_data:
                    i += 1
                    continue
                    
                parts = line_data.split()
                if len(parts) >= 7:
                    cust_no = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    demand = int(parts[3])
                    ready_time = float(parts[4])
                    due_time = float(parts[5])
                    service_time = float(parts[6])
                    
                    data['nodes'].append((cust_no, x, y))
                    data['demands'].append((cust_no, demand))
                    data['time_windows'].append((cust_no, ready_time, due_time))
                    data['service_times'].append((cust_no, service_time))
                    
                    if cust_no == 0:
                        data['depot'] = 0
                    
                    i += 1
                else:
                    break
            break
        else:
            i += 1
    
    data['dimension'] = len(data['nodes'])
    return data


def create_clients_and_depot(data: Dict) -> Tuple[List[Client], Client]:
    clients = []
    depot = None
    
    time_windows_dict = {tw[0]: (tw[1], tw[2]) for tw in data.get('time_windows', [])}
    service_times_dict = {st[0]: st[1] for st in data.get('service_times', [])}
    
    if len(data['nodes']) == 0 and len(data['demands']) > 0:
        for node_id, demand in data['demands']:
            x, y = 0.0, 0.0
            ready_time, due_time = time_windows_dict.get(node_id, (0, float('inf')))
            service_time = service_times_dict.get(node_id, 0)
            
            if node_id == data['depot']:
                depot = Client(node_id, x, y, 0, ready_time, due_time, service_time)
            else:
                clients.append(Client(node_id, x, y, demand, ready_time, due_time, service_time))
    else:
        for node in data['nodes']:
            node_id, x, y = node
            demand = next((d[1] for d in data['demands'] if d[0] == node_id), 0)
            ready_time, due_time = time_windows_dict.get(node_id, (0, float('inf')))
            service_time = service_times_dict.get(node_id, 0)
            
            if node_id == data['depot']:
                depot = Client(node_id, x, y, 0, ready_time, due_time, service_time)
            else:
                clients.append(Client(node_id, x, y, demand, ready_time, due_time, service_time))
    
    if depot is None:
        depot_demand = next((d for d in data['demands'] if d[0] == data['depot']), None)
        if depot_demand:
            ready_time, due_time = time_windows_dict.get(data['depot'], (0, float('inf')))
            service_time = service_times_dict.get(data['depot'], 0)
            depot = Client(data['depot'], 0.0, 0.0, 0, ready_time, due_time, service_time)
        else:
            raise ValueError("Depot not found in instance data")
    
    return clients, depot


def load_instance(file_path: str) -> Tuple[List[Client], Client, int]:
    data = parse_vrplib(file_path)
    clients, depot = create_clients_and_depot(data)
    capacity = data['capacity']
    
    return clients, depot, capacity
