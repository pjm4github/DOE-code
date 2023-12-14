#
# package gov.pnnl.goss.gridappsd;
#
# import org.slf4j.Logger;
#
#
# import org.junit.Test;
# import org.junit.runner.RunWith;
# import org.mockito.ArgumentCaptor;
# import org.mockito.Captor;
# import org.mockito.Mock;
# import org.mockito.runners.MockitoJUnitRunner;
#
# import pnnl.goss.core.Client;
# import pnnl.goss.core.ClientFactory;
#
# @RunWith(MockitoJUnitRunner.class)
# public class StatusReporterComponentTests {
#
# 	@Mock
# 	Logger logger;
#
# 	@Mock
# 	ClientFactory client_factory;
#
# 	@Mock
# 	Client client;
#
# 	@Captor
# 	ArgumentCaptor<String> argCaptor;
#
# 	//status reporter no longer exists
# 	@Test
# 	public void whenReportStatusOnTopic_clientPublishCalled(){
#
# 		// ArgumentCaptor<String> argCaptor = ArgumentCaptor.forClass(String.class);
#
# 		try {
# 			Mockito.when(client_factory.create(Mockito.any(), Mockito.any())).thenReturn(client);
# 		} catch (Exception e) {
# 			// TODO Auto-generated catch block
# 			print(e);
# 		}
#
# 		Mockito.verify(client).publish(argCaptor.capture(), argCaptor.capture());
#
# 		List<String> allValues = argCaptor.getAllValues();
# 		assertEquals(2, allValues.size());
# 		assertEquals("big/status", allValues.get(0));
# 		assertEquals("Things are good", allValues.get(1));
#
# 	}
#
# }

import unittest
from unittest.mock import Mock, patch, call

class StatusReporterComponentTests(unittest.TestCase):
    def setUp(self):
        self.log = Mock()
        self.clientFactory = Mock()
        self.client = Mock()
        self.argCaptor = Mock()

    def test_whenReportStatusOnTopic_clientPublishCalled(self):
        # Configure the client_factory mock to return the client instance
        self.clientFactory.create.return_value = self.client

        # Call the function or method that you want to test here, which should publish the message
        # For example, you can call the function that reports the status here

        # Verify that the client.publish method is called with the expected arguments
        self.client.publish.assert_called_once_with("big/status", "Things are good")

if __name__ == "__main__":
    unittest.main()
