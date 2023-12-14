import json
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent



class DistXfmrCodeOCTest(DistComponent):
    sz_cim_class = "XfmrCodeOCTest"

    def __init__(self, results):
        super().__init__()
        self.pname = ""
        self.tname = ""
        self.nll = 0.0
        self.iexc = 0.0

        if results.hasNext():
            soln = results.next()
            self.pname = self.safe_name(soln.get("?pname").toString())
            self.tname = self.safe_name(soln.get("?tname").toString())
            self.nll = float(soln.get("?nll").toString())
            self.iexc = float(soln.get("?iexc").toString())

    def display_string(self):
        return f"{self.pname}:{self.tname} NLL={self.nll:.4f} iexc={self.iexc:.4f}"

    def get_key(self):
        return self.tname

    def get_json_entry(self):
        return json.dumps({"name": self.pname})
