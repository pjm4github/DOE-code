#
# package gov.pnnl.goss.gridappsd;
#
# import java.io.Serializable;
# import java.text.SimpleDateFormat;
# import java.util.Date;
#
# import org.apache.http.auth.Credentials;
# import org.apache.http.auth.UsernamePasswordCredentials;
# import org.slf4j.Logger;
# import org.slf4j.LoggerFactory;
#
# import com.google.gson.Gson;
#
# import gov.pnnl.goss.gridappsd.dto.PowerSystemConfig;
# import gov.pnnl.goss.gridappsd.dto.RequestSimulation;
# import gov.pnnl.goss.gridappsd.dto.SimulationConfig;
# import junit.framework.TestCase;
# import pnnl.goss.core.Client;
# import pnnl.goss.core.Client.PROTOCOL;
# import pnnl.goss.core.ClientFactory;
# import pnnl.goss.core.GossResponseEvent;
# import pnnl.goss.core.Request.RESPONSE_FORMAT;
# import pnnl.goss.core.client.ClientServiceFactory;
# import pnnl.goss.gridappsd.utils.GridAppsDConstants;
#
# public class TestApplication extends TestCase {
#
# 	private static Logger log = LoggerFactory.getLogger(TestApplication.class);
#
# 	ClientFactory client_factory = new ClientServiceFactory();
#
# 	Client client;
#
# 	public void testApplication() {
#
# 		try {
#
# 			Step1: Create GOSS Client
# 			Credentials credentials = new UsernamePasswordCredentials(
# 					GridAppsDConstants.username, GridAppsDConstants.password);
# 			client = client_factory.create(PROTOCOL.STOMP, credentials);
#
# 			Create Request Simulation object
# 			PowerSystemConfig powerSystemConfig = new PowerSystemConfig();
# 			powerSystemConfig.GeographicalRegion_name = "ieee8500_Region";
# 			powerSystemConfig.SubGeographicalRegion_name = "ieee8500_SubRegion";
# 			powerSystemConfig.Line_name = "ieee8500";
#
# 			SimulationConfig simulation_config = new SimulationConfig();
# 			simulation_config.duration = 60; .setDuration("");
# 			 TODO: Should this be an array?
# 			simulation_config.output_object_mrid = ""; .setOutput_object_mrid(null);
# 			simulation_config.power_flow_solver_method = ""; .setPower_flow_solver_method("");
# 			simulation_config.simulation_id = ""; .setSimulation_name("");
# 			simulation_config.simulator = ""; .setSimulator("");
# 			 TODO: Should this be an array?
# 			simulation_config.simulator_name  ""; .setSimulator_name(null);
#
# 			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
# 			simulation_config.start_time = sdf.format(new Date()); .setStart_time("");
#
# 			RequestSimulation requestSimulation = new RequestSimulation(powerSystemConfig, simulation_config);
#
# 			Gson  gson = new Gson();
# 			String request = gson.toJson(requestSimulation);
# 			request = "{\"power_system_config\":{\"GeographicalRegion_name\":\"ieee13nodecktassets_Region\",\"SubGeographicalRegion_name\":\"ieee13nodecktassets_SubRegion\",\"Line_name\":\"ieee13nodecktassets\"}, "+
# 					    "\"simulation_config\":{\"start_time\":\"03/07/2017 00:00:00\",\"duration\":\"60\",\"simulator\":\"GridLAB-D\",\"simulation_name\":\"my test simulation\",\"power_flow_solver_method\":\"FBS\"}}";
# 			String simulation_id = client.getResponse(request, GridAppsDConstants.topic_requestSimulation, RESPONSE_FORMAT.JSON).to"";
# 			assertNotNull(simulation_id);
# 			log.debug("REceived simulation id  = "+simulation_id);
#
# 			client.subscribe(GridAppsDConstants.topic_simulationOutput+simulation_id, new GossResponseEvent() {
#
# 				@Override
# 				public void onMessage(Serializable response) {
# 					System.out.println("simulation output is: "+response);
#
# 				}
# 			});
#
# 			client.subscribe(GridAppsDConstants.topic_simulationStatus+simulation_id, new GossResponseEvent() {
#
# 				@Override
# 				public void onMessage(Serializable response) {
# 					System.out.println("simulation status is: "+response);
#
# 				}
# 			});
#
#
# 		} catch (Exception e) {
# 			print(e);
# 		}
#
# 	}
#
#
# }

import json
from datetime import datetime
import logging
import uuid
import threading
from multiprocessing.connection import Connection

from gov_pnnl_goss.gridappsd.dto.RequestSimulation import RequestSimulation
from gov_pnnl_goss.gridappsd.dto.SimulationConfig import SimulationConfig
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.DTOComponentTests import PowerSystemConfig
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants

# from pnnl.goss.gridappsd.utils import GridAppsDConstants
# from pnnl.goss.gridappsd.dto import PowerSystemConfig, RequestSimulation, SimulationConfig
# from pnnl.goss.gridappsd import topic_requestSimulation, topic_simulationOutput, topic_simulationStatus
#
# from stomp import Connection
# from stomp.exception import ConnectFailedException

logging.basicConfig(level=logging.DEBUG)


class ConnectFailedException:
	pass



class TestApplication:
    def __init__(self):
        self.client = None

    def create_goss_client(self):
        try:
            self.client = Connection([(GridAppsDConstants.gossServer, GridAppsDConstants.gossServerPort)])
            self.client.start()
            self.client.connect(GridAppsDConstants.username, GridAppsDConstants.password, wait=True)

        except ConnectFailedException as e:
            print("GOSS connection failed:", e)

    def send_request_simulation(self):
        if self.client:
            try:
                power_system_config = PowerSystemConfig()
                power_system_config.GeographicalRegion_name = "ieee8500_Region"
                power_system_config.SubGeographicalRegion_name = "ieee8500_SubRegion"
                power_system_config.Line_name = "ieee8500"

                simulation_config = SimulationConfig()
                simulation_config.duration = 60
                simulation_config.output_object_mrid = None
                simulation_config.power_flow_solver_method = ""
                simulation_config.simulation_id = ""
                simulation_config.simulation_name = ""
                simulation_config.simulator = ""
                simulation_config.simulator_name = None

                start_time = datetime.now().strftime("%Y-%multiplicities-%d %H:%M:%S")
                simulation_config.start_time = start_time

                request_simulation = RequestSimulation(power_system_config, simulation_config)

                request = json.dumps(request_simulation.to_dict())
                request = "{\"power_system_config\":{\"GeographicalRegion_name\":\"ieee13nodecktassets_Region\",\"SubGeographicalRegion_name\":\"ieee13nodecktassets_SubRegion\",\"Line_name\":\"ieee13nodecktassets\"}, " + \
                          "\"simulation_config\":{\"start_time\":\"03/07/2017 00:00:00\",\"duration\":\"60\",\"simulator\":\"GridLAB-D\",\"simulation_name\":\"my test simulation\",\"power_flow_solver_method\":\"FBS\"}}"

                simulation_id = str(uuid.uuid4())
                self.client.send(destination=self.topic_requestSimulation, body=request, headers={"reply-to": "/temp-queue/response-queue-" + simulation_id})

                print("Sent request for simulation with ID:", simulation_id)

                def subscribe_simulation_output():
                    def on_message(headers, message):
                        print("Simulation output is:", message)

                    self.client.subscribe(destination=self.topic_simulationOutput + simulation_id, id=1, ack='auto',
                                          headers={"reply-to": "/temp-queue/response-queue-" + simulation_id})
                    self.client.set_listener('simulation_output', on_message)

                def subscribe_simulation_status():
                    def on_message(headers, message):
                        print("Simulation status is:", message)

                    self.client.subscribe(destination=self.topic_simulationStatus + simulation_id, id=2, ack='auto',
                                          headers={"reply-to": "/temp-queue/response-queue-" + simulation_id})
                    self.client.set_listener('simulation_status', on_message)

                thread_output = threading.Thread(target=subscribe_simulation_output)
                thread_output.start()

                thread_status = threading.Thread(target=subscribe_simulation_status)
                thread_status.start()

                thread_output.join()
                thread_status.join()

            except Exception as e:
                print("Error sending request for simulation:", e)
        else:
            print("GOSS client not initialized. Create a GOSS client first.")

if __name__ == "__main__":
    test_app = TestApplication()
    test_app.create_goss_client()
    test_app.send_request_simulation()
