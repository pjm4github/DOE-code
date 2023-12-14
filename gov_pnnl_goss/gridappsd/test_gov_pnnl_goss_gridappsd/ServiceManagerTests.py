#
# package gov.pnnl.goss.gridappsd;
#
# import gov.pnnl.goss.gridappsd.api.LogManager;
# import gov.pnnl.goss.gridappsd.service.ServiceManagerImpl;
#
# import java.io.File;
# import java.util.HashMap;
# import java.util.Hashtable;
# import java.util.Map;
#
# import org.junit.Before;
# import org.junit.Test;
# import org.junit.runner.RunWith;
# import org.mockito.Mock;
# import org.mockito.runners.MockitoJUnitRunner;
#
# import pnnl.goss.core.ClientFactory;
#
# @RunWith(MockitoJUnitRunner.class)
# public class ServiceManagerTests {
#
# 	@Mock
# 	LogManager log_manager;
#
# 	@Mock
# 	ClientFactory client_factory;
#
# 	ServiceManagerImpl service_manager;
#
# 	@Before
# 	public void beforeTests(){
# 		service_manager = new ServiceManagerImpl(log_manager, client_factory);
#
# 		//use directory relative to current running directory
# 		File functions = new File("");
# 		File currentDir = new File(functions.getAbsolutePath());
# 		File parentDir = currentDir.getParentFile();
#
# 		Hashtable<String, String> props = new Hashtable<String, String>();
# 		props.put("applications.path", parentDir.getAbsolutePath()+File.separator+"applications");
# 		props.put("services.path", parentDir.getAbsolutePath()+File.separator+"services");
# 		service_manager.updated(props);
#
# 		service_manager.start();
# 	}
#
# 	@Test
# 	public void testPythonServiceStart_WithNoDependencyNoSimulation(){
# 		//This will only succeed if fncs is installed on the system
# //		service_manager.startService("fncs", null);
# 	}
#
# 	@Test
# 	public void testPythonServiceStart_WithDependencyAndSimulation(){
#
# 		HashMap<String, Object> props = new HashMap<String, Object>();
# 		props.put("simulation_id", "simulation_1");
#
# 		service_manager.startService("fncsgossbridge", props);
# 	}
#
# 	@Test
# 	public void testCppServiceStart_WithDependencyAndSimulation(){
# 		//This will only succeed if gridlabd is installed on the system
# //		service_manager.startService("GridLAB-D", "simulation_1");
# 	}
#
# }


import unittest
import os

from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.simulation.FNCSOutputEvent import ClientFactory


# from goss.gridappsd import LogManager
# from goss.gridappsd.service import ServiceManagerImpl
# from goss.core import ClientFactory


class ServiceManagerImpl:
	pass


class ServiceManagerTests(unittest.TestCase):

	def setUp(self):
		self.logger = LogManager(ServiceManagerTests.__name__)
		self.clientFactory = ClientFactory()
		self.serviceManager = ServiceManagerImpl(self.logger, self.clientFactory)

		# Use a directory relative to the current running directory
		current_dir = os.path.abspath(os.path.dirname(__file__))
		parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

		props = {
			"applications.path": os.path.join(parent_dir, "applications"),
			"services.path": os.path.join(parent_dir, "services")
		}

		self.serviceManager.updated(props)
		self.serviceManager.start()

	def test_python_service_start_with_no_dependency_no_simulation(self):
		# This will only succeed if FNCS is installed on the system
		pass

	# self.service_manager.start_service("fncs", None)

	def test_python_service_start_with_dependency_and_simulation(self):
		props = {"simulation_id": "simulation_1"}
		self.serviceManager.start_service("fncsgossbridge", props)

	def test_cpp_service_start_with_dependency_and_simulation(self):
		# This will only succeed if GridLAB-D is installed on the system
		pass
	# self.service_manager.start_service("GridLAB-D", "simulation_1")


if __name__ == '__main__':
	unittest.main()
