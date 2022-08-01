import cv2
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import sys
from pathlib import Path
from config import UPLOAD_FOLDER, REMOVE_TIME
from utils import allowed_file, get_current_time, get_model, preprocess, process, get_image_w_h, remove_old_files

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

try:
    sys.path.remove(str(parent))
except ValueError:
    pass


@app.route('/')
def upload_form():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        remove_old_files(UPLOAD_FOLDER, REMOVE_TIME)

        now = get_current_time()
        filename = now + secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        model = get_model()

        image = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
        w, h = get_image_w_h(image)

        image = preprocess(image)
        res_image = process(model, image)

        res_image = cv2.resize(res_image, (w, h), interpolation=cv2.INTER_AREA)

        cv2.imwrite(os.path.join(UPLOAD_FOLDER, now + os.path.basename(filename)), res_image)

        os.remove(os.path.join(UPLOAD_FOLDER, os.path.basename(filename)))

        #TODO if your model has an answer (text prediction), you can show prediction text on webpage
        answer = 'model answer'
        flash('Result: ' + answer)

        filename = os.path.join(now + os.path.basename(filename))
        return render_template('home.html', filename=filename)

    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static',
                    filename='uploads/' + filename, code=301))


@app.route('/about', methods=['GET', 'POST'])
def about_page():
    if request.method == 'POST':
        return redirect(url_for('upload_form'))
    return render_template('about.html')


if __name__ == "__main__":
    app.run(port=5085)