from typing import Dict, List
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistPowerXfmrMesh(DistComponent):
    sz_cim_class = "PowerXfmrMesh"

    def __init__(self, results: List[Dict], mapper: Dict[str, int]):
        super().__init__()
        self.fwdg = []
        self.twdg = []
        self.size = 0
        self.r = []
        self.x = []

        if results:
            soln = results[0]
            pname = soln.get("?pname")
            self.name = self.safe_name(pname)
            self.set_size(mapper.get(pname))
            for i in range(self.size):
                self.fwdg[i] = int(soln.get("?fnum"))
                self.twdg[i] = int(soln.get("?tnum"))
                self.r[i] = float(soln.get("?r"))
                self.x[i] = float(soln.get("?x"))
                if (i + 1) < self.size:
                    soln = results[i + 1]

    def display_string(self):
        buf = [f"{self.name} {self.size}"]
        for i in range(self.size):
            buf.append(f"fwdg={self.fwdg[i]} twdg={self.twdg[i]} r={self.r[i]} x={self.x[i]}")
        return "\n".join(buf)

    def get_key(self):
        return self.name

    def get_json_entry(self):
        return f'{{"name":"{self.name}"}}'

    def set_size(self, val):
        self.size = val
        self.fwdg = [0] * self.size
        self.twdg = [0] * self.size
        self.r = [0.0] * self.size
        self.x = [0.0] * self.size
