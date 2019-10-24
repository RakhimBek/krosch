#!/usr/bin/env python

# WS client example

import asyncio
import random
import websockets

position = 0

def start():
    return '''{ "team": "krosch"}'''

def sendGoto(goto, car):
    return '{ "goto": "'+str(goto)+'", "car": "'+car+'" }'

def run():
    async def hello(position):
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            name = start()
            if position == 0 :
                await websocket.send(name)
                print(f"> {name}")
                position += 1

            if position == 1:
                greeting = await websocket.recv()
                print(f"< {greeting}")
                position += 1

            if position == 2:
                routes = await websocket.recv()
                print(f"< {routes}")
                position += 1

            if position == 3:
                points = await websocket.recv()
                print(f"< {points}")
                position += 1

            if position == 4:
                traffic = await websocket.recv()
                print(f"< {traffic}")
                position += 1

            while True:
                point = random.randint(0,9)
                if position == 5:
                    goto = sendGoto(point,"btr")
                    print(f"> {goto}")
                    await websocket.send(goto)
                    position += 1

                if position == 6:
                    if point == 1:
                        teamsum = await  websocket.recv()
                        print(f"< {teamsum}")
                    position += 1

                if position == 7:
                    points = await  websocket.recv()
                    print(f"< {points}")
                    position += 1

                if position == 8:
                    traffic = await  websocket.recv()
                    print(f"< {traffic}")
                    position = 5

    asyncio.get_event_loop().run_until_complete(hello(position))

if __name__ == '__main__':
    while True :
        run()
