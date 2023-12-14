from abc import ABC, abstractmethod
from typing import Dict
from gov_pnnl_goss.gridappsd.api.ServiceManager import SimulationContext
from gov_pnnl_goss.gridappsd.dto.SimulationConfig import SimulationConfig


class SimulationManager(ABC):
    """
    This represents Internal Function 405 Simulation Control Manager.
    This is the management function that controls the running/execution of the Distribution Simulator (401).
    @author shar064
    """

    @abstractmethod
    def start_simulation(self, simulation_id, simulation_config: SimulationConfig,
                         sim_context: SimulationContext, simulation_context: Dict[str, object]):
        # This method is called by Process Manager to start a simulation
        # @param simulation_id
        # @param simulationFile
        # @param simulationConfig	Map<String, Object> simulation_context
        pass

    @abstractmethod
    def get_simulation_context_for_id(self, simulation_id):
        pass

    @abstractmethod
    def end_simulation(self, simulation_id):
        pass

    @abstractmethod
    def pause_simulation(self, simulation_id):
        pass

    @abstractmethod
    def resume_simulation(self, simulation_id):
        pass
