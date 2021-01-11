from flask import Flask

app = Flask(__name__)

images = []

# POST /images  {location:}
@app.route('/images', methods=['POST'])
def create_image():
    return 'creating image...'

# GET /images
@app.route('/images')
def list_images():
    return 'listing images...'

# DELETE /images/<string:id>
@app.route('/images/<string:id>', methods=['DELETE'])
def delete_image(id):
    return 'deleting image {}...'.format(id)

app.run(port=5000)