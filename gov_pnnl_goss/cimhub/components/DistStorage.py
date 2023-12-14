import json
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent

import math


class DistStorage(DistComponent):
    sz_cim_class = "Storage"
    sz_csv_header = "Name,NumPhases,Bus,Phases,kV,kVA,Capacity,Connection,kW,pf,kWh,State"

    def __init__(self, results):
        super().__init__()
        self.id = ""
        self.name = ""
        self.bus = ""
        self.phases = ""
        self.state = ""
        self.p = 0.0
        self.q = 0.0
        self.ratedU = 0.0
        self.ratedS = 0.0
        self.ratedE = 0.0
        self.storedE = 0.0
        self.maxIFault = 0.0
        self.bDelta = False

        if results:
            if results.hasNext():
                soln = results.next()
                self.name = self.safe_name(soln["name"].toString())
                self.id = soln["voltage_id"].toString()
                self.bus = self.safe_name(soln["bus"].toString())
                self.phases = self.optional_string(soln, "?phases", "ABC")
                self.phases = self.phases.replace('\n', ':')
                self.p = float(soln["precisions"].toString())
                self.q = float(soln["q"].toString())
                self.ratedU = float(soln["ratedU"].toString())
                self.ratedS = float(soln["ratedS"].toString())
                self.maxIFault = float(soln["ipu"].toString())
                self.bDelta = False
                self.ratedE = float(soln["ratedE"].toString())
                self.storedE = float(soln["storedE"].toString())
                self.state = soln["state"].toString()

    def get_json_entry(self):
        return json.dumps({
            "name": self.name,
            "mRID": self.id,
            "CN1": self.bus,
            "phases": self.phases,
            "ratedS": format(self.ratedS, ".1f"),
            "ratedU": format(self.ratedU, ".1f"),
            "precisions": format(self.p, ".1f"),
            "q": format(self.q, ".1f"),
            "ratedE": format(self.ratedE, ".1f"),
            "storedE": format(self.storedE, ".1f"),
            "batteryState": self.state
        })

    @staticmethod
    def dss_battery_state(s):
        if s == "Charging":
            return "charging"
        if s == "Discharging":
            return "discharging"
        if s == "Waiting":
            return "idling"
        if s == "Full":
            return "idling"
        if s == "Empty":
            return "idling"
        return "idling"

    def display_string(self):
        s = f"{self.name} @ {self.bus} phases={self.phases} vnom={format(self.ratedU, '.4f')} " \
            f"vanom={format(self.ratedS, '.4f')} kw={format(0.001 * self.p, '.4f')} " \
            f"kvar={format(0.001 * self.q, '.4f')} capacity={format(0.001 * self.ratedE, '.4f')} " \
            f"stored={format(0.001 * self.storedE, '.4f')} {self.dss_battery_state(self.state)} " \
            f"ilimit={format(self.maxIFault, '.4f')}"
        return s

    def get_json_symbols(self, mapper):
        pt = mapper.get(f"BatteryUnit:{self.name}:1")
        return json.dumps({
            "name": self.name,
            "parent": self.bus,
            "phases": self.phases,
            "kva": format(0.001 * self.ratedS, ".1f"),
            "x1": format(pt.x, ".1f"),
            "y1": format(pt.y, ".1f")
        })

    def get_glm(self):
        buf = ["object inverter {",
               f"  name \"inv_bat_{self.name}\";",
               f"  parent \"{self.bus}_stmtr\";"]
        if self.bDelta and "D" not in self.phases:
            buf.append(f"  phases {self.phases.replace(':', '')}D;")
        elif "S" not in self.phases and "N" not in self.phases:
            buf.append(f"  phases {self.phases.replace(':', '')}N;")
        else:
            buf.append(f"  phases {self.phases.replace(':', '')};")
        buf.append("  generator_status ONLINE;")
        buf.append("  generator_mode CONSTANT_PQ;")
        buf.append("  inverter_type FOUR_QUADRANT;")
        buf.append("  four_quadrant_control_mode CONSTANT_PQ; // LOAD_FOLLOWING;")
        buf.append("  charge_lockout_time 1;")
        buf.append("  discharge_lockout_time 1;")
        buf.append(f"  sense_object \"{self.bus}_stmtr\";")
        buf.append(f"  charge_on_threshold {format(-0.02 * self.ratedS, '.3f')};")
        buf.append(f"  charge_off_threshold {format(0.0 * self.ratedS, '.3f')};")
        buf.append(f"  discharge_off_threshold {format(0.4 * self.ratedS, '.3f')};")
        buf.append(f"  discharge_on_threshold {format(0.6 * self.ratedS, '.3f')};")
        buf.append("  inverter_efficiency 0.975;")
        buf.append(f"  V_base {format(self.ratedU, '.3f')};")
        buf.append(f"  rated_power {format(self.ratedS, '.3f')};")
        buf.append(f"  max_charge_rate {format(self.ratedS, '.3f')};")
        buf.append(f"  max_discharge_rate {format(self.ratedS, '.3f')};")
        buf.append(f"  P_Out {format(self.p, '.3f')};")
        buf.append(f"  Q_Out {format(self.q, '.3f')};")
        buf.append("  object battery {")
        buf.append(f"    name \"bat_{self.name}\";")
        buf.append("    nominal_voltage 48;")
        buf.append(f"    battery_capacity {format(self.ratedE, '.1f')};")
        buf.append(f"    state_of_charge {format(self.storedE / self.ratedE, '.4f')};")
        buf.append("    use_internal_battery_model true;")
        buf.append("    generator_mode CONSTANT_PQ;")
        buf.append("    generator_status ONLINE;")
        buf.append("    battery_type LI_ION;")
        buf.append("    round_trip_efficiency 0.86;")
        buf.append(f"    rated_power {format(self.ratedS, '.3f')};")
        buf.append("  };")
        buf.append("}")
        return '\n'.join(buf)

    def get_dss(self):
        nphases = self.dss_phase_count(self.phases, self.bDelta)
        kv = 0.001 * self.ratedU
        kva = 0.001 * self.ratedS
        if nphases < 2:
            kv /= math.sqrt(3.0)
        s = math.sqrt(self.p * self.p + self.q * self.q)
        pf = 1.0
        if s > 0.0:
            pf = self.p / s
        if self.q < 0.0:
            pf *= -1.0
        return (
            f"new Storage.{self.name} phases={nphases} "
            f"bus1={self.dss_shunt_phases(self.bus, self.phases, self.bDelta)} "
            f"conn={self.dss_conn(self.bDelta)} kva={format(kva, '.3f')} kv={format(kv, '.3f')} "
            f"kwhrated={0.001 * self.ratedE:.3f} kwhstored={0.001 * self.storedE:.3f} "
            f"state={self.dss_battery_state(self.state)} "
            f"vminpu={1 / self.maxIFault:.4f} LimitCurrent=yes kw={self.p / 1000.0:.2f}")

    def get_csv(self):
        nphases = self.dss_phase_count(self.phases, self.bDelta)
        kv = 0.001 * self.ratedU
        kva = 0.001 * self.ratedS
        if nphases < 2:
            kv /= math.sqrt(3.0)
        s = math.sqrt(self.p * self.p + self.q * self.q)
        pf = 1.0
        if s > 0.0:
            pf = self.p / s
        if self.q < 0.0:
            pf *= -1.0
        return (f"{self.name},{nphases},{self.bus},{self.csv_phase_string(self.phases)},"
                f"{kv:.3f},{kva:.3f},{0.001 * self.ratedE:.3f},{self.dss_conn(self.bDelta)},"
                f"{0.001 * self.p:.3f},{pf:.4f},{0.001 * self.storedE:.3f},"
                f"{self.dss_battery_state(self.state)}")

    def get_key(self):
        return self.name

    def csv_header(self):
        return self.sz_csv_header
