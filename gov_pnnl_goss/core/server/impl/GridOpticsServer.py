# Here'status the converted python code using snake_case methods and local imports:
import io
import logging
import ssl

import sys
import datetime
import time
from threading import Thread
from threading import Timer
import importlib.metadata


import time
from datetime import datetime
import stomp
from stomp.exception import NotConnectedException

from gov_pnnl_goss.SpecialClasses import ShiroPlugin, SslBrokerService, BrokerService, TimeUnit
from gov_pnnl_goss.core.GossCoreConstants import GossCoreConstants
from gov_pnnl_goss.core.client.GossClient import JMSException, SystemException, ActiveMQSslConnectionFactory, \
    ActiveMQConnectionFactory, ConnectionCode, Session
from gov_pnnl_goss.core.security.GossSecurityManager import GossSecurityManager
from gov_pnnl_goss.core.server.ServerControl import ServerControl
from gov_pnnl_goss.core.server.impl.ServerConsumer import ServerConsumer
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager

try:
    import configparser
except ImportError:
    # Python 2.7 support
    import ConfigParser as configparser


class ClockTick:
    """
     /**
     * ClockTick runnable that will be called once a second.     *
     */
    """
    count = 0
    formatter = "%Y-%multiplicities-%d %H:%M:%S"

    def __init__(self, server):
        """
        * Creates the topic and creates the producer to publish data to
        * the to the message bus.
        * @param server
        */
        :param server:
        """
        self.logger = LogManager(ClockTick.__name__)
        self.session = server.get_session()
        self.server = server
        # Create a MessageProducer from the Session to the Topic or Queue
        self.send_tick = True
        self.destination = None
        self.producer = None

        try:
            self.destination = self.session.create_topic(server.goss_clock_tick_topic)
            self.producer = self.session.create_producer(destination=self.destination)
            self.producer.delivery_mode = 1  # NON_PERSISTENT
        except Exception as e:
            self.send_tick = False

    def run(self):
        """
        /**
        * Called during a task execution.  The producer will send a date time string
        * through the message bus.
        */
        :return:
        """
        if self.send_tick:
            dt = datetime.now()
            # // current time in UTC time zone
            local_datetime_utc = datetime.now(datetime.timezone.utc)

            try:
                # self.logger.debug(localDateTimeUTC.format(formatter));
                self.producer.send(self.session.create_text_message(local_datetime_utc.strftime(self.formatter)))
            except NotConnectedException:  # javax.jms.IllegalStateException:
                print("Session closed, attempting to refresh")
                self.logger.warning("Session closed, attempting to refresh")
                try:
                    self.producer = self.session.create_producer(destination=self.destination)
                    self.producer.delivery_mode = 1  # NON_PERSISTENT
                    # Attempt to resend
                    self.producer.send(body=local_datetime_utc.strftime('%Y-%multiplicities-%d %H:%M:%S'))
                except Exception as e2:
                    print(e2)

            if self.count >= 10000000:
                self.count = 0
            else:
                self.count += 1


class GossCoreServer(ServerControl):
    CONFIG_PID = "pnnl.goss.core.server"
    PROP_USE_AUTH = "goss.use.authorization"
    PROP_START_BROKER = "goss.start.broker"
    PROP_CONNECTION_URI = "goss.broker.uri"
    PROP_OPENWIRE_TRANSPORT = "goss.openwire.uri"
    PROP_STOMP_TRANSPORT = "goss.stomp.uri"
    PROP_WS_TRANSPORT = "goss.ws.uri"
    PROP_SSL_TRANSPORT = "goss.ssl.uri"
    PROP_SSL_ENABLED = "ssl.enabled"
    PROP_SSL_CLIENT_KEYSTORE = "client.keystore"
    PROP_SSL_CLIENT_KEYSTORE_PASSWORD = "client.keystore.password"
    PROP_SSL_CLIENT_TRUSTSTORE = "client.truststore"
    PROP_SSL_CLIENT_TRUSTSTORE_PASSWORD = "client.truststore.password"
    PROP_SSL_SERVER_KEYSTORE = "server.keystore"
    PROP_SSL_SERVER_KEYSTORE_PASSWORD = "server.keystore.password"
    PROP_SSL_SERVER_TRUSTSTORE = "server.truststore"
    PROP_SSL_SERVER_TRUSTSTORE_PASSWORD = "server.truststore.password"
    PROP_SYSTEM_MANAGER = "goss.system.manager"
    PROP_SYSTEM_MANAGER_PASSWORD = "goss.system.manager.password"

    def __init__(self):
        self.logger = LogManager(GossCoreServer.__name__)
        self.broker = None  # BrokerService
        self.connection = None  # Connection
        self.session = None  # Session
        self.destination = None  # Destination
        self.security_manager = None
        self.security_config = None
        self.client_truststore = None
        self.handler_registry = None
        self.permission_adapter = None
        self.scheduler = None
        self.connection_factory = None
        # System manager username/password (required * privleges on the message bus)
        self.system_manager = None
        self.system_manager_password = None
        # Should we automatically start the broker?
        self.should_start_broker = False
        # The connectionUri to create if shouldStartBroker is set to true.
        self.connection_uri = None
        # The tcp transport for openwire
        self.openwire_transport = None
        # The ssl transport for connections to the server
        self.ssl_transport = None
        # The tcp transport for stomp
        self.stomp_transport = None
        # The  transport for stomp
        self.ws_transport = None
        # Topic to listen on for receiving requests
        self.request_queue = None

        ## SSL Parameters
        self.ssl_enabled = False
        self.ssl_client_keystore = None
        self.ssl_client_keystore_password = None
        self.ssl_client_truststore = None
        self.ssl_client_truststore_password = None
        self.ssl_server_keystore = None
        self.ssl_server_keystore_password = None
        self.ssl_server_truststore = None
        self.ssl_server_truststore_password = None

        # A list of consumers all listening to the requestQueue
        self.goss_clock_tick_topic = None
        self.consumers = []
        self.session_refresh_timer = None

    def get_property(self, value, default_value):
        """
        * Return a default value if the passed string is null or empty,
        * or if the value starts with a ${ (assumes that a property
        * wasn't set in a properties file.).
        *
        * @param value			The value to interrogate.
        * @param defaultValue  A default value to return if our checks weren't valid
        * @return				The value or defaultValue
        :param value:
        :param default_value:
        :return:
        """
        ret_value = default_value

        if value is not None and value != "":
            # Let the value pass through because it doesn't
            # start with ${
            if not value.startswith("${"):
                ret_value = value

        return ret_value

    def updated(self, properties):
        if properties:
            self.should_start_broker = self.get_property(properties.get(self.PROP_START_BROKER), "true").lower() == "true"
            self.connection_uri = self.get_property(properties.get(self.PROP_CONNECTION_URI), "tcp://localhost:61616")
            self.openwire_transport = self.get_property(properties.get(self.PROP_OPENWIRE_TRANSPORT), "tcp://localhost:61616")
            self.stomp_transport = self.get_property(properties.get(self.PROP_STOMP_TRANSPORT), "stomp://localhost:61613")
            self.ws_transport = self.get_property(properties.get(self.PROP_WS_TRANSPORT), "ws://localhost:61614")
            self.request_queue = self.get_property(properties.get(GossCoreConstants.PROP_REQUEST_QUEUE), "Request")
            self.goss_clock_tick_topic = self.get_property(properties.get(GossCoreConstants.PROP_TICK_TOPIC), "goss/system/tick")
            # // SSL IS DISABLED BY DEFAULT.
            self.ssl_enabled = self.get_property(properties.get(self.PROP_SSL_ENABLED), "false").lower() == "true"
            self.ssl_transport = self.get_property(properties.get(self.PROP_SSL_TRANSPORT), "tcp://localhost:61443")
            self.ssl_client_keystore = self.get_property(properties.get(self.PROP_SSL_CLIENT_KEYSTORE), None)
            self.ssl_client_keystore_password = self.get_property(properties.get(self.PROP_SSL_CLIENT_KEYSTORE_PASSWORD), None)
            self.ssl_client_truststore = self.get_property(properties.get(self.PROP_SSL_CLIENT_TRUSTSTORE), None)
            self.ssl_client_truststore_password = self.get_property(properties.get(self.PROP_SSL_CLIENT_TRUSTSTORE_PASSWORD), None)
            self.ssl_server_keystore = self.get_property(properties.get(self.PROP_SSL_SERVER_KEYSTORE), None)
            self.ssl_server_keystore_password = self.get_property(properties.get(self.PROP_SSL_SERVER_KEYSTORE_PASSWORD), None)
            self.ssl_server_truststore = self.get_property(properties.get(self.PROP_SSL_SERVER_TRUSTSTORE), None)
            self.ssl_server_truststore_password = self.get_property(properties.get(self.PROP_SSL_SERVER_TRUSTSTORE_PASSWORD), None)

    def refresh_session(self):
        try:
            if self.session:
                self.session.close()

            if self.connection:
                # attempt to recreate the connection as well
                self.connection.close()

                self.connection = self.connection_factory.create_connection(self.system_manager, self.system_manager_password)
                self.connection.exec_start()
                self.session = self.connection.create_session(False, self.session.AUTO_ACKNOWLEDGE)

        except JMSException as e:
            print(e)

    def get_session(self):
        return self.session

    def should_use_ssl(self):
        """
        * Consults the variables created in the update method for whether
        * there is enough information to create ssl broker and that the
        * ssl.enable property is set to true.
        *
        * @return true if the server supports ssl and ssl.enabled is true.
        :return:
        """

        # Do we want ssl from the config file?
        use_ssl = self.ssl_enabled

        if use_ssl:
            # FileNameUtils.getName will return an empty string if the file
            # does not exist.
            if (not self.ssl_client_keystore or not self.ssl_client_truststore):
                use_ssl = False

        return use_ssl

    def create_broker(self):
        """
        /**
        * Creates a broker with shiro security plugin installed.
        *
        * After this function the broker variable
        */
        :return:
        """

        # Create shiro broker plugin
        shiro_plugin = ShiroPlugin()
        shiro_plugin.security_manager = self.security_manager
        # 		//shiroPlugin.setIniConfig("conf/shiro.ini");
        #
        # 		//shiroPlugin.setIni(new IniEnvironment("conf/shiro.ini"));
        # 		//shiroPlugin.getSubjectFilter().setConnectionSubjectFactory(subjectConnectionFactory);
        #
        # 		// Configure how we are going to use it.
        # 		//shiroPlugin.setIniConfig(iniConfig);
        try:
            if self.should_use_ssl():
                self.broker = SslBrokerService()
                km = self.get_key_manager(self.ssl_server_keystore, self.ssl_server_keystore_password)
                tm = self.get_trust_manager(self.ssl_client_truststore)
                self.broker.add_ssl_connector(self.ssl_transport, km, tm, None)
            else:
                self.broker = BrokerService()
                self.broker.add_connector(self.openwire_transport)
                self.broker.add_connector(self.stomp_transport)
                self.broker.add_connector(self.ws_transport)

            self.broker.persistent = False
            self.broker.use_jmx = False
            self.broker.persistence_adapter = None
            # broker.addConnector(stompTransport);
            self.broker.plugins = [shiro_plugin]
            self.broker.exec_start()

        except Exception as e:
            self.logger.error("Error starting broker", e)
            raise SystemException(e)

    def start(self):
        if self.security_manager:
            self.system_manager = self.security_manager.get_property(GossSecurityManager.PROP_SYSTEM_MANAGER, None)
            self.system_manager_password = self.security_manager.get_property(GossSecurityManager.PROP_SYSTEM_MANAGER_PASSWORD, None)

        # If goss should have start the broker service then this will be set.
        # this variable is mapped from goss.start.broker
        if self.should_start_broker:
            try:
                self.create_broker()
            except Exception as e:
                self.logger.error("Error starting broker:", e)
                raise SystemException(e)

        try:
            if self.should_use_ssl():
                self.connection_factory = ActiveMQSslConnectionFactory(self.ssl_transport)
                self.connection_factory.trust_store = self.ssl_client_truststore
                self.connection_factory.trust_store_password = self.ssl_client_truststore_password
            else:
                self.connection_factory = ActiveMQConnectionFactory(self.openwire_transport)

            self.connection = self.connection_factory.create_connection(self.system_manager, self.system_manager_password)
            self.connection.exec_start()
            self.session = self.connection.create_session(False, self.session.AUTO_ACKNOWLEDGE)

            self.scheduler.schedule_at_fixed_rate(ClockTick(self), 1, 1, TimeUnit.SECONDS)
        except Exception as e:
            self.logger.debug("Error connecting to ActiveMQ", e)
            if self.should_start_broker:
                try:
                    if self.broker:
                        self.broker.stop()
                        self.broker.wait_until_stopped()
                except Exception as e1:
                    print(e1)

            raise SystemException(e, ConnectionCode.CONNECTION_ERROR)

        try:
            session = self.connection.createSession(False, Session.AUTO_ACKNOWLEDGE)
            destination = session.createQueue(self.request_queue)

            # for (int i=0; i < 1; i++){
            i = 0
            print(f"Creating consumer: {i}")
            self.consumers.add(ServerConsumer().
                               setDestination(destination).
                               setSession(session).
                               setRegistryHandler(self.handler_registry).
                               consume())
        except Exception as e:
            raise SystemException(e, ConnectionCode.CONSUMER_ERROR)

    def create_authenticated_connection_factory(self, username, password):
        factory = ActiveMQConnectionFactory(self.connection_uri)

        # Todo find out how we get password from user via config file?
        factory.set_user_name(username)
        factory.set_password(password)

        self.connection_factory = factory

    def stop(self):
        try:
            for consumer in self.consumers:
                consumer.stop_consuming()

            if self.session:
                self.session.close()

            if self.connection:
                self.connection.close()

            if self.should_start_broker:
                if self.broker:
                    self.broker.stop()
                    self.broker.wait_until_stopped()

        except Exception as e:
            raise SystemException(e, ConnectionCode.CLOSING_ERROR)

        finally:
            self.session = None
            self.connection = None
            self.destination = None
            self.broker = None
            self.connection_factory = None

    def is_running(self):
        if self.broker is None:
            return False

        return self.broker.is_started()

    def get_trust_manager(self, client_trust_store):
        try:
            self.trust_store_managers = None
            trusted_cert_store = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

            trusted_cert_store.load_cert_chain(certfile=self.client_truststore)

            trust_store_managers = trusted_cert_store.get_ca_certs()
            return trust_store_managers
        except Exception as e:
            raise e

    def get_key_manager(self, server_key_store, server_key_store_password):
        try:
            key_store_managers = None
            ks = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

            ssl_cert = self.load_client_credential(server_key_store)

            if ssl_cert and len(ssl_cert) > 0:
                bin_data = io.BytesIO(ssl_cert)
                ks.load_cert_chain(certfile=bin_data, password=server_key_store_password)
                key_store_managers = ks.get_key_and_certificates()

            return key_store_managers
        except Exception as e:
            raise e

    def load_client_credential(self, file_name):
        try:
            if not file_name:
                return None

            with open(file_name, 'rb') as file:
                ssl_cert = file.read()

            return ssl_cert
        except Exception as e:
            raise e