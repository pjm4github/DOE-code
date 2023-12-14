# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json
import random
from enum import Enum


class TestType(Enum):
    simulation_vs_expected = 1
    simulation_vs_timeseries = 2
    expected_vs_timeseries = 3
    timeseries_vs_timeseries = 4


class TestConfig:
    serial_version_UID = 1

    def __init__(self):
        self.events = []
        self.rules = []
        self.expected_results = {}
        self.test_input = True
        self.test_output = True
        self.compare_with_sim_id = ""
        self.compare_with_sim_id_two = ""
        self.app_id = ""
        self.test_id = f"{random.randint(0, 65535)}"
        self.test_type = TestType.simulation_vs_expected
        self.store_matches = False

    def get_expected_result_object(self):
        return self.expected_results

    def set_expected_result_object(self, expected_results):
        self.expected_results = expected_results

    def get_events(self):
        return self.events

    def set_events(self, events):
        self.events = events

    def get_rules(self):
        return self.rules

    def set_rules(self, rules):
        self.rules = rules

    def get_test_input(self):
        return self.test_input

    def set_test_input(self, test_input):
        self.test_input = test_input

    def get_test_output(self):
        return self.test_output

    def set_test_output(self, test_output):
        self.test_output = test_output

    def get_compare_with_sim_id(self):
        return self.compare_with_sim_id

    def set_compare_with_sim_id(self, compare_with_sim_id):
        self.compare_with_sim_id = compare_with_sim_id

    def get_compare_with_sim_id_two(self):
        return self.compare_with_sim_id_two

    def set_compare_with_sim_id_two(self, compare_with_sim_id_two):
        self.compare_with_sim_id_two = compare_with_sim_id_two

    def get_app_id(self):
        return self.app_id
    
    def set_app_id(self, app_id):
        self.app_id = app_id

    def get_test_id(self):
        return self.test_id

    def set_test_id(self, test_id):
        self.test_id = test_id

    def get_test_type(self):
        return self.test_type

    def set_test_type(self, test_type):
        self.test_type = test_type

    def get_store_matches(self):
        return self.store_matches

    def set_store_matches(self, store_matches):
        self.store_matches = store_matches

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        return json.loads(json_string)
