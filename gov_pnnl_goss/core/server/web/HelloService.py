
from gov_pnnl_goss.core.server.web.Activator import HttpService


class HelloService(HttpService):
    def __init__(self):
        pass

    def register_servlet(self, alias, servlet, init_params, context):
        print("Registering servlet")
    
    def register_resources(self, alias, name, context):
        print("Register Resource")
    
    def unregister(self, alias):
        print("Unregister")
    
    def create_default_http_context(self):
        print("Create Context!")
        return None
