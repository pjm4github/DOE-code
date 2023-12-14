from typing import Dict
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent



class DistPowerXfmrCore(DistComponent):
    """
    Here is an example RDF transformer model:
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
            @prefix cim: <http://iec.ch/TC57/CIM#>.
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
            @prefix xsd: <http://www.w3.org/2001/XMLSchema#>.

            # Define a PowerTransformer instance
            cim:PowerTransformer_001 a cim:PowerTransformer.

            # Define attributes of the PowerTransformer
            cim:PowerTransformer_001 cim:IdentifiedObject.name "PT001".
            cim:PowerTransformer_001 cim:Equipment.EquipmentContainer cim:Substation_001.
            cim:PowerTransformer_001 cim:PowerTransformer.ratedS "1000"^^xsd:float.
            cim:PowerTransformer_001 cim:PowerTransformer.ratedU "138"^^xsd:float.

            # Define winding instances and their properties
            cim:Winding_001 a cim:PowerTransformerEnd.
            cim:Winding_001 cim:IdentifiedObject.name "Winding_1".
            cim:Winding_001 cim:PowerTransformerEnd.ratedU "138"^^xsd:float.
            cim:Winding_001 cim:PowerTransformerEnd.ratedS "500"^^xsd:float.

            cim:Winding_002 a cim:PowerTransformerEnd.
            cim:Winding_002 cim:IdentifiedObject.name "Winding_2".
            cim:Winding_002 cim:PowerTransformerEnd.ratedU "13.8"^^xsd:float.
            cim:Winding_002 cim:PowerTransformerEnd.ratedS "500"^^xsd:float.

            # Connect windings to the PowerTransformer
            cim:PowerTransformer_001 cim:PowerTransformer.PowerTransformerEnd cim:Winding_001.
            cim:PowerTransformer_001 cim:PowerTransformer.PowerTransformerEnd cim:Winding_002.

            # Define substation and its relationship with the PowerTransformer
            cim:Substation_001 a cim:Substation.
            cim:Substation_001 cim:IdentifiedObject.name "Substation_1".
            cim:Substation_001 cim:Substation.Region cim:Region_001.

            # Define a region
            cim:Region_001 a cim:SubGeographicalRegion.
            cim:Region_001 cim:IdentifiedObject.name "Region_1".

            # Additional properties and relationships can be represented as needed.

    """
    sz_cim_class = "PowerXfmrCore"

    def __init__(self, results: Dict):
        super().__init__()
        self.name = ""
        self.wdg = 0
        self.b = 0.0
        self.g = 0.0
        if results:
            soln = results[0]
            self.name = self.safe_name(soln.get("?pname"))
            self.wdg = int(soln.get("?enum"))
            self.b = float(soln.get("?b"))
            self.g = float(soln.get("?g"))

    def display_string(self):
        return f"{self.name} wdg={self.wdg} g={self.g:.4f} b={self.b:.4f}"

    def get_key(self):
        return self.name

    def get_json_entry(self):
        return f'{{"name":"{self.name}"}}'
