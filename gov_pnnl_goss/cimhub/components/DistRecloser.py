from typing import Dict
from gov_pnnl_goss.cimhub.components.DistSwitch import DistSwitch


class DistRecloser(DistSwitch):
    sz_cim_class = "Recloser"

    def __init__(self, results: Dict[str, int]):
        super().__init__(results)

    def cim_class(self):
        return self.sz_cim_class

    def get_glm(self):
        buf = []
        buf.append("object recloser {")
        buf.append(f"  name \"swt_{self.name}\";")
        buf.append(f"  from \"{self.bus1}\";")
        buf.append(f"  to \"{self.bus2}\";")
        buf.append(f"  phases {self.glm_phases};")

        if self.open:
            buf.append("  status OPEN;")
        else:
            buf.append("  status CLOSED;")

        self.append_glm_ratings(buf, self.glm_phases, self.normal_current_limit, self.emergency_current_limit)
        buf.append("}")
        return "\n".join(buf)

    def get_dss(self):
        buf = super().get_dss()
        buf += f"  new Recloser.{self.name} MonitoredObj=Line.{self.name} PhaseTrip=20000.0 GroundTrip=10000.0\n"
        return buf
