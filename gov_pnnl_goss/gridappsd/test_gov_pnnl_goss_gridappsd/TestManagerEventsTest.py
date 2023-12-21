

import unittest
from unittest.mock import Mock, patch
import json
import mockito as Mockito
from mockito.matchers import ArgumentCaptor

from gov_pnnl_goss.gridappsd.api.AppManager import AppManager
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.api.TestManager import TestConfig, Event
from gov_pnnl_goss.gridappsd.simulation.SimulationEvent import ClientFactory
from logging import getLogger

from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.CompareResultsTest import TestManagerImpl


class ProcessEvents:
	pass


class GsonBuilder:
	pass


class RuntimeTypeAdapterFactory:
	pass


class CommOutage:
	pass


class Fault:
	pass


class ScheduledCommandEvent:
	pass


class ObjectMridAttributeMap:
	pass


class RequestTestUpdate:
	pass


class TestManagerEventsTest(unittest.TestCase):
	def setUp(self):
		self.tm = TestManagerImpl()
		self.appManager = Mock()
		self.clientFactory = Mock()
		self.client = Mock()
		self.configurationManager = Mock()
		self.dataManager = Mock()
		self.DataManager = Mock()
		self.simulationManager = Mock()
		self.logManager = Mock()
		self.argCaptor = ArgumentCaptor()
		self.argCaptorLogMessage = ArgumentCaptor()

		self.processEvent = None

		self.start_time = 1248130793

		self.events = []
		self.processEvent = ProcessEvents(self.logManager, self.events, self.start_time, 120, "system")

		self.gson = None
		self.setup_gson()

	def setup_gson(self):
		self.gson = GsonBuilder()
		commandAdapterFactory = RuntimeTypeAdapterFactory.of(Event, "event_type") \
			.registerSubtype(CommOutage, "CommOutage") \
			.registerSubtype(Fault, "Fault") \
			.registerSubtype(ScheduledCommandEvent, "ScheduledCommandEvent")
		self.gson.registerTypeAdapterFactory(commandAdapterFactory)
		self.gson.setPrettyPrinting()
		self.gson = self.gson.create()

	def test_add_events(self):
		co = CommOutage()
		objectMap = ObjectMridAttributeMap()
		objectMap.set_objectMRID("123")
		objectMap.set_attribute("Shunt")
		co.get_inputOutageList().append(objectMap)
		print(self.gson.toJson(co))

		f = Fault.parse(
			"{\"PhaseConnectedFaultKind\": \"lineToLine\", \"FaultImpedance\": {\"rGround\": 0.2 , \"xGround\": 0.3}, \"equipmentMrid\": \"235242342342342\", \"phases\": \"ABC\", \"event_type\": \"Fault\", \"occuredDateTime\": 1557439240708, \"stopDateTime\": 1557439240708}")
		print(self.gson.toJson(f))

		test_cfg1 = "{\"events\": [{\"allOutputOutage\": true, \"allInputOutage\": true, \"inputOutageList\": [{\"objectMRID\": \"61A547FB-9F68-5635-BB4C-F7F537FD824E\", \"attribute\": \"ShuntCompensator.sections\"}, {\"objectMRID\": \"61A547FB-9F68-5635-BB4C-F7F537FD824E\", \"attribute\": \"ShuntCompensator.sections\"}], \"outputOutageList\": [\"61A547FB-9F68-5635-BB4C-F7F537FD824E\", \"61A547FB-9F68-5635-BB4C-F7F537FD824E\"], \"event_type\": \"CommOutage\", \"occuredDateTime\": 1248130819, \"stopDateTime\": 1248130824}, {\"PhaseConnectedFaultKind\": \"lineToLine\", \"FaultImpedance\": {\"rGround\": 0.2, \"xGround\": 0.3}, \"ObjectMRID\": [\"235242342342342\"], \"phases\": \"ABC\", \"event_type\": \"Fault\", \"occuredDateTime\": 1248130809, \"stopDateTime\": 1248130816}], \"appId\": \"sample_app\"}"
		tc = self.gson.fromJson(test_cfg1, TestConfig)

		firstEvent = tc.get_events()[0]
		self.assertEqual(CommOutage, firstEvent.__class__)
		self.assertEqual("61A547FB-9F68-5635-BB4C-F7F537FD824E", firstEvent.get_inputOutageList()[0].get_objectMRID())

		status = self.processEvent.get_status_json()
		self.assertEqual(0, len(status.get("data")))
		print(len(status.get("data")) == 0)

		self.processEvent.add_events(tc.get_events())
		status = self.processEvent.get_status_json()
		data_array = status.get("data")
		self.assertEqual(2, len(data_array))
		print(status)
		self.assertEqual(data_array[0]["status"], "SCHEDULED")
		self.assertEqual(data_array[1]["status"], "SCHEDULED")

	def test_process_events(self):
		test_cfg1 = "{\"events\": [{\"allOutputOutage\": true, \"allInputOutage\": true, \"inputOutageList\": [{\"objectMRID\": \"mrid1123457899\", \"attribute\": \"ShuntThing\"}, {\"objectMRID\": \"mrid234578908\", \"attribute\": \"SwitchThing\"}], \"outputOutageList\": [\"mrid1123457899\", \"mrid234578908\"], \"event_type\": \"CommOutage\", \"occuredDateTime\": 1248130819, \"stopDateTime\": 1248130824}, {\"PhaseConnectedFaultKind\": \"lineToLine\", \"FaultImpedance\": {\"rGround\": 0.2, \"xGround\": 0.3}, \"ObjectMRID\": [\"235242342342342\"], \"phases\": \"ABC\", \"event_type\": \"Fault\", \"occuredDateTime\": 1248130809, \"stopDateTime\": 1248130816}], \"appId\": \"sample_app\"}"
		tc = self.gson.fromJson(test_cfg1, TestConfig)

		self.processEvent.add_events(tc.get_events())
		status = self.processEvent.get_status_json()
		print(status)

		start_time = 1248130809 - 19
		current_time = start_time
		duration = 120
		data_array = None
		while current_time <= start_time + duration:
			current_time += 3
			self.processEvent.process_at_time(self.client, "1234", current_time)
			status = self.processEvent.get_status_json()
			data_array = status.get("data")
		self.assertEqual(data_array[0]["status"], "CLEARED")
		self.assertEqual(data_array[1]["status"], "CLEARED")

	def test_command(self):
		request_update = {
			"events": [{
				"faultMRID": "12312312",
				"occuredDateTime": 1248130809,
				"stopDateTime": 1248130824
			}],
			"command": "update_events"
		}

		reqTest1 = RequestTestUpdate.parse(json.dumps(request_update))
		print(reqTest1.to_"")
		print(reqTest1.get_command())
		self.assertEqual(reqTest1.get_command(), "update_events")

		request_status = {"command": "query_events"}
		reqTest2 = RequestTestUpdate.parse(json.dumps(request_status))
		print(reqTest2.get_command())
		self.assertEqual(reqTest2.get_command(), "query_events")

	def test_update_events(self):
		test_cfg1 = {
			"events": [{
				"allOutputOutage": True,
				"allInputOutage": True,
				"inputOutageList": ["mrid1123457899", "mrid234578908"],
				"outputOutageList": ["mrid1123457899", "mrid234578908"],
				"event_type": "CommOutage",
				"occuredDateTime": 1248130819,
				"stopDateTime": 1248130824
			}, {
				"impedance": "lineToLine",
				"PhaseConnectedFaultKind": {
					"lineToGround": 0.2,
					"lineToLine": 0.3
				},
				"equipmentMrid": "235242342342342",
				"phases": "ABC",
				"event_type": "Fault",
				"occuredDateTime": 1248130809,
				"stopDateTime": 1248130816
			}],
			"appId": "sample_app"
		}
		tc = TestConfig.parse(json.dumps(test_cfg1))

		self.process_event.add_events(tc.get_events())
		status = self.process_event.get_status_json()
		dataArray0 = status.get("data").getAsJsonArray()
		faultMRID = dataArray0.get(0).getAsJsonObject().get("faultMRID").getAs""
		occuredDateTime = dataArray0.get(0).getAsJsonObject().get("occuredDateTime").getAsLong()
		stopDateTime = dataArray0.get(0).getAsJsonObject().get("stopDateTime").getAsLong()
		occuredDateTime -= 6
		stopDateTime -= 6
		print(faultMRID + " " + occuredDateTime + " " + stopDateTime)

		request_update = {
			"events": [{
				"faultMRID": faultMRID,
				"occuredDateTime": occuredDateTime,
				"stopDateTime": stopDateTime
			}],
			"command": "update_events"
		}
		reqTest1 = RequestTestUpdate.parse(json.dumps(request_update))
		print("Update event")
		print(reqTest1.to_"")
		self.assertEqual(reqTest1.get_command(), "update_events")

		self.process_event.update_event_times(reqTest1.get_events())

		status1 = self.process_event.get_status_json()
		dataArray1 = status1.get("data").getAsJsonArray()
		faultMRID1 = dataArray1.get(0).getAsJsonObject().get("faultMRID").getAs""
		occuredDateTime1 = dataArray1.get(0).getAsJsonObject().get("occuredDateTime").getAsLong()
		stopDateTime1 = dataArray1.get(0).getAsJsonObject().get("stopDateTime").getAsLong()
		self.assertEqual(faultMRID, faultMRID1)
		self.assertEqual(occuredDateTime, occuredDateTime1)
		self.assertEqual(stopDateTime, stopDateTime1)

		start_time = 1248130809 - 19
		current_time = start_time
		duration = 120
		dataArray = None
		while current_time <= start_time + duration:
			current_time += 3
			self.process_event.process_at_time(self.client, "1234", current_time)
			status = self.process_event.get_status_json()
			print(status)
			dataArray = status.get("data").getAsJsonArray()
		self.assertEqual(dataArray.get(0).getAsJsonObject().get("status").getAs"", "CLEARED")
		self.assertEqual(dataArray.get(1).getAsJsonObject().get("status").getAs"", "CLEARED")

		rt = RequestTestUpdate.parse(json.dumps(test_cfg1))
		print(tc.get_events())
#
	def test_basic_parse_schedule(self):
		tcs = {
			"events": [{
				"allOutputOutage": False,
				"allInputOutage": False,
				"event_type": "ScheduledCommandEvent",
				"occuredDateTime": 1248130812,
				"stopDateTime": 1248130842
			}],
			"appId": "sample_app"
		}
		tct = self.gson.fromJson(json.dumps(tcs), TestConfig)

		tcs = {

				"events": [{
					"allOutputOutage": False,
					"allInputOutage": False,
					"inputOutageList": [{
						"objectMrid": "_30E704EB-29F1-FA2C-D797-6E25DFEF0A9B",
						"attribute": "ShuntCompensator.sections"
					}],
					"outputOutageList": ["_FF7722DD-151E-7018-10CA-297882C1A5AE"],
					"event_type": "CommOutage",
					"occuredDateTime": 1248130812,
					"stopDateTime": 1248130842
				}],
				"appId": "sample_app"

			}
		tct = self.gson.fromJson(json.dumps(tcs), TestConfig)

		tcs = {
			"events": [{
				"PhaseConnectedFaultKind": "lineToLine",
				"FaultImpedance": {
					"rGround": 0.001,
					"xGround": 0.001
				},
				"ObjectMRID": ["235242342342342"],
				"phases": "ABC",
				"event_type": "Fault",
				"occuredDateTime": 1248130809,
				"stopDateTime": 1248130816
			}],
			"appId": "sample_app"
		}
		tct = self.gson.fromJson(json.dumps(tcs), TestConfig)

		tcs = {
			"expected_results": {
				"output": {
					"0": {
						"simulation_id": "559402036",
						"message": {}
					}
				}
			},
			"appId": "sample_app"
		}
		tct = self.gson.fromJson(json.dumps(tcs), TestConfig)

		tcs = {
			"expectedResults": {
				"output": {
					"0": {
						"simulation_id": "559402036",
						"message": {
							"timestamp": 1535574871,
							"measurements": [{
								"angle": -122.66883087158203,
								"magnitude": 2438.561767578125,
								"measurement_mrid": "_84541f26-084d-4ea7-a254-ea43678d51f9"
							}, {
								"angle": 21.723935891052907,
								"magnitude": 45368.78524042436,
								"measurement_mrid": "_c48d8d88-12be-4b15-8b44-eedc752250c6"
							}, {
								"measurement_mrid": "_307E4291-5FEA-4388-B2E0-2B3D22FE8183",
								"value": 0
							}]
						}
					},
					"1": {
						"simulation_id": "559402036",
						"message": {
							"timestamp": 1535574872,
							"measurements": [{
								"angle": -38.381605233862224,
								"magnitude": 52769.16136465681,
								"measurement_mrid": "_84541f26-084d-4ea7-a254-ea43678d51f9"
							}, {
								"angle": 21.723935891052907,
								"magnitude": 45368.78524042436,
								"measurement_mrid": "_c48d8d88-12be-4b15-8b44-eedc752250c6"
							}, {
								"measurement_mrid": "_307E4291-5FEA-4388-B2E0-2B3D22FE8183",
								"value": 1
							}]
						}
					}
				}
			},
			"appId": "sample_app"
		}
		tct = self.gson.fromJson(json.dumps(tcs), TestConfig)
		self.assertIsNotNone(tct)
		self.assertIsNotNone(tct.get_expected_result_object())
		print("Expected")
		print(tct.get_expected_result_object())

	def test_parse_schedule(self):
		test_cfg1 = {
			"events": [{
				"allOutputOutage": False,
				"allInputOutage": False,
				"inputOutageList": [{
					"objectMrid": "_30E704EB-29F1-FA2C-D797-6E25DFEF0A9B",
					"attribute": "ShuntCompensator.sections"
				}, {
					"objectMrid": "_BFB56ABA-A1F4-E1C9-F43F-B6889A8336C6",
					"attribute": "ShuntCompensator.sections"
				}],
				"outputOutageList": ["_FF7722DD-151E-7018-10CA-297882C1A5AE"],
				"event_type": "CommOutage",
				"occuredDateTime": 1248130819,
				"stopDateTime": 1248130824
			}, {
				"PhaseConnectedFaultKind": "lineToLine",
				"FaultImpedance": {
					"rGround": 0.001,
					"xGround": 0.001
				},
				"ObjectMRID": ["235242342342342"],
				"phases": "ABC",
				"event_type": "Fault",
				"occuredDateTime": 1248130809,
				"stopDateTime": 1248130816
			}, {
				"message": {
					"forward_differences": [{
						"object": "1234",
						"attribute": "ShuntCompensator.sections",
						"value": "0"
					}],
					"reverse_differences": [{
						"object": "1234",
						"attribute": "ShuntCompensator.sections",
						"value": "1"
					}]
				},
				"event_type": "ScheduledCommandEvent",
				"occuredDateTime": 1248130812,
				"stopDateTime": 1248130842
			}],
			"appId": "sample_app"
		}
		tc = self.gson.fromJson(json.dumps(test_cfg1), TestConfig)
		event = tc.get_events()[2]
		print("Parsed ScheduledCommandEvent")
		print(event.getMessage())

	def create_scheduled_event(self):
		dm = {
			"forward_differences": [{
				"object": "1234",
				"attribute": "ShuntCompensator.sections",
				"value": "0"
			}],
			"reverse_differences": [{
				"object": "1234",
				"attribute": "ShuntCompensator.sections",
				"value": "1"
			}],
			"timestamp": 1248130812,
			"difference_mrid": "1234"
		}
		print(dm)

		schEvent = {
			"event_type": "ScheduledCommandEvent",
			"setMessage": dm,
			"setTimeInitiated": 1248130812,
			"setTimeCleared": 1248130812 + 30
		}
		return schEvent

	def test_scheduled_event(self):
		sch_event = self.create_scheduled_event()
		self.process_event.add_event(sch_event)

		status = self.process_event.get_status_json()
		print(status)
		start_time = 1248130809 - 19
		current_time = start_time
		duration = 120
		data_array = None

		while current_time <= start_time + duration:
			current_time += 3
			self.process_event.process_at_time(self.client, "1234", current_time)
			status = self.process_event.get_status_json()
			data_array = status.get("data")

		self.assertEqual(data_array[0]["status"], "CLEARED")


	def test_past_schedule(self):
		sch_event = self.create_scheduled_event()
		self.process_event.add_event(sch_event)

		status = self.process_event.get_status_json()
		print(status)
		data_array = status.get("data")
		self.assertEqual(data_array[0]["status"], "SCHEDULED")

		self.process_event.process_at_time(self.client, "1234", self.start_time + 1000)
		status = self.process_event.get_status_json()
		data_array = status.get("data")

		self.assertEqual(data_array[0]["status"], "CLEARED")


	def test_future_schedule(self):
		sch_event = self.create_scheduled_event()
		sch_event["time_initiated"] += 1000
		sch_event["time_cleared"] += 1000
		self.process_event.add_event(sch_event)

		status = self.process_event.get_status_json()
		print(status)
		data_array = status.get("data")
		self.assertEqual(data_array[0]["status"], "SCHEDULED")

		self.process_event.process_at_time(self.client, "1234", self.start_time)
		status = self.process_event.get_status_json()
		data_array = status.get("data")

		self.assertEqual(data_array[0]["status"], "CLEARED")


if __name__ == '__main__':
	unittest.main()

