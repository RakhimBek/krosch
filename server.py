''''
< { "team": "Имя команды"}
> { "token" : "12321", "cars:": ["sb1", "sb2"], "level": 1 }
'''
import sys
from flask import Flask, request
import json
app = Flask(__name__)


#@app.route('/')
#def hello_world():
#    return 'Hello World!'

def response_team():
    data = '''{ "token" : "12321", "cars:": ["sb1", "sb2"], "level": 1 }'''
    return data

def response_routes():
    data = '''{"routes": [{a: 1, b, 7, time: 31},
            { a: 6, b, 30, time: 1}, {a: 10, b, 17, time: 12}, ]}'''
    return data

@app.route('/', methods=['POST']) #allow POST requests
def form_example():
    if request.method == 'POST':

        try:
            app.logger.error(str(request.get_json()))
            incoming = json.loads(str(request.get_json()))
        except Exception as e:
            print(e)

        data = response_team()

        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        try:
            return response
        except Exception as e:
            return str(e)



if __name__ == '__main__':
    app.run()
