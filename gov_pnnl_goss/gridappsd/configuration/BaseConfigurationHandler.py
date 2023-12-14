from abc import ABC, abstractmethod
from gov_pnnl_goss.gridappsd.api import ConfigurationHandler, DataManager, LogManager


class BaseConfigurationHandler(ConfigurationHandler, ABC):
    MODEL_STATE = "model_state"

    def __init__(self, log_manager: LogManager, data_manager: DataManager):
        super().__init__(log_manager, data_manager)

    @abstractmethod
    def start(self):
        pass

    def print_file_to_output(self, config_file, out):
        with open(config_file, 'r') as reader:
            for line in reader:
                out.write(line)
        out.flush()
