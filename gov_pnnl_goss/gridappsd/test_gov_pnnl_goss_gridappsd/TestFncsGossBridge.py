#
# package gov.pnnl.goss.gridappsd;
#
# import java.io.Serializable;
#
# import org.apache.http.auth.Credentials;
# import org.apache.http.auth.UsernamePasswordCredentials;
#
# import junit.framework.TestCase;
# import pnnl.goss.core.Client;
# import pnnl.goss.core.Client.PROTOCOL;
# import pnnl.goss.core.ClientFactory;
# import pnnl.goss.core.GossResponseEvent;
# import pnnl.goss.core.client.ClientServiceFactory;
# import pnnl.goss.gridappsd.utils.GridAppsDConstants;
# import pnnl.goss.gridappsd.utils.RunCommandLine;
#
# public class TestFncsGossBridge extends TestCase {
#
#
#
# 	public static void main(String[] args){
#
# 		try {
#
# 			ClientFactory client_factory = new ClientServiceFactory();
#
# 			Client client;
#
# 			//Step1: Create GOSS Client
# 			Credentials credentials = new UsernamePasswordCredentials(
# 					GridAppsDConstants.username, GridAppsDConstants.password);
# 			client = client_factory.create(PROTOCOL.STOMP, credentials);
#
# 			//Subscribe to bridge output
# 			client.subscribe("goss/gridappsd/fncs/output", new GossResponseEvent() {
#
# 				@Override
# 				public void onMessage(Serializable response) {
# 					System.out.println("simulation output is: "+response);
#
# 				}
# 			});
#
# 			//Start fncs_goss_bridge.py
# 			RunCommandLine.runCommand("python ./scripts/fncs_goss_bridge.py");
#
# 		} catch (Exception e) {
# 			print(e);
# 		}
#
# 	}
#
#
# }

import unittest
import subprocess

from gov_pnnl_goss.gridappsd.simulation.SimulationEvent import ClientFactory
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.ProcessManagerComponentTests import GossResponseEvent
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.TestDataApplication import Credentials
# from pnnl.goss.core.client import ClientFactory
# from pnnl.goss.core.enums import PROTOCOL
# from pnnl.goss.core.enums import GossResponseEvent
# from pnnl.goss.core.util import Credentials
# from pnnl.goss.gridappsd.utils import GridAppsDConstants


from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class TestFncsGossBridge(unittest.TestCase):

    def test_fncs_goss_bridge(self):
        try:
            client_factory = ClientFactory()
            client = None

            # Step 1: Create GOSS Client
            credentials = Credentials(GridAppsDConstants.username, GridAppsDConstants.password)
            client = client_factory.create(self.PROTOCOL.STOMP, credentials)

            # Subscribe to bridge output
            simulation_output = []

            def handle_response(response):
                nonlocal simulation_output
                simulation_output.append(response)
                print("simulation output is:", response)

            client.subscribe("goss/gridappsd/fncs/output", GossResponseEvent(handle_response))

            # Start fncs_goss_bridge.py using subprocess
            subprocess.call(["python", "./scripts/fncs_goss_bridge.py"])

            # Perform your assertions here if needed
            # Example:
            self.assertTrue(len(simulation_output) > 0)

        except Exception as e:
            self.fail(f"Test failed with exception: {str(e)}")

if __name__ == '__main__':
    unittest.main()
