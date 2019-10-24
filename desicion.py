from clusterize import clusterize
from networkx_util import routes_to_graph, traffic_to_graph, points_to_graph


# расстояние между данными точками
def distance(routes, current_traffic, from_point, to_point):
    home_time = routes.get_edge_data(from_point, to_point).get("weight")
    home_jam = current_traffic.get_edge_data(from_point, to_point).get("weight")
    return home_jam * home_time


# Расстояние до целевой точки от данной
def home_distance_from(routes, current_traffic, from_point):
    return distance(routes, current_traffic, from_point, 1)


# visited - посещенные вершины
# routes - расстояния
# points - точки
# regions - регионы
# current_traffic - текущая дорожная ситуация
# current_point - текущая точка
# car_info - описание машины {id, volume} = {ИД, свободное объем}
# remained_distance - оставшееся расстояние(время)
def decision(visited, routes, points, regions, current_traffic, current_point, car_info, remained_distance):
    region = regions[current_point]
    remained = [x for x in region if x not in visited]
    home_distance = home_distance_from(routes, current_traffic, current_point)
    weighted_points = []
    for point in remained:
        xy_distance = distance(routes, current_traffic, current_point, point)
        yz_distance = home_distance_from(routes, current_traffic, point)
        if (xy_distance + yz_distance) > remained_distance:
            return {
                "goto": 1,
                "car": car_info["id"]
            }

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
        [{"a": 0, "b": 1, "time": 9}, {"a": 0, "b": 2, "time": 12}, {"a": 1, "b": 2, "time": 7}]
    )
    traffic_graph = traffic_to_graph(
        [{"a": 0, "b": 1, "jam": 1.1}, {"a": 0, "b": 2, "jam": 1.2}, {"a": 1, "b": 2, "jam": 1}]
    )
    point_graph = points_to_graph(
        [{"a": 0, "b": 1, "money": 188}, {"a": 0, "b": 2, "money": 1000}, {"a": 1, "b": 2, "money": 100}]
    )

    clusters = clusterize(route_graph, traffic_graph, 10)
    print(decision([0, 1], route_graph, point_graph, clusters, traffic_graph, 0, {"id": "sp0", "volume": 1000}, 100))
