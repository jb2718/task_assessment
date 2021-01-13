import cv2
import datetime
import numpy as np
import os
import requests

from flask_uploads import UploadSet
from PIL import Image, ImageChops
from skimage import metrics
from typing import Union
from werkzeug.datastructures import FileStorage

IMAGE_FORMATS = tuple('jpg jpeg png'.split())
IMAGE_SET = UploadSet('images', IMAGE_FORMATS)

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = "{}/static/images".format(PARENT_DIR)

def calculate_similarity(files_data, urls_payload):
    folder = 'assets'
    paths = save_images(files_data, urls_payload, folder=folder)
    filename1 = get_basename(paths['image1'])
    filename2 = get_basename(paths['image2'])
    return compare_images(filename1, filename2, folder)


def compare_images(image1, image2, folder):
    file_path1 = get_path(filename=image1, folder=folder)
    first_image = cv2.imread(file_path1)
    first_image = cv2.cvtColor(first_image, cv2.COLOR_BGR2GRAY)

    file_path2 = get_path(filename=image2, folder=folder)
    second_image = cv2.imread(file_path2)
    second_image = cv2.cvtColor(second_image, cv2.COLOR_BGR2GRAY)

    similarity_index = metrics.structural_similarity(first_image, second_image)
    percentage = "{}%".format(similarity_index * 100)

    # Clean up files
    os.remove(file_path1)
    os.remove(file_path2)

    return percentage


def save_from_url_to_filestorage(image_url, folder):
    req = requests.get(image_url)
    headers = req.headers
    
    # Name file
    extension = headers['Content-Type'].split('/')[1]
    datetime_object = datetime.datetime.now()
    filename = "temp_{}.{}".format(datetime_object.strftime("%f"), extension)
    filepath = "{}/{}".format(IMAGES_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(req.content)

    with open(filepath, "rb") as f:
        file_storage = FileStorage(f)
        saved_file = save_image(file_storage, folder=folder)

    os.remove(filepath)
    return saved_file


def get_basename(file: Union[str, FileStorage]) -> str:
    # extracts name of image from full path
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_path(filename: str = None, folder: str = None) -> str:
    return IMAGE_SET.path(filename, folder)


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    # takes file name or FileStorage and returns file name
    if isinstance(file, FileStorage):
        return file.filename
    return file


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    return IMAGE_SET.save(image, folder, name)


def save_images(file_data, urls_payload, folder: str = None):
    saved_files = {}

    if len(file_data) == 2:
        # files_to_upload = file_data
        saved_files['image1'] = save_image(file_data['image1'], folder=folder)
        saved_files['image2'] = save_image(file_data['image2'], folder=folder)
    elif len(file_data) == 1:
        # default the filestorage object to 'image1'
        for key in file_data.keys():
            file_to_save = {}
            file_to_save['image1'] = file_data[key]
            saved_files['image1'] = save_image(file_to_save['image1'], folder=folder)

        for key in urls_payload.keys():
            saved_files['image2'] = save_from_url_to_filestorage(urls_payload[key], folder)
    else:
        saved_files['image1'] = save_from_url_to_filestorage(urls_payload['image1_location'], folder)
        saved_files['image2'] = save_from_url_to_filestorage(urls_payload['image2_location'], folder)

    return saved_files


def valid_number_of_images(file_data, urls_payload):
    num_urls = 0
    num_files = 0

    if urls_payload:
        num_urls = len(urls_payload)

    if file_data:
        num_files = len(file_data)

    return num_files + num_urls == 2