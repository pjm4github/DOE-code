from gov_pnnl_goss.cimhub.components.DistSwitch import DistSwitch


class DistJumper(DistSwitch):
    sz_cim_class = "Jumper"

    def __init__(self, results):
        super().__init__(results)

    def cim_class(self):
        return self.sz_cim_class

