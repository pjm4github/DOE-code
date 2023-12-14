import unittest
import time
from mockito import mock, when, unstub, any
from openai.types.chat.completion_create_params import ResponseFormat

from gov_pnnl_goss.core import Client
from gov_pnnl_goss.core.Response import Response
from gov_pnnl_goss.gridappsd.dto.ConfigurationRequest import ConfigurationRequest
from gov_pnnl_goss.gridappsd.dto.RequestAppStart import RequestAppStart
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class TestConfigurationManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.OPENWIRE_CLIENT_CONNECTION = "tcp://localhost:6000"
        cls.STOMP_CLIENT_CONNECTION = "stomp://localhost:6000"

    def setUp(self):
        self.simulationId = None
        self.client = None
        self.testConfig = mock()

    def tearDown(self):
        unstub()

    def create_mock_client(self):
        #     Client getClient() throws Exception{
        # 		if(client==null){
        # 			Dictionary properties = new Properties();
        # 			properties.put("goss.system.manager", "system");
        # 			properties.put("goss.system.manager.password", "manager");
        #
        # 			// The following are used for the core-client connection.
        # 			properties.put("goss.openwire.uri", "tcp://0.0.0.0:61616");
        # 			properties.put("goss.stomp.uri", "stomp://0.0.0.0:61613");
        # 			properties.put("goss.ws.uri", "ws://0.0.0.0:61614");
        # 			properties.put("goss.ssl.uri", "ssl://0.0.0.0:61443");
        # 			ClientServiceFactory client_factory = new ClientServiceFactory();
        # 			client_factory.updated(properties);
        #
        # 			//Step1: Create GOSS Client
        # 			Credentials credentials = new UsernamePasswordCredentials(
        # 					TestConstants.username, TestConstants.password);
        # 	//		client = client_factory.create(PROTOCOL.OPENWIRE, credentials);
        # 			client = client_factory.create(PROTOCOL.STOMP, credentials);
        # 		}
        # 		return client;
        # 	}

        client = mock(Client)
        when(client).getResponse(any(), any(), ResponseFormat.JSON).thenReturn(Response(data="{}"))
        return client

    def test_sanity_ServerStarted(self):
        # Replace the following lines with your actual code for checking if the server started
        server_control = self.server_control  # Replace with your actual server control instance
        self.assertIsNotNone(server_control)
        # 		log.debug("TEST: serverCanStartSuccessfully");
        # 		System.out.println("TEST: serverCanStartSuccessfully");
        # 		assertNotNull(serverControl);
        # 		log.debug("TEST_END: serverCanStartSuccessfully");

        # Add your server started validation logic here

    def test_start_simulation(self):
        when(self.testConfig.configure(self)).thenReturn(self.testConfig)
        when(self.testConfig.apply()).thenReturn(None)

        response = Response()
        response.data = "{}"
        when(self.client.getResponse(any(), any(), ResponseFormat.JSON)).thenReturn(response)

        simulation_id = self.start_simulation()

        self.assertEqual(simulation_id, "{}")
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.simulationId)

    def test_get_configuration_property(self):
        #     	//ConfigurationManager manager = getService(ConfigurationManager.class);
        #
        #     	//manager.getConfigurationProperty(key)
        pass

    def test_get_GLM_base_configuration(self):
        start = int(time.time() * 1000)  # Current timestamp in milliseconds

        object_mrid = "_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"

        config_request = ConfigurationRequest()
        config_request.configuration_type = "GLDBaseConfigurationHandler"
        properties = {
            "ZFRACTION": "0.0",
            "IFRACTION": "1.0",
            "PFRACTION": "0.0",
            "SCHEDULENAME": "ieeezipload",
            "LOADSCALINGFACTOR": "1.0",
            "MODELID": object_mrid,
        }
        if self.simulationId is not None:
            properties["SIMULATIONID"] = self.simulationId
        config_request.parameters = properties

        print(f"CONFIG BASE GLM REQUEST: {GridAppsDConstants.topic_requestConfig}")
        print(config_request)
        print()
        print()

        response = Response()
        response.data = "{}"
        when(self.client.getResponse(any(), any(), ResponseFormat.JSON)).thenReturn(response)

        self.testgetGLMBaseConfiguration()  # Call the method

        end = int(time.time() * 1000)  # Current timestamp in milliseconds
        print(f"Took {(end - start)} ms")

    def test_get_GLD_all_configuration(self):
        start = int(time.time() * 1000)  # Current timestamp in milliseconds

        object_mrid = "_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"

        config_request = ConfigurationRequest()
        config_request.configuration_type = "GLDAllConfigurationHandler"
        properties = {
            "DIRECTORY": "/tmp/gridappsd_tmp/" + self.simulationId if self.simulationId else "12345",
            "SIMULATIONNAME": "ieee8500",
            "ZFRACTION": "0.0",
            "IFRACTION": "1.0",
            "PFRACTION": "0.0",
            "SCHEDULENAME": "ieeezipload",
            "LOADSCALINGFACTOR": "1.0",
            "SOLVERMETHOD": "NR",
            "SIMULATIONSTARTTIME": "2018-02-18 00:00:00",
            "SIMULATIONDURATION": "60",
            "SIMULATIONBROKERHOST": "localhost",
            "SIMULATIONBROKERPORT": "61616",
            "MODELID": object_mrid,
        }
        config_request.parameters = properties

        print(f"CONFIG BASE ALL REQUEST: {GridAppsDConstants.topic_requestConfig}")
        print(config_request)
        print()
        print()

        response = Response()
        response.data = "{}"
        when(self.client.getResponse(any(), any(), ResponseFormat.JSON)).thenReturn(response)

        self.testgetGLDAllConfiguration()  # Call the method

        end = int(time.time() * 1000)  # Current timestamp in milliseconds
        print(f"Took {(end - start)} ms")


    def test_get_GLD_simulation_output_configuration(self):
        start = int(time.time() * 1000)  # Current timestamp in milliseconds

        object_mrid = "_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"

        config_request = ConfigurationRequest()
        config_request.configuration_type = "GLDSimulationOutputConfigurationHandler"
        properties = {
            "MODELID": object_mrid,
            "DICTIONARY_FILE": "",
            "SIMULATIONID": self.simulationId if self.simulationId else None,
        }
        config_request.parameters = properties

        print(f"CONFIG SIM OUTPUT REQUEST: {GridAppsDConstants.topic_requestConfig}")
        print(config_request)
        print()
        print()

        response = Response()
        response.data = "{}"
        when(self.client.getResponse(any(), any(), ResponseFormat.JSON)).thenReturn(response)

        self.testgetGLDSimulationOutputConfiguration()  # Call the method

        end = int(time.time() * 1000)  # Current timestamp in milliseconds
        print(f"Took {(end - start)} ms")

    def test_get_GLM_symbols_configuration(self):
        start = int(time.time() * 1000)  # Current timestamp in milliseconds

        object_mrid = "_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"

        config_request = ConfigurationRequest()
        config_request.configuration_type = "CIMSymbolsConfigurationHandler"
        properties = {
            "MODELID": object_mrid,
            "SIMULATIONID": self.simulationId if self.simulationId else None,
        }
        config_request.parameters = properties

        print(f"CONFIG CIM SYMBOLS REQUEST: {GridAppsDConstants.topic_requestConfig}")
        print(config_request)
        print()
        print()

        response = Response()
        response.data = "{}"
        when(self.client.getResponse(any(), any(), ResponseFormat.JSON)).thenReturn(response)

        self.testgetGLMSymbolsConfiguration()  # Call the method

        end = int(time.time() * 1000)  # Current timestamp in milliseconds
        print(f"Took {(end - start)} ms")

    def test_get_CIM_symbols_configuration(self):
        pass



    def test_get_CIM_dict_configuration(self):
        start = int(time.time() * 1000)  # Current timestamp in milliseconds

        object_mrid = "_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"

        config_request = ConfigurationRequest()
        config_request.configuration_type = "CIMDictionaryConfigurationHandler"
        properties = {
            "MODELID": object_mrid,
            "SIMULATIONID": self.simulationId if self.simulationId else None,
        }
        config_request.parameters = properties

        print(f"CONFIG CIM DICTIONARY REQUEST: {GridAppsDConstants.topic_requestConfig}")
        print(config_request)
        print()
        print()

        response = Response()
        response.data = "{}"
        when(self.client.getResponse(any(), any(), ResponseFormat.JSON)).thenReturn(response)

        self.testgetCIMDictConfiguration()  # Call the method

        end = int(time.time() * 1000)  # Current timestamp in milliseconds
        print(f"Took {(end - start)} ms")

    def test_get_CIM_feeder_index_configuration(self):
        start = int(time.time() * 1000)  # Current timestamp in milliseconds

        object_mrid = "_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"

        config_request = ConfigurationRequest()
        config_request.configuration_type = "CIMFeederIndexConfigurationHandler"
        properties = {
            "MODELID": object_mrid,
            "SIMULATIONID": self.simulationId if self.simulationId else None,
        }
        config_request.parameters = properties

        print(f"CONFIG CIM FEEDER INDEX REQUEST: {GridAppsDConstants.topic_requestConfig}")
        print(config_request)
        print()
        print()

        response = Response()
        response.data = "{}"
        when(self.client.getResponse(any(), any(), ResponseFormat.JSON)).thenReturn(response)

        self.testgetCIMFeederIndexConfiguration()  # Call the method

        end = int(time.time() * 1000)  # Current timestamp in milliseconds
        print(f"Took {(end - start)} ms")

    def test_config(self, configuration_type, model_id, simulation_id):
        try:
            config_request = ConfigurationRequest()
            config_request.configuration_type = configuration_type
            properties = {
                "MODELID": model_id,
                "SIMULATIONID": simulation_id if simulation_id else None,
            }
            config_request.parameters = properties

            print(f"CONFIG {configuration_type} REQUEST: {GridAppsDConstants.topic_requestConfig}")
            print(config_request)
            print()
            print()

            response = Response()
            response.data = "{}"
            when(self.client.getResponse(any(), any(), ResponseFormat.JSON)).thenReturn(response)

            self.testgetGLDAllConfiguration()  # Replace with the actual test method

        except Exception as e:
            print(e)

    def test_get_client(self):
        pass

    @staticmethod
    def start_simulation():
        # Sleep for 3 seconds
        time.sleep(3)

        APPLICATION_OBJECT_CONFIG = ""
        runtime_options = f"-c \"{APPLICATION_OBJECT_CONFIG}\""
        simulation_id = "12345"
        app_start = RequestAppStart("app_id", runtime_options, simulation_id)

        # Simulate sending a message to GridAPPS-D
        # send_message(GridAppsDConstants.topic_app_start, app_start)

        # Sleep for 30 seconds
        time.sleep(30)

        return simulation_id

if __name__ == '__main__':
    unittest.main()
