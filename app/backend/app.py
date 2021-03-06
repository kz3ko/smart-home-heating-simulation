from flask import Flask, jsonify, request
from flask_cors import CORS

from simulation.main import Simulation

app = Flask(__name__)
simulation = Simulation()
CORS(app)


@app.route('/start', methods=['POST'])
def start_simulation() -> jsonify:
    simulation.start()

    return jsonify(message='Simulation started.', status=200)


@app.route('/stop', methods=['POST'])
def stop_simulation() -> jsonify:
    simulation.stop()

    return jsonify(message='Simulation started.', status=200)


@app.route('/rooms', methods=['GET'])
def get_rooms_data() -> jsonify:
    return jsonify(roomsData=simulation.get_rooms(), status=200)


@app.route('/rooms/<int:room_id>', methods=['GET'])
def get_room_data(room_id: int) -> jsonify:
    try:
        return jsonify(roomData=simulation.get_room(room_id), status=200)
    except ValueError:
        return jsonify(roomData=[], status=404)


@app.route('/datetime', methods=['GET'])
def get_datetime() -> jsonify:
    return jsonify(dateTime=str(simulation.datetime), status=200)


@app.route('/settings', methods=['POST'])
def update_settings() -> jsonify:
    settings = request.get_json()
    simulation.set_settings(settings)

    return jsonify(message='Settings updated.', status=200)


@app.route('/update-room/<int:room_id>', methods=['POST'])
def update_room(room_id: int) -> jsonify:
    room_data = request.get_json()
    try:
        simulation.update_room(room_id, room_data)
        return jsonify(message=f'Updated room with "{room_id}" id.', status=200)
    except ValueError:
        return jsonify(message=f'There is no room with "{room_id} id!', status=404)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
