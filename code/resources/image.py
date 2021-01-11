from flask import request
from flask_restful import Resources
from http import HTTPStatus
from models.image import Image, image_list

class ImageListResource(Resource):
    def get(self):
        return {'data': image_list}, HTTPStatus.OK

    def post(self):
        data = request.get_json()
        new_image = Image(location=data['location'])
        image_list.append(new_image)
        return new_image.data, HTTPStatus.CREATED


class ImageResource(Resource):
    def delete(self, image_id):
        for image in image_list:
            if image['id'] == image_id:
                image_list.remove(image)
                return {}, HTTPStatus.NO_CONTENT
        return {'message': 'image not found'}, HTTPStatus.NOT_FOUND

class ImageCompareResource(Resource):
    # pass