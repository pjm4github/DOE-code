
import random
from collections import namedtuple
import sys
import math
import argparse
import xml.etree.ElementTree as ET
import rdflib
import os.path
import csv
from rdflib import Ontology, QueryFactory, QueryExecutionFactory

class gld_link:
    def __init__(self, name):
        self.name = name
        self.from_nd = None
        self.to_nd = None
        self.phases = ""
        self.vbase = -1.0
        self.z1 = complex(0.0, 0.0)
        self.z0 = complex(0.0, 0.0)
        self.bdelta = False

    def add_phases(self, phs):
        buf = []
        if "A" in self.phases or "A" in phs:
            buf.append("A")
        if "B" in self.phases or "B" in phs:
            buf.append("B")
        if "C" in self.phases or "C" in phs:
            buf.append("C")
        self.phases = "".join(buf)

    def get_phases(self):
        return self.phases

    def apply_zbase(self, vbase):
        self.z1 = self.z1 * vbase * 1

class SpacingCount:
    # helper class to keep track of the conductor counts for WireSpacingInfo instances
    def __init__(self, nconds, nphases):
        self.nconds = nconds
        self.nphases = nphases

    def get_num_conductors(self):
        return self.nconds

    def get_num_phases(self):
        return self.nphases


class GldNode:
    # 	// helper class to accumulate nodes and loads
    # 	// all EnergyConsumer data will be attached to node objects, then written as load objects
    # 	//	 this preserves the input ConnectivityNode names
    # 	// TODO - another option is to leave all nodes un-loaded,
    # 	//	 and attach all loads to parent nodes, closer to what OpenDSS does
    def __init__(self, name):
        self.name = name
        self.phases = ""
        self.nomvln = -1.0
        self.pa_z = 0.0
        self.pb_z = 0.0
        self.pc_z = 0.0
        self.qa_z = 0.0
        self.qb_z = 0.0
        self.qc_z = 0.0
        self.pa_i = 0.0
        self.pb_i = 0.0
        self.pc_i = 0.0
        self.qa_i = 0.0
        self.qb_i = 0.0
        self.qc_i = 0.0
        self.pa_p = 0.0
        self.pb_p = 0.0
        self.pc_p = 0.0
        self.qa_p = 0.0
        self.qb_p = 0.0
        self.qc_p = 0.0
        self.b_delta = False
        self.b_swing = False
        self.b_secondary = False

class CIMDataRDFToGLM:
    ns_cim = "http://iec.ch/TC57/CIM100#"
    ns_rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    base_uri = "http://gridlabd"
    combined_owl = "Combined.owl"

    pos120 = complex(-0.5, 0.5 * math.sqrt(3.0))
    neg120 = complex(-0.5, -0.5 * math.sqrt(3.0))
    map_spacings = {}
    map_nodes = {}

    def __init__(self, name):
        self.name = name
        self.map_nodes = GldNode(name)
        self.phases = ""
        self.nomvln = -1.0
        self.pa_z = 0.0
        self.pb_z = 0.0
        self.pc_z = 0.0
        self.qa_z = 0.0
        self.qb_z = 0.0
        self.qc_z = 0.0
        self.pa_i = 0.0
        self.pb_i = 0.0
        self.pc_i = 0.0
        self.qa_i = 0.0
        self.qb_i = 0.0
        self.qc_i = 0.0
        self.pa_p = 0.0
        self.pb_p = 0.0
        self.pc_p = 0.0
        self.qa_p = 0.0
        self.qb_p = 0.0
        self.qc_p = 0.0
        self.b_delta = False
        self.b_swing = False
        self.b_secondary = False

    @staticmethod
    def c_format(c:complex):
        sgn = "-" if c.imag < 0.0 else "+"
        return functions"{c.real:.6f}{sgn}{abs(c.imag):.6f}j"

    def add_phases(self, phs):
        buf = []
        if "A" in self.phases or "A" in phs:
            buf.append("A")
        if "B" in self.phases or "B" in phs:
            buf.append("B")
        if "C" in self.phases or "C" in phs:
            buf.append("C")
        if "status" in phs:
            self.b_secondary = True
        if "S" in phs:
            self.b_secondary = True
        if "D" in phs:
            self.b_delta = True
        self.phases = "".join(buf)

    def get_phases(self):
        if self.b_delta and not self.b_secondary:
            return self.phases + "D"
        if self.b_secondary:
            return self.phases + "S"
        return self.phases + "N"

    def apply_zip(self, Z, I, P):
        total = Z + I + P
        Z /= total
        I /= total
        P /= total

        total = self.pa_z + self.pa_i + self.pa_p
        self.pa_z = total * Z
        self.pa_i = total * I
        self.pa_p = total * P
        total = self.qa_z + self.qa_i + self.qa_p
        self.qa_z = total * Z
        self.qa_i = total * I
        self.qa_p = total * P

        total = self.pb_z + self.pb_i + self.pb_p
        self.pb_z = total * Z
        self.pb_i = total * I
        self.pb_p = total * P
        total = self.qb_z + self.qb_i + self.qb_p
        self.qb_z = total * Z
        self.qb_i = total * I
        self.qb_p = total * P

        total = self.pc_z + self.pc_i + self.pc_p
        self.pc_z = total * Z
        self.pc_i = total * I
        self.pc_p = total * P
        total = self.qc_z + self.qc_i + self.qc_p
        self.qc_z = total * Z
        self.qc_i = total * I
        self.qc_p = total * P

    def rescale_load(self, scale):
        self.pa_z *= scale
        self.pb_z *= scale
        self.pc_z *= scale
        self.qa_z *= scale
        self.qb_z *= scale
        self.qc_z *= scale
        self.pa_i *= scale
        self.pb_i *= scale
        self.pc_i *= scale
        self.qa_i *= scale
        self.qb_i *= scale
        self.qc_i *= scale
        self.pa_p *= scale
        self.pb_p *= scale
        self.pc_p *= scale
        self.qa_p *= scale
        self.qb_p *= scale
        self.qc_p *= scale

    def has_load(self):
        if self.pa_z != 0.0: return True
        if self.pb_z != 0.0: return True
        if self.pc_z != 0.0: return True
        if self.qa_z != 0.0: return True
        if self.qb_z != 0.0: return True
        if self.qc_z != 0.0: return True
        if self.pa_i != 0.0: return True
        if self.pb_i != 0.0: return True
        if self.pc_i != 0.0: return True
        if self.qa_i != 0.0: return True
        if self.qb_i != 0.0: return True
        if self.qc_i != 0.0: return True
        if self.pa_p != 0.0: return True
        if self.pb_p != 0.0: return True
        if self.pc_p != 0.0: return True
        if self.qa_p != 0.0: return True
        if self.qb_p != 0.0: return True
        if self.qc_p != 0.0: return True
        return False

    def add_load(self, Z, I, P, nphases, phs):
        # determine which phases are present
        self.add_phases(phs)

        # apply ZIP to the loads
        self.apply_zip(Z, I, P)

        # rescale the ZIP load
        self.rescale_load(nphases / 3.0)

    def add_transformer(self, num_phases, phs, conn, vprim, vsec, zscen, ires, tap):

        # determine which phases are present
        self.add_phases(phs)

        # apply the transformer impedance to the appropriate nodes
        ratio = vprim / vsec
        Z = zscen * ratio * ratio
        I = ires / vsec
        P = 0.0

        if "A" in phs:
            if conn == "D":
                self.pa_z += 3 * Z
                self.pa_i += 3 * I
            elif conn == "Y":
                self.pa_z += 3 * Z
                self.pa_i += 3 * I
            else:
                self.pa_z += Z
                self.pa_i += I

        if "B" in phs:
            if conn == "D":
                self.pb_z += 3 * Z
                self.pb_i += 3 * I
            elif conn == "Y":
                self.pb_z += 3 * Z
                self.pb_i += 3 * I
            else:
                self.pb_z += Z
                self.pb_i += I

        if "C" in phs:
            if conn == "D":
                self.pc_z += 3 * Z
                self.pc_i += 3 * I
            elif conn == "Y":
                self.pc_z += 3 * Z
                self.pc_i += 3 * I
            else:
                self.pc_z += Z
                self.pc_i += I

        # rescale the transformer load
        self.rescale_load(num_phases / 3.0)

    def dump(self, outfile):
        outfile.write(functions"# node {self.name} {self.get_phases()}  vnom={self.nomvln}\n")
        outfile.write(functions"# A={CIMDataRDFToGLM.c_format(self.pa_z)}  B={CIMDataRDFToGLM.c_format(self.pb_z)}  C={CIMDataRDFToGLM.c_format(self.pc_z)}\n")
        outfile.write(functions"# AP={CIMDataRDFToGLM.c_format(self.pa_p)}  BP={CIMDataRDFToGLM.c_format(self.pb_p)}  CP={CIMDataRDFToGLM.c_format(self.pc_p)}\n")
        outfile.write(functions"# AI={CIMDataRDFToGLM.c_format(self.pa_i)}  BI={CIMDataRDFToGLM.c_format(self.pb_i)}  CI={CIMDataRDFToGLM.c_format(self.pc_i)}\n")
        outfile.write(functions"# AQ={CIMDataRDFToGLM.c_format(self.qa_z)}  BQ={CIMDataRDFToGLM.c_format(self.qb_z)}  CQ={CIMDataRDFToGLM.c_format(self.qc_z)}\n")
        outfile.write(functions"# AQP={CIMDataRDFToGLM.c_format(self.qa_p)}  BQP={CIMDataRDFToGLM.c_format(self.qb_p)}  CQP={CIMDataRDFToGLM.c_format(self.qc_p)}\n")

    def connect_transparent(self, node):
        self.pa_z += node.pa_z
        self.pb_z += node.pb_z
        self.pc_z += node.pc_z
        self.pa_p += node.pa_p
        self.pb_p += node.pb_p
        self.pc_p += node.pc_p
        self.pa_i += node.pa_i
        self.pb_i += node.pb_i
        self.pc_i += node.pc_i
        self.qa_z += node.qa_z
        self.qb_z += node.qb_z
        self.qc_z += node.qc_z
        self.qa_p += node.qa_p
        self.qb_p += node.qb_p
        self.qc_p += node.qc_p
        self.qa_i += node.qa_i
        self.qb_i += node.qb_i
        self.qc_i += node.qc_i
        self.add_phases(node.phases)

    def transform_ygd(self, node, num_phases, phs, conn, vprim, vsec, zscen, ires, tap):
        ratio = vprim / vsec
        Z = zscen * ratio * ratio
        I = ires / vsec
        P = 0.0

        if "A" in phs:
            if conn == "D":
                self.pa_z += 3 * Z
                self.pa_i += 3 * I
            elif conn == "Y":
                self.pa_z += 3 * Z
                self.pa_i += 3 * I
            else:
                self.pa_z += Z
                self.pa_i += I

        if "B" in phs:
            if conn == "D":
                self.pb_z += 3 * Z
                self.pb_i += 3 * I
            elif conn == "Y":
                self.pb_z += 3 * Z
                self.pb_i += 3 * I
            else:
                self.pb_z += Z
                self.pb_i += I

        if "C" in phs:
            if conn == "D":
                self.pc_z += 3 * Z
                self.pc_i += 3 * I
            elif conn == "Y":
                self.pc_z += 3 * Z
                self.pc_i += 3 * I
            else:
                self.pc_z += Z
                self.pc_i += I

        # rescale the transformer load
        self.rescale_load(num_phases / 3.0)

    @staticmethod
    def safe_property(r, p, def_value):
        if r.value(p, None):
            return r.value(p)
        return def_value

    @staticmethod
    def safe_phases_x(r, p):
        if r.value(p, None):
            return r.value(p).toPython()
        return "#PhaseCode.ABCN"

    @staticmethod
    def safe_regulating_mode(r, p, def_value):
        if r.value(p, None):
            arg = r.value(p).toPython()
            hash_index = arg.rfind("#RegulatingControlModeKind.")
            return arg[hash_index + 27:]
        return def_value

    @staticmethod
    def gld_cap_mode(s):
        if s == "currentFlow":
            return "CURRENT"
        if s == "voltage":
            return "VOLT"
        if s == "reactivePower":
            return "VAR"
        if s == "timeScheduled":
            return "MANUAL"
        if s == "powerFactor":
            return "MANUAL"
        if s == "userDefined":
            return "MANUAL"
        return "time"

    @staticmethod
    def safe_double(r, p, def_value):
        if r.value(p, None):
            return r.value(p).toPython()
        return def_value

    @staticmethod
    def safe_int(r, p, def_value):
        if r.value(p, None):
            return r.value(p).toPython()
        return def_value

    @staticmethod
    def safe_boolean(r, p, def_value):
        if r.value(p, None):
            return r.value(p).toPython() == "true"
        return def_value

    @staticmethod
    def get_equipment_type(r):
        s = r.rdf_type.toPython()
        hash_index = s.rfind("#")
        t = s[hash_index + 1:]
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
    def gld_prefixed_node_name(arg):
        return arg

    def gld_name(self, arg, bus):
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
        if bus:
            return self.gld_prefixed_node_name(s)
        return s

    def gld_id(self, arg):
        hash_index = arg.rfind("#")
        return self.gld_name(arg[hash_index + 1:], False)


    def safe_res_name(self, r, p):
        if r.value(p, None):
            s = r.value(p).toPython()
        else:
            s = r.local_name.toPython()
        return self.gld_name(s, False)

    @staticmethod
    def safe_resource_lookup(self, mdl, pt_name, r, p, def_value):
        if r.value(p, None):
            res = mdl.resource(r.value(p))
            s =self.safe_res_name(res, pt_name)
            return s
        return def_value

    @staticmethod
    def get_mat_idx(n, row, col):
        seq = -1
        for j in range(col):
            seq += (n - j)
        for i in range(col, row + 1):
            seq += 1
        return seq

    def get_impedance_matrix(self, mdl, name, pt_count, r, b_want_sec):
        pt_data = mdl.get_property(CIMDataRDFToGLM.ns_cim.PhaseImpedanceData.PhaseImpedance)
        pt_seq = mdl.get_property(CIMDataRDFToGLM.ns_cim.PhaseImpedanceData.sequenceNumber)
        pt_r = mdl.get_property(CIMDataRDFToGLM.ns_cim.PhaseImpedanceData.r)
        pt_x = mdl.get_property(CIMDataRDFToGLM.ns_cim.PhaseImpedanceData.x)
        pt_b = mdl.get_property(CIMDataRDFToGLM.ns_cim.PhaseImpedanceData.b)
        nphases = r.value(pt_count).toPython()

        size = 0
        for i in range(nphases):
            for j in range(i, nphases):
                size += 1
        r_mat = [0.0] * size
        x_mat = [0.0] * size
        c_mat = [0.0] * size
        len_mile = 1609.344

        iter = mdl.subjects(predicate=pt_data, object=r)
        for r_data in iter:
            seq = r_data.value(pt_seq).toPython() - 1
            if r_data.has_property(pt_r):
                r_mat[seq] = len_mile * r_data.value(pt_r).toPython()
            if r_data.has_property(pt_x):
                x_mat[seq] = len_mile * r_data.value(pt_x).toPython()
            if r_data.has_property(pt_b):
                c_mat[seq] = len_mile * r_data.value(pt_b).toPython() * 1.0e9 / 377.0

        buf = []

        if nphases == 1:
            seq = self.get_mat_idx(nphases, 0, 0)
            buf.append("object line_configuration {")
            buf.append(functions"    name \"lcon_{name}_A\";")
            buf.append(functions"    z11 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c11 {c_mat[seq]:.6f};")
            buf.append("}")
            buf.append("object line_configuration {")
            buf.append(functions"    name \"lcon_{name}_B\";")
            buf.append(functions"    z22 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c22 {c_mat[seq]:.6f};")
            buf.append("}")
            buf.append("object line_configuration {")
            buf.append(functions"    name \"lcon_{name}_C\";")
            buf.append(functions"    z33 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c33 {c_mat[seq]:.6f};")
            buf.append("}")
        elif nphases == 2 and name.contains("triplex") and b_want_sec:
            buf.append("object triplex_line_configuration {")
            buf.append(functions"    name \"tcon_{name}\";")
            seq = self.get_mat_idx(nphases, 0, 0)
            buf.append(functions"    z11 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            seq = self.get_mat_idx(nphases, 1, 0)
            buf.append(functions"    z12 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    z21 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            seq = self.get_mat_idx(nphases, 1, 1)
            buf.append(functions"    z22 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append("}")
        elif nphases == 2:
            buf.append("object line_configuration {")
            buf.append(functions"    name \"lcon_{name}_AB\";")
            seq = self.get_mat_idx(nphases, 0, 0)
            buf.append(functions"    z11 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c11 {c_mat[seq]:.6f};")
            seq = self.get_mat_idx(nphases, 1, 0)
            buf.append(functions"    z12 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c12 {c_mat[seq]:.6f};")
            buf.append(functions"    z21 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c21 {c_mat[seq]:.6f};")
            seq = self.get_mat_idx(nphases, 1, 1)
            buf.append(functions"    z22 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c22 {c_mat[seq]:.6f};")
            buf.append("}")
            buf.append("object line_configuration {")
            buf.append(functions"    name \"lcon_{name}_BC\";")
            seq = self.get_mat_idx(nphases, 0, 0)
            buf.append(functions"    z22 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c22 {c_mat[seq]:.6f};")
            seq = self.get_mat_idx(nphases, 1, 0)
            buf.append(functions"    z23 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c23 {c_mat[seq]:.6f};")
            buf.append(functions"    z32 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c32 {c_mat[seq]:.6f};")
            seq = self.get_mat_idx(nphases, 1, 1)
            buf.append(functions"    z33 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c33 {c_mat[seq]:.6f};")
            buf.append("}")
            buf.append("object line_configuration {")
            buf.append(functions"    name \"lcon_{name}_AC\";")
            seq = self.get_mat_idx(nphases, 0, 0)
            buf.append(functions"    z11 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c11 {c_mat[seq]:.6f};")
            seq = self.get_mat_idx(nphases, 1, 0)
            buf.append(functions"    z13 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c13 {c_mat[seq]:.6f};")
            buf.append(functions"    z31 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c31 {c_mat[seq]:.6f};")
            seq = self.get_mat_idx(nphases, 1, 1)
            buf.append(functions"    z33 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};")
            buf.append(functions"    c33 {c_mat[seq]:.6f};")
            buf.append("}")
        elif nphases == 3:
            buf.append("object line_configuration {")
            buf.append(functions"    name \"lcon_{name}_ABC\";")
            seq = self.get_mat_idx(nphases, 0, 0)
            buf.append(functions"  z11 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};\n")
            buf.append(functions"  c11 {c_mat[seq]:.6f};\n")
            seq = self.get_mat_idx(nphases, 1, 0)
            buf.append(functions"  z12 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};\n")
            buf.append(functions"  c12 {c_mat[seq]:.6f};\n")
            buf.append(functions"  z21 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};\n")
            buf.append(functions"  c21 {c_mat[seq]:.6f};\n")
            seq = self.get_mat_idx(nphases, 1, 1)
            buf.append(functions"  z22 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};\n")
            buf.append(functions"  c22 {c_mat[seq]:.6f};\n")
            seq = self.get_mat_idx(nphases, 2, 0)
            buf.append(functions"  z31 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};\n")
            buf.append(functions"  c31 {c_mat[seq]:.6f};\n")
            buf.append(functions"  z13 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};\n")
            buf.append(functions"  c13 {c_mat[seq]:.6f};\n")
            seq = self.get_mat_idx(nphases, 2, 1)
            buf.append(functions"  z32 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};\n")
            buf.append(functions"  c32 {c_mat[seq]:.6f};\n")
            buf.append(functions"  z23 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};\n")
            buf.append(functions"  c23 {c_mat[seq]:.6f};\n")
            seq = self.get_mat_idx(nphases, 2, 2)
            buf.append(functions"  z33 {CIMDataRDFToGLM.c_format(complex(r_mat[seq], x_mat[seq]))};\n")
            buf.append(functions"  c33 {c_mat[seq]:.6f};\n")
            buf.append("}\n")
        return '\n'.join(buf)

    @staticmethod
    def phase_string(arg):
        hash_index = arg.rfind("#PhaseCode.")
        return arg[hash_index + 11:]

    @staticmethod
    def phase_kind_string(arg):
        hash_index = arg.rfind("#SinglePhaseKind.")
        return arg[hash_index + 17:]

    @staticmethod
    def first_phase(phs):
        if "A" in phs:
            return "A"
        if "B" in phs:
            return "B"
        return "C"

    @staticmethod
    def bus_shunt_phases(phs, conn):
        if "w" in conn and "N" not in phs:
            return phs + "N"
        if "d" in conn and "D" not in phs:
            return phs + "D"
        return phs

    @staticmethod
    def shunt_delta(r, p):
        if r.has_property(p):
            arg = r.value(p).toPython()
            hash_index = arg.rfind("#PhaseShuntConnectionKind.")
            conn = arg[hash_index + 26:]
            if "D" in conn:
                return True
        return False

    def wire_phases(self, mdl, r, p1, p2):
        it = mdl.list_resources_with_property(p1, r)
        if it.has_next():
            b_a = False
            b_b = False
            b_c = False
            b_secondary = False
            while it.has_next():
                r_p = it.next_resource()
                if r_p.has_property(p2):
                    s = self.phase_kind_string(r_p.value(p2).toPython())
                    if s == "A":
                        b_a = True
                    if s == "B":
                        b_b = True
                    if s == "C":
                        b_c = True
                    if s == "s1":
                        b_secondary = True
                    if s == "s2":
                        b_secondary = True
            buf = ""
            if b_a:
                buf += "A"
            if b_b:
                buf += "B"
            if b_c:
                buf += "C"
            if b_secondary:
                buf += "S"
            return buf
        return "ABC"

    @staticmethod
    def count_phases(phs):
        if "ABC" in phs:
            return 3
        elif "AB" in phs:
            return 2
        elif "AC" in phs:
            return 2
        elif "BC" in phs:
            return 2
        elif "A" in phs:
            return 1
        elif "B" in phs:
            return 1
        elif "C" in phs:
            return 1
        else:
            return 3  # defaults to 3 phases

    @staticmethod
    def get_wdg_connection(r, p, default):
        if r.has_property(p):
            arg = r.value(p).toPython()
            hash_idx = arg.rfind("#WindingConnection.")
            if hash_idx != -1:
                return arg[hash_idx + 19:]  # D, Y, Z, Yn, Zn, A, I
        return default

    def get_prop_value(self, mdl, uri, prop):
        res = mdl.get_resource(uri)
        p = mdl.get_property(self.ns_cim, prop)
        return str(res.value(p))

    def accumulate_loads(self, nd, phs, pL, qL, Pv, Qv, Pz, Pi, Pp, Qz, Qi, Qp):
        # we have to equally divide the total pL and qL among the actual phases defined in "phs"
        fa, fb, fc, denom = 0.0, 0.0, 0.0, 0.0
        if "A" in phs or "S" in phs:
            fa = 1.0
            denom += 1.0
        if "B" in phs or "S" in phs:
            fb = 1.0
            denom += 1.0
        if "C" in phs:
            fc = 1.0
            denom += 1.0
        if fa > 0.0:
            fa /= denom
        if fb > 0.0:
            fb /= denom
        if fc > 0.0:
            fc /= denom

        # we also have to divide the total pL and qL among constant ZIP components
        fpz, fqz, fpi, fqi, fpp, fqp = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        denom = Pz + Pi + Pp
        if denom > 0.0:
            fpz = Pz / denom
            fpi = Pi / denom
            fpp = Pp / denom
        else:
            if 0.9 < Pv < 1.1:
                fpi = 1.0
            elif 1.9 < Pv < 2.1:
                fpz = 1.0
            else:
                fpp = 1.0
        denom = Qz + Qi + Qp
        if denom > 0.0:
            fqz = Qz / denom
            fqi = Qi / denom
            fqp = Qp / denom
        else:
            if 0.9 < Qv < 1.1:
                fqi = 1.0
            elif 1.9 < Qv < 2.1:
                fqz = 1.0
            else:
                fqp = 1.0

        # now update the node phases and phase loads
        self.add_phases(phs)
        self.pa_z += fa * pL * fpz
        self.pb_z += fb * pL * fpz
        self.pc_z += fc * pL * fpz
        self.qa_z += fa * qL * fqz
        self.qb_z += fb * qL * fqz
        self.qc_z += fc * qL * fqz
        self.pa_i += fa * pL * fpi
        self.pb_i += fb * pL * fpi
        self.pc_i += fc * pL * fpi
        self.qa_i += fa * qL * fqi
        self.qb_i += fb * qL * fqi
        self.qc_i += fc * qL * fqi
        self.pa_p += fa * pL * fpp
        self.pb_p += fb * pL * fpp
        self.pc_p += fc * pL * fpp
        self.qa_p += fa * qL * fqp
        self.qb_p += fb * qL * fqp
        self.qc_p += fc * qL * fqp
        return True

    def get_bus_name(self, mdl, eq_id, seq):
        str_seq = str(seq)
        pt_node = mdl.get_property(self.ns_cim, "Terminal.ConnectivityNode")
        pt_equip = mdl.get_property(self.ns_cim, "Terminal.ConductingEquipment")
        pt_seq = mdl.get_property(self.ns_cim, "Terminal.sequenceNumber")
        pt_name = mdl.get_property(self.ns_cim, "IdentifiedObject.name")
        res_id = mdl.get_resource(eq_id)
        iter = mdl.list_resources_with_property(pt_equip, res_id)
        idx = 0
        found = False
        while iter.hasNext():
            res = iter.next_resource()  # this is a terminal of eq_id
            idx += 1
            if res.has_property(pt_seq):
                if res.has_property(pt_seq, str_seq):
                    found = True
            else:
                if idx == seq:
                    found = True
            if found:
                CN = res.value(pt_node).toPython()
                if CN.has_property(pt_name):
                    return self.gld_name(CN.value(pt_name).toPython(), True)
                else:
                    return self.gld_name(CN.local_name, True)
        return "x"

    @staticmethod
    def get_gld_transformer_connection(wye, nwdg):
        if nwdg == 3:
            if wye[0] == "I" and wye[1] == "I" and wye[2] == "I":
                return "SINGLE_PHASE_CENTER_TAPPED"

        if wye[0] == "D":
            if wye[1] == "D":
                return "DELTA_DELTA"
            elif wye[1] == "Y":
                return "DELTA_GWYE"
            elif wye[1] == "Z":
                return "D_Z"
            elif wye[1] == "Yn":
                return "DELTA_GWYE"
            elif wye[1] == "Zn":
                return "D_Zn"
            elif wye[1] == "A":
                return "D_A"
            elif wye[1] == "I":
                return "D_I"

        elif wye[0] == "Y":
            if wye[1] == "D":
                return "Y_D"  # TODO - flip?
            elif wye[1] == "Y":
                return "WYE_WYE"
            elif wye[1] == "Z":
                return "Y_Z"
            elif wye[1] == "Yn":
                return "WYE_WYE"
            elif wye[1] == "Zn":
                return "Y_Z"
            elif wye[1] == "A":
                return "WYE_WYE"  # TODO - approximately correct
            elif wye[1] == "I":
                return "Y_I"

        elif wye[0] == "Z":
            if wye[1] == "D":
                return "Z_D"
            elif wye[1] == "Y":
                return "Z_Y"
            elif wye[1] == "Z":
                return "Z_Z"
            elif wye[1] == "Yn":
                return "Z_Yn"
            elif wye[1] == "Zn":
                return "Z_Zn"
            elif wye[1] == "A":
                return "Z_A"
            elif wye[1] == "I":
                return "Z_I"

        elif wye[0] == "Yn":
            if wye[1] == "D":
                return "Yn_D"
            elif wye[1] == "Y":
                return "WYE_WYE"
            elif wye[1] == "Z":
                return "Yn_Z"
            elif wye[1] == "Yn":
                return "WYE_WYE"
            elif wye[1] == "Zn":
                return "Yn_Zn"
            elif wye[1] == "A":
                return "WYE_WYE"  # TODO - approximately correct
            elif wye[1] == "I":
                return "Yn_I"

        elif wye[0] == "Zn":
            if wye[1] == "D":
                return "Zn_D"
            elif wye[1] == "Y":
                return "Zn_Y"
            elif wye[1] == "Z":
                return "Zn_Z"
            elif wye[1] == "Yn":
                return "Zn_Yn"
            elif wye[1] == "Zn":
                return "Zn_Zn"
            elif wye[1] == "A":
                return "Zn_A"
            elif wye[1] == "I":
                return "Zn_I"

        elif wye[0] == "A":
            if wye[1] == "D":
                return "A_D"
            elif wye[1] == "Y":
                return "WYE_WYE"  # TODO - approximately correct
            elif wye[1] == "Z":
                return "A_Z"
            elif wye[1] == "Yn":
                return "WYE_WYE"  # TODO - approximately correct
            elif wye[1] == "Zn":
                return "A_Zn"
            elif wye[1] == "A":
                return "WYE_WYE"  # TODO - approximately correct
            elif wye[1] == "I":
                return "A_I"

        elif wye[0] == "I":
            if wye[1] == "D":
                return "I_D"
            elif wye[1] == "Y":
                return "I_Y"
            elif wye[1] == "Z":
                return "I_Z"
            elif wye[1] == "Yn":
                return "I_Yn"
            elif wye[1] == "Zn":
                return "I_Zn"
            elif wye[1] == "A":
                return "I_A"
            elif wye[1] == "I":
                return "SINGLE_PHASE"

        return "** Unsupported **"  # TODO


    def get_power_transformer_data(self, mdl, rXf):
        ptEnd = mdl.getProperty(self.ns_cim, "TransformerEnd.endNumber")
        ptTerm = mdl.getProperty(self.ns_cim, "TransformerEnd.Terminal")
        ptPhs = mdl.getProperty(self.ns_cim, "ConductingEquipment.phases")
        ptNode = mdl.getProperty(self.ns_cim, "Terminal.ConnectivityNode")
        ptName = mdl.getProperty(self.ns_cim, "IdentifiedObject.name")
        ptXfmr = mdl.getProperty(self.ns_cim, "PowerTransformerEnd.PowerTransformer")
        ptEndRw = mdl.getProperty(self.ns_cim, "PowerTransformerEnd.r")
        ptEndC = mdl.getProperty(self.ns_cim, "PowerTransformerEnd.connectionKind")
        ptEndV = mdl.getProperty(self.ns_cim, "PowerTransformerEnd.ratedU")
        ptEndS = mdl.getProperty(self.ns_cim, "PowerTransformerEnd.ratedS")
        ptEndGrnd = mdl.getProperty(self.ns_cim, "TransformerEnd.grounded")
        ptEndRn = mdl.getProperty(self.ns_cim, "TransformerEnd.rground")
        ptEndXn = mdl.getProperty(self.ns_cim, "TransformerEnd.xground")
        ptEndN = mdl.getProperty(self.ns_cim, "TransformerEnd.endNumber")

        xfName = mdl.getProperty(rXf, ptName).get""

        it = mdl.listResourcesWithProperty(ptXfmr, rXf)
        nwdg = sum(1 for _ in it)
        bus = ["" for _ in range(nwdg)]
        phs = ["" for _ in range(nwdg)]
        xfmrPhase = ""
        v = [0.0 for _ in range(nwdg)]
        s = [0.0 for _ in range(nwdg)]
        zb = [0.0 for _ in range(nwdg)]
        rw = [0.0 for _ in range(nwdg)]
        rn = [0.0 for _ in range(nwdg)]
        xn = [0.0 for _ in range(nwdg)]
        wye = ["Y" for _ in range(nwdg)]
        rEnds = [None for _ in range(nwdg)]

        it = mdl.listResourcesWithProperty(ptXfmr, rXf)
        for i, wdg in enumerate(it):
            i = self.safe_int(wdg, ptEnd, 1) - 1
            trm = wdg.getProperty(ptTerm).getResource()
            phs[i] = self.phase_string(self.safe_phases_x(trm, ptPhs))
            CN = trm.getProperty(ptNode).getResource()
            if CN.hasProperty(ptName):
                bus[i] = self.gld_name(CN.getProperty(ptName).get"", True)
            else:
                bus[i] = self.gld_name(CN.getLocalName(), True)

        it = mdl.listResourcesWithProperty(ptXfmr, rXf)
        for i, rEnd in enumerate(it):
            i = self.safe_int(rEnd, ptEndN, 1) - 1
            v[i] = self.safe_double(rEnd, ptEndV, 1.0)
            s[i] = self.safe_double(rEnd, ptEndS, 1.0)
            zb[i] = v[i] * v[i] / s[i]
            rw[i] = self.safe_double(rEnd, ptEndRw, 0.0) / zb[i]
            rn[i] = self.safe_double(rEnd, ptEndRn, 0.0)
            xn[i] = self.safe_double(rEnd, ptEndXn, 0.0)
            wye[i] = self.get_wdg_connection(rEnd, ptEndC, "Y")
            rEnds[i] = rEnd

        ptFrom = mdl.getProperty(self.ns_cim, "TransformerMeshImpedance.FromTransformerEnd")
        ptTo = mdl.getProperty(self.ns_cim, "TransformerMeshImpedance.ToTransformerEnd")
        ptMeshX = mdl.getProperty(self.ns_cim, "TransformerMeshImpedance.x")
        ptCoreB = mdl.getProperty(self.ns_cim, "TransformerCoreAdmittance.b")
        ptCoreG = mdl.getProperty(self.ns_cim, "TransformerCoreAdmittance.g")
        ptCoreN = mdl.getProperty(self.ns_cim, "TransformerCoreAdmittance.TransformerEnd")

        bufX = ["object transformer_configuration {", "  name \"xcon_" + xfName + "\";",
                functions"  connect_type {self.get_gld_transformer_connection(wye, nwdg)};", functions"  primary_voltage {v[0]:.6f};",
                functions"  secondary_voltage {v[1]:.6f};", functions"  power_rating {status[0] * 0.001:.6f};", functions"  resistance {sum(rw):.6f};"]

        it = mdl.listResourcesWithProperty(ptFrom, rEnds[0])
        for rMesh in it:
            rTo = rMesh.getProperty(ptTo).getResource()
            x = self.safe_double(rMesh, ptMeshX, 1.0) / zb[0]
            if rTo.equals(rEnds[1]):
                bufX.append(functions"  reactance {x:.6f};")

        for i in range(nwdg):
            it = mdl.listResourcesWithProperty(ptCoreN, rEnds[i])
            for rCore in it:
                g = self.safe_double(rCore, ptCoreG, 0.0) * zb[i]
                b = self.safe_double(rCore, ptCoreB, 0.0) * zb[i]
                if g > 0.0:
                    bufX.append(functions"  shunt_resistance {1.0 / g:.6f};")
                if b > 0.0:
                    bufX.append(functions"  shunt_reactance {1.0 / b:.6f};")

        if nwdg > 2:
            bufX.append("// ***** too many windings for GridLAB-D *****")

        if "S" in phs[1]:
            xfmrPhase = phs[1]
        else:
            xfmrPhase = phs[0]

        bufX.append("}")
        bufX.append("object transformer {")
        bufX.append(functions"  name \"xf_{xfName}\";")
        bufX.append(functions"  from \"{bus[0]}\";")
        bufX.append(functions"  to \"{bus[1]}\";")
        bufX.append(functions"  phases {xfmrPhase};")
        bufX.append(functions"  configuration \"xcon_{xfName}\";")
        bufX.append("}")

        for i in range(nwdg):
            nd = self.map_nodes.get(bus[i])
            nd.AddPhases(xfmrPhase)
            nd.nomvln = v[i] / math.sqrt(3.0)

        return "\n".join(bufX)

    def get_regulator_data(self, mdl, rXf, name, xf_group, bus1, bus2, phs):
        bA = False
        bB = False
        bC = False
        bLTC = False
        iTapA = 0
        iTapB = 0
        iTapC = 0
        ldcRa = 0.0
        ldcRb = 0.0
        ldcRc = 0.0
        ldcXa = 0.0
        ldcXb = 0.0
        ldcXc = 0.0
        CT = 1.0
        PT = 1.0
        Vband = 2.0
        Vreg = 120.0
        dStep = 0.625
        highStep = 0
        lowStep = 0
        neutralStep = 0
        normalStep = 0
        initDelay = 0
        ptName = mdl.getProperty(self.ns_cim, "IdentifiedObject.name")

        itTank = mdl.listResourcesWithProperty(mdl.getProperty(self.ns_cim, "TransformerTank.PowerTransformer"), rXf)
        for rTank in itTank:
            it = mdl.listResourcesWithProperty(mdl.getProperty(self.ns_cim, "TransformerTankEnd.TransformerTank"), rTank)
            for wdg in it:
                this_phs = self.phase_string(self.safe_phases_x(wdg, mdl.getProperty(self.ns_cim, "TransformerTankEnd.phases")))
                itRtc = mdl.listResourcesWithProperty(mdl.getProperty(self.ns_cim, "RatioTapChanger.TransformerEnd"), wdg)
                if itRtc.hasNext():
                    rtc = itRtc.nextResource()
                    ctl = mdl.getProperty(rtc, mdl.getProperty(self.ns_cim, "TapChanger.TapChangerControl")).getResource()
                    ldcX = self.safe_double(ctl, mdl.getProperty(self.ns_cim, "TapChangerControl.lineDropX"), 0.0)
                    ldcR = self.safe_double(ctl, mdl.getProperty(self.ns_cim, "TapChangerControl.lineDropR"), 0.0)
                    Vreg = self.safe_double(ctl, mdl.getProperty(self.ns_cim, "RegulatingControl.targetValue"), 120.0)
                    Vband = self.safe_double(ctl, mdl.getProperty(self.ns_cim, "RegulatingControl.targetDeadband"), 2.0)
                    bLTC = self.safe_boolean(rtc, mdl.getProperty(self.ns_cim, "TapChanger.ltcFlag"), False)
                    highStep = self.safe_int(rtc, mdl.getProperty(self.ns_cim, "TapChanger.highStep"), 32)
                    lowStep = self.safe_int(rtc, mdl.getProperty(self.ns_cim, "TapChanger.lowStep"), 0)
                    neutralStep = self.safe_int(rtc, mdl.getProperty(self.ns_cim, "TapChanger.neutralStep"), 16)
                    normalStep = self.safe_int(rtc, mdl.getProperty(self.ns_cim, "TapChanger.normalStep"), 16)
                    initDelay = self.safe_double(rtc, mdl.getProperty(self.ns_cim, "TapChanger.initialDelay"), 30)
                    dStep = self.safe_double(rtc, mdl.getProperty(self.ns_cim, "RatioTapChanger.stepVoltageIncrement"), 0.625)
                    subsDelay = self.safe_double(rtc, mdl.getProperty(self.ns_cim, "TapChanger.subsequentDelay"), 2)
                    dTap = self.safe_double(rtc, mdl.getProperty(self.ns_cim, "TapChanger.step"), 1.0)
                    iTap = int(round((dTap - 1.0) / 0.00625))
                    if "A" in this_phs:
                        bA = True
                        iTapA = iTap
                        ldcXa = ldcX
                        ldcRa = ldcR
                    if "B" in this_phs:
                        bB = True
                        iTapB = iTap
                        ldcXb = ldcX
                        ldcRb = ldcR
                    if "C" in this_phs:
                        bC = True
                        iTapC = iTap
                        ldcXc = ldcX
                        ldcRc = ldcR
                    itAsset = mdl.listResourcesWithProperty(mdl.getProperty(self.ns_cim, "Asset.PowerSystemResources"), rtc)
                    for rAsset in itAsset:
                        if rAsset.hasProperty(mdl.getProperty(self.ns_cim, "Asset.AssetInfo")):
                            rDS = rAsset.getProperty(mdl.getProperty(self.ns_cim, "Asset.AssetInfo")).getResource()
                            PT = self.safe_double(rDS, mdl.getProperty(self.ns_cim, "TapChangerInfo.ptRatio"), 1.0)
                            CT = self.safe_double(rDS, mdl.getProperty(self.ns_cim, "TapChangerInfo.ctRating"), 1.0)

        dReg = 0.01 * 0.5 * dStep * (highStep - lowStep)
        bLineDrop = False
        if bA and (ldcRa != 0.0 or ldcXa != 0.0):
            bLineDrop = True
        if bB and (ldcRb != 0.0 or ldcXb != 0.0):
            bLineDrop = True
        if bC and (ldcRc != 0.0 or ldcXc != 0.0):
            bLineDrop = True

        buf = "object regulator_configuration {\n  name \"rcon_" + name + "\";\n"
        if "D" in xf_group.lower() or "d" in xf_group.lower():
            buf += "  connect_type CLOSED_DELTA;\n"
        else:
            buf += "  connect_type WYE_WYE;\n"
        buf += "  band_center " + str(Vreg) + ";\n"
        buf += "  band_width " + str(Vband) + ";\n"
        buf += "  dwell_time " + str(initDelay) + ";\n"
        buf += "  raise_taps " + str(abs(highStep - neutralStep)) + ";\n"
        buf += "  lower_taps " + str(abs(neutralStep - lowStep)) + ";\n"
        buf += "  regulation " + str(dReg) + ";\n"
        buf += "  Type B;\n"
        if Vreg > 0.0 and Vband > 0.0 and bLTC:
            if bLineDrop:
                buf += "  Control MANUAL; // LINE_DROP_COMP;\n"
            else:
                buf += "  Control MANUAL; // OUTPUT_VOLTAGE;\n"
        else:
            buf += "  Control MANUAL;\n"
        if bA:
            buf += "  tap_pos_A " + str(iTapA) + ";\n"
        if bB:
            buf += "  tap_pos_B " + str(iTapB) + ";\n"
        if bC:
            buf += "  tap_pos_C " + str(iTapC) + ";\n"
        buf += "  current_transducer_ratio " + str(CT) + ";\n"
        buf += "  power_transducer_ratio " + str(PT) + ";\n"
        if bA:
            buf += "  compensator_r_setting_A " + str(ldcRa) + ";\n"
            buf += "  compensator_x_setting_A " + str(ldcXa) + ";\n"
        if bB:
            buf += "  compensator_r_setting_B " + str(ldcRb) + ";\n"
            buf += "  compensator_x_setting_B " + str(ldcXb) + ";\n"
        if bC:
            buf += "  compensator_r_setting_C " + str(ldcRc) + ";\n"
            buf += "  compensator_x_setting_C " + str(ldcXc) + ";\n"
        buf += "}\n"

        buf += "object regulator {\n  name \"reg_" + name + "\";\n"
        buf += "  from \"" + bus1 + "\";\n"
        buf += "  to \"" + bus2 + "\";\n"
        buf += "  phases " + phs + ";\n"
        buf += "  configuration \"rcon_" + name + "\";\n"
        buf += "}\n"

        return buf

    @staticmethod
    def merge_phases(phs1, phs2):
        buf = ""
        if "A" in phs1 or "A" in phs2:
            buf += "A"
        if "B" in phs1 or "B" in phs2:
            buf += "B"
        if "C" in phs1 or "C" in phs2:
            buf += "C"
        return buf

    def get_power_transformer_tanks(self, mdl, rXf, it_tank, b_want_sec):
        pt_name = mdl.getProperty(self.ns_cim, "IdentifiedObject.name")
        pt_asset_psr = mdl.getProperty(self.ns_cim, "Asset.PowerSystemResources")
        pt_asset_inf = mdl.getProperty(self.ns_cim, "Asset.AssetInfo")
        pt_group = mdl.getProperty(self.ns_cim, "PowerTransformer.vectorGroup")
        pt_end = mdl.getProperty(self.ns_cim, "TransformerTankEnd.TransformerTank")
        pt_end_n = mdl.getProperty(self.ns_cim, "TransformerEnd.endNumber")
        pt_term = mdl.getProperty(self.ns_cim, "TransformerEnd.Terminal")
        pt_phs = mdl.getProperty(self.ns_cim, "TransformerTankEnd.phases")
        pt_node = mdl.getProperty(self.ns_cim, "Terminal.ConnectivityNode")
        pt_rtc_end = mdl.getProperty(self.ns_cim, "RatioTapChanger.TransformerEnd")

        xf_name = self.safe_res_name(rXf, pt_name)
        xf_group = mdl.getProperty(rXf, pt_group).get""
        xf_code = ""
        xf_phase = ""
        bus = ["", ""]
        phs = ["", ""]
        b_regulator = False

        while it_tank.hasNext():
            r_tank = it_tank.nextResource()
            it = mdl.listResourcesWithProperty(pt_end, r_tank)
            for wdg in it:
                i = self.safe_int(wdg, pt_end_n, 1) - 1
                if 0 <= i <= 1:
                    phs[i] = self.phase_string(self.safe_phases_x(wdg, pt_phs))
                    xf_phase = self.merge_phases(xf_phase, phs[i])
                    trm = wdg.getProperty(pt_term).getResource()
                    CN = trm.getProperty(pt_node).getResource()
                    if CN.hasProperty(pt_name):
                        bus[i] = self.gld_name(CN.getProperty(pt_name).get"", True)
                    else:
                        bus[i] = self.gld_name(CN.getLocalName(), True)
                it_rtc = mdl.listResourcesWithProperty(pt_rtc_end, wdg)
                if it_rtc.hasNext():
                    b_regulator = True

            it = mdl.listResourcesWithProperty(pt_asset_psr, r_tank)
            if it.hasNext():
                r_asset = it.nextResource()
                if r_asset.hasProperty(pt_asset_inf):
                    r_DS = r_asset.getProperty(pt_asset_inf).getResource()
                    xf_code = mdl.getProperty(r_DS, pt_name).get""

        if "status" in phs[0]:
            phs[0] = phs[1] + "S"
            xf_phase = phs[0]
        elif "status" in phs[1]:
            phs[1] = phs[0] + "S"
            xf_phase = phs[1]
        elif "D" in xf_group:
            phs[0] = xf_phase + "D"
            phs[1] = xf_phase
        elif "d" in xf_group:
            phs[0] = xf_phase
            phs[1] = xf_phase + "D"
        else:
            phs[0] = xf_phase
            phs[1] = xf_phase

        nd = self.map_nodes.get(bus[0])
        nd.add_phases(phs[0])
        nd = self.map_nodes.get(bus[1])
        nd.add_phases(phs[1])

        buf = ""
        if b_regulator:
            return self.get_regulator_data(mdl, rXf, xf_name, xf_group, bus[0], bus[1], phs[0])
        else:
            if "S" in xf_phase and not b_want_sec:
                pass
            else:
                buf += "object transformer {\n"
                buf += "  name \"xf_" + xf_name + "\";\n"
                buf += "  from \"" + bus[0] + "\";\n"
                buf += "  to \"" + bus[1] + "\";\n"
                buf += "  phases " + xf_phase + ";\n"
                buf += "  // " + xf_group + "\n"
                buf += "  configuration \"xcon_" + xf_code + "\";\n}\n"

        return buf

    def get_line_spacing(self, mdl, r_line):
        buf = " spacing="
        pt_asset_psr = mdl.getProperty(self.ns_cim, "Asset.PowerSystemResources")
        pt_asset_inf = mdl.getProperty(self.ns_cim, "Asset.AssetInfo")
        pt_name = mdl.getProperty(self.ns_cim, "IdentifiedObject.name")
        it_asset = mdl.listResourcesWithProperty(pt_asset_psr, r_line)
        nconds = 0
        nphases = 0
        b_cncables = False
        b_tscables = False
        ws_name = ""
        wire_name = ""

        while it_asset.hasNext():
            r_asset = it_asset.nextResource()
            if r_asset.hasProperty(pt_asset_inf):
                r_ds = r_asset.getProperty(pt_asset_inf).getResource()
                # status = r_ds.as(OntResource.class).getRDFType().to""
                s = str(r_ds.getRDFType())
                hash = s.lastIndexOf("#")
                t = s.substring(hash + 1)
                if t == "WireSpacingInfo":
                    ws_name = self.safe_res_name(r_ds, pt_name)
                    buf += ws_name
                    spc = self.map_spacings.get(ws_name)
                    nconds = spc.getNumConductors()
                    nphases = spc.getNumPhases()
                elif t == "OverheadWireInfo":
                    wire_name = self.safe_res_name(r_ds, pt_name)
                elif t == "ConcentricNeutralCableInfo":
                    b_cncables = True
                    wire_name = self.safe_res_name(r_ds, pt_name)
                elif t == "TapeShieldCableInfo":
                    b_tscables = True
                    wire_name = self.safe_res_name(r_ds, pt_name)

        if nconds > 0:
            pt_segment = mdl.getProperty(self.ns_cim, "ACLineSegmentPhase.ACLineSegment")
            pt_phase = mdl.getProperty(self.ns_cim, "ACLineSegmentPhase.phase")
            it = mdl.listResourcesWithProperty(pt_segment, r_line)
            w_a, w_b, w_c, w_n, w_s1, w_s2, w_s = "", "", "", "", "", "", ""

            while it.hasNext():
                r_p = it.nextResource()
                if r_p.hasProperty(pt_phase):
                    s_phase = self.phase_kind_string(r_p.getProperty(pt_phase).getObject().to"")
                    it_asset = mdl.listResourcesWithProperty(pt_asset_psr, r_p)

                    while it_asset.hasNext():
                        r_asset = it_asset.nextResource()
                        if r_asset.hasProperty(pt_asset_inf):
                            r_ds = r_asset.getProperty(pt_asset_inf).getResource()
                            # status = r_ds.as(OntResource.class).getRDFType().to""
                            s = str(r_ds.getRDFType())
                            hash = s.lastIndexOf("#")
                            t = s.substring(hash + 1)

                            if t == "ConcentricNeutralCableInfo":
                                b_cncables = True
                            if t == "TapeShieldCableInfo":
                                b_tscables = True
                            w_s = self.safe_res_name(r_ds, pt_name)

                            if s_phase == "A":
                                w_a = w_s
                            if s_phase == "B":
                                w_b = w_s
                            if s_phase == "C":
                                w_c = w_s
                            if s_phase == "N":
                                w_n = w_s
                            if s_phase == "s1":
                                w_s1 = w_s
                            if s_phase == "s2":
                                w_s2 = w_s

            if len(w_s) < 1:
                if b_cncables:
                    buf += " CNcables=["
                elif b_tscables:
                    buf += " TScables=["
                else:
                    buf += " wires=["

                for i in range(nconds):
                    buf += wire_name + " "

                buf += "]"
            else:
                if b_cncables:
                    buf += " CNcables=["
                elif b_tscables:
                    buf += " TScables=["
                else:
                    buf += " wires=["

                if len(w_a) > 0:
                    buf += w_a + " "
                if len(w_b) > 0:
                    buf += w_b + " "
                if len(w_c) > 0:
                    buf += w_c + " "
                if len(w_s1) > 0:
                    buf += w_s1 + " "
                if len(w_s2) > 0:
                    buf += w_s2 + " "

                if not (b_cncables or b_tscables):
                    for i in range(nconds - nphases):
                        buf += w_n + " "

                buf += "]"

                if nconds > nphases and (b_cncables or b_tscables):
                    buf += " wires=["

                    for i in range(nconds - nphases):
                        buf += w_n + " "

                    buf += "]"

            return buf

        return ""

    def get_wire_data(self, mdl, res):
        buf = ""

        pt_gmr = mdl.getProperty(self.ns_cim, "WireInfo.gmr")
        pt_wire_radius = mdl.getProperty(self.ns_cim, "WireInfo.radius")
        pt_wire_diameter = mdl.getProperty(self.ns_cim, "WireInfo.diameter")
        pt_wire_current = mdl.getProperty(self.ns_cim, "WireInfo.ratedCurrent")
        pt_wire_r25 = mdl.getProperty(self.ns_cim, "WireInfo.rAC25")
        pt_wire_r50 = mdl.getProperty(self.ns_cim, "WireInfo.rAC50")
        pt_wire_r75 = mdl.getProperty(self.ns_cim, "WireInfo.rAC75")
        pt_wire_rdc = mdl.getProperty(self.ns_cim, "WireInfo.rDC20")

        norm_amps = self.safe_double(res, pt_wire_current, 0.0)
        radius = self.safe_double(res, pt_wire_radius, 0.0)

        if radius <= 0:
            radius = 0.5 * self.safe_double(res, pt_wire_diameter, 0.0)

        gmr = self.safe_double(res, pt_gmr, 0.0)

        if gmr <= 0:
            gmr = 0.7788 * radius

        wire_rac = self.safe_double(res, pt_wire_r50, 0.0)

        if wire_rac <= 0:
            wire_rac = self.safe_double(res, pt_wire_r25, 0.0)

        if wire_rac <= 0:
            wire_rac = self.safe_double(res, pt_wire_r75, 0.0)

        wire_rdc = self.safe_double(res, pt_wire_rdc, 0.0)

        if wire_rdc <= 0:
            wire_rdc = wire_rac
        elif wire_rac <= 0:
            wire_rac = wire_rdc

        buf += " gmr=" + format(gmr, ".6g") + " radius=" + format(radius, ".6g") + \
            " rac=" + format(wire_rac, ".6g") + " rdc=" + format(wire_rdc, ".6g") + \
            " normamps=" + format(norm_amps, ".6g") + " Runits=multiplicities Radunits=multiplicities gmrunits=multiplicities"

        return buf

    def get_cable_data(self, mdl, res):
        buf = []

        pt_over_ins = mdl.get_property(self.ns_cim, "CableInfo.diameterOverInsulation")
        pt_over_jacket = mdl.get_property(self.ns_cim, "CableInfo.diameterOverJacket")
        pt_ins_layer = mdl.get_property(self.ns_cim, "WireInfo.insulationThickness")

        d_ins = self.safe_double(res, pt_over_ins, 0.0)
        d_jacket = self.safe_double(res, pt_over_jacket, 0.0)
        t_ins = self.safe_double(res, pt_ins_layer, 0.0)
        d_eps = 2.3  # TODO: How to put this into the CIM?

        buf.append(functions"\n~ EpsR={d_eps:.6f} Ins={t_ins:.6f} DiaIns={d_ins:.6f} DiaCable={d_jacket:.6f}")
        return ''.join(buf)

    def get_cap_control_data(self, mdl, r_cap, ctl):
        buf = []

        pt_term = mdl.get_property(self.ns_cim, "RegulatingControl.Terminal")
        pt_discrete = mdl.get_property(self.ns_cim, "RegulatingControl.discrete")
        pt_enabled = mdl.get_property(self.ns_cim, "RegulatingControl.enabled")
        pt_mode = mdl.get_property(self.ns_cim, "RegulatingControl.mode")
        pt_phase = mdl.get_property(self.ns_cim, "RegulatingControl.monitoredPhase")
        pt_bw = mdl.get_property(self.ns_cim, "RegulatingControl.targetDeadband")
        pt_val = mdl.get_property(self.ns_cim, "RegulatingControl.targetValue")
        pt_mult = mdl.get_property(self.ns_cim, "RegulatingControl.targetValueUnitMultiplier")
        pt_name = mdl.get_property(self.ns_cim, "IdentifiedObject.name")

        ctl_name = self.safe_res_name(ctl, pt_name)
        cap_name = self.safe_res_name(r_cap, pt_name)
        d_bw = self.safe_double(ctl, pt_bw, 1.0)
        d_val = self.safe_double(ctl, pt_val, 120.0)
        d_mult = self.safe_double(ctl, pt_mult, 1.0)
        d_on = d_mult * (d_val - 0.5 * d_bw)
        d_off = d_mult * (d_val + 0.5 * d_bw)
        b_discrete = self.safe_boolean(ctl, pt_discrete, True)
        b_enabled = self.safe_boolean(ctl, pt_enabled, True)
        s_phase = self.phase_string(self.safe_phases_x(ctl, pt_phase))
        s_mode = self.gld_cap_mode(self.safe_regulating_mode(ctl, pt_mode, "voltage"))

        pt_cond_eq = mdl.get_property(self.ns_cim, "Terminal.ConductingEquipment")
        r_term = mdl.get_property(ctl, pt_term).getResource()
        r_cond_eq = mdl.get_property(r_term, pt_cond_eq).getResource()
        s_eq_type = self.get_equipment_type(r_cond_eq)
        s_eq_name = self.safe_res_name(r_cond_eq, pt_name)

        nterm = 0
        s_match = self.safe_res_name(r_term, pt_name)
        iter = mdl.list_resources_with_property(pt_cond_eq, r_cond_eq)
        for r in iter:
            nterm += 1
            s = self.safe_res_name(r, pt_name)
            if s == s_match:
                break

        buf.append(functions"  control MANUAL; // {s_mode};\n")
        if s_mode == "VOLT":
            buf.append(functions"  voltage_set_low {d_on:.6f};\n")
            buf.append(functions"  voltage_set_high {d_off:.6f};\n")
        elif s_mode == "CURRENT":
            buf.append(functions"  current_set_low {d_on:.6f};\n")
            buf.append(functions"  current_set_high {d_off:.6f};\n")
        elif s_mode == "VAR":
            buf.append(functions"  VAr_set_low {d_off:.6f};\n")
            buf.append(functions"  VAr_set_high {d_on:.6f};\n")

        if s_eq_type != "cap" or s_eq_name != cap_name:
            buf.append(functions"  remote_sense \"{s_eq_type}_{s_eq_name}\";\n")

        buf.append(functions"  pt_phase {s_phase};\n")
        if len(s_phase) > 1:
            buf.append("  control_level INDIVIDUAL;")
        else:
            buf.append("  control_level BANK;")

        return ''.join(buf)

    def get_xfmr_code(self, mdl, _id, smult, vmult, b_want_sec):
        buf = []

        pt_info = mdl.get_property(self.ns_cim, "TransformerEndInfo.TransformerTankInfo")
        pt_end_n = mdl.get_property(self.ns_cim, "TransformerEndInfo.endNumber")
        pt_u = mdl.get_property(self.ns_cim, "TransformerEndInfo.ratedU")
        pt_s = mdl.get_property(self.ns_cim, "TransformerEndInfo.ratedS")
        pt_r = mdl.get_property(self.ns_cim, "TransformerEndInfo.r")
        pt_c = mdl.get_property(self.ns_cim, "TransformerEndInfo.connectionKind")
        pt_ck = mdl.get_property(self.ns_cim, "TransformerEndInfo.phaseAngleClock")
        pt_from = mdl.get_property(self.ns_cim, "ShortCircuitTest.EnergisedEnd")
        pt_to = mdl.get_property(self.ns_cim, "ShortCircuitTest.GroundedEnds")  # TODO: This is actually a collection
        pt_zsc = mdl.get_property(self.ns_cim, "ShortCircuitTest.leakageImpedance")
        pt_ll = mdl.get_property(self.ns_cim, "ShortCircuitTest.loss")
        pt_end = mdl.get_property(self.ns_cim, "NoLoadTest.EnergisedEnd")
        pt_nll = mdl.get_property(self.ns_cim, "NoLoadTest.loss")
        pt_imag = mdl.get_property(self.ns_cim, "NoLoadTest.excitingCurrent")

        xf_res = mdl.get_resource(_id)
        name = self.safe_res_name(xf_res, mdl.get_property(self.ns_cim, "IdentifiedObject.name"))

        n_windings = 0
        n_phases = 3
        iter = mdl.list_resources_with_property(pt_info, xf_res)
        for _ in iter:
            n_windings += 1

        d_u = [0.0] * n_windings
        d_s = [0.0] * n_windings
        d_r = [0.0] * n_windings
        d_xsc = [0.0] * n_windings
        z_base = [0.0] * n_windings
        s_c = [''] * n_windings
        d_nll = 0.0
        d_imag = 0.0
        d_xhl = 0.0
        d_xlt = 0.0
        d_xht = 0.0

        iter = mdl.list_resources_with_property(pt_info, xf_res)
        for wdg in iter:
            i = wdg.get_property(pt_end_n).get_int() - 1
            d_u[i] = vmult * self.safe_double(wdg, pt_u, 1.0)
            d_s[i] = smult * self.safe_double(wdg, pt_s, 1.0)
            d_r[i] = self.safe_double(wdg, pt_r, 0)
            z_base[i] = d_u[i] * d_u[i] / d_s[i]
            d_r[i] /= z_base[i]
            s_c[i] = self.get_wdg_connection(wdg, pt_c, "Y")
            if s_c[i] == "I":
                n_phases = 1

            iter_test = mdl.list_resources_with_property(pt_from, wdg)
            for test in iter_test:
                d_xsc[i] = self.safe_double(test, pt_zsc, 0.0001) / z_base[i]

            iter_test = mdl.list_resources_with_property(pt_end, wdg)
            for test in iter_test:
                d_nll = self.safe_double(test, pt_nll, 0)
                d_imag = self.safe_double(test, pt_imag, 0)

        ibase = d_s[0] / d_u[0]
        if n_phases > 1:
            ibase /= 3.0 ** 0.5
            for i in range(n_windings):
                d_u[i] /= 3.0 ** 0.5
        d_nll /= d_s[0]
        d_imag /= 100.0  # This puts d_im in per-unit
        d_imag /= ibase
        connect_type = self.get_gld_transformer_connection(s_c, n_windings)

        if not b_want_sec and connect_type == "SINGLE_PHASE_CENTER_TAPPED":
            return ""

        buf.append("object transformer_configuration {")
        buf.append(functions"  name \"xcon_{name}\";")
        buf.append(functions"  connect_type {connect_type};")
        buf.append(functions"  primary_voltage {d_u[0]:.6f};")
        buf.append(functions"  secondary_voltage {d_u[1]:.6f};")
        buf.append(functions"  power_rating {0.001 * d_s[0]:.6f};")  # kva

        if connect_type == "SINGLE_PHASE_CENTER_TAPPED":
            buf.append("  // The default split puts 50% of R and 80% of X on the H branch")
            buf.append(functions"  // resistance {d_r[1]:.6f};")
            buf.append(functions"  // reactance {d_xsc[0]:.6f};")
            d_x0 = 0.5 * (d_xsc[0] + d_xsc[0] - d_xsc[1])
            d_x1 = 0.5 * (d_xsc[0] + d_xsc[1] - d_xsc[0])
            d_x2 = 0.5 * (d_xsc[0] + d_xsc[1] - d_xsc[0])
            buf.append(functions"  impedance {CIMDataRDFToGLM.c_format(complex(d_r[0], d_x0))};")
            buf.append(functions"  impedance1 {CIMDataRDFToGLM.c_format(complex(d_r[1], d_x1))};")
            buf.append(functions"  impedance2 {CIMDataRDFToGLM.c_format(complex(d_r[2], d_x2))};")
        else:
            buf.append(functions"  resistance {d_r[0] + d_r[1]:.6f};")
            buf.append(functions"  reactance {d_xsc[0]:.6f};")

        if d_nll > 0.0:
            buf.append(functions"  shunt_resistance {1.0 / d_nll:.6f};")
        if d_imag > 0.0:
            buf.append(functions"  shunt_reactance {1.0 / d_imag:.6f};")

        buf.append("}")
        return '\n'.join(buf)


    def get_bus_position_string(self, mdl, id):
        pt_x = mdl.get_property(self.ns_cim, "PositionPoint.xPosition")
        pt_y = mdl.get_property(self.ns_cim, "PositionPoint.yPosition")
        pt_pos_seq = mdl.get_property(self.ns_cim, "PositionPoint.sequenceNumber")
        pt_loc = mdl.get_property(self.ns_cim, "PositionPoint.Location")
        pt_geo = mdl.get_property(self.ns_cim, "PowerSystemResource.Location")

        pt_bank = mdl.get_property(self.ns_cim, "DistributionTransformer.TransformerBank")
        pt_xfmr = mdl.get_property(self.ns_cim, "DistributionTransformerWinding.Transformer")

        pt_node = mdl.get_property(self.ns_cim, "Terminal.ConnectivityNode")
        pt_trm_seq = mdl.get_property(self.ns_cim, "Terminal.sequenceNumber")
        pt_equip = mdl.get_property(self.ns_cim, "Terminal.ConductingEquipment")

        # for drilling Eq=>VoltageLevel=>Sub=>Geo, or Eq=>Line=>Geo
        pt_cont = mdl.get_property(self.ns_cim, "Equipment.EquipmentContainer")
        pt_sub = mdl.get_property(self.ns_cim, "VoltageLevel.Substation")

        bus = mdl.get_resource(id)
        trm, eq = None, None
        trm_seq = "1"

        geo = None
        ref_geo = None  # bank, line, or substation

        # first look for a terminal equipment that directly has a GeoLocation
        # but the GeoLocation could also be on a TransformerBank, Line, or Substation
        terms = mdl.list_resources_with_property(pt_node, bus)
        while terms.has_next() and geo is None:
            trm = terms.next_resource()
            eq = trm.get_property(pt_equip).get_resource()
            if eq.has_property(pt_geo):
                geo = eq.get_property(pt_geo).get_resource()
                trm_seq = self.safe_property(trm, pt_trm_seq, "1")
            elif eq.has_property(pt_xfmr):
                xf = eq.get_property(pt_xfmr).get_resource()
                if xf.has_property(pt_bank):
                    bank = xf.get_property(pt_bank).get_resource()
                    if bank.has_property(pt_geo):
                        ref_geo = bank.get_property(pt_geo).get_resource()
            elif eq.has_property(pt_cont):
                rcont = eq.get_property(pt_cont).get_resource()
                if rcont.has_property(pt_geo):
                    ref_geo = rcont.get_property(pt_geo).get_resource()
                elif rcont.has_property(pt_sub):
                    rsub = eq.get_property(pt_sub).get_resource()
                    if rsub.has_property(pt_geo):
                        ref_geo = rsub.get_property(pt_geo).get_resource()

        if geo is None:
            geo = ref_geo

        if geo is not None:
            iter = mdl.list_resources_with_property(pt_loc, geo)
            pos = None
            while iter.has_next():
                pos = iter.next_resource()
                if pos.has_property(pt_pos_seq, trm_seq):
                    return pos.get_property(pt_x).get_"" + ", " + pos.get_property(pt_y).get_""
            if pos is not None:
                return pos.get_property(pt_x).get_"" + ", " + pos.get_property(pt_y).get_""
        else:
            # print("NO GEO FOUND")
            pass

        return ""


    def find_conductor_amps(self, mdl, res, pt_data_sheet, pt_amps):
        i_min = 1.0
        i_val = 0.0
        if res.has_property(pt_data_sheet):
            r_inf = res.get_property(pt_data_sheet).get_resource()
            if r_inf.has_property(pt_amps):
                i_val = self.safe_double(r_inf, pt_amps, 0.0)
                if i_val > i_min:
                    i_min = i_val
        return ""
        # return " normamps=" + functions"{i_min:.6f}"

    def find_base_voltage(self, res, pt_equip, pt_eq_base_v, pt_lev_base_v, pt_base_nom_v):
        r_base = None
        if res.has_property(pt_eq_base_v):
            r_base = res.get_property(pt_eq_base_v).get_resource()
        elif res.has_property(pt_equip):
            r_equip = res.get_property(pt_equip).get_resource()
            if r_equip.has_property(pt_eq_base_v):
                r_base = r_equip.get_property(pt_eq_base_v).get_resource()
            elif r_equip.has_property(pt_lev_base_v):
                r_base = r_equip.get_property(pt_lev_base_v).get_resource()
        if r_base is not None:
            return self.safe_double(r_base, pt_base_nom_v, 1.0)
        return 1.0

    def get_sequence_line_configurations(self, name, sq_r1, sq_x1, sq_c1, sq_r0, sq_x0, sq_c0):
        seq_zs = self.c_format(complex((sq_r0 + 2.0 * sq_r1) / 3.0, (sq_x0 + 2.0 * sq_x1) / 3.0))
        seq_zm = self.c_format(complex((sq_r0 - sq_r1) / 3.0, (sq_x0 - sq_x1) / 3.0))
        seq_cs = functions"{(sq_c0 + 2.0 * sq_c1) / 3.0:.6f}"
        seq_cm = functions"{(sq_c0 - sq_c1) / 3.0:.6f}"

        buf = []

        buf.append(functions"object line_configuration {{")
        buf.append(functions"  name \"lcon_{name}_ABC\";")
        buf.append(functions"  z11 {seq_zs};")
        buf.append(functions"  z12 {seq_zm};")
        buf.append(functions"  z13 {seq_zm};")
        buf.append(functions"  z21 {seq_zm};")
        buf.append(functions"  z22 {seq_zs};")
        buf.append(functions"  z23 {seq_zm};")
        buf.append(functions"  z31 {seq_zm};")
        buf.append(functions"  z32 {seq_zm};")
        buf.append(functions"  z33 {seq_zs};")
        buf.append(functions"  c11 {seq_cs};")
        buf.append(functions"  c12 {seq_cm};")
        buf.append(functions"  c13 {seq_cm};")
        buf.append(functions"  c21 {seq_cm};")
        buf.append(functions"  c22 {seq_cs};")
        buf.append(functions"  c23 {seq_cm};")
        buf.append(functions"  c31 {seq_cm};")
        buf.append(functions"  c32 {seq_cm};")
        buf.append(functions"  c33 {seq_cs};")
        buf.append(functions"}}")

        buf.append(functions"object line_configuration {{")
        buf.append(functions"  name \"lcon_{name}_AB\";")
        buf.append(functions"  z11 {seq_zs};")
        buf.append(functions"  z12 {seq_zm};")
        buf.append(functions"  z21 {seq_zm};")
        buf.append(functions"  z22 {seq_zs};")
        buf.append(functions"  c11 {seq_cs};")
        buf.append(functions"  c12 {seq_cm};")
        buf.append(functions"  c21 {seq_cm};")
        buf.append(functions"  c22 {seq_cs};")
        buf.append(functions"}}")

        buf.append(functions"object line_configuration {{")
        buf.append(functions"  name \"lcon_{name}_AC\";")
        buf.append(functions"  z11 {seq_zs};")
        buf.append(functions"  z13 {seq_zm};")
        buf.append(functions"  z31 {seq_zm};")
        buf.append(functions"  z33 {seq_zs};")
        buf.append(functions"  c11 {seq_cs};")
        buf.append(functions"  c13 {seq_cm};")
        buf.append(functions"  c31 {seq_cm};")
        buf.append(functions"  c33 {seq_cs};")
        buf.append(functions"}}")

        buf.append(functions"object line_configuration {{")
        buf.append(functions"  name \"lcon_{name}_BC\";")
        buf.append(functions"  z22 {seq_zs};")
        buf.append(functions"  z23 {seq_zm};")
        buf.append(functions"  z32 {seq_zm};")
        buf.append(functions"  z33 {seq_zs};")
        buf.append(functions"  c22 {seq_cs};")
        buf.append(functions"  c23 {seq_cm};")
        buf.append(functions"  c32 {seq_cm};")
        buf.append(functions"  c33 {seq_cs};")
        buf.append(functions"}}")

        buf.append(functions"object line_configuration {{")
        buf.append(functions"  name \"lcon_{name}_A\";")
        buf.append(functions"  z11 {seq_zs};")
        buf.append(functions"  c11 {seq_cs};")
        buf.append(functions"}}")

        buf.append(functions"object line_configuration {{")
        buf.append(functions"  name \"lcon_{name}_B\";")
        buf.append(functions"  z22 {seq_zs};")
        buf.append(functions"  c22 {seq_cs};")
        buf.append(functions"}}")

        buf.append(functions"object line_configuration {{")
        buf.append(functions"  name \"lcon_{name}_C\";")
        buf.append(functions"  z33 {seq_zs};")
        buf.append(functions"  c33 {seq_cs};")
        buf.append(functions"}}")

        return "\n".join(buf)

    def get_ac_line_parameters(self, mdl, name, r, len, freq, phs, out):
        pt_r1 = mdl.get_property(self.ns_cim, "ACLineSegment.r")
        pt_r0 = mdl.get_property(self.ns_cim, "ACLineSegment.r0")
        pt_x1 = mdl.get_property(self.ns_cim, "ACLineSegment.x")
        pt_x0 = mdl.get_property(self.ns_cim, "ACLineSegment.x0")
        pt_b1 = mdl.get_property(self.ns_cim, "ACLineSegment.bch")
        pt_b0 = mdl.get_property(self.ns_cim, "ACLineSegment.b0ch")

        if r.has_property(pt_x1):
            r1 = self.safe_double(r, pt_r1, 0)
            r0 = self.safe_double(r, pt_r0, 0)
            x1 = self.safe_double(r, pt_x1, 0)
            x0 = self.safe_double(r, pt_x0, x1)
            b0 = self.safe_double(r, pt_b0, 0)
            b1 = self.safe_double(r, pt_b1, b0)
            c0 = 1.0e9 * b0 / freq / 2.0 / math.pi
            c1 = 1.0e9 * b1 / freq / 2.0 / math.pi
            scale = 5280.0 / len  # so that we end up with ohms and nF for len[ft]*sequence config Z [per mile]
            out.append(self.get_sequence_line_configurations(name, scale * r1, scale * x1, scale * c1, scale * r0, scale * x0, scale * c0))
            return functions"lcon_{name}_{phs}"
        return ""

    def process(self, args):
        fName = ""
        fOut = ""
        fBus = ""
        fEnc = ""
        freq = 60.0
        vmult = 0.001
        smult = 0.001
        load_scale = 1.0
        fInFile = 0
        fNameSeq = 0
        bWantSched = False
        bWantZIP = False
        bWantSec = True
        fSched = ""
        Zcoeff = 0.0
        Icoeff = 0.0
        Pcoeff = 0.0

        parser = argparse.ArgumentParser(description="CDPSM_to_GLM converter")
        parser.add_argument("input_file", help="Input XML file")
        parser.add_argument("output_root", help="Root input_code_filename for output files")
        parser.add_argument("-l", "--load_scale", type=float, default=1.0, help="Load scaling factor (default: 1.0)")
        parser.add_argument("-t", "--triplex", choices=["y", "dimensions"], default="y",
                           help="Include secondary for triplex (default: y)")
        parser.add_argument("-e", "--encoding", choices=["u", "i"], default="u",
                           help="Encoding (UTF-8 or ISO-8859-1, default: u)")
        parser.add_argument("-functions", "--frequency", type=float, choices=[50.0, 60.0], default=60.0,
                           help="System frequency (default: 60.0)")
        parser.add_argument("-v", "--vmult", type=float, choices=[1.0, 0.001], default=0.001,
                           help="Multiplier for converting voltage to V for GridLAB-D (default: 0.001)")
        parser.add_argument("-status", "--smult", type=float, choices=[1000.0, 1.0, 0.001], default=0.001,
                           help="Multiplier for converting precisions,q,status to VA for GridLAB-D (default: 0.001)")
        parser.add_argument("-q", "--unique_names", choices=["y", "dimensions"], default="y", help="Use unique names (default: y)")
        parser.add_argument("-dimensions", "--schedule_name", help="Root input_code_filename for scheduled ZIP loads (default: none)")
        parser.add_argument("-z", "--constant_z", type=float, choices=[0.0, 1.0], default=0.0,
                           help="Constant Z portion (default: 0.0 for CIM-defined)")
        parser.add_argument("-i", "--constant_i", type=float, choices=[0.0, 1.0], default=0.0,
                           help="Constant I portion (default: 0.0 for CIM-defined)")
        parser.add_argument("-precisions", "--constant_p", type=float, choices=[0.0, 1.0], default=0.0,
                            help="Constant P portion (default: 0.0 for CIM-defined)")

        args = parser.parse_args(args)

        fName = args.input_file
        fOut = args.output_root + "_base.glm"
        fBus = args.output_root + "_busxy.glm"

        if args.encoding == "u":
            fEnc = "UTF8"
        else:
            fEnc = "ISO-8859-1"

        freq = args.frequency
        vmult = args.vmult
        smult = args.smult
        load_scale = args.load_scale

        if args.triplex == "dimensions":
            bWantSec = False

        if args.unique_names == "dimensions":
            fNameSeq = 1

        if args.schedule_name:
            fSched = args.schedule_name
            bWantSched = True

        Zcoeff = args.constant_z
        Icoeff = args.constant_i
        Pcoeff = args.constant_p

        if Pcoeff:
            bWantZIP = True

        print(functions"{fEnc} functions={freq:.6f} v={vmult:.6f} status={smult:.6f}")

        model = rdflib.Graph()
        model.parse(fName, format="xml")

        with open(fOut, 'w', newline='') as out, open(fBus, 'w', newline='') as outBus:
            writer = csv.writer(out)
            writer_bus = csv.writer(outBus)

            print("***** XML has been read *****")

            q_prefix = functions"PREFIX r: <{self.ns_rdf}> PREFIX c: <{self.ns_cim}> "
            ptName = model.getProperty(self.ns_cim, "IdentifiedObject.name")
            ptType = model.getProperty(self.ns_rdf, "type")
            ptOpen = model.getProperty(self.ns_cim, "Switch.normalOpen")

            ptEqBaseV = model.getProperty(self.ns_cim, "ConductingEquipment.BaseVoltage")
            ptLevBaseV = model.getProperty(self.ns_cim, "VoltageLevel.BaseVoltage")
            ptEquip = model.getProperty(self.ns_cim, "Equipment.EquipmentContainer")
            ptBaseNomV = model.getProperty(self.ns_cim, "BaseVoltage.nominalVoltage")


            # Dump all the GeoLocation references
            #
            # pt_geo = rdflib.URIRef(self.ns_cim + "PowerSystemResource.GeoLocation")
            # query = functions"{q_prefix}select ?status where {{?status r:type c:GeoLocation}}"
            # results = model.query(query)
            # for row in results:
            #     id = row[0].toPython()
            #     res = model.resource(id)
            #     name = self.safe_res_name(res, ptName)
            #     it = model.subjects(pt_geo, res)
            #     for rEq in it:
            #         s_type = rEq.value(model.predicate(self.ns_rdf + "type")).toPython()
            #         writer_bus.writerow(["// " + name + "==>" + s_type + ":" + self.safe_res_name(rEq, ptName)])
            # writer_bus.writerow()
            #

            # ConnectivityNode ==> bus coordinate CSV
            query = functions"{q_prefix}select ?status where {{?status r:type c:ConnectivityNode}}"
            results = model.query(query)
            for row in results:
                id = row[0].toPython()
                res = model.resource(id)
                name = self.gld_prefixed_node_name(self.safe_res_name(res, ptName))
                str_pos = self.get_bus_position_string(model, id)
                if len(str_pos) > 0:
                    writer_bus.writerow([functions'"{name}", {str_pos}'])
                else:
                    writer_bus.writerow(["// " + name + ", *****"])
                self.map_nodes[name] = GldNode(name)
            writer_bus.writerow()

            # EnergySource ==> Circuit
            NumCircuits = 0
            NumSources = 0
            query = functions"{q_prefix}select ?status ?name ?v ?ckt where {{?status r:type c:EnergySource. " \
                    functions"?status c:IdentifiedObject.name ?name;" \
                    functions" c:EnergySource.voltageMagnitude ?v;" \
                    functions" c:Equipment.EquipmentContainer ?ckt" \
                    functions"}}"
            results = model.query(query)
            ptESr0 = rdflib.URIRef(self.ns_cim + "EnergySource.r0")
            ptESr1 = rdflib.URIRef(self.ns_cim + "EnergySource.r")
            ptESx0 = rdflib.URIRef(self.ns_cim + "EnergySource.x0")
            ptESx1 = rdflib.URIRef(self.ns_cim + "EnergySource.x")
            ptESVnom = rdflib.URIRef(self.ns_cim + "EnergySource.nominalVoltage")
            ptESVmag = rdflib.URIRef(self.ns_cim + "EnergySource.voltageMagnitude")
            ptESVang = rdflib.URIRef(self.ns_cim + "EnergySource.voltageAngle")
            for row in results:
                NumSources += 1
                id = row[0].toPython()
                name = self.gld_name(row[1].toPython(), False)
                vSrce = row[2].toPython()
                ckt = row[3].toPython()
                res = model.resource(id)
                vmag = vmult * self.safe_double(res, ptESVmag, 1.0)
                vnom = vmult * self.safe_double(res, ptESVnom, vmag)
                vang = self.safe_double(res, ptESVang, 0.0) * 57.3
                r0 = self.safe_double(res, ptESr0, 0.0)
                r1 = self.safe_double(res, ptESr1, 0.0)
                x1 = self.safe_double(res, ptESx1, 0.001)
                x0 = self.safe_double(res, ptESx0, x1)
                vpu = vmag / vnom
                bus1 = self.get_bus_name(model, id, 1)  # TODO - no phase model
                srcClass = "Vsource."
                if NumCircuits < 1:
                    srcClass = "Circuit."
                    name = self.gld_name(self.get_prop_value(model, ckt, "IdentifiedObject.name"), False)
                    nd = self.map_nodes[bus1]
                    nd.bSwing = True
                    NumCircuits = 1
                elif name == "source":
                    name = "_" + name
            if NumCircuits < 1:  # // try the first breaker
                query = functions"{q_prefix}select ?status where {{?status r:type c:Breaker}}"
                results = model.query(query)
                for row in results:
                    id = row[0].toPython()
                    res = model.resource(id)
                    bus1 = self.get_bus_name(model, id, 1)
                    nd = self.map_nodes[bus1]
                    nd.bSwing = True
                    name = self.safe_res_name(res, ptName)
                    # out.write("new Circuit." + name + " phases=3 bus1=" + bus1 + " basekv=1\dimensions")
            # out.write("// set frequency=" + "{:6g}".format(freq))

            # SynchronousMachine ==> Generator
            writer.writerow()
            query = functions"{q_prefix}select ?status where {{?status r:type c:SynchronousMachine}}"
            results = model.query(query)
            ptGenS = rdflib.URIRef(self.ns_cim + "GeneratingUnit.ratedNetMaxP")
            ptGenP = rdflib.URIRef(self.ns_cim + "GeneratingUnit.initialP")
            ptGenRef = rdflib.URIRef(self.ns_cim + "SynchronousMachine.GeneratingUnit")
            ptGenQ = rdflib.URIRef(self.ns_cim + "SynchronousMachine.baseQ")
            ptGenQmin = rdflib.URIRef(self.ns_cim + "SynchronousMachine.minQ")
            ptGenQmax = rdflib.URIRef(self.ns_cim + "SynchronousMachine.maxQ")


            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""

                res = model.getResource(id)
                # TODO - generators need phase modeling as well
                bus1 = self.get_bus_name(model, id, 1)
                name = self.safe_res_name(res, ptName)
                resUnit = res.getProperty(ptGenRef).getResource()

                genS = self.safe_double(resUnit, ptGenS, 1.0) * 1000.0  # assume MW per CPSM
                genP = self.safe_double(resUnit, ptGenP, 1.0) * 1000.0
                genQ = self.safe_double(res, ptGenQ, 0.0) * 1000.0
                genQmin = self.safe_double(res, ptGenQmin, 0.44 * genS) * 1000.0 * -1.0
                genQmax = self.safe_double(res, ptGenQmax, 0.44 * genS) * 1000.0
                genKv = vmult * self.find_base_voltage(res, ptEquip, ptEqBaseV,
                                                  ptLevBaseV, ptBaseNomV)

                # out.write ("new Generator." + name + " phases=3 bus1=" + bus1 +
                #                            " conn=w kva=" + String.format("%6g", genS) + " kw=" + String.format("%6g", genP) +
                #                            " kvar=" + String.format("%6g", genQ) + " minkvar=" + String.format("%6g", genQmin) +
                #                            " maxkvar=" + String.format("%6g", genQmax) + " kv=" + String.format("%6g", genKv))

            # EnergyConsumer ==> Load
            total_load_w = 0.0
            out.write("\n")
            query = QueryFactory.create(self.qPrefix + "select ?status where {?status r:type c:EnergyConsumer}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            ptP = model.getProperty(self.ns_cim, "EnergyConsumer.pfixed")
            ptQ = model.getProperty(self.ns_cim, "EnergyConsumer.qfixed")
            ptCust = model.getProperty(self.ns_cim, "EnergyConsumer.customerCount")
            ptPhsLoad1 = model.getProperty(self.ns_cim, "EnergyConsumerPhase.EnergyConsumer")
            ptPhsLoad2 = model.getProperty(self.ns_cim, "EnergyConsumerPhase.phase")
            ptConnLoad = model.getProperty(self.ns_cim, "EnergyConsumer.phaseConnection")
            ptResponse = model.getProperty(self.ns_cim, "EnergyConsumer.LoadResponse")
            ptPv = model.getProperty(self.ns_cim, "LoadResponseCharacteristic.pVoltageExponent")
            ptQv = model.getProperty(self.ns_cim, "LoadResponseCharacteristic.qVoltageExponent")
            ptPz = model.getProperty(self.ns_cim, "LoadResponseCharacteristic.pConstantImpedance")
            ptPi = model.getProperty(self.ns_cim, "LoadResponseCharacteristic.pConstantCurrent")
            ptPp = model.getProperty(self.ns_cim, "LoadResponseCharacteristic.pConstantPower")
            ptQz = model.getProperty(self.ns_cim, "LoadResponseCharacteristic.qConstantImpedance")
            ptQi = model.getProperty(self.ns_cim, "LoadResponseCharacteristic.qConstantCurrent")
            ptQp = model.getProperty(self.ns_cim, "LoadResponseCharacteristic.qConstantPower")
            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""

                res = model.getResource(id)
                phs = self.wire_phases(model, res, ptPhsLoad1, ptPhsLoad2)
                phs_delta = self.shunt_delta(res, ptConnLoad)
                bus1 = self.get_bus_name(model, id, 1)

                name = self.safe_res_name(res, ptName)  # not used as a parameter
                pL = smult * self.safe_double(res, ptP, 1)
                qL = smult * self.safe_double(res, ptQ, 0)
                total_load_w += pL
                Pp = 100
                Qp = 100
                Pv = 0
                Qv = 0
                Pz = 0
                Qz = 0
                Pi = 0
                Qi = 0
                if res.hasProperty(ptResponse):
                    rModel = res.getProperty(ptResponse).getResource()
                    Pv = self.safe_double(rModel, ptPv, 0)
                    Qv = self.safe_double(rModel, ptQv, 0)
                    Pz = self.safe_double(rModel, ptPz, 0)
                    Pi = self.safe_double(rModel, ptPi, 0)
                    Pp = self.safe_double(rModel, ptPp, 0)
                    Qz = self.safe_double(rModel, ptQz, 0)
                    Qi = self.safe_double(rModel, ptQi, 0)
                    Qp = self.safe_double(rModel, ptQp, 0)

                nd = self.map_nodes[bus1]
                nd.nomvln = self.find_base_voltage(res, ptEquip, ptEqBaseV,
                                              ptLevBaseV, ptBaseNomV) / math.sqrt(3.0)
                nd.bDelta = phs_delta
                # accumulate P and Q by phase first, and only then update the node phases
                self.accumulate_loads(nd, phs, pL, qL, Pv, Qv, Pz, Pi, Pp, Qz, Qi, Qp)

            # LinearShuntCompensator ==> Capacitor
            out.write("\n")
            query = QueryFactory.create(self.qPrefix + "select ?status ?name where {?status r:type c:LinearShuntCompensator. " +
                                        "?status c:IdentifiedObject.name ?name" +
                                        "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            ptSecB = model.getProperty(self.ns_cim, "LinearShuntCompensator.bPerSection")
            ptSecN = model.getProperty(self.ns_cim, "LinearShuntCompensator.normalSections")
            ptNumSteps = model.getProperty(self.ns_cim, "ShuntCompensator.maximumSections")
            ptPhsShunt1 = model.getProperty(self.ns_cim, "ShuntCompensatorPhase.ShuntCompensator")
            ptPhsShunt2 = model.getProperty(self.ns_cim, "ShuntCompensatorPhase.phase")
            ptConnShunt = model.getProperty(self.ns_cim, "ShuntCompensator.phaseConnection")
            ptAVRDelay = model.getProperty(self.ns_cim, "ShuntCompensator.aVRDelay")
            ptNomU = model.getProperty(self.ns_cim, "ShuntCompensator.nomU")
            ptCapCtl = model.getProperty(self.ns_cim, "RegulatingControl.RegulatingCondEq")

            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)
                phs = self.wire_phases(model, res, ptPhsShunt1, ptPhsShunt2)
                phs_delta = self.shunt_delta(res, ptConnShunt)
                bus1 = self.get_bus_name(model, id, 1)
                nd = self.map_nodes[bus1]
                nd.nomvln = self.find_base_voltage(res, ptEquip, ptEqBaseV, ptLevBaseV,
                                              ptBaseNomV) / math.sqrt(3.0)
                nd.add_phases(phs)

                cap_b = self.safe_int(res, ptNumSteps, 1) * self.safe_double(res, ptSecB, 0.0001)
                cap_v = self.safe_double(res, ptNomU, 120.0)
                cap_q = cap_v * cap_v * cap_b
                cap_q /= len(phs)
                if len(phs) > 1 and not phs_delta:
                    cap_v /= math.sqrt(3.0)

                out.write("object capacitor {" + "\n")
                out.write("    name \"cap_" + name + "\";" + "\n")
                out.write("    parent \"" + bus1 + "\";" + "\n")
                if phs_delta:
                    out.write("    phases " + phs + "D;" + "\n")
                    out.write("    phases_connected " + phs + "D;" + "\n")
                else:
                    out.write("    phases " + phs + "N;" + "\n")
                    out.write("    phases_connected " + phs + "N;" + "\n")
                out.write("    cap_nominal_voltage " + "{:6g}".format(cap_v) + ";" + "\n")
                if "A" in phs:
                    out.write("    capacitor_A " + "{:6g}".format(cap_q) + ";" + "\n")
                    out.write("    switchA CLOSED;" + "\n")
                if "B" in phs:
                    out.write("    capacitor_B " + "{:6g}".format(cap_q) + ";" + "\n")
                    out.write("    switchB CLOSED;" + "\n")
                if "C" in phs:
                    out.write("    capacitor_C " + "{:6g}".format(cap_q) + ";" + "\n")
                    out.write("    switchC CLOSED;" + "\n")

                # see if we have capacitor control settings
                itCtl = model.listResourcesWithProperty(ptCapCtl, res)
                if itCtl.hasNext():
                    out.write(self.get_cap_control_data(model, res, itCtl.nextResource()) + "\n")
                    delay = self.safe_double(res, ptAVRDelay, 10.0)
                    out.write("    dwell_time " + "{:6g}".format(delay) + ";" + "\n")

                out.write("}" + "\n")

            # for GridLAB-D, we need to write the transformers first so that we can identify
            # the secondary nodes and carry primary phasing down to them
            # Transformer Codes
            out.write("\n")
            query = QueryFactory.create(self.qPrefix + "select ?status ?name where {?status r:type c:TransformerTankInfo. " +
                                        "?status c:IdentifiedObject.name ?name" +
                                        "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                s = self.get_xfmr_code(model, id, smult, vmult, bWantSec)
                if len(s) > 0:
                    out.write(s + "\n")

            # Transformers
            out.write("\n")
            query = QueryFactory.create(self.qPrefix + "select ?status ?name where {?status r:type c:PowerTransformer. " +
                                        "?status c:IdentifiedObject.name ?name" +
                                        "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)

                ptTank = model.getProperty(self.ns_cim, "TransformerTank.PowerTransformer")
                itTank = model.listResourcesWithProperty(ptTank, res)
                if itTank.hasNext():  # write all the tanks to this bank
                    s = self.get_power_transformer_tanks(model, res, itTank, bWantSec)
                    if len(s) > 0:
                        out.write(s + "\n")
                else:  # standalone power transformer
                    out.write(self.get_power_transformer_data(model, res) + "\n")

            # WireData
            out.write("\n")
            query = QueryFactory.create(self.qPrefix + "select ?status where {?status r:type c:OverheadWireInfo}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""
                res = model.getResource(id)
                name = self.safe_res_name(res, ptName)

                # out.write ("new WireData." + name  + GetWireData (model, res))

            out.write("\n")
            query = QueryFactory.create(self.qPrefix + "select ?status where {?status r:type c:TapeShieldCableInfo}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            ptLap = model.getProperty(self.ns_cim, "TapeShieldCableInfo.tapeLap")
            ptThickness = model.getProperty(self.ns_cim, "TapeShieldCableInfo.tapeThickness")
            ptOverScreen = model.getProperty(self.ns_cim, "CableInfo.diameterOverScreen")

            while results.hasNext():
                soln = results.next()
                id = soln.get("?status").to""
                res = model.getResource(id)
                name = self.safe_res_name(res, ptName)

                tapeLap = self.safe_double(res, ptLap, 0.0)
                tapeThickness = self.safe_double(res, ptThickness, 0.0)
                dScreen = self.safe_double(res, ptOverScreen, 0.0)

                # out.write ("new TSData." + name + GetWireData (model, res) + GetCableData (model, res) +
                # " DiaShield=" + String.format("%6g", dScreen + 2.0 * tapeThickness) +
                # " tapeLayer=" + String.format("%6g", tapeThickness) + " tapeLap=" + String.format("%6g", tapeLap))

            out.write("\n")
            query = QueryFactory.create(self.qPrefix + "select ?status where {?status r:type c:ConcentricNeutralCableInfo}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            ptOverNeutral = model.getProperty(self.ns_cim, "ConcentricNeutralCableInfo.diameterOverNeutral")
            ptStrandCount = model.getProperty(self.ns_cim, "ConcentricNeutralCableInfo.neutralStrandCount")
            ptStrandGmr = model.getProperty(self.ns_cim, "ConcentricNeutralCableInfo.neutralStrandGmr")
            ptStrandRadius = model.getProperty(self.ns_cim, "ConcentricNeutralCableInfo.neutralStrandRadius")
            ptStrandRes = model.getProperty(self.ns_cim, "ConcentricNeutralCableInfo.neutralStrandRDC20")

            while results.hasNext():
                soln = results.next()
                id = soln.get("?status").to""
                res = model.getResource(id)
                name = self.safe_res_name(res, ptName)

                cnDia = self.safe_double(res, ptOverNeutral, 0.0)
                cnCount = self.safe_int(res, ptStrandCount, 0)
                cnGmr = self.safe_double(res, ptStrandGmr, 0.0)
                cnRadius = self.safe_double(res, ptStrandRadius, 0.0)
                cnRes = self.safe_double(res, ptStrandRes, 0.0)

                # out.write ("new CNData." + name + GetWireData (model, res) + GetCableData (model, res) +
                # " k=" + Integer.toString(cnCount) + " GmrStrand=" + String.format("%6g", cnGmr) +
                # " DiaStrand=" + String.format("%6g", 2 * cnRadius) + " Rstrand=" + String.format("%6g", cnRes))

            out.write("\n")
            query = QueryFactory.create(self.qPrefix + "select ?status ?name where {?status r:type c:WireSpacingInfo. " +
                                       "?status c:IdentifiedObject.name ?name" +
                                       "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            ptWireX = model.getProperty(self.ns_cim, "WirePosition.xCoord")
            ptWireY = model.getProperty(self.ns_cim, "WirePosition.yCoord")
            ptWireP = model.getProperty(self.ns_cim, "WirePosition.phase")
            ptWireS = model.getProperty(self.ns_cim, "WirePosition.WireSpacingInfo")

            while results.hasNext():
                soln = results.next()
                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)

                nconds = 0
                nphases = 0
                wireXa = 0
                wireXb = 0
                wireXc = 0
                wireXn = 0
                wireXs1 = 0
                wireXs2 = 0
                wireYa = 0
                wireYb = 0
                wireYc = 0
                wireYn = 0
                wireYs1 = 0
                wireYs2 = 0
                wireA = False
                wireB = False
                wireC = False
                wireN = False
                wireS1 = False
                wireS2 = False

                wIter = model.listResourcesWithProperty(ptWireS, res)
                while wIter.hasNext():
                    wa = wIter.nextResource()
                    nconds += 1
                    phs = self.Phase_Kind_String(wa.getProperty(ptWireP).getObject().to"")  # TODO - protect
                    if phs == "A":
                        wireXa = self.safe_double(wa, ptWireX, 0)
                        wireYa = self.safe_double(wa, ptWireY, 0)
                        wireA = True
                        nphases += 1
                    if phs == "B":
                        wireXb = self.safe_double(wa, ptWireX, 0)
                        wireYb = self.safe_double(wa, ptWireY, 0)
                        wireB = True
                        nphases += 1
                    if phs == "C":
                        wireXc = self.safe_double(wa, ptWireX, 0)
                        wireYc = self.safe_double(wa, ptWireY, 0)
                        wireC = True
                        nphases += 1
                    if phs == "N":
                        wireXn = self.safe_double(wa, ptWireX, 0)
                        wireYn = self.safe_double(wa, ptWireY, 0)
                        wireN = True
                    if phs == "s1":
                        wireXs1 = self.safe_double(wa, ptWireX, 0)
                        wireYs1 = self.safe_double(wa, ptWireY, 0)
                        wireS1 = True
                        nphases += 1
                    if phs == "s2":
                        wireXs2 = self.safe_double(wa, ptWireX, 0)
                        wireYs2 = self.safe_double(wa, ptWireY, 0)
                        wireS2 = True
                        nphases += 1

                if nconds > 0 and nphases > 0:
                    self.map_spacings[name] = SpacingCount(nconds, nphases)  # keep track for wire assignments below
                    # out.write ("new LineSpacing." + name + " nconds=" + Integer.toString(nconds) +
                    # " nphases=" + Integer.toString(nphases) + " units=multiplicities")
                    icond = 0
                    if wireA:
                        # out.write ("~ cond=" + Integer.toString(++icond) +
                        # " x=" + String.format("%6g", wireXa) + " h=" + String.format("%6g", wireYa))
                        pass
                    if wireB:
                        # out.write ("~ cond=" + Integer.toString(++icond) +
                        # " x=" + String.format("%6g", wireXb) + " h=" + String.format("%6g", wireYb))
                        pass
                    if wireC:
                        # out.write ("~ cond=" + Integer.toString(++icond) +
                        # " x=" + String.format("%6g", wireXc) + " h=" + String.format("%6g", wireYc))
                        pass
                    if wireS1:
                        # out.write ("~ cond=" + Integer.toString(++icond) +
                        # " x=" + String.format("%6g", wireXs1) + " h=" + String.format("%6g", wireYs1))
                        pass
                    if wireS2:
                        # out.write ("~ cond=" + Integer.toString(++icond) +
                        # " x=" + String.format("%6g", wireXs2) + " h=" + String.format("%6g", wireYs2))
                        pass
                    if wireN:
                        # out.write ("~ cond=" + Integer.toString(++icond) +
                        # " x=" + String.format("%6g", wireXn) + " h=" + String.format("%6g", wireYn))
                        pass

            NumLineCodes = 0
            out.write("\n")
            query = QueryFactory.create(self.qPrefix +
                                        "select ?status ?name where {?status r:type c:PerLengthPhaseImpedance. " +
                                       "?status c:IdentifiedObject.name ?name" +
                                       "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()



            while results.hasNext():
                soln = results.next()
                NumLineCodes += 1

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)
                ptCount = model.getProperty(self.ns_cim, "PerLengthPhaseImpedance.conductorCount")

                if res.hasProperty(ptCount):
                    out.write(self.get_impedance_matrix(model, name, ptCount, res, bWantSec) + "\n")

            query = QueryFactory.create(self.qPrefix + "select ?status ?name where {?status r:type c:PerLengthSequenceImpedance. " +
                                       "?status c:IdentifiedObject.name ?name" +
                                       "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            ptSeqR1 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.r")
            ptSeqR0 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.r0")
            ptSeqX1 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.x")
            ptSeqX0 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.x0")
            ptSeqB1 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.bch")
            ptSeqB0 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.b0ch")

            while results.hasNext():
                soln = results.next()
                NumLineCodes += 1

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)

                len = 1609.344  # want ohms/mile and nF/mile

                sqR1 = len * self.safe_double(res, ptSeqR1, 0)
                sqR0 = len * self.safe_double(res, ptSeqR0, 0)
                sqX1 = len * self.safe_double(res, ptSeqX1, 0)
                sqX0 = len * self.safe_double(res, ptSeqX0, 0)
                sqC1 = len * self.safe_double(res, ptSeqB1, 0) * 1.0e9 / freq / 2.0 / math.pi
                sqC0 = len * self.safe_double(res, ptSeqB0, 0) * 1.0e9 / freq / 2.0 / math.pi

                if sqR0 <= 0:
                    sqR0 = sqR1
                if sqX0 <= 0:
                    sqX0 = sqX1

                out.write(self.get_sequence_line_configurations(name, sqR1, sqX1, sqC1, sqR0, sqX0, sqC0) + "\n")

            out.write("\n")
            query = QueryFactory.create(self.qPrefix + "select ?status ?name ?len where {?status r:type c:ACLineSegment. " +
                                       "?status c:IdentifiedObject.name ?name;" +
                                       "	 c:Conductor.length ?len" +
                                       "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            ptPhsZ = model.getProperty(self.ns_cim, "ACLineSegment.PerLengthImpedance")
            ptLineLen = model.getProperty(self.ns_cim, "Conductor.length")
            ptDataSheet = model.getProperty(self.ns_cim, "PowerSystemResource.AssetDatasheet")
            ptAmps = model.getProperty(self.ns_cim, "WireInfo.ratedCurrent")
            ptPhsLine1 = model.getProperty(self.ns_cim, "ACLineSegmentPhase.ACLineSegment")
            ptPhsLine2 = model.getProperty(self.ns_cim, "ACLineSegmentPhase.phase")

            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""
                if fNameSeq > 0:
                    name = self.gld_id(id)
                else:
                    name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)
                len = soln.get("?len").to""
                phs = self.wire_phases(model, res, ptPhsLine1, ptPhsLine2)
                bus1 = self.get_bus_name(model, id, 1)
                bus2 = self.get_bus_name(model, id, 2)
                dLen = 3.28084 * self.safe_double(res, ptLineLen, 1.0)

                nd1 = self.map_nodes.get(bus1)
                nd1.nomvln = self.find_base_voltage(res, ptEquip, ptEqBaseV,
                                                    ptLevBaseV, ptBaseNomV) / math.sqrt(3.0)
                nd2 = self.map_nodes.get(bus2)
                nd2.nomvln = nd1.nomvln

                if "S" in phs:  # look for the primary phase at either end of this triplex line segment
                    if len(nd1.phases) > 0:
                        phs = nd1.phases + phs
                    if len(nd2.phases) > 0:
                        phs = nd2.phases + phs
                nd1.add_phases(phs)
                nd2.add_phases(phs)

                zPhase = self.safe_resource_lookup(model, ptName, res, ptPhsZ, "")
                zParms = self.get_ac_line_parameters(model, name, res, dLen, freq, phs, out)
                zSpace = self.get_line_spacing(model, res)
                linecode = ""

                if nd1.bSecondary:
                    if bWantSec:
                        out.write("object triplex_line {" + "\n")
                        out.write("  name \"tpx_" + name + "\";" + "\n")
                        out.write("  phases " + phs + ";" + "\n")
                        if nd1.has_load():
                            out.write("  from \"" + bus2 + "\";" + "\n")
                            out.write("  to \"" + bus1 + "\";" + "\n")
                        else:
                            out.write("  from \"" + bus1 + "\";" + "\n")
                            out.write("  to \"" + bus2 + "\";" + "\n")
                        out.write(functions"  length {dLen:.6f};" + "\n")
                        if len(zPhase) > 0:
                            out.write("  configuration \"tcon_" + zPhase + "\";" + "\n")
                        elif len(zParms) > 0:
                            out.write("  configuration \"" + zParms + "\";" + "\n")
                        out.write("}" + "\n")
                else:
                    out.write("object overhead_line {" + "\n")
                    out.write("  name \"line_" + name + "\";" + "\n")
                    out.write("  phases " + phs + ";" + "\n")
                    out.write("  from \"" + bus1 + "\";" + "\n")
                    out.write("  to \"" + bus2 + "\";" + "\n")
                    out.write(functions"  length {dLen:.6f};" + "\n")
                    if len(zPhase) > 0:
                        out.write("  configuration \"lcon_" + zPhase + "_" + phs + "\";" + "\n")
                    elif len(zParms) > 0:
                        out.write("  configuration \"" + zParms + "\";" + "\n")
                    out.write("}" + "\n")

            while results.hasNext():
                soln = results.next()
                NumLineCodes += 1

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)
                ptCount = model.getProperty(self.ns_cim, "PerLengthPhaseImpedance.conductorCount")

                if res.hasProperty(ptCount):
                    out.write(self.get_impedance_matrix(model, name, ptCount, res, bWantSec) + "\n")

            query = QueryFactory.create(self.qPrefix +
                                        "select ?status ?name where {?status r:type c:PerLengthSequenceImpedance. " +
                                       "?status c:IdentifiedObject.name ?name" +
                                       "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            ptSeqR1 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.r")
            ptSeqR0 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.r0")
            ptSeqX1 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.x")
            ptSeqX0 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.x0")
            ptSeqB1 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.bch")
            ptSeqB0 = model.getProperty(self.ns_cim, "PerLengthSequenceImpedance.b0ch")

            while results.hasNext():
                soln = results.next()
                NumLineCodes += 1

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)

                len = 1609.344  # want ohms/mile and nF/mile

                sqR1 = len * self.safe_double(res, ptSeqR1, 0)
                sqR0 = len * self.safe_double(res, ptSeqR0, 0)
                sqX1 = len * self.safe_double(res, ptSeqX1, 0)
                sqX0 = len * self.safe_double(res, ptSeqX0, 0)
                sqC1 = len * self.safe_double(res, ptSeqB1, 0) * 1.0e9 / freq / 2.0 / math.pi
                sqC0 = len * self.safe_double(res, ptSeqB0, 0) * 1.0e9 / freq / 2.0 / math.pi

                if sqR0 <= 0:
                    sqR0 = sqR1
                if sqX0 <= 0:
                    sqX0 = sqX1

                out.write(self.get_sequence_line_configurations(name, sqR1, sqX1, sqC1, sqR0, sqX0, sqC0) + "\n")

            out.write("\n")
            query = QueryFactory.create(self.qPrefix + "select ?status ?name ?len where {?status r:type c:ACLineSegment. " +
                                       "?status c:IdentifiedObject.name ?name;" +
                                       "	 c:Conductor.length ?len" +
                                       "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            ptPhsZ = model.getProperty(self.ns_cim, "ACLineSegment.PerLengthImpedance")
            ptLineLen = model.getProperty(self.ns_cim, "Conductor.length")
            ptDataSheet = model.getProperty(self.ns_cim, "PowerSystemResource.AssetDatasheet")
            ptAmps = model.getProperty(self.ns_cim, "WireInfo.ratedCurrent")
            ptPhsLine1 = model.getProperty(self.ns_cim, "ACLineSegmentPhase.ACLineSegment")
            ptPhsLine2 = model.getProperty(self.ns_cim, "ACLineSegmentPhase.phase")

            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""
                if fNameSeq > 0:
                    name = self.gld_id(id)
                else:
                    name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)
                len = soln.get("?len").to""
                phs = self.wire_phases(model, res, ptPhsLine1, ptPhsLine2)
                bus1 = self.get_bus_name(model, id, 1)
                bus2 = self.get_bus_name(model, id, 2)
                dLen = 3.28084 * self.safe_double(res, ptLineLen, 1.0)

                nd1 = self.map_nodes.get(bus1)
                nd1.nomvln = self.find_base_voltage(res, ptEquip, ptEqBaseV,
                                                    ptLevBaseV, ptBaseNomV) / math.sqrt(3.0)
                nd2 = self.map_nodes.get(bus2)
                nd2.nomvln = nd1.nomvln

                if "S" in phs:  # look for the primary phase at either end of this triplex line segment
                    if len(nd1.phases) > 0:
                        phs = nd1.phases + phs
                    if len(nd2.phases) > 0:
                        phs = nd2.phases + phs
                nd1.add_phases(phs)
                nd2.add_phases(phs)

                zPhase = self.safe_resource_lookup(model, ptName, res, ptPhsZ, "")
                zParms = self.get_ac_line_parameters(model, name, res, dLen, freq, phs, out)
                zSpace = self.get_line_spacing(model, res)
                linecode = ""

                if nd1.bSecondary:
                    if bWantSec:
                        out.write("object triplex_line {" + "\n")
                        out.write("  name \"tpx_" + name + "\";" + "\n")
                        out.write("  phases " + phs + ";" + "\n")
                        if nd1.has_load():
                            out.write("  from \"" + bus2 + "\";" + "\n")
                            out.write("  to \"" + bus1 + "\";" + "\n")
                        else:
                            out.write("  from \"" + bus1 + "\";" + "\n")
                            out.write("  to \"" + bus2 + "\";" + "\n")
                        out.write(functions"  length {dLen:.6f};" + "\n")
                        if len(zPhase) > 0:
                            out.write("  configuration \"tcon_" + zPhase + "\";" + "\n")
                        elif len(zParms) > 0:
                            out.write("  configuration \"" + zParms + "\";" + "\n")
                        out.write("}" + "\n")
                else:
                    out.write("object overhead_line {" + "\n")
                    out.write("  name \"line_" + name + "\";" + "\n")
                    out.write("  phases " + phs + ";" + "\n")
                    out.write("  from \"" + bus1 + "\";" + "\n")
                    out.write("  to \"" + bus2 + "\";" + "\n")
                    out.write(functions"  length {dLen:.6f};" + "\n")
                    if len(zPhase) > 0:
                        out.write("  configuration \"lcon_" + zPhase + "_" + phs + "\";" + "\n")
                    elif len(zParms) > 0:
                        out.write("  configuration \"" + zParms + "\";" + "\n")
                    out.write("}" + "\n")

            # LoadBreakSwitch ==> Line switch=y
            query = QueryFactory.create(q_prefix + "select ?status ?name ?open where {?status r:type c:LoadBreakSwitch. "
                                        "?status c:IdentifiedObject.name ?name;"
                                        "c:Switch.normalOpen ?open"
                                        "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            pt_phs_swt1 = model.getProperty(self.ns_cim, "SwitchPhase.Switch")
            pt_phs_swt2 = model.getProperty(self.ns_cim, "SwitchPhase.phaseSide1")  # TODO - phaseSide2?
            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)
                phs = self.wire_phases(model, res, pt_phs_swt1, pt_phs_swt2)
                open = soln.get("?open").to""

                bus1 = self.get_bus_name(model, id, 1)
                bus2 = self.get_bus_name(model, id, 2)

                nd1 = self.map_nodes.get(bus1)
                nd1.nomvln = self.find_base_voltage(res, self.pt_equip, self.pt_eq_base_v,
                                                    self.pt_lev_base_v, self.pt_base_nom_v) / math.sqrt(3.0)
                nd1.add_phases(phs)
                nd2 = self.map_nodes.get(bus2)
                nd2.nomvln = nd1.nomvln
                nd2.add_phases(phs)

                out.write("object switch {\n  name \"swt_" + name + "\";" + "\n")
                out.write("  phases " + phs + ";" + "\n")
                out.write("  from \"" + bus1 + "\";" + "\n")
                out.write("  to \"" + bus2 + "\";" + "\n")
                if open == "false":
                    out.write("  status CLOSED;" + "\n")
                else:
                    out.write("  status OPEN;" + "\n")

            # Fuse ==> Line switch=y
            query = QueryFactory.create(q_prefix + "select ?status ?name ?open where {?status r:type c:Fuse. "
                                        "?status c:IdentifiedObject.name ?name;"
                                        "c:Switch.normalOpen ?open"
                                        "}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            if results.hasNext():
                out.write("\n")
                out.write("// Fuses" + "\n")
            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)
                phs = self.wire_phases(model, res, pt_phs_swt1, pt_phs_swt2)
                open = soln.get("?open").to""

                bus1 = self.get_bus_name(model, id, 1)
                bus2 = self.get_bus_name(model, id, 2)

                nd1 = self.map_nodes.get(bus1)
                nd1.nomvln = self.find_base_voltage(res, self.pt_equip, self.pt_eq_base_v,
                                                    self.pt_lev_base_v, self.pt_base_nom_v) / math.sqrt(3.0)
                nd1.add_phases(phs)
                nd2 = self.map_nodes.get(bus2)
                nd2.nomvln = nd1.nomvln
                nd2.add_phases(phs)

            # Breaker ==> Line switch=y (NOTE: a source may be attached to the first instance)
            query = QueryFactory.create(q_prefix + "select ?status ?name where {?status r:type c:Breaker. "
                                        "?status c:IdentifiedObject.name ?name}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            if results.hasNext():
                out.write("\n")
                out.write("// Breakers" + "\n")
            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)
                phs = self.wire_phases(model, res, pt_phs_swt1, pt_phs_swt2)
                open = self.safe_property(res, self.pt_open, "false")

                bus1 = self.get_bus_name(model, id, 1)
                bus2 = self.get_bus_name(model, id, 2)

                nd1 = self.map_nodes.get(bus1)
                nd1.nomvln = self.find_base_voltage(res, self.pt_equip, self.pt_eq_base_v,
                                                    self.pt_lev_base_v, self.pt_base_nom_v) / math.sqrt(3.0)
                nd1.add_phases(phs)
                nd2 = self.map_nodes.get(bus2)
                nd2.nomvln = nd1.nomvln
                nd2.add_phases(phs)

            # Disconnector ==> Line switch=y
            query = QueryFactory.create(q_prefix + "select ?status ?name where {?status r:type c:Disconnector. "
                                        "?status c:IdentifiedObject.name ?name}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            if results.hasNext():
                out.write("\n")
                out.write("// Disconnectors" + "\n")
            while results.hasNext():
                soln = results.next()

                id = soln.get("?status").to""
                name = self.gld_name(soln.get("?name").to"", False)
                res = model.getResource(id)
                phs = self.wire_phases(model, res, pt_phs_swt1, pt_phs_swt2)
                open = self.safe_property(res, self.pt_open, "false")

                bus1 = self.get_bus_name(model, id, 1)
                bus2 = self.get_bus_name(model, id, 2)

                nd1 = self.map_nodes.get(bus1)
                nd1.nomvln = self.find_base_voltage(res, self.pt_equip, self.pt_eq_base_v,
                                                    self.pt_lev_base_v, self.pt_base_nom_v) / math.sqrt(3.0)
                nd1.add_phases(phs)
                nd2 = self.map_nodes.get(bus2)
                nd2.nomvln = nd1.nomvln
                nd2.add_phases(phs)

            # unsupported stuff - TODO - add Jumper and Disconnector
            out.write("\n")
            query = QueryFactory.create(q_prefix + "select ?status where {?status r:type c:Junction}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            while results.hasNext():
                soln = results.next()
                id = soln.get("?status").to""
                res = model.getResource(id)
                name = self.safe_res_name(res, self.pt_name)

            query = QueryFactory.create(q_prefix + "select ?status where {?status r:type c:BusbarSection}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            while results.hasNext():
                soln = results.next()
                id = soln.get("?status").to""
                res = model.getResource(id)
                name = self.safe_res_name(res, self.pt_name)

            query = QueryFactory.create(q_prefix + "select ?status where {?status r:type c:Bay}")
            qexec = QueryExecutionFactory.create(query, model)
            results = qexec.execSelect()
            while results.hasNext():
                soln = results.next()
                id = soln.get("?status").to""
                res = model.getResource(id)
                name = self.safe_res_name(res, self.pt_name)

            # write the swing node as a substation, and exclude from the others
            for key, nd in self.map_nodes.items():
                if nd.b_swing:
                    out.write("object substation {" + "\n")
                    out.write("  name \"" + nd.name + "\";" + "\n")
                    out.write("  bustype SWING;" + "\n")
                    out.write("  phases " + nd.get_phases() + ";" + "\n")
                    out.write("  nominal_voltage " + "{:.6f}".format(nd.nomvln) + ";" + "\n")
                    out.write("  base_power 12MVA;" + "\n")
                    out.write("  power_convergence_value 100VA;" + "\n")
                    out.write("  positive_sequence_voltage ${VSOURCE};" + "\n")
                    out.write("}" + "\n")
                    break  # there can be only one swing bus

            # write the nodes and loads; by now, all should have phases and nominal voltage
            for key, nd in self.map_nodes.items():
                if nd.has_load() and not nd.b_swing:
                    nd.rescale_load(load_scale)
                    if self.b_want_zip:
                        nd.apply_zip(self.z_coeff, self.i_coeff, self.p_coeff)
                    va = complex(nd.nomvln)
                    vb = va * self.neg120
                    vc = va * self.pos120
                    amps = None
                    vmagsq = nd.nomvln * nd.nomvln
                    if nd.b_secondary:
                        if self.b_want_sec:
                            out.write("object triplex_load {" + "\n")
                            out.write("  name \"" + nd.name + "\";" + "\n")
                            out.write("  phases " + nd.get_phases() + ";" + "\n")
                            out.write("  nominal_voltage " + "{:.6f}".format(nd.nomvln) + ";"+ "\n")
                            base1 = complex(nd.pa_z + nd.pa_i + nd.pa_p, nd.qa_z + nd.qa_i + nd.qa_p)
                            base2 = complex(nd.pb_z + nd.pb_i + nd.pb_p, nd.qb_z + nd.qb_i + nd.qb_p)
                            if self.b_want_sched:
                                out.write("  base_power_1 " + self.f_sched + ".value*" + "{:.6f}".format(base1.abs()) + ";"+ "\n")
                                out.write("  base_power_2 " + self.f_sched + ".value*" + "{:.6f}".format(base2.abs()) + ";"+ "\n")
                            else:
                                out.write("  base_power_1 " + "{:.6f}".format(base1.abs()) + ";"+ "\n")
                                out.write("  base_power_2 " + "{:.6f}".format(base2.abs()) + ";"+ "\n")
                            if nd.pa_p > 0.0:
                                base = complex(nd.pa_p, nd.qa_p)
                                out.write("  power_pf_1 " + "{:.6f}".format(nd.pa_p / base.abs()) + ";"+ "\n")
                                out.write("  power_fraction_1 " + "{:.6f}".format(nd.pa_p / base1.real) + ";"+ "\n")
                            if nd.pb_p > 0.0:
                                base = complex(nd.pb_p, nd.qb_p)
                                out.write("  power_pf_2 " + "{:.6f}".format(nd.pb_p / base.abs()) + ";"+ "\n")
                                out.write("  power_fraction_2 " + "{:.6f}".format(nd.pb_p / base2.real) + ";"+ "\n")
                            if nd.pa_i > 0.0:
                                base = complex(nd.pa_i, nd.qa_i)
                                out.write("  current_pf_1 " + "{:.6f}".format(nd.pa_i / base.abs()) + ";"+ "\n")
                                out.write("  current_fraction_1 " + "{:.6f}".format(nd.pa_i / base1.real) + ";"+ "\n")
                            if nd.pb_i > 0.0:
                                base = complex(nd.pb_i, nd.qb_i)
                                out.write("  current_pf_2 " + "{:.6f}".format(nd.pb_i / base.abs()) + ";")
                                out.write("  current_fraction_2 " + "{:.6f}".format(nd.pb_i / base2.real) + ";"+ "\n")
                            if nd.pa_z > 0.0:
                                base = complex(nd.pa_z, nd.qa_z)
                                out.write("  impedance_pf_1 " + "{:.6f}".format(nd.pa_z / base.abs()) + ";"+ "\n")
                                out.write("  impedance_fraction_1 " + "{:.6f}".format(nd.pa_z / base1.real) + ";"+ "\n")
                            if nd.pb_z > 0.0:
                                base = complex(nd.pb_z, nd.qb_z)
                                out.write("  impedance_pf_2 " + "{:.6f}".format(nd.pb_z / base.abs()) + ";"+ "\n")
                                out.write("  impedance_fraction_2 " + "{:.6f}".format(nd.pb_z / base2.real) + ";"+ "\n")
                            out.write("}" + "\n")
                    else:
                        if self.b_want_sched:  # TODO
                            pass
                        else:
                            out.write("object load {" + "\n")
                            out.write("  name \"" + nd.name + "\";" + "\n")
                            out.write("  phases " + nd.get_phases() + ";"+ "\n")
                            out.write("  nominal_voltage " + "{:.6f}".format(nd.nomvln) + ";"+ "\n")
                            if nd.pa_p > 0.0 or nd.qa_p != 0.0:
                                out.write("  constant_power_A " + self.c_format(complex(nd.pa_p, nd.qa_p)) + ";"+ "\n")
                            if nd.pb_p > 0.0 or nd.qb_p != 0.0:
                                out.write("  constant_power_B " + self.c_format(complex(nd.pb_p, nd.qb_p)) + ";"+ "\n")
                            if nd.pc_p > 0.0 or nd.qc_p != 0.0:
                                out.write("  constant_power_C " + self.c_format(complex(nd.pc_p, nd.qc_p)) + ";"+ "\n")
                            if nd.pa_z > 0.0 or nd.qa_z != 0.0:
                                s = complex(nd.pa_z, nd.qa_z)
                                z = vmagsq / s.conjugate()
                                out.write("  constant_impedance_A " + self.c_format(z) + ";"+ "\n")
                            if nd.pb_z > 0.0 or nd.qb_z != 0.0:
                                s = complex(nd.pb_z, nd.qb_z)
                                z = vmagsq / s.conjugate()
                                out.write("  constant_impedance_B " + self.c_format(z) + ";"+ "\n")
                            if nd.pc_z > 0.0 or nd.qc_z != 0.0:
                                s = complex(nd.pc_z, nd.qc_z)
                                z = vmagsq / s.conjugate()
                                out.write("  constant_impedance_C " + self.c_format(z) + ";"+ "\n")
                            if nd.pa_i > 0.0 or nd.qa_i != 0.0:
                                s = complex(nd.pa_i, nd.qa_i)
                                amps = s / va
                                out.write("  constant_current_A " + self.c_format(amps) + ";"+ "\n")
                            if nd.pb_i > 0.0 or nd.qb_i != 0.0:
                                s = complex(nd.pb_i, nd.qb_i)
                                amps = s/ va * self.neg120.conjugate()
                                out.write("	 constant_current_B " + self.c_format(amps) + ";"+ "\n")
                            if nd.pc_i > 0.0 or nd.qc_i != 0.0:
                                s = complex(nd.pc_i, nd.qc_i)
                                amps = s / va*self.pos120.conjugate()
                                out.write("	 constant_current_C " + self.c_format(amps) + ";"+ "\n")
                            out.write("}" + "\n")
                elif not nd.bSwing:
                    if nd.bSecondary:
                        if bWantSec:
                            out.write("object triplex_node {" + "\n")
                            out.write("	 name \"" + nd.name + "\";" + "\n")
                            out.write("	 phases " + nd.GetPhases() + ";"+ "\n")
                            out.write(functions"	 nominal_voltage {nd.nomvln:.6f};" + "\n")
                            out.write("}" + "\n")
                    else:
                        out.write("object node {" + "\n")
                        out.write("	 name \"" + nd.name + "\";" + "\n")
                        out.write("	 phases " + nd.GetPhases() + ";"+ "\n")
                        out.write(functions"	 nominal_voltage {nd.nomvln:.6f};" + "\n")
                        out.write("}" + "\n")
            out.write("\n")
            out.write (functions"// total load = {total_load_w:.6f}W" + "\n")

            out.write ("// buscoords " + fBus + "\n")
            out.close ()

        # for (HashMap.Entry<String,SpacingCount> pair : mapSpacings.entrySet()) {
        # 	System.out.printf ("%status ==> %d, %d\dimensions", pair.getKey(), pair.getValue().getNumConductors(), pair.getValue().getNumPhases());
        # }`