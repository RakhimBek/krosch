import matplotlib.pyplot as plt
import networkx as nx
import json

file = open("json.txt", "r", encoding='utf-8')

lines = file.readlines()
routes_ = json.loads(lines[0])['routes']
points_ = json.loads(lines[1])['points']
traffic_ = json.loads(lines[2])['traffic']

G = nx.Graph()



for route in routes_:
    G.add_edge(route['a'], route['b'], weight=route['time'])

    print(route)

print('')
plt.axis('off')
plt.show()