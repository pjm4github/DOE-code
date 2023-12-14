# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import logging

from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.core.GossResponseEvent import GossResponseEvent
from gov_pnnl_goss.gridappsd.data.DataRequest import DataRequest


class DataEvent(GossResponseEvent):
    """

     1. Start FNCS
     2. Start GridLAB-D with input file location and name
     3. Start GOSS-FNCS Bridge
     4. Call FNCS IsInitialized()
     5. Publish 'Simulation Initialized' on 'simulation/[id]/status' once IsInitialized() returns.
           If IsInitialized() does not return in given time then publish error on 'simulation/[id]/status' and send 'die' message to GOSS-FNCS topic simulation/[id]/input
    @author shar064


    """
    def __init__(self, manager):
        self.data_manager = manager
        self.log = LogManager(__class__.__name__)


    def on_message(self, message):
        # Parse message. message is in JSON string.
        # create and return response as simulation id
        # make synchronous call to DataManager and receive file location
        # Start FNCS
        # Start GridLAB-D with input file location and name
        # Start GOSS-FNCS Bridge
        # Call FNCS IsInitialized()
        # Publish 'Simulation Initialized' on 'simulation/[id]/status' once IsInitialized() returns.
        # If IsInitialized() does not return in given time then publish error on 
        # 'simulation/[id]/status' and send 'die' message to GOSS-FNCS topic simulation/[id]/input
        pass
        #
        # requestData = None
        #
        # if isinstance(message, DataRequest):
        #     requestData =  message.getRequestContent()
        # elif isinstance(message, DataResponse):
        #     # TODO figure out why it is double nested in dataresponse
        #     if isinstance(message.getData(), DataResponse):
        #         requestData = message.getData().getData()
        #     else:
        #         requestData = message.getData()
        # else:
        #     requestData = message
        # try:
        #     #TODO set up simulation id and temp data path
        #     r = self.data_manager.processDataRequest(requestData, 0, ".")
        #     # TODO create client and send response on it
        #
        # except Exception as e:
        #     #TODO Auto-generated catch block
        #     print(e)
