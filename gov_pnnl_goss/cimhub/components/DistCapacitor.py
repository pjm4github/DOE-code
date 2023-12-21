import math
import json
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistCapacitor(DistComponent):
    sz_cim_class = "Capacitor"
    sz_csv_header = "Name,Bus,Phases,kV,kVAR,NumPhases,Connection"

    def __init__(self, results):
        super().__init__()
        self.bDelta = False
        self.basev = 0.0
        self.bus = ""
        self.conn = ""
        self.ctrl = "false"
        self.deadband = 0.0
        self.delay = 0.0
        self.grnd = ""
        self.id = ""
        self.kvar = 0.0
        self.kvar_A = 0.0
        self.kvar_B = 0.0
        self.kvar_C = 0.0
        self.mode = ""
        self.monbus = ""
        self.monclass = ""
        self.moneq = ""
        self.monphs = ""
        self.name = ""
        self.nomu = 0.0
        self.nphases = 0
        self.phs = "ABC"
        self.setpoint = 0.0

        if results:
            if results.has_next():
                soln = results.next()
                self.name = self.safe_name(soln.get("?name").to"")
                self.id = soln.get("?voltage_id").to""
                self.bus = self.safe_name(soln.get("?bus").to"")
                self.basev = float(soln.get("?basev").to"")
                self.phs = self.optional_string(soln, "?phs", "ABC")
                self.conn = soln.get("?conn").to""
                self.grnd = soln.get("?grnd").to""
                self.ctrl = self.optional_string(soln, "?ctrlenabled", "false")
                self.nomu = float(soln.get("?nomu").to"")
                bsection = float(soln.get("?bsection").to"")
                self.kvar = self.nomu * self.nomu * bsection / 1000.0
                if self.ctrl == "true":
                    self.mode = soln.get("?mode").to""
                    self.setpoint = float(soln.get("?setpoint").to"")
                    self.deadband = float(soln.get("?deadband").to"")
                    self.delay = float(soln.get("?delay").to"")
                    self.moneq = soln.get("?moneq").to""
                    self.monclass = soln.get("?monclass").to""
                    self.monbus = soln.get("?monbus").to""
                    self.monphs = soln.get("?monphs").to""
                self.set_derived_parameters()

    def get_json_entry(self):
        buf = {
            "name": self.name,
            "mRID": self.id,
            "CN1": self.bus,
            "phases": self.phs,
            "kvar_A": round(self.kvar_A, 1),
            "kvar_B": round(self.kvar_B, 1),
            "kvar_C": round(self.kvar_C, 1),
            "nominalVoltage": round(self.basev, 1),
            "nomU": round(self.nomu, 1),
            "phaseConnection": self.conn,
            "grounded": self.grnd.lower(),
            "enabled": self.ctrl.lower(),
            "mode": self.mode if self.mode else None,
            "targetValue": round(self.setpoint, 1),
            "targetDeadband": round(self.deadband, 1),
            "aVRDelay": round(self.delay, 1),
            "monitoredName": self.moneq if self.moneq else None,
            "monitoredClass": self.monclass if self.monclass else None,
            "monitoredBus": self.monbus if self.monbus else None,
            "monitoredPhase": self.monphs if self.monphs else None,
        }
        return json.dumps(buf)

    @staticmethod
    def dss_cap_mode(s):
        if s == "currentFlow":
            return "current"
        if s == "voltage":
            return "voltage"
        if s == "reactivePower":
            return "kvar"
        if s == "timeScheduled":
            return "time"
        if s == "powerFactor":
            return "pf"
        if s == "userDefined":
            return "time"  # i.e. unsupported in CIM
        return "time"

    def set_derived_parameters(self):
        bA = 0
        bB = 0
        bC = 0
        if "A" in self.phs:
            bA = 1
        if "B" in self.phs:
            bB = 1
        if "C" in self.phs:
            bC = 1
        kvar_ph = self.kvar / (bA + bB + bC)
        self.kvar_A = kvar_ph * bA
        self.kvar_B = kvar_ph * bB
        self.kvar_C = kvar_ph * bC
        self.bDelta = self.conn == "D"
        self.nphases = bA + bB + bC

    def glm_cap_mode(self, s):
        if s == "currentFlow":
            return "CURRENT"
        if s == "voltage":
            return "VOLT"
        if s == "reactivePower":
            return "VAR"
        if s == "timeScheduled":
            return "MANUAL"  # TODO - support in GridLAB-D?
        if s == "powerFactor":
            return "MANUAL"  # TODO - support in GridLAB-D?
        if s == "userDefined":
            return "MANUAL"
        return "time"

    def display_string(self):
        buf = f"{self.name} @ {self.bus} on {self.phs} basev={round(self.basev, 4)}"
        buf += f" {round(self.nomu / 1000.0, 4)} [kV] {round(self.kvar, 4)} [kvar] conn={self.conn} grnd={self.grnd}"
        if self.ctrl == "true":
            buf += f"\n  control mode={self.mode} set={round(self.setpoint, 4)} bandwidth={round(self.deadband, 4)} delay={round(self.delay, 4)}"
            buf += f" monitoring: {self.moneq}:{self.monclass}:{self.monbus}:{self.monphs}"
        return buf

    def get_json_symbols(self, map):
        pt = map.get(f"LinearShuntCompensator:{self.name}:1")
        buf = {
            "name": self.name,
            "parent": self.bus,
            "phases": self.phs,
            "kvar_A": round(self.kvar_A, 1),
            "kvar_B": round(self.kvar_B, 1),
            "kvar_C": round(self.kvar_C, 1),
            "x1": round(pt.x, 1),
            "y1": round(pt.y, 1),
        }
        return json.dumps(buf)

    def get_glm(self):
        buf = f"object capacitor {{\n"
        buf += f"  name \"cap_{self.name}\";\n"
        buf += f"  parent \"{self.bus}\";\n"
        if self.bDelta:
            buf += f"  phases {self.phs}D;\n"
            buf += f"  phases_connected {self.phs}D;\n"
        else:
            buf += f"  phases {self.phs}N;\n"
            buf += f"  phases_connected {self.phs}N;\n"
        gld_nomu = self.nomu
        if self.nphases > 1:
            gld_nomu /= math.sqrt(3.0)
        buf += f"  cap_nominal_voltage {round(gld_nomu, 2)};\n"
        buf += f"  nominal_voltage {round(gld_nomu, 2)};\n"
        if self.kvar_A > 0.0:
            buf += f"  capacitor_A {round(self.kvar_A * 1000.0, 2)};\n"
            buf += f"  switchA CLOSED;\n"
        if self.kvar_B > 0.0:
            buf += f"  capacitor_B {round(self.kvar_B * 1000.0, 2)};\n"
            buf += f"  switchB CLOSED;\n"
        if self.kvar_C > 0.0:
            buf += f"  capacitor_C {round(self.kvar_C * 1000.0, 2)};\n"
            buf += f"  switchC CLOSED;\n"
        if self.ctrl == "true":
            glmMode = self.glm_cap_mode(self.mode)
            dOn = self.setpoint - 0.5 * self.deadband
            dOff = self.setpoint + 0.5 * self.deadband
            buf += f"  control MANUAL; // {glmMode};\n"
            if glmMode == "VOLT":
                buf += f"  voltage_set_low {round(dOn, 2)};\n"
                buf += f"  voltage_set_high {round(dOff, 2)};\n"
            elif glmMode == "CURRENT":
                buf += f"  current_set_low {round(dOn, 2)};\n"
                buf += f"  current_set_high {round(dOff, 2)};\n"
            elif glmMode == "VAR":
                buf += f"  VAr_set_low {round(dOff, 2)};\n"
                buf += f"  VAr_set_high {round(dOn, 2)};\n"
            elif self.mode == "timeScheduled":
                buf += f"  // CIM timeScheduled on={round(dOn, 2)} off={round(dOff, 2)};\n"
            glmClass = self.glm_class_prefix(self.monclass)
            if glmClass != "cap" or self.moneq != self.name:
                buf += f"  remote_sense \"{glmClass}_{self.moneq}\";\n"
            buf += f"  pt_phase {self.monphs};\n"
            if len(self.monphs) > 1:
                buf += f"  control_level INDIVIDUAL;\n"
            else:
                buf += f"  control_level BANK;\n"
            buf += f"  dwell_time {round(self.delay, 2)};\n"
        buf += f"}}\n"
        return buf

    def get_dss(self):
        buf = f"new Capacitor.{self.name}"
        buf += f" phases={self.dss_phase_count(self.phs, self.bDelta)} bus1={self.dss_shunt_phases(self.bus, self.phs, self.bDelta)}"
        buf += f" conn={self.dss_conn(self.bDelta)} kv={round(0.001 * self.nomu, 2)} kvar={round(self.kvar, 2)}"
        buf += "\n"
        if self.ctrl == "true":
            dssClass = self.dss_class_prefix(self.monclass)
            dOn = self.setpoint - 0.5 * self.deadband
            dOff = self.setpoint + 0.5 * self.deadband
            if self.mode == "reactivePower":
                dOn /= 1000.0
                dOff /= 1000.0
            nterm = 1  # TODO: need to search for this
            buf += f"new CapControl.{self.name} capacitor={self.name} type={self.dss_cap_mode(self.mode)}"
            buf += f" on={round(dOn, 2)} off={round(dOff, 2)} delay={round(self.delay, 2)} delayoff={round(self.delay, 2)}"
            buf += f" element={dssClass}.{self.moneq} terminal={nterm} ptratio=1 ptphase={self.first_dss_phase(self.monphs)}"
            buf += "\n"
        return buf

    def sz_csv_cap_header(self):
        return self.sz_csv_header

    @staticmethod
    def sz_csv_cap_control_header():
        return "Name,Capacitor,MonitoredElement,ElementTerminal,Type,PTRatio,CTRatio,ONSetting,OFFSetting"

    def get_cap_csv(self):
        nphases = self.dss_phase_count(self.phs, self.bDelta)
        buf = f"{self.name},{self.bus},{self.csv_phase_string(self.phs)},"
        buf += f"{round(0.001 * self.nomu, 2)},{round(self.kvar, 2)},{nphases},{self.dss_conn(self.bDelta)}\n"
        return buf

    def get_cap_control_csv(self):
        if self.ctrl == "false":
            return ""
        dssClass = self.dss_class_prefix(self.monclass)
        dOn = self.setpoint - 0.5 * self.deadband
        dOff = self.setpoint + 0.5 * self.deadband
        if self.mode == "reactivePower":
            dOn /= 1000.0
            dOff /= 1000.0
        nterm = 1  # TODO: need to search for this

        buf = f"{self.name},{self.name},{dssClass}.{self.moneq},"
        buf += f"{nterm},{self.dss_cap_mode(self.mode)},1,1,{round(dOn, 2)},{round(dOff, 2)}\n"

        return buf

    def get_key(self) -> str:
        return self.name

