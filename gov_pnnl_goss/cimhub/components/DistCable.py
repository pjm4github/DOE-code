from gov_pnnl_goss.cimhub.components.DistWire import DistWire


class DistCable(DistWire):
    sz_cim_class = "Cable"
    sz_csv_header = f"{DistWire.sz_csv_header},InsMat,EpsRel,InsThick,DIACore,DIAJacket,DIAIns,DIAScreen,SheathNeutral"

    def __init__(self):
        super().__init__()
        self.dcore = 0.0
        self.djacket = 0.0
        self.dins = 0.0
        self.dscreen = 0.0
        self.sheath_neutral = False

    def append_cable_display(self, buf):
        buf = self.append_wire_display(buf)
        buf.append(f" dcore={self.dcore:.6f} djacket={self.djacket:.6f} dins={self.dins:.6f}")
        buf.append(f" dscreen={self.dscreen:.6f} sheathNeutral={str(self.sheath_neutral)}")
        return "\n".join(buf)

    def append_dss_cable_attributes(self, buf):
        buf = self.append_dss_wire_attributes(buf)
        d_eps = 2.3  # TODO - should be a setting
        buf.append(f"\n~ EpsR={d_eps:.2f} Ins={self.insthick:.6f}")
        buf.append(f" DiaIns={self.dins:.6f} DiaCable={self.djacket:.6f}")
        return "\n".join(buf)

    def append_csv_cable_attributes(self, buf):
        buf = self.append_csv_wire_attributes(buf)
        d_eps = 2.3  # TODO - should be a setting
        buf.append(f",{self.insmat},{d_eps:.2f},{self.insthick:.6f}")
        buf.append(f",{self.dcore:.6f},{self.djacket:.6f},{self.dins:.6f},{self.dscreen:.6f}")
        buf.append(f",{str(self.sheath_neutral)}")
        return "\n".join(buf)

    def append_glm_cable_attributes(self, buf):
        buf = self.append_glm_wire_attributes(buf)
        d_eps = 2.3  # TODO - should be a setting
        buf.append(f"  conductor_gmr {self.gmr * self.g_ft_per_m:.6f};")
        buf.append(f"  conductor_diameter {2.0 * self.rad * self.g_ft_per_m * 12.0:.6f};")
        buf.append(f"  conductor_resistance {self.r50 * self.g_m_per_mile:.6f};")
        buf.append(f"  outer_diameter {self.djacket * self.g_ft_per_m * 12.0:.6f};")
        buf.append(f"  insulation_relative_permitivitty {d_eps:.2f};")
        return "\n".join(buf)

    def display_string(self) -> str:
        return "Not implemented"

    def get_key(self) -> str:
        return "Not implemented"

    def get_json_entry(self) -> str:
        return "{}"
