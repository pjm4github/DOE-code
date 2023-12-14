import os
import json
import openpyxl

from gov_pnnl_goss.gridappsd.api import AppManager
# from gov_pnnl_goss.gridappsd.api import ConfigurationManager
from gov_pnnl_goss.gridappsd.api import DataManager
from gov_pnnl_goss.gridappsd.api import LogManager
from gov_pnnl_goss.gridappsd.api import ServiceManager
# from gov_pnnl_goss.gridappsd.api import SimulationManager
# from gov_pnnl_goss.gridappsd.api import TestManager
from gov_pnnl_goss.gridappsd.configuration.DSSAllConfigurationHandler import DSSAllConfigurationHandler
from gov_pnnl_goss.gridappsd.configuration.GLDAllConfigurationHandler import GLDAllConfigurationHandler
from gov_pnnl_goss.gridappsd.configuration.OchreAllConfigurationHandler import OchreAllConfigurationHandler
# from gov_pnnl_goss.gridappsd.dto import AppInfo
# from gov_pnnl_goss.gridappsd.dto import ApplicationObject
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
# from gov_pnnl_goss.gridappsd.dto import ModelCreationConfig
from gov_pnnl_goss.gridappsd.dto import RequestSimulation
# from gov_pnnl_goss.gridappsd.dto import ServiceConfig
# from gov_pnnl_goss.gridappsd.dto import ServiceInfo
from gov_pnnl_goss.gridappsd.dto.SimulationConfig import SimulationConfig
from gov_pnnl_goss.gridappsd.dto.SimulationContext import SimulationContext
# from gov_pnnl_goss.gridappsd.dto import SimulationOutput
# from gov_pnnl_goss.gridappsd.dto import SimulationOutputObject
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class ProcessNewSimulationRequest:
    def __init__(self, log_manager, security_config):
        self.logger_manager = log_manager
        self.security_config = security_config

    def process(self, configuration_manager, simulation_manager, simulation_id,
                event, sim_request, app_manager, service_manager, test_manager, data_manager, username):
        self.process(
            configuration_manager, simulation_manager, simulation_id, sim_request,
            SimulationConfig.DEFAULT_SIMULATION_BROKER_PORT, app_manager,
            service_manager, test_manager, data_manager, username)

    def process(self, configuration_manager, simulation_manager, simulation_id,
                sim_request, simulation_port, app_manager, service_manager, test_manager, data_manager, username):
        try:
            sim_request.simulation_config['simulation_broker_port'] = simulation_port
            self.logger.info(f"Parsed config {sim_request}")

            if sim_request is None or sim_request.get('power_system_config') is None or \
                    sim_request.get('simulation_config') is None:
                self.logger.info("No simulation file returned for request {sim_request}")
                raise Exception("Invalid configuration received")

            # Make request to configuration manager to get power grid model
            # file locations and names
            self.logger.info(f"Creating simulation and power grid model files for simulation Id {simulation_id}")

            simulation_config_dir = configuration_manager.get_configuration_property(
                GridAppsDConstants.GRIDAPPSD_TEMP_PATH)
            if not simulation_config_dir or not simulation_config_dir.strip():
                self.logger.error("No simulation file returned for request {sim_request}")
                raise Exception("No simulation file returned for request {sim_request}")

            if not simulation_config_dir.endswith(os.path.sep):
                simulation_config_dir += os.path.sep
            simulation_config_dir = os.path.join(simulation_config_dir, simulation_id, os.path.sep)

            if not os.path.exists(simulation_config_dir):
                os.makedirs(simulation_config_dir)

            simulation_context = {
                "request": sim_request,
                "simulation_id": simulation_id,
                "simulationHost": "127.0.0.1",
                "simulationPort": simulation_port,
                "simulationDir": simulation_config_dir
            }

            sim_context = SimulationContext()
            sim_context.request = sim_request
            sim_context.simulationId = simulation_id
            sim_context.simulationPort = simulation_port
            sim_context.simulationDir = simulation_config_dir

            if sim_request['simulation_config']['simulator'] == "GridLAB-D":
                sim_context.startupFile = os.path.join(simulation_config_dir, "model_startup.glm")
            elif sim_request['simulation_config']['simulator'] == "OCHRE":
                sim_context.startupFile = os.path.join(simulation_config_dir, "ochre_helics_config.json")

            sim_context.simulationUser = username
            try:
                sim_context.simulatorPath = service_manager.get_service(
                    sim_request['simulation_config']['simulator'])['execution_path']
            except KeyError:
                if not service_manager.get_service(sim_request['simulation_config']['simulator']):
                    self.logger.error(
                        f"Cannot find service with voltage_id = {sim_request['simulation_config']['simulator']}")
                elif not service_manager.get_service(
                        sim_request['simulation_config']['simulator'])['execution_path']:
                    self.logger.error(
                        f"Cannot find execution path for service = {sim_request['simulation_config']['simulator']}")

            gld_interface = None
            gld_service = service_manager.get_service("GridLAB-D")
            if gld_service:
                gld_interface = GridAppsDConstants.getGLDInterface(gld_service['service_dependencies'])

            num_federates = 2
            simulator = sim_request['simulation_config']['simulator']

            if simulator.lower() == DSSAllConfigurationHandler.CONFIGTARGET:
                simulation_params = self.generate_simulation_parameters(sim_request)
                simulation_params[DSSAllConfigurationHandler.SIMULATIONID] = simulation_id
                simulation_params[DSSAllConfigurationHandler.DIRECTORY] = simulation_config_dir
                if gld_interface:
                    simulation_params[GridAppsDConstants.GRIDLABD_INTERFACE] = gld_interface

                configuration_manager.generate_configuration(
                    DSSAllConfigurationHandler.TYPENAME, simulation_params, None, simulation_id, username)
            elif simulator.lower() == OchreAllConfigurationHandler.TYPENAME:
                simulation_params = self.generate_simulation_parameters(sim_request)
                simulation_params[DSSAllConfigurationHandler.SIMULATIONID] = simulation_id
                simulation_params[DSSAllConfigurationHandler.DIRECTORY] = simulation_config_dir

                if sim_request['simulation_config']['model_creation_config']['separated_loads_file']:
                    separated_loads = self.get_separated_load_names(
                        sim_request['simulation_config']['model_creation_config']['separated_loads_file'])
                    num_federates = len(separated_loads) + 2
                    simulation_params[GLDAllConfigurationHandler.SEPARATED_LOADS_FILE] = \
                        sim_request['simulation_config']['model_creation_config']['separated_loads_file']
                else:
                    self.logger.error(f"No {GLDAllConfigurationHandler.SEPARATED_LOADS_FILE} parameter provided")
                    raise Exception(f"Missing parameter {GLDAllConfigurationHandler.SEPARATED_LOADS_FILE}")

                if gld_interface:
                    simulation_params[GridAppsDConstants.GRIDLABD_INTERFACE] = gld_interface

                configuration_manager.generate_configuration(
                    GLDAllConfigurationHandler.TYPENAME, simulation_params, None, simulation_id, username)
                configuration_manager.generate_configuration(
                    OchreAllConfigurationHandler.TYPENAME, simulation_params, None, simulation_id, username)
            else:
                simulation_params = self.generate_simulation_parameters(sim_request)
                simulation_params[GLDAllConfigurationHandler.SIMULATIONID] = simulation_id
                simulation_params[GLDAllConfigurationHandler.DIRECTORY] = simulation_config_dir
                if gld_interface:
                    simulation_params[GridAppsDConstants.GRIDLABD_INTERFACE] = gld_interface

                configuration_manager.generate_configuration(
                    GLDAllConfigurationHandler.TYPENAME, simulation_params, None, simulation_id, username)

            self.logger.debug(f"Simulation and power grid model files generated for simulation Id {simulation_id}")

            # Start Apps and Services

            simulation_context["numFederates"] = num_federates
            sim_context.numFederates = num_federates

            if 'service_configs' not in sim_request or sim_request['service_configs'] is None:
                self.logger.warn(f"No services found in request = {sim_request['simulation_config']['simulator']}")
            else:
                connect_service_instance_ids = []
                connect_service_ids = []
                connected_app_instance_ids = []
                self.logger.info(f"Service configs {sim_request['service_configs']}")
                for service_config in sim_request['service_configs']:
                    self.logger.info(f"Starting service {service_config['voltage_id']}")

                    service_instance_id = service_manager.start_service_for_simulation(
                        service_config['voltage_id'], None, simulation_context)
                    if service_instance_id:
                        connect_service_instance_ids.append(service_instance_id)
                        connect_service_ids.append(service_config['voltage_id'])

                if 'application_config' not in sim_request or sim_request['application_config'] is None:
                    self.logger.warn(
                        f"No applications found in request = {sim_request['simulation_config']['simulator']}")
                else:
                    for app in sim_request['application_config']['applications']:
                        app_info = app_manager.get_app(app['name'])
                        if not app_info:
                            self.logger.error(f"Cannot start application {app['name']}. Application not available")
                            raise Exception(f"Cannot start application {app['name']}. Application not available")

                        prereqs_list = app_manager.get_app(app['name'])['prereqs']
                        for prereq in prereqs_list:
                            if prereq not in connect_service_ids:
                                service_instance_id = service_manager.start_service_for_simulation(
                                    prereq, None, simulation_context)
                                if service_instance_id:
                                    connect_service_instance_ids.append(service_instance_id)
                                    self.logger.info(f"Started {prereq} with instance voltage_id {service_instance_id}")

                        app_instance_id = app_manager.start_app_for_simulation(
                            app['name'], app['config_string'], simulation_context)
                        connected_app_instance_ids.append(app_instance_id)
                        self.logger.info(f"Started {app['name']} with instance voltage_id {app_instance_id}")

                simulation_context["connectedServiceInstanceIds"] = connect_service_instance_ids
                simulation_context["connectedAppInstanceIds"] = connected_app_instance_ids
                sim_context.serviceInstanceIds = connect_service_instance_ids
                sim_context.appInstanceIds = connected_app_instance_ids

                simulation_service_info = service_manager.get_service(sim_request['simulation_config']['simulator'])
                service_dependencies = simulation_service_info['service_dependencies']
                for service in service_dependencies:
                    service_instance_id = service_manager.start_service_for_simulation(
                        service, None, simulation_context)
                    if service_instance_id:
                        sim_context.add_service_instance_id(service_instance_id)

                data_manager.process_data_request(sim_context, "timeseries", simulation_id, None, username)

                # Start test if requested
                test_manager.handle_test_request(sim_request['test_config'], sim_context)

                # Start simulation
                self.logger.debug(f"Starting simulation for voltage_id {simulation_id}")
                simulation_manager.start_simulation(simulation_id, sim_request['simulation_config'], sim_context,
                                                    simulation_context)
                self.logger.info(f"Started simulation for voltage_id {simulation_id}")

        except Exception as e:
            self.logger.error(f"Failed to start simulation correctly: {e}")
            print(e)

    def generate_simulation_parameters(self, request_simulation):
        params = {}

        params[GLDAllConfigurationHandler.MODELID] = request_simulation['power_system_config']['Line_name']

        model_config = request_simulation['simulation_config']['model_creation_config']
        z_fraction = model_config['z_fraction']
        i_fraction = model_config['i_fraction']
        p_fraction = model_config['p_fraction']

        params[GLDAllConfigurationHandler.ZFRACTION] = str(z_fraction)
        params[GLDAllConfigurationHandler.IFRACTION] = str(i_fraction)
        params[GLDAllConfigurationHandler.PFRACTION] = str(p_fraction)
        params[GLDAllConfigurationHandler.LOADSCALINGFACTOR] = str(model_config['load_scaling_factor'])
        params[GLDAllConfigurationHandler.RANDOMIZEFRACTIONS] = model_config['randomize_zipload_fractions']
        params[GLDAllConfigurationHandler.USEHOUSES] = model_config['use_houses']

        if 'schedule_name' in model_config:
            params[GLDAllConfigurationHandler.SCHEDULENAME] = model_config['schedule_name']
        else:
            params[GLDAllConfigurationHandler.SCHEDULENAME] = ""

        params[GLDAllConfigurationHandler.SIMULATIONNAME] = request_simulation['simulation_config']['simulation_name']
        params[GLDAllConfigurationHandler.SOLVERMETHOD] = request_simulation['simulation_config'][
            'power_flow_solver_method']

        params[GLDAllConfigurationHandler.SIMULATIONBROKERHOST] = request_simulation['simulation_config'][
            'simulation_broker_location']
        params[GLDAllConfigurationHandler.SIMULATIONBROKERPORT] = str(
            request_simulation['simulation_config']['simulation_broker_port'])

        params[GLDAllConfigurationHandler.SIMULATIONSTARTTIME] = request_simulation['simulation_config']['start_time']
        params[GLDAllConfigurationHandler.SIMULATIONDURATION] = str(request_simulation['simulation_config']['duration'])

        if 'model_state' in model_config:
            params[GLDAllConfigurationHandler.MODEL_STATE] = json.dumps(model_config['model_state'])

        params[GLDAllConfigurationHandler.SIMULATOR] = request_simulation['simulation_config']['simulator']
        params[GLDAllConfigurationHandler.RUN_REALTIME] = request_simulation['simulation_config']['run_realtime']

        if 'separated_loads_file' in model_config:
            params[GLDAllConfigurationHandler.SEPARATED_LOADS_FILE] = model_config['separated_loads_file']
        else:
            params[GLDAllConfigurationHandler.SEPARATED_LOADS_FILE] = ""

        return params



    def get_separated_load_names(self, file_name):
        load_names = []
        is_header = True

        try:
            workbook = openpyxl.load_workbook(file_name)
            sheet = workbook.active

            for row in sheet.iter_rows():
                if not is_header:
                    load_name = row[5].value
                    load_names.append(load_name)
                is_header = False

        except Exception as e:
            print(f"Error reading Excel file: {e}")

        return load_names


    def generate_config_file(self, config_file, simulation_output):
        """
        Example usage:
        simulation_output_data = {
            'output_objects': [
                {
                    'name': 'swt_g9343_48332_sw',
                    'properties': ['status']
                },
                {
                    'name': 'swt_l5397_48332_sw',
                    'properties': ['status']
                },
                {
                    'name': 'swt_a8869_48332_sw',
                    'properties': ['status']
                }
            ]
        }

        generate_config_file('configfile.json', simulation_output_data)

        :param config_file:
        :param simulation_output:
        :return:
        """
        config_data = {}

        for obj in simulation_output['output_objects']:
            config_data[obj['name']] = obj['properties']

        with open(config_file, 'w') as outfile:
            json.dump(config_data, outfile, indent=4)
