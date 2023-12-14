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
# public class TestGetTicks {
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
# 			client = client_factory.create(PROTOCOL.OPENWIRE, credentials);
#
# 			//Subscribe to bridge output
# 			client.subscribe("*", new GossResponseEvent() {
#
# 				@Override
# 				public void onMessage(Serializable response) {
# 					System.out.println("simulation output is: "+response);
#
# 				}
# 			});
#
# 			//Start fncs_goss_bridge.py
# 			//RunCommandLine.runCommand("python ./scripts/fncs_goss_bridge.py");
#
#
#
# 			while (true){
# 				Thread.sleep(1000);
# 			}
#
#
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

import unittest
import time
import json

import paho.mqtt.client as mqtt

from gov_pnnl_goss.gridappsd.utils import GridAppsDConstants


#import paho.mqtt.client as mqtt
#from pnnl.goss.gridappsd.utils import GridAppsDConstants

def on_message(client, userdata, message):
    print("simulation output is:", message.payload.decode())

class TestGetTicks(unittest.TestCase):

    def test_get_ticks(self):
        try:
            client = mqtt.Client()

            # Step 1: Connect to the MQTT broker
            client.username_pw_set(GridAppsDConstants.username, GridAppsDConstants.password)
            client.on_message = on_message
            client.connect("localhost", 1883, 60)

            # Subscribe to all topics
            client.subscribe("#")

            # Start the MQTT client loop
            client.loop_start()

            time.sleep(5)  # Wait for 5 seconds to receive messages

        except Exception as e:
            self.fail("An error occurred: " + str(e))


if __name__ == '__main__':
    unittest.main()
