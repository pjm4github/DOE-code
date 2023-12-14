import json


class RemoteApplicationRegistrationResponse:
    def __init__(self):
        self.heartbeat_topic = None
        self.start_control_topic = None
        self.status_control_topic = None
        self.stop_control_topic = None
        self.error_topic = None
        self.unregister_topic = None
        self.application_id = None
        self.properties = {}

    def get_application_id(self):
        return self.application_id
    
    def set_application_id(self, application_id):
        self.application_id = application_id

    def get_status_control_topic(self):
        return self.status_control_topic

    def set_status_control_topic(self, status_control_topic):
        self.status_control_topic = status_control_topic

    def set_stop_control_topic(self, stop_control_topic):
        self.stop_control_topic = stop_control_topic

    def get_unregister_topic(self):
        return self.unregister_topic
    
    def set_unregister_topic(self, unregister_topic):
        self.unregister_topic = unregister_topic
    
    def get_heartbeat_topic(self):
        return self.heartbeat_topic
    
    def set_heartbeat_topic(self, heartbeat_topic):
        self.heartbeat_topic = heartbeat_topic
    
    def get_start_control_topic(self):
        return self.start_control_topic
    
    def set_start_control_topic(self, start_control_topic):
        self.start_control_topic = start_control_topic
    
    def get_stop_control_topic(self):
        return self.stop_control_topic
    
    def set_control_stop_topic(self, stop_control_topic):
        self.stop_control_topic = stop_control_topic
    
    def get_error_topic(self):
        return self.error_topic
    
    def set_error_topic(self, error_topic):
        self.error_topic = error_topic

    def __getitem__(self, key):
        # Define how property access works when using square brackets
        #         response['errorTopic'] = "Error"
        #         response['heartbeatTopic'] = "/queue/" + GridAppsDConstants.topic_remoteapp_heartbeat + "." + app_id
        #         response['startControlTopic'] = "/topic/" + GridAppsDConstants.topic_remoteapp_start + "." + app_id
        #         response['stopControlTopic']
        #         self.heartbeat_topic = None
        #         self.start_control_topic = None
        #         self.status_control_topic = None
        #         self.stop_control_topic = None
        #         self.error_topic = None
        #         self.unregister_topic = None
        #         self.application_id = None
        if key == 'applicationId':
            return self.application_id
        elif key == 'errorTopic':
            return self.error_topic
        elif key == 'heartbeatTopic':
            return self.heartbeat_topic
        elif key == 'startControlTopic':
            return self.start_control_topic
        elif key == 'stopControlTopic':
            return self.stop_control_topic
        elif key in self.properties:
            print("Warning the key is not a standard key!")
            return self.properties[key]
        else:
            raise KeyError(f"Property '{key}' not found")

    def __setitem__(self, key, value):
        # Define how property assignment works when using square brackets
        if key == 'applicationId':
            self.application_id = value
        elif key == 'errorTopic':
            self.error_topic = value
        elif key == 'heartbeatTopic':
            self.heartbeat_topic = value
        elif key == 'startControlTopic':
            self.start_control_topic = value
        elif key == 'stopControlTopic':
            self.stop_control_topic = value
        elif key in self.properties:
            print("Warning setting a non standard key value!")
            self.properties[key] = value
        else:
            print("Warning creating a non standard key and setting its value!")
            self.properties[key] = value

    def __delitem__(self, key):
        # Define how property deletion works when using 'del' keyword
        if key in self.properties:
            del self.properties[key]
        else:
            raise KeyError(f"Property '{key}' not found")

    def keys(self):
        # Return a list of property keys
        return list(self.properties.keys())

    def items(self):
        # Return a list of (key, value) pairs for properties
        return list(self.properties.items())

    def __repr__(self):
        # Customize the string representation of the class
        return repr(self.properties)

    def __str__(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj['start_control_topic'] == None:
            raise ValueError("Expected attribute StartTopic not found")
        return obj
