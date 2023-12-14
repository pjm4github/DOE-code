
# local imports
# from request_handler_registry import RequestHandlerRegistry
# from data_source_registry import DataSourceRegistry
# from client_factory import ClientFactory
# from request_handler_interface import RequestHandlerInterface
# from request_handler import RequestHandler
# from request_upload_handler import RequestUploadHandler
# from authorization_handler import AuthorizationHandler
from gov_pnnl_goss.core.ClientFactory import ClientFactory
from gov_pnnl_goss.core.security.AuthorizationHandler import AuthorizationHandler
from gov_pnnl_goss.core.server.DataSourceRegistry import DataSourceRegistry
from gov_pnnl_goss.core.server.RequestHandler import RequestHandler
from gov_pnnl_goss.core.server.RequestHandlerRegistry import RequestHandlerRegistry
from gov_pnnl_goss.core.server.RequestUploadHandler import RequestUploadHandler


class Commands:
    
    def __init__(self):
        self.registry = RequestHandlerRegistry()
        self.ds_registry = DataSourceRegistry()
        self.client_factory = ClientFactory()

    def help(self):
        sb = []
        sb.append("Help for gs commands\n")
        sb.append("  listDataSources - Lists the known datasources that have been registered with the server\n")
        sb.append("  listHandlers - Lists the known request handlers that have been registered with the server.\n")
        print(''.join(sb))

    def show_client_connections(self):
        for c in self.client_factory.list().items():
            print(f"Client id: {c[0]} protocol {c[1]}")

    def list_data_sources(self):
        ds_list = self.ds_registry.get_available()
        for k, v in ds_list.items():
            print(f"name: {k} type: {v}")

    def list_handlers(self):
        for rh in self.registry.list():
            if isinstance(rh, RequestHandler):
                handler = rh
                for k, v in handler.get_handles().items():
                    print(f"RequestHandler: {handler.__class__.__name__} handles: {k} authorized by: {v}")
            elif isinstance(rh, RequestUploadHandler):
                handler = rh
                for k, v in handler.get_handler_data_types().items():
                    print(f"RequestUploadHandler: {handler.__class__.__name__} handles data: {k} authorized by: {v}")
            elif isinstance(rh, AuthorizationHandler):
                handler = rh
                print(f"AuthorizationHandler registered: {handler.__class__.__name__}")

#     def echo(self, message):
#         request = EchoRequest(message)
#         self.registry.handle(request)
    
#     def get_echo_handler(self):
#         handler = self.registry.get_handler(EchoRequest)
#         print(functions"handler is null: {not handler}")
#         if handler:
#             print(functions"Found handler: {handler.__class__.__name__}")
