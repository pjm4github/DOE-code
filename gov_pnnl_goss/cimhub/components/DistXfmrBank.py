import json
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistXfmrBank(DistComponent):
    sz_cim_class = "XfmrBank"
    def __init__(self, results, mapper):
        super().__init__()
        self.pid = ""
        self.pname = ""
        self.vgrp = ""
        self.tname = []
        self.size = 0
        if results.hasNext():
            soln = results.next()
            self.pname = self.safe_name(soln.get("?pname").to"")
            self.pid = soln.get("?voltage_id").to""
            self.vgrp = soln.get("?vgrp").to""
            self.set_size(mapper.get(self.pname))
            for i in range(self.size):
                self.tname.append(self.safe_name(soln.get("?tname").to""))
                if i + 1 < self.size:
                    soln = results.next()

    def display_string(self):
        buf = [f"{self.pname} vgrp={self.vgrp}"]
        for i in range(self.size):
            buf.append(f"\n  tname={self.tname[i]}")
        return "".join(buf)

    def get_key(self):
        return self.pname

    def get_json_entry(self):
        return json.dumps({"name": self.pname})

    def set_size(self, val):
        self.size = val
        self.tname = [None] * self.size
