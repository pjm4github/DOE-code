from .DistSwitch import DistSwitch


class DistDisconnector(DistSwitch):
    sz_cim_class = "Disconnector"

    def __init__(self, results):
        super().__init__(results)

    def cim_class(self):
        return self.sz_cim_class
