
import uuid
import io
import pickle


class RESPONSE_FORMAT:
    XML = "XML"
    JSON = "JSON"


class Response:
    serial_version_UID = 8541810525300877513

    def __init__(self):
        self.id = str(uuid.uuid4())
    
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
    
    def sizeof(self):
        byte_output_stream = io.BytesIO()
        pickle.dump(self, byte_output_stream)
        return len(byte_output_stream.getvalue())
