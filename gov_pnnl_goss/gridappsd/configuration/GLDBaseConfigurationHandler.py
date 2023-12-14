# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
# gld_base_configuration_handler.py
from gov_pnnl_goss.SpecialClasses import File
from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
from gov_pnnl_goss.cimhub.CIMQuerySetter import CIMQuerySetter
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.configuration.BaseConfigurationHandler import BaseConfigurationHandler
from gov_pnnl_goss.gridappsd.api import ConfigurationHandler, DataManager, SimulationManager, PowergridModelDataManager
from gov_pnnl_goss.gridappsd.configuration.CIMDictionaryConfigurationHandler import PrintWriter, FileWriter
from gov_pnnl_goss.gridappsd.configuration.GLDAllConfigurationHandler import GLDAllConfigurationHandler
from gov_pnnl_goss.gridappsd.data.handlers.BlazegraphQueryHandler import BlazegraphQueryHandler
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.utils import GridAppsDConstants
import logging


class GLDBaseConfigurationHandler(BaseConfigurationHandler, ConfigurationHandler):
    TYPENAME = "GridLAB-D Base GLM"
    ZFRACTION = "z_fraction"
    IFRACTION = "i_fraction"
    PFRACTION = "p_fraction"
    SCHEDULENAME = "schedule_name"
    LOADSCALINGFACTOR = "load_scaling_factor"
    MODELID = "model_id"
    SIMULATIONID = "simulation_id"
    USEHOUSES = "use_houses"
    def __init__(self, log_manager: LogManager, data_manager: DataManager):
        super().__init__(log_manager, data_manager)
        self.log = LogManager(GLDBaseConfigurationHandler.__name__)

        self.client = None
        self.logger = log_manager
        self.config_manager = None
        self.simulation_manager = None
        self.powergrid_model_manager = None

    def start(self):
        if self.config_manager is not None:
            self.config_manager.registerConfigurationHandler(self.TYPENAME, self)
        else:
            self.log.warning("No Config manager available for " + self.getClass())

        if self.powergrid_model_manager is None:
            #TODO send log message and exception
            pass
            
    def generate_config(self, parameters, output_file, process_id, username):
        self.log.info(ProcessStatus.RUNNING, process_id,
                      "Generating Base GridLAB-D configuration file using parameters: "+str(parameters))

        simulationId = GridAppsDConstants.getStringProperty(parameters, self.SIMULATIONID, None)
        configFile = None

        if simulationId is not None:
            simulationContext = self.simulation_manager.getSimulationContextForId(simulationId)
            if simulationContext is not None:
                configFile = File(simulationContext.getSimulationDir() + File.separator +
                                  GLDAllConfigurationHandler.BASE_FILENAME)
                if configFile.exists():
                    self.print_file_to_output(configFile, output_file)
                    self.log.info(ProcessStatus.RUNNING, process_id,
                                  "Dictionary GridLAB-D base file for simulation " + simulationId + " already exists.")
                    return
            else:
                self.log.warn(ProcessStatus.RUNNING, process_id,
                              "No simulation context found for simulation_id: ")
                
        bWantZip = False
        bWantSched = False
        zFraction = GridAppsDConstants.getDoubleProperty(parameters, self.ZFRACTION, 0)
        if zFraction == 0:
            zFraction = 0
            bWantZip = True
            
        iFraction = GridAppsDConstants.getDoubleProperty(parameters, self.IFRACTION, 0)
        if iFraction == 0:
            iFraction = 1
            bWantZip = True

        pFraction = GridAppsDConstants.getDoubleProperty(parameters, self.PFRACTION, 0)
        if pFraction == 0:
            pFraction = 0
            bWantZip = True

        bWantRandomFractions = GridAppsDConstants.getBooleanProperty(parameters,
                                                                     GLDAllConfigurationHandler.RANDOMIZEFRACTIONS,
                                                                     False)
        loadScale = GridAppsDConstants.getDoubleProperty(parameters, self.LOADSCALINGFACTOR, 1)
        scheduleName = GridAppsDConstants.getStringProperty(parameters, self.SCHEDULENAME, None)

        if scheduleName is not None and scheduleName.strip():
            bWantSched = True

        modelId = GridAppsDConstants.getStringProperty(parameters, self.MODELID, None)
        
        if modelId is None or not modelId.strip():
            raise Exception("Missing parameter " + self.MODELID)

        bgHost = self.config_manager.getConfigurationProperty(GridAppsDConstants.BLAZEGRAPH_HOST_PATH)

        if bgHost is None or not bgHost.strip():
            bgHost = BlazegraphQueryHandler.DEFAULT_ENDPOINT

        queryHandler = BlazegraphQueryHandler(bgHost, self.log, process_id, username)
        queryHandler.addFeederSelection(modelId)

        useHouses = GridAppsDConstants.getBooleanProperty(parameters, self.USEHOUSES, False)

        bHaveEventGen = True
        cimImporter = CIMImporter()
        qs = CIMQuerySetter()

        if configFile is not None:
            cimImporter.generateGLMFile(queryHandler, qs, PrintWriter(FileWriter(configFile)),
                                        scheduleName, loadScale, bWantSched, bWantZip, bWantRandomFractions,
                                        useHouses, zFraction, iFraction, pFraction, bHaveEventGen)
        else:
            cimImporter.generateGLMFile(queryHandler, qs, output_file, scheduleName, loadScale, bWantSched,
                                        bWantZip, bWantRandomFractions, useHouses, zFraction, iFraction,
                                        pFraction, bHaveEventGen)

        if configFile is not None:
            self.print_file_to_output(configFile, output_file)

        self.log.info(ProcessStatus.RUNNING, process_id, "Finished generating Base GridLAB-D configuration file.")
