# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import logging
from datetime import datetime

from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
from gov_pnnl_goss.gridappsd.api.ConfigurationHandler import ConfigurationHandler
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.PowergridModelDataManager import PowergridModelDataManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.configuration.BaseConfigurationHandler import BaseConfigurationHandler
from gov_pnnl_goss.gridappsd.configuration.CIMDictionaryConfigurationHandler import PrintWriter, FileWriter
from gov_pnnl_goss.gridappsd.configuration.GLDAllConfigurationHandler import GLDAllConfigurationHandler
from gov_pnnl_goss.gridappsd.data.handlers.BlazegraphQueryHandler import BlazegraphQueryHandler
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class CIMSymbolsConfigurationHandler(BaseConfigurationHandler, ConfigurationHandler):
    TYPENAME = "GridLAB-D Symbols"
    MODELID = "model_id"
    SIMULATIONID = "simulation_id"

    def __init__(self, log_manager=None, data_manager=None):
        super().__init__(log_manager, data_manager)
        self.config_manager = ConfigurationManager()
        self.simulation_manager = SimulationManager()
        self.powergrid_model_manager = PowergridModelDataManager()
        self.logger = log_manager
        self.log = LogManager(CIMSymbolsConfigurationHandler.__name__)
        self.type_name = "GridLAB-D Symbols"
        self.model_id = "model_id"
        self.simulation_id = "simulation_id"

    def start(self):
        if self.config_manager is not None:
            self.config_manager.register_configuration_handler(self.TYPENAME, self)
        else:
            self.log.warning("No Config manager available for " + str(self.__class__))

        if self.powergrid_model_manager is None:
            # TODO send log message and exception
            pass

    def generate_config(self, parameters, out, process_id, username):
        self.log.info('Running', process_id, f"Generating Symbols GridLAB-D configuration file using parameters: {parameters}")

        simulation_id = parameters.get(self.simulation_id, None)
        config_file = None

        if simulation_id is not None:
            simulation_context = self.simulation_manager.get_simulation_context_for_id(simulation_id)

            if simulation_context:
                config_file = simulation_context.get_simulation_dir() + '/' + GLDAllConfigurationHandler.DICTIONARY_FILENAME
                # If the config file already has been created for this simulation then return it
                if config_file:
                    self.print_file_to_output(config_file, out)
                    self.log.info('Running', process_id, f'Dictionary GridLAB-D symbols file for simulation {simulation_id} already exists.')
                    return
            else:
                self.log.warning('Running', process_id, f'No simulation context found for simulation_id: {simulation_id}')

        model_id = parameters.get(self.model_id, None)

        if not model_id or not model_id.strip():
            self.log.error('Running', process_id, f'No {self.model_id} parameter provided')
            raise Exception(f'Missing parameter {self.model_id}')

        bg_host = self.config_manager.get_configuration_property(GridAppsDConstants.BLAZEGRAPH_HOST_PATH)

        if bg_host is None or not bg_host.strip():
            bg_host = BlazegraphQueryHandler.DEFAULT_ENDPOINT
        # TODO write a query handler that uses the built in powergrid model data manager that talks to blazegraph internally
        query_handler = BlazegraphQueryHandler(bg_host, self.log, process_id, username)
        query_handler.add_feeder_selection(model_id)

        cim_importer = CIMImporter()

        if config_file is not None:
            cim_importer.generate_json_symbol_file(query_handler, PrintWriter(FileWriter(config_file)))
        else:
            cim_importer.generate_json_symbol_file(query_handler, out)

        if config_file is not None:
            self.print_file_to_output(config_file, out)

        self.log.info('Running', process_id, 'Finished generating Symbols GridLAB-D configuration file.')
