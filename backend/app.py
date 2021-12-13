from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/home', methods=['GET'])
def home() -> jsonify:
    return jsonify(message='Hello world!', status=200)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
