#!/usr/bin/env python

# WS client example 172.30.9.50:3000

import asyncio
import random
import sys

import websockets
import json
import datetime

# status / token / need recovery connect/ allcarsum
from clusterize import get_regions
from desicion import decision
from networkx_util import routes_to_graph, points_map, traffic_to_graph

CAR_VOLUME = 1_000_000;
new_state = [0, datetime.datetime.now()]
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
all_data = [False,False,False]

# контекст
context = {
    "traffic": {},
    "routes": {},
    "cars": {},
    "last_traffic": {},
    "points": {},
    "visited": {0, 1},
    "current_point": 0,
    "current_car": ""
}


def start():
    return '''{ "team": "krosch"}'''


def sendGoto(goto, car):
    return '{ "goto": "' + str(goto) + '", "car": "' + car + '" }'
#
async def writer(websocket):
    while True:
        if new_state[0] == 0 :
            name = start()
            await websocket.send(name)
            print(f"> {name}")
            new_state[0] = 1
            new_state[1] = datetime.datetime.now()

        if current_state[2] == True:
            await websocket.send('{ "reconnect" : "' + current_state[1] + '"}')
            new_state[0] = 3
            new_state[1] = datetime.datetime.now()

async def reader(websocket):
    while True:
        message = await websocket.recv()
        messageJ = json.loads(message)
        if "token" in messageJ:
            # Server: { "token" : "dd76b4f8191893288054f74385a07e5f", ...
            new_state[0] = 2
            new_state[1] = datetime.datetime.now()
            current_state[1] = messageJ["token"]
            cars_json = messageJ["cars"]
            for car_id in cars_json:
                context["cars"][car_id] = {"id": car_id, "volume": CAR_VOLUME}
        if "routes" in messageJ:
            # Server: { "routes":[{"a":0,"b":1,"time":1 ...
            routes_json = messageJ["routes"]
            context["routes"] = routes_to_graph(routes_json)
        if "points" in messageJ:
            # Server: { "points":[{"p":0,"money":13966},{"p ...
            context["points"] = points_map(messageJ["points"])
        if "traffic" in messageJ:
            # Server: { "traffic":[{"a":0,"b":1,"jam":"1.46"},{"a"...
            context["traffic"] = traffic_to_graph(messageJ["traffic"])
        if "point" in messageJ:
            # Server: { "point": 1, "car": "sb0", "carsum": 0 }
            context["current_point"] = messageJ["point"]
            context["cars"][messageJ["car"]] = {"id": messageJ["car"],
                                                  "volume": CAR_VOLUME - messageJ["carsum"]}
            context["visited"].add(int(messageJ["point"]))
        print(f"> {message}")

# await asyncio.gather(reader(websocket),
#                                  writer(websocket))

def run():
    async def hello():
        while True:
            uri = "ws://172.30.9.50:8080/race"
            async with websockets.connect(uri) as websocket:

                if current_state[2] == True:
                    token = '{"reconnect": "'+ current_state[1] +'"}';
                    await websocket.send(token)
                    print(f"> {token}")
                    current_state[2] = False

                # Client: {"team": "Имя команды"}
                name = start()
                if current_state[0] == 0:
                    await websocket.send(name)
                    print(f"> {name}")
                    current_state[0] = 1

            # Server: { "token" : "dd76b4f8191893288054f74385a07e5f", ...
            if current_state[0] == 1:
                request = await receive(websocket)
                current_state[1] = request["token"]
                cars_json = request["cars"]
                for car_id in cars_json:
                    context["cars"][car_id] = {"id": car_id, "volume": CAR_VOLUME}

                context["current_car"] = request["cars"][0]
                current_state[0] = 2

            # Server: { "routes":[{"a":0,"b":1,"time":1 ...
            if current_state[0] == 2:
                traffic_json = await receive(websocket)
                if "routes" in traffic_json:
                    routes_json = traffic_json["routes"]
                    context["routes"] = routes_to_graph(routes_json)
                    all_data[0]=True

            # Server: { "points":[{"p":0,"money":13966},{"p ...
                if "points" in traffic_json:
                    context["points"] = points_map(traffic_json["points"])
                    all_data[1] = True

            # Server: { "traffic":[{"a":0,"b":1,"jam":"1.46"},{"a"...
                if "traffic" in traffic_json:
                    context["traffic"] = traffic_to_graph(traffic_json["traffic"])
                    context["regions"] = get_regions(context["routes"], context["traffic"], 1000)
                    all_data[2] = True
                if all_data[0] and all_data[1] and all_data[2]:
                    current_state[0] = 5
                # кластеризация


            while True:
                # Client: { "goto": 2, "car": "sb0" }
                if current_state[0] == 5:

                    if saveMode[2] == False:
                        decision_result = decision(
                            visited=context["visited"],
                            routes=context["routes"],
                            points=context["points"],
                            regions=context["regions"],
                            current_traffic=context["traffic"],
                            current_point=context["current_point"],
                            car_info=context["cars"][context["current_car"]],
                            remained_distance=500
                        )
                        saveMode[0] = decision_result["goto"]
                        saveMode[1] = decision_result["car"]
                        saveMode[2] = True

                    goto = sendGoto(saveMode[0], saveMode[1])
                    print(f"> {goto}")
                    await websocket.send(goto)
                    saveMode[2] = False
                    current_state[0] = 6

                # Server: {"teamsum":115906}
                if current_state[0] == 6:
                    if saveMode[0] == 1:
                        teamsum_json = await receive(websocket)
                        current_state[3] += int(teamsum_json["teamsum"])
                    current_state[0] = 7

                # Server: { "point": 1, "car": "sb0", "carsum": 0 }
                if current_state[0] == 7:
                    point_json = await receive(websocket)
                    if "point" in point_json:
                        context["current_point"] = point_json["point"]
                        context["cars"][point_json["car"]] = {"id": point_json["car"],
                                                              "volume": CAR_VOLUME - point_json["carsum"]}
                        context["visited"].add(int(point_json["point"]))
                    current_state[0] = 8

                # Server: { "traffic":[{"a":0,"b":1,"jam":"1.40"},{"a":0,"b":3,"jam":"1
                if current_state[0] == 8:
                    traffic_json = await receive(websocket)
                    traffic.clear()
                    traffic.extend(traffic_json["traffic"])
                    current_state[0] = 5

    async def receive(websocket):
        data = await websocket.recv()
        print(f"raw data: {data}")
        json_data = json.loads(data)
        print(f"< {json_data}")
        return json_data

    asyncio.get_event_loop().run_until_complete(hello())


if __name__ == '__main__':
    while True:
        try:
            run()
        except Exception as e:
            e.__traceback__.print_exc(file=sys.stdout)
            if  current_state[1] == '':
                current_state[0] = 0
            else:
                current_state[2] = True

