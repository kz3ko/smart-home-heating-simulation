from flask import Flask, jsonify, request

from simulation.main import Simulation

app = Flask(__name__)
simulation = Simulation()


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


@app.route('/rooms/<name>', methods=['GET'])
def get_room_data(name: str) -> jsonify:
    try:
        return jsonify(roomData=simulation.get_room(name), status=200)
    except KeyError:
        return jsonify(roomData=[], status=404)


@app.route('/update-room/<name>', methods=['POST'])
def update_room(name: str) -> jsonify:
    room_data = request.get_json()
    simulation.update_room(name, room_data)

    return jsonify(message=f'Updated "{name}" room.', status=200)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
