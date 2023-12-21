# package gov.pnnl.goss.gridappsd;
#
# import gov.pnnl.goss.gridappsd.api.AppManager;
# import gov.pnnl.goss.gridappsd.api.ConfigurationManager;
# import gov.pnnl.goss.gridappsd.api.DataManager;
# import gov.pnnl.goss.gridappsd.api.FieldBusManager;
# import gov.pnnl.goss.gridappsd.api.LogDataManager;
# import gov.pnnl.goss.gridappsd.api.LogManager;
# import gov.pnnl.goss.gridappsd.api.RoleManager;
# import gov.pnnl.goss.gridappsd.api.ServiceManager;
# import gov.pnnl.goss.gridappsd.api.SimulationManager;
# import gov.pnnl.goss.gridappsd.api.TestManager;
# import gov.pnnl.goss.gridappsd.data.DataManagerImpl;
# import gov.pnnl.goss.gridappsd.dto.LogMessage.LogLevel;
# import gov.pnnl.goss.gridappsd.dto.LogMessage.ProcessStatus;
# import gov.pnnl.goss.gridappsd.dto.PowergridModelDataRequest;
# import gov.pnnl.goss.gridappsd.process.ProcessEvent;
# import gov.pnnl.goss.gridappsd.process.ProcessManagerImpl;
# import gov.pnnl.goss.gridappsd.process.ProcessNewSimulationRequest;
# import gov.pnnl.goss.gridappsd.utils.GridAppsDConstants;
#
# import java.text.ParseException;
#
# import org.junit.Test;
# import org.junit.runner.RunWith;
# import org.mockito.ArgumentCaptor;
# import org.mockito.Captor;
# import org.mockito.Mock;
# import org.mockito.runners.MockitoJUnitRunner;
#
# import pnnl.goss.core.Client;
# import pnnl.goss.core.ClientFactory;
# import pnnl.goss.core.DataResponse;
# import pnnl.goss.core.security.SecurityConfig;
#
# @RunWith(MockitoJUnitRunner.class)
# public class ProcessEventTests {
#
# 	@Mock
# 	LogDataManager logDataManager;
# 	@Mock
# 	ProcessManagerImpl processManager;
# 	@Mock
# 	ConfigurationManager configuration_manager;
# 	@Mock
# 	SimulationManager simulation_manager;
# 	@Mock
# 	AppManager app_manager;
# 	@Mock
# 	ServiceManager service_manager;
# //	@Mock
# //	DataManager data_manager;
# 	@Mock
# 	LogManager log_manager;
# 	@Mock
# 	ClientFactory client_factory;
# 	@Mock
# 	Client client;
# 	@Mock
# 	TestManager test_manager;
# 	@Mock
# 	SecurityConfig security_config;
# 	@Mock
# 	FieldBusManager field_bus_manager;
#
# 	@Captor
# 	ArgumentCaptor<String> argCaptor;
# 	@Captor
# 	ArgumentCaptor<Long> argLongCaptor;
# 	@Captor
# 	ArgumentCaptor<LogLevel> argLogLevelCaptor;
# 	@Captor
# 	ArgumentCaptor<ProcessStatus> argProcessStatusCaptor;
#
#
# 	@Test
# 	public void testWhen_RequestPGQueryRequestSent() throws ParseException{
#
# 		ProcessNewSimulationRequest new_simulation_process = new ProcessNewSimulationRequest();
# 		DataManager data_manager = new DataManagerImpl(client_factory, log_manager);
#
# 		ProcessEvent pe = new ProcessEvent(processManager, client,
# 				new_simulation_process, configuration_manager, simulation_manager, app_manager, log_manager, service_manager, data_manager, test_manager, security_config, field_bus_manager);
#
# 		PowergridModelDataRequest pgDataRequest = new PowergridModelDataRequest();
# 		String queryString = "select ?line_name ?subregion_name ?region_name WHERE {?line rdf:type cim:Line."+
#                               			 "?line cim:IdentifiedObject.name ?line_name."+
#                                          "?line cim:Line.Region ?subregion."+
#                                          "?subregion cim:IdentifiedObject.name ?subregion_name."+
#                                          "?subregion cim:SubGeographicalRegion.Region ?region."+
#                                          "?region cim:IdentifiedObject.name ?region_name"+
#                                         "}";
# 		pgDataRequest.setRequestType(PowergridModelDataRequest.RequestType.QUERY.to"");
# 		pgDataRequest.setQueryString(queryString);
# 		pgDataRequest.setResultFormat(PowergridModelDataRequest.ResultFormat.JSON.to"");
# 		pgDataRequest.setModelId(null);
#
# 		DataResponse message = new DataResponse();
# 		message.setDestination(GridAppsDConstants.topic_requestData+".powergridmodel");
# 		message.setData(pgDataRequest);
#
# 		pe.onMessage(message);
#
# 	}
#
#
# 	@Test
# 	public void testWhen_RequestPGQueryObjectTypesRequestSent() throws ParseException{
#
# 		ProcessNewSimulationRequest new_simulation_process = new ProcessNewSimulationRequest();
# 		DataManager data_manager = new DataManagerImpl(client_factory, log_manager);
#
# 		ProcessEvent pe = new ProcessEvent(processManager, client,
# 				new_simulation_process, configuration_manager, simulation_manager, app_manager, log_manager, service_manager, data_manager, test_manager, security_config, field_bus_manager);
#
# 		PowergridModelDataRequest pgDataRequest = new PowergridModelDataRequest();
#
# 		pgDataRequest.setRequestType(PowergridModelDataRequest.RequestType.QUERY_OBJECT_TYPES.to"");
# 		pgDataRequest.setResultFormat(PowergridModelDataRequest.ResultFormat.JSON.to"");
# 		pgDataRequest.setModelId("ieee13");
#
# 		DataResponse message = new DataResponse();
# 		message.setDestination(GridAppsDConstants.topic_requestData+".powergridmodel");
# 		message.setData(pgDataRequest);
#
# 		pe.onMessage(message);
#
# 	}
#
#
# 	@Test
# 	public void testWhen_RequestPGQueryModelNamesRequestSent() throws ParseException{
#
# 		ProcessNewSimulationRequest new_simulation_process = new ProcessNewSimulationRequest();
# 		DataManager data_manager = new DataManagerImpl(client_factory, log_manager);
#
# 		ProcessEvent pe = new ProcessEvent(processManager, client,
# 				new_simulation_process, configuration_manager, simulation_manager, app_manager, log_manager, service_manager, data_manager, test_manager, security_config, field_bus_manager);
#
# 		PowergridModelDataRequest pgDataRequest = new PowergridModelDataRequest();
#
# 		pgDataRequest.setRequestType(PowergridModelDataRequest.RequestType.QUERY_MODEL_NAMES.to"");
# 		pgDataRequest.setResultFormat(PowergridModelDataRequest.ResultFormat.JSON.to"");
#
# 		DataResponse message = new DataResponse();
# 		message.setDestination(GridAppsDConstants.topic_requestData+".powergridmodel");
# 		message.setData(pgDataRequest);
#
# 		pe.onMessage(message);
#
# 	}
#
#
# }


import unittest
from multiprocessing.connection import Client
from unittest.mock import Mock
from datetime import datetime

from gov_pnnl_goss.gridappsd.api.AppManager import AppManager
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.FieldBusManager import FieldBusManager
from gov_pnnl_goss.gridappsd.api.LogDataManager import LogDataManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.api.ServiceManager import ServiceManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.api.TestManager import TestManager, DataResponse
from gov_pnnl_goss.gridappsd.process.ProcessManagerImpl import ProcessManagerImpl
from gov_pnnl_goss.gridappsd.process.ProcessNewSimulationRequest import ProcessNewSimulationRequest
from gov_pnnl_goss.gridappsd.simulation.FNCSOutputEvent import ClientFactory, SecurityConfig, GridAppsDConstants


# from gov.pnnl.goss.gridappsd.api.AppManager import AppManager
# from gov.pnnl.goss.gridappsd.api.ConfigurationManager import ConfigurationManager
# from gov.pnnl.goss.gridappsd.api.DataManager import DataManager
# from gov.pnnl.goss.gridappsd.api.FieldBusManager import FieldBusManager
# from gov.pnnl.goss.gridappsd.api.LogDataManager import LogDataManager
# from gov.pnnl.goss.gridappsd.api.LogManager import LogManager
# from gov.pnnl.goss.gridappsd.api.RoleManager import RoleManager
# from gov.pnnl.goss.gridappsd.api.ServiceManager import ServiceManager
# from gov.pnnl.goss.gridappsd.api.SimulationManager import SimulationManager
# from gov.pnnl.goss.gridappsd.api.TestManager import TestManager
# from gov.pnnl.goss.gridappsd.data.DataManagerImpl import DataManagerImpl
# from gov.pnnl.goss.gridappsd.dto.LogMessage import LogLevel, ProcessStatus
# from gov.pnnl.goss.gridappsd.dto.PowergridModelDataRequest import PowergridModelDataRequest
# from gov.pnnl.goss.gridappsd.process.ProcessEvent import ProcessEvent
# from gov.pnnl.goss.gridappsd.process.ProcessManagerImpl import ProcessManagerImpl
# from gov.pnnl.goss.gridappsd.process.ProcessNewSimulationRequest import ProcessNewSimulationRequest
# from gov.pnnl.goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants
# from pnnl.goss.core.Client import Client
# from pnnl.goss.core.ClientFactory import ClientFactory
# from pnnl.goss.core.DataResponse import DataResponse
# from pnnl.goss.core.security.SecurityConfig import SecurityConfig


class DataManagerImpl:
	pass


class ProcessEvent:
	pass


class PowergridModelDataRequest:
	pass


class ProcessEventTests(unittest.TestCase):

    #@Mock
    logDataManager = LogDataManager
    processManager = ProcessManagerImpl
    configurationManager = ConfigurationManager
    simulationManager = SimulationManager
    appManager = AppManager
    serviceManager = ServiceManager
    logManager = LogManager
    clientFactory = ClientFactory
    client = Client
    testManager = TestManager
    securityConfig = SecurityConfig
    fieldBusManager = FieldBusManager

    #@Mock
    argCaptor = Mock()
    argLongCaptor = Mock()
    argLogLevelCaptor = Mock()
    argProcessStatusCaptor = Mock()

    def test_when_request_pg_query_request_sent(self):
        newSimulationProcess = ProcessNewSimulationRequest()
        dataManager = DataManagerImpl(self.clientFactory, self.logManager)

        pe = ProcessEvent(self.processManager, self.client,
                          newSimulationProcess, self.configurationManager, self.simulationManager,
						  self.appManager, self.logManager,
                          self.serviceManager, dataManager, self.testManager,
						  self.securityConfig, self.fieldBusManager)

        pgDataRequest = PowergridModelDataRequest()
        query_string = "select ?line_name ?subregion_name ?region_name WHERE {?line rdf:type cim:Line." + \
                       "?line cim:IdentifiedObject.name ?line_name." + \
                       "?line cim:Line.Region ?subregion." + \
                       "?subregion cim:IdentifiedObject.name ?subregion_name." + \
                       "?subregion cim:SubGeographicalRegion.Region ?region." + \
                       "?region cim:IdentifiedObject.name ?region_name" + \
                       "}"
        pgDataRequest.set_request_type(PowergridModelDataRequest.RequestType.QUERY)
        pgDataRequest.set_query_string(query_string)
        pgDataRequest.set_result_format(PowergridModelDataRequest.ResultFormat.JSON)
        pgDataRequest.set_model_id(None)

        message = DataResponse()
        message.set_destination(GridAppsDConstants.topic_requestData + ".powergridmodel")
        message.set_data(pgDataRequest)

        pe.on_message(message)

    def test_when_request_pg_query_object_types_request_sent(self):
        newSimulationProcess = ProcessNewSimulationRequest()
        dataManager = DataManagerImpl(self.clientFactory, self.logManager)

        pe = ProcessEvent(self.processManager, self.client,
                          newSimulationProcess, self.configurationManager, self.simulationManager,
						  self.appManager, self.logManager,
                          self.serviceManager, dataManager,
						  self.testManager, self.securityConfig, self.fieldBusManager)

        pgDataRequest = PowergridModelDataRequest()

        pgDataRequest.set_request_type(PowergridModelDataRequest.RequestType.QUERY_OBJECT_TYPES)
        pgDataRequest.set_result_format(PowergridModelDataRequest.ResultFormat.JSON)
        pgDataRequest.set_model_id("ieee13")

        message = DataResponse()
        message.set_destination(GridAppsDConstants.topic_requestData + ".powergridmodel")
        message.set_data(pgDataRequest)

        pe.on_message(message)

    def test_when_request_pg_query_model_names_request_sent(self):
        newSimulationProcess = ProcessNewSimulationRequest()
        dataManager = DataManagerImpl(self.clientFactory, self.logManager)

        pe = ProcessEvent(self.processManager, self.client,
                          newSimulationProcess, self.configurationManager, self.simulationManager,
						  self.appManager, self.logManager,
                          self.serviceManager, dataManager, self.testManager, self.securityConfig, self.fieldBusManager)

        pgDataRequest = PowergridModelDataRequest()

        pgDataRequest.set_request_type(PowergridModelDataRequest.RequestType.QUERY_MODEL_NAMES)
        pgDataRequest.set_result_format(PowergridModelDataRequest.ResultFormat.JSON)

        message = DataResponse()
        message.set_destination(GridAppsDConstants.topic_requestData + ".powergridmodel")
        message.set_data(pgDataRequest)

        pe.on_message(message)


if __name__ == '__main__':
    unittest.main()
