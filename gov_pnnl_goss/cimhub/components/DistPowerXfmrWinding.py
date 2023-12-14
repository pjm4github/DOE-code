from typing import Dict, List
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent
from gov_pnnl_goss.cimhub.components.DistCoordinates import DistCoordinates


class DistPowerXfmrWinding(DistComponent):
    sz_cim_class = "PowerXfmrWinding"
    sz_csv_header = "Name,NumPhases,NumWindings,Bus1,kV1,Conn1,kVA1,Bus2,kV2,Conn2,kVA2," \
                    "Bus3,kV3,Conn3,kVA3,%x12,%x13,%x23,%loadloss,%imag,%noloadloss"

    def __init__(self, results: List[Dict], mapper: Dict[str, int]):
        super().__init__()
        self.size = 0  # Initialize arrays with size
        self.bus = []
        self.conn = []
        self.ename = []
        self.eid = []
        self.basev = []
        self.ratedU = []
        self.ratedS = []
        self.r = []
        self.wdg = []
        self.ang = []
        self.grounded = []
        self.rg = []
        self.xg = []
        self.normal_current_limit = 0.0
        self.emergency_current_limit = 0.0

        if results:
            soln = results[0]
            pname = soln.get("?pname")
            self.name = self.safe_name(pname)
            self.id = soln.get("?voltage_id")
            self.vgrp = soln.get("?vgrp")
            self.set_size(mapper.get(pname))
            self.glm_used = True
            for i in range(self.size):
                self.eid[i] = soln.get("?eid")
                self.ename[i] = self.safe_name(soln.get("?ename"))
                self.bus[i] = self.safe_name(soln.get("?bus"))
                self.basev[i] = float(soln.get("?basev"))
                self.conn[i] = soln.get("?conn")
                self.ratedU[i] = float(soln.get("?ratedU"))
                self.ratedS[i] = float(soln.get("?ratedS"))
                self.r[i] = float(soln.get("?r"))
                self.wdg[i] = int(soln.get("?enum"))
                self.ang[i] = int(soln.get("?ang"))
                self.grounded[i] = bool(soln.get("?grounded"))
                self.rg[i] = self.optional_double(soln, "?rground", 0.0)
                self.xg[i] = self.optional_double(soln, "?xground", 0.0)
                if (i + 1) < self.size:
                    soln = results[i + 1]

    def set_size(self, val):
        self.size = val
        self.bus = [None] * self.size
        self.conn = [None] * self.size
        self.ename = [None] * self.size
        self.eid = [None] * self.size
        self.basev = [0.0] * self.size
        self.ratedU = [0.0] * self.size
        self.ratedS = [0.0] * self.size
        self.r = [0.0] * self.size
        self.wdg = [0] * self.size
        self.ang = [0] * self.size
        self.grounded = [False] * self.size
        self.rg = [0.0] * self.size
        self.xg = [0.0] * self.size

    def display_string(self):
        buf = [f"{self.name} {self.vgrp}"]
        for i in range(self.size):
            buf.append(f"bus={self.bus[i]} basev={self.basev[i]} conn={self.conn[i]} ang={self.ang[i]}")
            buf.append(f"U={self.ratedU[i]} S={self.ratedS[i]} r={self.r[i]}")
            buf.append(f"grounded={self.grounded[i]} rg={self.rg[i]} xg={self.xg[i]}")
        return "\n".join(buf)

    def get_json_entry(self):
        return f'{{"name":"{self.name}","mRID":"{self.id}"}}'

    def get_json_symbols(self, mapper: Dict[str, DistCoordinates]):
        pt1 = mapper.get(f"PowerTransformer:{self.name}:1")
        pt2 = mapper.get(f"PowerTransformer:{self.name}:2")
        bus1 = self.bus[0]
        bus2 = self.bus[1]

        buf = [f'{{"name":"{self.name}","from":"{bus1}","to":"{bus2}","phases":"ABC","configuration":"{self.vgrp}",',
               f'"x1":{pt1.x},"y1":{pt1.y},"x2":{pt2.x},"y2":{pt2.y}}}']
        return ''.join(buf)

    def get_glm(self, mesh, core):
        buf = [f'object transformer_configuration {{', f'  name "xcon_{self.name}";']
        s_connect = self.get_gld_transformer_connection(self.conn, self.size)
        if s_connect == "Y_D":
            buf.append(f'  connect_type WYE_WYE; // should be Y_D')
        else:
            buf.append(f'  connect_type {s_connect};')
        buf.append(f'  primary_voltage {self.ratedU[0]};')
        buf.append(f'  secondary_voltage {self.ratedU[1]};')
        buf.append(f'  power_rating {self.ratedS[0] * 0.001};')
        idx = core.wdg - 1
        Zbase = self.ratedU[idx] * self.ratedU[idx] / self.ratedS[idx]
        if core.b > 0.0:
            buf.append(f'  shunt_reactance {1.0 / Zbase / core.b};')
        if core.g > 0.0:
            buf.append(f'  shunt_resistance {1.0 / Zbase / core.g};')
        buf.append(f'}}')
        buf.append(f'object transformer {{')
        buf.append(f'  name "xf_{self.name}";')
        buf.append(f'  from "{self.bus[0]}";')
        buf.append(f'  to "{self.bus[1]}";')
        buf.append(f'  phases ABC;')
        buf.append(f'  configuration "xcon_{self.name}";')
        self.append_glm_ratings(buf, "ABC", self.normal_current_limit, self.emergency_current_limit)
        buf.append(f'  // vector group {self.vgrp};')
        buf.append(f'}}')
        return '\n'.join(buf)

    def get_dss(self, mesh, core):
        b_delta = False
        i = 0
        fwdg = 0
        twdg = 0
        zbase = 0.0
        xpct = 0.0
        x12 = 0.0
        x13 = 0.0
        x23 = 0.0
        loadloss = 0.0
        buf = [f'new Transformer.{self.name} phases=3 windings={self.size}']

        for i in range(mesh.size):
            fwdg = mesh.fwdg[i]
            twdg = mesh.twdg[i]
            zbase = self.ratedU[fwdg - 1] * self.ratedU[fwdg - 1] / self.ratedS[fwdg - 1]
            xpct = 100.0 * mesh.x[i] / zbase
            if (fwdg == 1 and twdg == 2) or (fwdg == 2 and twdg == 1):
                x12 = xpct
            elif (fwdg == 1 and twdg == 3) or (fwdg == 3 and twdg == 1):
                x13 = xpct
            elif (fwdg == 2 and twdg == 3) or (fwdg == 3 and twdg == 2):
                x23 = xpct

        for i in range(self.size):
            if "D" in self.conn[i]:
                b_delta = True
            else:
                b_delta = False
            zbase = self.ratedU[i] * self.ratedU[i] / self.ratedS[i]
            loadloss += 100.0 * self.r[i] / zbase
            buf.append(f',wdg={i + 1},bus={self.bus[i]},conn={self.dss_conn(b_delta)},'
                       f'kv={0.001 * self.ratedU[i]},kva={0.001 * self.ratedS[i]},%r={100.0 * self.r[i] / zbase}')
        if i < 3:
            buf.append(',,,,')
        buf.append(f',{x12},{x13},{x23}')
        i = core.wdg
        zbase = self.ratedU[i] * self.ratedU[i] / self.ratedS[i]
        buf.append(f',{loadloss},{core.b * zbase * 100.0},{core.b * zbase * 100.0}\n')
        return ''.join(buf)

    def csv_header(self):
        return self.sz_csv_header

    def get_csv(self, mesh, core):
        i = 0
        # fwdg = 0
        # twdg = 0
        # zbase = 0.0
        # xpct = 0.0
        x12 = 0.0
        x13 = 0.0
        x23 = 0.0
        loadloss = 0.0
        buf = [f'{self.name},3,{self.size}']

        for i in range(mesh.size):
            fwdg = mesh.fwdg[i]
            twdg = mesh.twdg[i]
            zbase = self.ratedU[fwdg - 1] * self.ratedU[fwdg - 1] / self.ratedS[fwdg - 1]
            xpct = 100.0 * mesh.x[i] / zbase
            if (fwdg == 1 and twdg == 2) or (fwdg == 2 and twdg == 1):
                x12 = xpct
            elif (fwdg == 1 and twdg == 3) or (fwdg == 3 and twdg == 1):
                x13 = xpct
            elif (fwdg == 2 and twdg == 3) or (fwdg == 3 and twdg == 2):
                x23 = xpct

        for i in range(self.size):
            if "D" in self.conn[i]:
                b_delta = True
            else:
                b_delta = False
            zbase = self.ratedU[i] * self.ratedU[i] / self.ratedS[i]
            loadloss += 100.0 * self.r[i] / zbase
            buf.append(f',{self.bus[i]},{0.001 * self.ratedU[i]},{self.dss_conn(b_delta)},{0.001 * self.ratedS[i]}')
        if i < 3:
            buf.append(',,,')
        buf.append(f',{x12},{x13},{x23}')
        i = core.wdg
        zbase = self.ratedU[i] * self.ratedU[i] / self.ratedS[i]
        buf.append(f',{loadloss},{core.b * zbase * 100.0},{core.b * zbase * 100.0}\n')
        return ''.join(buf)

    def get_key(self):
        return self.name
