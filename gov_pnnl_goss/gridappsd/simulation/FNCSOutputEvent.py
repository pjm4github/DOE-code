import json
from stomp import Connection12

from gov_pnnl_goss.core.ClientFactory import ClientFactory
from gov_pnnl_goss.core.security.SecurityConfig import SecurityConfig
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class FNCSOutputEvent:
    def __init__(self, client_factory, security_config):
        self.client_factory = client_factory
        self.security_config = security_config

    def on_message(self, message):
        try:
            credentials = (self.security_config.get_manager_user(), self.security_config.get_manager_password())
            client = self.client_factory.create("STOMP", credentials, True)

            # TODO: Parse message and update simulation status or communicate with the bridge accordingly
            client.send(GridAppsDConstants.topic_COSIM_input, "test message")

        except Exception as e:
            # TODO: Handle the exception appropriately
            print(e)


# Example usage
if __name__ == "__main__":
    # Create instances of SecurityConfig and ClientFactory
    security_config = SecurityConfig()
    client_factory = ClientFactory()

    # Create an instance of FNCSOutputEvent and call its on_message method with a message
    fncs_output_event = FNCSOutputEvent(client_factory, security_config)
    message = {}  # Replace with your JSON message
    fncs_output_event.on_message(message)
