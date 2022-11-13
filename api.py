from flask import Flask, jsonify, request
from flask_cors import CORS
import simulation

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def hello():
    return 'Hello world!'


@app.route('/start-ws', methods=['POST'])
def start_websocket():
    simulation.start_websocket()
    return jsonify({'message': 'Started Websocket'})


@app.route('/run', methods=['POST'])
def test():
    print(request.json)
    simulation.run(request.json)
    return jsonify({'message': 'Started simulation!'})


@app.route('/grid', methods=['POST'])
def grid():
    print(request.json)
    return jsonify(simulation.grid(request.json))
