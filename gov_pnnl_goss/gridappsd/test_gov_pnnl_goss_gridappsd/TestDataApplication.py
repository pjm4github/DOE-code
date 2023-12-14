#
# package gov.pnnl.goss.gridappsd;
#
#
# import junit.framework.TestCase;
#
# import java.io.Serializable;
#
# import org.apache.http.auth.Credentials;
# import org.apache.http.auth.UsernamePasswordCredentials;
#
# import com.google.gson.Gson;
#
# import gov.pnnl.goss.gridappsd.dto.PowerSystemConfig;
# import pnnl.goss.core.Client;
# import pnnl.goss.core.Client.PROTOCOL;
# import pnnl.goss.core.ClientFactory;
# import pnnl.goss.core.GossResponseEvent;
# import pnnl.goss.core.client.ClientServiceFactory;
# import pnnl.goss.gridappsd.utils.GridAppsDConstants;
#
# public class TestDataApplication extends TestCase {
#
# 	ClientFactory client_factory = new ClientServiceFactory();
#
# 	Client client;
#
# 	public void testApplication() {
#
# 		try {
#
# 			//Step1: Create GOSS Client
# 			Credentials credentials = new UsernamePasswordCredentials(
# 					GridAppsDConstants.username, GridAppsDConstants.password);
# 			client = client_factory.create(PROTOCOL.STOMP, credentials);
#
# 			//Create Request Simulation object
# 			PowerSystemConfig powerSystemConfig = new PowerSystemConfig();
# 			powerSystemConfig.GeographicalRegion_name = "ieee8500_Region";
# 			powerSystemConfig.SubGeographicalRegion_name = "ieee8500_SubRegion";
# 			powerSystemConfig.Line_name = "ieee8500";
#
#
# 			Gson  gson = new Gson();
# 			String request = gson.toJson(powerSystemConfig);
# //			DataRequest request = new DataRequest();
# //			request.setRequestContent(powerSystemConfig);
# 			String response = client.getResponse(request,GridAppsDConstants.topic_requestData, null).toString();
#
# 			//TODO subscribe to response
# 			client.subscribe(GridAppsDConstants.topic_simulationOutput+response, new GossResponseEvent() {
#
#
# 				@Override
# 				public void onMessage(Serializable response) {
# 					System.out.println("simulation output is: "+response);
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

import unittest
# from goss.gridappsd import PowerSystemConfig
# from goss.core import ClientFactory, Credentials, PROTOCOL
# from goss.core.client import ClientServiceFactory
# from goss.core.response import GossResponseEvent
# from goss.gridappsd.utils import GridAppsDConstants
import json

from gov_pnnl_goss.core.client.ClientServiceFactory import Credentials, ClientServiceFactory
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.DTOComponentTests import PowerSystemConfig
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.ProcessManagerComponentTests import GossResponseEvent
from gov_pnnl_goss.gridappsd.utils import GridAppsDConstants



class TestDataApplication(unittest.TestCase):

    def test_application(self):
        try:
            # Step1: Create GOSS Client
            credentials = Credentials(GridAppsDConstants.username, GridAppsDConstants.password)
            client_factory = ClientServiceFactory()
            client = client_factory.create(self.PROTOCOL.STOMP, credentials)

            # Create PowerSystemConfig object
            power_system_config = PowerSystemConfig(
                GeographicalRegion_name="ieee8500_Region",
                SubGeographicalRegion_name="ieee8500_SubRegion",
                Line_name="ieee8500"
            )

            # Convert PowerSystemConfig to JSON string
            request = json.dumps(power_system_config.to_dict())

            # Send the JSON request and get the response
            response = client.getResponse(request, GridAppsDConstants.topic_requestData, None).decode('utf-8')

            # TODO: Subscribe to response

            def on_message(response):
                print(f"simulation output is: {response}")

            client.subscribe(GridAppsDConstants.topic_simulationOutput + response,
                             GossResponseEvent(on_message))

        except Exception as e:
            print(e)


if __name__ == '__main__':
    unittest.main()
