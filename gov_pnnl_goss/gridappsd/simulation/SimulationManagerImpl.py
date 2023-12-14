import logging
import time

from gov_pnnl_goss.gridappsd.simulation.SimulationProcess import SimulationProcess
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class SimulationManagerImpl:
    def __init__(self, client_factory, server_control, log_manager, service_manager, app_manager, security_config):
        self.client_factory = client_factory
        self.server_control = server_control
        self.logger_manager = log_manager
        self.service_manager = service_manager
        self.app_manager = app_manager
        self.security_config = security_config
        self.client = None
        self.sim_contexts = {}

    def start(self):
        try:
            self.client = self.client_factory.create("STOMP", (self.security_config.get_manager_user(), self.security_config.get_manager_password()))
            self.logger_manager.info("STARTED", None, f"{self.__class__.__name__} Started")
        except Exception as e:
            logging.error(f"Error during initialization: {str(e)}")

    def start_simulation(self, simulation_id, simulation_config, sim_context, simulation_context):
        try:
            self.logger_manager.info("STARTING", simulation_id, f"Starting simulation {simulation_id}")
            self.sim_contexts[sim_context.get_simulation_id()] = sim_context
            sim_proc = SimulationProcess(sim_context, self.service_manager, simulation_config, simulation_id, self.logger_manager, self.app_manager, self.client, self.security_config, simulation_context)
            sim_proc.start()
        except Exception as e:
            logging.error(f"Error during simulation start: {str(e)}")

    def pause_simulation(self, simulation_id):
        # Not implementing yet
        pass

    def resume_simulation(self, simulation_id):
        # Not implementing yet
        pass

    def end_simulation(self, simulation_id):
        try:
            self.client.publish(GridAppsDConstants.topic_COSIM_input, "{\"command\": \"stop\"}")
        except Exception as e:
            logging.error(f"Error during simulation end: {str(e)}")

    def remove_simulation(self, simulation_id):
        self.end_simulation(simulation_id)

    def get_simulation_contexts(self):
        return self.sim_contexts

    def get_simulation_context_for_id(self, simulation_id):
        return self.sim_contexts.get(simulation_id)
