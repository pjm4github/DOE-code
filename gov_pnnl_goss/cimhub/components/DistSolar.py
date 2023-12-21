import json
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent

import math


class DistSolar(DistComponent):
    sz_cim_class = "Solar"
    sz_csv_header = "Name,NumPhases,Bus,Phases,kV,kVA,Connection,kW,pf"

    def __init__(self, results):
        super().__init__()
        self.id = ""
        self.name = ""
        self.bus = ""
        self.phases = ""
        self.p = 0.0
        self.q = 0.0
        self.ratedU = 0.0
        self.ratedS = 0.0
        self.maxIFault = 0.0
        self.bDelta = False

        if results:
            if results.hasNext():
                soln = results.next()
                self.name = self.safe_name(soln["name"].to"")
                self.id = soln["voltage_id"].to""
                self.bus = self.safe_name(soln["bus"].to"")
                self.phases = self.optional_string(soln, "?phases", "ABC")
                self.phases = self.phases.replace('\n', ':')
                self.p = float(soln["precisions"].to"")
                self.q = float(soln["q"].to"")
                self.ratedU = float(soln["ratedU"].to"")
                self.ratedS = float(soln["ratedS"].to"")
                self.maxIFault = float(soln["ipu"].to"")
                self.bDelta = False

    def get_json_entry(self):
        return json.dumps({
            "name": self.name,
            "mRID": self.id,
            "CN1": self.bus,
            "phases": self.phases,
            "ratedS": format(self.ratedS, ".1f"),
            "ratedU": format(self.ratedU, ".1f"),
            "precisions": format(self.p, ".3f"),
            "q": format(self.q, ".3f"),
            "maxIFault": format(self.maxIFault, ".3f")
        })

    def display_string(self):
        return f"{self.name} @ {self.bus} phases={self.phases} vnom={format(self.ratedU, '.4f')} vanom={format(self.ratedS, '.4f')} kw={format(0.001 * self.p, '.4f')} kvar={format(0.001 * self.q, '.4f')} ilimit={format(self.maxIFault, '.4f')}"

    def get_json_symbols(self, map):
        pt = map.get(f"PhotovoltaicUnit:{self.name}:1")
        return json.dumps({
            "name": self.name,
            "parent": self.bus,
            "phases": self.phases,
            "kva": format(0.001 * self.ratedS, ".1f"),
            "x1": format(pt.x, ".1f"),
            "y1": format(pt.y, ".1f")
        })

    def get_glm(self):
        buf = []
        buf.append("object inverter {")
        buf.append(f"  name \"inv_pv_{self.name}\";")
        buf.append(f"  parent \"{self.bus}_pvmtr\";")
        if self.bDelta and "D" not in self.phases:
            buf.append(f"  phases {self.phases.replace(':', '')}D;")
        elif "S" not in self.phases and "N" not in self.phases:
            buf.append(f"  phases {self.phases.replace(':', '')}N;")
        else:
            buf.append(f"  phases {self.phases.replace(':', '')};")
        buf.append("  generator_status ONLINE;")
        buf.append("  four_quadrant_control_mode CONSTANT_PQ;")
        buf.append("  inverter_type FOUR_QUADRANT;")
        buf.append("  inverter_efficiency 1.0;")
        buf.append("  power_factor 1.0;")
        buf.append(f"  V_base {format(self.ratedU, '.3f')};")
        buf.append(f"  rated_power {format(self.ratedS, '.3f')};")
        buf.append(f"  P_Out {format(self.p, '.3f')};")
        buf.append(f"  Q_Out {format(self.q, '.3f')};")
        buf.append("  object solar {")
        buf.append(f"    name \"pv_{self.name}\";")
        buf.append("    generator_mode SUPPLY_DRIVEN;")
        buf.append("    generator_status ONLINE;")
        buf.append("    panel_type SINGLE_CRYSTAL_SILICON;")
        buf.append("    efficiency 0.2;")
        buf.append(f"    rated_power {format(self.ratedS, '.3f')};")
        buf.append("  };")
        buf.append("}")
        return "\n".join(buf)

    def get_dss(self):
        buf = []
        buf.append(f"new PVSystem.{self.name}")
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
        buf.append(
            f" phases={nphases} bus1={self.dss_shunt_phases(self.bus, self.phases, self.bDelta)} conn={self.dss_conn(self.bDelta)} kva={format(kva, '.3f')} kv={format(kv, '.3f')} pmpp={format(kva, '.3f')} irrad={format(0.001 * self.p / kva, '.3f')} pf={format(pf, '.4f')} vminpu={format(1.0 / self.maxIFault, '.4f')} LimitCurrent=yes")
        return "".join(buf)

    @staticmethod
    def get_csv_header():
        return "Name,NumPhases,Bus,Phases,kV,kVA,Connection,kW,pf"

    def csv_header(self):
        return self.sz_csv_header

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
        s = f"{self.name},{nphases},{self.bus},{self.csv_phase_string(self.phases)}," \
            f"{format(kv, '.3f')},{format(kva, '.3f')},{self.dss_conn(self.bDelta)}," \
            f"{format(0.001 * self.p, '.4f')},{format(pf, '.4f')}\n"
        return s

    def get_key(self):
        return self.name
