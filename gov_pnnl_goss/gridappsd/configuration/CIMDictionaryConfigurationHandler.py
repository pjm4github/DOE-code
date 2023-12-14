# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json
import logging
import os

from gov_pnnl_goss.SpecialClasses import Gson
from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
from gov_pnnl_goss.cimhub.dto.ModelState import ModelState
from gov_pnnl_goss.gridappsd.api.ConfigurationHandler import ConfigurationHandler
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.api.PowergridModelDataManager import PowergridModelDataManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.configuration.BaseConfigurationHandler import BaseConfigurationHandler
from gov_pnnl_goss.gridappsd.configuration.GLDAllConfigurationHandler import GLDAllConfigurationHandler
from gov_pnnl_goss.gridappsd.data.handlers.BlazegraphQueryHandler import BlazegraphQueryHandler
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


# from .GLDAllConfigurationHandler import GLDAllConfigurationHandler
# from .base_configuration_handler import BaseConfigurationHandler
# from .configuration_handler import ConfigurationHandler
# from .configuration_manager import ConfigurationManager
# from .simulation_manager import SimulationManager
# from .powergrid_model_data_manager import PowergridModelDataManager
# from .log_manager import LogManager
# from ..dto.LogMessage import ProcessStatus
# from ...cimhub.dto.ModelState import ModelState


class PrintWriter:
    pass


class FileWriter:
    pass


class CIMDictionaryConfigurationHandler(BaseConfigurationHandler, ConfigurationHandler):
    TYPENAME = "CIM Dictionary"
    MODELID = "model_id"
    SIMULATIONID = "simulation_id"
    USEHOUSES = "use_houses"
    MODELSTATE = "model_state"  # TODO this is made up - need to check this

    def __init__(self, log_manager: LogManager, data_manager: DataManager):
        super().__init__(log_manager, data_manager)
        self.log = LogManager(CIMDictionaryConfigurationHandler.__class__.__name__)
        self.client = None
        self.config_manager = ConfigurationManager()
        self.simulation_manager = SimulationManager()
        self.powergrid_model_manager = PowergridModelDataManager()

    def start(self):
        if self.config_manager is not None:
            self.config_manager.register_configuration_handler(self.TYPENAME, self)
        else:
            self.log.warning(f'No Config manager available for {self.__class__.__name__}')

        if self.powergrid_model_manager is None:
            # TODO send log message and exception
            pass

    def generate_config(self, parameters, out, process_id, username):
        self.log.info(ProcessStatus.RUNNING, process_id, f'Generating Dictionary GridLAB-D configuration file using parameters: {parameters}')
        simulation_id = parameters.get(self.SIMULATIONID, None)
        use_houses = False
        if self.USEHOUSES in parameters:
            use_houses = parameters.get(self.USEHOUSES, False)

        config_file = None
        if simulation_id:
            simulation_context = self.simulation_manager.get_simulation_context_for_id(simulation_id)
            if simulation_context:
                config_file = os.path.join(simulation_context.get_simulation_dir(), GLDAllConfigurationHandler.DICTIONARY_FILENAME)
                # If the config file already has been created for this simulation then return it
                if config_file:
                    self.print_file_to_output(config_file, out)
                    self.log.info(ProcessStatus.RUNNING, process_id, f'Generating Dictionary GridLAB-D configuration file using parameters: {parameters}')
                    return
            else:
                self.log.warning(ProcessStatus.RUNNING, process_id, f'No simulation context found for simulation_id: {simulation_id}')

        model_state = ModelState()
        model_state_str = parameters.get(self.MODELSTATE, None)
        if model_state_str is None or not model_state_str.strip():
            self.log.warning(ProcessStatus.RUNNING, process_id, f'No {self.MODELSTATE} parameter provided')
        else:
            model_state = json.loads(model_state_str)

        model_id = parameters.get(self.MODELID, None)
        if model_id is None or not model_id.strip():
            self.log.error(ProcessStatus.ERROR, process_id, f'No {self.MODELID} parameter provided')
            raise Exception(f'Missing parameter {self.MODELID}')

        bg_host = self.config_manager.get_configuration_property(GridAppsDConstants.BLAZEGRAPH_HOST_PATH)
        if bg_host is None or not bg_host.strip():
            bg_host = BlazegraphQueryHandler.DEFAULT_ENDPOINT

        query_handler = BlazegraphQueryHandler(bg_host, self.logger, process_id, username)
        query_handler.add_feeder_selection(model_id)

        cim_importer = CIMImporter()
        if config_file:
            cim_importer.generate_dictionary_file(query_handler, PrintWriter(FileWriter(config_file)),use_houses, model_state)
        else:
            cim_importer.generate_dictionary_file(query_handler, out, use_houses, model_state)

        if config_file:
            self.print_file_to_output(config_file, out)
        
        self.log.info(ProcessStatus.RUNNING, process_id, 'Finished generating Dictionary GridLAB-D configuration file.')
