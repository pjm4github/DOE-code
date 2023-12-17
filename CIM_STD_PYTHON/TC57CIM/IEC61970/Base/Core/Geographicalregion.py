

class GeographicalRegion(IdentifiedObject):
    def __init__(self):
        super().__init__()
        self.regions = SubGeographicalRegion()  # All sub-geographical regions within this geographical region.
