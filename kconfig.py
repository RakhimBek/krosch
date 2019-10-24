# -*- coding: utf-8 -*-
#24.10.2019, created by Egor Eremenko
# all Configuration


server_ip_prod = 'c0194471.ngrok.io'
server_port_prod = '80'

server_ip_test = 'localhost'
server_port_test = '5000'

websockets_host_test = 'localhost'
websockets_port_test = 8765

def test_address():
    return 'http://' + server_ip_test + ':' + server_port_test


def prod_address():
    return 'http://' + server_ip_prod + ':' + server_port_prod