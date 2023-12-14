
import logging
import random
import time

from gov_pnnl_goss.core.client.GossClient import Session, JMSException, SecurityConstants


# from javax.jms import JMSException, Message, TextMessage, ObjectMessage, BlobMessage, Session, MessageProducer, Destination
# from security_constants import SecurityConstants

class Destination:
    pass


class DefaultClientPublisher:
    
    def __init__(self, session: Session, username: str = None):
        self.session = session
        self.username = username
        if session:
            try:
                self.producer = session.createProducer(None)
            except JMSException as e:
                logging.error(e)

    def close(self):
        try:
            self.producer.close()
        except JMSException as e:
            logging.error(e)

    def send_message(self, message, destination: Destination, reply_destination: Destination, response_format):
        message_obj = None
        
        if isinstance(message, str):
            message_obj = self.session.createTextMessage(message)
        else:
            message_obj = self.session.createObjectMessage(message)
        
        message_obj.setBooleanProperty(SecurityConstants.HAS_SUBJECT_HEADER, bool(self.username))
        
        if self.username:
            message_obj.setStringProperty(SecurityConstants.SUBJECT_HEADER, self.username)
        
        message_obj.setJMSReplyTo(reply_destination)
        correlation_id = self.create_random_string()
        message_obj.setJMSCorrelationID(correlation_id)
        message_obj.setJMSDestination(destination)
        
        if response_format:
            message_obj.setStringProperty("RESPONSE_FORMAT", response_format)
        
        logging.debug("Sending: {} on destination: {}".format(message, destination))
        self.producer.send(destination, message_obj)

    def publish(self, destination: Destination, data):
        message = None
        
        if isinstance(data, str):
            message = self.session.createTextMessage(data)
        else:
            message = self.session.createObjectMessage(data)
        
        if message:
            message.setBooleanProperty(SecurityConstants.HAS_SUBJECT_HEADER, bool(self.username))
        
        if self.username:
            message.setStringProperty(SecurityConstants.SUBJECT_HEADER, self.username)
        
        logging.debug("Publishing: {} on destination: {}".format(data.__class__, destination))
        self.producer.send(destination, message)

    def publish_blob_message(self, destination: Destination, file):
        activeMQSession = self.session
        message = activeMQSession.createBlobMessage(file)
        
        message.setBooleanProperty(SecurityConstants.HAS_SUBJECT_HEADER, bool(self.username))
        
        if self.username:
            message.setStringProperty(SecurityConstants.SUBJECT_HEADER, self.username)
        
        logging.debug("Publishing on destination: {}".format(destination))
        self.producer.send(destination, message)
    
    def create_random_string(self):
        random_long = random.Random(time.time()).randint(0, 2**32)
        return format(random_long, 'x')

