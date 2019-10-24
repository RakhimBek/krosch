#!/usr/bin/env python

# WS client example

import asyncio
import random
import websockets
import json

# status / token / need recovery connect/ allcarsum
current_state = [0, '' ,False,0]
#save mode close soket  -  pos,car, было отправлено
saveMode = [0,'',False]
# cars[name] = [position, carsum]
cars = {}
#routes
routes = []
#points
points = []
#traffic
traffic = []

def start():
    return '''{ "team": "krosch"}'''

def sendGoto(goto, car):
    return '{ "goto": "'+str(goto)+'", "car": "'+car+'" }'

def run():
    async def hello():
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:

            if current_state[2] == True:
                await websocket.send(current_state[1])
                print(f"> {current_state[1]}")
                current_state[2] = False

            name = start()
            if current_state[0] == 0 :
                await websocket.send(name)
                print(f"> {name}")
                current_state[0] += 1

            if current_state[0] == 1:
                greeting = await websocket.recv()
                print(f"< {greeting}")
                request = json.loads(greeting)
                current_state[1] = request["token"]
                carsJ = request["cars"];
                for i in range(len(carsJ)):
                    cars[carsJ[i]] = [0,0]
                current_state[0] += 1

            if current_state[0] == 2:
                routesR = await websocket.recv()
                print(f"< {routesR}")
                routes.extend(json.loads(routesR)["routes"])
                current_state[0] += 1

            if current_state[0] == 3:
                pointsR = await websocket.recv()
                print(f"< {pointsR}")
                points.extend(json.loads(pointsR)["points"])
                current_state[0] += 1

            if current_state[0] == 4:
                trafficR = await websocket.recv()
                print(f"< {trafficR}")
                traffic.clear()
                traffic.extend(json.loads(trafficR)["traffic"])
                current_state[0] += 1


            while True:
                if current_state[0] == 5:
                    if saveMode[2] == False:
                        saveMode[0] = random.randint(0, 9)
                        saveMode[1] = "btr"
                        saveMode[2] = True
                    goto = sendGoto(saveMode[0], saveMode[1])
                    saveMode[2] = False
                    print(f"> {goto}")
                    await websocket.send(goto)
                    current_state[0] += 1

                if current_state[0] == 6:
                    if saveMode[0] == 1:
                        teamsum = await  websocket.recv()
                        current_state[3] += int(json.loads(teamsum)["teamsum"])
                        print(f"< {teamsum}")
                    current_state[0] += 1

                if current_state[0] == 7:
                    pointR = await  websocket.recv()
                    print(f"< {pointR}")
                    pointJ = json.loads(pointR)
                    cars[pointJ["car"]] = [pointJ["point"],pointJ["carsum"]]
                    current_state[0] += 1

                if current_state[0] == 8:
                    trafficR = await  websocket.recv()
                    print(f"< {trafficR}")
                    traffic.clear()
                    traffic.extend(json.loads(trafficR)["traffic"])
                    current_state[0] = 5

    asyncio.get_event_loop().run_until_complete(hello())

if __name__ == '__main__':
    while True :
        # try:
            run()
        # except:
        #     current_state[2] = True

