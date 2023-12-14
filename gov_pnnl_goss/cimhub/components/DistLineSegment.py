from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent



class DistLineSegment(DistComponent):
    sz_cim_class = "LineSegment"
    def __init__(self):
        super().__init__()
        self.id = ""
        self.name = ""
        self.bus1 = ""
        self.bus2 = ""
        self.phases = ""
        self.len = 0.0
        self.basev = 0.0
        self.normal_current_limit = 0.0
        self.emergency_current_limit = 0.0
        self.b_triplex = False
        self.b_cable = False
        self.glm_phases = ""

    def label_string(self):
        return ""

    def append_shared_glm_attributes(self, buf, config_root, b_spacing, b_force_n):
        if 'status' in self.phases:
            self.b_triplex = True
            buf.append("object triplex_line {\n")
            buf.append("  name \"tpx_" + self.name + "\";\n")
        else:
            self.b_triplex = False
            if self.b_cable:
                buf.append("object underground_line {\n")
            else:
                buf.append("object overhead_line {\n")
            buf.append("  name \"line_" + self.name + "\";\n")

        buf.append("  from \"" + self.bus1 + "\";\n")
        buf.append("  to \"" + self.bus2 + "\";\n")
        phs = []
        if 'A' in self.phases:
            phs.append("A")
        if 'B' in self.phases:
            phs.append("B")
        if 'C' in self.phases:
            phs.append("C")
        if self.b_triplex:
            phs.append("S")
        if 'N' in self.phases or b_force_n:
            phs.append("N")
        self.glm_phases = "".join(phs)
        buf.append("  phases " + self.glm_phases + ";\n")
        buf.append("  length " + "{:.4f}".format(self.len * self.g_ft_per_m) + ";\n")
        self.append_glm_ratings(buf, self.glm_phases, self.normal_current_limit, self.emergency_current_limit)
        if b_spacing:
            buf.append("  configuration \"" + config_root + "\";\n")
        elif self.b_triplex:
            buf.append("  configuration \"tcon_" + config_root + "_12\";\n")
        else:
            buf.append("  configuration \"lcon_" + config_root + "_" + self.glm_phases + "\";\n")
        buf.append("}\n")

    def get_json_symbols(self, mapper):
        pt1 = mapper.get("ACLineSegment:" + self.name + ":1")
        pt2 = mapper.get("ACLineSegment:" + self.name + ":2")
        lbl_phs = []
        if 'A' in self.phases:
            lbl_phs.append("A")
        if 'B' in self.phases:
            lbl_phs.append("B")
        if 'C' in self.phases:
            lbl_phs.append("C")
        if 'status' in self.phases:
            lbl_phs.append("S")
        if not lbl_phs:
            lbl_phs.append("ABC")

        buf = []
        buf.append("{\"name\":\"" + self.name + "\"")
        buf.append(",\"from\":\"" + self.bus1 + "\"")
        buf.append(",\"to\":\"" + self.bus2 + "\"")
        buf.append(",\"phases\":\"" + "".join(lbl_phs) + "\"")
        buf.append(",\"length\":" + "{:.2f}".format(self.len * self.g_ft_per_m))
        buf.append(",\"configuration\":\"" + self.label_string() + "\"")
        buf.append(",\"x1\":" + str(pt1.x))
        buf.append(",\"y1\":" + str(pt1.y))
        buf.append(",\"x2\":" + str(pt2.x))
        buf.append(",\"y2\":" + str(pt2.y))
        buf.append("}")
        return "".join(buf)

    def display_string(self):
        return ""

    def get_json_entry(self):
        buf = []
        buf.append(f"{{\"name\":\"{self.name}\"")
        buf.append(f",\"mRID\":\"{self.id}\"")
        buf.append("}")
        return "".join(buf)

    def get_key(self):
        return self.name
