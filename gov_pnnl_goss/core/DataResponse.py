
import json
from json import JSONEncoder, JSONDecoder
from typing import Any

from gov_pnnl_goss.core.DataError import DataError
from gov_pnnl_goss.core.Response import Response


class DataResponse(Response):
    serial_version_UID = 3555288982317165831

    def __init__(self, username: str=None, data: Any=None, destination: str=None, reply_destination: str=None):
        super().__init__()
        self.username = username
        self.data = data
        self.destination = destination
        self.reply_destination = reply_destination

        self.error = None
        self.response_complete = False

    def was_data_error(self):
        return self.is_error()

    def is_error(self):
        return isinstance(self.data, DataError)

    def set_error(self, error):
        self.error = error

    def get_error(self):
        return self.error

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def is_response_complete(self):
        return self.response_complete

    def set_response_complete(self, response_complete):
        self.response_complete = response_complete

    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    def get_reply_destination(self):
        return self.reply_destination

    def set_reply_destination(self, reply_destination):
        self.reply_destination = reply_destination

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_string):
        return JSONDecoder().decode(json_string)

class InterfaceAdapter:
    CLASSNAME = "CLASSNAME"
    DATA = "DATA"

    def deserialize(self, json_element, _, json_deserialization_context):
        if isinstance(json_element, str):
            return json_element
        else:
            json_object = json_element
            class_name = json_object.get(self.CLASSNAME).getAsString()

            if "java.lang.String" == class_name:
                return json_object.get(self.DATA).getAsString()
            else:
                klass = self.get_object_class(class_name)
                return json_deserialization_context.deserialize(json_object.get(self.DATA), klass)

    def get_object_class(self, class_name):
        co = globals().get(class_name, None)
        if not co:
            raise ValueError("GClass not found")
        return co

    def serialize(self, json_element, _, json_serialization_context):
        json_object = globals().get(json_element, {})
        json_object.addProperty(self.CLASSNAME, json_element.__class__.__name__)
        json_object.add(self.DATA, json_serialization_context.serialize(json_element))
        return json_object
