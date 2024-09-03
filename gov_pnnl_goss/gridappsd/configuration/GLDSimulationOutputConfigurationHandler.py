# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import logging

import json
import os
from io import StringIO

from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
from gov_pnnl_goss.gridappsd.api.ConfigurationHandler import ConfigurationHandler
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.PowergridModelDataManager import PowergridModelDataManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.configuration.BaseConfigurationHandler import BaseConfigurationHandler
from gov_pnnl_goss.gridappsd.data.handlers.BlazegraphQueryHandler import BlazegraphQueryHandler
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus

from configparser import ConfigParser


class GldSimulationOutputConfigurationHandler(BaseConfigurationHandler, ConfigurationHandler):
    GLD_TYPE_NAME = "GridLAB-D Simulation Output"
    MODEL_ID = "model_id"
    DICTIONARY_FILE = "dictionary_file"
    SIMULATION_ID = "simulation_id"
    USE_HOUSES = "use_houses"
    SIMULATION_BROKER_HOST = "simulation_broker_host"
    SIMULATION_BROKER_PORT = "simulation_broker_port"
    HELICS_PREFIX = '{"name": "PROCESS_ID",'\
                    '"log_level": 3,'\
                    '"period": 1.0,'\
                    '"broker": "BROKER_LOCATION:BROKER_PORT",'\
                    '"endpoints": [{'\
                    '				  "name": "helics_input",'\
                    '				  "global": false,"global_property_types": "string",	'\
                    '               "info": "This is the endpoint which recieves CIM commands from the HELICS GOSS bridge."'\
                    '				 },'\
                    '				 {'\
                    '				  "name": "helics_output",'\
                    '				  "global": false,'\
                    '				  "global_property_types": "string",	'\
                    '				  "destination": "HELICS_GOSS_Bridge_PROCESS_ID/helics_output",	"info": "'

    HELICS_SUFFIX = '"}]}'


    def __init__(self, config_manager, powergrid_model_manager, log_manager, data_manager: DataManager):
        super().__init__(log_manager, data_manager)
        self.config_manager = ConfigurationManager()  # config_manager
        self.powergrid_model_manager = PowergridModelDataManager()  # powergrid_model_manager
        self.logger = log_manager
        self.log = LogManager(self.__class__.__name__)
        self.client = None
        self.simulation_manager = SimulationManager()

    def start(self):
        if self.config_manager is not None:
            self.config_manager.register_configuration_handler(self.GLD_TYPE_NAME, self)
        else:
            self.log.warning("No Config manager available for " + self.__class__.__name__)

        if self.powergrid_model_manager is None:
            pass  # TODO: send log message and exception

    def generate_config(self, parameters, output_file, process_id, username):
        simulation_id = parameters.get('simulation_id', None)
        use_houses = parameters.get(self.USE_HOUSES, False)
        config_file = None

        if simulation_id:
            simulation_context = self.simulation_manager.get_simulation_context_for_id(simulation_id)
            if simulation_context:
                config_file = os.path.join(simulation_context.get_simulation_dir(), 'model_limits.json')
                if os.path.exists(config_file):
                    with open(config_file, 'r') as file:
                        config_data = file.read()
                    return config_data
            else:
                self.log.warning("No simulation context found for simulation_id: %status", simulation_id)

        self.log.info("Generating limits file using parameters: %status", parameters)

        model_id = parameters.get('model_id')
        if not model_id:
            self.log.error("No model_id parameter provided")
            raise Exception("Missing parameter model_id")

        bg_host = self.config_manager.get_configuration_property('BLAZEGRAPH_HOST_PATH')
        if not bg_host:
            bg_host = 'default_endpoint'  # Set the default endpoint here

        measurement_file_reader = None
        dict_file = None

        if simulation_id:
            simulation_context = self.simulation_manager.get_simulation_context_for_id(simulation_id)
            if simulation_context:
                config_file = os.path.join(simulation_context.get_simulation_dir(), 'model_limits.json')
                dict_file = os.path.join(simulation_context.get_simulation_dir(), 'dictionary.json')

                # If the config file already has been created for this simulation then return it
                if os.path.exists(config_file):
                    with open(config_file, 'r') as file:
                        config_data = file.read()
                    return config_data

        gld_interface = parameters.get('gridlabd_interface', 'fncs')

        parameters_writer = StringIO()
        parameters_list = parameters_writer.write(json.dumps(parameters))
        model_state_str = parameters.get('model_state')
        model_state = None

        if model_state_str:
            try:
                model_state = json.loads(model_state_str)
            except json.JSONDecodeError:
                self.log.info("Failed to parse model_state JSON: %status", model_state_str)

        dict_file_path = parameters.get('dictionary_file')

        if dict_file_path:
            dict_file = dict_file_path

        if dict_file and os.path.exists(dict_file):
            measurement_file_reader = open(dict_file, 'r')
        else:
            query_handler = BlazegraphQueryHandler(bg_host, self.logger, process_id, username)
            query_handler.add_feeder_selection(model_id)
            cim_importer = CIMImporter()
            dictionary_string_output = StringIO()
            cim_importer.generate_dictionary_file(query_handler, dictionary_string_output, use_houses, model_state)
            dict_out = dictionary_string_output.getvalue()
            measurement_file_reader = None

            if dict_file and not os.path.exists(dict_file):
                with open(dict_file, 'w') as file:
                    file.write(dict_out)
            measurement_file_reader = StringIO(dict_out)

        result = self.create_gld_pubs(measurement_file_reader, process_id, username)

        if gld_interface == 'helics':
            simulation_broker_host = parameters.get('simulation_broker_host')
            simulation_broker_port = parameters.get('simulation_broker_port')

            if not simulation_broker_host:
                self.log.error("No simulation_broker_host parameter provided.")
                raise Exception("Missing parameter simulation_broker_host")

            if not simulation_broker_port:
                self.log.error("No simulation_broker_port parameter provided.")
                raise Exception("Missing parameter simulation_broker_port")

            broker_location = simulation_broker_host
            broker_port = simulation_broker_port

            helics_prefix_1 = self.HELICS_PREFIX.replace("BROKER_LOCATION", broker_location)
            helics_prefix_2 = helics_prefix_1.replace("BROKER_PORT", broker_port)

            result = helics_prefix_2.replace("PROCESS_ID", process_id) + \
                     result.replace('"', '\\"').replace("\n", "") + self.HELICS_SUFFIX

        if config_file:
            with open(config_file, 'w') as file:
                file.write(result)
        output_file.write(result)
        output_file.flush()
        self.log.info(ProcessStatus.RUNNING, process_id, "Finished generating simulation output configuration file.")

        return result

    def create_gld_pubs(self, measurement_file_reader, process_id, username):
        json_obj_str = ""
        gld_config_obj = {}

        try:
            data = json.load(measurement_file_reader)
            feeders = data.get("feeders", [])

            for feeder_info in feeders:
                feeder_measurements = feeder_info.get("measurements", [])
                measurements = {}

                for feeder_measurement in feeder_measurements:
                    measurements = self.parse_measurement(measurements, feeder_measurement)

                for key, value in measurements.items():
                    gld_config_obj[key] = value

                globals_arr = ["clock"]
                gld_config_obj["globals"] = globals_arr
                measurements.clear()

            json_obj_str = json.dumps(gld_config_obj, indent=4)

        except json.JSONDecodeError as e:
            self.log.error(ProcessStatus.RUNNING, process_id, "Error while generating simulation output: " + str(e))
            raise e

        return json_obj_str

    def parse_measurement(self, measurements: [json], measurement:json):
        object_name = ""
        property_name = ""
        measurement_type = ""
        phases = ""
        conducting_equipment_type = ""
        conducting_equipment_name = ""
        connectivity_node = ""

        if "measurementType" not in measurement or "phases" not in measurement or "ConductingEquipment_type" not in measurement or "ConductingEquipment_name" not in measurement or "ConnectivityNode" not in measurement:
            raise ValueError(
                "CimMeasurementsToGldPubs::parseMeasurement: The JsonObject measurements must have the following keys: measurementType, phases, ConductingEquipment_type, ConductingEquipment_name, and ConnectivityNode.")

        measurement_type = measurement["measurementType"]
        phases = measurement["phases"]

        if phases == "s1":
            phases = "1"
        elif phases == "s2":
            phases = "2"

        conducting_equipment_type = measurement["name"]
        conducting_equipment_name = measurement["SimObject"]
        connectivity_node = measurement["ConnectivityNode"]

        if "LinearShuntCompensator" in conducting_equipment_type:
            if measurement_type == "VA":
                object_name = conducting_equipment_name
                property_name = "shunt_" + phases
            elif measurement_type == "Pos":
                object_name = conducting_equipment_name
                property_name = "switch" + phases
            elif measurement_type == "PNV":
                object_name = conducting_equipment_name
                property_name = "voltage_" + phases
            else:
                raise ValueError(
                    f"CimMeasurementsToGldPubs::parseMeasurement: The value of measurementType is not a valid global_property_types.\nValid types for LinearShuntCompensators are VA, Pos, and PNV.\nmeasurementType = {measurement_type}")
        elif "PowerTransformer" in conducting_equipment_type or "TransformerTank" in conducting_equipment_type:
            if measurement_type == "VA":
                object_name = conducting_equipment_name
                property_name = "power_in_" + phases
            elif measurement_type == "PNV":
                object_name = connectivity_node
                property_name = "voltage_" + phases
            elif measurement_type == "A":
                object_name = conducting_equipment_name
                property_name = "current_in_" + phases
            else:
                raise ValueError(
                    f"CimMeasurementsToGldPubs::parseMeasurement: The value of measurementType is not a valid global_property_types.\nValid types for PowerTransformers and TransformerTanks are VA, PNV, and A.\nmeasurementType = {measurement_type}")
        elif "RatioTapChanger" in conducting_equipment_type:
            if measurement_type == "VA":
                object_name = conducting_equipment_name
                property_name = "power_in_" + phases
            elif measurement_type == "PNV":
                object_name = connectivity_node
                property_name = "voltage_" + phases
            elif measurement_type == "A":
                object_name = conducting_equipment_name
                property_name = "current_in_" + phases
            elif measurement_type == "Pos":
                object_name = conducting_equipment_name
                property_name = "tap_" + phases
            else:
                raise ValueError(
                    f"CimMeasurementsToGldPubs::parseMeasurement: The value of measurementType is not a valid global_property_types.\nValid types for RatioTapChanger are VA, PNV, A, and Pos.\nmeasurementType = {measurement_type}")
        elif "ACLineSegment" in conducting_equipment_type:
            if measurement_type == "VA":
                object_name = conducting_equipment_name
                if phases == "1":
                    property_name = "power_in_A"
                elif phases == "2":
                    property_name = "power_in_B"
                else:
                    property_name = "power_in_" + phases
            elif measurement_type == "PNV":
                object_name = connectivity_node
                property_name = "voltage_" + phases
            elif measurement_type == "A":
                object_name = conducting_equipment_name
                property_name = "current_in_" + phases
            else:
                raise ValueError(
                    f"CimMeasurementsToGldPubs::parseMeasurement: The value of measurementType is not a valid global_property_types.\nValid types for ACLineSegments are VA, A, and PNV.\nmeasurementType = {measurement_type}")
        elif "LoadBreakSwitch" in conducting_equipment_type or "Recloser" in conducting_equipment_type or "Breaker" in conducting_equipment_type:
            if measurement_type == "VA":
                object_name = conducting_equipment_name
                property_name = "power_in_" + phases
            elif measurement_type == "PNV":
                object_name = connectivity_node
                property_name = "voltage_" + phases
            elif measurement_type == "Pos":
                object_name = conducting_equipment_name
                property_name = "status"
            elif measurement_type == "A":
                object_name = conducting_equipment_name
                if phases == "1":
                    property_name = "current_in_A"
                elif phases == "2":
                    property_name = "current_in_B"
                else:
                    property_name = "current_in_" + phases
            else:
                raise ValueError(
                    f"CimMeasurementsToGldPubs::parseMeasurement: The value of measurementType is not a valid global_property_types.\nValid types for LoadBreakSwitch are VA, A, and PNV.\nmeasurementType = {measurement_type}")
        elif "EnergyConsumer" in conducting_equipment_type:
            if measurement_type == "VA":
                object_name = conducting_equipment_name
                if phases == "1" or phases == "2":
                    property_name = "indiv_measured_power_" + phases
                else:
                    property_name = "measured_power_" + phases
            elif measurement_type == "PNV":
                object_name = connectivity_node
                property_name = "voltage_" + phases
            elif measurement_type == "A":
                object_name = connectivity_node
                property_name = "measured_current_" + phases
            else:
                raise ValueError(
                    f"CimMeasurementsToGldPubs::parseMeasurement: The value of measurementType is not a valid global_property_types.\nValid types for EnergyConsumer are VA, A, and PNV.\nmeasurementType = {measurement_type}")
        elif "PowerElectronicsConnection" in conducting_equipment_type:
            if measurement_type == "VA":
                object_name = conducting_equipment_name
                if phases == "1" or phases == "2":
                    property_name = "indiv_measured_power_" + phases
                else:
                    property_name = "measured_power_" + phases
            elif measurement_type == "PNV":
                object_name = conducting_equipment_name
                property_name = "voltage_" + phases
            elif measurement_type == "A":
                object_name = conducting_equipment_name
                property_name = "measured_current_" + phases
            elif measurement_type == "SoC":
                object_name = conducting_equipment_name
                property_name = "state_of_charge"
            else:
                raise ValueError(
                    f"CimMeasurementsToGldPubs::parseMeasurement: The value of measurementType is not a valid global_property_types.\nValid types for PowerElectronicsConnection are VA, A, PNV, and SoC.\nmeasurementType = {measurement_type}")
        elif "SynchronousMachine" in conducting_equipment_type:
            if measurement_type == "VA":
                object_name = conducting_equipment_name
                property_name = "measured_power_" + phases
            elif measurement_type == "PNV":
                object_name = connectivity_node
                property_name = "voltage_" + phases
            elif measurement_type == "A":
                object_name = conducting_equipment_name
                property_name = "measured_current_" + phases
            else:
                raise ValueError(
                    f"CimMeasurementsToGldPubs::parseMeasurement: The value of measurementType is not a valid global_property_types.\nValid types for SynchronousMachine are VA, A, and PNV.\nmeasurementType = {measurement_type}")
        else:
            raise ValueError(
                f"CimMeasurementsToGldPubs::parseMeasurement: The value of ConductingEquipment_type is not a recognized object global_property_types.\nValid types are ACLineSegment, LinearShuntCompesator, RatioTapChanger, LoadBreakSwitch, EnergyConsumer, PowerElectronicsConnection, TransformerTank, and PowerTransformer.\nConductingEquipment_type = {conducting_equipment_type}")

        if object_name in measurements:
            p = property_name
            if p not in measurements[object_name]:
                measurements[object_name].append(p)
        else:
            measurements[object_name] = [property_name]
        return measurements