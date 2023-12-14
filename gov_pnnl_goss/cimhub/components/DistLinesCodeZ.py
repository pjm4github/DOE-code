from gov_pnnl_goss.cimhub.components.DistLineSegment import DistLineSegment


class DistLinesCodeZ(DistLineSegment):
    sz_cim_class = "LinesCodeZ"
    sz_csv_header = "Name,Bus1,Phases,Bus2,Phases,LineCode,Length,Units"

    def __init__(self, results, mapper):
        super().__init__()
        if results:
            soln = next(results)
            self.name = self.safe_name(soln.get("?name").toString())
            self.id = soln.get("?voltage_id").toString()
            self.bus1 = self.safe_name(soln.get("?bus1").toString())
            self.bus2 = self.safe_name(soln.get("?bus2").toString())
            self.basev = float(soln.get("?basev").toString())
            self.len = float(soln.get("?len").toString())
            self.lname = soln.get("?lname").toString()
            self.codeid = soln.get("?codeid").toString()
            nphs = mapper.get(self.name)
            if nphs > 0:
                buf = [soln.get("?phs").toString()]
                for _ in range(1, nphs):
                    soln = next(results)
                    buf.append(soln.get("?phs").toString())
                self.phases = "".join(buf)
            else:
                self.phases = "ABC"

    def get_json_entry(self):
        buf = []
        buf.append(f"{{\"name\":\"{self.name}\"")
        buf.append(f",\"mRID\":\"{self.id}\"")
        buf.append("}")
        return "".join(buf)

    def display_string(self):
        buf = []
        buf.append(f"{self.name} from {self.bus1} to {self.bus2} "
                   f"phases={self.phases} basev= {self.basev: .4f}"
                   f"len={self.len: .4f} linecode={self.lname}")
        return " ".join(buf)

    def get_glm(self):
        buf = []
        self.append_shared_glm_attributes(buf, self.lname, False, False)
        return "".join(buf)

    def get_key(self):
        return self.name

    def label_string(self):
        return self.lname

    def get_dss(self):
        buf = []
        buf.append(f"new Line.{self.name}")
        buf.append(f" phases={self.dss_phase_count(self.phases, False)}")
        buf.append(f" bus1={self.dss_bus_phases(self.bus1, self.phases)} "
                   f"bus2={self.dss_bus_phases(self.bus2, self.phases)}")
        buf.append(f" length={(self.len * self.g_ft_per_m):.3f} linecode={self.lname} units=ft")
        self.append_dss_ratings(buf, self.normal_current_limit, self.emergency_current_limit)
        return " ".join(buf)

    def get_csv(self):
        return f"{self.name},{self.bus1},{self.csv_phase_string(self.phases)},{self.bus2}," \
               f"{self.csv_phase_string(self.phases)},{self.lname},{(self.len * self.g_ft_per_m):.3f},ft"
