from flask import Flask
from flask_restful import Api
from resources.image import ImageListResource, ImageResource, ImageCompareResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ImageListResource, '/images')
api.add_resource(ImageResource, '/images/<int:image_id>')
# TODO: api.add_resource(ImageCompareResource, '/images/compare')


if __name__ == '__main__':
    app.run(port=5000)