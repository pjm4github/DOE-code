# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import logging
from pathlib import Path
from io import StringIO
import subprocess

from gov_pnnl_goss.gridappsd.api.ConfigurationHandler import ConfigurationHandler
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.PowergridModelDataManager import PowergridModelDataManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.configuration.DSSAllConfigurationHandler import DSSAllConfigurationHandler
from gov_pnnl_goss.gridappsd.configuration.OchreAllConfigurationHandler import GridAPPSD
from gov_pnnl_goss.gridappsd.dto.YBusExportResponse import YBusExportResponse


class YBusExportConfigurationHandler(ConfigurationHandler):
    TYPENAME = "YBus Export"
    DIRECTORY = "directory"
    SIMULATIONID = "simulation_id"
    MODELID = "model_id"
    ZFRACTION = "z_fraction"
    IFRACTION = "i_fraction"
    PFRACTION = "p_fraction"
    SCHEDULENAME = "schedule_name"
    LOADSCALINGFACTOR = "load_scaling_factor"

    def __init__(self, log_manager=None):

        self.logger = log_manager
        self.log = LogManager(YBusExportConfigurationHandler.__class__.__name__)
        self.power_grid_model_data_manager = PowergridModelDataManager()
        self.config_manager = ConfigurationManager()  # config_manager
        self.simulation_manager = SimulationManager()


    def start(self):
        if self.config_manager:
            self.config_manager.register_configuration_handler(self.TYPENAME, self)
        else:
            # TODO send log message and exception
            self.log.warning("No Config manager available for " + self.__class__.__name__)

    def generate_config(self, parameters, out, process_id, username):
        response = YBusExportResponse()
        simulation_id = parameters.get(self.SIMULATIONID)
        model_id = None
        base_dss_dir = None
        
        if simulation_id:
            simulation_context = self.simulation_manager.get_simulation_context(simulation_id)
            if not simulation_context:
                raise Exception("Simulation context not found for simulation_id = " + simulation_id)
            base_dss_dir = Path(simulation_context.get_simulation_dir())
            parameters["i_fraction"] = str(simulation_context.get_request().get_simulation_config().get_model_creation_config().get_i_fraction())
            parameters["z_fraction"] = str(simulation_context.get_request().get_simulation_config().get_model_creation_config().get_z_fraction())
            parameters["p_fraction"] = str(simulation_context.get_request().get_simulation_config().get_model_creation_config().get_p_fraction())
            parameters["load_scaling_factor"] = str(simulation_context.get_request().get_simulation_config().get_model_creation_config().get_load_scaling_factor())
            parameters["schedule_name"] = simulation_context.get_request().get_simulation_config().get_model_creation_config().get_schedule_name()
            parameters["model_id"] = simulation_context.get_request().get_power_system_config().get_line_name()
            parameters["directory"] = simulation_context.get_simulation_dir()
            parameters["simulation_start_time"] = simulation_context.get_request().get_simulation_config().get_start_time()
            parameters["simulation_duration"] = simulation_context.get_request().get_simulation_config().get_duration()
        else:
            model_id = parameters.get(self.MODELID)
            simulation_id = process_id
            if not model_id:
                raise Exception("Model Id or simulation Id not provided in request parameters.")
            base_dss_dir = self.config_manager.get_configuration_property(self.GRIDAPPSD_TEMP_PATH, 'models', model_id)
            parameters["i_fraction"] = GridAPPSD.get_double_property(parameters, self.IFRACTION, 0)
            parameters["z_fraction"] = GridAPPSD.get_double_property(parameters, self.ZFRACTION, 0)
            parameters["p_fraction"] = GridAPPSD.get_double_property(parameters, self.PFRACTION, 0)
            parameters["load_scaling_factor"] = GridAPPSD.get_double_property(parameters, self.LOADSCALINGFACTOR, 1)
            parameters["schedule_name"] = GridAPPSD.get_string_property(parameters, self.SCHEDULENAME, "")
            parameters["model_id"] = model_id
            parameters["directory"] = base_dss_dir
        
        yparse_path = base_dss_dir + "/base_ysparse.csv"
        nodelist_path = base_dss_dir + "/base_nodelist.csv"
        summary_path = base_dss_dir + "/base_summary.csv"
        
        if yparse_path and nodelist_path and summary_path:
            response.set_yparse(yparse_path.read_text())
            response.set_nodelist(nodelist_path.read_text())
            response.set_summary(summary_path.read_text())
            out.print(response)
        else:
            if not base_dss_dir.exists():
                base_dss_dir.mkdir()
            command_file = base_dss_dir / "opendsscmdInput.txt"
            dss_base_file = base_dss_dir / "model_base.dss"
            parameters["directory"] = base_dss_dir.absolute()
            
            if not dss_base_file.exists():
                base_print_writer = StringIO()
                dss_all_configuration_handler = DSSAllConfigurationHandler(self.logger,
                                                                           SimulationManager(),
                                                                           self.config_manager.get_instance())
                dss_all_configuration_handler.generate_config(parameters, base_print_writer, process_id, username)
            
            if not dss_base_file.exists():
                raise Exception("Error: Could not create DSS base file to export YBus matrix")
            
            with command_file.open("w") as file_writer:
                file_writer.write("redirect model_base.dss\n")
                file_writer.write("batchedit transformer..* wdg=2 tap=1\n")
                file_writer.write("batchedit regcontrol..* enabled=false\n")
                file_writer.write("batchedit vsource..* enabled=false\n")
                file_writer.write("batchedit isource..* enabled=false\n")
                file_writer.write("batchedit load..* enabled=false\n")
                file_writer.write("batchedit generator..* enabled=false\n")
                file_writer.write("batchedit pvsystem..* enabled=false\n")
                file_writer.write("batchedit storage..* enabled=false\n")
                file_writer.write("solve\n")
                file_writer.write("export y triplet base_ysparse.csv\n")
                file_writer.write("export nodelist base_nodelist.csv\n")
                file_writer.write("export summary base_summary.csv\n")
                file_writer.flush()
            
            process_service_builder = subprocess.Popen(['opendsscmd', command_file], cwd=base_dss_dir)
            process_service_builder.communicate()

            if not yparse_path.exists() or not nodelist_path.exists() or not summary_path.exists():
                raise Exception("Error: Failed to generate Y Bus matrix.")
            
            response.set_yparse(yparse_path.read_text())
            response.set_nodelist(nodelist_path.read_text())
            response.set_summary(summary_path.read_text())
            out.print(response)

