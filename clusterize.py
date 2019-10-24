def append_or_insert(clusters, x, y):
    if x in clusters:
        clusters[x].append(y)
    else:
        clusters[x] = [y]


# Точки на расстоянии size
def clusterize(timed_edges, traffic, size):
    traffic_jam = dict()
    for edge_jam in traffic:
        key = (int(edge_jam["a"]), int(edge_jam["b"]))
        traffic_jam[key] = float(edge_jam["jam"])

    clusters = {}
    for timed_edge in timed_edges:
        a, b = timed_edge["a"], timed_edge["b"]
        distance = traffic_jam[(a, b)] * timed_edge["time"]
        if distance <= size:
            a, b = timed_edge["a"], timed_edge["b"]
            append_or_insert(clusters, a, b)
            append_or_insert(clusters, b, a)

    return clusters


if __name__ == '__main__':
    times = [{"a": 0, "b": 3, "time": 9}, {"a": 0, "b": 5, "time": 12}, {"a": 0, "b": 6, "time": 7}]
    jams = [{"a": 0, "b": 3, "jam": 1.1}, {"a": 0, "b": 5, "jam": 1.2}, {"a": 0, "b": 6, "jam": 1}]
    print(clusterize(times, jams, 10))
