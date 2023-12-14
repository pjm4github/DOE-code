# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import os
import logging
from datetime import datetime

from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
from gov_pnnl_goss.gridappsd.api.ConfigurationHandler import ConfigurationHandler
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.api.PowergridModelDataManager import PowergridModelDataManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.configuration.BaseConfigurationHandler import BaseConfigurationHandler
from gov_pnnl_goss.gridappsd.data.handlers.BlazegraphQueryHandler import BlazegraphQueryHandler
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus


class DSSCoordinateConfigurationHandler(BaseConfigurationHandler, ConfigurationHandler):
    TYPENAME = "DSS Coordinate"
    # ZFRACTION = "z_fraction"
    # IFRACTION = "i_fraction"
    # PFRACTION = "p_fraction"
    # SCHEDULENAME = "schedule_name"
    # LOADSCALINGFACTOR = "load_scaling_factor"
    MODELID = "model_id"
    SIMULATIONID = "simulation_id"
    def __init__(self, log_manager: LogManager, data_manager: DataManager):
        super().__init__(log_manager, data_manager)
        self.log = LogManager(__name__)
        self.client = None
        self.config_manager = ConfigurationManager()
        self.simulation_manager = SimulationManager()
        self.powergrid_model_manager = PowergridModelDataManager()
        self.logger = log_manager
        self.type_name = "DSS Coordinate"

    def start(self):
        if self.config_manager is not None:
            self.config_manager.register_configuration_handler(self.type_name, self)
        else:
            self.log.warn("No Config manager available for {}".format(__class__.__name__))

        if self.powergrid_model_manager is None:
            pass  #TODO send log message and exception

    def generate_config(self, parameters, out, process_id, username):
        self.logger.info(ProcessStatus.RUNNING, process_id, "Generating DSS Coordinate configuration file using parameters: {}".format(parameters))

        simulation_id = parameters.get('simulation_id', None)
        config_file = None
        if simulation_id:
            simulation_context = self.simulation_manager.get_simulation_context_for_id(simulation_id)
            if simulation_context:
                config_file = os.path.join(simulation_context.get_simulation_dir(), "DSS_base_configuration_filename")
                if os.path.exists(config_file):
                    self.print_file_to_output(config_file, out)
                    self.logger.info(ProcessStatus.RUNNING, process_id, "Dictionary DSS coordinates file for simulation {} already exists.".format(simulation_id))
                    return
            else:
                self.logger.warn(ProcessStatus.RUNNING, process_id, "No simulation context found for simulation_id: {}".format(simulation_id))

        model_id = parameters.get('model_id', None)
        if not model_id or len(model_id.strip()) == 0:
            self.logger.error(ProcessStatus.ERROR, process_id, "No model_id parameter provided")
            raise Exception("Missing parameter {}".format('model_id'))

        bg_host = self.config_manager.get_configuration_property("BLAZEGRAPH_HOST_PATH")
        if not bg_host or len(bg_host.strip()) == 0:
            bg_host = BlazegraphQueryHandler.DEFAULT_ENDPOINT
        
        query_handler = BlazegraphQueryHandler(bg_host, self.logger, process_id, username)
        query_handler.add_feeder_selection(model_id)

        cim_importer = CIMImporter()
        # If the simulation info is available also write to file
        if config_file:
            cim_importer.generate_dss_coordinates(query_handler, open(config_file, 'w'))
        else:
            cim_importer.generate_dss_coordinates(query_handler, out)

        if config_file:
            # config was written to file, so return that
            self.print_file_to_output(config_file, out)
        self.logger.info(ProcessStatus.RUNNING, process_id, "Finished generating DSS Coordinate configuration file.")
