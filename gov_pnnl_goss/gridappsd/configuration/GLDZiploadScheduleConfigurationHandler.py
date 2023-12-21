# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import io
import logging
from datetime import datetime
import os
from dateutil import parser
from calendar import timegm

from gov_pnnl_goss.SpecialClasses import File
from gov_pnnl_goss.gridappsd.api.ConfigurationHandler import ConfigurationHandler
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.data.conversion.ProvenLoadScheduleToGridlabdLoadScheduleConverter \
    import ProvenLoadScheduleToGridlabdLoadScheduleConverter
from gov_pnnl_goss.gridappsd.api.PowergridModelDataManager import PowergridModelDataManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.configuration.BaseConfigurationHandler import BaseConfigurationHandler
from gov_pnnl_goss.gridappsd.configuration.GLDAllConfigurationHandler import ProvenTimeSeriesDataManagerImpl
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.dto.RequestTimeseriesDataBasic import RequestTimeseriesDataBasic
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class Calendar:
    pass


class FileOutputStream(io.FileIO):
    pass


class GldZiploadScheduleConfigurationHandler(BaseConfigurationHandler, ConfigurationHandler):
    TYPENAME = "GridLAB-D Zipload Schedule"
    DIRECTORY = "directory"
    SIMULATIONNAME = "simulation_name"
    SCHEDULENAME = "schedule_name"
    SIMULATIONSTARTTIME = "simulation_start_time"
    SIMULATIONDURATION = "simulation_duration"
    SIMULATIONID = "simulation_id"
    STARTTIME_FILTER = "startTime"
    ENDTIME_FILTER = "endTime"
    TIMEFILTER_YEAR = 2018
    cimhub_PREFIX = "model"

    def __init__(self, log_manager: LogManager = None, data_manager: DataManager = None):
        super().__init__(log_manager, data_manager)
        self.logger = log_manager
        self.data_manager = DataManager()
        self.config_manager = ConfigurationManager()  # config_manager
        # self.powergrid_model_manager = PowergridModelDataManager()  # powergrid_model_manager
        self.log = LogManager(self.__class__.__name__)
        self.simulation_manager = SimulationManager()


    @Start
    def start(self):
        if self.config_manager:
            self.config_manager.register_configuration_handler(self.TYPENAME, self)
        else:
            self.log.error(f"{ProcessStatus.ERROR}, No Config manager avilable for "
                           f"{GldZiploadScheduleConfigurationHandler.__name__}")

    def generate_config(self, parameters, out, process_id, username):
        self.log.info(f"{ProcessStatus.RUNNING}, {process_id}, "
                      f"Generating zipload schedule GridLAB-D configuration files using parameters: {parameters}")
        schedule_name = GridAppsDConstants.getStringProperty(parameters, self.SCHEDULENAME, None)
        directory = GridAppsDConstants.getStringProperty(parameters, self.DIRECTORY, None)
        if directory == None or directory.trim().length() == 0:
            self.log.error(ProcessStatus.ERROR, process_id, "No " + self.DIRECTORY + " parameter provided")
            raise Exception("Missing parameter " + self.DIRECTORY)
        
        simulation_start_time = GridAppsDConstants.getLongProperty(parameters, self.SIMULATIONSTARTTIME, -1)
        if simulation_start_time < 0:
            self.log.error(ProcessStatus.ERROR, process_id, "No " + self.SIMULATIONSTARTTIME + " parameter provided")
            raise Exception("Missing parameter " + self.SIMULATIONSTARTTIME)
        
        simulation_duration = GridAppsDConstants.getLongProperty(parameters, self.SIMULATIONDURATION, 0)
        if simulation_duration == 0:
            self.log.error(ProcessStatus.ERROR, process_id, "No " + self.SIMULATIONDURATION + " parameter provided")
            raise Exception("Missing parameter " + self.SIMULATIONDURATION)
        
        dir = File(directory)
        if not dir.exists():
            dir.mkdirs()
        
        temp_data_path = dir.getAbsolutePath()
        
        simulation_id = GridAppsDConstants.getStringProperty(parameters, self.SIMULATIONID, None)
        load_profile = GridAppsDConstants.getStringProperty(parameters, self.SCHEDULENAME, "ieeezipload")
        sim_id = "1"
        if not simulation_id:
            self.log.error(f"{ProcessStatus.ERROR}, No  {self.SIMULATIONID} parameter provided")
            raise Exception("Missing parameter " + self.SIMULATIONID)
        
        try:
            sim_id = simulation_id
        except Exception as e:
            self.log.error(f"{ProcessStatus.ERROR}, {simulation_id},Simulation ID not a valid simulation_id, defaulting to {sim_id}")
        
        request = RequestTimeseriesDataBasic()
        request.setQueryMeasurement(load_profile)
        request.setResponseFormat(ProvenLoadScheduleToGridlabdLoadScheduleConverter.OUTPUT_FORMAT)
        
        query_filter = {}
        c = Calendar.getInstance()
        c.setTime(datetime.utcfromtimestamp(simulation_start_time))
        simulation_year = c.get(Calendar.YEAR)
        c.set(Calendar.YEAR, self.TIMEFILTER_YEAR)
        query_filter.put(self.STARTTIME_FILTER, "" + c.getTimeInMillis())
        c.add(Calendar.SECOND, int(simulation_duration))
        query_filter.put(self.ENDTIME_FILTER, "" + c.getTimeInMillis())
        
        request.setQueryFilter(query_filter)
        request.setSimulationYear(simulation_year)
        request.setOriginalFormat("loadprofile")
        
        resp = self.data_manager.processDataRequest(request, ProvenTimeSeriesDataManagerImpl.DATA_MANAGER_TYPE, sim_id, temp_data_path, username)

        if resp.getData() == None:
            raise Exception("No load schedule data in time series data store. Setting useClimate = false.")
        else:
            load_schedule_file = File(directory + File.separator + schedule_name + ".player")
            fout = FileOutputStream(load_schedule_file)
            fout.write(resp.getData().to"".getBytes())
            fout.flush()
            fout.close()

        self.log.info(ProcessStatus.RUNNING, process_id, "Finished generating all GridLAB-D configuration files.")

