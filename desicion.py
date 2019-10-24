from clusterize import clusterize


# visited - посещенные вершины
# regions - регионы
# current_point - текущая точка
# car_info - описание машины {id, volume} = {ИД, свободное объем}
def decision(visited, regions, current_point, car_info):
    region = regions[current_point]
    remained = [x for x in region if x not in visited]
    for point in remained:
        return {
            "goto": point,
            "car": car_info["id"]
        }


if __name__ == '__main__':
    clusters = clusterize([{"a": 0, "b": 3, "time": 9}, {"a": 0, "b": 5, "time": 12}, {"a": 0, "b": 6, "time": 7}], 10)
    decision([], clusters, 0, {"id": "sp0"})
