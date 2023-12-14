import os
import json

from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
from gov_pnnl_goss.cimhub.CIMQuerySetter import CIMQuerySetter
from gov_pnnl_goss.cimhub.dto.ModelState import ModelState
from gov_pnnl_goss.gridappsd.data.handlers import BlazegraphQueryHandler
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.utils import GridAppsDConstants


class DSSAllConfigurationHandler:
    TYPENAME = "DSS All"
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
    CONFIGTARGET = "dss"
    CIM2DSS_PREFIX = "model"

    def __init__(self, logManager, simulationManager, configManager):
        self.logger = logManager
        self.simulation_manager = simulationManager
        self.config_manager = configManager
        self.powergrid_model_manager = None  # PowergridModelDataManager()

    def start(self):
        if self.config_manager is not None:
            self.config_manager.registerConfigurationHandler(DSSAllConfigurationHandler.TYPENAME, self)
        else:
            # TODO: Send log message and exception
            self.logger.warn("No Config manager available for " + str(self.__class__))

        if self.powergrid_model_manager is None:
            # TODO: Send log message and exception
            pass

    def generate_config(self, parameters, out, processId, username):
        bWantZip = False
        bWantSched = False
        simContext = None

        self.logger.info(ProcessStatus.RUNNING, processId, f"Generating all DSS configuration files using parameters: {parameters}")

        zFraction = parameters.get(self.ZFRACTION, 0)
        if zFraction == 0:
            zFraction = 0
            bWantZip = True

        iFraction = parameters.get(self.IFRACTION, 0)
        if iFraction == 0:
            iFraction = 1
            bWantZip = True

        pFraction = parameters.get(self.PFRACTION, 0)
        if pFraction == 0:
            pFraction = 0
            bWantZip = True

        bWantRandomFractions = parameters.get(self.RANDOMIZEFRACTIONS, False)
        loadScale = parameters.get(self.LOADSCALINGFACTOR, 1)
        scheduleName = parameters.get(self.SCHEDULENAME, None)

        if scheduleName and scheduleName.strip():
            bWantSched = True

        directory = parameters.get(self.DIRECTORY, None)

        if not directory or not directory.strip():
            self.logger.error(ProcessStatus.ERROR, processId, f"No {self.DIRECTORY} parameter provided")
            raise Exception(f"Missing parameter {self.DIRECTORY}")

        modelId = parameters.get(self.MODELID, None)

        if not modelId or not modelId.strip():
            self.logger.error(ProcessStatus.ERROR, processId, f"No {self.MODELID} parameter provided")
            raise Exception(f"Missing parameter {self.MODELID}")

        bgHost = self.config_manager.getConfigurationProperty(GridAppsDConstants.BLAZEGRAPH_HOST_PATH)

        if not bgHost or not bgHost.strip():
            bgHost = BlazegraphQueryHandler.DEFAULT_ENDPOINT

        modelStateStr = parameters.get(self.MODELSTATE, None)
        modelState = ModelState()

        if modelStateStr and modelStateStr.strip():
            modelState = json.loads(modelStateStr)

        queryHandler = BlazegraphQueryHandler(bgHost, self.logger, processId, username)
        queryHandler.addFeederSelection(modelId)

        dir = os.path.abspath(directory)

        if not os.path.exists(dir):
            os.makedirs(dir)

        fRoot = os.path.join(dir, self.CIM2DSS_PREFIX)
        useHouses = parameters.get(self.USEHOUSES, False)
        bHaveEventGen = True

        # TODO: Add climate

        # CIMHub utility uses
        cimImporter = CIMImporter()
        qs = CIMQuerySetter()
        cimImporter.start(queryHandler, qs, self.CONFIGTARGET, fRoot, scheduleName, loadScale, bWantSched, bWantZip,
                          bWantRandomFractions, useHouses, zFraction, iFraction, pFraction, bHaveEventGen, modelState,
                          False)

        self.logger.info(ProcessStatus.RUNNING, processId, "Finished generating all DSS configuration files.")
