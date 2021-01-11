image_list = []

def get_next_id():
    if len(image_list) > 0:
        last_image = image_list[-1]
    else:
        return 1

    return last_image['id'] + 1

class Image:
    def __init__(self, location):
        self.id =  get_next_id()
        self.location = location

    @property
    def data(self):
        return {
            'id': self.id,
            'location': self.location
        }