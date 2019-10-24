#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json

def start():

    return json.loads('''{ "team": "krosch"}''')

def sendGoto(goto, car):
    return '{ "goto": '+str(goto)+', "car": "'+car+'" }'

def run():
    async def hello():
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            name = start()

            await websocket.send(name)
            print(f"> {name}")

            greeting = await websocket.recv()
            print(f"< {greeting}")

            routes = await websocket.recv()
            print(f"< {routes}")

            points = await websocket.recv()
            print(f"< {points}")

            traffic = await websocket.recv()
            print(f"< {traffic}")

            for x in range(6):
                goto = sendGoto(3,"btr")
                print(f"> {goto}")
                await websocket.send(goto)

                points = await  websocket.recv()
                print(f"< {points}")

                traffic = await  websocket.recv()
                print(f"< {traffic}")

    asyncio.get_event_loop().run_until_complete(hello())


if __name__ == '__main__':
    run()
