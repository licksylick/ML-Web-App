import os
import time
from datetime import datetime
import cv2
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S_")


def get_model():
    # TODO load your model here
    model = ''
    return model


def preprocess(image):
    # TODO preprocess image (use transforms etc)
    image = cv2.resize(image, (256, 256))  # example
    return image


def process(model, image):
    # TODO process image with model
    return image


def get_image_w_h(image):
    h, w, _ = image.shape
    return w, h


def remove_old_files(path, last_modified_time):
    for f in os.listdir(path):
        if os.stat(os.path.join(path, f)).st_mtime < time.time() - last_modified_time:
            os.remove(os.path.join(UPLOAD_FOLDER, f))
