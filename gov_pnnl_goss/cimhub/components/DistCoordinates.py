# from rdflib import QueryResult
from .DistComponent import DistComponent


class DistCoordinates(DistComponent):
    sz_cim_class = "Coordinates"
    def __init__(self, results):
        super().__init__()
        if results:
            row = results[0]  # Assuming results is a list of query results, adjust as needed
            self.name = self.safe_name(row["name"].toPython())
            self.x = float(row["x"].toPython())
            self.y = float(row["y"].toPython())
            self.seq = int(row["seq"].toPython())
            self.cname = row["class"].toPython()

    def get_json_entry(self):
        entry = {
            "name": self.name
        }
        return entry

    def display_string(self):
        return f"{self.cname}:{self.name}:{self.seq} x={self.x:.4f} y={self.y:.4f}"

    def get_key(self):
        return f"{self.cname}:{self.name}:{self.seq}"
