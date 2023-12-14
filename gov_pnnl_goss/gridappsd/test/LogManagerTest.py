import unittest

from gov_pnnl_goss.SpecialClasses import UsernamePasswordCredentials
from gov_pnnl_goss.core.GossResponseEvent import GossResponseEvent
from gov_pnnl_goss.core.client.ClientServiceFactory import ClientServiceFactory
from gov_pnnl_goss.core.client.GossClient import Protocol
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus, LogMessage


class System:
    pass

import logging


class LogManagerTest(unittest.TestCase):

    def setUp(self):
        client_factory = ClientServiceFactory()
        credentials = UsernamePasswordCredentials("system", "manager")
        self.client = client_factory.create(Protocol.STOMP, credentials)
        self.logger = LogManager(LogManagerTest.__name__)

    def test_send_log_message(self):
        destination = "goss.gridappsd.process.log"
        source = "test"
        request_id = "test request"
        timestamp = str(System.currentTimeMillis())
        log_message = "this is a test"
        log_level = logging.DEBUG
        process_status = ProcessStatus.RUNNING
        store_to_db = True
        log_message_obj = LogMessage(source, request_id, timestamp, log_message, log_level, process_status, store_to_db, None)

        id = str(self.client.getResponse(log_message_obj, destination, None))
        
        def on_message(dummy):
            response = dummy
            self.assertIsNotNone(response.data)

        self.client.subscribe("goss.gridappsd.response.data." + id, GossResponseEvent().onMessage(on_message))


if __name__ == '__main__':
    unittest.main()
