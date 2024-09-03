import encodings
import threading
import logging
from datetime import time
from enum import Enum
import ssl
import pika
import ssl
import json
import uuid

from stomp import Connection, ConnectionListener, exception

# from gov_pnnl_goss.SpecialClasses import Session, JMSException, SystemException, ActiveMQConnectionFactory, \
#     StompJmsConnectionFactory, ObjectMessage, TextMessage, StompJmsBytesMessage, StompJmsDestination, \
#     StompJmsTextMessage, JsonSyntaxException, ConnectionCode, StompJmsTempQueue, StompJmsTopic, IllegalStateException, \
#     Gson

from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.core.GossCoreConstants import GossCoreConstants
from gov_pnnl_goss.core.GossResponseEvent import GossResponseEvent
from gov_pnnl_goss.core.Response import Response, RESPONSE_FORMAT
from gov_pnnl_goss.core.ResponseError import ResponseError
from gov_pnnl_goss.core.client.ClientConfiguration import ClientConfiguration
from gov_pnnl_goss.core.client.DefaultClientConsumer import DefaultClientConsumer
from gov_pnnl_goss.core.client.DefaultClientListener import DefaultClientListener
from gov_pnnl_goss.core.client.DefaultClientPublisher import DefaultClientPublisher
from gov_pnnl_goss.core.security.SecurityConstants import SecurityConstants
from gov_pnnl_goss.core.security.jwt.UserRepositoryImpl import ResponseEvent
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class PROTOCOL(Enum):
    STOMP = "STOMP"
    OPENWIRE = "OPENWIRE"
    SSL = "SSL"


class ActiveMQSslConnectionFactory:
    def __init__(self, broker_uri, trust_store, trust_store_password):
        """
        # Usage
            broker_uri = "ssl://your-broker-uri"
            trust_store = "/path/to/truststore"
            trust_store_password = "truststore-password"

            factory = ActiveMQSslConnectionFactory(broker_uri, trust_store, trust_store_password)
            connection = factory.create_connection()
            connection.connect()

        :param broker_uri:
        :param trust_store:
        :param trust_store_password:
        """
        self.broker_uri = broker_uri
        self.trust_store = trust_store
        self.trust_store_password = trust_store_password

    def create_connection(self):

        stomp_port = 61613
        conn = Connection([(self.broker_uri, stomp_port )])


        # Set SSL options, including the SSL version
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

        # You can further customize SSL options if needed
        # ssl_context.load_cert_chain(certfile='client.crt', keyfile='client.key')

        # Set SSL parameters for the connection
        conn.set_ssl(for_hosts=[(self.broker_uri, 61613)],
                     key_file=None, cert_file=None,
                     ca_certs=self.trust_store,
                     ssl_context=ssl_context,
                     # ssl_version=Connection.ssl_version_sslv23,
                     ssl_version_certfile=None, ssl_version_keyfile=None,
                     ssl_cert_password=self.trust_store_password)


        # Use the SSL context when connecting
        # conn.set_ssl(for_hosts=[(stomp_host, stomp_port)], ssl_context=ssl_context)

        # Connect to the STOMP server
        # conn.connect(username=stomp_user, password=stomp_pass, wait=True)

        return conn
# from gov_pnnl_goss.core.Client import Client
# class GossClient(Client):
#
#
#     log = logging.getLogger('GossClient')
#     SYSTEM_USERNAME = "system"
#
#
#     def __init__(self, protocol, credentials, openwire_uri, stomp_uri, trust_store_password=None, trust_store=None,
#                  use_token=False):
#         self.uuid = uuid.uuid4()
#         self.protocol = protocol
#         self.credentials = credentials
#         self.broker_uri = openwire_uri
#         self.stomp_uri = stomp_uri
#         self.trust_store_password = trust_store_password
#         self.trust_store = trust_store
#         self.use_token = use_token
#         self.client_publisher = None
#         self.connection = None
#         self.session = None
#         self.used = False
#         self.threads = []
#         self.token = None

        # Other methods would be translated similarly, following the structure and logic of the Java code.
        # This includes createSslSession, createSession, getResponse, subscribe, publish, close, getSession,
        # getTemporaryDestination, getDestination, getToken, setCredentials, getProtocol, reset, isUsed, setUsed,
        # getClientId, and the nested ResponseEvent class.
# class GossClient(ConnectionListener):
#     # logger = LogManager(__name__)
#     # 	//TODO should probably be configurable
#     SYSTEM_USERNAME = "system"
#
#     def __init__(self, protocol, credentials,
#                  openwire_uri, stomp_uri, trust_store_password, trust_store,
#                  use_token=False):
#         self.uuid = uuid.uuid4()
#         self.protocol = protocol
#         self.credentials = credentials
#         self.broker_uri = openwire_uri
#         self.stomp_uri = stomp_uri
#         self.trust_store_password = trust_store_password
#         self.trust_store = trust_store
#         self.use_token = use_token
#         self.logger = LogManager(__name__)
#         # More stuff
#         self.connection = None
#         self.session = None
#         self.used = False
#         #self.trust_store = trust_store
#         #self.trust_store_password = trust_store_password
#         self.threads = []
#         self.protocol = None
#         self.credentials = None
#         self.token = None
#         #self.use_token = False
#         self.client_publisher = None

    # def create_ssl_session(self):
    #     cf = ActiveMQSslConnectionFactory(self.broker_uri, self.trust_store, self.trust_store_password)
    #     # TODO needs to be refactored to use stomp
    #     # cf.set_ssl(for_hosts=[(self.broker_uri, 61613)],
    #     #              key_file=None, cert_file=None,
    #     #              ca_certs=self.trust_store, ssl_version=stomp.ssl_version_sslv23,
    #     #              ssl_version_certfile=None, ssl_version_keyfile=None,
    #     #              ssl_cert_password=self.trust_store_password)
    #     #
    #     # cf.setTrustStore(self.trust_store)
    #     # cf.setTrustStorePassword(self.trust_store_password)
    #
    #     # if self.token is not None:
    #     #     cf.setUserName(self.token)
    #     #     cf.setPassword("")
    #     # elif self.credentials is not None:
    #     #     cf.setUserName(self.credentials.getUserPrincipal().getName())
    #     #     cf.setPassword(self.credentials.getPassword())
    #
    #     try:
    #         connection = cf.create_connection()  # cf.createConnection()
    #         if connection is None:
    #             raise exception.ConnectFailedException("Session error when connecting")
    #         connection.connect(username=self.SYSTEM_USERNAME,
    #                            password=self.trust_store_password,
    #                            wait=True)
    #         connection.start()
    #         session = connection.createSession(False, Session.AUTO_ACKNOWLEDGE)
    #         if session is None:
    #             raise exception.ConnectFailedException("Session error when connecting") #  ConnectionCode.SESSION_ERROR)
    #
    #         if self.credentials is not None:
    #             self.client_publisher = DefaultClientPublisher(self.credentials.getUserPrincipal().getName(), session)
    #         else:
    #             self.client_publisher = DefaultClientPublisher(session)
    #
    #         self.connection = connection
    #         self.session = session
    #
    #     except JMSException as e:
    #         raise SystemException(e)

    def create_ssl_session(self):
        try:
            cf = ActiveMQSslConnectionFactory(self.broker_uri)
            cf.trust_store = self.trust_store
            cf.trust_store_password = self.trust_store_password

            if self.token is not None:
                cf.user_name = self.token
                cf.password = ""
            elif self.credentials is not None:
                cf.user_name = self.credentials.user_principal.name
                cf.password = self.credentials.password

            self.connection = cf.create_connection()
            if self.connection is None:
                raise SystemException(ConnectionCode.CONNECTION_ERROR)

            self.connection.start()
            self.session = self.connection.create_session(False, Session.AUTO_ACKNOWLEDGE)
            if self.session is None:
                raise SystemException(ConnectionCode.SESSION_ERROR)

            username = self.credentials.user_principal.name if self.credentials else None
            self.client_publisher = DefaultClientPublisher(username, self.session) if username else DefaultClientPublisher(self.session)
        except Exception as e:
            raise SystemException.wrap(e)


    def create_session(self):
        try:
            if self.token:
                username = "tmp"
            elif self.credentials:
                username = self.credentials.user_principal.name
                if self.use_token and self.SYSTEM_USERNAME != username:
                    self.token = self.get_token(self.credentials)
            else:
                self.log.info("No credentials provided")

            if self.protocol == PROTOCOL.SSL:
                self.create_ssl_session()
            elif self.protocol == PROTOCOL.OPENWIRE:
                factory = ActiveMQConnectionFactory(self.broker_uri)
                if self.token:
                    factory.user_name = self.token
                    factory.password = ""
                elif self.credentials:
                    factory.user_name = username
                    factory.password = self.credentials.password
                self.connection = factory.create_connection()
            elif self.protocol == PROTOCOL.STOMP:
                factory = StompJmsConnectionFactory()
                factory.broker_uri = self.stomp_uri.replace("stomp", "tcp")
                if self.token:
                    self.connection = factory.create_connection(self.token, "")
                elif self.credentials:
                    self.connection = factory.create_connection(username, self.credentials.password)
                else:
                    self.connection = factory.create_connection()

            self.connection.exec_start()
            self.session = self.connection.create_session(False, Session.AUTO_ACKNOWLEDGE)

            if username:
                self.client_publisher = DefaultClientPublisher(username, self.session)
            else:
                self.client_publisher = DefaultClientPublisher(self.session)
        except Exception as e:
            raise SystemException.wrap(e)


    #
    # def create_session(self):
    #     self.config = ClientConfiguration().set("TCP_BROKER", self.broker_uri)
    #     username = None
    #
    #     if self.token is not None:
    #         # todo
    #         username = "tmp"
    #     elif self.credentials is not None:
    #         self.config.set("CREDENTIALS", self.credentials)
    #         username = self.credentials.getUserPrincipal().getName()
    #
    #         if self.use_token and self.SYSTEM_USERNAME != self.credentials.getUserPrincipal().getName():
    #             self.token = self.get_token(self.credentials)
    #
    #     if self.protocol == Protocol.SSL:
    #         self.create_ssl_session()
    #     elif self.protocol == Protocol.OPENWIRE:
    #         if self.credentials is not None:
    #             self.logger.debug("Creating OPENWIRE client session for " + str(self.credentials.getUserPrincipal()))
    #         else:
    #             self.logger.debug("Creating OPENWIRE client session without credentials")
    #
    #         factory = ActiveMQConnectionFactory(self.broker_uri)
    #
    #         if self.token is not None:
    #             factory.setUserName(self.token)
    #             factory.setPassword("")
    #         elif self.credentials is not None:
    #             factory.setUserName(self.credentials.getUserPrincipal().getName())
    #             factory.setPassword(self.credentials.getPassword())
    #
    #         self.connection = factory.createConnection()
    #     elif self.protocol == Protocol.STOMP:
    #         factory = StompJmsConnectionFactory()
    #         factory.setBrokerURI(self.stomp_uri.replace("stomp", "tcp"))
    #
    #         if self.token is not None:
    #             self.connection = factory.createConnection(self.token, "")
    #         elif self.credentials is not None:
    #             self.connection = factory.createConnection(self.credentials.getUserPrincipal().getName(), self.credentials.getPassword())
    #         else:
    #             self.connection = factory.createConnection()
    #
    #     try:
    #         self.connection.start()
    #     except Exception as e:
    #         self.logger.error("Error while starting connection: " + str(e))
    #         # TODO: handle exception
    #
    #     self.session = self.connection.createSession(False, Session.AUTO_ACKNOWLEDGE)
    #
    #     if username is not None:
    #         self.client_publisher = DefaultClientPublisher(username, self.session)
    #     else:
    #         self.client_publisher = DefaultClientPublisher(self.session)

    def get_response(self, message, topic, response_format):
        if self.protocol is None:
            self.protocol = PROTOCOL.OPENWIRE

        if topic is None:
            return ResponseError("topic cannot be null")
        if message is None:
            return ResponseError("message cannot be null")

        try:
            reply_destination = self.get_temporary_destination(self.session)
            destination = self.session.create_queue(topic)

            self.log.debug(f"Creating consumer for destination {reply_destination}")
            client_consumer = DefaultClientConsumer(self.session, reply_destination)
            try:
                self.client_publisher.send_message(message, destination, reply_destination, response_format)
                response_message = client_consumer.message_consumer.receive()

                if isinstance(response_message, ObjectMessage):
                    object_message = response_message
                    if isinstance(object_message.object, Response):
                        response = object_message.object
                elif isinstance(response_message, TextMessage):
                    response = response_message.text
                elif isinstance(response_message, StompJmsBytesMessage):
                    stomp_message = response_message
                    buffer = stomp_message.content
                    response = buffer.decode()[buffer.decode().index(":") + 1:]
                else:
                    response = None

                return response
            finally:
                if client_consumer is not None:
                    client_consumer.close()
        except Exception as e:
            raise SystemException.wrap(e).set("topic", topic).set("message", message)


    # def get_response(self, message, topic, response_format):
    #     """
    #         /**
    #          * Sends request and gets response for synchronous communication.
    #          *
    #          * @param request
    #          *            instance of pnnl.goss.core.Request or any of its subclass.
    #          * @return return an Object which could be a pnnl.goss.core.DataResponse,
    #          *         pnnl.goss.core.UploadResponse or pnnl.goss.core.DataError.
    #          * @throws IllegalStateException
    #          *             when GossCLient is initialized with an GossResponseEvent.
    #          *             Cannot synchronously receive a message when a MessageListener
    #          *             is set.
    #          * @throws JMSException
    #          */
    #     :param message:
    #     :param topic:
    #     :param response_format:
    #     :return:
    #     """
    #
    #     if self.protocol is None:
    #         self.protocol = Protocol.OPENWIRE
    #
    #     if topic is None:
    #         # TODO handle with an ErrorCode lookup!
    #         return ResponseError("topic cannot be None")
    #     if message is None:
    #         # TODO handle with an ErrorCode lookup!
    #         return ResponseError("message cannot be None")
    #
    #     response = None
    #     reply_destination = self.get_temporary_destination(self.get_session())
    #     destination = self.session.createQueue(topic)
    #
    #     self.logger.debug("Creating consumer for destination " + str(reply_destination))
    #     client_consumer = DefaultClientConsumer(self.session, reply_destination)
    #     try:
    #         self.client_publisher.send_message(message, destination, reply_destination, response_format)
    #         response_message = client_consumer.get_message_consumer().receive()
    #         if isinstance(response_message, ObjectMessage):
    #             object_message = response_message
    #             if isinstance(object_message.getObject(), Response):
    #                 response = object_message.getObject()
    #         elif isinstance(response_message, TextMessage):
    #             response = response_message.getText()
    #         elif isinstance(response_message, StompJmsBytesMessage):
    #             stomp_message = response_message
    #             buffer = stomp_message.getContent()
    #             response = buffer.to"".substring(buffer.to"".indexOf(":") + 1)
    #     except JMSException as e:
    #         SystemException.wrap(e).set("topic", topic).set("message", message)
    #     finally:
    #         if client_consumer is not None:
    #             client_consumer.close()
    #     return response
    #
    # def on_message(self, headers, body):
    #     pass
    #
    # def on_error(self, headers, message):
    #     pass
    #
    # def on_disconnected(self):
    #     pass
    #
    # def on_connected(self, headers, body):
    #     pass
    #
    # def on_receipt(self, headers, message):
    #     pass
    #
    # def on_sent(self, headers, message):
    #     pass
    #
    # def generate_config(self, parameters, out, process_id, username):
    #     pass
    #
    # def send_request(self, message, topic, response_format):
    #     pass
    #
    # def subscribe(self, topic_name, event):
    #     """
    #     /**
    #     * Lets the client subscribe to a Topic of the given name for event based
    #     * communication.
    #     *
    #     * @param topicName
    #     *            throws IllegalStateException if GossCLient is not initialized
    #     *            with an GossResponseEvent. Cannot asynchronously receive a
    #     *            message when a MessageListener is not set. throws JMSException
    #     */
    #     :param topic_name:
    #     :param event:
    #     :return:
    #     """
    #     if event is None:
    #         raise ValueError("event cannot be None")
    #
    #     destination = None
    #
    #     if self.protocol == Protocol.OPENWIRE:
    #         destination = self.get_destination(topic_name, self.connection, self.session)
    #         DefaultClientConsumer(DefaultClientListener(ResponseEvent(self)), self.session, destination)
    #     elif self.protocol == Protocol.STOMP:
    #         def stomp_message_listener():
    #             destination = StompJmsDestination(topic_name)
    #             consumer = DefaultClientConsumer(self.session, destination)
    #
    #             while self.session is not None:
    #                 try:
    #                     msg = consumer.get_message_consumer().receive(10000)
    #
    #                     if isinstance(msg, StompJmsBytesMessage):
    #                         stomp_message = msg
    #                         buffer = stomp_message.get_content()
    #                         message = buffer.to"".split(":")[1]
    #
    #                         data_response = DataResponse(message)
    #                         data_response.set_destination(msg.get_jms_destination().to"")
    #
    #                         if msg.get_jms_reply_to() is not None:
    #                             data_response.set_reply_destination(msg.get_jms_reply_to())
    #
    #                         if msg.get_boolean_property(SecurityConstants.HAS_SUBJECT_HEADER):
    #                             username = msg.get_string_property(SecurityConstants.SUBJECT_HEADER)
    #                             data_response.set_username(username)
    #                         else:
    #                             self.logger.warning("No username received in STOMP message")
    #
    #                         event.on_message(data_response)
    #                     elif isinstance(msg, StompJmsTextMessage):
    #                         stomp_message = msg
    #                         buffer = stomp_message.get_content()
    #                         message = buffer.to"".split(":")[1]
    #
    #                         try:
    #                             try:
    #                                 data_response = DataResponse.parse(message)
    #                             except JsonSyntaxException:
    #                                 data_response = DataResponse()
    #                                 data_response.set_data(message)
    #
    #                             data_response.set_destination(stomp_message.get_stomp_jms_destination().to"")
    #
    #                             if msg.get_jms_reply_to() is not None:
    #                                 data_response.set_reply_destination(msg.get_jms_reply_to())
    #
    #                             if msg.get_boolean_property(SecurityConstants.HAS_SUBJECT_HEADER):
    #                                 username = msg.get_string_property(SecurityConstants.SUBJECT_HEADER)
    #                                 data_response.set_username(username)
    #                             else:
    #                                 self.logger.warning("No username received in STOMP message")
    #
    #                             event.on_message(data_response)
    #                         except JsonSyntaxException:
    #                             data_response = DataResponse(message)
    #                             data_response.set_destination(stomp_message.get_stomp_jms_destination().to"")
    #
    #                             if msg.get_jms_reply_to() is not None:
    #                                 data_response.set_reply_destination(msg.get_jms_reply_to())
    #
    #                             if msg.get_boolean_property(SecurityConstants.HAS_SUBJECT_HEADER):
    #                                 data_response.set_username(msg.get_string_property(SecurityConstants.SUBJECT_HEADER))
    #
    #                             event.on_message(data_response)
    #                     else:
    #                         # TODO: Warn of unknown message global_property_types???
    #                         pass
    #                 except JMSException as ex:
    #                     # Happens when a timeout occurs.
    #                     if self.session is not None:
    #                         self.logger.debug("Closing session")
    #                         self.session.close()
    #                         self.session = None
    #
    #             # End of stomp_message_listener
    #
    #         thread = threading.Thread(target=stomp_message_listener)
    #         thread.start()
    #         self.threads.append(thread)
    #
    #     return self
    #
    # def publish(self, topic, data):
    #     if isinstance(topic, str):
    #         destination = self.get_destination(topic, self.connection, self.session)
    #     else:
    #         destination = topic
    #         self.logger.debug("Publishing to " + destination)
    #
    #     try:
    #         if data is None:
    #             raise ValueError("data cannot be None")
    #         if isinstance(data, str):
    #             self.client_publisher.publish(destination, data)
    #         else:
    #             self.client_publisher.publish(destination, json.dumps(data))
    #
    #     except JMSException as e:
    #         self.logger.error("publish error", e)
    #     except Exception as e:
    #         # TODO Auto-generated catch block
    #         raise AttributeError(e)
    # # 	/*
    # # 	 * private void publishTo(Destination destination, Serializable data) throws
    # # 	 * SystemException { try { clientPublisher.publishTo(destination, data); }
    # # 	 * catch (JMSException e) { SystemException.wrap(e).set("destination",
    # # 	 * destination).set("data", data); } }
    # # 	 */
    # #
    #
    # def close(self):
    #     # 	/**
    #     # 	 * Closes the GossClient connection with server.
    #     # 	 */
    #     try:
    #         self.logger.debug("Client closing!")
    #         if self.session is not None:
    #             self.session.close()
    #             self.session = None
    #
    #         self.connection = None
    #         self.client_publisher = None
    #     except JMSException as e:
    #         self.logger.error("Close Error", e)
    #
    # def subscribe(self, topic_name, event):
    #     if event is None:
    #         raise ValueError("event cannot be null")
    #
    #     try:
    #         if self.protocol == PROTOCOL.OPENWIRE:
    #             destination = self.get_destination(topic_name, self.connection, self.session)
    #             DefaultClientConsumer(DefaultClientListener(event), self.session, destination)
    #         elif self.protocol == PROTOCOL.STOMP:
    #             # STOMP subscription logic would go here
    #             pass  # Placeholder for STOMP subscription logic
    #     except Exception as e:
    #         raise SystemException.wrap(e)
    #
    # def publish(self, topic, data):
    #     if data is None:
    #         raise ValueError("data cannot be null")
    #
    #     try:
    #         destination = self.get_destination(topic, self.connection, self.session)
    #         if isinstance(data, str):
    #             self.client_publisher.publish(destination, data)
    #         else:
    #             gson = Gson()
    #             self.client_publisher.publish(destination, gson.to_json(data))
    #     except Exception as e:
    #         self.log.error("publish error", e)
    #         raise SystemException.wrap(e)
    #
    # def close(self):
    #     try:
    #         self.log.debug("Client closing!")
    #         if self.session is not None:
    #             self.session.close()
    #             self.session = None
    #
    #         self.connection = None
    #         self.client_publisher = None
    #     except Exception as e:
    #         self.log.error("Close Error", e)
    #
    # # ... other methods and attributes ...
    # # def get_session(self):
    # #     if self.session is None:
    # #         try:
    # #             # // Will throw exceptions if not able to create session.
    # #             if self.protocol == Protocol.SSL:
    # #                 self.create_ssl_session()
    # #             else:
    # #                 self.create_session()
    # #         except JMSException as e:
    # #             raise SystemException.wrap(e, ConnectionCode.SESSION_ERROR)
    # #         except Exception as e:
    # #             raise AttributeError(e)
    # #     return self.session
    # #
    # # def get_temporary_destination(self, session):
    # #     destination = None
    # #
    # #     try:
    # #         if self.protocol == Protocol.SSL:
    # #             destination = session.createTemporaryQueue()
    # #             if destination is None:
    # #                 raise SystemException(ConnectionCode.DESTINATION_ERROR)
    # #         else:
    # #             if self.protocol == Protocol.OPENWIRE:
    # #                 destination = session.createTemporaryQueue()
    # #                 if destination is None:
    # #                     raise SystemException(ConnectionCode.DESTINATION_ERROR)
    # #             elif self.protocol == Protocol.STOMP:
    # #                 destination = StompJmsTempQueue("/queue/", str(uuid.UUID.randomUUID()))
    # #     except JMSException as e:
    # #         raise SystemException.wrap(e).set("destination", "null")
    # #
    # #     return destination
    # #
    # # def get_destination(self, topic_name, destination_connection, session):
    # #     destination = None
    # #
    # #     try:
    # #         if self.protocol == Protocol.OPENWIRE:
    # #             destination = session.createTopic(topic_name)
    # #
    # #             if destination is None:
    # #                 raise SystemException(ConnectionCode.DESTINATION_ERROR)
    # #         elif self.protocol == Protocol.STOMP:
    # #             if destination_connection is None:
    # #                 raise exception.ConnectFailedException(f"Session error when connecting to topicName:{topic_name}")
    # #             destination = StompJmsTopic(destination_connection, topic_name)
    # #     except JMSException as e:
    # #         raise SystemException.wrap(e).set("destination", "null")
    # #
    # #     return destination
    # #
    # # def get_token(self, credentials):
    # #     self.log.info("Get token for " + credentials.getUserPrincipal().getName())
    # #     response = None
    # #
    # #     try:
    # #         factory = StompJmsConnectionFactory()
    # #         factory.setBrokerURI(self.stomp_uri.replace("stomp", "tcp"))
    # #         pw_connection = None
    # #         pw_connection = factory.createConnection(credentials.getUserPrincipal().getName(), credentials.getPassword())
    # #         pw_connection.start()
    # #
    # #         pw_session = pw_connection.createSession(False, Session.CLIENT_ACKNOWLEDGE)
    # #         dt = str(int(time.time() * 1000))
    # #         reply_destination = pw_session.createQueue("temp.token_resp." + credentials.getUserPrincipal().getName() + "-" + dt)
    # #         destination = self.get_destination(GossCoreConstants.PROP_TOKEN_QUEUE, pw_connection, pw_session)
    # #         pw_client_publisher = DefaultClientPublisher(credentials.getUserPrincipal().getName(), pw_session)
    # #         user_auth_str = credentials.getUserPrincipal().getName() + ":" + credentials.getPassword()
    # #         base64_str = encodings.base64.b64encode(user_auth_str.encode()).decode()
    # #
    # #         consumer = pw_session.createConsumer(reply_destination)
    # #         pw_client_publisher.send_message(base64_str.strip(), destination, reply_destination, RESPONSE_FORMAT.JSON)
    # #         try:
    # #             response_message = consumer.receive()
    # #             self.log.info("Received token for " + credentials.getUserPrincipal().getName())
    # #
    # #             if isinstance(response_message, ObjectMessage):
    # #                 object_message = response_message
    # #                 if isinstance(object_message.getObject(), Response):
    # #                     obj_response = object_message.getObject()
    # #                     response = object_message.to""
    # #             else:
    # #                 response = response_message.getText()
    # #             self.log.info("GossClient received token:" + response + " for user " + credentials.getUserPrincipal().getName())
    # #
    # #         except Exception as e:
    # #             self.log.error("Error occurred while receiving token: " + str(e))
    # #     except JMSException as e:
    # #         self.log.error("Error occurred while receiving token: " + str(e))
    # #         raise Exception(e)
    # #     except Exception as e:
    # #         pass
    # #     return response
    # #
    # # def set_credentials(self, credentials):
    # #     self.credentials = credentials
    # #     return self
    # #
    # # def get_protocol(self):
    # #     return self.protocol
    # #
    # # def reset(self):
    # #     """
    # #     /**
    # #     * Reset the client to an initial un-connected state. If the client
    # #     * currently has a session, then the session should be closed. If
    # #     * credentials are set then they will be unset after this call. The protocol
    # #     * of the client will not be changed.
    # #     */
    # #     :return:
    # #     """
    # #     pass
    # #
    # # def is_used(self):
    # #     """
    # #     /**
    # #     * Returns whether the current instances is being used or if it can be used
    # #     * by another process.
    # #     *
    # #     * @return
    # #     */
    # #     :return:
    # #     """
    # #     return self.used
    # #
    # # def set_used(self, used):
    # #     if not used:
    # #         if self.session is not None:
    # #             raise IllegalStateException("Cannot set unused without reset.")
    # #     self.used = used
    # #
    # # def get_client_id(self):
    # #     """
    # #     /**
    # #     * An implementation that allows the caching of clients for future use.
    # #     *
    # #     * @return
    # #     */
    # #     :return:
    # #     """
    # #     return str(self.uuid)
    #
    # class ResponseEvent(GossResponseEvent):
    #     def __init__(self, client):
    #         self.client = client
    #         self.gson = Gson()
    #
    #     def on_message(self, response):
    #         response_data = "{}"
    #         if isinstance(response, DataResponse):
    #             # String request = (String)((DataResponse) response).getData();
    #             # if (request.trim().equals("list_handlers")){
    #             # 	//responseData = "Listing handlers here!";
    #             # 	responseData = gson.toJson(handlerRegistry.list());
    #             # }
    #             # else if (request.trim().equals("list_datasources")){
    #             # 	//responseData = "Listing Datasources here!";
    #             # 	responseData = gson.toJson(datasource_registry.getAvailable());
    #             # }
    #             pass
    #             # Implement the logic for handling DataResponse here
    #
    #         self.client.publish("goss/management/response", response_data)



    class GossClient:
        def __init__(self, protocol, credentials, broker_uri, use_ssl=False):
            self.protocol = protocol
            self.credentials = credentials
            self.broker_uri = broker_uri
            self.use_ssl = use_ssl
            self.connection = None
            self.channel = None

        def create_ssl_session(self):
            ssl_options = {
                'ssl_version': ssl.PROTOCOL_TLSv1_2,
                'ca_certs': '/path/to/ca_certificate.pem',
                'keyfile': '/path/to/client_key.pem',
                'certfile': '/path/to/client_certificate.pem',
                'cert_reqs': ssl.CERT_REQUIRED
            }
            return ssl_options

        def create_session(self):
            if self.use_ssl:
                ssl_options = self.create_ssl_session()
                parameters = pika.ConnectionParameters(host=self.broker_uri,
                                                       port=5671,
                                                       ssl_options=pika.SSLOptions(ssl_options),
                                                       credentials=pika.PlainCredentials(self.credentials.username,
                                                                                         self.credentials.password))
            else:
                parameters = pika.ConnectionParameters(host=self.broker_uri,
                                                       credentials=pika.PlainCredentials(self.credentials.username,
                                                                                         self.credentials.password))

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

        def subscribe(self, topic_name, routing_key, callback):
            """
            Subscribe to a topic with a given routing key.

            :param topic_name: Name of the topic exchange.
            :param routing_key: Routing key to bind to.
            :param callback: Callback function to process received messages.
            """

            def wrapper(ch, method, properties, body):
                message = json.loads(body)
                callback(message)

            # Declare the exchange
            self.channel.exchange_declare(exchange=topic_name, exchange_type='topic')

            # Declare a queue and bind it to the exchange with the given routing key
            result = self.channel.queue_declare('', exclusive=True)
            queue_name = result.method.queue
            self.channel.queue_bind(exchange=topic_name, queue=queue_name, routing_key=routing_key)

            # Start consuming messages
            self.channel.basic_consume(queue=queue_name, on_message_callback=wrapper, auto_ack=True)
            self.channel.start_consuming()

        # def subscribe(self, queue_name, callback):
        #     def wrapper(ch, method, properties, body):
        #         message = json.loads(body)
        #         callback(message)
        #
        #     self.channel.queue_declare(queue=queue_name)
        #     self.channel.basic_consume(queue=queue_name, on_message_callback=wrapper, auto_ack=True)
        #     self.channel.start_consuming()

        def publish(self, queue_name, data):
            self.channel.queue_declare(queue=queue_name)
            message = json.dumps(data)
            self.channel.basic_publish(exchange='', routing_key=queue_name, body=message)

        def close(self):
            self.connection.close()

    # Example usage
    # credentials = pika.PlainCredentials('username', 'password')
    # client = GossClient('SSL', credentials, 'broker.example.com', use_ssl=True)
    # client.create_session()
    # client.publish('some_queue', {'key': 'value'})
    # client.close()
