from gov_pnnl_goss.SpecialClasses import UsernamePasswordCredentials
from gov_pnnl_goss.core.client.GossClient import Protocol


import unittest
from mockito import mock, when

from gov_pnnl_goss.gridappsd.test.TestConstants import TestConstants


class TestSimulationStart(unittest.TestCase):

    def setUp(self):
        self.client_factory = None
        self.client = None

    def test_gridappsd(self):
        credentials = UsernamePasswordCredentials("system", "manager")
        when(self.client_factory.create(Protocol.STOMP, credentials)).thenReturn(self.client)
        
        simulation_id = self.client.getResponse(TestConstants.REQUEST_SIMULATION_CONFIG_ESC, "goss.gridappasd.process.request.simulation", None).toString()

        self.assertIsNotNone(simulation_id)

if __name__ == '__main__':
    unittest.main()
