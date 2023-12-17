from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.IdentifiedObject import IdentifiedObject


class SubGeographicalRegion(IdentifiedObject):
    def __init__(self):
        super().__init__()
        self.lines = Line()  # The lines within the sub-geographical region.
        self.substations = Substation()  # The substations in this sub-geographical region.
