import logging
import sys

# sys.path.append('/path/to/org.junit.Assert/')  # Add path to org.junit.Assert library
# sys.path.append(
#     '/path/to/org.mockito.runners.MockitoJUnitRunner/')  # Add path to org.mockito.runners.MockitoJUnitRunner library
# sys.path.append(
#     '/path/to/gov.pnnl.goss.gridappsd.utils.GridAppsDConstants/')  # Add path to gov.pnnl.goss.gridappsd.utils.GridAppsDConstants library
# sys.path.append('/path/to/pnnl.goss.core.Client/')  # Add path to pnnl.goss.core.Client library
# sys.path.append('/path/to/pnnl.goss.core.ClientFactory/')  # Add path to pnnl.goss.core.ClientFactory library
# sys.path.append('/path/to/pnnl.goss.core.GossResponseEvent/')  # Add path to pnnl.goss.core.GossResponseEvent library
# sys.path.append(
#     '/path/to/pnnl.goss.core.server.ServerControl/')  # Add path to pnnl.goss.core.server.ServerControl library
# from org.amdatu.testing.configurator.TestConfigurator import cleanUp, configure, createServiceDependency
# from org.junit.Assert import assertNotNull
# from org.apache.http.auth import Credentials, UsernamePasswordCredentials
# from java.io import Serializable
# from java.util.concurrent import TimeUnit
# from org.amdatu.testing.configurator.TestConfiguration import TestConfiguration
# from org.junit import After, Before, Test
# from org.junit.runner import RunWith
# from org.mockito.runners import MockitoJUnitRunner
# from org.slf4j import Logger, LoggerFactory
# from gov.pnnl.goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants
# from pnnl.goss.core import Client
# from pnnl.goss.core.Client import PROTOCOL
# from pnnl.goss.core.ClientFactory import ClientFactory
# from pnnl.goss.core import GossResponseEvent
# from pnnl.goss.core.server.ServerControl import ServerControl
#
# log = LoggerFactory.getLogger(AppManagerTest)
#

# class AppManagerTest:
#     def __init__(self):
#         self.testConfig = None
#         self.client_factory = None
#         self.serverControl = None
#         self.client = None
#         self.logger = LogManager(AppManagerTest.__name__)
#
#     def before(self):
#         self.testConfig = configure(self).add(CoreGossConfig.configureServerAndClientPropertiesConfig()).add(
#             createServiceDependency().setService(ClientFactory)).add(createServiceDependency().setService(Logger)).add(
#             createServiceDependency().setService(SecurityManager)).add(
#             createServiceDependency().setService(ServerControl))
#         self.testConfig.apply()
#         TimeUnit.MILLISECONDS.sleep(1000)
#
#     def sanity_ServerStarted(self):
#         log.debug("TEST: serverCanStartSuccessfully")
#         print("TEST: serverCanStartSuccessfully")
#         assertNotNull(self.serverControl)
#         log.debug("TEST_END: serverCanStartSuccessfully")
#
#
#     def testGetConfigurationProperty(self):
#         pass
#
#
#     def testConnect(self):
#         try:
#             credentials = UsernamePasswordCredentials(TestConstants.username, TestConstants.password)
#             self.client = self.client_factory.create(PROTOCOL.STOMP, credentials)
#
#             # TODO: Implement the rest of the method
#         except Exception as e:
#             print(e)
#
#
#     def after(self):
#         cleanUp(self)


import unittest
from multiprocessing.connection import Client
from unittest.mock import Mock

from gov_pnnl_goss.SpecialClasses import UsernamePasswordCredentials, TimeUnit
from gov_pnnl_goss.core.ClientFactory import ClientFactory
from gov_pnnl_goss.core.GossResponseEvent import GossResponseEvent
from gov_pnnl_goss.core.client.GossClient import Protocol
from gov_pnnl_goss.core.security.impl.Activator import SecurityManager
from gov_pnnl_goss.core.server.ServerControl import ServerControl
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.test import CoreGossConfig
from gov_pnnl_goss.gridappsd.test.TestConstants import TestConstants
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


# from pnnl.goss.core import Client, PROTOCOL
# from pnnl.goss.core.server import ServerControl
# from org.amdatu.testing.configurator import TestConfigurator, configure, createServiceDependency, cleanUp
# from org.apache.http.auth import UsernamePasswordCredentials
# from gov.pnnl.goss.gridappsd.utils import GridAppsDConstants

class TestConfiguration:
    def __init__(self):
        self.dependencies = {}

    def add(self, dependency):
        return self

    def apply(self):
        pass

def configure(test_case):
    return TestConfiguration()

def createServiceDependency():
    return Mock()

def cleanUp(test_case):
    pass


class myGossResponseEvent(GossResponseEvent):
    def __init__(self):
        pass

    def onMessage(self, response):
        print("RESPNOSE " + response)


class AppManagerTest(unittest.TestCase):
    OPENWIRE_CLIENT_CONNECTION = "tcp://localhost:6000"
    STOMP_CLIENT_CONNECTION = "stomp://localhost:6000"

    def __init__(self):
        super().__init__()
        self.logger = LogManager(AppManagerTest.__name__)
        self.test_config = TestConfiguration()
        self.client_factory = ClientFactory()
        self.server_control = ServerControl()
        self.client = Client(TestConstants.username, TestConstants.password)
        # self.context: BundleContext = FrameworkUtil.getBundle(this.getClass()).getBundleContext()

    def setUp(self):
        self.testConfig = configure(self) \
            .add(CoreGossConfig.configureServerAndClientPropertiesConfig()) \
            .add(createServiceDependency().setService(ClientFactory)) \
            .add(createServiceDependency().setService(logging.Logger)) \
            .add(createServiceDependency().setService(SecurityManager)) \
            .add(createServiceDependency().setService(ServerControl))
        self.testConfig.apply()
        self.serverControl = None  # Set this to the actual server control instance
        # Configuration update is asyncronous, so give a bit of time to catch up
        TimeUnit.MILLISECONDS.sleep(1000);

    def test_sanity_serverStarted(self):
        self.logger.debug("TEST: serverCanStartSuccessfully")
        print("TEST: serverStarted")
        self.assertIsNotNone(self.serverControl)
        print("TEST_END: serverStarted")

    def test_connect(self):
        try:
            # Step 1: Create GOSS Client
            credentials = UsernamePasswordCredentials(TestConstants.username, TestConstants.password)
            self.client = ClientFactory.create(Protocol.STOMP, credentials)

            # Create Request Simulation object
            # PowerSystemConfig powerSystemConfig = new PowerSystemConfig()
            # powerSystemConfig.GeographicalRegion_name = "ieee8500_Region"
            # powerSystemConfig.SubGeographicalRegion_name = "ieee8500_SubRegion"
            # powerSystemConfig.Line_name = "ieee8500"

            # Gson gson = new Gson()
            # String request = gson.toJson(powerSystemConfig);
            # DataRequest request = new DataRequest();
            # request.setRequestContent(powerSystemConfig);
            print(self.client)
            response = self.client.getResponse("", GridAppsDConstants.topic_requestData, None)
            # TODO subscribe to response
            self.client.subscribe(GridAppsDConstants.topic_simulationOutput + response, lambda r: myGossResponseEvent().onMessage(r)
                                  # lambda r: print("RESPONSE", r)
                                )

        except Exception as e:
            print(e)



    def tearDown(self):
        cleanUp(self)


if __name__ == '__main__':
    unittest.main()
