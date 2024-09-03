# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.DataManagerHandler import DataManagerHandler
from gov_pnnl_goss.gridappsd.api.PowergridModelDataManager import ResultFormat, PowergridModelDataManager
from gov_pnnl_goss.gridappsd.dto.PowergridModelDataRequest import PowergridModelDataRequest


class BGPowergridModelDataManagerHandlerImpl(DataManagerHandler):

    def __init__(self, data_manager: PowergridModelDataManager):
        self.data_manager = data_manager

    def handle(self, request_content, process_id, username):

        if isinstance(request_content, PowergridModelDataRequest):
            pg_data_request = request_content
        else:
            pg_data_request = PowergridModelDataRequest.parse(request_content)
        # A
        if pg_data_request.request_type == PowergridModelDataRequest.RequestType.QUERY:
            if pg_data_request.query_string is None or not self.verify_result_format(pg_data_request.result_format):
                # TODO: send error
                pass
            return self.data_manager.query(
                pg_data_request.model_id, pg_data_request.query_string, pg_data_request.result_format, process_id, username)
        # B
        elif pg_data_request.request_type == PowergridModelDataRequest.RequestType.QUERY_MODEL:
            if pg_data_request.model_id is None or not self.verify_result_format(pg_data_request.result_format):
                # TODO: send error
                pass
            return self.data_manager.query_model(
                pg_data_request.model_id, pg_data_request.object_type, pg_data_request.filter,
                pg_data_request.result_format, process_id, username)
        # C
        elif pg_data_request.request_type == PowergridModelDataRequest.RequestType.QUERY_MODEL_NAMES:
            if not self.verify_result_format(pg_data_request.result_format):
                # TODO: send error
                pass
            return self.data_manager.query_model_names(pg_data_request.result_format, process_id, username)
        # D
        elif pg_data_request.request_type == PowergridModelDataRequest.RequestType.QUERY_MODEL_INFO:
            if not self.verify_result_format(pg_data_request.result_format):
                # TODO: send error
                pass
            return self.data_manager.query_model_names_and_ids(pg_data_request.result_format, process_id, username)
        # E
        elif pg_data_request.request_type == PowergridModelDataRequest.RequestType.QUERY_OBJECT:
            if (pg_data_request.model_id is None or pg_data_request.object_id is None
                    or not self.verify_result_format(pg_data_request.result_format)):
                # TODO: send error
                pass
            return self.data_manager.query_object(
                pg_data_request.model_id, pg_data_request.object_id, pg_data_request.result_format, process_id, username)
        # F
        elif pg_data_request.request_type == PowergridModelDataRequest.RequestType.QUERY_OBJECT_TYPES:
            if pg_data_request.model_id is None or not self.verify_result_format(pg_data_request.result_format):
                # TODO: send error
                pass
            return self.data_manager.query_object_types(
                pg_data_request.model_id, pg_data_request.result_format, process_id, username)
        # G
        elif pg_data_request.request_type == PowergridModelDataRequest.RequestType.QUERY_OBJECT_IDS:
            if pg_data_request.model_id is None or not self.verify_result_format(pg_data_request.result_format):
                # TODO: send error
                pass
            return self.data_manager.query_object_ids(
                pg_data_request.result_format, pg_data_request.model_id, pg_data_request.object_type, process_id, username)
        # H
        elif pg_data_request.request_type == PowergridModelDataRequest.RequestType.QUERY_OBJECT_DICT:
            if (pg_data_request.model_id is None or not self.verify_result_format(pg_data_request.result_format)
                    or pg_data_request.object_id is None):
                # TODO: send error
                pass
            return self.data_manager.query_object_dict_by_type(
                pg_data_request.result_format, pg_data_request.model_id, pg_data_request.object_type,
                pg_data_request.object_id, process_id, username)
        # I
        elif pg_data_request.request_type == PowergridModelDataRequest.RequestType.QUERY_OBJECT_MEASUREMENTS:
            if (pg_data_request.model_id is None or not self.verify_result_format(pg_data_request.result_format)
                    or pg_data_request.object_id is None):
                # TODO: send error
                pass
            return self.data_manager.query_measurement_dict_by_object(
                pg_data_request.result_format, pg_data_request.model_id, pg_data_request.object_type,
                pg_data_request.object_id, process_id, username)
        # J
        else:
            # TODO: report error, request global_property_types not recognized
            print(f"DOESNT RECOGNIZE REQUEST TYPE {pg_data_request.request_type}")

        return None

    def verify_result_format(self, result_format: ResultFormat)->bool:
        return result_format is not None and (result_format == ResultFormat.JSON
                                              or result_format == ResultFormat.XML)
