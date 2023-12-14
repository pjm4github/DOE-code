import json
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistXfmrCodeSCTest(DistComponent):
    sz_cim_class = "XfmrCodeSCTest"

    def __init__(self, results, mapper):
        super().__init__()
        self.pname = ""
        self.tname = ""
        self.fwdg = []
        self.twdg = []
        self.z = []
        self.ll = []
        self.size = 0

        if results.hasNext():
            soln = results.next()
            p = soln.get("?pname").toString()
            t = soln.get("?tname").toString()
            self.pname = self.safe_name(p)
            self.tname = self.safe_name(t)
            self.set_size(mapper.get(self.tname))
            for i in range(self.size):
                self.fwdg.append(int(soln.get("?enum").toString()))
                self.twdg.append(int(soln.get("?gnum").toString()))
                self.z.append(float(soln.get("?z").toString()))
                self.ll.append(float(soln.get("?ll").toString()))
                if i + 1 < self.size:
                    soln = results.next()

    def display_string(self):
        buf = [f"{self.pname}:{self.tname}"]
        for i in range(self.size):
            buf.append(
                f"\n  fwdg={self.fwdg[i]} twdg={self.twdg[i]} z={self.z[i]: .4f} LL={self.ll[i]:.4f}"
            )
        return "".join(buf)

    def get_key(self):
        return self.tname

    def set_size(self, val):
        self.size = val
        self.fwdg = [0] * self.size
        self.twdg = [0] * self.size
        self.z = [0.0] * self.size
        self.ll = [0.0] * self.size

    def get_json_entry(self):
        entry = {"name": self.pname, }
        return json.dumps(entry)
