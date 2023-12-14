from gov_pnnl_goss.cimhub.components.DistCable import DistCable


class DistConcentricNeutralCable(DistCable):
    sz_cim_class = "ConcentricNeutralCable"
    def __init__(self, results):
        super().__init__()

        if results:
            soln = results[0]  # Assuming results is a list of query results, adjust as needed
            self.name = self.safe_name(soln.get("?name").toString())
            self.id = soln.get("?voltage_id").toString()
            self.rad = float(soln.get("?rad").toString())
            self.gmr = float(soln.get("?gmr").toString())
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
            self.sheath_neutral = self.optional_boolean(soln, "?sheathneutral", False)
            self.dneut = self.optional_double(soln, "?dianeut", 0.0)
            self.strand_cnt = self.optional_int(soln, "?strand_cnt", 0)
            self.strand_gmr = self.optional_double(soln, "?strand_gmr", 0.0)
            self.strand_rad = self.optional_double(soln, "?strand_rad", 0.0)
            self.strand_rdc = self.optional_double(soln, "?strand_rdc", 0.0)

    def get_json_entry(self) -> str:
        return f'{{"name":"{self.name}", "mRID":"{self.id}"}}'

    def display_string(self) -> str:
        buf = super().display_string()
        buf += f" dneut={self.dneut:.6f} strand_cnt={self.strand_cnt} "
        buf += f"strand_gmr={self.strand_gmr:.6f} strand_rad={self.strand_rad:.6f} strand_rdc={self.strand_rdc:.6f}"
        return buf

    def get_dss(self) -> str:
        buf = super().get_dss()
        buf += f"\n~ k={self.strand_cnt} GmrStrand={self.strand_gmr:.6f} DiaStrand={2.0 * self.strand_rad:.6f} Rstrand={self.strand_rdc:.6f}\n"
        return buf

    def get_glm(self) -> str:
        buf = ""  # DistCable.get_glm()
        buf += f"object underground_line_conductor {{\n"
        buf += f"  name \"cncab_{self.name}\";\n"
        buf += f"  neutral_gmr {self.strand_gmr * self.g_ft_per_m:.6f};\n"
        buf += f"  neutral_diameter {2.0 * self.strand_rad * self.g_ft_per_m * 12.0:.6f};\n"
        buf += f"  neutral_resistance {self.strand_rdc * self.g_m_per_mile:.6f};\n"
        buf += f"  neutral_strands {self.strand_cnt};\n"
        buf += super().append_glm_cable_attributes(buf)
        buf += f"}}\n"
        return buf

    @property
    def sz_csv_header(self) -> str:
        return f"{super().sz_csv_header},DIAn,Ns,GMRs,DIAs,RESs"

    def get_csv(self) -> str:
        buf = super().get_csv()
        buf += f",{self.dneut:.6f},{self.strand_cnt},{self.strand_gmr:.6f},{2.0 * self.strand_rad:.6f},{self.strand_rdc:.6f}\n"
        return buf

    def get_key(self) -> str:
        return super().get_key()

    def optional_double(self, results, parameter, default_value):
        if results and results[parameter]:
            return float(results[parameter])
        return default_value

    def optional_int(self, results, parameter, default_value):
        if results and results[parameter]:
            return int(results[parameter])
        return default_value

