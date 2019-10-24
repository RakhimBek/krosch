import networkx as nx


# import matplotlib.pyplot as plt
# import json
# file = open("json.txt", "r", encoding='utf-8')
# lines = file.readlines()
# routes_ = json.loads(lines[0])['routes']
# points_ = json.loads(lines[1])['points']
# traffic_ = json.loads(lines[2])['traffic']
# plt.axis('off')
# plt.show()


def routes_to_graph(routes):
    g = nx.Graph()
    for route in routes:
        g.add_edge(route["a"], route["b"], weight=route["time"])
    return g


# [{"p":0,"money":0},{"p":1,"money":0}...
def points_map(points_data):
    points = {}
    for point_data in points_data:
        points[point_data["p"]] = point_data["money"]

    return points


def traffic_to_graph(routes):
    g = nx.Graph()
    for route in routes:
        g.add_edge(route["a"], route["b"], weight=route["jam"])
    return g


if __name__ == '__main__':
    traffic = [{"a": 0, "b": 3, "jam": 1.9}, {"a": 0, "b": 5, "jam": 1.2}, {"a": 0, "b": 6, "jam": 1.1}]

    graph = traffic_to_graph(traffic)
    print(graph.number_of_nodes())
    for edge in graph.edges:
        print(edge)

    print(graph.get_edge_data(0, 3))
    print(graph.get_edge_data(3, 0))
