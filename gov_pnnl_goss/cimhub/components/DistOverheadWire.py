from gov_pnnl_goss.cimhub.components.DistWire import DistWire


class DistOverheadWire(DistWire):
    sz_cim_class = "OverheadWire"

    def __init__(self, results):
        super().__init__()
        if results.has_next():
            soln = results.next()
            self.name = self.safe_name(soln.get("?name").to_string())
            self.id = soln.get("?voltage_id").to_string()
            self.rad = float(soln.get("?rad").to_string())
            self.gmr = float(soln.get("?gmr").to_string())
            self.rdc = self.optional_double(soln, "?rdc", 0.0)
            self.r25 = self.optional_double(soln, "?r25", 0.0)
            self.r50 = self.optional_double(soln, "?r50", 0.0)
            self.r75 = self.optional_double(soln, "?r75", 0.0)
            self.corerad = self.optional_double(soln, "?corerad", 0.0)
            self.amps = self.optional_double(soln, "?amps", 0.0)
            self.insthick = self.optional_double(soln, "?insthick", 0.0)
            self.ins = self.optional_boolean(soln, "?ins", False)
            self.insmat = self.optional_string(soln, "?insmat", "N/A")
            self.can_bury = False

    def display_string(self):
        buf = ""
        buf += self.append_wire_display(buf)
        return buf

    def get_dss(self):
        buf = "new WireData."
        buf += self.append_dss_wire_attributes(buf)
        buf += "\n"
        return buf

    def get_glm(self):
        dia_out = 2.0 * self.rad * self.g_ft_per_m * 12.0
        res_out = self.r50 * self.g_m_per_mile
        gmr_out = self.gmr * self.g_ft_per_m

        buf = "object overhead_line_conductor {\n"
        buf += f"  name \"wire_{self.name}\";\n"
        buf += f"  geometric_mean_radius {gmr_out:.6f};\n"
        buf += f"  diameter {dia_out:.6f};\n"
        buf += f"  resistance {res_out:.6f};\n"
        buf += self.append_glm_wire_attributes(buf)
        buf += "}\n"

        if self.can_bury:
            buf += "object underground_line_conductor {\n"
            buf += f"  name \"ugwire_{self.name}\";\n"
            buf += f"  conductor_gmr {gmr_out:.6f};\n"
            buf += f"  conductor_diameter {dia_out:.6f};\n"
            buf += f"  outer_diameter {1.2 * dia_out:.6f};\n"
            buf += f"  conductor_resistance {res_out:.6f};\n"
            buf += self.append_glm_wire_attributes(buf)
            buf += "}\n"
        return buf

    def get_csv_header(self):
        return self.sz_csv_header

    def get_csv(self):
        buf = ""
        buf += self.append_csv_wire_attributes(buf)
        buf += "\n"
        return buf

    def get_key(self):
        return self.name

    def get_json_entry(self):
        buf = ""
        buf += f"{{\"name\":\"{self.name}\""
        buf += f",\"mRID\":\"{self.id}\""
        buf += "}"
        return buf
