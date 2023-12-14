from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistFeeder(DistComponent):
    sz_cim_class = "Feeder"

    def __init__(self, results):
        super().__init__()
        if results:
            row = results[0]
            self.feeder_name = self.safe_name(row["feeder"].toPython())
            self.feeder_id = row["fid"].toPython()
            self.region_name = self.safe_name(row["region"].toPython())
            self.region_id = row["rgnid"].toPython()
            self.substation_name = self.safe_name(self.optional_string(row, "?station", None))
            self.substation_id = self.optional_string(row, "?sid", None)
            self.subregion_name = self.safe_name(self.optional_string(row, "?subregion", None))
            self.subregion_id = self.optional_string(row, "?sgrid", None)

    def get_json_entry(self):
        entry = {
            "name": self.feeder_name,
            "mRID": self.feeder_id,
            "substationName": self.substation_name,
            "substationID": self.substation_id,
            "subregionName": self.subregion_name,
            "subregionID": self.subregion_id,
            "regionName": self.region_name,
            "regionID": self.region_id
        }
        return entry

    def display_string(self):
        return f"{self.feeder_name}:{self.feeder_id}\n" \
               f"  {self.substation_name}:{self.substation_id}\n" \
               f"  {self.subregion_name}:{self.subregion_id}\n" \
               f"  {self.region_name}:{self.region_id}\n"

    def get_key(self):
        return self.feeder_name
