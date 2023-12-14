
#from request_handler_interface import RequestHandlerInterface
from gov_pnnl_goss.SpecialClasses import RequestHandlerInterface


class AuthorizationHandler(RequestHandlerInterface):
    def __init__(self):
        pass

    def is_authorized(self, request, permissions):
        pass
