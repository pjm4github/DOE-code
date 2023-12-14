import os
import json
import time
# from java.io import File
# from java.io import IOException
# from java.io import Serializable
# from java.nio.file import Files
# from java.util import ArrayList
# from java.util import List
# from javax.jms import Connection
# from javax.jms import ConnectionFactory
# from javax.jms import JMSConnectionFactory
# from javax.jms import JMSException
# from javax.jms import MessageProducer
# from javax.jms import Session
# from javax.jms import TextMessage
# from org.fusesource.stomp.jms import StompJmsConnectionFactory
# from org.fusesource.stomp.jms import StompJmsDestination
# from org.mockito.runners import MockitoJUnitRunner
# from pnnl.goss.core import Client
# from pnnl.goss.core import Client

#
#
# class AppManagerTest2:
#
#     APPLICATION_OBJECT_CONFIG = {"static_inputs":
#                                      {"ieee8500":
#                                           {"control_method": "ACTIVE",
#                                            "capacitor_delay": 60,
#                                            "regulator_delay": 60,
#                                            "desired_pf": 0.99,
#                                            "d_max": 0.9,
#                                            "d_min": 0.1,
#                                            "substation_link": "xf_hvmv_sub",
#                                            "regulator_list":
#                                                ["reg_FEEDER_REG", "reg_VREG2", "reg_VREG3", "reg_VREG4"],
#                                            "regulator_configuration_list":
#                                                ["rcon_FEEDER_REG", "rcon_VREG2", "rcon_VREG3", "rcon_VREG4"],
#                                            "capacitor_list":
#                                                ["cap_capbank0a", "cap_capbank0b", "cap_capbank0c", "cap_capbank1a",
#                                                 "cap_capbank1b", "cap_capbank1c", "cap_capbank2a", "cap_capbank2b",
#                                                 "cap_capbank2c", "cap_capbank3"],
#                                            "voltage_measurements":
#                                                ["l2955047,1", "l3160107,1", "l2673313,2", "l2876814,2", "m1047574,3",
#                                                 "l3254238,4"],
#                                            "maximum_voltages": 7500,
#                                            "minimum_voltages": 6500,
#                                            "max_vdrop": 5200,
#                                            "high_load_deadband": 100,
#                                            "desired_voltages": 7000,
#                                            "low_load_deadband": 100,
#                                            "pf_phase": "ABC"
#                                            }
#                                       }
#                                  }
#
#

#



import unittest
import os
import time
import json
from stomp import Connection, ConnectionListener

from gov_pnnl_goss.SpecialClasses import StompJmsConnectionFactory, Session, StompJmsDestination
from gov_pnnl_goss.gridappsd.dto.AppInfo import AppInfo, AppType
from gov_pnnl_goss.gridappsd.dto.RequestAppRegister import RequestAppRegister
from gov_pnnl_goss.gridappsd.dto.RequestAppStart import RequestAppStart
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class AppManagerTest2(unittest.TestCase, ConnectionListener):
    APPLICATION_OBJECT_CONFIG = json.dumps(
        {"static_inputs": {"ieee8500":
                               {"control_method": "ACTIVE",
                                "capacitor_delay": 60,
                                "regulator_delay": 60,
                                "desired_pf": 0.99,
                                "d_max": 0.9,
                                "d_min": 0.1,
                                "substation_link": "xf_hvmv_sub",
                                "regulator_list":
                                    ["reg_FEEDER_REG",
                                     "reg_VREG2",
                                     "reg_VREG3",
                                     "reg_VREG4"],
                                "regulator_configuration_list":
                                    ["rcon_FEEDER_REG",
                                     "rcon_VREG2",
                                     "rcon_VREG3",
                                     "rcon_VREG4"],
                                "capacitor_list":
                                    ["cap_capbank0a",
                                     "cap_capbank0b",
                                     "cap_capbank0c",
                                     "cap_capbank1a",
                                     "cap_capbank1b",
                                     "cap_capbank1c",
                                     "cap_capbank2a",
                                     "cap_capbank2b",
                                     "cap_capbank2c",
                                     "cap_capbank3"],
                                "voltage_measurements":
                                    ["l2955047,1",
                                     "l3160107,1",
                                     "l2673313,2",
                                     "l2876814,2",
                                     "m1047574,3",
                                     "l3254238,4"],
                                "maximum_voltages": 7500,
                                "minimum_voltages": 6500,
                                "max_vdrop": 5200,
                                "high_load_deadband": 100,
                                "desired_voltages": 7000,
                                "low_load_deadband": 100,
                                "pf_phase": "ABC"}
                           }
         })

    def __init__(self):
        super().__init__()
        self.connection = None
        self.app_info = None
        self.app_data = None

    def test(self):
        try:
            # Dictionary properties = new Hashtable();
            # properties.put("goss.system.manager", "system");
            # properties.put("goss.system.manager.password", "manager");
            #
            # # The following are used for the core-client connection.
            # properties.put("goss.openwire.uri", "tcp://0.0.0.0:61616");
            # properties.put("goss.stomp.uri", "stomp://0.0.0.0:61613");
            # properties.put("goss.ws.uri", "ws://0.0.0.0:61614");
            # properties.put("goss.ssl.uri", "ssl://0.0.0.0:61443");
            # testConfig = configure(this)
            # 		.add(CoreGossConfig.configureServerAndClientPropertiesConfig())
            # 		.add(createServiceDependency().setService(ClientFactory.class));
            # testConfig.apply();
            # ClientServiceFactory client_factory = new ClientServiceFactory();
            # client_factory.updated(properties);

            # Step1: Create GOSS Client
            #           Credentials credentials = new UsernamePasswordCredentials(
            #   		GridAppsDConstants.username, GridAppsDConstants.password);
            #           client = client_factory.create(PROTOCOL.OPENWIRE, credentials);
            # Create Request Simulation object
            #           PowerSystemConfig powerSystemConfig = new PowerSystemConfig();
            #       powerSystemConfig.GeographicalRegion_name = "ieee8500_Region";
            #       powerSystemConfig.SubGeographicalRegion_name = "ieee8500_SubRegion";
            #       powerSystemConfig.Line_name = "ieee8500";
            #
            #
            #       Gson  gson = new Gson();
            #       String request = gson.toJson(powerSystemConfig);
            #       DataRequest request = new DataRequest();
            #       request.setRequestContent(powerSystemConfig);
            #       System.out.println(client);

            # Register App
            self.register_app()

            time.sleep(3000)

            runtime_options = "-c " + self.APPLICATION_OBJECT_CONFIG
            simulation_id = "12345"
            app_start = RequestAppStart(self.app_info.getId(), runtime_options, simulation_id)
            self.send_message(GridAppsDConstants.topic_app_start, app_start)

            time.sleep(30000)

        except Exception as e:
            print(e)

    def register_app(self):

        app_info = AppInfo()
        app_info.set_id("vvo")
        app_info.set_creator("pnnl")
        app_info.set_description("VVO app")
        app_info.set_execution_path("app/vvoapp.py")

        inputs = []
        inputs.append(GridAppsDConstants.topic_COSIM_input)
        app_info.set_inputs(inputs)

        outputs = []
        outputs.append(GridAppsDConstants.topic_COSIM_input)
        app_info.set_outputs(outputs)

        app_info.set_launch_on_startup(False)
        app_info.set_multiple_instances(True)
        options = []
        options.append("SIMULATION_ID")
        app_info.set_options(options)

        prereqs = []
        prereqs.append("fncsgossbridge")
        app_info.set_prereqs(prereqs)
        app_info.set_type(AppType.PYTHON)
        print(self.app_info)

        parent_dir = os.curdir
        filename = parent_dir + os.sep + "resources" + os.sep + "vvo.zip"

        with open(filename, 'r') as f:
            file_data = f.read()

        app_register = RequestAppRegister(app_info, file_data)
        print("REGISTER" + app_register)
        # 		DataRequest request = new DataRequest();
        # 		request.setRequestContent(appRegister);
        # 		client.publish(GridAppsDConstants.topic_requestSimulation, appRegister);
        self.send_message(GridAppsDConstants.topic_app_register, app_register)

        # 	String response = client.getResponse(request,GridAppsDConstants.topic_app_register, RESPONSE_FORMAT.JSON).toString();

        # Sleep for 3 seconds
        time.sleep(3)

        # Define runtimeOptions and simulationId
        runtimeOptions = f'-c "{self.APPLICATION_OBJECT_CONFIG}"'
        simulationId = "12345"

        # Create and send RequestAppStart message
        appStart = RequestAppStart(self.app_info.id, runtimeOptions, simulationId)
        self.send_message(GridAppsDConstants.topic_app_start, appStart)
        print(appStart)

        # Sleep for 30 seconds
        time.sleep(30)

    def send_message(self, destination, message):


        if self.connection:
            message_json = json.dumps(message, default=lambda o: o.__dict__)
            self.connection.send(destination, message_json, headers={'content-type': 'application/json'})
        else:
            connection_factory = StompJmsConnectionFactory()
            connection_factory.set_broker_URI("tcp://localhost:61613")
            connection_factory.set_username("system")
            connection_factory.set_password("manager")

            self.connection = connection_factory.create_connection()
            session = self.connection.createSession(False, Session.AUTO_ACKNOWLEDGE)
            producer = session.createProducer(StompJmsDestination(destination))

            if isinstance(message, str):
                text_message = session.createTextMessage(message)
            else:
                text_message = session.createTextMessage(json.loads(message))
            producer.send(text_message)

    def setUp(self):
        self.broker_uri = "tcp://localhost:61613"
        self.connection = Connection([(self.broker_uri, 61613)])
        self.connection.set_listener('', self)
        # self.connection.start()
        self.connection.connect('system', 'manager', wait=True)

    def tearDown(self):
        self.connection.disconnect()

    def test_register_and_start_app(self):
        self.app_info = AppInfo(
            id="vvo",
            creator="pnnl",
            description="VVO app",
            execution_path="app/vvoapp.py",
            inputs=[GridAppsDConstants.topic_COSIM_input],
            outputs=[GridAppsDConstants.topic_COSIM_input],
            launch_on_startup=False,
            multiple_instances=True,
            options=["SIMULATION_ID"],
            prereqs=["fncsgossbridge"],
            type=AppType.PYTHON
        )

        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        app_zip_file = os.path.join(parent_dir, "resources", "vvo.zip")

        with open(app_zip_file, 'r') as f:
            self.app_data = f.read()

        app_register_request = RequestAppRegister(self.app_info, self.app_data)
        self.send_message(GridAppsDConstants.topic_app_register, app_register_request)

        time.sleep(3)  # Wait for registration to complete

        application_object_config = {
            "static_inputs": {
                "ieee8500": {
                    "control_method": "ACTIVE",
                    "capacitor_delay": 60,
                    "regulator_delay": 60,
                    "desired_pf": 0.99,
                    "d_max": 0.9,
                    "d_min": 0.1,
                    "substation_link": "xf_hvmv_sub",
                    # ... other properties ...
                }
            }
        }

        runtime_options = "-c '" + json.dumps(application_object_config) + "'"
        simulation_id = "12345"
        app_start_request = RequestAppStart(self.app_info.id, runtime_options, simulation_id)
        self.send_message(GridAppsDConstants.topic_app_start, app_start_request)

        time.sleep(30)  # Wait for the app to run

        # Add assertions here based on the expected behavior of your app


    def on_error(self, headers, message):
        print(f"Received error: {message}")

    def on_message(self, headers, message):
        print(f"Received message: {message}")

    def on_connected(self, headers, body):
        print(f"Connected to {self.broker_uri}")


if __name__ == '__main__':
    AppManagerTest2.test()
