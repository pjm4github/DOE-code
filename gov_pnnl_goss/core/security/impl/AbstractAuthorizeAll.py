
# from request import Request
# from set import Set
# from authorization_handler import AuthorizationHandler
from gov_pnnl_goss.core.security.AuthorizationHandler import AuthorizationHandler


class AbstractAuthorizeAll(AuthorizationHandler):
    
    def is_authorized(self, request, permissions):
        return True
