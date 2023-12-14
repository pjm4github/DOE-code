
from gov_pnnl_goss.core.Request import Request
from gov_pnnl_goss.core.RequestAsync import RequestAsync


class RequestHandlerRegistry:
    
    def get_handler(self, request_cls):
        pass
    
    def get_upload_handler(self, data_type):
        pass
    
    def list_handlers(self):
        pass
    
    def handle(self, a, b=None):
        if isinstance(a, Request):
            self.handle_request(request=a)
        elif isinstance(a, RequestAsync):
            self.handle_async_request(request=a)
        elif isinstance(a, str) and b:
            self.handle_data(data_type=a, data=b)
        else:
            raise ValueError("wrong parameters")

    def handle_request(self, request):
        pass
    
    def handle_data(self, data_type, data):
        pass
    
    def handle_async_request(self, request):
        pass
    
    def check_access(self, request, identifier):
        pass

