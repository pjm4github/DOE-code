
import os
import threading
import queue
import logging

from gov_pnnl_goss.core.GossCoreConstants import GossCoreConstants
from gov_pnnl_goss.core.client.GossClient import GossClient


class Credentials:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class ClientServiceFactory:
    def __init__(self):
        self.client_instances = []
        self.properties = {}
        self.ssl_enabled = False

    def set_openwire_uri(self, broker_to_connect_to):
        self.properties['GossCoreConstants.PROP_OPENWIRE_URI'] = broker_to_connect_to

    def exists(self, value):
        return value is not None and value != ''

    def updated(self, properties):
        #@ConfigurationDependency(pid=CONFIG_PID)
        # TODO Check the function of the previous wrapper
        CONFIG_PID = os.getpid()
        logging.info("Updating configuration properties")
        if properties:
            with threading.Lock(self.properties):
                for key in properties.keys():
                    self.properties[key] = properties[key]

            self.ssl_enabled = bool(self.properties.get('GossCoreConstants.PROP_SSL_ENABLED', False))

            if self.ssl_enabled:
                uri = self.properties.get('GossCoreConstants.PROP_SSL_URI')
                trust_store = self.properties.get('GossCoreConstants.PROP_SSL_CLIENT_TRUSTSTORE')
                trust_password = self.properties.get('GossCoreConstants.PROP_SSL_CLIENT_TRUSTSTORE_PASSWORD')

                if not self.exists(trust_store):
                    raise Exception('GossCoreConstants.PROP_SSL_CLIENT_TRUSTSTORE Wasn\'t set')

                if not self.exists(trust_password):
                    raise Exception('GossCoreConstants.PROP_SSL_CLIENT_TRUSTSTORE_PASSWORD Wasn\'t set')

                if not self.exists(uri):
                    raise Exception('GossCoreConstants.PROP_SSL_URI Wasn\'t set')

                self.properties['DEFAULT_OPENWIRE_URI'] = uri
                self.properties['DEFAULT_STOMP_URI'] = uri

            else:
                value = self.properties.get('GossCoreConstants.PROP_OPENWIRE_URI')
                if not self.exists(value):
                    raise Exception(f'GossCoreConstants.PROP_OPENWIRE_URI Not found in configuration file: {CONFIG_PID}')

    def create(self, protocol, credentials, use_token=False):
        config_properties = {}

        if not self.properties:
            logging.info("Reading configuration properties")
            try:

                # Open and read the file line by line
                file_path = 'conf' + os.path.sep + 'pnnl.goss.core.client.cfg'
                with open(file_path, 'r') as file:
                    for line in file:
                        # Split each line into key and value using the '=' delimiter
                        parts = line.strip().split('=')

                        # Ensure there are two parts (key and value)
                        if len(parts) == 2:
                            key = parts[0].strip()  # Remove leading/trailing whitespace
                            value = parts[1].strip()  # Remove leading/trailing whitespace

                            # Add the key-value pair to the dictionary
                            config_properties[key] = value

                # config_properties.load(open('conf' + os.path.sep + 'pnnl.goss.core.client.cfg', 'r'))

                dictionary = {
                    'GossCoreConstants.PROP_OPENWIRE_URI': config_properties.get('goss.openwire.uri'),
                    'GossCoreConstants.PROP_STOMP_URI': config_properties.get('goss.stomp.uri')
                }

                self.updated(dictionary)

            except FileNotFoundError as e:
                logging.error(e)
            except IOError as e:
                logging.error(e)
            except Exception as e:
                logging.error(e)

        client = None

        for c in self.client_instances:
            if not c.is_used() and c.get_protocol() == protocol:
                client = c
                client.set_used(True)
                break

        if client is None:
            openwire_uri = self.properties.get('ClientFactory.DEFAULT_OPENWIRE_URI')
            stomp_uri = self.properties.get('ClientFactory.DEFAULT_STOMP_URI')

            if self.ssl_enabled:
                protocol = "SSL"
                trust_store_password = self.properties.get(GossCoreConstants.PROP_SSL_CLIENT_TRUSTSTORE_PASSWORD)
                trust_store = self.properties.get(GossCoreConstants.PROP_SSL_CLIENT_TRUSTSTORE)

                client = GossClient(protocol, credentials, openwire_uri, stomp_uri, trust_store_password, trust_store,
                                    use_token)
            else:
                client = GossClient(protocol, credentials, openwire_uri, stomp_uri, use_token)

        client.set_used(True)
        client.create_session()
        self.client_instances.append(client)

        return client

    def get(self, uuid):
        for c in self.client_instances:
            if c.get_client_id() == uuid:
                return c

        return None

    def destroy(self):
        while self.client_instances:
            client = self.client_instances.pop(0)
            client.reset()
            client = None

    def list(self):
        result = {}
        for c in self.client_instances:
            result[c.get_client_id()] = c.get_protocol()

        return result
