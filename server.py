''''
< { "team": "Имя команды"}
> { "token" : "12321", "cars:": ["sb1", "sb2"], "level": 1 }
'''

from flask import Flask, request
import json
app = Flask(__name__)


#@app.route('/')
#def hello_world():
#    return 'Hello World!'

@app.route('/', methods=['POST']) #allow POST requests
def form_example():
    if request.method == 'POST': #this block is only entered when the form is submitted

        data = '''{ "token" : "12321", "cars:": ["sb1", "sb2"], "level": 1 }'''
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response



if __name__ == '__main__':
    app.run()
