import json
import os

import plate_scanner

from flask import Flask

app = Flask(__name__)

cache_file = "server_state.json"


@app.route('/add_by_file/<filename>', methods=['GET'])
def add_by_file(filename):
    images = list()
    if os.path.exists(cache_file):
        images = json.loads(open(cache_file, "r").read())
    result = plate_scanner.run("Car photos/" + filename)
    images.append(result)
    open(cache_file, "w").write(json.dumps(images))
    return json.dumps(result)


@app.route('/scan_image', methods=['PUSH'])
def post_image():
    pass


@app.route('/get_info/<int:number>', methods=['GET'])
def get_info(number=10):
    images = list()
    if os.path.exists(cache_file):
        images = json.loads(open(cache_file, "r").read())
    return json.dumps(images[-number:])


if __name__ == '__main__':
    app.run(port=3000)
