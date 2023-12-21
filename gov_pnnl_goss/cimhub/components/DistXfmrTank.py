from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent

import json


class DistXfmrTank(DistComponent):
    sz_cim_class = "XfmrTank"
    sz_csv_header = "Name,Wdg1Bus,Phase,Wdg2Bus,Phase,Wdg3Bus,Phase,XfmrCode"
    
    def __init__(self, results, mapper):
        super().__init__()
        self.id = ""
        self.pname = ""
        self.vgrp = ""
        self.tname = ""
        self.tankinfo = ""
        self.infoid = ""
        self.bus = []
        self.phs = []
        self.ename = []
        self.eid = []
        self.basev = []
        self.rg = []
        self.xg = []
        self.wdg = []
        self.grounded = []

        self.normalCurrentLimit = 0.0
        self.emergencyCurrentLimit = 0.0
        self.glmUsed = False
        self.size = 0

        # Parse the ResultSet to initialize object attributes
        if results.hasNext():
            soln = results.next()
            self.pname = self.safe_name(soln.get("?pname").to"")
            self.id = soln.get("?voltage_id").to""
            self.infoid = soln.get("?infoid").to""
            self.vgrp = soln.get("?vgrp").to""
            self.tname = self.safe_name(soln.get("?tname").to"")
            self.tankinfo = self.safe_name(soln.get("?xfmrcode").to"")
            self.set_size(mapper.get(self.tname))
            self.glmUsed = True

            for i in range(self.size):
                self.eid.append(soln.get("?eid").to"")
                self.ename.append(self.safe_name(soln.get("?ename").to""))
                self.bus.append(self.safe_name(soln.get("?bus").to""))
                self.basev.append(float(soln.get("?basev").to""))
                self.phs.append(soln.get("?phs").to"")
                self.rg.append(self.optional_double(soln, "?rground", 0.0))
                self.xg.append(self.optional_double(soln, "?xground", 0.0))
                self.wdg.append(int(soln.get("?enum").to""))
                self.grounded.append(bool(soln.get("?grounded").to""))

                if i + 1 < self.size:
                    soln = results.next()

    def display_string(self):
        buf = [f"pname={self.pname} vgrp={self.vgrp} tname={self.tname} tankinfo={self.tankinfo}"]
        for i in range(self.size):
            buf.append(f"\n  {self.wdg[i]} bus={self.bus[i]} basev={self.basev[i]:.4f} phs={self.phs[i]}")
            buf.append(f" grounded={self.grounded[i]} rg={self.rg[i]:.4f} xg={self.xg[i]:.4f}")
        return "\n".join(buf)

    def get_json_entry(self):
        entry = {"name": self.pname, "mRID": self.id}
        return json.dumps(entry)

    def get_json_symbols(self, mapper):
        pt1 = mapper.get("PowerTransformer:" + self.pname + ":1")
        pt2 = mapper.get("PowerTransformer:" + self.pname + ":2")
        bus1 = self.bus[0]
        bus2 = self.bus[1]
        lbl_phs = "".join(self.phs)

        buf = {
            "name": self.pname,
            "from": bus1,
            "to": bus2,
            "phases": self.phs[0],
            "configuration": f"{self.tankinfo}:{self.vgrp}",
            "x1": pt1.x,
            "y1": pt1.y,
            "x2": pt2.x,
            "y2": pt2.y,
        }
        return json.dumps(buf)

    def get_glm(self):
        buf = ["object transformer {",
               f'  name "xf_{self.pname}";',
               f'  from "{self.bus[0]}";',
               f'  to "{self.bus[1]}";']

        if "status" in self.phs[1]:
            buf.append(f"  phases {self.phs[0]}S;")
        else:
            buf.append(f"  phases {self.phs[0]};")

        buf.append(f'  configuration "xcon_{self.tankinfo}";')
        buf.append(f"  // vector group {self.vgrp};")
        buf.append("}")
        return "\n".join(buf)

    def get_dss(self):
        buf = [f"new Transformer.{self.tname} bank={self.pname} xfmrcode={self.tankinfo}"]
        # Winding ratings
        self.append_dss_ratings(buf, self.normalCurrentLimit, self.emergencyCurrentLimit)
        for i in range(self.size):
            buf.append(f"~ wdg={i + 1} bus={self.dss_xfmr_bus_phases(self.bus[i], self.phs[i])}")
        return "\n".join(buf)

    def get_csv(self):
        buf = [self.tname]
        for i in range(self.size):
            buf.append(f",{self.bus[i]},{self.csv_phase_string(self.phs[i])}")
        if self.size < 3:
            buf.append(",,")
        buf.append(f",{self.tankinfo}")
        return "".join(buf)

    def get_key(self):
        return self.tname

    def set_size(self, val):
        self.size = val
        self.bus = [None] * val
        self.phs = [None] * val
        self.ename = [None] * val
        self.eid = [None] * val
        self.wdg = [0] * val
        self.grounded = [False] * val
        self.basev = [0.0] * val
        self.rg = [0.0] * val
        self.xg = [0.0] * val
