import json
from DistComponent import DistComponent


class DistThermostat(DistComponent):
    sz_cim_class = "Thermostat"
    class ThermostatControlMode:
        COOLING = "COOLING"
        HEATING = "HEATING"

    def __init__(self, result):
        super().__init__()
        self.id = ""
        self.name = ""
        self.aggregatorName = ""
        self.baseSetpoint = 0.0
        self.controlMode = ""
        self.priceCap = 0.0
        self.rampHigh = 0.0
        self.rampLow = 0.0
        self.rangeHigh = 0.0
        self.rangeLow = 0.0
        self.useOverride = False
        self.usePredictive = False

        if result.hasNext():
            soln = result.next()
            self.name = self.safe_name(soln.get("?name").to"")
            self.id = soln.get("?voltage_id").to""
            self.aggregatorName = self.safe_name(soln.get("?aggregatorName").to"")
            self.baseSetpoint = float(soln.get("?baseSetpoint").to"")
            control_mode_index = int(soln.get("?controlMode").to"")
            self.controlMode = self.thermostat_control_mode(control_mode_index)
            self.priceCap = float(soln.get("?priceCap").to"")
            self.rampHigh = float(soln.get("?rampHigh").to"")
            self.rampLow = float(soln.get("?rampLow").to"")
            self.rangeHigh = float(soln.get("?rangeHigh").to"")
            self.rangeLow = float(soln.get("?rangeLow").to"")
            self.useOverride = bool(soln.get("?useOverride").to"")
            self.usePredictive = bool(soln.get("?usePredictive").to"")

    def display_string(self):
        buf = [f"{self.name} aggregatorName={self.aggregatorName} base setpoint={self.baseSetpoint: .4f}",
               f" control mode={self.controlMode} price capacity={self.priceCap: .4f}",
               f" ramp high={self.rampHigh: .4f} ramp low={self.rampLow: .4f}",
               f" range high={self.rangeHigh: .4f} range low={self.rangeLow: .4f}",
               f" use override={str(self.useOverride)} use predictive={str(self.usePredictive)}"]
        return "".join(buf)

    def get_key(self):
        return self.name

    def get_json_entry(self):
        return json.dumps({"name": self.name, "mRID": self.id})

    @staticmethod
    def thermostat_control_mode(index):
        if index == 0:
            return DistThermostat.ThermostatControlMode.COOLING
        elif index == 1:
            return DistThermostat.ThermostatControlMode.HEATING
