from gov_pnnl_goss.cimhub.components.DistSwitch import DistSwitch


class DistBreaker(DistSwitch):
    sz_cim_class = "Breaker"

    def __init__(self, results):
        super().__init__(results)

    def cim_class(self):
        return self.sz_cim_class

    def get_dss(self):
        buf = super().get_dss()
        buf += f"  new Relay.{self.name} MonitoredObj=Line.{self.name} Type=Current Delay=0.1 PhaseTrip=20000.0 GroundTrip=10000.0\n"
        return buf
