
import logging

from gov_pnnl_goss.core.client.GossClient import JMSException, SystemException, ConnectionCode
from gov_pnnl_goss.core.server.impl.ServerListener import ServerListener
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


# from javax.jms import Session, Destination, MessageConsumer, MessageListener, JMSException
# from pnnl.goss.core.server.impl.server_listener import ServerListener
# from pnnl.goss.core.server.impl.request_handler_registry import RequestHandlerRegistry
# from pnnl.goss.core.server.exception import SystemException, ConnectionCode


class ServerConsumer:
    
    def __init__(self):
        self.logger = LogManager(ServerConsumer.__name__)

    def set_destination(self, destination):
        self.destination = destination
        return self
    
    def set_session(self, session):
        self.session = session
        return self
    
    def set_registry_handler(self, registry):
        self.handler_registry = registry
        return self
    
    def consume(self):
        self.logger.debug("consume")
        try:
            consumer = self.session.createConsumer(self.destination)
            consumer.setMessageListener(
                ServerListener()
                    .set_session(self.session)
                    .set_registry_handler(self.handler_registry)
            )
        except JMSException as e:
            raise SystemException(f"{e}, {ConnectionCode.CONSUMER_ERROR}")
        self.logger.debug("end consume")
        return self
