from .DistSwitch import DistSwitch


class DistFuse(DistSwitch):
    sz_cim_class = "Fuse"

    def __init__(self, results):
        super().__init__(results)

    def cim_class(self):
        return self.sz_cim_class

    def get_glm(self):
        buf = []
        buf.append("object fuse {")
        buf.append("  name \"swt_" + self.name + "\";")
        buf.append("  from \"" + self.bus1 + "\";")
        buf.append("  to \"" + self.bus2 + "\";")
        buf.append("  phases " + self.glm_phases + ";")
        buf.append("  current_limit " + "{:.2f}".format(self.rated) + ";")
        if self.open:
            buf.append("  status OPEN;")
        else:
            buf.append("  status CLOSED;")
        buf.append("  mean_replacement_time 3600;")
        self.append_glm_ratings(buf, self.glm_phases, self.normal_current_limit, self.emergency_current_limit)
        buf.append("}")
        return "\n".join(buf)

    def get_dss(self):
        buf = []
        buf.append(super().get_dss())
        buf.append("  new Fuse." + self.name + " MonitoredObj=Line." + self.name +
                   " RatedCurrent=" + "{:.2f}".format(self.rated))
        return "\n".join(buf)
