#!/usr/bin/env python

# WS client example

import asyncio
import random
import websockets

current_state = [0,'',False, 0]

def start():
    return '''{ "team": "krosch"}'''

def sendGoto(goto, car):
    return '{ "goto": "'+str(goto)+'", "car": "'+car+'" }'

def run():
    async def hello(current_state):
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
                current_state[1] = 'sad'
                current_state[0] += 1

            if current_state[0] == 1:
                greeting = await websocket.recv()
                print(f"< {greeting}")
                current_state[0] += 1

            if current_state[0] == 2:
                routes = await websocket.recv()
                print(f"< {routes}")
                current_state[0] += 1


            while True:
                if current_state[0] == 3:
                    current_state[3] = random.randint(0, 9)
                    goto = sendGoto(current_state[3],"btr")
                    print(f"> {goto}")
                    await websocket.send(goto)
                    current_state[0] += 1

                if current_state[0] == 4:
                    if current_state[3] == 1:
                        teamsum = await  websocket.recv()
                        print(f"< {teamsum}")
                    current_state[0] += 1

                if current_state[0] == 5:
                    points = await  websocket.recv()
                    print(f"< {points}")
                    current_state[0] += 1

                if current_state[0] == 6:
                    traffic = await  websocket.recv()
                    print(f"< {traffic}")
                    current_state[0] = 3

    asyncio.get_event_loop().run_until_complete(hello(current_state))

if __name__ == '__main__':
    while True :
        try:
            run()
        except:
            current_state[2] = True

