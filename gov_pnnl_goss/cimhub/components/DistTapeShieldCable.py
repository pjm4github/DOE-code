import json

from gov_pnnl_goss.cimhub.components.DistCable import DistCable


class DistTapeShieldCable(DistCable):
    sz_cim_class = "TapeShieldCable"
    sz_csv_header = DistCable.sz_csv_header + ",Tlap,Tthick"

    def __init__(self, results):
        super().__init__()
        self.tlap = 0.0
        self.tthick = 0.0

        if results:
            if results.hasNext():
                soln = results.next()
                self.name = self.safe_name(soln["name"].to"")
                self.id = soln["voltage_id"].to""
                self.rad = float(soln["rad"].to"")
                self.gmr = float(soln["gmr"].to"")
                self.rdc = self.optional_double(soln, "?rdc", 0.0)
                self.r25 = self.optional_double(soln, "?r25", 0.0)
                self.r50 = self.optional_double(soln, "?r50", 0.0)
                self.r75 = self.optional_double(soln, "?r75", 0.0)
                self.corerad = self.optional_double(soln, "?corerad", 0.0)
                self.amps = self.optional_double(soln, "?amps", 0.0)
                self.insthick = self.optional_double(soln, "?insthick", 0.0)
                self.ins = self.optional_boolean(soln, "?ins", False)
                self.insmat = self.optional_string(soln, "?insmat", "N/A")
                self.dcore = self.optional_double(soln, "?diacore", 0.0)
                self.djacket = self.optional_double(soln, "?diajacket", 0.0)
                self.dins = self.optional_double(soln, "?diains", 0.0)
                self.dscreen = self.optional_double(soln, "?diascreen", 0.0)
                self.sheathNeutral = self.optional_boolean(soln, "?sheathneutral", False)
                self.tlap = self.optional_double(soln, "?tapelap", 0.0)
                self.tthick = self.optional_double(soln, "?tapethickness", 0.0)

    def get_json_entry(self):
        return json.dumps({"name": self.name, "mRID": self.id})

    def display_string(self):
        buf = []
        self.append_cable_display(buf)
        buf.append(f" tlap={self.tlap:.2f} tthick={self.tthick:.6f}")
        return "".join(buf)

    def get_dss(self):
        buf = []
        buf.append(f"new TSData.")
        self.append_dss_cable_attributes(buf)
        buf.append(f"\n~ DiaShield={self.dscreen + 2.0 * self.tthick:.6f} "
                   f"tapeLayer={self.tthick:.6f} tapeLap={self.tlap: .3f}")
        buf.append("\n")
        return "".join(buf)

    def get_glm(self):
        buf = []
        # equation 4.89 from Kersting 3rd edition gives rshield = 18.826/ds/T [Ohms/mile]
        # where ds is shield diameter [in] and T is tape thickness [mil]
        rshield = 1.214583e-5 / self.dscreen / self.tthick  # for dscreen and tthick in [multiplicities]

        buf.append(f"object underground_line_conductor {{")
        buf.append(f"  name \"tscab_{self.name}\";")
        buf.append(f"  shield_gmr {0.5 * self.dscreen * self.g_ft_per_m:.6f};")
        buf.append(f"  shield_diameter {self.dscreen * self.g_ft_per_m * 12.0:.6f};")
        buf.append(f"  shield_resistance {rshield:.6f};")
        buf.append(f"  shield_thickness {self.tthick * self.g_ft_per_m * 12.0:.6f};")
        self.append_glm_cable_attributes(buf)
        buf.append("}\n")
        return "".join(buf)

    def sz_csv_header(self):
        return self.sz_csv_header

    def get_csv(self):
        buf = []
        self.append_csv_cable_attributes(buf)
        buf.append(f",{self.tlap:.3f},{self.tthick:.6f}\n")
        return "".join(buf)

    def get_key(self):
        return self.name
