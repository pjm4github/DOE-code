
import json

from gov_pnnl_goss.SpecialClasses import UsernamePasswordCredentials
from gov_pnnl_goss.core.ClientFactory import ClientFactory
from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.core.GossResponseEvent import GossResponseEvent
from gov_pnnl_goss.core.client.GossClient import Gson, Protocol
from gov_pnnl_goss.core.security.SecurityConfig import SecurityConfig
from gov_pnnl_goss.core.server.DataSourceRegistry import DataSourceRegistry
from gov_pnnl_goss.core.server.RequestHandlerRegistry import RequestHandlerRegistry
from gov_pnnl_goss.core.server.ServerControl import ServerControl
# from gov_pnnl_goss.gridappsd.app.AppManagerImpl import UsernamePasswordCredentials
# from gov_pnnl_goss.core.Client import PROTOCOL
#

class ManagementLauncher:

    def __init__(self):
        self.client_factory = None
        self.server_control = None
        self.security_config = None
        self.handler_registry = None
        self.datasource_registry = None

    class ResponseEvent(GossResponseEvent):

        def __init__(self, client):
            self.client = client
            self.gson = Gson()
            self.client_factory = ClientFactory()
            self.server_control = ServerControl()
            self.security_config = SecurityConfig()
            self.handler_registry = RequestHandlerRegistry()
            self.datasource_registry = DataSourceRegistry()

        def on_message(self, response):
            response_data = "{}"
            if isinstance(response, DataResponse):
                request = response.get_data()
                if request.strip() == "list_handlers":
                    response_data = json.dumps(self.handler_registry.list())
                elif request.strip() == "list_datasources":
                    response_data = json.dumps(self.datasource_registry.get_available())

            print("On message: " + response.to_string())
            self.client.publish("goss/management/response", response_data)

    def start(self):
        try:
            print("START " + self.security_config.get_manager_user() + " " +
                  self.security_config.get_manager_password() + " " + self.security_config)
            client = self.client_factory.create(Protocol.STOMP,
                                                UsernamePasswordCredentials(self.security_config.get_manager_user(),
                                                                            self.security_config.get_manager_password()),
                                                False)
            client.subscribe("topic/goss/management/request", self.ResponseEvent(client))
            client.subscribe("topic/goss/management/go", self.ResponseEvent(client))
        except Exception as e:
            # TODO Auto-generated catch block
            print(e)

    def stop(self):
        print("Stopping ManagementLauncher")
