import json
import networkx as nx
import matplotlib.pyplot as plt
from urllib import request, parse
from kconfig import test_address, prod_address


def open_url(url, data_dict):
    data_json = json.dumps(data_dict, sort_keys=True)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    req = request.Request(url, data_json.encode('utf-8'), method='POST', headers=headers)
    with request.urlopen(req) as response:
        return json.loads(response.read())


def read(data):
    return open_url(get_address(), data)


'''
G = nx.petersen_graph()
plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
plt.subplot(122)
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()
'''


def get_address():
    address = test_address()
    print(address)
    return address


def auth():
    #    {"team": "Имя команды"}
    print(read({"team": "krosch"}))


def traffic():
    req = {
        "traffic": [
            {"a": 1, "b": 7, "jam": 1.0},
            {"a": 6, "b": 30, "jam": 1.5},
            {"a": 10, "b": 17, "jam": 1.9}
        ]
    }

    print(read(req))


def points():
    req = {
        "points": [
            {"p": 0, "money": 1000200},
            {"p": 1, "money": 1000234},
            {"p": 2, "money": 1323200},
            {"p": 3, "money": 1434545},
        ]}

    print(read(req))


def goto():
    req = {"goto": 2, "car": "sb4"}
    print(read(req))


def trafficjam():
    req = {"trafficjam": [
        {"a": 1, "b": 7, "jam": 1.0},
        {"a": 6, "b": 30, "jam": 1.5},
        {"a": 10, "b": 17, "jam": 1.9},
    ]}
    print(read(req))


def reconnect():
    req = {"reconnect": "12321"}
    print(read(req)["reconnect"])


if __name__ == '__main__':
#    auth()
#    traffic()
#    points()
#    goto()
#    trafficjam()
    reconnect()
