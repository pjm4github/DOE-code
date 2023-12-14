from enum import Enum
from io import IOBase

from stomp import exception
import mqueue as mqueue


class File(IOBase):
    pass


class StompJmsTempQueue(mqueue):
    pass


class ShiroPlugin:
    pass


class SslBrokerService:
    pass


class BrokerService:
    pass


class SystemException(Exception):
    pass


class IllegalStateException(Exception):
    pass


class Gson:
    pass


class ActiveMQConnectionFactory:
    pass


class StompJmsConnectionFactory:
    def __init__(self):
        self.broker_url = ""
        self.username = ""
        self.password = ""
        self.conn = None

    def set_broker_URI(self, b):
        self.broker_url = b
        # setBrokerURI("tcp://localhost:61613")

    def set_username(self, u):
        self.username = u
        # .setUsername("system")

    def set_password(self, p):
        self.password = p
        # connection_factory.setPassword("manager")

    def create_connection(self):
        self.conn = "DUMMY"
        # connection = connection_factory.createConnection()


class Session:
    pass


class ObjectMessage:
    pass


class TextMessage:
    pass


class StompJmsBytesMessage:
    pass


class StompJmsDestination:
    pass


class JsonSyntaxException(Exception):
    pass


class StompJmsTextMessage:
    pass


class StompJmsTopic:
    pass


class ConnectionCode:
    pass


JMSException = exception.ConnectFailedException


class MACVerifier:
    pass


class UsernamePasswordToken:
    pass


class UnauthTokenBasedRealm:
    pass


class PermissionResolverAware:
    pass


class AuthenticationToken:
    pass


class UsernamePasswordCredentials:
    def __init__(self, un, pw):
        pass
    pass

class JndiLdapRealm:
    pass


class JndiLdapContextFactory:
    pass


class PrincipalCollection:
    pass


class AuthorizationInfo:
    pass


class SimpleAuthorizationInfo:
    pass


class AuthenticationInfo:
    pass


class PermissionResolver:
    pass


class ServiceDependency:
    pass


class RequestHandlerInterface:
    pass


class TimeUnit:
    pass


class ConfigurationException(Exception):
    pass


class SQLException(Exception):
    pass


class InvalidDestinationException(Exception):
    pass


class HttpService:
    pass


class HttpContext:
    pass


class Filter:
    pass


class Hashtable(dict):
    def __init__(self):
        super().__init__()

    def put(self, key, value):
        self[key] = value


class HttpServlet:

    def do_get(self, req, resp):
        pass


class FilterConfig:
    pass


class HttpServletRequest:
    pass


class StringBuilder:
    pass


class HttpServletResponse:
    pass


class InputStreamReader:
    pass


class IOException(Exception):
    pass


class JsonObject:
    pass


class AuthenticationException(Exception):
    pass


class Status:
    pass


class HttpServletRequestWrapper:
    pass


class ServletInputStream:
    pass


class ByteArrayOutputStream:
    pass


class ByteArrayInputStream:
    pass


class IOUtils:
    pass


class ReadListener:
    pass


class MessageListener:
    pass


class RequestLogMessage:
    # Define the RequestLogMessage class as needed, including attributes for log message request
    pass


class ResultSet:
    pass

class RuntimeException(Exception):
    pass