# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json
from enum import Enum

from gov_pnnl_goss.SpecialClasses import Gson
from gov_pnnl_goss.core.Event import Event


class Fault(Event):
    serial_version_UID = 7348798730580951117

    class PhaseConnectedFaultKind(Enum):
        line_to_ground = 0
        line_to_line = 1
        line_to_line_to_ground = 2
        line_open = 3

    class FaultImpedance(Enum):
        r_ground = 0
        r_line_to_line = 1
        x_ground = 2
        x_line_to_line = 3

    class PhaseCode(Enum):
        ABCN = 225
        ABC = 224
        ABN = 193
        ACN = 41
        BCN = 97
        AB = 132
        AC = 96
        BC = 65
        AN = 129
        BN = 65
        CN = 33
        A = 128
        B = 64
        C = 32
        N = 16
        s1N = 528
        s2N = 272
        s12N = 784
        s1 = 512
        s2 = 256
        s12 = 768
        none = 0
        X = 1024
        XY = 3072
        XN = 1040
        XYN = 3088

        def __init__(self, newValue):
            self.value = newValue

        def get_value(self):
            return self.value

    def __init__(self):
        super().__init__()
        self.fault_impedance = {}
        self.phase_connected_fault_kind = None
        self.object_mrid = []
        self.phases = None

    def get_fault_impedance(self):
        return self.fault_impedance

    def set_fault_impedance(self, impedance):
        self.fault_impedance = impedance

    def get_phase_connected_fault_kind(self):
        return self.phase_connected_fault_kind

    def set_phase_connected_fault_kind(self, phase_connect_fault_kind):
        self.phase_connected_fault_kind = phase_connect_fault_kind

    def get_object_mrid(self):
        return self.object_mrid

    def set_object_mrid(self, object_mrid):
        self.object_mrid = object_mrid

    def get_phases(self):
        return self.phases

    def set_phases(self, phases):
        self.phases = phases

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        gson = Gson()
        obj = gson.from_json(json_string, Fault)
        # TODO: Check for mandatory fields and impedance-faultKind combination
        return obj
