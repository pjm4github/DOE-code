import json
import datetime
from typing import List


class GridAppsDConstants:
    # Topics
    topic_prefix = "goss.gridappsd"

    # Process Manager topics
    topic_process_prefix = f"{topic_prefix}.process"
    topic_request = f"{topic_prefix}.process"

    # Process Manager Request Topics
    topic_requestSimulation = f"{topic_process_prefix}.request.simulation"
    topic_requestData = f"{topic_process_prefix}.request.data"
    topic_requestConfig = f"{topic_process_prefix}.request.config"
    topic_requestApp = f"{topic_process_prefix}.request.app"
    topic_app_register_remote = f"{topic_requestApp}.remote.register"
    topic_requestSimulationStatus = f"{topic_process_prefix}.request.status.simulation"
    topic_requestPlatformStatus = f"{topic_process_prefix}.request.status.platform"
    topic_requestMyRoles = f"{topic_process_prefix}.request.roles"
    topic_requestField = f"{topic_process_prefix}.request.field"

    # Remote Application topics
    topic_remoteapp_prefix = f"{topic_prefix}.remoteapp"
    topic_remoteapp_heartbeat = f"{topic_remoteapp_prefix}.heartbeat"
    topic_remoteapp_start = f"{topic_remoteapp_prefix}.start"
    topic_remoteapp_stop = f"{topic_remoteapp_prefix}.stop"
    topic_remoteapp_status = f"{topic_remoteapp_prefix}.status"

    topic_requestListAppsWithInstances = "goss.gridappsd.process.request.list.apps"
    topic_requestListServicesWithInstances = "goss.gridappsd.process.request.list.services"

    topic_responseData = f"{topic_prefix}.response.data"

    topic_platformLog = f"{topic_prefix}.platform.log"

    # Field Request Topics
    topic_requestFieldContext = f"{topic_process_prefix}.request.field.context"

    # App Request Topics
    topic_app_register = f"{topic_requestApp}.register"
    topic_app_list = f"{topic_requestApp}.list"
    topic_app_get = f"{topic_requestApp}.get"
    topic_app_deregister = f"{topic_requestApp}.deregister"
    topic_app_start = f"{topic_requestApp}.start"
    topic_app_stop = f"{topic_requestApp}.stop"
    topic_app_stop_instance = f"{topic_requestApp}.stopinstance"

    # Configuration Manager topics
    topic_configuration = f"{topic_prefix}.configuration"
    topic_configuration_powergrid = f"{topic_configuration}.powergrid"
    topic_configuration_simulation = f"{topic_configuration}.simulation"

    # Simulation Topics
    topic_simulation = f"{topic_prefix}.simulation"
    topic_simulationInput = f"{topic_simulation}.input"
    topic_simulationOutput = f"/topic/{topic_simulation}.output"
    topic_simulationLog = f"{topic_simulation}.log."
    topic_simulationTestOutput = f"{topic_simulation}.test.output."
    topic_simulationTestInput = f"/topic/{topic_simulation}.test.input."

    # Service Topics
    topic_service = f"{topic_prefix}.simulation"
    topic_serviceInput = f"{topic_service}.input"
    topic_serviceOutput = f"{topic_service}.output"
    topic_serviceLog = f"{topic_service}.log"

    # Application Topics
    topic_application = f"{topic_prefix}.simulation"
    topic_applicationInput = f"{topic_application}.input"
    topic_applicationOutput = f"{topic_application}.output"
    topic_applicationLog = f"{topic_application}.log"

    # Test topics
    topic_test = f"{topic_prefix}.test"
    topic_testInput = f"{topic_test}.input"
    topic_testOutput = f"{topic_test}.output"
    topic_testLog = f"{topic_test}.log"

    # Data Manager Topics
    topic_getDataFilesLocation = f"{topic_prefix}.data.filesLocation"
    topic_getDataContent = f"{topic_prefix}.data.content"

    # GOSS Bridge Topics
    topic_COSIM = f"{topic_prefix}.cosim"
    topic_COSIM_input = f"{topic_COSIM}.input"
    topic_COSIM_output = f"{topic_COSIM}.output"
    topic_COSIM_timestamp = f"{topic_COSIM}.timestamp"

    FNCS_PATH = "fncs.path"
    FNCS_BRIDGE_PATH = "fncs.bridge.path"
    VVO_APP_PATH = "vvo.app.path"
    GRIDLABD_PATH = "gridlabd.path"
    GRIDAPPSD_TEMP_PATH = "gridappsd.temp.path"
    APPLICATIONS_PATH = "applications.path"
    SERVICES_PATH = "services.path"
    GRIDLABD_INTERFACE = "gridlabd.interface"
    GRIDLABD_INTERFACE_HELICS = "helics"
    GRIDLABD_INTERFACE_FNCS = "fncs"

    BLAZEGRAPH_HOST_PATH = "blazegraph.host.path"
    BLAZEGRAPH_NS_PATH = "blazegraph.ns.path"
    PROVEN_PATH = "proven.path"
    PROVEN_WRITE_PATH = "proven.write.path"
    PROVEN_QUERY_PATH = "proven.query.path"
    PROVEN_ADVANCED_QUERY_PATH = "proven.advanced_query.path"

    # SDF_SIMULATION_REQUEST = datetime.datetime.strptime("MM/dd/yyyy HH:mm:ss", "%mm/%dd/%Y %H:%M:%S")
    SDF_SIMULATION_REQUEST = datetime.datetime.now().strftime("%multiplicities/%d/%Y %H:%M:%S")
    #SDF_GLM_CLOCK = datetime.datetime.strptime("yyyy-MM-dd HH:mm:ss", "%Y-%multiplicities-%d %H:%M:%S")
    SDF_GLM_CLOCK = datetime.datetime.now().strftime("%Y-%multiplicities-%d %H:%M:%S")

    #GRIDAPPSD_DATE_FORMAT = datetime.datetime.strptime("yyyy-MM-dd HH:mm:ss", "%Y-%multiplicities-%d %H:%M:%S")
    GRIDAPPSD_DATE_FORMAT = datetime.datetime.now().strftime("%Y-%multiplicities-%d %H:%M:%S")

    @staticmethod
    def getDoubleProperty(props, keyName, defaultValue):
        if keyName in props:
            val = props[keyName]
            if val is not None:
                return float(val)
        return defaultValue

    @staticmethod
    def getBooleanProperty(props, keyName, defaultValue):
        if keyName in props:
            val = props[keyName]
            if val is not None:
                return bool(val)
        return defaultValue

    @staticmethod
    def getStringProperty(props, keyName, defaultValue):
        if keyName in props:
            val = props[keyName]
            if val is not None:
                return str(val)
        return defaultValue

    @staticmethod
    def getLongProperty(props, keyName, defaultValue):
        if keyName in props:
            val = props[keyName]
            if val is not None:
                return int(val)
        return defaultValue

    @staticmethod
    def getGLDInterface(dependencies):
        for dep in dependencies:
            if GridAppsDConstants.GRIDLABD_INTERFACE_FNCS.lower() == dep.strip().lower():
                return GridAppsDConstants.GRIDLABD_INTERFACE_FNCS
            elif GridAppsDConstants.GRIDLABD_INTERFACE_HELICS.lower() == dep.strip().lower():
                return GridAppsDConstants.GRIDLABD_INTERFACE_HELICS
        return GridAppsDConstants.GRIDLABD_INTERFACE_FNCS
