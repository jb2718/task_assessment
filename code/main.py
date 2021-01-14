# import cv2
import datetime
import fastapi
import os
import requests
import shutil
import uvicorn

from fastapi import Security, Depends, HTTPException, File, UploadFile
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKey
# from skimage import metrics
from PIL import Image, ImageChops
from typing import Optional, List


API_KEY = "kmrhn74zgzcq4nqb"
API_KEY_NAME = "app_id"
PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = "{}/static".format(PARENT_DIR)

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)



def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header)
):
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Invalid credentials")


def get_similarity(path_to_img1, path_to_img2) -> str:
    # file_path1 = get_path(filename=image1, folder=folder)
    # first_image = cv2.imread(path_to_img1)
    # first_image = open(path_to_img1, 'r')
    # second_image = open(path_to_img2, 'r')
    with open(path_to_img1, "r") as f1:
        with open(path_to_img1, "r") as f2:
            percentage = ImageChops.difference(f1, f2)

    # second_image.close()
    # first_image.close()
    # first_image = cv2.cvtColor(first_image, cv2.COLOR_BGR2GRAY)

    # file_path2 = get_path(filename=image2, folder=folder)
    # second_image = cv2.imread(path_to_img2)
    # second_image = cv2.cvtColor(second_image, cv2.COLOR_BGR2GRAY)

    # similarity_index = metrics.structural_similarity(first_image, second_image)
    # percentage = "{}%".format(similarity_index * 100)
    # return "100%"

    return percentage

def name_file(extension) -> str:
    datetime_object = datetime.datetime.now()
    file_name = "temp_{}.{}".format(datetime_object.strftime("%f"), extension)
    return file_name

def path_to_image(filename):
    return "{}/{}".format(IMAGES_DIR, filename)

def save_image_from_URL(url: str) -> str:
    resp = requests.get(url)
    headers = resp.headers
    
    extension = headers['Content-Type'].split('/')[1]
    temp_file_name = name_file(extension)
    img_path = path_to_image(temp_file_name)

    with open(img_path, "wb") as f:
        f.write(resp.content)

    return temp_file_name


def save_image_from_local(img_file) -> str:
    extension = img_file.filename.split('.')[1]
    temp_file_name = name_file(extension)
    img_path = path_to_image(temp_file_name)

    with open(img_path, "wb") as f:
        shutil.copyfileobj(img_file.file, f)

    return temp_file_name


api = fastapi.FastAPI()


@api.post('/compare/images')
def compare_images(
    img_url1: Optional[str] = None,
    img_url2: Optional[str] = None,
    image1: UploadFile = File(None),
    image2: UploadFile = File(None),
    api_key: APIKey = Depends(get_api_key)
):
    if img_url1 is not None and img_url2 is not None:
        saved_file1 = save_image_from_URL(img_url1)
        saved_file2 = save_image_from_URL(img_url2)
    elif image1 is not None and image2 is not None:
        saved_file1 = save_image_from_local(image1)
        saved_file2 = save_image_from_local(image2)
    else:
        raise HTTPException(status_code=400, detail="BAD REQUEST: Two images required")

    image_x = Image(path_to_image(saved_file1))
    image_y = Image(path_to_image(saved_file2))
    
    percentage = ImageChops.difference() 
    os.remove(path_to_image(saved_file1))
    os.remove(path_to_image(saved_file2))

    return {"data": { "similarity": percentage }}


if __name__ ==  '__main__':
    uvicorn.run(api)