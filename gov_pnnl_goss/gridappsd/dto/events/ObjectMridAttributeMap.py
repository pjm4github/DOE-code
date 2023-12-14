# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106

class ObjectMridAttributeMap:
    serial_version_UID = 1

    def __init__(self, object_mrid=None, attribute=None):
        self.object_mrid = object_mrid
        self.attribute = attribute
    
    def get_object_mrid(self):
        return self.object_mrid
    
    def set_object_mrid(self, object_mrid):
        self.object_mrid = object_mrid
    
    def get_attribute(self):
        return self.attribute
    
    def set_attribute(self, attribute):
        self.attribute = attribute
