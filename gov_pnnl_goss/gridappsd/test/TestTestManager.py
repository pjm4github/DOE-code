import unittest
from unittest.mock import Mock, patch, PropertyMock
from queue import Queue
import time
import logging

from gov_pnnl_goss.gridappsd.api.TestManager import TestManager
from gov_pnnl_goss.gridappsd.test.AppManagerTest import TestConfiguration


# from gov.pnnl.goss.gridappsd.api.test_configuration import TestConfiguration
# from gov.pnnl.goss.gridappsd.api.test_manager import TestManager


class TestTestManager(unittest.TestCase):

    def setUp(self):
        self.test_config = TestConfiguration()
        self.logger = Mock()
        self.client_factory = Mock()
        self.client = Mock()
        self.arg_captor = Queue()
        self.test_manager = TestManager()

    def test_context(self):
        self.assertIsNotNone(self.test_manager.context)

    def test_load_config(self):
        #   TestManager manager = null;
        #   try {
        #   	manager = getService(TestManager.class);
        #   } catch (InterruptedException e) {
        #   	// TODO Auto-generated catch block
        #   	print(e);
        #   }
        path = "/Users/jsimpson/git/adms/GOSS-GridAPPS-D/gov.pnnl.goss.gridappsd/applications/python/exampleTestConfig.json"
        test_config = self.test_manager.load_test_config(path)
        self.assertEqual(test_config.get_power_system_configuration(), "ieee8500")
        self.assertEqual("ieee8500", "ieee8500")

    def test_get_service(self):
        clazz = TestConfiguration
        service = self.test_manager.get_service(clazz)
        self.assertIsNotNone(service)

    #    @Test
    #    public void testLoadScript(){
    #    	String path = "/Users/jsimpson/git/adms/GOSS-GridAPPS-D/gov.pnnl.goss.gridappsd/applications/python/exampleTestConfig.json";
    #    	TestScript testScript = tm.loadTestScript(path);
    #    	assertEquals(testScript.name,"VVO");
    #    }
    #

    @patch('time.sleep', return_value=None)
    def test_run_test(self, mock_sleep):
        self.test_manager.run_test()
        mock_sleep.assert_called_once_with(1000)

    def tearDown(self):
        # cleanup
        pass


if __name__ == '__main__':
    unittest.main()
