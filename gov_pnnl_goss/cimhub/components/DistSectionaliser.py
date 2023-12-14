from gov_pnnl_goss.cimhub.components.DistSwitch import DistSwitch

class DistSectionaliser(DistSwitch):
    sz_cim_class = "Sectionalizer"

    def __init__(self, results):
        super().__init__(results)

    def cim_class(self):
        return self.sz_cim_class

    def get_glm(self):
        buf = ["object sectionalizer {",
               f"  name \"swt_{self.name}\";",
               f"  from \"{self.bus1}\";",
               f"  to \"{self.bus2}\";",
               f"  phases {self.glm_phases};"]
        if self.open:
            buf.append("  status OPEN;")
        else:
            buf.append("  status CLOSED;")

        self.append_glm_ratings(buf, self.glm_phases, self.normal_current_limit, self.emergency_current_limit)
        buf.append("}")

        return "\n".join(buf)
