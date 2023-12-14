import json

from gov_pnnl_goss.core.ClientFactory import ClientFactory
from gov_pnnl_goss.core.security.SecurityConfig import SecurityConfig
from gov_pnnl_goss.gridappsd.simulation.FNCSOutputEvent import FNCSOutputEvent
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class SimulationEvent:
    def __init__(self, client_factory, security_config):
        self.client_factory = client_factory
        self.security_config = security_config

    def on_message(self, message):
        try:
            event = json.loads(message)
            username = event.get('username')

            credentials = (self.security_config.get_manager_user(), self.security_config.get_manager_password())
            client = self.client_factory.create("STOMP", credentials, True)

            # Extract simulation voltage_id and simulation files from message
            # TODO: Parse message to get simulation_id and simulationFile
            simulation_id = "1"
            simulation_file = "input_code_filename"

            # Start FNCS
            self.run_command("./fncs_broker 2")

            # TODO: Check if FNCS is started correctly and send publish simulation status accordingly
            client.send(GridAppsDConstants.topic_simulationLog + simulation_id, "FNCS Co-Simulator started")

            # Start GridLAB-D
            self.run_command(f"gridlabd {simulation_file}")

            # TODO: Check if GridLAB-D is started correctly and send publish simulation status accordingly
            client.send(GridAppsDConstants.topic_simulationLog + simulation_id, "GridLAB-D started")

            # Start GOSS-FNCS Bridge
            self.run_command("python ./scripts/fncs_goss_bridge.py")

            # TODO: Check if the bridge is started correctly and send publish simulation status accordingly
            client.send(GridAppsDConstants.topic_simulationLog + simulation_id, "FNCS-GOSS Bridge started")

            # Subscribe to GOSS FNCS Bridge output topic
            client.subscribe(GridAppsDConstants.topic_COSIM_output, FNCSOutputEvent())

            # Communicate with GOSS FNCS Bridge to get status and output
            client.send(GridAppsDConstants.topic_COSIM, "isInitialized")

        except Exception as e:
            # TODO: Handle the exception appropriately
            print(e)

    def run_command(self, command):
        # Implement the logic to run a command here
        pass  # Replace with your command execution code


# Example usage
if __name__ == "__main__":
    # Create instances of SecurityConfig and ClientFactory
    security_config = SecurityConfig()
    client_factory = ClientFactory()

    # Create an instance of SimulationEvent and call its on_message method with a message
    simulation_event = SimulationEvent(client_factory, security_config)
    message = {}  # Replace with your JSON message
    simulation_event.on_message(json.dumps(message))
