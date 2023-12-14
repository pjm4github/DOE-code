#
# package gov.pnnl.goss.gridappsd;
#
# import static org.junit.Assert.assertEquals;
#
#
# import org.apache.http.auth.Credentials;
# import org.junit.Test;
# import org.junit.runner.RunWith;
# import org.mockito.ArgumentCaptor;
# import org.mockito.Captor;
# import org.mockito.Mock;
# import org.mockito.Mockito;
# import org.mockito.runners.MockitoJUnitRunner;
#
# import gov.pnnl.goss.gridappsd.api.ConfigurationManager;
# import gov.pnnl.goss.gridappsd.api.LogManager;
# import gov.pnnl.goss.gridappsd.dto.FncsBridgeResponse;
# import gov.pnnl.goss.gridappsd.simulation.SimulationManagerImpl;
# import pnnl.goss.core.Client.PROTOCOL;
# import pnnl.goss.core.ClientFactory;
# import pnnl.goss.core.server.ServerControl;
# import gov.pnnl.goss.gridappsd.utils.GridAppsDConstants;
#
# @RunWith(MockitoJUnitRunner.class)
# public class SimulationManagerTests {
#     @Mock
#     ConfigurationManager mockConfigurationManager;
#
#     @Mock
#     LogManager log_manager;
#
#     @Mock
#     FncsBridgeResponse mockFncsBridgeResponse;
#
#     @Mock
#     ClientFactory mockClientFactory;
#
#     @Mock
#     ServerControl mockServerControl;
#
#     @Captor
#     ArgumentCaptor<PROTOCOL> protocalCapture;
#
#     @Captor
#     ArgumentCaptor<Credentials> credentialCapture;
#
#
#     Credentials creds;
#
#     @Test
#     public void correctCredsWhenStarted(){
#         // TODO the client_factory doesn't return a satisfactory client so that there is a null pointer exception that is thrown in start of manager.
#
#         SimulationManagerImpl manager = new SimulationManagerImpl(mockClientFactory, mockServerControl, log_manager, mockConfigurationManager);
#
#         try {
#             manager.start();
#
#             Mockito.verify(mockClientFactory).create(protocalCapture.capture(), credentialCapture.capture());
#         } catch (Exception e) {
#             // TODO Auto-generated catch block
#             print(e);
#         }
#
#
#
#
#         assertEquals(PROTOCOL.STOMP, protocalCapture.getValue());
#
#
#         assertEquals(GridAppsDConstants.username, credentialCapture.getValue().getUserPrincipal().getName());
#         assertEquals(GridAppsDConstants.password, credentialCapture.getValue().getPassword());
#
#     }
#
#
#     @Captor
#     ArgumentCaptor<PROTOCOL> captProtocol;
#
#     @Captor
#     ArgumentCaptor<Credentials> captCreds;
#
#     @Test
#     public void clientFactoryCreateCalledWhen_simulationManagerStartCalled() {
#
#         creds = new UsernamePasswordCredentials("foo", "bar");
#
#         SimulationManagerImpl simulation_manager = new SimulationManagerImpl(mockClientFactory,mockServerControl,
#                 mockStatusReporter,mockConfigurationManager);
#         try {
#             simulation_manager.start();
#             //Mockito.verify(mockClientFactory).create(PROTOCOL.OPENWIRE, creds);
#         }
#     }
# }
import base64
import unittest
from unittest.mock import Mock, patch, call
# from http import HTTPBasicCredentials

from gov_pnnl_goss.gridappsd.simulation.SimulationManagerImpl import SimulationManagerImpl
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.TestConstants import TestConstants


class SimulationManagerTests(unittest.TestCase):
    def setUp(self):
        self.mockConfigurationManager = Mock()
        self.logManager = Mock()
        self.mockFncsBridgeResponse = Mock()
        self.mockClientFactory = Mock()
        self.mockServerControl = Mock()
        self.protocalCapture = Mock()
        self.credentialCapture = Mock()


        username = "your_username"
        password = "your_password"

        # Encode the username and password as bytes and then as base64
        self.credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")

        # Include the credentials in your HTTP request headers
        self.headers = {
            "Authorization": f"Basic {self.credentials}"
        }

        self.credentialCapture.return_value = self.credentials  # HTTPBasicCredentials("username", "password")

    def test_correctCredsWhenStarted(self):
        # Configure the mockClientFactory to return the client instance
        self.mockClientFactory.create.return_value = self.mockClientFactory

        # Call the function or method that you want to test here, which should start the manager
        # For example, you can call the function that starts the manager here
        # SimulationManagerImpl(manager, mockServerControl, log_manager, mockConfigurationManager)

        # Verify that the mockClientFactory.create method is called with the expected arguments
        self.mockClientFactory.create.assert_called_once_with(self.protocalCapture, self.credentialCapture)

        # Assert the values captured in protocalCapture and credentialCapture
        self.assertEqual(self.PROTOCOL.STOMP, self.protocalCapture)
        self.assertEqual("username", self.credentialCapture.user_principal.name)
        self.assertEqual("password", self.credentialCapture.password)

    def test_clientFactoryCreateCalledWhen_simulationManagerStartCalled(self):
        creds = self.credentials  # HTTPBasicCredentials("foo", "bar")
        simulationManager = SimulationManagerImpl(self.mockClientFactory, self.mockServerControl, self.logManager, self.mockConfigurationManager)
        simulationManager.start()

        # Verify that the mockClientFactory.create method is called with the expected arguments
        self.mockClientFactory.create.assert_called_once_with(self.PROTOCOL.OPENWIRE, creds)

if __name__ == "__main__":
    unittest.main()
