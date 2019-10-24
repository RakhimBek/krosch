#!/usr/bin/env python

# WS client example

import asyncio
import websockets


def run():
    async def hello():
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            name = input("What's your name? ")

            await websocket.send(name)
            print(f"> {name}")

            greeting = await websocket.recv()
            print(f"< {greeting}")

    asyncio.get_event_loop().run_until_complete(hello())


if __name__ == '__main__':
    run()
