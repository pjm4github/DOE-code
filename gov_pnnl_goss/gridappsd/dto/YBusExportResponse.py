# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json

class YBusExportResponse:
    serial_version_UID = 1

    def __init__(self):
        self.y_parse = []
        self.node_list = []
        self.summary = []
        self.vnom = []
    
    def get_y_parse(self):
        return self.y_parse
    
    def set_y_parse(self, y_parse):
        self.y_parse = y_parse
    
    def get_node_list(self):
        return self.node_list
    
    def set_node_list(self, node_list):
        self.node_list = node_list
    
    def get_summary(self):
        return self.summary
    
    def set_summary(self, summary):
        self.summary = summary
    
    def get_vnom(self):
        return self.vnom
    
    def set_vnom(self, vnom):
        self.vnom = vnom
    
    def __str__(self):
        return json.dumps(self.__dict__)
