from src.parser import parse_vrplib, create_clients_and_depot

data = parse_vrplib('instance/VRPLIB/tests/data/C101.txt')
print(f"Name: {data['name']}")
print(f"Depot: {data['depot']}")
print(f"Capacity: {data['capacity']}")
print(f"Nodes: {len(data['nodes'])}")
print(f"First 3 nodes: {data['nodes'][:3]}")
print(f"Time windows: {len(data['time_windows'])}")
print(f"First 3 TW: {data['time_windows'][:3]}")

clients, depot = create_clients_and_depot(data)
print(f"\nParsed {len(clients)} clients")
print(f"Depot: {depot}")
print(f"First client: {clients[0]}")
