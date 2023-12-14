# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import logging
from collections import defaultdict

from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager


class DataManagerImpl(DataManager):
    def __init__(self, client_factory, log_manager):
        self.handlers = defaultdict(list)
        self.data_managers = {}
        self.data_converters = {}
        self.log = LogManager(type(self).__name__)
        self.client = None
        self.client_factory = client_factory
        self.logger = log_manager

    def start(self):
        self.log.info("Starting " + type(self).__name__)
        self.register_data_manager_handler(self.logger.get_log_data_manager(), "logDataManagerMySQL")
        # try:
        # 	credentials = UsernamePasswordCredentials(
        # 			GridAppsDConstants.username, GridAppsDConstants.password)
        # 	client = client_factory.create(PROTOCOL.STOMP,credentials)
        #
        # 	client.subscribe(GridAppsDConstants.topic_requestData, new DataEvent(this))
        #
        # except Exception as e:
        # 		print(e)

    def register_handler(self, handler, request_class):
        self.log.info("Data Manager Registration: " + str(type(handler)) + " - " + str(request_class))
        self.handlers[request_class].append(handler)

    def register_data_manager_handler(self, handler, name):
        self.log.info("Data Manager Handler Registration: " + str(type(handler)) + " - " + name)
        self.data_managers[name] = handler

    def process_data_request(self, request, type, simulation_id, temp_data_path, username):
        if request and type:
            response_data = None
            if type in self.data_managers:
                response_data = self.data_managers[type].handle(request, str(simulation_id), username)
            else:
                print("TYPE NOT SUPPORTED")
                # TODO: throw error that type not supported

            data_response = DataResponse()
            data_response.set_data(response_data)
            data_response.set_response_complete(True)
            return data_response
        # TODO this will be phased out

        # self.handlers = self.get_handlers(request.getClass())
        # if self.handlers:
        # 	# iterate through all handlers until we get one with a result
        # 	for handler in self.handlers:
        # 		# datahandler.handle
        # 		r = handler.handle(request, simulationId, tempDataPath, self.logger)
        # 		if r:
        # 			return r
        # 		# Return result from handler
        # # return null if no valid results
        # return None

    def get_handlers(self, request_class):
        if request_class in self.handlers:
            self.log.debug("Data handler " + self.handlers.get(request_class) + " found for " + request_class)
            return self.handlers.get(request_class)
        self.log.warning("No data handler found for request type " + request_class);
        return None
        # return self.handlers.get(request_class)

    def get_all_handlers(self):
        return [handler for handlers in self.handlers.values() for handler in handlers]

    def get_handler(self, request_class, handler_class):
        return None

    def register_converter(self, input_format, output_format, converter):
        converter_key = (input_format + ':' + output_format).upper()
        self.data_converters[converter_key] = converter

    def get_converter(self, input_format, output_format):
        converter_key = (input_format + ':' + output_format).upper()
        if converter_key in self.data_converters:
            return self.data_converters[converter_key]
        else:
            self.log.warning("No Data converter available for " + input_format + " to " + output_format)
            return None
