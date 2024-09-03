from gov_pnnl_goss.SpecialClasses import UsernamePasswordCredentials
from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.core.Response import RESPONSE_FORMAT
from gov_pnnl_goss.core.client.ClientServiceFactory import ClientServiceFactory
from gov_pnnl_goss.core.client.GossClient import Protocol
from gov_pnnl_goss.gridappsd.dto.PowergridModelDataRequest import PowergridModelDataRequest
from gov_pnnl_goss.gridappsd.test.TestConstants import TestConstants


class BGPGModelManagerTest:
    
    def __init__(self):
        self.client = None
    
    @staticmethod
    def main(args):
        tester = BGPGModelManagerTest()
        tester.test_query_model_info()
        print(0)
    
    def test_query(self):
        try:
            pg_data_request = PowergridModelDataRequest()
            # query_string = "SELECT ?feeder ?fid  WHERE {" \
            # 		+ "?status r:global_property_types c:Feeder." \
            # 		+ "?status c:IdentifiedObject.name ?feeder." \
            # 		+ "?status c:IdentifiedObject.mRID ?fid." \
            # 		+ "?status c:Feeder.NormalEnergizingSubstation ?sub." \
            # 		+ "?sub c:IdentifiedObject.name ?station." \
            # 		+ "?sub c:IdentifiedObject.mRID ?sid." \
            # 		+ "?sub c:Substation.Region ?sgr." \
            # 		+ "?sgr c:IdentifiedObject.name ?subregion." \
            # 		+ "?sgr c:IdentifiedObject.mRID ?sgrid." \
            # 		+ "?sgr c:SubGeographicalRegion.Region ?rgn." \
            # 		+ "?rgn c:IdentifiedObject.name ?region." \
            # 		+ "?rgn c:IdentifiedObject.mRID ?rgnid." \
            # 		+ "}  ORDER by ?station ?feeder";

            query_string = "SELECT ?name ?mRID ?substationName ?substationID " \
                           "?subregionName ?subregionID ?regionName " \
                           "?regionID WHERE { " \
                           "?status r:global_property_types c:Feeder. " \
                           "?status c:IdentifiedObject.name ?name. " \
                           "?status c:IdentifiedObject.mRID ?mRID. " \
                           "?status c:Feeder.NormalEnergizingSubstation ?subStation. " \
                           "?subStation c:IdentifiedObject.name ?substationName. " \
                           "?subStation c:IdentifiedObject.mRID ?substationID. " \
                           "?subStation c:Substation.Region ?subRegion. " \
                           "?subRegion c:IdentifiedObject.name ?subregionName. " \
                           "?subRegion c:IdentifiedObject.mRID ?subregionID. " \
                           "?subRegion c:SubGeographicalRegion.Region " \
                           "?region. ?region c:IdentifiedObject.name ?regionName. " \
                           "?region c:IdentifiedObject.mRID ?regionID. " \
                           "} ORDER by ?name"
            pg_data_request.set_request_type(PowergridModelDataRequest.RequestType.QUERY.value)
            pg_data_request.set_query_string(query_string)
            pg_data_request.set_result_format(PowergridModelDataRequest.ResultFormat.JSON.value)
            pg_data_request.set_model_id(None)
            
            print("QUERY REQUEST:", pg_data_request)
            print()
            print()
            
            client = self.get_client()
            
            response = client.get_response(str(pg_data_request), "topic_requestData.powergridmodel", RESPONSE_FORMAT.JSON)
            
            if isinstance(response, str):
                response_str = response
                data_response = DataResponse.parse(response_str)
                print(data_response.get_data())
            else:
                print(response)
                print(response.__class__)
            
        except Exception as e:
            print(e)
    
    def test_query_model_names(self):
        try:
            pg_data_request = PowergridModelDataRequest()
            pg_data_request.set_request_type(PowergridModelDataRequest.RequestType.QUERY_MODEL_NAMES.value)
            pg_data_request.set_result_format(PowergridModelDataRequest.ResultFormat.JSON.value)
            
            print("MODEL NAMES REQUEST:", "topic_requestData.powergridmodel")
            print(pg_data_request)
            print()
            print()
            
            client = self.get_client()
            
            response = client.get_response(str(pg_data_request), "topic_requestData.powergridmodel", RESPONSE_FORMAT.JSON)
            
            if isinstance(response, str):
                response_str = response
                data_response = DataResponse.parse(response_str)
                print(data_response.get_data())
            else:
                print(response)
                print(response.__class__)
            
        except Exception as e:
            print(e)
    
    def test_query_model_info(self):
        try:
            pg_data_request = PowergridModelDataRequest()
            pg_data_request.set_request_type(PowergridModelDataRequest.RequestType.QUERY_MODEL_INFO.value)
            pg_data_request.set_result_format(PowergridModelDataRequest.ResultFormat.JSON.value)
            
            print("MODEL INFO REQUEST:", "topic_requestData.powergridmodel")
            print(pg_data_request)
            print()
            print()
            
            client = self.get_client()
            
            response = client.get_response(str(pg_data_request), "topic_requestData.powergridmodel", RESPONSE_FORMAT.JSON)
            
            if isinstance(response, str):
                response_str = response
                data_response = DataResponse.parse(response_str)
                print(data_response.get_data())
            else:
                print(response)
                print(response.__class__)
            
        except Exception as e:
            print(e)
    
    def test_query_object_types(self):
        try:
            model_id = "_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"
            pg_data_request = PowergridModelDataRequest()
            pg_data_request.set_request_type(PowergridModelDataRequest.RequestType.QUERY_OBJECT_TYPES.value)
            pg_data_request.set_result_format(PowergridModelDataRequest.ResultFormat.JSON.value)
            pg_data_request.set_model_id(model_id)
            
            print("OBJECT TYPES REQUEST:", "topic_requestData.powergridmodel")
            print(pg_data_request)
            print()
            print()
            
            client = self.get_client()
            
            response = client.get_response(str(pg_data_request), "topic_requestData.powergridmodel", RESPONSE_FORMAT.JSON)
            
            if isinstance(response, str):
                response_str = response
                data_response = DataResponse.parse(response_str)
                print(data_response.get_data())
            else:
                print(response)
                print(response.__class__)
            
        except Exception as e:
            print(e)
    
    def test_query_object(self):
        try:
            object_mrid = "_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"
            pg_data_request = PowergridModelDataRequest()
            pg_data_request.set_request_type(PowergridModelDataRequest.RequestType.QUERY_OBJECT.value)
            pg_data_request.set_result_format(PowergridModelDataRequest.ResultFormat.JSON.value)
            pg_data_request.set_object_id(object_mrid)
            pg_data_request.set_model_id(None)
            
            print("OBJECT REQUEST:", "topic_requestData.powergridmodel")
            print(pg_data_request)
            print()
            print()
            
            client = self.get_client()
            
            response = client.get_response(str(pg_data_request), "topic_requestData.powergridmodel", RESPONSE_FORMAT.JSON)
            
            if isinstance(response, str):
                response_str = response
                data_response = DataResponse.parse(response_str)
                print(data_response.get_data())
            else:
                print(response)
                print(response.__class__)
            
        except Exception as e:
            print(e)
    
    def test_query_model(self):
        try:
            model_id = "_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"
            pg_data_request = PowergridModelDataRequest()
            pg_data_request.set_request_type(PowergridModelDataRequest.RequestType.QUERY_MODEL.value)
            pg_data_request.set_result_format(PowergridModelDataRequest.ResultFormat.JSON.value)
            pg_data_request.set_model_id(model_id)
            pg_data_request.set_object_type("http://iec.ch/TC57/CIM100#ConnectivityNode")
            pg_data_request.set_filter("?status cim:IdentifiedObject.name 'q14733'")
            
            print("QUERY MODEL REQUEST:", "topic_requestData.powergridmodel")
            print(pg_data_request)
            print()
            print()
            
            client = self.get_client()
            
            response = client.get_response(str(pg_data_request), "topic_requestData.powergridmodel", RESPONSE_FORMAT.JSON)
            
            if isinstance(response, str):
                response_str = response
                data_response = DataResponse.parse(response_str)
                print(data_response.get_data())
            else:
                print(response)
                print(response.__class__)
            
        except Exception as e:
            print(e)
    
    def get_client(self):
        if self.client is None:
            properties = {}
            properties["goss.system.manager"]= "system"
            properties["goss.system.manager.password"]= "manager"
            properties["goss.openwire.uri"]= "tcp://0.0.0.0:61616"
            properties["goss.stomp.uri"]= "stomp://0.0.0.0:61613"
            properties["goss.ws.uri"]= "ws://0.0.0.0:61614"
            properties["goss.ssl.uri"]= "ssl://0.0.0.0:61443"
            
            client_factory = ClientServiceFactory()
            client_factory.updated(properties)
            
            credentials = UsernamePasswordCredentials(TestConstants.username, TestConstants.password)
            self.client = client_factory.create(Protocol.STOMP, credentials)
            
        return self.client
