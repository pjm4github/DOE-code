
# from javax.jms import MessageConsumer, Session, Destination, JMSException
from gov_pnnl_goss.core.client.GossClient import JMSException


class DefaultClientConsumer:
    def __init__(self, client_listener, session, destination):
        try:
            self.message_consumer = session.create_consumer(destination)
            self.message_consumer.message_listener = client_listener
        except Exception as e:
            print(e)

    def close(self):
        try:
            self.message_consumer.close()
        except JMSException as e:
            print(e)
