#!flask/bin/python
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def api():
    if "action" in request.args:
        action = request.args['action']
        if "start" in action:
            return "This should start the Jenkins container \n"
        elif "stop" in action:
            return "This should stop the Jenkins container \n"
        else:
            return "Not a valid action, chose from start/stop \n"
    else:
	return "API only for action, choices['start', 'stop'] \n"

if __name__ == '__main__':
    app.run(host='0.0.0.0')