# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import os
from io import StringIO
from logging import getLogger

from gov_pnnl_goss.SpecialClasses import File
from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
from gov_pnnl_goss.gridappsd.api.ConfigurationHandler import ConfigurationHandler
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.api.PowergridModelDataManager import PowergridModelDataManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.configuration.BaseConfigurationHandler import BaseConfigurationHandler
import logging

from gov_pnnl_goss.gridappsd.configuration.CIMDictionaryConfigurationHandler import PrintWriter, FileWriter
from gov_pnnl_goss.gridappsd.data.handlers.BlazegraphQueryHandler import BlazegraphQueryHandler
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class DSSBaseConfigurationHandler(BaseConfigurationHandler, ConfigurationHandler):

    def __init__(self, log_manager: LogManager, data_manager: DataManager):
        super().__init__(log_manager, data_manager)
        self.log = getLogger(__name__)
        self.client = None
        self.config_manager = ConfigurationManager()
        self.simulation_manager = SimulationManager()
        self.powergrid_model_manager = PowergridModelDataManager()
        self.log = LogManager(DSSBaseConfigurationHandler.__name__)
        self.cimhub_prefix = "model"
        self.dssbase_filename = self.cimhub_prefix + "base.dss"
        self.dssbusxy_filename = self.cimhub_prefix + "busxy.ds"
        self.dssguid_filename = self.cimhub_prefix + "guid.ds"
        self.dssdictionary_filename = self.cimhub_prefix + "dict.json"
        self.typename = "DSS Base"
        self.zfraction = "z_fraction"
        self.ifraction = "i_fraction"
        self.pfraction = "p_fraction"
        self.schedulename = "schedule_name"
        self.loadscalingfactor = "load_scaling_factor"
        self.modelid = "model_id"
        self.buscoords = "buscoords"
        self.guids = "guids"
        self.simulationid = "simulation_id"

    def start(self):
        if self.config_manager is not None:
            self.config_manager.register_configuration_handler(self.typename, self)
        else:
            self.log.warn("No Config manager avilable for " + str(__class__))

        if self.powergrid_model_manager is None:
            pass  # TODO send log message and exception

    def generate_config(self, parameters, out, process_id, username):
        b_want_zip = False
        b_want_sched = False
        self.log.info(ProcessStatus.RUNNING, process_id, "Generating Base DSS configuration file using parameters: " + str(parameters))
        simulation_id = parameters.get(self.simulationid, None)
        config_file = None
        id_file = None
        if simulation_id:
            simulation_context = self.simulation_manager.get_simulation_context_for_id(simulation_id)
            if simulation_context:
                config_file = File(os.path.join(simulation_context.get_simulation_dir(), self.dssbase_filename))
                id_file = File(os.path.join(simulation_context.get_simulation_dir(), self.dssguid_filename))
                # If the config file already has been created for this simulation then return it
                if config_file:
                    self.print_file_to_output(config_file, out)
                    self.log.info(ProcessStatus.RUNNING, process_id, "Dictionary DSS base file for simulation " + simulation_id + " already exists.")
                    return
            else:
                self.log.warning(ProcessStatus.RUNNING, process_id, "No simulation context found for simulation_id: " + simulation_id)

        z_fraction = parameters.get(self.zfraction, 0)
        if z_fraction == 0:
            z_fraction = 0
            b_want_zip = True

        i_fraction = parameters.get(self.ifraction, 0)
        if i_fraction == 0:
            i_fraction = 1
            b_want_zip = True

        p_fraction = parameters.get(self.pfraction, 0)
        if p_fraction == 0:
            p_fraction = 0
            b_want_zip = True

        load_scale = parameters.get(self.loadscalingfactor, 0)

        schedule_name = parameters.get(self.schedulename, None)
        if schedule_name and schedule_name.strip():
            b_want_sched = True

        model_id = parameters.get(self.modelid, None)
        if not model_id or not model_id.strip():
            self.log.error(ProcessStatus.ERROR, process_id, "No " + self.modelid + " parameter provided")
            raise Exception("Missing parameter " + self.modelid)

        bg_host = self.config_manager.get_configuration_property(GridAppsDConstants.BLAZEGRAPH_HOST_PATH)
        if not bg_host or not bg_host.strip():
            bg_host = BlazegraphQueryHandler.DEFAULT_ENDPOINT

        buscoords = parameters.get(self.buscoords, None)
        if not buscoords or not buscoords.strip():
            buscoords = self.dssbusxy_filename

        guids = parameters.get(self.guids, None)
        if not guids or not guids.strip():
            guids = self.dssguid_filename
        # TODO write a query handler that uses the built in powergrid model data manager that talks to blazegraph internally
        query_handler = BlazegraphQueryHandler(bg_host, self.log, process_id, username)
        query_handler.add_feeder_selection(model_id)

        cim_importer = CIMImporter()
        # If the simulation info is available also write to file
        if config_file:
            cim_importer.generate_dss_file(query_handler, PrintWriter(FileWriter(config_file)),
                                           PrintWriter(FileWriter(id_file)), buscoords, guids,
                                           load_scale, b_want_sched, None, b_want_zip, z_fraction,
                                           i_fraction, p_fraction)
            # config was written to base file, so return that
            self.print_file_to_output(config_file, out)
        else:
            id_file_writer = StringIO()
            cim_importer.generate_dss_file(query_handler, out, id_file_writer, buscoords,
                                           guids, load_scale, b_want_sched, None,
                                           b_want_zip, z_fraction, i_fraction, p_fraction)
            id_file_writer.close()

        self.log.info(ProcessStatus.RUNNING, process_id, "Finished generating DSS Base configuration file.")
