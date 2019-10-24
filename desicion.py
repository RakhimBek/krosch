from clusterize import clusterize

from networkx_util import routes_to_graph, traffic_to_graph, points_to_graph


# visited - посещенные вершины
# routes - расстояния
# points - точки
# regions - регионы
# current_traffic - текущая дорожная ситуация
# current_point - текущая точка
# car_info - описание машины {id, volume} = {ИД, свободное объем}
def decision(visited, routes, points, regions, current_traffic, current_point, car_info):
    region = regions[current_point]
    remained = [x for x in region if x not in visited]

    weighted_points = []
    for point in remained:
        time = routes.get_edge_data(current_point, point).get("weight")
        jam = current_traffic.get_edge_data(current_point, point).get("weight")
        money = points.get_edge_data(current_point, point).get("weight")
        if money <= car_info["volume"]:
            weight = time * jam + money
            weighted_points.append((point, weight))

    if len(weighted_points) > 0:
        weighted_points.sort(key=lambda x: x[1])
        return {
            "goto": weighted_points[0][0],
            "car": car_info["id"]
        }

    return {
        "goto": 1,
        "car": car_info["id"]
    }


if __name__ == '__main__':
    route_graph = routes_to_graph(
        [{"a": 0, "b": 3, "time": 9}, {"a": 0, "b": 5, "time": 12}, {"a": 0, "b": 6, "time": 7}]
    )
    traffic_graph = traffic_to_graph(
        [{"a": 0, "b": 3, "jam": 1.1}, {"a": 0, "b": 5, "jam": 1.2}, {"a": 0, "b": 6, "jam": 1}]
    )
    point_graph = points_to_graph(
        [{"a": 0, "b": 3, "money": 188}, {"a": 0, "b": 5, "money": 1000}, {"a": 0, "b": 6, "money": 100}]
    )

    clusters = clusterize(route_graph, traffic_graph, 10)
    print(decision([], route_graph, point_graph, clusters, traffic_graph, 0, {"id": "sp0", "volume": 1000}))
