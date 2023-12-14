import re
import subprocess
import time
import json
from threading import Thread
import logging

from gov_pnnl_goss.gridappsd.api import AppManager
from gov_pnnl_goss.gridappsd.api import LogManager
from gov_pnnl_goss.gridappsd.api import ServiceManager
from gov_pnnl_goss.gridappsd.configuration import GLDAllConfigurationHandler
from gov_pnnl_goss.gridappsd.configuration import OchreAllConfigurationHandler
from gov_pnnl_goss.gridappsd.dto import FncsBridgeResponse
from gov_pnnl_goss.gridappsd.dto import LogMessage
from gov_pnnl_goss.gridappsd.dto import ServiceInfo
from gov_pnnl_goss.gridappsd.dto.LogMessage import LogLevel
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.dto import RequestSimulation
from gov_pnnl_goss.gridappsd.dto import SimulationConfig
from gov_pnnl_goss.gridappsd.dto import SimulationContext
from gov_pnnl_goss.gridappsd.simulation import SimulationManagerImpl
from gov_pnnl_goss.gridappsd.utils import GridAppsDConstants
from gov_pnnl_goss.gridappsd.utils import RunCommandLine


class SimulationProcess(Thread):
    def __init__(self, simContext, serviceManager, simulationConfig, simulationId, logManager, appManager, client, securityConfig, simulationContext):
        super().__init__()
        self.sim_context = simContext
        self.service_manager = serviceManager
        self.simulation_config = simulationConfig
        self.simulation_id = simulationId
        self.logger_manager = logManager
        self.app_manager = appManager
        self.client = client
        self.security_config = securityConfig
        self.simulation_context = simulationContext
        self.gridlabd_constant = "GridLAB-D"
        self.running = True

    def is_running(self):
        return self.running

    def set_running(self, running):
        self.running = running

    def run(self):
        simulator_process = None
        initialized_tracker = {"is_inited": False}
        simulation_tracker = {"is_finished": False}

        try:
            simulation_file = self.sim_context.get_startup_file()

            service_dir = self.service_manager.get_service_config_directory()
            try:
                subprocess.run(["cp", service_dir + "/etc/appliance_schedules.glm",
                                simulation_file.parent / GLDAllConfigurationHandler.SCHEDULES_FILENAME])
            except Exception as e:
                self.logger_manager.warn(ProcessStatus.RUNNING, self.simulation_id, "Could not copy schedules file to working directory")

            process_builder = subprocess.Popen if hasattr(subprocess, "Popen") else subprocess.run

            if self.simulation_config.get_simulator() == OchreAllConfigurationHandler.TYPENAME:
                # Start gridlabd
                gld_startup_file = self.sim_context.simulation_dir / "model_startup.glm"
                gld_simulator_path = self.service_manager.get_service(self.gridlabd_constant).get_execution_path()

                commands = [gld_simulator_path, gld_startup_file]
                process_builder(commands, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=simulation_file.parent)

                self.logger_manager.info(ProcessStatus.RUNNING, self.simulation_id,
                                     f"Starting gridlabd simulator with command {' '.join(commands)}")

                # Start ochre
                commands = [self.sim_context.get_simulator_path()]

                service_info = self.service_manager.get_service(self.simulation_config.get_simulator())
                static_args_list = service_info.get_static_args()

                for static_arg in static_args_list:
                    if static_arg is not None:
                        if self.simulation_context is not None:
                            if "(" in static_arg:
                                replace_args = re.findall(r'\((.*?)\)', static_arg)
                                for args in replace_args:
                                    static_arg = static_arg.replace(f"({args})", str(self.simulation_context[args]))
                        commands.append(static_arg)

                process_builder(commands, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

                self.logger_manager.info(ProcessStatus.RUNNING, self.simulation_id,
                                     f"Command for ochre ready {' '.join(commands)}")

            elif self.simulation_config.get_simulator() == self.gridlabd_constant:
                commands = [self.sim_context.get_simulator_path(), simulation_file]

                process_builder(commands, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=simulation_file.parent)
            else:
                self.logger_manager.warn(ProcessStatus.RUNNING, self.simulation_id, "No known simulator: " + self.simulation_config.get_simulator())

            self.logger_manager.info(ProcessStatus.RUNNING, self.simulation_id, f"Starting simulator with command {' '.join(commands)}")

            # Watch the process
            self.watch(simulator_process, "Simulator-" + self.simulation_id)

            self.logger_manager.info(ProcessStatus.RUNNING, self.simulation_id, f"Started simulator with command {' '.join(commands)}")

            # TODO: check if GridLAB-D is started correctly and send publish simulation status accordingly
            self.logger_manager.info(ProcessStatus.RUNNING, self.simulation_id, f"{self.simulation_config.get_simulator()} simulator started")

            # Subscribe to fncs-goss-bridge output topic
            goss_fncs_response_event = self.GossFncsResponseEvent(self.logger_manager, initialized_tracker, simulation_tracker, self.simulation_id)
            self.client.subscribe("/topic/" + GridAppsDConstants.topic_COSIM_output, goss_fncs_response_event)

            self.logger.info(ProcessStatus.RUNNING, self.simulation_id, "Checking if co-simulation is initialized, currently " + str(initialized_tracker["is_inited"]))

            init_attempts = 0
            while not initialized_tracker["is_inited"] and init_attempts < SimulationManagerImpl.MAX_INIT_ATTEMPTS:
                # Send 'isInitialized' call to fncs-goss-bridge to check initialization until it is initialized.
                # TODO add limiting how long it checks for initialized, or cancel if the fncs process exits
                # This call would return true/false for initialization and simulation output of time step 0.
                self.client.publish(GridAppsDConstants.topic_COSIM_input, "{\"command\": \"isInitialized\"}")
                init_attempts += 1
                time.sleep(1)

            if init_attempts < SimulationManagerImpl.MAX_INIT_ATTEMPTS:
                self.logger.info(ProcessStatus.RUNNING, self.simulation_id, "Co-Simulation Bridge Initialized")

                # Send the start simulation command to the co-simulation bridge
                self.start_simulation(goss_fncs_response_event, self.simulation_config, self.simulation_id)
                while not simulation_tracker["is_finished"]:
                    self.logger.debug(ProcessStatus.RUNNING, self.simulation_id, "Checking if co-simulation federation is finished, currently " + str(simulation_tracker["is_finished"]))
                    time.sleep(1)
            else:
                self.logger.error(ProcessStatus.ERROR, self.simulation_id, "Co-simulation Bridge Initialization Failed")

            # Call to stop the simulation
            self.client.publish(GridAppsDConstants.topic_COSIM_input, "{\"command\":  \"stop\"}")
            self.logger.info(ProcessStatus.COMPLETE, self.simulation_id, f"Simulation {self.simulation_id} complete")
        except Exception as e:
            self.logger.error("Error during simulation", e)
            try:
                self.logger.error(ProcessStatus.ERROR, self.simulation_id, "Simulation error: " + str(e))
            except Exception as e1:
                self.logger.error("Error while reporting error status", e)

        finally:
            # Shut down applications and services connected with the simulation
            service_instance_ids = self.sim_context.get_service_instance_ids()
            simulator_process.terminate()
            try:
                simulator_process.wait(0.01)
            except KeyboardInterrupt:
                simulator_process.kill()
            except Exception:
                simulator_process.kill()
            for service_instance_id in service_instance_ids:
                self.service_manager.stop_service_instance(service_instance_id)

            app_instance_ids = self.sim_context.get_app_instance_ids()
            for app_instance_id in app_instance_ids:
                self.app_manager.stop_app_instance(app_instance_id)

    def start_simulation(self, goss_event, simulation_config, simulation_id):
        # Send the start simulation command to the fncsgossbridge so that it runs it'status time loop to move the fncs simulation forward
        self.logger.debug(ProcessStatus.RUNNING, simulation_id, "Sending start simulation to bridge.")
        message = "{\"command\": \"StartSimulation\"}"
        self.client.publish(GridAppsDConstants.topic_COSIM_input, message)

    def watch(self, process, process_name):
        def read_input_stream():
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                line = line.decode("utf-8").strip()
                if line:
                    if "DEBUG" in line:
                        self.logger.debug(ProcessStatus.RUNNING, process_name, line)
                    elif "ERROR" in line:
                        self.logger.error(ProcessStatus.ERROR, process_name, line)
                    elif "FATAL" in line and "INFO" not in line:
                        self.logger.fatal(ProcessStatus.ERROR, process_name, line)
                    elif "WARN" in line:
                        self.logger.warn(ProcessStatus.RUNNING, process_name, line)
                    else:
                        self.logger.debug(ProcessStatus.RUNNING, process_name, line)

        Thread(target=read_input_stream, daemon=True).start()

    class GossFncsResponseEvent:
        def __init__(self, log_manager, initialized_tracker, simulation_tracker, simulation_id):
            self.logger = log_manager
            self.initialized_tracker = initialized_tracker
            self.simulation_tracker = simulation_tracker
            self.simulation_id = simulation_id

        def on_message(self, response):
            try:
                data_response = json.loads(response)

                self.logger.debug(ProcessStatus.RUNNING, self.simulation_id, "Co-simulation Bridge response:" + str(data_response))

                if "command" in data_response:
                    if data_response["command"] == "isInitialized":
                        self.logger.info("Bridge Initialized response: " + str(data_response))
                        if data_response["response"] == "True":
                            self.initialized_tracker["is_inited"] = True
                    elif data_response["command"] == "simulationFinished":
                        self.simulation_tracker["is_finished"] = True
            except Exception as e:
                self.logger.error("Error while processing response", e)
