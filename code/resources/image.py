from flask import request, abort
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from functools import wraps
from http import HTTPStatus
from libs import image_helper
from schemas.image import ImageSchema

image_schema = ImageSchema()

def api_key_required(view_function):
    @wraps(view_function)

    def decorated_function(*args, **kwargs):
        print(request.headers)
        if request.headers.get('x-api-key'):
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


class ImagesCompareResource(Resource):
    @api_key_required
    def post(self):
        json_data = request.get_json()
        files_data = request.files.to_dict()

        if not image_helper.valid_number_of_images(files_data, json_data):
            return {'message': '2 images required'}, 400 
        
        try:
            percentage = image_helper.calculate_similarity(files_data, json_data)
            return {"data": { "similarity": percentage }}
        except UploadNotAllowed:
            return {'message': 'Extension not allowed. Only .jpg, .jpeg, and .png are valid'}, 400
        return {}, 200
        