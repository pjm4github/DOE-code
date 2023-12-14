# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import io
import logging
import time
from datetime import datetime
import json


from gov_pnnl_goss.SpecialClasses import UsernamePasswordCredentials, Gson
from gov_pnnl_goss.core.ClientFactory import ClientFactory
from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.core.GossResponseEvent import GossResponseEvent
from gov_pnnl_goss.core.client.GossClient import Protocol
from gov_pnnl_goss.core.security.SecurityConfig import SecurityConfig
from gov_pnnl_goss.gridappsd.api.AppManager import AppManager
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.DataManagerHandler import DataManagerHandler
from gov_pnnl_goss.gridappsd.api.ServiceManager import ServiceManager
from gov_pnnl_goss.gridappsd.api.SimulationManager import SimulationManager
from gov_pnnl_goss.gridappsd.api.TimeseriesDataManager import TimeseriesDataManager
from gov_pnnl_goss.gridappsd.dto.RequestTimeseriesData import RequestTimeseriesData

from gov_pnnl_goss.gridappsd.dto.SimulationContext import SimulationContext
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.dto.RequestTimeseriesDataAdvanced import RequestTimeseriesDataAdvanced
from gov_pnnl_goss.gridappsd.dto.RequestTimeseriesDataBasic import RequestTimeseriesDataBasic
from gov_pnnl_goss.gridappsd.dto.TimeSeriesEntryResult import TimeSeriesEntryResult
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


# import gov.pnnl.proven.api.producer.ProvenResponse; This is missing
class ProvenProducer:
    def __init__(self):
        pass
    def rest_producer(self, *args):
        pass
    def set_message_info(self, *args):
        pass
    def get_advanced_ts_query(self, *args):
        pass
    def send_message(self, *args):
        pass
    def send_bulk_message(self, *args):
        pass


class ProvenTimeSeriesDataManagerImpl(TimeseriesDataManager, DataManagerHandler):

    DATA_MANAGER_TYPE = "timeseries"
    
    def __init__(self):
        self.keywords = []
        self.request_id = ""
        self.proven_uri = ""
        self.proven_query_uri = ""
        self.proven_advanced_query_uri = ""
        self.proven_write_uri = ""
        self.proven_query_producer = ProvenProducer()
        self.proven_write_producer = ProvenProducer()
        self.gson = Gson()
        self.count = 0
        self.log = LogManager(ProvenTimeSeriesDataManagerImpl.__name__)
        self.logger = self.log
        self.data_manager = DataManager()
        self.client_factory = ClientFactory()
        self.config_manager = ConfigurationManager()
        self.simulation_manager = SimulationManager()
        self.service_manager = ServiceManager()
        self.app_manager = AppManager()
        self.security_config = SecurityConfig()

        #  #  credentials = UsernamePasswordCredentials(GridAppsDConstants.username, GridAppsDConstants.password)

    def start(self):
        self.logger.debug(ProcessStatus.RUNNING, None, "Starting " + self.__class__.__name__)
        self.data_manager.register_data_manager_handler(self, self.DATA_MANAGER_TYPE)
        self.proven_uri = self.config_manager.get_configuration_property(GridAppsDConstants.PROVEN_PATH)
        self.proven_write_uri = self.config_manager.get_configuration_property(GridAppsDConstants.PROVEN_WRITE_PATH)
        self.proven_query_uri = self.config_manager.get_configuration_property(GridAppsDConstants.PROVEN_QUERY_PATH)
        self.proven_advanced_query_uri = self.config_manager.get_configuration_property(GridAppsDConstants.PROVEN_ADVANCED_QUERY_PATH)
        self.proven_query_producer.rest_producer(self.proven_query_uri, None, None)
        self.proven_write_producer.rest_producer(self.proven_write_uri, None, None)
        try:
            self.subscribe_and_store_data_from_topic("/topic/goss.gridappsd.*.output", None, None, None)
        except Exception as e:
            print(e)

    def handle(self, request_content, process_id, username):
        if isinstance(request_content, SimulationContext):
            self.store_all_data(request_content)
        if isinstance(request_content, RequestTimeseriesData):
            return self.query(request_content)
        elif isinstance(request_content, str):
            time_series_request = None
            try:
                time_series_request = RequestTimeseriesDataAdvanced.parse(request_content)
            except Exception:
                try:
                    time_series_request = RequestTimeseriesDataBasic.parse(request_content)
                except Exception as e:
                    raise Exception("Failed to parse time series data request")
            return self.query(time_series_request)

    def query(self, request_timeseries_data):
        response = None

        if isinstance(request_timeseries_data, RequestTimeseriesDataAdvanced):
            self.proven_query_producer.rest_producer(self.proven_advanced_query_uri, None, None)
            self.proven_query_producer.set_message_info("GridAPPSD", "QUERY", self.__class__.__name__, self.keywords)
            response = self.proven_query_producer.get_advanced_ts_query(str(request_timeseries_data), self.request_id)
        else:
            self.proven_query_producer.rest_producer(self.proven_query_uri, None, None)
            self.proven_query_producer.set_message_info("GridAPPSD", "QUERY", self.__class__.__name__, self.keywords)
            response = self.proven_query_producer.send_message(request_timeseries_data.to_string(), self.request_id)

        result = TimeSeriesEntryResult.parse(str(response.data))

        if len(result.get_data()) == 0:
            return None

        orig_format = "PROVEN_" + request_timeseries_data.get_query_measurement().to_string()

        if request_timeseries_data.get_original_format() is not None:
            orig_format = "PROVEN_" + request_timeseries_data.get_original_format().to_string()

        response_format = request_timeseries_data.get_response_format()
        converter = DataManager.get_converter(orig_format, response_format)

        if converter is not None:
            sw = io.StringIO()
            converter.convert(str(response.data), io.StringIO(sw), request_timeseries_data)
            return sw.getvalue()

        return str(response.data)

    def store_all_data(self, simulation_context):
        simulation_id = simulation_context.get_simulation_id()
        self.store_simulation_input(simulation_id)
        self.store_simulation_output(simulation_id)
        for instance_id in simulation_context.get_service_instance_ids():
            service_id = self.service_manager.get_service_id_for_instance(instance_id)
            self.store_service_input(simulation_id, service_id, instance_id)
            self.store_service_output(simulation_id, service_id, instance_id)
        for instance_id in simulation_context.get_app_instance_ids():
            app_id = self.app_manager.get_app_id_for_instance(instance_id)
            self.store_app_input(simulation_id, app_id, instance_id)
            self.store_app_output(simulation_id, app_id, instance_id)

    def on_message(self, message, instance_id, simulation_id ):
        event = DataResponse(message)

        for str_value in event.get_destination().split("."):
            print(str_value)

        try:
            # TODO: Remove if block once changes are made to get measurement name from datatype
            app_or_service_id = event.get_destination().split(".")[2]

            if app_or_service_id is None:
                data = json.loads(event.get_data().toString())
                if isinstance(data, dict) and "datatype" in data:
                    datatype = data["datatype"]
                    if datatype is not None:
                        self.proven_write_producer.send_bulk_message(event.get_data().toString(), datatype, instance_id,
                                                                     simulation_id, int(time.time() * 1000))
            else:
                self.proven_write_producer.send_bulk_message(event.get_data().toString(), app_or_service_id, instance_id,
                                                        simulation_id, int(time.time() * 1000))

        except Exception as e:
            import traceback

            s_stack_trace = traceback.format_exc()
            print(s_stack_trace)
            self.log.error(ProcessStatus.RUNNING, None,
                              f"Error storing timeseries data for message at {event.get_destination()}: {s_stack_trace}")

    def subscribe_and_store_data_from_topic(self, topic, app_or_service_id, instance_id, simulation_id):
        credentials = UsernamePasswordCredentials(self.security_config.get_manager_user(), self.security_config.get_manager_password())
        input_client = self.client_factory.create(Protocol.STOMP, credentials, True)
        input_client.subscribe(topic, GossResponseEvent(),
                               lambda message: self.on_message(message, instance_id, simulation_id ))

    def store_simulation_output(self, simulation_id):
        self.subscribe_and_store_data_from_topic("/topic/" + GridAppsDConstants.topic_simulation + ".output."
                                                 + simulation_id, "simulation", None, simulation_id)

    def store_simulation_input(self, simulation_id):
        self.subscribe_and_store_data_from_topic("/topic/" + GridAppsDConstants.topic_simulation + ".input." +
                                                 simulation_id, "simulation", None, simulation_id)

    def store_service_output(self, simulation_id, service_id, instance_id):
        self.subscribe_and_store_data_from_topic("/topic/" + GridAppsDConstants.topic_simulation + "." +
                                                 service_id + "." + simulation_id + ".output",
                                                 service_id, instance_id, simulation_id)

    def store_service_input(self, simulation_id, service_id, instance_id):
        self.subscribe_and_store_data_from_topic("/topic/" + GridAppsDConstants.topic_simulation + "." +
                                                 service_id + "." + simulation_id + ".input",
                                                 service_id, instance_id, simulation_id)

    def store_app_output(self, simulation_id, app_id, instance_id):
        self.subscribe_and_store_data_from_topic("/topic/" + GridAppsDConstants.topic_simulation + "." + app_id +
                                                 "." + simulation_id + ".output", app_id, instance_id, simulation_id)

    def store_app_input(self, simulation_id, app_id, instance_id):
        self.subscribe_and_store_data_from_topic("/topic/" + GridAppsDConstants.topic_simulation + "." + app_id +
                                                 "." + simulation_id + ".input", app_id, instance_id, simulation_id)
