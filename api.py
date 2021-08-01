import flask
from flask import request, jsonify
from database import Conn

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    db = Conn()
    all = db.get_all()
    return jsonify(all)


if __name__ == '__main__':
    app.run(host='0.0.0.0')