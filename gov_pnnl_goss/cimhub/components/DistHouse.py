from enum import Enum
import random

from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistHouse(DistComponent):
    sz_cim_class = "House"

    class HouseCooling(Enum):
        none = "none"
        electric = "electric"
        heat_pump = "heatPump"

    class HouseHeating(Enum):
        none = "none"
        gas = "gas"
        heat_pump = "heatPump"
        resistance = "resistance"

    class HouseThermalIntegrity(Enum):
        unknown = "unknown"
        very_little = "veryLittle"
        normal = "normal"
        above_normal = "aboveNormal"
        below_normal = "belowNormal"
        good = "good"
        very_good = "veryGood"
        little = "little"

    gld_house_cooling = {
        HouseCooling.none: "NONE",
        HouseCooling.electric: "ELECTRIC",
        HouseCooling.heat_pump: "HEAT_PUMP"
    }

    gld_house_heating = {
        HouseHeating.none: "NONE",
        HouseHeating.gas: "GAS",
        HouseHeating.heat_pump: "HEAT_PUMP",
        HouseHeating.resistance: "RESISTANCE"
    }

    gld_house_thermal_integrity = {
        HouseThermalIntegrity.unknown: "UNKNOWN",
        HouseThermalIntegrity.very_little: "VERY_LITTLE",
        HouseThermalIntegrity.normal: "NORMAL",
        HouseThermalIntegrity.above_normal: "ABOVE_NORMAL",
        HouseThermalIntegrity.below_normal: "BELOW_NORMAL",
        HouseThermalIntegrity.good: "GOOD",
        HouseThermalIntegrity.very_good: "VERY_GOOD",
        HouseThermalIntegrity.little: "LITTLE"
    }

    def __init__(self):
        super().__init__()
        self.id = None
        self.name = None
        self.parent = None
        self.cooling_setpoint = None
        self.cooling_system = None
        self.floor_area = None
        self.heating_setpoint = None
        self.heating_system = None
        self.hvac_power_factor = None
        self.number_of_stories = None
        self.thermal_integrity = None

    def init_from_query_solution(self, soln):
        self.name = self.safe_name(soln.get("?name").to"")
        self.id = soln.get("?voltage_id").to""
        self.parent = self.safe_name(soln.get("?parent").to"")
        self.cooling_setpoint = float(self.optional_string(soln, "?coolingSetpoint", "200.0"))
        self.cooling_system = self.HouseCooling(soln.get("?coolingSystem").to"")
        self.floor_area = float(soln.get("?floorArea").to"")
        self.heating_setpoint = float(self.optional_string(soln, "?heatingSetpoint", "-100.0"))
        self.heating_system = self.HouseHeating(soln.get("?heatingSystem").to"")
        self.hvac_power_factor = float(self.optional_string(soln, "?hvacPowerFactor", "1.0"))
        try:
            self.number_of_stories = int(soln.get("?numberOfStories").to"")
        except ValueError:
            self.number_of_stories = int(float(soln.get("?numberOfStories").to""))
        self.thermal_integrity = self.HouseThermalIntegrity(soln.get("?thermalIntegrity").to"")

    def display_string(self):
        buf = []
        buf.append(f"{self.name} @ {self.parent}")
        buf.append(f"cooling setpoint={self.cooling_setpoint:.3f} cooling system={self.cooling_system.name}")
        buf.append(f"floor area={self.floor_area:.2f} heating setpoint={self.heating_setpoint:.3f}")
        buf.append(f"heating system={self.heating_system.name} hvac power factor={self.hvac_power_factor:.4f}")
        buf.append(f"number of stories={self.number_of_stories}")
        buf.append(f"thermal integrity={self.thermal_integrity.name}")
        return ' '.join(buf)

    def get_key(self):
        return self.name

    def get_json_entry(self):
        return f'{{"name":"{self.name}","mRID":"{self.id}"}}'

    def get_glm(self, r: random.Random):
        local_heat_set = self.heating_setpoint
        skew_value = 2700.0 * r.random()
        scalar1 = 324.9 * self.floor_area ** 0.442 / 8907.0
        scalar2 = 0.8 + 0.4 * r.random()
        scalar3 = 0.8 + 0.4 * r.random()
        resp_scalar = scalar1 * scalar2
        unresp_scalar = scalar1 * scalar3
        techdata = [0.9, 1.0, 0.9, 1.0, 0.0, 1.0, 0.0]

        buf = []
        buf.append(f"object house {{")
        buf.append(f"  name \"{self.name}\";")
        buf.append(f"  parent \"ld_{self.parent}_ldmtr\";")
        buf.append(f"  floor_area {self.floor_area:.2f};")
        buf.append(f"  number_of_stories {self.number_of_stories};")
        buf.append(f"  thermal_integrity_level {self.gld_house_thermal_integrity[self.thermal_integrity]};")
        buf.append(f"  cooling_system_type {self.gld_house_cooling[self.cooling_system]};")
        buf.append(f"  cooling_setpoint {self.cooling_setpoint:.3f};")
        if self.heating_system != self.HouseHeating.none:
            buf.append(f"  heating_system_type {self.gld_house_heating[self.heating_system]};")
            buf.append(f"  heating_setpoint {self.heating_setpoint:.3f};")
        elif self.cooling_system != self.HouseCooling.none:
            buf.append(f"  heating_setpoint {self.heating_setpoint:.3f}; "
                       f"// because GridLAB-D will override to RESISTANCE heating")
        if self.heating_system != self.HouseHeating.none or self.cooling_system != self.HouseCooling.none:
            buf.append(f"  hvac_power_factor {self.hvac_power_factor:.4f};")
        buf.append(f"  object ZIPload {{ // responsive")
        buf.append(f"    schedule_skew {skew_value:.2f};")
        buf.append(f"    base_power responsive_loads*{resp_scalar:.6f};")
        buf.append(f"    heatgain_fraction {techdata[0]:.2f};")
        buf.append(f"    impedance_pf {techdata[1]:.2f};")
        buf.append(f"    current_pf {techdata[2]:.2f};")
        buf.append(f"    power_pf {techdata[3]:.2f};")
        buf.append(f"    impedance_fraction {techdata[4]:.2f};")
        buf.append(f"    current_fraction {techdata[5]:.2f};")
        buf.append(f"    power_fraction {techdata[6]:.2f};")
        buf.append(f"  }};")
        buf.append(f"  object ZIPload {{ // unresponsive")
        buf.append(f"    schedule_skew {skew_value:.2f};")
        buf.append(f"    base_power unresponsive_loads*{unresp_scalar:.6f};")
        buf.append(f"    heatgain_fraction {techdata[0]:.2f};")
        buf.append(f"    impedance_pf {techdata[1]:.2f};")
        buf.append(f"    current_pf {techdata[2]:.2f};")
        buf.append(f"    power_pf {techdata[3]:.2f};")
        buf.append(f"    impedance_fraction {techdata[4]:.2f};")
        buf.append(f"    current_fraction {techdata[5]:.2f};")
        buf.append(f"    power_fraction {techdata[6]:.2f};")
        buf.append(f"  }};")
        buf.append(f"}}")
        return '\n'.join(buf)
