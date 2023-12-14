
import logging

import xml.etree.ElementTree as ET

from gov_pnnl_goss.core.DataError import DataError
from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.core.Request import Request
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class ServerPublisher:

    def __init__(self, session):
        self.session = session
        self.logger = LogManager(ServerPublisher.__name__)

    def send_error(self, error_string, destination):
        err_resp = DataResponse(DataError(error_string))
        err_resp.set_response_complete(True)
        self.send_response(err_resp, destination)

    def send_response(self, response, destination, response_format=None):
        message = None
        if response_format is None:
            message = self.session.createObjectMessage(response)
            # print("Sending response for QueryId: " + response.getId() + " on destination: " + destination)
        elif response_format == Request.RESPONSE_FORMAT.XML:
            # xstream = XStream()
            # xml = xstream.toXML(response.get_data())
            xml = ET.fromstring(response.get_data())
            message = self.session.create_text_message(xml)
        self.logger.debug("Sending response for QueryId: {} on destination: {}".format(response.get_id(), destination))
        self.session.create_producer(destination).send(message)

    def send_event(self, response, destination_name):
        destination = self.session.create_topic(destination_name)
        message = self.session.createObjectMessage(response)
        self.logger.debug("Sending response for QueryId: on destination: {}".format(destination))
        self.session.create_producer(destination).send(message)

    def send_text_event(self, message, destination_name):
        destination = self.session.create_topic(destination_name)
        response = self.session.create_text_message(message)
        self.session.create_producer(destination).send(response)

    def close(self):
        # //		try {
        # //			session.close();
        # //		} catch (JMSException e) {
        # //			print(e);
        # //		}
        self.session.close()
