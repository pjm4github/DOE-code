import math
import json
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent



class DistSubstation(DistComponent):
    """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix cim: <http://iec.ch/TC57/CIM#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#>.

    # Define a Distribution Substation instance
    cim:DistributionSubstation_001 a cim:DistributionSubstation.

    # Define attributes of the Distribution Substation
    cim:DistributionSubstation_001 cim:IdentifiedObject.name "Substation001".
    cim:DistributionSubstation_001 cim:Substation.region cim:SubGeographicalRegion_001.

    # Define the location of the Distribution Substation
    cim:Location_001 a cim:Location.
    cim:Location_001 cim:IdentifiedObject.name "Location001".
    cim:Location_001 cim:Location.CoordinateSystem "WGS84"^^xsd:string.
    cim:Location_001 cim:Location.Latitude "38.12345"^^xsd:double.
    cim:Location_001 cim:Location.Longitude "-122.67890"^^xsd:double.
    cim:Location_001 cim:Location.Elevation "100"^^xsd:double.

    # Connect the Distribution Substation to its location
    cim:DistributionSubstation_001 cim:Substation.Location cim:Location_001.

    # Define the sub-geographical region
    cim:SubGeographicalRegion_001 a cim:SubGeographicalRegion.
    cim:SubGeographicalRegion_001 cim:IdentifiedObject.name "Region001".


    """
    sz_cim_class = "Substation"
    sz_csv_header = "Name,Bus,kV,pu,X"
    
    def __init__(self, results):
        super().__init__()
        self.id = ""
        self.name = ""
        self.bus = ""
        self.basev = 0.0
        self.nomv = 0.0
        self.vmag = 0.0
        self.vang = 0.0
        self.r1 = 0.0
        self.x1 = 0.0
        self.r0 = 0.0
        self.x0 = 0.0

        if results:
            if results.hasNext():
                soln = results.next()
                self.name = self.safe_name(soln["name"].toString())
                self.id = soln["voltage_id"].toString()
                self.bus = self.safe_name(soln["bus"].toString())
                self.basev = float(soln["basev"].toString())
                self.nomv = float(soln["nomv"].toString())
                self.vmag = float(soln["vmag"].toString())
                self.vang = float(soln["vang"].toString())
                self.r1 = float(soln["r1"].toString())
                self.x1 = float(soln["x1"].toString())
                self.r0 = float(soln["r0"].toString())
                self.x0 = float(soln["x0"].toString())

    def get_json_entry(self):
        return json.dumps({
            "name": self.name,
            "mRID": self.id
        })

    def display_string(self):
        return (f"{self.name} @ {self.bus} basev={format(self.basev, '.4f')} nomv={format(self.nomv, '.4f')} "
                f"vmag={format(self.vmag, '.4f')} vang={format(self.vang, '.4f')} "
                f"r1={format(self.r1, '.4f')} x1={format(self.x1, '.4f')} "
                f"r0={format(self.r0, '.4f')} x0={format(self.x0, '.4f')}")

    def get_json_symbols(self, map):
        pt = map.get(f"EnergySource:{self.name}:1")
        return json.dumps({
            "name": self.name,
            "bus": self.bus,
            "phases": "ABC",
            "nominal_voltage": format(self.nomv / math.sqrt(3.0), '.1f'),
            "x1": format(pt.x, '.1f'),
            "y1": format(pt.y, '.1f')
        })

    def get_dss(self):
        return (f"new Circuit.{self.name} phases=3 bus1={self.bus} basekv={format(0.001 * self.nomv, '.3f')} "
                f"pu={format(self.vmag / self.nomv, '.5f')} "
                f"angle={format(self.vang * 180.0 / math.pi, '.5f')} "
                f"r0={format(self.r0, '.5f')} x0={format(self.x0, '.5f')} "
                f"r1={format(self.r1, '.5f')} x1={format(self.x1, '.5f')}\n")

    def get_csv(self):
        return (f"{self.name},{self.bus},{format(0.001 * self.nomv, '.3f')},"
                f"{format(self.vmag / self.nomv, '.5f')},{format(self.x1, '.5f')}\n")

    def get_key(self):
        return self.name

    def sz_csv_header(self):
        return self.sz_csv_header
