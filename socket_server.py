#!/usr/bin/env python

# WS socket_server example
import kconfig as kfg
import asyncio
import websockets
import json
#required only for tests
import test_responses as rsp

def run():
    async def hello(websocket, path):

        #loading request
        try:
            request = await json.loads(websocket.recv())
        except Exception as e:
            print('Error: ', e)
            return

        print(request[0])

        # parsing request
        if request[0] == 'team':
            token = rsp.test_init_response('token')
            routes = rsp.test_init_response('routes')
            points = rsp.test_init_response('points')
            traffic = rsp.test_init_response('traffic')

            # sending responses
            try:
                await websocket.send(token)
                await websocket.send(routes)
                await websocket.send(points)
                await websocket.send(traffic)
            except Exception as e:
                print('Error: ', e)
                return

        if request[0] == 'goto':
            #parse goto json parameters
            point = int(request['goto'])
            car = str(request['car'])

            #get test responses
            response_list = rsp.test_goto_response(point, car)
            teamsum = response_list[0]
            point = response_list[1]
            traffic = response_list[2]

            # return teamsum only if car goes to point 1 (garage)
            if point == 1:
                try:
                    await websocket.send(teamsum)
                except Exception as e:
                    print('Error: ', e)
                    return

            # return poain and traffic if car goes to other points (garage)
            try:
                await websocket.send(point)
                await websocket.send(traffic)
            except Exception as e:
                print('Error: ', e)
                return

    start_server = websockets.serve(hello, kfg.websockets_host_test, kfg.websockets_port_test)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    run()
