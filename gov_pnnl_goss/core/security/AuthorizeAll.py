
# local import
from gov_pnnl_goss.core.security.AuthorizationHandler import AuthorizationHandler


class AuthorizeAll(AuthorizationHandler):

    def __init__(self):
        pass

    def is_authorized(self, request, permissions):
        return True
