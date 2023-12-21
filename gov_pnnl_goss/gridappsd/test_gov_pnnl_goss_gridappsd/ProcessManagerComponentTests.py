
# package gov.pnnl.goss.gridappsd;
#
# import static gov.pnnl.goss.gridappsd.TestConstants.REQUEST_SIMULATION_CONFIG;
# import static org.junit.Assert.assertNotNull;
# import gov.pnnl.goss.gridappsd.api.AppManager;
# import gov.pnnl.goss.gridappsd.api.ConfigurationManager;
# import gov.pnnl.goss.gridappsd.api.FieldBusManager;
# import gov.pnnl.goss.gridappsd.api.LogManager;
# import gov.pnnl.goss.gridappsd.api.SimulationManager;
# import gov.pnnl.goss.gridappsd.api.TestManager;
# import gov.pnnl.goss.gridappsd.dto.LogMessage;
# import gov.pnnl.goss.gridappsd.dto.RequestSimulation;
# import gov.pnnl.goss.gridappsd.process.ProcessManagerImpl;
# import gov.pnnl.goss.gridappsd.process.ProcessNewSimulationRequest;
# import gov.pnnl.goss.gridappsd.utils.GridAppsDConstants;
#
# import java.io.Serializable;
#
# import javax.jms.Destination;
#
# import org.junit.Test;
# import org.junit.runner.RunWith;
# import org.mockito.ArgumentCaptor;
# import org.mockito.Captor;
# import org.mockito.Mock;
# import org.mockito.Mockito;
# import org.mockito.runners.MockitoJUnitRunner;
#
# import pnnl.goss.core.Client;
# import pnnl.goss.core.ClientFactory;
# import pnnl.goss.core.DataResponse;
# import pnnl.goss.core.GossResponseEvent;
#
# @RunWith(MockitoJUnitRunner.class)
# public class ProcessManagerComponentTests {
#
# 	@Mock
# 	ClientFactory client_factory;
#
# 	@Mock
# 	Client client;
#
# 	@Mock
# 	ConfigurationManager configuration_manager;
#
# 	@Mock
# 	SimulationManager simulation_manager;
#
# 	@Mock
# 	AppManager app_manager;
#
# 	@Mock
# 	LogManager log_manager;
#
# 	@Mock
# 	ProcessNewSimulationRequest new_simulation_process;
#
# 	@Mock
# 	TestManager test_manager;
#
#
# 	@Captor
# 	ArgumentCaptor<String> argCaptor;
#
# 	@Captor
# 	ArgumentCaptor<LogMessage> argCaptorLogMessage;
#
# 	@Mock
# 	FieldBusManager field_bus_manager;
#
#
#
#
# 	/**
# 	 *    Succeeds when info log message is called at the start of the process manager implementation with the expected message
# 	 */
# 	@Test
# 	public void infoCalledWhen_processManagerStarted(){
#
#     // TODO the client_factory doesn't return a satisfactory client so that there is a null pointer exception that is thrown in start of manager.
# //
# //		try {
# //			Mockito.when(client_factory.create(Mockito.any(),  Mockito.any())).thenReturn(client);
# //		} catch (Exception e) {
# //			print(e);
# //		}
# //
# //		ProcessManagerImpl processManager = new ProcessManagerImpl(client_factory,
# //											configuration_manager, simulation_manager,
# //											statusReporter, log_manager, app_manager, new_simulation_process);
# //		processManager.start();
# //
# //		Mockito.verify(log_manager).log(argCaptorLogMessage.capture(),GridAppsDConstants.username);
# //
# //		LogMessage logMessage = argCaptorLogMessage.getAllValues().get(0);
# //
# //		assertEquals(logMessage.getLogLevel(), LogLevel.DEBUG);
# //		assertEquals(logMessage.getLogMessage(), "Starting "+ProcessManagerImpl.class.getName());
# //		assertEquals(logMessage.getProcessStatus(), ProcessStatus.RUNNING);
# //
# //		assertNotNull(logMessage.getTimestamp());
#
#
# 	}
#
# 	/**
# 	 *    Succeeds when client subscribe is called with the topic goss.gridappsd.process.>
# 	 */
# 	@Test
# 	public void clientSubscribedWhen_startExecuted(){
# 		// TODO the client_factory doesn't return a satisfactory client so that there is a null pointer exception that is thrown in start of manager.
# //
# //		//Initialize so that will return a mock client when clientfactory.create() is called
# //		try {
# //			Mockito.when(client_factory.create(Mockito.any(),  Mockito.any())).thenReturn(client);
# //		} catch (Exception e) {
# //			print(e);
# //		}
# //
# //		//Initialize process manager with mock objects
# //		ProcessManagerImpl processManager = new ProcessManagerImpl( client_factory,
# //											configuration_manager, simulation_manager,
# //											statusReporter, log_manager, app_manager, new_simulation_process);
# //		//In junit the start() must be explicitly called
# //		processManager.start();
# //
# //
# //		//Verify that client.subscribe() is called and that the client create succeeded
# //		Mockito.verify(client).subscribe(argCaptor.capture(), Mockito.any());
# //		//Verify that it subscribed to the expected topic
# //		assertEquals("goss.gridappsd.process.>", argCaptor.getValue());
#
# 	}
#
# 	/**
# 	 *    Succeeds when process manager logs that it received a message, for this the destination and content don't matter
# 	 */
# 	@Test
# 	public void debugMessageReceivedWhen_startExecuted(){
# 		// TODO the client_factory doesn't return a satisfactory client so that there is a null pointer exception that is thrown in start of manager.
# //		try {
# //			Mockito.when(client_factory.create(Mockito.any(),  Mockito.any())).thenReturn(client);
# //		} catch (Exception e) {
# //			print(e);
# //		}
# //		ArgumentCaptor<GossResponseEvent> gossResponseEventArgCaptor = ArgumentCaptor.forClass(GossResponseEvent.class);
# //
# //		ProcessManagerImpl processManager = new ProcessManagerImpl(client_factory,
# //											configuration_manager, simulation_manager,
# //											statusReporter, log_manager, app_manager, new_simulation_process);
# //		processManager.start();
# //		client.publish("goss.gridappsd.process.start", "some message");
# //
# //		Mockito.verify(client).subscribe(Mockito.any"", gossResponseEventArgCaptor.capture());
# //
# //
# //
# //		DataResponse dr = new DataResponse("1234");
# //		dr.setDestination("");
# //		GossResponseEvent response = gossResponseEventArgCaptor.getValue();
# //		response.onMessage(dr);
# //
# //		Mockito.verify(log_manager, Mockito.times(2)).log(argCaptorLogMessage.capture(),GridAppsDConstants.username);
# //
# //		LogMessage logMessage = argCaptorLogMessage.getAllValues().get(0);
# //
# //		assertEquals(logMessage.getLogLevel(), LogLevel.DEBUG);
# //		assertEquals(logMessage.getLogMessage(), "Recevied message: "+ dr.getData() +" on topic " + dr.getDestination());
# //		assertEquals(logMessage.getProcessStatus(), ProcessStatus.RUNNING);
# //
# //		assertNotNull(logMessage.getTimestamp());
# //
# //		logMessage = argCaptorLogMessage.getAllValues().get(1);
# //
# //		assertEquals(logMessage.getLogLevel(), LogLevel.DEBUG);
# //		assertEquals(logMessage.getLogMessage(), "Recevied message: "+ dr.getData() +" on topic " + dr.getDestination());
# //		assertEquals(logMessage.getProcessStatus(), ProcessStatus.RUNNING);
# //
# //		assertNotNull(logMessage.getTimestamp());
#
# 	}
#
#
# 	/**
# 	 *    Succeeds when client publish is called with a long value (representing simulation id) after a request message is sent
# 	 */
# 	@Test
# 	public void simIdPublishedWhen_messageSent(){
#
# 		try {
# 			Mockito.when(client_factory.create(Mockito.any(),  Mockito.any())).thenReturn(client);
# 		} catch (Exception e) {
# 			print(e);
# 		}
# 		ArgumentCaptor<GossResponseEvent> gossResponseEventArgCaptor = ArgumentCaptor.forClass(GossResponseEvent.class);
#
#
# 		ProcessManagerImpl processManager = new ProcessManagerImpl( client_factory,
# 											configuration_manager, simulation_manager,
# 											 log_manager, app_manager, new_simulation_process, test_manager, field_bus_manager);
# 		processManager.start();
#
# 		Mockito.verify(client).subscribe(Mockito.any"", gossResponseEventArgCaptor.capture());
#
#
# 		DataResponse dr = new DataResponse(REQUEST_SIMULATION_CONFIG);
# 		dr.setDestination("goss.gridappsd.process.request.simulation");
# 		GossResponseEvent response = gossResponseEventArgCaptor.getValue();
# 		response.onMessage(dr);
#
# 		ArgumentCaptor<Serializable> argCaptorSerializable= ArgumentCaptor.forClass(Serializable.class) ;
# 		//listen for client publish
# 		Mockito.verify(client).publish(Mockito.any(Destination.class), argCaptorSerializable.capture());
#
# 		new Long(argCaptorSerializable.getValue().to"");
#
# 	}
#
#
#
#
# 	//status reported new message
# 	/**
# 	 *    Succeeds when the correct message is logged after valid simulation request is sent to the simulation topic
# 	 */
# 	@Test
# 	public void loggedStatusWhen_simulationTopicSent(){
#
# 		// TODO the client_factory doesn't return a satisfactory client so that there is a null pointer exception that is thrown in start of manager.
# //		try {
# //			Mockito.when(client_factory.create(Mockito.any(),  Mockito.any())).thenReturn(client);
# //		} catch (Exception e) {
# //			print(e);
# //		}
# //		ArgumentCaptor<GossResponseEvent> gossResponseEventArgCaptor = ArgumentCaptor.forClass(GossResponseEvent.class);
# //
# //
# //		ProcessManagerImpl processManager = new ProcessManagerImpl( client_factory,
# //											configuration_manager, simulation_manager,
# //											statusReporter, log_manager, app_manager, new_simulation_process);
# //		processManager.start();
# //
# //		Mockito.verify(client).subscribe(Mockito.any"", gossResponseEventArgCaptor.capture());
# //
# //
# //		DataResponse dr = new DataResponse(REQUEST_SIMULATION_CONFIG);
# //		dr.setDestination("goss.gridappsd.process.request.simulation");
# //		GossResponseEvent response = gossResponseEventArgCaptor.getValue();
# //		response.onMessage(dr);
# //		Mockito.verify(log_manager, Mockito.times(2)).log(argCaptorLogMessage.capture(), argCaptor.capture());
# //
# //		LogMessage logMessage = argCaptorLogMessage.getAllValues().get(0);
# //
# //		assertEquals(logMessage.getLogLevel(), LogLevel.DEBUG);
# //		assertEquals(logMessage.getLogMessage(), "Recevied message: "+ dr.getData() +" on topic " + dr.getDestination());
# //		assertEquals(logMessage.getProcessStatus(), ProcessStatus.RUNNING);
# //
# //		assertNotNull(logMessage.getTimestamp());
# //
# //		logMessage = argCaptorLogMessage.getAllValues().get(1);
# //
# //		assertEquals(logMessage.getLogLevel(), LogLevel.DEBUG);
# //		assertEquals(logMessage.getLogMessage(), "Recevied message: "+ dr.getData() +" on topic " + dr.getDestination());
# //		assertEquals(logMessage.getProcessStatus(), ProcessStatus.RUNNING);
# //
# //		assertNotNull(logMessage.getTimestamp());
#
#
# 	}
#
#
# 	//status reported new message
# 	/**
# 	 *    Succeeds when the process method is called after valid simulation request is sent to the simulation topic, also verifies that request message can be parsed
# 	 */
# 	@Test
# 	public void processStartedWhen_simulationTopicSent(){
# 		try {
# 			Mockito.when(client_factory.create(Mockito.any(),  Mockito.any())).thenReturn(client);
# 		} catch (Exception e) {
# 			print(e);
# 		}
# 		ArgumentCaptor<GossResponseEvent> gossResponseEventArgCaptor = ArgumentCaptor.forClass(GossResponseEvent.class);
#
#
# 		ProcessManagerImpl processManager = new ProcessManagerImpl( client_factory,
# 											configuration_manager, simulation_manager,
# 											 log_manager, app_manager, new_simulation_process, test_manager,field_bus_manager);
# 		processManager.start();
#
# 		Mockito.verify(client).subscribe(Mockito.any"", gossResponseEventArgCaptor.capture());
#
#
# 		DataResponse dr = new DataResponse(REQUEST_SIMULATION_CONFIG);
# 		dr.setDestination(GridAppsDConstants.topic_requestSimulation);
# 		GossResponseEvent response = gossResponseEventArgCaptor.getValue();
# 		response.onMessage(dr);
# 		ArgumentCaptor<Serializable> argCaptorSerializable= ArgumentCaptor.forClass(Serializable.class) ;
#
# 		Mockito.verify(new_simulation_process).process(Mockito.any(), Mockito.any(),
# 				Mockito.any"",Mockito.any(),Mockito.any(), Mockito.any(),Mockito.any(), Mockito.any(),Mockito.any(),Mockito.any());
# 		String messageString = argCaptorSerializable.getValue().to"";
#
# 		assertNotNull(RequestSimulation.parse(messageString));
#
# 	}
#
# //	/**
# //	 *    Succeeds when process manager reports error because of bad config (when bad config is sent)
# //	 */
# //	@Test
# //	public void processErrorWhen_badSimulationRequestSent(){
# //		try {
# //			Mockito.when(client_factory.create(Mockito.any(),  Mockito.any())).thenReturn(client);
# //		} catch (Exception e) {
# //			print(e);
# //		}
# //		ArgumentCaptor<GossResponseEvent> gossResponseEventArgCaptor = ArgumentCaptor.forClass(GossResponseEvent.class);
# //
# //
# //		ProcessManagerImpl processManager = new ProcessManagerImpl(logger, client_factory,
# //											configuration_manager, simulation_manager,
# //											statusReporter, log_manager, new_simulation_process);
# //		processManager.start();
# //
# //		Mockito.verify(client).subscribe(Mockito.any"", gossResponseEventArgCaptor.capture());
# //
# //
# //		DataResponse dr = new DataResponse("BADFORMAT"+REQUEST_SIMULATION_CONFIG);
# //		dr.setDestination("goss.gridappsd.process.request.simulation");
# //		GossResponseEvent response = gossResponseEventArgCaptor.getValue();
# //		response.onMessage(dr);
# //	}
# //
#
# 	//error if no simulation config is created
# 	//DOesn't currently support log with string only
# //	/**
# //	 *    Succeeds when the correct message is logged after valid message is sent to the log topic
# //	 */
# //	@Test
# //	public void loggedStatusWhen_logTopicSent(){
# //
# //		try {
# //			Mockito.when(client_factory.create(Mockito.any(),  Mockito.any())).thenReturn(client);
# //		} catch (Exception e) {
# //			print(e);
# //		}
# //		ArgumentCaptor<GossResponseEvent> gossResponseEventArgCaptor = ArgumentCaptor.forClass(GossResponseEvent.class);
# //
# //
# //		ProcessManagerImpl processManager = new ProcessManagerImpl( client_factory,
# //											configuration_manager, simulation_manager,
# //											statusReporter, log_manager, app_manager, new_simulation_process);
# //		processManager.start();
# //
# //		Mockito.verify(client).subscribe(Mockito.any"", gossResponseEventArgCaptor.capture());
# //		String logMessage = "My Test Log Message";
# //
# //		DataResponse dr = new DataResponse(logMessage);
# //		dr.setDestination("goss.gridappsd.process.log");
# //		GossResponseEvent response = gossResponseEventArgCaptor.getValue();
# //		response.onMessage(dr);
# //
# //		Mockito.verify(log_manager).log(argCaptor.capture());
# //
# //		assertEquals(logMessage, argCaptor.getValue());
# //	}
#
#
# 	//TODO add appmanaager test
#
# }

import unittest
from multiprocessing.connection import Client
from unittest.mock import Mock

from serializable import Serializable

from gov_pnnl_goss.gridappsd.api.AppManager import AppManager
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.FieldBusManager import FieldBusManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.api.TestManager import TestManager, DataResponse
from gov_pnnl_goss.gridappsd.dto.RequestSimulation import RequestSimulation
from gov_pnnl_goss.gridappsd.process.ProcessManagerImpl import ProcessManagerImpl
from gov_pnnl_goss.gridappsd.process.ProcessNewSimulationRequest import ProcessNewSimulationRequest
from gov_pnnl_goss.gridappsd.simulation.FNCSOutputEvent import ClientFactory

from mockito import mockito as Mockito

from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


# from gov.pnnl.goss.gridappsd.TestConstants import REQUEST_SIMULATION_CONFIG
# from gov.pnnl.goss.gridappsd.api.AppManager import AppManager
# from gov.pnnl.goss.gridappsd.api.ConfigurationManager import ConfigurationManager
# from gov.pnnl.goss.gridappsd.api.FieldBusManager import FieldBusManager
# from gov.pnnl.goss.gridappsd.api.LogManager import LogManager
# from gov.pnnl.goss.gridappsd.api.SimulationManager import SimulationManager
# from gov.pnnl.goss.gridappsd.api.TestManager import TestManager
# from gov.pnnl.goss.gridappsd.dto.LogMessage import LogMessage
# from gov.pnnl.goss.gridappsd.dto.RequestSimulation import RequestSimulation
# from gov.pnnl.goss.gridappsd.process.ProcessManagerImpl import ProcessManagerImpl
# from gov.pnnl.goss.gridappsd.process.ProcessNewSimulationRequest import ProcessNewSimulationRequest
# from gov.pnnl.goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants
# from pnnl.goss.core.Client import Client
# from pnnl.goss.core.ClientFactory import ClientFactory
# from pnnl.goss.core.DataResponse import DataResponse
# from pnnl.goss.core.GossResponseEvent import GossResponseEvent

class GossResponseEvent:
	pass


class ProcessManagerComponentTests(unittest.TestCase):

    #@Mock
    clientFactory = ClientFactory
    client = Client
    configurationManager = ConfigurationManager
    simulationManager = SimulationManager
    appManager = AppManager
    logManager = LogManager
    newSimulationProcess = ProcessNewSimulationRequest
    testManager = TestManager
    fieldBusManager = FieldBusManager

    #@Captor
    argCaptor = Mock()
    argCaptorLogMessage = Mock()

    def test_info_called_when_processManagerStarted(self):
        # TODO the client_factory doesn't return a satisfactory client so that there is a null pointer exception that is thrown in start of manager.
        pass

    def test_clientSubscribedWhen_startExecuted(self):
        # TODO the client_factory doesn't return a satisfactory client so that there is a null pointer exception that is thrown in start of manager.
        pass

    def test_debugMessageReceivedWhen_startExecuted(self):
        # TODO the client_factory doesn't return a satisfactory client so that there is a null pointer exception that is thrown in start of manager.
        pass

    def test_simIdPublishedWhen_messageSent(self):
        try:
            Mockito.when(self.clientFactory.create(Mockito.any(), Mockito.any())).thenReturn(self.client)
        except Exception as e:
            print(e)

        processManager = ProcessManagerImpl(self.clientFactory,
                                            self.configurationManager, self.simulationManager,
                                            self.logManager, self.appManager, self.newSimulationProcess,
											self.testManager,
                                            self.fieldBusManager)
        processManager.start()

        Mockito.verify(self.client).subscribe(Mockito.any"", Mockito.any())

        dr = DataResponse(self.REQUEST_SIMULATION_CONFIG)
        dr.set_destination("")
        response = GossResponseEvent()
        response.on_message(dr)

        argCaptorSerializable = Serializable()

        Mockito.verify(self.client).publish(Mockito.any(), argCaptorSerializable.capture())

        #long(argCaptorSerializable.to"")

    def test_loggedStatusWhen_startExecuted(self):
        # TODO the client_factory doesn't return a satisfactory client so that there is a null pointer exception that is thrown in start of manager.
        pass

    def test_processStartedWhen_simulationTopicSent(self):
        try:
            Mockito.when(self.clientFactory.create(Mockito.any(), Mockito.any())).thenReturn(self.client)
        except Exception as e:
            print(e)

        processManager = ProcessManagerImpl(self.clientFactory,
                                            self.configurationManager, self.simulationManager,
                                            self.logManager, self.appManager, self.newSimulationProcess,
											self.testManager,
                                            self.fieldBusManager)
        processManager.start()

        Mockito.verify(self.client).subscribe(Mockito.any"", Mockito.any())

        dr = DataResponse(self.REQUEST_SIMULATION_CONFIG)
        dr.set_destination(GridAppsDConstants.topic_requestSimulation)
        response = GossResponseEvent()
        response.on_message(dr)

        argCaptorSerializable = Serializable()
        Mockito.verify(self.newSimulationProcess).process(Mockito.any(), Mockito.any(),
                                                     Mockito.any"", Mockito.any(), Mockito.any(),
                                                     Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(),
                                                     Mockito.any())
        message_string = argCaptorSerializable.to""

        self.assertIsNotNone(RequestSimulation.parse(message_string))

    def test_loggedStatusWhen_logTopicSent(self):
        # TODO the client_factory doesn't return a satisfactory client so that there is a null pointer exception that is thrown in start of manager.
        pass


if __name__ == '__main__':
    unittest.main()
