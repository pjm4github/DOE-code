# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import logging
from collections import defaultdict
from io import IOBase

from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class ConfigurationManagerImpl(ConfigurationManager):
    
    CONFIG_PID = "pnnl.goss.gridappsd"
    
    def __init__(self, log_manager=None, data_manager=None):
        self.client = None
        self.client_factory = None
        self.logger = log_manager
        self.log = LogManager(ConfigurationManagerImpl.__name__)
        self.data_manager = data_manager
        self.configuration_properties = defaultdict(str)
        self.config_handlers = {}
        
    def start(self):
        pass  # TODO send log "Starting configuration manager"
        
    def get_simulation_file(self, simulation_id, power_system_config):
        """
        /**
        * This method returns simulation file path with name.
        * Return GridLAB-D file path with name for RC1.
        * @param simulationId
        * @param configRequest
        * @return
        */
        :param simulation_id:
        :param power_system_config:
        :return:
        """
        self.log.warning(ProcessStatus.RUNNING, simulation_id, "ConfigurationManager.getSimulationFile will be deprecated")
        # TODO call data_manager'status method to get power grid model data and create simulation file
        resp = self.data_manager.processDataRequest(power_system_config, None, simulation_id, self.get_configuration_property(GridAppsDConstants.GRIDAPPSD_TEMP_PATH), "")
        
        if isinstance(resp, DataResponse) and resp.get_data() and isinstance(resp.get_data(), IOBase):
            # Update simulation status after every step, for example:
            # self.status_reporter.reportStatus(GridAppsDConstants.topic_simulationLog + simulationId,
            #                               "Simulation files created");
            return resp.get_data()
        else:
            return None
        
    def updated(self, config):
        self.configuration_properties = config
        
    def get_configuration_property(self, key):
        if self.configuration_properties:
            value = self.configuration_properties.get(key)
            if value:
                return str(value)
        return None
        
    def register_configuration_handler(self, type, handler):
        self.log.info(ProcessStatus.RUNNING, None, "Registring config " + type + " " + self.__class__.__name__)
        self.config_handlers[type] = handler
        
    def generate_configuration(self, type, parameters, out, process_id, username):
        if type in self.config_handlers and self.config_handlers[type] is not None:
            self.config_handlers[type].generate_config(parameters, out, process_id, username)
        else:
            self.log.error(ProcessStatus.ERROR, process_id, "No configuration handler registered for '" + type + "'")
            raise Exception("No configuration handler registered for '" + type + "'")
