from flask import Flask, jsonify, request

app = Flask(__name__)

images = [
    {
        'id': 1,
        'location': 'https://picsum.photos/200'
    }
]

image_id_incrementor = 1

# POST /images  {location:}
@app.route('/images', methods=['POST'])
def create_image():
    global image_id_incrementor 

    request_data = request.get_json()
    image_id_incrementor += 1

    new_image = {
        'id': image_id_incrementor,
        'location': request_data['location'] 
    } 

    images.append(new_image)
    return jsonify(new_image)

# GET /images
@app.route('/images')
def list_images():
    return jsonify({'data': images})

# DELETE /images/<string:id>
@app.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    for image in images:
        if image['id'] == image_id:
            images.remove(image)
            return {}
    return jsonify({'message': 'image not found'})

# GET /images
@app.route('/images')
def get_similarity(image1, image2):
    return 'getting similarity between images...'

app.run(port=5000)