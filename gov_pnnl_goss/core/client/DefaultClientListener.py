
import logging

from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.core.GossResponseEvent import GossResponseEvent
from gov_pnnl_goss.core.Response import Response
from gov_pnnl_goss.core.client.GossClient import ObjectMessage, TextMessage
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


# from .goss_response_event import GossResponseEvent
# from .response import Response
# from .data_response import DataResponse


class DefaultClientListener:
    def __init__(self, event: GossResponseEvent):
        self.logger = LogManager("DefaultClientListener")
        self.logger.debug("Instantiating")
        self.response_event = event

    def on_message(self, message):
        try:
            if isinstance(message, ObjectMessage):
                self.logger.debug("message of type: %s received" % message.__class__)
                object_message = message
                if isinstance(object_message.get_object(), Response):
                    response = object_message.get_object()
                    self.response_event.on_message(response)
                else:
                    response = DataResponse(object_message.get_object())
                    if response.get_destination() is None:
                        response.set_destination(message.get_JMS_destination().to_string())
                    self.response_event.on_message(response)
            elif isinstance(message, TextMessage):
                text_message = message
                response = DataResponse(text_message.get_text())
                if response.get_destination() is None:
                    response.set_destination(message.get_JMS_destination().to_string())
                self.response_event.on_message(response)
        except Exception as e:
            self.logger.error("ERROR Receiving message", e)
            e.print_stack()
