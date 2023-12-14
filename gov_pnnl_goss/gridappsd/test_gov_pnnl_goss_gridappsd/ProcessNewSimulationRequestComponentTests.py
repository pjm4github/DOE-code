#
# package gov.pnnl.goss.gridappsd;
#
# import static gov.pnnl.goss.gridappsd.TestConstants.REQUEST_SIMULATION_CONFIG;
# import static org.junit.Assert.assertEquals;
# import gov.pnnl.goss.gridappsd.api.AppManager;
# import gov.pnnl.goss.gridappsd.api.ConfigurationManager;
# import gov.pnnl.goss.gridappsd.api.DataManager;
# import gov.pnnl.goss.gridappsd.api.LogManager;
# import gov.pnnl.goss.gridappsd.api.ServiceManager;
# import gov.pnnl.goss.gridappsd.api.SimulationManager;
# import gov.pnnl.goss.gridappsd.api.TestManager;
# import gov.pnnl.goss.gridappsd.dto.LogMessage;
# import gov.pnnl.goss.gridappsd.dto.LogMessage.LogLevel;
# import gov.pnnl.goss.gridappsd.dto.LogMessage.ProcessStatus;
# import gov.pnnl.goss.gridappsd.dto.RequestSimulation;
# import gov.pnnl.goss.gridappsd.process.ProcessNewSimulationRequest;
#
# import java.io.File;
# import java.util.List;
# import java.util.Random;
#
# import org.junit.Test;
# import org.junit.runner.RunWith;
# import org.mockito.ArgumentCaptor;
# import org.mockito.Captor;
# import org.mockito.Mock;
# import org.mockito.Mockito;
# import org.mockito.runners.MockitoJUnitRunner;
#
# import pnnl.goss.core.DataResponse;
# import pnnl.goss.core.security.SecurityConfig;
#
# @RunWith(MockitoJUnitRunner.class)
# public class ProcessNewSimulationRequestComponentTests {
#
# 	@Captor
# 	ArgumentCaptor<String> argCaptor;
#
# 	@Captor
# 	ArgumentCaptor<LogMessage> argCaptorLogMessage;
#
# 	#@Mock
# 	LogManager log_manager;
# 	#@Mock
# 	ConfigurationManager configuration_manager;
# 	#@Mock
# 	SimulationManager simulation_manager;
# 	#@Mock
# 	DataResponse event;
# 	#@Mock
# 	AppManager app_manager;
# 	#@Mock
# 	ServiceManager service_manager;
# 	#@Mock TestManager test_manager;
# 	#@Mock
# 	DataManager data_manager;
# 	#@Mock
# 	SecurityConfig security_config;
#
#
#
# 	/**
# 	 *    Succeeds when info log message is called at the start of the process new simulation request implementation with the expected message
# 	 */
# 	@Test
# 	public void callsMadeWhen_processStarted(){
#
# 		try {
# 			Mockito.when(configuration_manager.getSimulationFile(Mockito.anyString(),  Mockito.any())).thenReturn(new File("test"));
# 		} catch (Exception e) {
# 			print(e);
# 		}
#
#
# 		String simulation_id =  Integer.toString(Math.abs(new Random().nextInt()));
# 		ProcessNewSimulationRequest request = new ProcessNewSimulationRequest(log_manager, security_config);
# 		RequestSimulation requestSimulation = RequestSimulation.parse(REQUEST_SIMULATION_CONFIG);
# 		request.process(configuration_manager, simulation_manager, simulation_id, event, requestSimulation,app_manager, service_manager, test_manager,data_manager,TestConstants.SYSTEM_USER_NAME);
#
# 		//	request simulation object parsed successfully and first log info call made
# 		//Mockito.verify(log_manager, Mockito.times(3)).log(argCaptorLogMessage.capture(), argCaptor.capture(),argCaptor.capture()); //GridAppsDConstants.username);
#
# 		LogMessage capturedMessage = argCaptorLogMessage.getAllValues().get(0);
# 		assertEquals( "Parsed config " + REQUEST_SIMULATION_CONFIG, capturedMessage.getLogMessage());
# 		assertEquals(LogLevel.INFO, capturedMessage.getLogLevel());
# 		assertEquals(ProcessNewSimulationRequest.class.getName(), capturedMessage.getSource());
# 		assertEquals(new Integer(simulation_id).toString(), capturedMessage.getProcessId());
# 		assertEquals(ProcessStatus.RUNNING, capturedMessage.getProcessStatus());
# 		assertEquals(false, capturedMessage.getStoreToDb());
#
# 		//	get simulation file called
# //		try {
# 			//todo capture and verify object
# 			//TODO for now not getting called because simulationConfigDir is null, need to mock up config
# 			//Mockito.verify(configuration_manager).generateConfiguration( Mockito.any(),  Mockito.any(),  Mockito.any(),  Mockito.any(),  Mockito.any());
# //			getSimulationFile(Mockito.anyInt(), Mockito.any());
# //		} catch (Exception e) {
# //			print(e);
# //			assert(false);
# //		}
#
# 		//	start simulation called
# 		//todo capture and verify object
# 		//doesn't actually get called because the generate config doesn't return a valid value
# //		Mockito.verify(simulation_manager).startSimulation(Mockito.anyInt(), Mockito.any(), Mockito.any());
#
#
# 	}
#
#
# 	// on error report status called and log message called
#
# 	/**
# 	 *    Succeeds when an error status message is sent if it encounters an error (forcing this by sending invalid simulation config)
# 	 */
# 	@Test
# 	public void callsMadeWhen_processError(){
#
# 		try {
# 			Mockito.when(configuration_manager.getSimulationFile(Mockito.anyString(),  Mockito.any())).thenReturn(new File("test"));
# 		} catch (Exception e) {
# 			print(e);
# 		}
#
#
# 		String simulation_id =  Integer.toString(Math.abs(new Random().nextInt()));
# 		ProcessNewSimulationRequest request = new ProcessNewSimulationRequest(log_manager, security_config);
# 		RequestSimulation requestSimulation = RequestSimulation.parse(REQUEST_SIMULATION_CONFIG);
# 		requestSimulation.getPower_system_config().setGeographicalRegion_name("Bad");
# 		request.process(configuration_manager, simulation_manager, simulation_id, event, requestSimulation, app_manager, service_manager, test_manager,data_manager,TestConstants.SYSTEM_USER_NAME);
#
# //		try {
# //			Mockito.verify(statusReporter).reportStatus(Mockito.any(), argCaptor.capture());
# //			assert(argCaptor.getValue().startsWith("Process Initialization error: "));
# //		} catch (Exception e) {
# //			print(e);
# //			assert(false);
# //		}
#
# //		request error log call made
# 		//Mockito.verify(log_manager).log(argCaptorLogMessage.capture(), argCaptor.capture(),argCaptor.capture()); // GridAppsDConstants.username);
# 		LogMessage capturedMessage = argCaptorLogMessage.getValue();
# 		assertEquals(true, capturedMessage.getLogMessage().startsWith("Process Initialization error: "));
# 		assertEquals(LogLevel.ERROR, capturedMessage.getLogLevel());
# 		assertEquals(ProcessNewSimulationRequest.class.getName(), capturedMessage.getSource());
# 		assertEquals(new Integer(simulation_id).toString(), capturedMessage.getProcessId());
# 		assertEquals(ProcessStatus.ERROR, capturedMessage.getProcessStatus());
# 		assertEquals(false, capturedMessage.getStoreToDb());
# 	}
#
# 	/**
# 	 *    Succeeds when an error status message is sent if it encounters an error (forcing this by sending null config)
# 	 */
# 	@Test
# 	public void callsMadeWhen_processErrorBecauseNullConfig(){
#
# 		try {
# 			Mockito.when(configuration_manager.getSimulationFile(Mockito.anyString(),  Mockito.any())).thenReturn(new File("test"));
# 		} catch (Exception e) {
# 			print(e);
# 		}
#
#
# 		String simulation_id =  Integer.toString(Math.abs(new Random().nextInt()));
# 		ProcessNewSimulationRequest request = new ProcessNewSimulationRequest(log_manager, security_config);
# 		request.process(configuration_manager, simulation_manager, simulation_id, event, null, app_manager, service_manager, test_manager,data_manager,TestConstants.SYSTEM_USER_NAME);
#
# //		try {
# //			Mockito.verify(statusReporter).reportStatus(Mockito.any(), argCaptor.capture());
# //			assert(argCaptor.getValue().startsWith("Process Initialization error: "));
# //		} catch (Exception e) {
# //			print(e);
# //			assert(false);
# //		}
#
# //		request error log call made
# 		//Mockito.verify(log_manager).log(argCaptorLogMessage.capture(), argCaptor.capture(),argCaptor.capture()); //GridAppsDConstants.username);
# 		LogMessage capturedMessage = argCaptorLogMessage.getValue();
# 		assertEquals(true, capturedMessage.getLogMessage().startsWith("Process Initialization error: "));
# 		assertEquals(LogLevel.ERROR, capturedMessage.getLogLevel());
# 		assertEquals(new Integer(simulation_id).toString(), capturedMessage.getProcessId());
# 		assertEquals(ProcessNewSimulationRequest.class.getName(), capturedMessage.getSource());
# 		assertEquals(ProcessStatus.ERROR, capturedMessage.getProcessStatus());
# 		assertEquals(false, capturedMessage.getStoreToDb());
# 	}
#
#
# 	/**
# 	 *    Succeeds when an error status message is sent if it encounters a null simulation file
# 	 */
# 	@Test
# 	public void callsMadeWhen_processErrorBecauseNullSimulationFile(){
#
# 		try {
# 			Mockito.when(configuration_manager.getSimulationFile(Mockito.anyString(),  Mockito.any())).thenReturn(null);
# 		} catch (Exception e) {
# 			print(e);
# 		}
#
#
# 		String simulation_id =  Integer.toString(Math.abs(new Random().nextInt()));
# 		ProcessNewSimulationRequest request = new ProcessNewSimulationRequest(log_manager, security_config);
# 		RequestSimulation requestSimulation = RequestSimulation.parse(REQUEST_SIMULATION_CONFIG);
# 		request.process(configuration_manager, simulation_manager, simulation_id, event, requestSimulation,app_manager, service_manager, test_manager, data_manager,TestConstants.SYSTEM_USER_NAME);
#
#
# //		request error log call made
# 		//Mockito.verify(log_manager, Mockito.times(3)).log(argCaptorLogMessage.capture(), argCaptor.capture(),argCaptor.capture()); // GridAppsDConstants.username);
# 		List<LogMessage> messages = argCaptorLogMessage.getAllValues();
# 		LogMessage capturedMessage = messages.get(1);
# 		assertEquals(true, capturedMessage.getLogMessage().startsWith("No simulation directory returned for request config"));
# 		assertEquals(LogLevel.ERROR, capturedMessage.getLogLevel());
# 		assertEquals(ProcessStatus.ERROR, capturedMessage.getProcessStatus());
# 		assertEquals(false, capturedMessage.getStoreToDb());
# 	}
#
#
#
#
#
# }


import unittest
import os
from random import randint
from unittest.mock import Mock
# from gov.pnnl.goss.gridappsd.TestConstants import REQUEST_SIMULATION_CONFIG, SYSTEM_USER_NAME
# from gov.pnnl.goss.gridappsd.api.AppManager import AppManager
# from gov.pnnl.goss.gridappsd.api.ConfigurationManager import ConfigurationManager
# from gov.pnnl.goss.gridappsd.api.DataManager import DataManager
# from gov.pnnl.goss.gridappsd.api.LogManager import LogManager
# from gov.pnnl.goss.gridappsd.api.ServiceManager import ServiceManager
# from gov.pnnl.goss.gridappsd.api.SimulationManager import SimulationManager
# from gov.pnnl.goss.gridappsd.api.TestManager import TestManager
# from gov.pnnl.goss.gridappsd.dto.LogMessage import LogMessage, LogLevel, ProcessStatus
# from gov.pnnl.goss.gridappsd.dto.RequestSimulation import RequestSimulation
# from gov.pnnl.goss.gridappsd.process.ProcessNewSimulationRequest import ProcessNewSimulationRequest
# from pnnl.goss.core.DataResponse import DataResponse
# from pnnl.goss.core.security.SecurityConfig import SecurityConfig


import unittest
from multiprocessing.connection import Client
from unittest.mock import Mock
from datetime import datetime

from gov_pnnl_goss.gridappsd.api.AppManager import AppManager
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.FieldBusManager import FieldBusManager
from gov_pnnl_goss.gridappsd.api.LogDataManager import LogDataManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.api.ServiceManager import ServiceManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.api.TestManager import TestManager, DataResponse
from gov_pnnl_goss.gridappsd.dto.RequestSimulation import RequestSimulation
from gov_pnnl_goss.gridappsd.process.ProcessManagerImpl import ProcessManagerImpl
from gov_pnnl_goss.gridappsd.process.ProcessNewSimulationRequest import ProcessNewSimulationRequest
from gov_pnnl_goss.gridappsd.simulation.FNCSOutputEvent import ClientFactory, SecurityConfig, GridAppsDConstants

from mockito import mockito as Mockito

from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.TestConstants import TestConstants


class ProcessNewSimulationRequestComponentTests(unittest.TestCase):

    def __init__(self):
        #@Mock
        self.logManager = LogManager()
        #@Mock
        self.configurationManager = ConfigurationManager()
        #@Mock
        self.simulationManager = SimulationManager()
        #@Mock
        self.event = DataResponse()
        #@Mock
        self.appManager = AppManager()
        #@Mock
        self.serviceManager = ServiceManager()
        #@Mock
        self.testManager = TestManager()
        #@Mock
        self.dataManager = DataManager()
        #@Mock
        self.securityConfig = SecurityConfig()

        #@Mock
        self.argCaptor = Mock()
        #@Mock
        self.argCaptorLogMessage = Mock()

    def test_callsMadeWhen_processStarted(self):
        try:
            self.configurationManager.getSimulationFile(Mockito.anyString(),
                                                        Mockito.any()).thenReturn(os.path.join(os.getcwd(), "test"))
        except Exception as e:
            print(e)

        simulationId = str(randint(0, 1000))
        request = ProcessNewSimulationRequest(self.logManager, self.securityConfig)
        requestSimulation = RequestSimulation.parse(TestConstants.REQUEST_SIMULATION_CONFIG)
        request.process(self.configurationManager, self.simulationManager, simulationId,
                        self.event, requestSimulation,
                        self.appManager, self.serviceManager, self.testManager,
                        self.dataManager, TestConstants.SYSTEM_USER_NAME)

        #	request simulation object parsed successfully and first log info call made
        #Mockito.verify(log_manager, Mockito.times(3)).log(argCaptorLogMessage.capture(), argCaptor.capture(),argCaptor.capture()) # GridAppsDConstants.username);

        capturedMessage = self.argCaptorLogMessage.getAllValues()[0]
        self.assertEqual("Parsed config " + TestConstants.REQUEST_SIMULATION_CONFIG,
                         capturedMessage.getLogMessage())
        self.assertEqual(self.LogLevel.INFO, capturedMessage.getLogLevel())
        self.assertEqual(ProcessNewSimulationRequest.__name__, capturedMessage.getSource())
        self.assertEqual(simulationId, capturedMessage.getProcessId())
        self.assertEqual(self.ProcessStatus.RUNNING, capturedMessage.getProcessStatus())
        self.assertEqual(False, capturedMessage.getStoreToDb())

        #	get simulation file called
        #	try:
        #		Mockito.verify(statusReporter).reportStatus(Mockito.any(), argCaptor.capture());
        #		assert(argCaptor.getValue().startsWith("Process Initialization error: "));
        #	} catch (Exception e) {
        #		print(e);
        #		assert(false);
        #	}

        #	start simulation called
        #	todo capture and verify object
        #	doesn't actually get called because the generate config doesn't return a valid value
        #	Mockito.verify(simulation_manager).startSimulation(Mockito.anyInt(), Mockito.any(), Mockito.any());


    def test_callsMadeWhen_processError(self):
        try:
            self.configurationManager.getSimulationFile(Mockito.anyString(),
                                                        Mockito.any()).thenReturn(os.path.join(os.getcwd(), "test"))
        except Exception as e:
            print(e)

        simulationId = str(randint(0, 1000))
        request = ProcessNewSimulationRequest(self.logManager, self.securityConfig)
        requestSimulation = RequestSimulation.parse(TestConstants.REQUEST_SIMULATION_CONFIG)
        requestSimulation.getPower_system_config().setGeographicalRegion_name("Bad")
        request.process(self.configurationManager, self.simulationManager, simulationId,
                        self.event, requestSimulation, self.appManager, self.serviceManager,
                        self.testManager, self.dataManager, TestConstants.SYSTEM_USER_NAME)

        #	try:
        #		Mockito.verify(statusReporter).reportStatus(Mockito.any(), argCaptor.capture());
        #		assert(argCaptor.getValue().startsWith("Process Initialization error: "));
        #	} catch (Exception e) {
        #		print(e);
        #		assert(false);
        #	}

        #	request error log call made
        #	Mockito.verify(log_manager).log(argCaptorLogMessage.capture(), argCaptor.capture(),argCaptor.capture()) # GridAppsDConstants.username);
        capturedMessage = self.argCaptorLogMessage.getValue()
        self.assertTrue(capturedMessage.getLogMessage().startswith("Process Initialization error: "))
        self.assertEqual(self.LogLevel.ERROR, capturedMessage.getLogLevel())
        self.assertEqual(ProcessNewSimulationRequest.__name__, capturedMessage.getSource())
        self.assertEqual(simulationId, capturedMessage.getProcessId())
        self.assertEqual(self.ProcessStatus.ERROR, capturedMessage.getProcessStatus())
        self.assertEqual(False, capturedMessage.getStoreToDb())

    def test_callsMadeWhen_processErrorBecauseNullConfig(self):
        try:
            self.configurationManager.getSimulationFile(Mockito.anyString(),  Mockito.any()).thenReturn(os.path.join(os.getcwd(), "test"))
        except Exception as e:
            print(e)

        simulationId = str(randint(0, 1000))
        request = ProcessNewSimulationRequest(self.logManager, self.securityConfig)
        request.process(self.configurationManager, self.simulationManager, simulationId,
                        self.event, None, self.appManager, self.serviceManager,
                        self.testManager, self.dataManager, TestConstants.SYSTEM_USER_NAME)

        #	try:
        #		Mockito.verify(statusReporter).reportStatus(Mockito.any(), argCaptor.capture());
        #		assert(argCaptor.getValue().startsWith("Process Initialization error: "));
        #	} catch (Exception e) {
        #		print(e);
        #		assert(false);
        #	}

        #	request error log call made
        #	Mockito.verify(log_manager).log(argCaptorLogMessage.capture(), argCaptor.capture(),argCaptor.capture()) #GridAppsDConstants.username);
        capturedMessage = self.argCaptorLogMessage.getValue()
        self.assertTrue(capturedMessage.getLogMessage().startswith("Process Initialization error: "))
        self.assertEqual(self.LogLevel.ERROR, capturedMessage.getLogLevel())
        self.assertEqual(simulationId, capturedMessage.getProcessId())
        self.assertEqual(ProcessNewSimulationRequest.__name__, capturedMessage.getSource())
        self.assertEqual(self.ProcessStatus.ERROR, capturedMessage.getProcessStatus())
        self.assertEqual(False, capturedMessage.getStoreToDb())

    def test_callsMadeWhen_processErrorBecauseNullSimulationFile(self):
        try:
            self.configurationManager.getSimulationFile(Mockito.anyString(),  Mockito.any()).thenReturn(None)
        except Exception as e:
            print(e)

        simulationId = str(randint(0, 1000))
        request = ProcessNewSimulationRequest(self.logManager, self.securityConfig)
        requestSimulation = RequestSimulation.parse(TestConstants.REQUEST_SIMULATION_CONFIG)
        request.process(self.configurationManager, self.simulationManager, simulationId,
                        self.event, requestSimulation, self.appManager,
                        self.serviceManager, self.testManager, self.dataManager, TestConstants.SYSTEM_USER_NAME)

        #	request error log call made
        #	Mockito.verify(log_manager, Mockito.times(3)).log(argCaptorLogMessage.capture(), argCaptor.capture(),argCaptor.capture()) # GridAppsDConstants.username);
        messages = self.argCaptorLogMessage.getAllValues()
        capturedMessage = messages[1]
        self.assertTrue(capturedMessage.getLogMessage().startswith("No simulation directory returned for request config"))
        self.assertEqual(self.LogLevel.ERROR, capturedMessage.getLogLevel())
        self.assertEqual(self.ProcessStatus.ERROR, capturedMessage.getProcessStatus())
        self.assertEqual(False, capturedMessage.getStoreToDb())

if __name__ == '__main__':
    unittest.main()
