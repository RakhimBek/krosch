from networkx_util import traffic_to_graph, routes_to_graph, distance


def append_or_insert(clusters, x, y):
    if x in clusters:
        clusters[x].append(y)
    else:
        clusters[x] = [y]


# Точки на расстоянии size
def get_regions(timed_edges, traffic, size):
    print(type(size))
    clusters = {}
    for timed_edge in timed_edges.edges:
        a, b = timed_edge[0], timed_edge[1]
        ab = distance(timed_edges, traffic, a, b)
        if ab <= size:
            append_or_insert(clusters, a, b)
            append_or_insert(clusters, b, a)

    return clusters


if __name__ == '__main__':
    times = routes_to_graph([{"a": 0, "b": 3, "time": 9}, {"a": 0, "b": 5, "time": 12}, {"a": 0, "b": 6, "time": 7}])
    jams = traffic_to_graph([{"a": 0, "b": 3, "jam": 1.1}, {"a": 0, "b": 5, "jam": 1.2}, {"a": 0, "b": 6, "jam": 1}])
    print(get_regions(times, jams, 10))
