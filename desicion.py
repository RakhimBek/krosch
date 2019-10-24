from clusterize import clusterize

# visited - посещенные вершины
# regions - регионы
# current_point - текущая точка
# car_info - описание машины {id, volume} = {ИД, свободное объем}
from networkx_util import routes_to_graph, traffic_to_graph


def decision(visited, regions, current_traffic, current_point, car_info):
    region = regions[current_point]
    remained = [x for x in region if x not in visited]
    for point in remained:
        return {
            "goto": point,
            "car": car_info["id"]
        }


if __name__ == '__main__':
    times = routes_to_graph([{"a": 0, "b": 3, "time": 9}, {"a": 0, "b": 5, "time": 12}, {"a": 0, "b": 6, "time": 7}])
    traffic = traffic_to_graph([{"a": 0, "b": 3, "jam": 1.1}, {"a": 0, "b": 5, "jam": 1.2}, {"a": 0, "b": 6, "jam": 1}])

    clusters = clusterize(times, traffic, 10)
    print(decision([], clusters, traffic, 0, {"id": "sp0"}))
