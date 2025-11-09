# Test Plotly + NetworkX Visualisation
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import networkx as nx
import numpy as np

print("✓ Plotly importé")
print("✓ NetworkX importé")
print("✓ Test réussi!")

# Test simple
fig = go.Figure()
fig.add_trace(go.Scatter(x=[0, 1, 2], y=[0, 1, 0], mode='lines+markers', name='Test'))
fig.update_layout(title="Test Plotly")
print("✓ Graphique Plotly créé")

# Test NetworkX
G = nx.Graph()
G.add_node(1, pos=(0, 0))
G.add_node(2, pos=(1, 1))
G.add_edge(1, 2)
print(f"✓ Graphe NetworkX créé: {G.number_of_nodes()} nœuds, {G.number_of_edges()} arêtes")

print("\n🎉 Plotly + NetworkX fonctionnent parfaitement!")
