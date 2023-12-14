from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


# @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
# @prefix cim: <http://iec.ch/TC57/CIM#>.
# @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
# @prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
#
# # Define a DistributionTransformer instance
# cim:DistributionTransformer_001 a cim:DistributionTransformer.
#
# # Define attributes of the Distribution Transformer
# cim:DistributionTransformer_001 cim:IdentifiedObject.name "Transformer001".
# cim:DistributionTransformer_001 cim:PowerTransformer.ratedS "500"^^xsd:float.
# cim:DistributionTransformer_001 cim:PowerTransformer.ratedU "138"^^xsd:float.
#
# # Define winding instances and their properties
# cim:PowerTransformerEnd_001 a cim:PowerTransformerEnd.
# cim:PowerTransformerEnd_001 cim:IdentifiedObject.name "Winding_1".
# cim:PowerTransformerEnd_001 cim:PowerTransformerEnd.ratedU "138"^^xsd:float.
# cim:PowerTransformerEnd_001 cim:PowerTransformerEnd.ratedS "500"^^xsd:float.
#
# cim:PowerTransformerEnd_002 a cim:PowerTransformerEnd.
# cim:PowerTransformerEnd_002 cim:IdentifiedObject.name "Winding_2".
# cim:PowerTransformerEnd_002 cim:PowerTransformerEnd.ratedU "13.8"^^xsd:float.
# cim:PowerTransformerEnd_002 cim:PowerTransformerEnd.ratedS "500"^^xsd:float.
#
# # Connect windings to the Distribution Transformer
# cim:DistributionTransformer_001 cim:PowerTransformer.PowerTransformerEnd cim:PowerTransformerEnd_001.
# cim:DistributionTransformer_001 cim:PowerTransformer.PowerTransformerEnd cim:PowerTransformerEnd_002.
#
# # Additional properties and relationships can be represented as needed.

class DistSubstation(DistComponent, PowerTransformer, TransformerEnd):
    """
    In the simplified CIM representation of a Distribution Transformer that I provided, let's identify the parent classes of the represented object:

    DistributionTransformer_001 is an instance of the DistributionTransformer class.

    Parent class: PowerTransformer
    PowerTransformerEnd_001 and PowerTransformerEnd_002 are instances of the PowerTransformerEnd class.

    Parent class: TransformerEnd
    TransformerEnd is a subclass of the PowerSystemResource class.

    Parent class: PowerSystemResource
    PowerSystemResource is a subclass of the IdentifiedObject class.

    Parent class: IdentifiedObject
    Here's how the parent classes are structured in this simplified CIM representation:

    DistributionTransformer is a subclass of PowerTransformer.
    PowerTransformerEnd is a subclass of TransformerEnd, which is in turn a subclass of PowerSystemResource, and ultimately, PowerSystemResource is a subclass of IdentifiedObject.
    """
    sz_cim_class = "DistributionTransformer"

    def __init__(self):
        self.name = "Transformer001"
        self.ratedS  = 500.0 # float.