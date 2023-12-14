import os
import shutil
import json
import subprocess
import logging

from gov_pnnl_goss.gridappsd.api import ConfigurationHandler
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class OchreAllConfigurationHandler(ConfigurationHandler):
    def __init__(self):
        self.logger = LogManager(OchreAllConfigurationHandler.__name__)
        super(OchreAllConfigurationHandler, self).__init__()

    def generate_config(self, input_data):
        try:
            # Get parameters from the input data
            directory = input_data.get("directory")
            simulation_broker_host = input_data.get("simulation_broker_host")
            simulation_broker_port = input_data.get("simulation_broker_port")
            model_id = input_data.get("model_id")
            separated_loads_file = input_data.get("separated_loads_file")

            # Create the target directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Copy necessary files and directories
            source_dir = "/gridappsd/services/gridappsd-ochre"
            shutil.copytree(os.path.join(source_dir, "inputs"), os.path.join(directory, "inputs"))
            shutil.copytree(os.path.join(source_dir, "agents"), os.path.join(directory, "agents"))

            # Run the Python script to generate the OCHRE HELICS config file
            subprocess.run([
                "python",
                os.path.join(source_dir, "bin", "make_config_file.py"),
                simulation_broker_host,
                directory,
                "ochre_helics_config.json",
                simulation_broker_port,
                model_id,
                separated_loads_file
            ], check=True)

            self.log.info("Generated OCHRE HELICS config file successfully.")

        except Exception as e:
            self.log.error("Error generating OCHRE HELICS config file: %status", str(e))


class GridAPPSD:
    pass


if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Connect to GridAPPS-D platform
    gridappsd_conn = GridAPPSD()

    # Create an instance of the configuration handler
    ochre_config_handler = OchreAllConfigurationHandler()

    # Subscribe to the configuration topic
    config_topic = "/topic/goss.gridappsd.config"
    gridappsd_conn.subscribe(config_topic, ochre_config_handler.generate_config)

    # Start listening for configuration requests
    gridappsd_conn.start()
