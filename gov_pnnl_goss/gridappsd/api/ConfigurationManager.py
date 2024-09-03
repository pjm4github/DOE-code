from abc import ABC, abstractmethod
from typing import Dict
from io import StringIO
from ConfigurationHandler import ConfigurationHandler


class ConfigurationManager(ABC):
    """
    This class implements subset of functionalities for Internal Functions
    405 Simulation Manager and 406 Power System Model Manager.
    ConfigurationManager is responsible for:
    - subscribing to configuration topics and
    - converting configuration message into simulation configuration files
      and power grid model files.
    @author shar064
    """

    @abstractmethod
    def get_simulation_file(self, simulation_id: str, power_system_config: Dict) -> str:
        """
        #  This method returns simulation file path with name.
        #  Return GridLAB-D file path with name for RC1.
        :param simulation_id:
        :param power_system_config:
        :return:
        """
        pass

    @abstractmethod
    def get_configuration_property(self, key: str) -> str:
        # 	String getConfigurationProperty(String key);
        pass

    @abstractmethod
    def register_configuration_handler(self, type: str, handler: 'ConfigurationHandler'):
        # void registerConfigurationHandler(String global_property_types, ConfigurationHandler handler);
        pass

    @abstractmethod
    def generate_configuration(self, type: str, parameters: Dict, out: StringIO, process_id: str, username: str):
        # void generateConfiguration(String global_property_types, Properties parameters, PrintWriter out,
        # String processId, String username) throws Exception;
        pass
