import calendar
import time

import os
import json
from datetime import datetime, timedelta

import openpyxl

from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
from gov_pnnl_goss.cimhub.CIMQuerySetter import CIMQuerySetter
from gov_pnnl_goss.cimhub.dto.ModelState import ModelState
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.data.handlers.BlazegraphQueryHandler import BlazegraphQueryHandler
from gov_pnnl_goss.gridappsd.dto.RequestTimeseriesDataBasic import RequestTimeseriesDataBasic
from gov_pnnl_goss.gridappsd.utils import GridAppsDConstants

from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.configuration import BaseConfigurationHandler
import logging


class ProvenWeatherToGridlabdWeatherConverter:
    pass


class ProvenTimeSeriesDataManagerImpl:
    pass


class GLDZiploadScheduleConfigurationHandler:
    pass


class GLDSimulationOutputConfigurationHandler:
    pass


class GLDConfigManager:
    pass


class GLDAllConfigurationHandler(BaseConfigurationHandler):
    TYPENAME = "GridLAB-D All"
    DIRECTORY = "directory"
    SIMULATIONNAME = "simulation_name"
    ZFRACTION = "z_fraction"
    IFRACTION = "i_fraction"
    PFRACTION = "p_fraction"
    RANDOMIZEFRACTIONS = "randomize_zipload_fractions"
    USEHOUSES = "use_houses"
    SCHEDULENAME = "schedule_name"
    LOADSCALINGFACTOR = "load_scaling_factor"
    MODELID = "model_id"
    SOLVERMETHOD = "solver_method"
    SIMULATIONSTARTTIME = "simulation_start_time"
    SIMULATIONDURATION = "simulation_duration"
    SIMULATIONID = "simulation_id"
    SIMULATIONBROKERHOST = "simulation_broker_host"
    SIMULATIONBROKERPORT = "simulation_broker_port"
    STARTTIME_FILTER = "startTime"
    ENDTIME_FILTER = "endTime"
    MODEL_STATE = "model_state"
    SIMULATOR = "simulator"
    SEPARATED_LOADS_FILE = "separated_loads_file"
    RUN_REALTIME = "run_realtime"
    TIMESTEP = "timestep"

    CONFIGTARGET = "both"  # Will build files for both glm and dss
    cimhub_PREFIX = "model"
    BASE_FILENAME = cimhub_PREFIX + "_base.glm"
    STARTUP_FILENAME = cimhub_PREFIX + "_startup.glm"
    SCHEDULES_FILENAME = cimhub_PREFIX + "_schedules.glm"
    MEASUREMENTOUTPUTS_FILENAME = cimhub_PREFIX + "_outputs.json"
    DICTIONARY_FILENAME = cimhub_PREFIX + "_dict.json"
    WEATHER_FILENAME = cimhub_PREFIX + "_weather.csv"

    def __init__(self, log_manager, data_manager):
        self.logger = log_manager
        self.log = LogManager(GLDAllConfigurationHandler.__name__)
        self.data_manager = data_manager
        self.client = None
        self.config_manager = None #  ConfigurationManager()
        self.powergrid_model_manager = None  # PowergridModelDataManager()
        self.simulation_manager = None  # SimulationManager()

    def start(self):
        if self.config_manager is not None:
            self.config_manager.registerConfigurationHandler(self.TYPENAME, self)
        else:
            # TODO: Send log message and exception
            self.log.warning("No Config manager available for " + str(self.__class__))

        if self.powergrid_model_manager is None:
            # TODO: Send log message and exception
            pass  # Handle the case where powergrid_model_manager is None

    def generateConfig(self, parameters, out, processId, username):
        bWantZip = True
        bWantSched = False
        separateLoads = []

        self.log.info(ProcessStatus.RUNNING, processId,
                             "Generating all GridLAB-D configuration files using parameters: " + str(parameters))

        zFraction = parameters.get(self.ZFRACTION, 0)
        iFraction = parameters.get(self.IFRACTION, 0)
        pFraction = parameters.get(self.PFRACTION, 0)

        if zFraction == 0 and iFraction == 0 and pFraction == 0:
            bWantZip = False

        bWantRandomFractions = parameters.get(self.RANDOMIZEFRACTIONS, False)

        loadScale = parameters.get(self.LOADSCALINGFACTOR, 1)

        scheduleName = parameters.get(self.SCHEDULENAME)
        if scheduleName is not None and len(scheduleName.strip()) > 0:
            bWantSched = True

        directory = parameters.get(self.DIRECTORY)
        if directory is None or len(directory.strip()) == 0:
            self.log.error(ProcessStatus.ERROR, processId, "No " + self.DIRECTORY + " parameter provided")
            raise Exception("Missing parameter " + self.DIRECTORY)

        modelId = parameters.get(self.MODELID)
        if modelId is None or len(modelId.strip()) == 0:
            self.log.error(ProcessStatus.ERROR, processId, "No " + self.MODELID + " parameter provided")
            raise Exception("Missing parameter " + self.MODELID)

        bgHost = self.config_manager.getConfigurationProperty(GridAppsDConstants.BLAZEGRAPH_HOST_PATH)
        if bgHost is None or len(bgHost.strip()) == 0:
            bgHost = BlazegraphQueryHandler.DEFAULT_ENDPOINT

        simulationID = parameters.get(self.SIMULATIONID)
        simId = "1"
        if simulationID is None or len(simulationID.strip()) == 0:
            self.log.error(ProcessStatus.ERROR, processId, "No " + self.SIMULATIONID + " parameter provided")
            raise Exception("Missing parameter " + self.SIMULATIONID)
        try:
            simId = simulationID
        except Exception as e:
            self.log.error(ProcessStatus.ERROR, simulationID,
                                  "Simulation ID not a valid " + simulationID + ", defaulting to " + simId)

        modelState = ModelState()
        modelStateStr = parameters.get(self.MODELSTATE)
        if modelStateStr is None or len(modelStateStr.strip()) == 0:
            self.log.info(ProcessStatus.RUNNING, processId, "No " + self.MODELSTATE + " parameter provided")
        else:
            modelState = json.loads(modelStateStr)

        simulationStartTime = parameters.get(self.SIMULATIONSTARTTIME, -1)
        if simulationStartTime < 0:
            self.log.error(ProcessStatus.ERROR, processId,
                                  "No " + self.SIMULATIONSTARTTIME + " parameter provided")
            raise Exception("Missing parameter " + self.SIMULATIONSTARTTIME)

        simulationDuration = parameters.get(self.SIMULATIONDURATION, 0)
        if simulationDuration == 0:
            self.log.error(ProcessStatus.ERROR, processId,
                                  "No " + self.SIMULATIONDURATION + " parameter provided")
            raise Exception("Missing parameter " + self.SIMULATIONDURATION)

        queryHandler = BlazegraphQueryHandler(bgHost, self.log, processId, username)
        queryHandler.addFeederSelection(modelId)

        dir = os.path.abspath(directory)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fRoot = os.path.join(dir, self.cimhub_PREFIX)

        useHouses = parameters.get(self.USEHOUSES, False)
        useClimate = True

        bHaveEventGen = True

        separatedLoadsFile = parameters.get(self.SEPARATED_LOADS_FILE)
        simulator = parameters.get(self.SIMULATOR)
        if separatedLoadsFile is not None and simulator == "ochre":
            separateLoads = self.getSeparatedLoadNames(separatedLoadsFile)
        elif separatedLoadsFile is None and simulator == "ochre":
            self.log.error(ProcessStatus.ERROR, processId,
                                  "No " + self.SEPARATED_LOADS_FILE + " parameter provided")
            raise Exception("Missing parameter " + self.SEPARATED_LOADS_FILE)

        # CIMHub utility uses
        cimImporter = CIMImporter()
        qs = CIMQuerySetter()
        cimImporter.start(queryHandler, qs, self.CONFIGTARGET, fRoot, scheduleName, loadScale, bWantSched, bWantZip,
                          bWantRandomFractions, useHouses, zFraction, iFraction, pFraction, -1, bHaveEventGen,
                          modelState, False, separateLoads)
        tempDataPath = os.path.abspath(dir)

        # If use climate, then generate GridLAB-D weather data file
        try:
            if useClimate:
                weatherRequest = RequestTimeseriesDataBasic()
                weatherRequest.setQueryMeasurement("weather")
                weatherRequest.setResponseFormat(ProvenWeatherToGridlabdWeatherConverter.OUTPUT_FORMAT)
                queryFilter = {self.STARTTIME_FILTER: str(simulationStartTime * 1000),
                               self.ENDTIME_FILTER: str((simulationStartTime + simulationDuration) * 1000)}
                weatherRequest.setQueryFilter(queryFilter)
                resp = self.dataManager.processDataRequest(weatherRequest,
                                                           ProvenTimeSeriesDataManagerImpl.DATA_MANAGER_TYPE, simId,
                                                           tempDataPath, username)
                if resp.getData() is None:
                    useClimate = False
                    raise Exception("No weather data in time series data store. Setting useClimate = false.")
                else:
                    weatherFile = os.path.join(directory, self.WEATHER_FILENAME)
                    with open(weatherFile, 'wb') as fout:
                        fout.write(resp.getData().encode())
        except json.JSONDecodeError as e:
            self.log.warning(ProcessStatus.RUNNING, processId,
                                 "No weather data was found in proven. Running Simulation without weather data.")
            useClimate = False
        except Exception as e:
            self.log.warning(ProcessStatus.RUNNING, processId, str(e))

        # Generate zip load profile player file
        if scheduleName is not None and len(scheduleName.strip()) > 0:
            ziploadScheduleConfigurationHandler = GLDZiploadScheduleConfigurationHandler(self.log,
                                                                                         self.dataManager)
            ziploadScheduleConfigurationHandler.generateConfig(parameters, None, processId, username)

        # Generate startup file
        startupFile = os.path.join(tempDataPath, self.STARTUP_FILENAME)
        with open(startupFile, 'w') as startupFileWriter:
            self.generateStartupFile(parameters, tempDataPath, startupFileWriter, modelId, processId, username,
                                     useClimate, useHouses)

        # Generate outputs file
        simulationOutputs = open(os.path.join(tempDataPath, self.MEASUREMENTOUTPUTS_FILENAME), 'w')
        simOutputParams = {
            GLDSimulationOutputConfigurationHandler.DICTIONARY_FILE: os.path.join(tempDataPath,
                                                                                  self.DICTIONARY_FILENAME),
            GLDSimulationOutputConfigurationHandler.DIFF_FILE: os.path.join(tempDataPath, self.DIFF_FILENAME),
            GLDSimulationOutputConfigurationHandler.EVENTS_FILE: os.path.join(tempDataPath, self.EVENTS_FILENAME),
            GLDSimulationOutputConfigurationHandler.EVENTS_XML_FILE: os.path.join(tempDataPath,
                                                                                  self.EVENTS_XML_FILENAME),
            GLDSimulationOutputConfigurationHandler.EVENTS_CSV_FILE: os.path.join(tempDataPath,
                                                                                  self.EVENTS_CSV_FILENAME),
            GLDSimulationOutputConfigurationHandler.INTERVALS_FILE: os.path.join(tempDataPath,
                                                                                 self.INTERVALS_FILENAME),
            GLDSimulationOutputConfigurationHandler.MEASUREMENTS_CSV_FILE: os.path.join(tempDataPath,
                                                                                        self.MEASUREMENTS_CSV_FILENAME),
            GLDSimulationOutputConfigurationHandler.MEASUREMENTS_FILE: os.path.join(tempDataPath,
                                                                                    self.MEASUREMENTS_FILENAME),
            GLDSimulationOutputConfigurationHandler.TROUBLESHOOT_FILE: os.path.join(tempDataPath,
                                                                                    self.TROUBLESHOOT_FILENAME),
            GLDSimulationOutputConfigurationHandler.TROUBLESHOOT_CSV_FILE: os.path.join(tempDataPath,
                                                                                        self.TROUBLESHOOT_CSV_FILENAME)
        }

        outputsParams = parameters.get(self.OUTPUTS)
        if outputsParams is not None:
            if GLDConfigManager.KEY_INTERVALS in outputsParams:
                if outputsParams[GLDConfigManager.KEY_INTERVALS]:
                    simulationOutputs.write(GLDSimulationOutputConfigurationHandler.INTERVALS_FILENAME + '\n')
            if GLDConfigManager.KEY_MEASUREMENTS in outputsParams:
                if outputsParams[GLDConfigManager.KEY_MEASUREMENTS]:
                    simulationOutputs.write(GLDSimulationOutputConfigurationHandler.MEASUREMENTS_FILENAME + '\n')
            if GLDConfigManager.KEY_DICTIONARY in outputsParams:
                if outputsParams[GLDConfigManager.KEY_DICTIONARY]:
                    simulationOutputs.write(GLDSimulationOutputConfigurationHandler.DICTIONARY_FILENAME + '\n')
            if GLDConfigManager.KEY_DIFF in outputsParams:
                if outputsParams[GLDConfigManager.KEY_DIFF]:
                    simulationOutputs.write(GLDSimulationOutputConfigurationHandler.DIFF_FILENAME + '\n')
            if GLDConfigManager.KEY_EVENTS in outputsParams:
                if outputsParams[GLDConfigManager.KEY_EVENTS]:
                    simulationOutputs.write(GLDSimulationOutputConfigurationHandler.EVENTS_FILENAME + '\n')
            if GLDConfigManager.KEY_MEASUREMENTS_CSV in outputsParams:
                if outputsParams[GLDConfigManager.KEY_MEASUREMENTS_CSV]:
                    simulationOutputs.write(
                        GLDSimulationOutputConfigurationHandler.MEASUREMENTS_CSV_FILENAME + '\n')
            if GLDConfigManager.KEY_EVENTS_XML in outputsParams:
                if outputsParams[GLDConfigManager.KEY_EVENTS_XML]:
                    simulationOutputs.write(GLDSimulationOutputConfigurationHandler.EVENTS_XML_FILENAME + '\n')
            if GLDConfigManager.KEY_EVENTS_CSV in outputsParams:
                if outputsParams[GLDConfigManager.KEY_EVENTS_CSV]:
                    simulationOutputs.write(GLDSimulationOutputConfigurationHandler.EVENTS_CSV_FILENAME + '\n')
            if GLDConfigManager.KEY_TROUBLESHOOT in outputsParams:
                if outputsParams[GLDConfigManager.KEY_TROUBLESHOOT]:
                    simulationOutputs.write(GLDSimulationOutputConfigurationHandler.TROUBLESHOOT_FILENAME + '\n')
            if GLDConfigManager.KEY_TROUBLESHOOT_CSV in outputsParams:
                if outputsParams[GLDConfigManager.KEY_TROUBLESHOOT_CSV]:
                    simulationOutputs.write(
                        GLDSimulationOutputConfigurationHandler.TROUBLESHOOT_CSV_FILENAME + '\n')
        simulationOutputs.close()

        # Generate playback file
        playbackFile = os.path.join(tempDataPath, self.PLAYBACK_FILENAME)
        playbackFileWriter = open(playbackFile, 'w')
        playbackFileWriter.write(self.PLAYBACK_START_DATE + ' ' + self.PLAYBACK_START_TIME + '\n')

        playbackFileWriter.write(self.PLAYBACK_END_DATE + ' ' + self.PLAYBACK_END_TIME + '\n')

        self.addSimulationStartTime(parameters, playbackFileWriter)
        playbackFileWriter.close()

        # Store GridLAB-D command line
        commandLine = "gridlabd " + self.CONFIGTARGET + " " + fRoot
        if scheduleName is not None and len(scheduleName.strip()) > 0:
            commandLine += " " + GLDZiploadScheduleConfigurationHandler.CONFIGTARGET + " " + fRoot
        commandLine += " " + self.STARTUP_FILENAME
        commandLine += " " + self.PLAYBACK_FILENAME
        commandLine += " " + self.MEASUREMENTOUTPUTS_FILENAME
        commandLine += " --heartbeat 120"

        configCommandFile = os.path.join(tempDataPath, self.CONFIGCOMMAND_FILENAME)
        with open(configCommandFile, 'w') as configCommandFileWriter:
            configCommandFileWriter.write(commandLine)

        # Write the parameters to a JSON file for reference
        configParametersFile = os.path.join(tempDataPath, self.PARAMETERS_FILENAME)
        with open(configParametersFile, 'w') as configParametersFileWriter:
            configParametersFileWriter.write(json.dumps(parameters, indent=4))

        self.log.info(ProcessStatus.COMPLETED, processId,
                             "GridLAB-D configuration files generated successfully for Model ID: " + modelId + ", Simulation ID: " + simId)


    def generateStartupFile(self, parameters, tempDataPath, startupFileWriter, modelId, processId, username, useClimate,
                            useHouses):
        # Generate the startup file content
        startupContent = ""

        startupContent += "// GridLAB-D startup file generated by GLDAllConfigurationHandler\n\n"

        startupContent += "#set profiler=1\n"
        startupContent += "#set clock=" + str(parameters.get(self.SIMULATIONDURATION)) + "status\n"

        if useClimate:
            startupContent += "#set weather_file=" + os.path.join(tempDataPath, self.WEATHER_FILENAME) + "\n"

        startupContent += "#set starttime=" + str(parameters.get(self.SIMULATIONSTARTTIME)) + "status\n"

        startupContent += "#set object class=triplex_meter\n"
        startupContent += "#set randomize=0.0\n"

        if useHouses:
            startupContent += "#set object class=house\n"
            startupContent += "#set use_actual_house=1\n"
            startupContent += "#set object class=house_meter\n"

        startupContent += "#set object class=tape\n"
        startupContent += "#set object class=player\n"
        startupContent += "#set object class=substation\n"
        startupContent += "#set object class=overhead_line\n"
        startupContent += "#set object class=fuse\n"
        startupContent += "#set object class=triplex_line\n"
        startupContent += "#set object class=triplex_node\n"
        startupContent += "#set object class=triplex_load\n"

        # Write the startup file content to the provided writer
        startupFileWriter.write(startupContent)

        self.log.info(ProcessStatus.RUNNING, processId,
                             "GridLAB-D startup file generated successfully for Model ID: " + modelId)

    def getSeparatedLoadNames(self, fileName):
        loadNames = []

        try:
            workbook = openpyxl.load_workbook(fileName)
            sheet = workbook.active  # Assuming the first sheet is the one of interest

            for row in sheet.iter_rows(min_row=2, values_only=True):
                load_name = row[5]  # Assuming the load name is in the sixth column (index 5)
                loadNames.append(load_name)

        except Exception as e:
            print("Error reading Excel file:", str(e))

        return loadNames
