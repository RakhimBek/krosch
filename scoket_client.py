#!/usr/bin/env python

# WS client example

import asyncio
import random
import websockets
import json

# status / token / need recovery connect/ allcarsum
from clusterize import get_regions
from networkx_util import routes_to_graph, points_map, traffic_to_graph

current_state = [0, '', False, 0]
# save mode close soket  -  pos,car, было отправлено
saveMode = [0, '', False]
# cars[name] = [position, carsum]
cars = {}
# routes
routes = []
# points
points = []
# traffic
traffic = []

# контекст
context = {
    "traffic": {},
    "routes": {},
    "cars": {},
    "last_traffic": {},
    "points": {},
    "visited": set()
}


def start():
    return '''{ "team": "krosch"}'''


def sendGoto(goto, car):
    return '{ "goto": "' + str(goto) + '", "car": "' + car + '" }'


def run():
    async def hello():
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:

            if current_state[2] == True:
                await websocket.send(current_state[1])
                print(f"> {current_state[1]}")
                current_state[2] = False

            # Client: {"team": "Имя команды"}
            name = start()
            if current_state[0] == 0:
                await websocket.send(name)
                print(f"> {name}")
                current_state[0] = 1

            # Server: { "token" : "dd76b4f8191893288054f74385a07e5f", ...
            if current_state[0] == 1:
                greeting = await websocket.recv()
                print(f"< {greeting}")
                request = json.loads(greeting)
                current_state[1] = request["token"]
                carsJ = request["cars"]
                for car in carsJ:
                    cars[car] = [0, 0]
                current_state[0] = 2

            # Server: { "routes":[{"a":0,"b":1,"time":1 ...
            if current_state[0] == 2:
                routesR = await websocket.recv()
                print(f"< {routesR}")
                routes_json = json.loads(routesR)["routes"]
                context["routes"] = routes_to_graph(routes_json)
                current_state[0] = 3

            # Server: { "points":[{"p":0,"money":13966},{"p ...
            if current_state[0] == 3:
                pointsR = await websocket.recv()
                print(f"< {pointsR}")
                context["points"] = points_map(json.loads(pointsR)["points"])
                current_state[0] = 4

            # Server: { "traffic":[{"a":0,"b":1,"jam":"1.46"},{"a"...
            if current_state[0] == 4:
                trafficR = await websocket.recv()
                print(f"< {trafficR}")
                context["traffic"] = traffic_to_graph(json.loads(trafficR)["traffic"])

                current_state[0] = 5
                # кластеризация
                context["regions"] = get_regions(context["routes"], context["traffic"], 1000)

            while True:
                # Client: { "goto": 2, "car": "sb0" }
                if current_state[0] == 5:
                    if saveMode[2] == False:
                        saveMode[0] = random.randint(0, 9)
                        saveMode[1] = "btr"
                        saveMode[2] = True
                    goto = sendGoto(saveMode[0], saveMode[1])
                    saveMode[2] = False
                    print(f"> {goto}")
                    await websocket.send(goto)
                    current_state[0] = 6

                # Server: {"teamsum":115906}
                if current_state[0] == 6:
                    if saveMode[0] == 1:
                        teamsum = await  websocket.recv()
                        current_state[3] += int(json.loads(teamsum)["teamsum"])
                        print(f"< {teamsum}")
                    current_state[0] = 7

                # Server: { "point": 1, "car": "sb0", "carsum": 0 }
                if current_state[0] == 7:
                    pointR = await  websocket.recv()
                    print(f"< {pointR}")
                    point_json = json.loads(pointR)
                    cars[point_json["car"]] = [point_json["point"], point_json["carsum"]]
                    context["visited"].add(int(point_json["point"]))
                    current_state[0] = 8

                # Server: { "traffic":[{"a":0,"b":1,"jam":"1.40"},{"a":0,"b":3,"jam":"1
                if current_state[0] == 8:
                    trafficR = await  websocket.recv()
                    print(f"< {trafficR}")
                    traffic.clear()
                    traffic.extend(json.loads(trafficR)["traffic"])
                    current_state[0] = 5

    asyncio.get_event_loop().run_until_complete(hello())


if __name__ == '__main__':
    while True:
        #try:
            run()
        #except Exception as e:
        #    print(str(e))
        #    current_state[2] = True
