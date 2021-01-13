from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage

class FileStorageField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs) -> FileStorage:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail()

        return value

        
class ImageSchema(Schema):
    image1 = FileStorageField(required=True)
    image2 = FileStorageField(required=True)