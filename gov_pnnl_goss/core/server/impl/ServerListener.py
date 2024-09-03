
import logging
from threading import Thread

from gov_pnnl_goss.SpecialClasses import InvalidDestinationException
from gov_pnnl_goss.core.ClientListener import MessageListener
from gov_pnnl_goss.core.DataError import DataError
from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.core.Event import Event
from gov_pnnl_goss.core.RequestAsync import RequestAsync
from gov_pnnl_goss.core.UploadRequest import UploadRequest
from gov_pnnl_goss.core.client.GossClient import ObjectMessage, SecurityConstants, RESPONSE_FORMAT
from gov_pnnl_goss.core.server.impl.ServerPublisher import ServerPublisher
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class ServerListener(MessageListener):

    def __init__(self):
        self.logger = LogManager(ServerListener.__name__)
        self.handler_registry = None
        self.session = None
        self.use_auth = True

    def set_session(self, session):
        self.session = session
        return self

    def set_registry_handler(self, registry):
        self.handler_registry = registry
        return self

    def on_message(self, message1):
        message = message1
        self.logger.debug("Message of global_property_types: " + message1.getClass() + " received")

        def process_message():
            server_publisher = ServerPublisher(self.session)
            username = ""

            try:
                object_message = ObjectMessage(message)
                # Assume that the passed object on the wire is of global_property_types Request.  An error will be thrown
                # if that is not the case.
                request = object_message.getObject()

                self.logger.debug("Handling request global_property_types: " + request.getClass())

                if self.use_auth:
                    if not message.getBooleanProperty(SecurityConstants.HAS_SUBJECT_HEADER):
                        self.logger.error("Identifier not set in message header")
                        server_publisher.send_error("Invalid subject in message!", message.getJMSReplyTo())
                        return

                    identifier = message.getStringProperty(SecurityConstants.SUBJECT_HEADER)
                    username = identifier
                    allowed = self.handler_registry.check_access(request, identifier)

                    if not allowed:
                        self.logger.info("Access denied to " + identifier + " for request global_property_types " + request.getClass().getName())
                        server_publisher.send_error("Access Denied for the requested data", message.getJMSReplyTo())
                        return

                    self.logger.debug("Access allowed to the request")

                if isinstance(request, UploadRequest):
                    upload_request = request
                    data_type = upload_request.get_data_type()
                    data = upload_request.get_data()

                    response = self.handler_registry.handle(data_type, data)
                    response.setId(request.getId())

                    server_publisher.send_response(response, message.getJMSReplyTo())
                    # //TODO: Added capability for event processing without upload. Example - FNCS
                    # /*UploadResponse response = new UploadResponse(true);
                    # response.setId(request.getId());
                    # serverPublisher.sendResponse(response, message.getJMSReplyTo());*/
                    if isinstance(data, Event):
                        data_response = DataResponse()
                        data_response.setUsername(username)
                        data_response.setData(data)
                        server_publisher.send_event(data_response, data.getClass().getName().substring(data.getClass().getName().lastIndexOf(".") + 1))
                        server_publisher.close()
                elif isinstance(request, RequestAsync):
                    request_async = request
                    # AbstractRequestHandler handler = handlerService.getHandler(request);
                    response = self.handler_registry.handle(request)
                    response.set_response_complete(True)
                    response.setUsername(username)
                    response.setId(request.getId())

                    if message.getStringProperty("RESPONSE_FORMAT") is not None:
                        server_publisher.send_response(response, message.getJMSReplyTo(), RESPONSE_FORMAT.valueOf(message.getStringProperty("RESPONSE_FORMAT")))
                    else:
                        server_publisher.send_response(response, message.getJMSReplyTo(), None)

                    while not response.is_response_complete():
                        Thread.sleep(request_async.get_frequency())
                        response = self.handler_registry.handle(request)
                        response.setId(request.getId())

                        if message.getStringProperty("RESPONSE_FORMAT") is not None:
                            server_publisher.send_response(response, message.getJMSReplyTo(), RESPONSE_FORMAT.valueOf(message.getStringProperty("RESPONSE_FORMAT")))
                        else:
                            server_publisher.send_response(response, message.getJMSReplyTo(), None)
                else:
                    response = self.handler_registry.handle(request)
                    # DataResponse response = (DataResponse) ServerRequestHandler.handle(request);
                    response.set_response_complete(True)
                    response.setUsername(username)
                    response.setId(request.getId())

                    if message.getStringProperty("RESPONSE_FORMAT") is not None:
                        server_publisher.send_response(response, message.getJMSReplyTo(), RESPONSE_FORMAT.valueOf(message.getStringProperty("RESPONSE_FORMAT")))
                    else:
                        server_publisher.send_response(response, message.getJMSReplyTo(), None)
                        # print(System.currentTimeMillis())
            except (InvalidDestinationException, Exception) as e:
                response = DataResponse(DataError("Exception occured: " + e.getMessage()))
                response.setUsername(username)
                server_publisher.send_response(response, message.getJMSReplyTo())

            server_publisher.close()
        
        thread = Thread(target=process_message)
        thread.start()
