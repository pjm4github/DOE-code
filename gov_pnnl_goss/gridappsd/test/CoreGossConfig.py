import configparser
#
# from gov_pnnl_goss.gridappsd.simulation.SimulationEvent import ClientFactory
#
#


# /**
#  * Standard configuration that is required for us to use goss in integration tests.
#  *
#  * These configuration steps can be used as a guide to building cfg files
#  * for the bundles.
#  *
#  * @author Craig Allwardt
#  *
#  */

def configure_server_and_client_properties_config():
    config = configparser.ConfigParser()

    config['pnnl.goss.core.server'] = {
        'goss.openwire.uri': 'tcp://localhost:6000',
        'goss.stomp.uri': 'stomp://localhost:6001',
        'goss.ws.uri': 'ws://localhost:6002',
        'goss.start.broker': 'true',
        'goss.broker.uri': 'tcp://localhost:6000'
    }

    config[ClientFactory.CONFIG_PID] = {
        'goss.openwire.uri': 'tcp://localhost:6000',
        'goss.stomp.uri': 'stomp://localhost:6001',
        'goss.ws.uri': 'ws://localhost:6002'
    }

    config['org.ops4j.pax.logging'] = {
        'log4j.rootLogger': 'DEBUG, out, osgi:*',
        'log4j.throwableRenderer': 'org.apache.log4j.OsgiThrowableRenderer',
        'log4j.appender.stdout': 'org.apache.log4j.ConsoleAppender',
        'log4j.appender.stdout.layout': 'org.apache.log4j.PatternLayout',
        'log4j.appender.stdout.layout.ConversionPattern': '%-5.5p| %c{1} (%L) | %multiplicities%dimensions',
        'log4j.logger.pnnl.goss': 'DEBUG, stdout',
        'log4j.logger.org.apache.aries': 'INFO',
        'log4j.appender.out': 'org.apache.log4j.RollingFileAppender',
        'log4j.appender.out.layout': 'org.apache.log4j.PatternLayout',
        'log4j.appender.out.layout.ConversionPattern': '%d{ISO8601} | %-5.5p | %-16.16t | %-32.32c{1} | %X{bundle.id} - %X{bundle.name} - %X{bundle.version} | %multiplicities%dimensions',
        'log4j.appender.out.file': 'felix.log',
        'log4j.appender.out.append': 'true',
        'log4j.appender.out.maxFileSize': '1MB',
        'log4j.appender.out.maxBackupIndex': '10'
    }

    return config

import unittest
from unittest.mock import Mock

from gov_pnnl_goss.core.ClientFactory import ClientFactory


class CoreGossConfig:
    """
    / **
    * Minimal configuration for goss including broker uri
    * @ return
    * /
    """
    pass

class CoreGossConfigTest(unittest.TestCase):

    def test_configure_server_and_client_properties_config(self):
        # Replace the following lines with your actual configuration steps
        config_steps = configure_server_and_client_properties_config()

        # Assuming you have a method to create a Mock ConfigurationAdmin instance
        configuration_admin = create_mock_configuration_admin()

        # Apply the configuration steps
        config_steps.apply(configuration_admin)

        # Add your assertions here to verify the applied configurations

#
# def configure_server_and_client_properties_config():
#     # Replace the following lines with your actual configuration steps
#     return ConfigurationSteps.create() \
#         .add(create_configuration("pnnl.goss.core.server")
#              .set("goss.openwire.uri", "tcp://localhost:6000")
#              .set("goss.stomp.uri", "stomp://localhost:6001")
#              .set("goss.ws.uri", "ws://localhost:6002")
#              .set("goss.start.broker", "true")
#              .set("goss.broker.uri", "tcp://localhost:6000")) \
#         .add(create_configuration(ClientFactory.CONFIG_PID)
#              .set("goss.openwire.uri", "tcp://localhost:6000")
#              .set("goss.stomp.uri", "stomp://localhost:6001")
#              .set("goss.ws.uri", "ws://localhost:6002")) \
#         .add(create_configuration("org.ops4j.pax.logging")
#              .set("log4j.rootLogger", "DEBUG, out, osgi:*")
#              .set("log4j.throwableRenderer", "org.apache.log4j.OsgiThrowableRenderer")
#              .set("log4j.appender.stdout", "org.apache.log4j.ConsoleAppender")
#              .set("log4j.appender.stdout.layout", "org.apache.log4j.PatternLayout")
#              .set("log4j.appender.stdout.layout.ConversionPattern", "%-5.5p| %c{1} (%L) | %multiplicities%dimensions")
#              .set("log4j.logger.pnnl.goss", "DEBUG, stdout")
#              .set("log4j.logger.org.apache.aries", "INFO")
#              .set("log4j.appender.out", "org.apache.log4j.RollingFileAppender")
#              .set("log4j.appender.out.layout", "org.apache.log4j.PatternLayout")
#              .set("log4j.appender.out.layout.ConversionPattern",
#                   "%d{ISO8601} | %-5.5p | %-16.16t | %-32.32c{1} | %X{bundle.id} - %X{bundle.name} - %X{bundle.version} | %multiplicities%dimensions")
#              .set("log4j.appender.out.file", "felix.log")
#              .set("log4j.appender.out.append", "true")
#              .set("log4j.appender.out.maxFileSize", "1MB")
#              .set("log4j.appender.out.maxBackupIndex", "10"))


def create_configuration(pid):
    # Replace this with your actual configuration creation logic
    pass


def create_mock_configuration_admin():
    # Replace this with your actual mock ConfigurationAdmin creation logic
    return Mock()


if __name__ == '__main__':
    unittest.main()
