import datetime
import fastapi
import os
import requests
import uvicorn

from fastapi import Security, Depends, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from typing import Optional


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
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid credentials")

def name_file(extension) -> str:
    datetime_object = datetime.datetime.now()
    filename = "temp_{}.{}".format(datetime_object.strftime("%f"), extension)
    return filename

def save_image_from_URL(url: str) -> str:
    resp = requests.get(url)
    headers = resp.headers
    
    extension = headers['Content-Type'].split('/')[1]
    filename = name_file(extension)
    path_to_file = "{}/{}".format(IMAGES_DIR, filename)

    with open(path_to_file, "wb") as f:
        f.write(resp.content)

    return filename


def save_image_from_local(file_path: str) -> str:
    file_name = os.path.split(file_path)[1]
    ext = os.path.splitext(file_name)[1]

    temp_file_name = name_file(ext)
    # path_to_file = "{}/{}".format(IMAGES_DIR, filename)

    # with open(path_to_file, "wb") as f:
    #     f.write(resp.content)

    # return temp_file_name
    return 'test'


api = fastapi.FastAPI()


@api.get('/compare/images')
def compare_images(api_key: APIKey = Depends(get_api_key)):
    saved_file = save_image_from_URL('https://i.imgur.com/gZKMme4.jpg')
    return saved_file


if __name__ ==  '__main__':
    uvicorn.run(api)