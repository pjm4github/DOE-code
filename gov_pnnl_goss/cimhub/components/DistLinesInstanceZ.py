from gov_pnnl_goss.cimhub.components.DistLineSegment import DistLineSegment


class DistLinesInstanceZ(DistLineSegment):
    sz_cim_class = "LinesInstanceZ"

    def __init__(self, results, mapper):
        super().__init__()
        if results.hasNext():
            soln = results.next()
            self.name = self.safe_name(soln.get("?name").toString())
            self.id = soln.get("?voltage_id").toString()
            self.bus1 = self.safe_name(soln.get("?bus1").toString())
            self.bus2 = self.safe_name(soln.get("?bus2").toString())
            self.phases = "ABC"
            self.len = float(soln.get("?len").toString())
            self.basev = float(soln.get("?basev").toString())
            self.r1 = float(soln.get("?r").toString())
            self.x1 = float(soln.get("?x").toString())
            self.b1 = self.optional_double(soln, "?b", 0.0)
            self.r0 = self.optional_double(soln, "?r0", 0.0)
            self.x0 = self.optional_double(soln, "?x0", 0.0)
            self.b0 = self.optional_double(soln, "?b0", 0.0)

    def get_json_entry(self):
        buf = '{"name":"' + self.name + '", "mRID":"' + self.id + '"}'
        return buf

    def display_string(self):
        return f"{self.name} from {self.bus1} to {self.bus2} phases={self.phases} " \
               f"basev={self.basev:.4f} len={self.len:.4f} r1={self.r1:.4f} x1={self.x1:.4f} " \
               f"b1={self.b1:.4f} r0={self.r0:.4f} x0={self.x0:.4f} b0={self.b0:.4f}"

    def get_glm(self):
        buf = []
        self.append_shared_glm_attributes(buf, self.name, False, False)

        seq_zs = self.c_format(complex((self.r0 + 2.0 * self.r1) / 3.0, (self.x0 + 2.0 * self.x1) / 3.0))
        seq_zm = self.c_format(complex((self.r0 - self.r1) / 3.0, (self.x0 - self.x1) / 3.0))
        seq_cs = f"{(1.0e9 * (self.b0 + 2.0 * self.b1) / 3.0 / self.g_omega):.4f}"
        seq_cm = f"{(1.0e9 * (self.b0 - self.b1) / 3.0 / self.g_omega):.4f}"

        buf.append("object line_configuration {\n")
        buf.append("  name \"lcon_" + self.name + "_ABC\";\n")
        for i in range(1, 4):
            for j in range(1, 4):
                indices = str(i) + str(j) + " "
                if i == j:
                    buf.append("  z" + indices + seq_zs + ";\n")
                    buf.append("  c" + indices + seq_cs + ";\n")
                else:
                    buf.append("  z" + indices + seq_zm + ";\n")
                    buf.append("  c" + indices + seq_cm + ";\n")
        buf.append("}\n")
        return "".join(buf)

    def label_string(self):
        return "seqZ"

    def get_dss(self):
        buf = [f"new Line.{self.name}", f" phases={self.dss_phase_count(self.phases, False)}",
               f" bus1={self.dss_bus_phases(self.bus1, self.phases)}"
               f" bus2={self.dss_bus_phases(self.bus2, self.phases)}",
               f" length={self.len:.1f} units=m\n"]
        self.append_dss_ratings(buf, self.normal_current_limit, self.emergency_current_limit)
        buf.append(f"~ r1={self.r1:.6f} x1={self.x1:.6f} c1={1.0e9 * self.b1 / self.g_omega:.6f}")
        buf.append(f" r0={self.r0:.6f} x0={self.x0:.6f} c0={1.0e9 * self.b0 / self.g_omega:.6f}\n")
        return "".join(buf)

    @property
    def sz_csv_header(self):
        return "Name,Bus1,Phases,Bus2,Phases,R1,X1,C1[nF],R0,X0,C0[nF],Length,Units"

    def get_csv(self):
        b = f"{self.name},{self.bus1},{self.csv_phase_string(self.phases)}," \
            f"{self.bus2},{self.csv_phase_string(self.phases)}," \
            f"{self.r1:.6f},{self.x1:.6f},{(1.0e9 * self.b1 / self.g_omega):.6f},{self.r0:.6f},{self.x0:.6f}," \
            f"{1.0e9 * self.b0 / self.g_omega:.6f}," \
            f"{self.len * self.g_ft_per_m:.3f},ft\n"
        return b
