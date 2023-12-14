
# from javax.servlet.http import HttpServletRequest
# from javax.ws.rs import Consumes, POST, Path, Produces
# from javax.ws.rs.core import Context, MediaType
# from org.apache.shiro.authc import AuthenticationException, AuthenticationInfo, UsernamePasswordToken
# from org.apache.shiro.mgt import SecurityManager
# from pnnl.goss.core.server import TokenIdentifierMap
from gov_pnnl_goss.SpecialClasses import AuthenticationException


# @Path("/login")


class LoginService:
    def __init__(self):
        self.security_manager = None
        self.token_map = None

    def start(self):
        pass

    # @POST
    # @Consumes([MediaType.APPLICATION_JSON, MediaType.TEXT_XML])
    # @Produces(MediaType.APPLICATION_JSON)
    def authenticate(self, request, params):
        session_token = None
        try:
            info = self.security_manager.authenticate(params)
            session_token = self.token_map.register_identifier(request.getRemoteAddr(), params.get_username())
        except AuthenticationException as e:
            return "{\"error\": \"Invalid Login\"}"

        return "{\"token\": \"" + session_token + "\"}"
