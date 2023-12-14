# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import logging
import os
import json

from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
from gov_pnnl_goss.cimhub.OperationalLimits import OperationalLimits
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.api.PowergridModelDataManager import PowergridModelDataManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.configuration.BaseConfigurationHandler import BaseConfigurationHandler
from gov_pnnl_goss.gridappsd.data.handlers.BlazegraphQueryHandler import BlazegraphQueryHandler
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus


class GldLimitsConfigurationHandler(BaseConfigurationHandler):
    TYPENAME = "GridLAB-D Limits"
    RANDOMIZEFRACTIONS = "randomize_zipload_fractions"
    MODELID = "model_id"
    SIMULATIONID = "simulation_id"
    cimhub_PREFIX = "model"
    LIMITS_FILENAME = cimhub_PREFIX + "_limits.json"

    def __init__(self, log_manager, data_manager):
        super().__init__(log_manager, data_manager)
        self.logger = log_manager
        self.data_manager = data_manager
        self.config_manager = ConfigurationManager()
        self.power_grid_model_manager = PowergridModelDataManager()
        self.simulation_manager = SimulationManager()
        self.log = LogManager(GldLimitsConfigurationHandler.__name__)

    def start(self):
        if self.config_manager:
            self.config_manager.register_configuration_handler(self.TYPENAME, self)
        else:
            self.log.warning("No Config manager avilable for " + GldLimitsConfigurationHandler.__name__)

    def on_start(self):
        self._create_message('GLD Limits Configuration Handler started')

    def _create_message(self, message):
        message = f"GLD Configuration: {message}"
        self.logger.info(message)

    def generate_config(self, parameters, process_id, output_path, username):
        simulation_id = parameters.get('simulation_id', None)
        config_file = None
        if simulation_id:
            simulation_context = self.simulation_manager.get_simulation_context_for_id(simulation_id)
            if simulation_context:
                config_file = os.path.join(simulation_context.get_simulation_dir(), 'model_limits.json')
                # limits_filename = functions"{simulation_context.get_simulation_dir()}/model_limits.json"
                if os.path.exists(config_file):
                    with open(config_file, 'r') as file:
                        config_data = json.load(file)
                        self._create_message(f"Limits file for simulation {simulation_id} already exists.")
                    return config_data
                else:
                    self.log.warning("No simulation context found for simulation_id: %status", simulation_id)
        self.log.info("Generating limits file using parameters: %status", parameters)
        model_id = parameters.get('model_id', None)
        if not model_id:
            self.logger.error(f"{ProcessStatus.ERROR}, No  {self.MODELID} parameter provided")

            raise Exception("Missing parameter: model_id")

        bg_host = self.config_manager.get_configuration_property('BLAZEGRAPH_HOST_PATH')
        if not bg_host:
            bg_host =  BlazegraphQueryHandler.DEFAULT_ENDPOINT  # Set the default endpoint here

        query_handler = BlazegraphQueryHandler(bg_host, self.logManager, process_id, username)
        query_handler.add_feeder_selection(model_id)

        cim_importer = CIMImporter()
        operational_limits = OperationalLimits()
        operational_limits.build_limit_maps(cim_importer, query_handler)

        limits_data = {
            'limits': {
                'voltages': operational_limits.voltage_map_to_json(output_path),
                'currents': operational_limits.current_map_to_json(output_path)
            }
        }
        config_data = json.dumps(limits_data, indent=2)

        if simulation_id:
            with open(config_file, 'w') as file:
                file.write(config_data)

        self.log.info("Finished generating GridLAB-D limits file.")

        return config_data
