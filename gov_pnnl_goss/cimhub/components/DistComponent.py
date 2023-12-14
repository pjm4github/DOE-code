from abc import abstractmethod
from typing import Dict


class DistComponent:
    sz_cim_class = "Component"
    nsCIM = "http://iec.ch/TC57/CIM100#"
    nsRDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    nsXSD = "http://www.w3.org/2001/XMLSchema#"

    def __init__(self):
        self.g_freq = 60.0
        self.g_omega = 377.0
        self.g_m_per_mile = 1609.3
        self.g_ft_per_m = 1.0 / 0.3048

    @staticmethod
    def optional_string(soln, parm, def_val):
        nd = soln.get(parm)
        if nd is not None:
            str_val = str(nd)
            if len(str_val) > 0:
                return str_val
        return def_val

    @staticmethod
    def optional_int(soln, parm, def_val):
        nd = soln.get(parm)
        if nd is not None:
            str_val = str(nd)
            if len(str_val) > 0:
                return int(str_val)
        return def_val

    @staticmethod
    def optional_double(soln, parm, def_val):
        nd = soln.get(parm)
        if nd is not None:
            str_val = str(nd)
            if len(str_val) > 0:
                return float(str_val)
        return def_val

    @staticmethod
    def optional_boolean(soln, parm, def_val):
        nd = soln.get(parm)
        if nd is not None:
            str_val = str(nd)
            if len(str_val) > 0:
                return str_val.lower() == 'true'
        return def_val

    @staticmethod
    def gld_bus_name(arg):
        return "nd_" + arg

    @staticmethod
    def safe_name(arg):
        if arg is None:
            return None
        s = arg.replace(' ', '_')
        s = s.replace('.', '_')
        s = s.replace('=', '_')
        s = s.replace('+', '_')
        s = s.replace('^', '_')
        s = s.replace('$', '_')
        s = s.replace('*', '_')
        s = s.replace('|', '_')
        s = s.replace('[', '_')
        s = s.replace(']', '_')
        s = s.replace('{', '_')
        s = s.replace('}', '_')
        s = s.replace('(', '_')
        s = s.replace(')', '_')
        return s

    @staticmethod
    def glm_class_prefix(t):
        if t == "LinearShuntCompensator":
            return "cap"
        if t == "ACLineSegment":
            return "line"
        if t == "EnergyConsumer":
            return ""
        if t == "PowerTransformer":
            return "xf"
        return "##UNKNOWN##"

    @staticmethod
    def dss_class_prefix(t):
        if t == "LinearShuntCompensator":
            return "capacitor"
        if t == "ACLineSegment":
            return "line"
        if t == "EnergyConsumer":
            return "load"
        if t == "PowerTransformer":
            return "transformer"
        return "##UNKNOWN##"

    @staticmethod
    def first_dss_phase(phs):
        if "A" in phs:
            return "1"
        if "B" in phs:
            return "2"
        return "3"

    @staticmethod
    def dss_phase_count(phs, b_delta):
        nphases = 0
        if "A" in phs:
            nphases += 1
        if "B" in phs:
            nphases += 1
        if "C" in phs:
            nphases += 1
        if "s1" in phs:
            nphases += 1
        if "s2" in phs:
            nphases += 1
        if nphases < 3 and b_delta:
            nphases = 1
        return nphases

    @staticmethod
    def dss_conn(b_delta):
        if b_delta:
            return "d"
        return "w"

    @staticmethod
    def dss_shunt_phases(bus, phs, b_delta):
        if "ABC" in phs:
            return f"{bus}.1.2.3"
        if not b_delta:
            return DistComponent.dss_bus_phases(bus, phs)
        if "A" in phs:
            return f"{bus}.1.2"
        elif "B" in phs:
            return f"{bus}.2.3"
        elif "C" in phs:
            return f"{bus}.3.1"
        return bus

    @staticmethod
    def dss_bus_phases(bus, phs):
        if "ABC" in phs:
            return f"{bus}.1.2.3"
        elif "AB" in phs or "A:B" in phs:
            return f"{bus}.1.2"
        elif "12" in phs:
            return f"{bus}.1.2"
        elif "AC" in phs or "A:C" in phs:
            return f"{bus}.1.3"
        elif "BC" in phs or "B:C" in phs:
            return f"{bus}.2.3"
        elif "B:A" in phs:
            return f"{bus}.2.1"
        elif "C:A" in phs:
            return f"{bus}.3.1"
        elif "C:B" in phs:
            return f"{bus}.3.2"
        elif "s1:s2" in phs or "s1s2" in phs:
            return f"{bus}.1.2"
        elif "s2:s1" in phs or "s2s1" in phs:
            return f"{bus}.2.1"
        elif "s1" in phs:
            return f"{bus}.1"
        elif "s2" in phs:
            return f"{bus}.2"
        elif "A" in phs:
            return f"{bus}.1"
        elif "B" in phs:
            return f"{bus}.2"
        elif "C" in phs:
            return f"{bus}.3"
        elif "1" in phs:
            return f"{bus}.1"
        elif "2" in phs:
            return f"{bus}.2"
        return f"{bus}"

    @staticmethod
    def dss_xfmr_bus_phases(bus, phs):
        if "s2" in phs:
            return f"{bus}.0.2"
        if "s1" in phs:
            return f"{bus}.1.0"
        return DistComponent.dss_bus_phases(bus, phs)

    @staticmethod
    def glm_phase_string(cim_phases):
        ret = []
        if "A" in cim_phases:
            ret.append("A")
        if "B" in cim_phases:
            ret.append("B")
        if "C" in cim_phases:
            ret.append("C")
        if "status" in cim_phases:
            ret.append("S")
        return "".join(ret)

    @staticmethod
    def csv_phase_string(cim_phases):
        ret = []
        if "A" in cim_phases:
            ret.append("A")
        if "B" in cim_phases:
            ret.append("B")
        if "C" in cim_phases:
            ret.append("C")
        if "s1" in cim_phases:
            ret.append("s1")
        if "s2" in cim_phases:
            ret.append("s2")
        if "s12" in cim_phases:
            ret.append("s12")
        return "".join(ret)

    @staticmethod
    def c_format(c: complex):
        if c.imag < 0:
            sgn = "-"
        else:
            sgn = "+"
        return f"{c.real:.6g}{sgn}{abs(c.imag):.6g}j"

    @staticmethod
    def get_gld_transformer_connection(conn, nwdg):
        if nwdg == 3:
            if conn[0] == "I" and conn[1] == "I" and conn[2] == "I":
                return "SINGLE_PHASE_CENTER_TAPPED"
        if conn[0] == "D":
            if conn[1] == "D":
                return "DELTA_DELTA"
            elif conn[1] == "Y":
                return "DELTA_GWYE"
            elif conn[1] == "Z":
                return "D_Z"
            elif conn[1] == "Yn":
                return "DELTA_GWYE"
            elif conn[1] == "Zn":
                return "D_Zn"
            elif conn[1] == "A":
                return "D_A"
            elif conn[1] == "I":
                return "D_I"
        elif conn[0] == "Y":
            if conn[1] == "D":
                return "Y_D"
            elif conn[1] == "Y":
                return "WYE_WYE"
            elif conn[1] == "Z":
                return "Y_Z"
            elif conn[1] == "Yn":
                return "WYE_WYE"
            elif conn[1] == "Zn":
                return "Y_Z"
            elif conn[1] == "A":
                return "WYE_WYE"
            elif conn[1] == "I":
                return "Y_I"
        elif conn[0] == "Z":
            if conn[1] == "D":
                return "Z_D"
            elif conn[1] == "Y":
                return "Z_Y"
            elif conn[1] == "Z":
                return "Z_Z"
            elif conn[1] == "Yn":
                return "Z_Yn"
            elif conn[1] == "Zn":
                return "Z_Zn"
            elif conn[1] == "A":
                return "Z_A"
            elif conn[1] == "I":
                return "Z_I"
        elif conn[0] == "Yn":
            if conn[1] == "D":
                return "Yn_D"
            elif conn[1] == "Y":
                return "WYE_WYE"
            elif conn[1] == "Z":
                return "Yn_Z"
            elif conn[1] == "Yn":
                return "WYE_WYE"
            elif conn[1] == "Zn":
                return "Yn_Zn"
            elif conn[1] == "A":
                return "WYE_WYE"
            elif conn[1] == "I":
                return "Yn_I"
        elif conn[0] == "Zn":
            if conn[1] == "D":
                return "Zn_D"
            elif conn[1] == "Y":
                return "Zn_Y"
            elif conn[1] == "Z":
                return "Zn_Z"
            elif conn[1] == "Yn":
                return "Zn_Yn"
            elif conn[1] == "Zn":
                return "Zn_Zn"
            elif conn[1] == "A":
                return "Zn_A"
            elif conn[1] == "I":
                return "Zn_I"
        elif conn[0] == "A":
            if conn[1] == "D":
                return "A_D"
            elif conn[1] == "Y":
                return "WYE_WYE"
            elif conn[1] == "Z":
                return "A_Z"
            elif conn[1] == "Yn":
                return "WYE_WYE"
            elif conn[1] == "Zn":
                return "A_Zn"
            elif conn[1] == "A":
                return "WYE_WYE"
            elif conn[1] == "I":
                return "A_I"
        elif conn[0] == "I":
            if conn[1] == "D":
                return "I_D"
            elif conn[1] == "Y":
                return "I_Y"
            elif conn[1] == "Z":
                return "I_Z"
            elif conn[1] == "Yn":
                return "I_Yn"
            elif conn[1] == "Zn":
                return "I_Zn"
            elif conn[1] == "A":
                return "I_A"
            elif conn[1] == "I":
                return "SINGLE_PHASE"
        return "** Unsupported **"

    def append_glm_ratings(self, buf, phs, norm_amps, emerg_amps):
        phases = ["A", "B", "C"]
        if norm_amps > 0.0:
            s_norm = f"{norm_amps:.2f}"
            for p in phases:
                if p in phs:
                    buf.append(f"  continuous_rating_{p} {s_norm};\n")
        if emerg_amps > 0.0:
            s_emerg = f"{emerg_amps:.2f}"
            for p in phases:
                if p in phs:
                    buf.append(f"  emergency_rating_{p} {s_emerg};\n")

    def append_dss_ratings(self, buf, norm_amps, emerg_amps):
        if norm_amps > 0.0:
            buf.append(f"~ normamps={norm_amps:.2f}\n")
        if emerg_amps > 0.0:
            buf.append(f"~ emergamps={emerg_amps:.2f}\n")

    def get_json_symbols(self, map: Dict[str, 'DistCoordinates']) -> str:
        return ""

    @abstractmethod
    def display_string(self) -> str:
        pass

    @abstractmethod
    def get_key(self) -> str:
        pass

    @abstractmethod
    def get_json_entry(self) -> str:
        pass