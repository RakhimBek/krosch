def append_or_insert(clusters, x, y):
    if x in clusters:
        clusters[x].append(y)
    else:
        clusters[x] = [y]

'''
Точки на расстояний size
'''
def clusterize(timed_edges, size):
    clusters = {}
    for edge in timed_edges:
        if edge["time"] <= size:
            a, b = int(edge["a"]), int(edge["b"])
            append_or_insert(clusters, a, b)
            append_or_insert(clusters, b, a)

    return clusters


if __name__ == '__main__':
    print(clusterize([{"a": 0, "b": 3, "time": 9}, {"a": 0, "b": 5, "time": 12}, {"a": 0, "b": 6, "time": 7}], 10))
