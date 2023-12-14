# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
# from base_configuration_handler import BaseConfigurationHandler
# from configuration_handler import ConfigurationHandler
# from configuration_manager import ConfigurationManager
# from logger import Logger
# from properties import Properties
# from process_status import ProcessStatus
# from simulation_manager import SimulationManager
# from powergrid_model_data_manager import PowergridModelDataManager
# from log_manager import LogManager
# from simulation_context import SimulationContext
# from print_writer import PrintWriter
# from query_handler import QueryHandler
# from blazegraph_query_handler import BlazegraphQueryHandler
# from cim_importer import CIMImporter
# from file_writer import FileWriter
# from gridapps_d_constants import GridAppsDConstants
# from client import Client
import os
from multiprocessing.connection import Client

from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
from gov_pnnl_goss.gridappsd.api.ConfigurationHandler import ConfigurationHandler
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.api.PowergridModelDataManager import PowergridModelDataManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.configuration.BaseConfigurationHandler import BaseConfigurationHandler

import logging

from gov_pnnl_goss.gridappsd.configuration.CIMDictionaryConfigurationHandler import FileWriter, PrintWriter
from gov_pnnl_goss.gridappsd.configuration.GLDAllConfigurationHandler import GLDAllConfigurationHandler
from gov_pnnl_goss.gridappsd.data.handlers.BlazegraphQueryHandler import BlazegraphQueryHandler
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class CIMFeederIndexConfigurationHandler(BaseConfigurationHandler, ConfigurationHandler):
    
    def __init__(self, log_manager: LogManager, data_manager: DataManager):
        super().__init__(log_manager, data_manager)
        self.log = LogManager(CIMFeederIndexConfigurationHandler.__name__)
        self.client = None

        self.config_manager = ConfigurationManager()

        self.simulation_manager = SimulationManager()

        self.powergrid_model_manager = PowergridModelDataManager()

        self.logger = log_manager

        self.typename = "CIM Feeder Index"
        self.modelid = "model_id"
        self.simulationid = "simulation_id"

    def start(self):
        if self.config_manager is not None:
            self.config_manager.register_configuration_handler(self.typename, self)

        else:
            self.log.warn("No Config manager avilable for " + self.getClass())

        if self.powergrid_model_manager is None:
            pass  # TODO send log message and exception

    def generate_config(self, parameters, out, process_id, username):
        self.log.info(ProcessStatus.RUNNING, process_id, "Generating Feeder Index GridLAB-D configuration file using parameters: " + str(parameters))

        simulationid = GridAppsDConstants.getStringProperty(parameters, self.simulationid, None)
        config_file = None

        if simulationid is not None:
            simulation_context = self.simulation_manager.get_simulation_context_for_id(simulationid)
            if simulation_context is not None:
                config_file = FileWriter(simulation_context.get_simulation_dir() + os.sep() + GLDAllConfigurationHandler.DICTIONARY_FILENAME)
                if config_file:
                    self.print_file_to_output(config_file, out)
                    self.log.info(ProcessStatus.RUNNING, process_id, "Dictionary GridLAB-D feeder file for simulation " + simulationid + " already exists.")
                    return
                else:
                    self.log.warn(ProcessStatus.RUNNING, process_id, "No simulation context found for simulation_id: " + simulationid)

        bg_host = self.config_manager.get_configuration_property(GridAppsDConstants.BLAZEGRAPH_HOST_PATH)
        if bg_host is None or len(bg_host.strip()) == 0:
            bg_host = BlazegraphQueryHandler.DEFAULT_ENDPOINT
        query_handler = BlazegraphQueryHandler(bg_host, self.log, process_id, username)
        
        cim_importer = CIMImporter()
        if config_file is not None:
            cim_importer.generate_feeder_index_file(query_handler, PrintWriter(FileWriter(config_file)))
        else:
            cim_importer.generate_feeder_index_file(query_handler, out)

        if config_file is not None:
            self.print_file_to_output(config_file, out)
        self.log.info(ProcessStatus.RUNNING, process_id, "Finished generating Feeder Index GridLAB-D configuration file.")
