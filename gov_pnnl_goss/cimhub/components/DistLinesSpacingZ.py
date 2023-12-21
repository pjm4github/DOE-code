from gov_pnnl_goss.cimhub.components.DistLineSegment import DistLineSegment


class DistLinesSpacingZ(DistLineSegment):
    sz_cim_class = "LineSpacingZ"
    sz_csv_header = "Name,Bus1,Phases,Bus2,Phases,Spacing,WireType,WireNames,Length,Units"

    def __init__(self, results, mapper):
        super().__init__()

        self.spacing = ""
        self.spcid = ""
        self.nwires = 0
        self.wire_phases = []
        self.wire_names = []
        self.wire_classes = []
        self.glm_config = ""
        if results:
            soln = next(results)
            self.name = self.safe_name(soln.get("?name").to"")
            self.id = soln.get("?voltage_id").to""
            self.bus1 = self.safe_name(soln.get("?bus1").to"")
            self.bus2 = self.safe_name(soln.get("?bus2").to"")
            self.len = float(soln.get("?len").to"")
            self.basev = float(soln.get("?basev").to"")
            self.spacing = soln.get("?spacing").to""
            self.spcid = soln.get("?spcid").to""
            self.nwires = mapper[self.name]
            self.wire_phases = [soln.get("?phs").to"" for _ in range(self.nwires)]
            self.wire_names = [soln.get("?phname").to"" for _ in range(self.nwires)]
            self.wire_classes = [soln.get("?phclass").to"" for _ in range(self.nwires)]
            buf = []

            for i in range(self.nwires):
                if not self.wire_phases[i] == "N":
                    buf.append(self.wire_phases[i])
                # if i + 1 < self.nwires:
                #     # This should probably just break if there are no more wires
                #     soln = next(results)

            self.phases = "".join(buf)

    def display_string(self):
        buf = [f'{self.name} from {self.bus1} to {self.bus2}',
               f' basev={self.basev:.4f} len={self.len:.4f} spacing={self.spacing}']
        for i in range(self.nwires):
            buf.append(f' phs={self.wire_phases[i]} wire={self.wire_names[i]} class={self.wire_classes[i]}')

        return "\n".join(buf)

    def get_json_entry(self):
        return f'{{"name":"{self.name}","mRID":"{self.id}"}}'

    def get_glm(self):
        b_force_n = False
        buf = ""
        if self.wire_classes[0] == "OverheadWireInfo":
            self.b_cable = False
        else:
            self.b_cable = True
            if self.wire_classes[-1] == "OverheadWireInfo":
                b_force_n = True
        self.append_shared_glm_attributes(buf, self.glm_config, True, b_force_n)
        return buf

    def get_key(self):
        return self.name

    def label_string(self):
        return f"{self.spacing}:{self.wire_names[0]}"

    def get_dss(self):
        b_cable = False
        buf = [f'new Line.{self.name}', f' phases={self.dss_phase_count(self.phases, False)}',
               f' bus1={self.dss_bus_phases(self.bus1, self.phases)}',
               f' bus2={self.dss_bus_phases(self.bus2, self.phases)}',
               f' length={self.len * self.g_ft_per_m:.1f} units=ft', f' spacing={self.spacing}_{self.phases}']
        buf = self.append_dss_ratings(buf, self.normal_current_limit, self.emergency_current_limit)

        if self.wire_classes[0] == "OverheadWireInfo":
            buf.append("~ wires=[")

        elif self.wire_classes[0] == "ConcentricNeutralCableInfo":
            buf.append("~ CNCables=[")
            b_cable = True

        elif self.wire_classes[0] == "TapeShieldCableInfo":
            buf.append("~ TSCables=[")
            b_cable = True

        for i in range(self.nwires):
            if b_cable and self.wire_classes[i] == "OverheadWireInfo":
                buf.append("] wires=[")
            elif i > 0:
                buf.append(",")
            buf.append(self.wire_names[i])

        buf.append("]")

        return "\n".join(buf)

    @staticmethod
    def get_csv_header():
        return "Name,Bus1,Phases,Bus2,Phases,Spacing,WireType,WireNames,Length,Units"

    def get_csv(self):
        wire_type = "TS" if self.wire_classes[0] == "TapeShieldCableInfo" else "CN" \
            if self.wire_classes[0] == "ConcentricNeutralCableInfo" else "OHD"
        wire_names = ",".join([f'"{name}"' for name in self.wire_names])
        return f"{self.name},{self.bus1},{self.csv_phase_string(self.phases)},{self.bus2}," \
               f"{self.csv_phase_string(self.phases)},{self.spacing},{wire_type},{wire_names}," \
               f"{(self.len * self.g_ft_per_m):.3f},ft\n"
