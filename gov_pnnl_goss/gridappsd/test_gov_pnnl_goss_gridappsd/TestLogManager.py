#
# package gov.pnnl.goss.gridappsd;
#
# import gov.pnnl.goss.gridappsd.utils.GridAppsDConstants;
# import junit.framework.TestCase;
#
# import org.apache.http.auth.Credentials;
# import org.apache.http.auth.UsernamePasswordCredentials;
# import org.slf4j.Logger;
# import org.slf4j.LoggerFactory;
#
# import pnnl.goss.core.Client;
# import pnnl.goss.core.Client.PROTOCOL;
# import pnnl.goss.core.ClientFactory;
# import pnnl.goss.core.client.ClientServiceFactory;
#
# public class TestLogManager extends TestCase {
#
# private static Logger log = LoggerFactory.getLogger(TestLogManager.class);
#
# 	ClientFactory client_factory = new ClientServiceFactory();
#
# 	Client client;
#
# 	public void testLogging() throws Exception {
#
#
# 			//Step1: Create GOSS Client
# 			Credentials credentials = new UsernamePasswordCredentials(
# 					GridAppsDConstants.username, GridAppsDConstants.password);
# 			client = client_factory.create(PROTOCOL.STOMP, credentials);
#
# 			String message = "{"
# 					+ "\"process_id\":\"app_123\","
# 					+ "\"process_status\":\"started\","
# 					+ "\"log_level\":\"debug\","
# 					+ "\"log_message\":\"Testing LogManager\","
# 					+ "\"timestamp\": \"8\14\17 2:22:22\"}";
# 			client.publish("goss.gridappsd.process.log", message);
#
# 	}
#
# 	public static void main(String[] args) throws Exception{
# 		TestLogManager test = new TestLogManager();
# 		test.testLogging();
# 	}
#
#
# }


import unittest
import time
import json

import paho.mqtt.client as mqtt

from gov_pnnl_goss.gridappsd.utils import GridAppsDConstants


# import paho.mqtt.client as mqtt
# from pnnl.goss.gridappsd.utils import GridAppsDConstants

class TestLogManager(unittest.TestCase):

    def test_logging(self):
        try:
            client = mqtt.Client()

            # Step 1: Connect to the MQTT broker
            client.username_pw_set(GridAppsDConstants.username, GridAppsDConstants.password)
            client.connect("localhost", 1883, 60)

            message = {
                "process_id": "app_123",
                "process_status": "started",
                "log_level": "debug",
                "log_message": "Testing LogManager",
                "timestamp": "8\14\17 2:22:22"
            }

            # Publish the log message
            client.publish("goss.gridappsd.process.log", json.dumps(message))

            time.sleep(1)  # Wait for a short time to allow the message to be processed

        except Exception as e:
            self.fail("An error occurred: " + str(e))

if __name__ == '__main__':
    unittest.main()
