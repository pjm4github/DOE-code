from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.Reactance import Reactance
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.Resistance import Resistance
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.Susceptance import Susceptance
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.Temperature import Temperature
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Wires.Clamp import Clamp
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Wires.Conductor import Conductor

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 on Fri Dec 15 16:45:14 2023
from typing import Optional

from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Wires.NonlinearShuntCompensatorPhasePoint import Conductance


class ACLineSegment(Conductor):

    def __init__(self) -> None:
        super().__init__()
        self.b0ch: Susceptance = None  # Zero sequence shunt susceptance
        self.bch: Susceptance = None   # Positive sequence shunt susceptance
        self.g0ch: Conductance = None  # Zero sequence shunt conductance
        self.gch: Conductance = None   # Positive sequence shunt conductance
        self.r: Resistance = None     # Positive sequence series resistance
        self.r0: Resistance = None    # Zero sequence series resistance
        self.short_circuit_end_temperature: Temperature = None  # Maximum permitted temperature
        self.x: Reactance = None     # Positive sequence series reactance
        self.x0: Reactance = None    # Zero sequence series reactance
        self.clamp: Clamp = None  # Clamps connected to the line segment



    def get_b0ch(self) -> Optional[Susceptance]:
        return self.b0ch

    def get_bch(self) -> Optional[Susceptance]:
        return self.bch

    def get_clamp(self) -> Optional[Clamp]:
        return self.clamp

    def get_g0ch(self) -> Optional[Conductance]:
        return self.g0ch

    def get_gch(self) -> Optional[Conductance]:
        return self.gch

    def get_r(self) -> Optional[Resistance]:
        return self.r

    def get_r0(self) -> Optional[Resistance]:
        return self.r0

    def get_short_circuit_end_temperature(self) -> Optional[Temperature]:
        return self.short_circuit_end_temperature

    def get_x(self) -> Optional[Reactance]:
        return self.x

    def get_x0(self) -> Optional[Reactance]:
        return self.x0

    def set_b0ch(self, new_val: Susceptance) -> None:
        self.b0ch = new_val

    def set_bch(self, new_val: Susceptance) -> None:
        self.bch = new_val

    def set_clamp(self, new_val: Clamp) -> None:
        self.clamp = new_val

    def set_g0ch(self, new_val: Conductance) -> None:
        self.g0ch = new_val

    def set_gch(self, new_val: Conductance) -> None:
        self.gch = new_val

    def set_r(self, new_val: Resistance) -> None:
        self.r = new_val

    def set_r0(self, new_val: Resistance) -> None:
        self.r0 = new_val

    def set_short_circuit_end_temperature(self, new_val: Temperature) -> None:
        self.short_circuit_end_temperature = new_val

    def set_x(self, new_val: Reactance) -> None:
        self.x = new_val

    def set_x0(self, new_val: Reactance) -> None:
        self.x0 = new_val
