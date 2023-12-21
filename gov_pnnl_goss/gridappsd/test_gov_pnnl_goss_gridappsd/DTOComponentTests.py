
# import gov.pnnl.goss.gridappsd.dto.ApplicationConfig;
# import gov.pnnl.goss.gridappsd.dto.ApplicationObject;
# import gov.pnnl.goss.gridappsd.dto.FncsBridgeResponse;
# import gov.pnnl.goss.gridappsd.dto.ModelCreationConfig;
# import gov.pnnl.goss.gridappsd.dto.PowerSystemConfig;
# import gov.pnnl.goss.gridappsd.dto.RequestSimulation;
# import gov.pnnl.goss.gridappsd.dto.SimulationConfig;
# import gov.pnnl.goss.gridappsd.dto.SimulationOutput;
# import gov.pnnl.goss.gridappsd.dto.SimulationOutputObject;
# import gov.pnnl.goss.gridappsd.utils.GridAppsDConstants;
# import pnnl.goss.core.Client;
# import pnnl.goss.core.ClientFactory;
#
# @RunWith(MockitoJUnitRunner.class)
# public class DTOComponentTests {
#     @Mock
#     Logger logger;
#     @Mock
#     ClientFactory client_factory;
#     @Mock
#     Client client;
#     @Captor
#     ArgumentCaptor<String> argCaptor;

import unittest
import datetime
from dateutil import parser as date_parser

from gov_pnnl_goss.gridappsd.dto.FncsBridgeResponse import FncsBridgeResponse
from gov_pnnl_goss.gridappsd.dto.RequestSimulation import RequestSimulation
from gov_pnnl_goss.gridappsd.dto.SimulationConfig import ModelCreationConfig, SimulationConfig, SimulationOutput
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.TestConstants import TestConstants


class ApplicationConfig:
    pass


class PowerSystemConfig:
    pass


class ApplicationObject:
    pass


class SimulationOutputObject:
    pass



class DTOComponentTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_power_system_config_format_check(self):
        # Verify that parsing a bad input fails
        parse_fail = None
        try:
            parse_fail = PowerSystemConfig.parse(self.SIMULATION_CONFIG)
        except Exception:
            pass
        self.assertIsNone(parse_fail)

        parsed = PowerSystemConfig.parse(TestConstants.POWER_SYSTEM_CONFIG)
        self.assertIsNotNone(parsed.GeographicalRegion_name)
        self.assertIsNotNone(parsed.SubGeographicalRegion_name)
        self.assertIsNotNone(parsed.Line_name)

        config = self.generate_power_system_config()

        # Assert equal serialized PSC and comparison string
        self.assertEqual(config.to"", TestConstants.POWER_SYSTEM_CONFIG)

    def test_application_object_format_check(self):
        # Verify that parsing a bad input fails
        parse_fail = None
        try:
            parse_fail = ApplicationObject.parse(TestConstants.SIMULATION_CONFIG)
        except Exception:
            pass
        self.assertIsNone(parse_fail)

        # Verify parse from string
        parsed = ApplicationObject.parse(TestConstants.APPLICATION_OBJECT)
        self.assertIsNotNone(parsed.name)
        self.assertIsNotNone(parsed.config_string)

        config = self.generate_application_object()

        # Assert equal serialized object and comparison string
        self.assertEqual(config.to"", TestConstants.APPLICATION_OBJECT_ESC)

    def test_application_config_format_check(self):
        # Verify that parsing a bad input fails
        parse_fail = None
        try:
            parse_fail = ApplicationConfig.parse(TestConstants.SIMULATION_CONFIG)
        except Exception:
            pass
        self.assertIsNone(parse_fail)

        # Verify parse from string
        parsed = ApplicationConfig.parse(TestConstants.APPLICATION_CONFIG)
        self.assertEqual(1, len(parsed.applications))

        config = self.generate_application_config()

        # Serialize DTO Object
        serialized = config.to""

        # Assert equal serialized object and comparison string
        self.assertEqual(serialized, TestConstants.APPLICATION_CONFIG_ESC)

    def test_fncs_bridge_response_format_check(self):
        # Verify that parsing a bad input fails
        parse_fail = None
        try:
            parse_fail = FncsBridgeResponse.parse(TestConstants.SIMULATION_CONFIG)
        except Exception:
            pass
        self.assertIsNone(parse_fail)

        # Verify parse from string
        parsed = FncsBridgeResponse.parse(TestConstants.FNCS_BRIDGE_RESPONSE)
        self.assertIsNotNone(parsed.command)
        self.assertIsNotNone(parsed.response)
        self.assertIsNotNone(parsed.output)

        config = self.generate_fncs_bridge_response()

        # Assert equal serialized object and comparison string
        self.assertEqual(config.to"", TestConstants.FNCS_BRIDGE_RESPONSE)

    def test_model_creation_config_format_check(self):
        # Verify that parsing a bad input fails
        parse_fail = None
        try:
            parse_fail = ModelCreationConfig.parse(TestConstants.SIMULATION_CONFIG)
        except Exception:
            pass
        self.assertIsNone(parse_fail)

        # Verify parse from string
        parsed = ModelCreationConfig.parse(TestConstants.MODEL_CREATION_CONFIG)
        self.assertIsNotNone(parsed.load_scaling_factor)
        self.assertIsNotNone(parsed.schedule_name)
        self.assertIsNotNone(parsed.z_fraction)
        self.assertIsNotNone(parsed.i_fraction)
        self.assertIsNotNone(parsed.p_fraction)

        config = self.generate_model_creation_config()

        # Assert equal serialized object and comparison string
        self.assertEqual(config.to"", TestConstants.MODEL_CREATION_CONFIG)

    def test_request_simulation_format_check(self):
        # Verify that parsing a bad input fails
        parse_fail = None
        try:
            parse_fail = RequestSimulation.parse(TestConstants.SIMULATION_CONFIG)
        except Exception:
            pass
        self.assertIsNone(parse_fail)

        # Verify parse from string
        parsed = RequestSimulation.parse(TestConstants.REQUEST_SIMULATION_CONFIG)
        self.assertIsNotNone(parsed.application_config)
        self.assertIsNotNone(parsed.power_system_config)
        self.assertIsNotNone(parsed.simulation_config)

        config = self.generate_request_simulation()

        # Assert equal serialized object and comparison string
        self.assertEqual(config.to"", TestConstants.REQUEST_SIMULATION_CONFIG_ESC)

    def test_simulation_config_format_check(self):
        # Verify that parsing a bad input fails
        parse_fail = None
        try:
            parse_fail = SimulationConfig.parse(TestConstants.REQUEST_SIMULATION_CONFIG)
        except Exception:
            pass
        self.assertIsNone(parse_fail)

        # Verify parse from string
        parsed = SimulationConfig.parse(TestConstants.SIMULATION_CONFIG)
        self.assertIsNotNone(parsed.duration)
        self.assertIsNotNone(parsed.model_creation_config)
        self.assertIsNotNone(parsed.power_flow_solver_method)
        self.assertIsNotNone(parsed.simulation_name)
        self.assertIsNotNone(parsed.simulation_output)
        self.assertIsNotNone(parsed.simulator)
        self.assertIsNotNone(parsed.start_time)
        self.assertIsNotNone(parsed.run_realtime)

        config = self.generate_simulation_config()

        # Assert equal serialized object and comparison string
        self.assertEqual(config.to"", TestConstants.SIMULATION_CONFIG)

    def test_simulation_output_format_check(self):
        # Verify that parsing a bad input fails
        parse_fail = None
        try:
            parse_fail = SimulationOutput.parse(TestConstants.SIMULATION_CONFIG)
        except Exception:
            pass
        self.assertIsNone(parse_fail)

        # Verify parse from string
        parsed = SimulationOutput.parse(TestConstants.SIMULATION_CONFIG_OUTPUT_FULL)
        self.assertEqual(29, len(parsed.output_objects))

        config = self.generate_simulation_output()

        # Assert equal serialized object and comparison string
        self.assertEqual(config.to"", TestConstants.SIMULATION_CONFIG_OUTPUT_SHORT)

    def test_simulation_output_object_format_check(self):
        # Verify that parsing a bad input fails
        parse_fail = None
        try:
            parse_fail = SimulationOutputObject.parse(TestConstants.SIMULATION_CONFIG)
        except Exception:
            pass
        self.assertIsNone(parse_fail)

        # Verify parse from string
        parsed = SimulationOutputObject.parse(TestConstants.SIMULATION_CONFIG_OUTPUT_OBJECT_1)
        self.assertIsNotNone(parsed.name)
        self.assertEqual(10, len(parsed.properties))

        config = self.generate_simulation_output_object("rcon_FEEDER_REG")

        # Assert equal serialized object and comparison string
        self.assertEqual(config.to"", TestConstants.SIMULATION_CONFIG_OUTPUT_OBJECT_1)

    def generate_simulation_config(self):
        config_output = self.generate_simulation_output()
        config = SimulationConfig()
        try:
            d = date_parser.parse("2009-07-21 00:00:00")
        except Exception as e:
            print(e)
            d = datetime.datetime.now()
        config.start_time = d.timestamp() * 1000
        config.duration = 120
        config.simulator = "GridLAB-D"
        config.run_realtime = True
        config.simulation_name = "ieee8500"
        config.power_flow_solver_method = "NR"
        config.simulation_id = "12345"

        config.simulation_output = config_output
        config.model_creation_config = self.generate_model_creation_config()

        return config

    def generate_power_system_config(self):
        config = PowerSystemConfig()
        config.GeographicalRegion_name = "ieee8500_Region"
        config.Line_name = "ieee8500"
        config.SubGeographicalRegion_name = "ieee8500_SubRegion"
        return config

    def generate_model_creation_config(self):
        config = ModelCreationConfig()
        config.load_scaling_factor = 1
        config.schedule_name = "ieeezipload"
        config.z_fraction = 0
        config.i_fraction = 1
        config.p_fraction = 0

        return config

    def generate_simulation_output(self):
        config_obj1 = self.generate_simulation_output_object("rcon_FEEDER_REG")
        config_obj2 = self.generate_simulation_output_object("rcon_VREG2")

        config = SimulationOutput()
        config.getOutputObjects().append(config_obj1)
        config.getOutputObjects().append(config_obj2)

        return config

    def generate_simulation_output_object(self, name):
        props_array = ["connect_type", "Control", "control_level", "PT_phase", "band_center", "band_width", "dwell_time", "raise_taps", "lower_taps", "regulation"]
        config = SimulationOutputObject()
        config.name = name
        config.properties = props_array
        return config

    def generate_application_object(self):
        obj = ApplicationObject()
        obj.config_string = TestConstants.APPLICATION_OBJECT_CONFIG_ESC.replace("\\\\", "\\")
        obj.name = "vvo"
        return obj

    def generate_application_config(self):
        config = ApplicationConfig()
        config.applications = [self.generate_application_object()]
        return config

    def generate_fncs_bridge_response(self):
        config = FncsBridgeResponse()
        config.command = "isInitialized"
        config.output = {}
        config.response = "true"
        return config

if __name__ == '__main__':
    unittest.main()

