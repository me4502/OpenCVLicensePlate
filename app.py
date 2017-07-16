import json
import os

from werkzeug.utils import secure_filename

import plate_scanner

from flask import Flask, request, flash, redirect

app = Flask(__name__)

cache_file = "server_state.json"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'Car photos'


@app.route('/add_by_file/<filename>', methods=['GET'])
def add_by_file(filename):
    images = list()
    if os.path.exists(cache_file):
        images = json.loads(open(cache_file, "r").read())
    result = plate_scanner.run("Car photos/" + filename)
    images.append(result)
    open(cache_file, "w").write(json.dumps(images))
    return json.dumps(result)


@app.route('/scan_image', methods=['GET', 'POST'])
def post_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/add_by_file/' + filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/get_info/<int:number>', methods=['GET'])
def get_info(number=10):
    images = list()
    if os.path.exists(cache_file):
        images = json.loads(open(cache_file, "r").read())
    return json.dumps(images[-number:])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(port=3000)
