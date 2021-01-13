from flask import Flask
from flask_restful import Api
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads
from resources.image import ImagesCompareResource
from libs.image_helper import IMAGE_SET

app = Flask(__name__)
api = Api(app)
app.config.from_object("default_config")
configure_uploads(app, IMAGE_SET)

api.add_resource(ImagesCompareResource, '/compare/images')

if __name__ == '__main__':
    app.run(port=5000)