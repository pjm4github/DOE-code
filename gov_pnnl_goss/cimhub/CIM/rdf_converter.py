import re

from rdflib import Graph
import json

def sort_dict_recursive(input_dict):
    if isinstance(input_dict, dict):
        sorted_dict = {}
        for key in sorted(input_dict.keys()):
            sorted_dict[key] = sort_dict_recursive(input_dict[key])
        return sorted_dict
    elif isinstance(input_dict, list):
        return [sort_dict_recursive(item) for item in input_dict]
    else:
        return input_dict

def process_dict(input_dict):
    # Iterate through the dictionary items
    for key, value in input_dict.items():
        if isinstance(value, list) and len(value) == 1:
            # If the value is a list with only one element, replace it with that element
            input_dict[key] = value[0]
        elif isinstance(value, dict):
            # If the value is a nested dictionary, recursively process it
            process_dict(value)

def build_init_struct(root_name, rdf_data):
    """
    :param root_name: A string that represents the class name of the object that will be created
    :param rdf_data: The RDF data field that is presented as an example of the
    :return:
    """

    g = Graph()

    g.parse(data=rdf_data, format="turtle")


    # Convert RDF graph to JSON
    result = []
    for subject, predicate, obj in g:
        result.append({
            "subject": str(subject),
            "predicate": str(predicate),
            "object": str(obj)
        })

    # Serialize the JSON data
    # json_data = json.dumps(result, indent=2)

    # Print or save the JSON data
    # print(json_data)

    lines = []
    for r in result:
        if r['object'].find('#') > 0:
            v = r['object'].split('#')[1]
        else:
            v = r['object']
        lines.append(f"{r['subject'].split('#')[1]}|{r['predicate'].split('#')[1]}|{v}")

    # Show the lines that are ready to be listed
    print_rdf = False
    if print_rdf:
        for l in lines:
            print(l)

    l0_objects = {}
    for l in lines:
        parts = l.split('|')
        if parts[0] not in l0_objects.keys():
            l0_objects[parts[0]] = ['|'.join(parts[1:])]
        else:
            l0_objects[parts[0]].append('|'.join(parts[1:]))

    # for o in l0_objects:
    #     print(f"{o}, {l0_objects[o]}")
    print_l0 = False
    if print_l0:
        print(json.dumps(l0_objects, indent=2))

    l1_objects = {}
    for o in l0_objects:
        subparts = l0_objects[o]
        subobjects = {}
        for s in subparts:
            parts = s.split('|')
            if parts[0] not in subobjects.keys():
                subobjects[parts[0]] = ['|'.join(parts[1:])]
            else:
                subobjects[parts[0]].append('|'.join(parts[1:]))
        l1_objects[o] = {'subobjects':  subobjects}

    print_l1 = False
    if print_l1:
        print(json.dumps(l1_objects, indent=2))


    l2_objects = {}
    for o in l1_objects: # the keys of the
        subparts = l1_objects[o]['subobjects']
        subobjects = {}
        for s in subparts:  # The keys of the sub-objects
            if s.find('.')<0:
                subobjects[s] = subparts[s]  # just keep this
                # this needs to be split further
            else:
                parts = s.split('.')
                value = l1_objects[o]['subobjects'][s]
                key = parts[0]
                new_key = parts[1]
                if key not in subobjects.keys():
                    subobjects[key] = {new_key: value}
                else:
                    subobjects[key][new_key] = value
        l2_objects[o] = {'subobjects': subobjects}  # replace the key with the sub-objects

    print_l2 = False
    if print_l2:
        print(json.dumps(l2_objects, indent=2))

    # Now remove the sub-objects
    # For any object that references another existing name, this will be a subclass that is extracted

    l3_objects = {}
    for o in l2_objects:
        l3_objects[o] = l2_objects[o]['subobjects']

    process_dict(l3_objects)

    sorted_dict = sort_dict_recursive(l3_objects)
    print_l3 = False
    if print_l3:
        print(json.dumps(sorted_dict, indent=2))

    # Now walk down the keys to the third object and look for a subfield
    # Look for the root_name in the dictionary and for any objects that are part of the CIM types
    # make them into class calls with parameters that meet the external call requirement with the example values.

    return sorted_dict



if __name__ == "__main__":
    rdf_data = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix cim: <http://iec.ch/TC57/CIM#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#>.

    # Define a PowerTransformer instance
    cim:PowerTransformer_001 a cim:PowerTransformer.

    # Define attributes of the PowerTransformer
    cim:PowerTransformer_001 cim:IdentifiedObject.name "Transformer001".
    cim:PowerTransformer_001 cim:PowerTransformer.ratedS "1000"^^xsd:float.
    cim:PowerTransformer_001 cim:PowerTransformer.ratedU "138"^^xsd:float.

    # Define winding instances and their properties
    cim:PowerTransformerEnd_001 a cim:PowerTransformerEnd.
    cim:PowerTransformerEnd_001 cim:IdentifiedObject.name "Winding_1".
    cim:PowerTransformerEnd_001 cim:PowerTransformerEnd.ratedU "138"^^xsd:float.
    cim:PowerTransformerEnd_001 cim:PowerTransformerEnd.ratedS "500"^^xsd:float.

    cim:PowerTransformerEnd_002 a cim:PowerTransformerEnd.
    cim:PowerTransformerEnd_002 cim:IdentifiedObject.name "Winding_2".
    cim:PowerTransformerEnd_002 cim:PowerTransformerEnd.ratedU "13.8"^^xsd:float.
    cim:PowerTransformerEnd_002 cim:PowerTransformerEnd.ratedS "500"^^xsd:float.

    # Connect windings to the PowerTransformer
    cim:PowerTransformer_001 cim:PowerTransformer.PowerTransformerEnd cim:PowerTransformerEnd_001.
    cim:PowerTransformer_001 cim:PowerTransformer.PowerTransformerEnd cim:PowerTransformerEnd_002.

    """


    rdf_data_bad = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix cim: <http://iec.ch/TC57/CIM#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
    
    # Define a PowerTransformer instance
    cim:PowerTransformer_001 a cim:PowerTransformer.
    
    # Define attributes of the PowerTransformer
    cim:PowerTransformer_001 cim:IdentifiedObject.name "Transformer001".
    cim:PowerTransformer_001 cim:PowerTransformer.ratedS "1000"^^xsd:float.
    cim:PowerTransformer_001 cim:PowerTransformer.ratedU "138"^^xsd:float.
    
    # Define winding instances and their properties
    cim:PowerTransformerEnd_001 a cim:PowerTransformerEnd.
    cim:PowerTransformerEnd_001 cim:IdentifiedObject.name "Winding_1".
    cim:PowerTransformerEnd_001 cim:PowerTransformerEnd.ratedU "138"^^xsd:float.
    cim:PowerTransformerEnd_001 cim:PowerTransformerEnd.ratedS "500"^^xsd:float.
    
    cim:PowerTransformerEnd_002 a cim:PowerTransformerEnd.
    cim:PowerTransformerEnd_002 cim:IdentifiedObject.name "Winding_2".
    cim:PowerTransformerEnd_002 cim:PowerTransformerEnd.ratedU "13.8"^^xsd:float.
    cim:PowerTransformerEnd_002 cim:PowerTransformerEnd.ratedS "500"^^xsd:float.
    
    # Connect windings to the PowerTransformer
    cim:PowerTransformer_001 cim:PowerTransformer.PowerTransformerEnd cim:PowerTransformerEnd_001.
    cim:PowerTransformer_001 cim:PowerTransformer.PowerTransformerEnd cim:PowerTransformerEnd_002.
    
    # Define the manufacturer of the PowerTransformer
    cim:PowerTransformer_001 cim:Equipment.Equipment.manufacturer "ABC Transformers Ltd.".
    
    # Define the location of the PowerTransformer
    cim:Location_001 a cim:Location.
    cim:Location_001 cim:IdentifiedObject.name "SubstationLocation".
    cim:Location_001 cim:Location.CoordinateSystem "WGS84"^^xsd:string.
    cim:Location_001 cim:Location.Latitude "38.12345"^^xsd:double.
    cim:Location_001 cim:Location.Longitude "-122.67890"^^xsd:double.
    cim:Location_001 cim:Location.Elevation "100"^^xsd:double.
    
    # Connect the PowerTransformer to its location
    cim:PowerTransformer_001 cim:PowerSystemResource.Location cim:Location_001.
    
    # Define the substation where the PowerTransformer is located
    cim:Substation_001 a cim:Substation.
    cim:Substation_001 cim:IdentifiedObject.name "Substation001".
    
    # Connect the PowerTransformer to the Substation
    cim:Substation_001 cim:Equipment.Equipment.PowerSystemResource cim:PowerTransformer_001.
    
    # Additional properties and relationships can be represented as needed.
    
    """

    rdf_data = """
    @prefix cim: <http://iec.ch/TC57/2013/CIM-schema-cim16#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    
    # CompositeSwitch instance
    cim:CompositeSwitch_12345 a cim:CompositeSwitch ;
        cim:IdentifiedObject.name "ExampleCompositeSwitch" ;
        cim:IdentifiedObject.description "A complex composite switch" ;
        cim:Equipment.EquipmentContainer cim:Substation1 ;
        cim:Switch.normalOpen "false" ;
        cim:Switch.ratedCurrent 1000.0 ;
        cim:Switch.ratedVoltage 138.0 ;
        cim:Switch.RetainedVoltage "true" ;
        cim:Switch.SwitchSchedule cim:SwitchSchedule_56789 .
    
    # Substation where the CompositeSwitch is located
    cim:Substation1 a cim:Substation ;
        cim:Substation.Region cim:Region1 .
    
    # Region information
    cim:Region1 a cim:SubGeographicalRegion ;
        cim:SubGeographicalRegion.RegionName "ExampleRegion" ;
        cim:Region.RegionName "ExampleRegion" .
    
    # Switching schedule associated with the CompositeSwitch
    cim:SwitchSchedule_56789 a cim:SwitchingSchedule ;
        cim:IdentifiedObject.name "ExampleSwitchSchedule" ;
        cim:SwitchingSchedule.SwitchingSteps cim:SwitchingStep_98765 .
    
    # Switching step within the Switching Schedule
    cim:SwitchingStep_98765 a cim:SwitchingStep ;
        cim:IdentifiedObject.name "SwitchingStep1" ;
        cim:SwitchingStep.sequenceNumber 1 ;
        cim:SwitchingStep.SwitchAction cim:SwitchAction_54321 .
    
    # Switching action within the Switching Step
    cim:SwitchAction_54321 a cim:SwitchAction ;
        cim:IdentifiedObject.name "OpenSwitchAction" ;
        cim:SwitchAction.actionType "Open" ;
        cim:SwitchAction.associatedSwitch cim:CompositeSwitch_12345 .
    """

    rdf_data = """
    @prefix cim: <http://iec.ch/TC57/2013/CIM-schema-cim16#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    
    # Connector instance
    cim:Connector_12345 a cim:Connector ;
        cim:IdentifiedObject.name "ExampleConnector" ;
        cim:IdentifiedObject.description "A complex connector" ;
        cim:Connector.phases "ABC" ;
        cim:Connector.ratedCurrent 2000.0 ;
        cim:Connector.ratedVoltage 220.0 ;
        cim:Connector.pins "3" ;
        cim:Connector.FacilityConnection cim:FacilityConnection_56789 .
    
    # Facility connection associated with the Connector
    cim:FacilityConnection_56789 a cim:FacilityConnection ;
        cim:IdentifiedObject.name "ExampleFacilityConnection" ;
        cim:FacilityConnection.connectingElements cim:PowerTransformer_98765,
                                                 cim:Line_54321 .
    
    # PowerTransformer connected to the Connector
    cim:PowerTransformer_98765 a cim:PowerTransformer ;
        cim:IdentifiedObject.name "ExamplePowerTransformer" ;
        cim:PowerTransformer.vectorGroup "Dyn11" ;
        cim:PowerTransformer.EquipmentContainer cim:Substation1 .
    
    # Line connected to the Connector
    cim:Line_54321 a cim:ACLineSegment ;
        cim:IdentifiedObject.name "ExampleLine" ;
        cim:Conductor.material "Copper" ;
        cim:ACLineSegment.length 500.0 ;
        cim:ACLineSegment.EquipmentContainer cim:Substation1 .
    
    # Substation where the Connector is located
    cim:Substation1 a cim:Substation ;
        cim:Substation.Region cim:Region1 .
    
    # Region information
    cim:Region1 a cim:SubGeographicalRegion ;
        cim:SubGeographicalRegion.RegionName "ExampleRegion" ;
        cim:Region.RegionName "ExampleRegion" .
    """
    rdf_data = """
    @prefix cim: <http://iec.ch/TC57/2013/CIM-schema-cim16#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    
    cim:CoolantType_12345 a cim:CoolantType ;
    cim:IdentifiedObject.name "ExampleCoolantType" ;
    cim:IdentifiedObject.description "A complex coolant global_property_types" ;
    cim:CoolantType.temperatureRange "-20°C to 100°C" ;
    cim:CoolantType.dielectricConstant 2.5 ;
    cim:CoolantType.conductivity 0.001 ;
    cim:CoolantType.flashPoint 50.0 .
    """

    rdf_data = """
    @prefix cim: <http://iec.ch/TC57/2013/CIM-schema-cim16#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    
    # Disconnector instance
    cim:Disconnector_12345 a cim:Disconnector ;
    cim:IdentifiedObject.name "ExampleDisconnector" ;
    cim:IdentifiedObject.description "A complex disconnector" ;
    cim:Switch.normalOpen "true" ;
    cim:Switch.ratedCurrent 800.0 ;
    cim:Switch.ratedVoltage 220.0 ;
    cim:Switch.RetainedVoltage "false" ;
    cim:Switch.SwitchSchedule cim:SwitchSchedule_56789 .
    
    # Substation where the Disconnector is located
    cim:Substation1 a cim:Substation ;
    cim:Substation.Region cim:Region1 .
    
    # Region information
    cim:Region1 a cim:SubGeographicalRegion ;
    cim:SubGeographicalRegion.RegionName "ExampleRegion" ;
    cim:Region.RegionName "ExampleRegion" .
    
    # Switching schedule associated with the Disconnector
    cim:SwitchSchedule_56789 a cim:SwitchingSchedule ;
    cim:IdentifiedObject.name "ExampleSwitchSchedule" ;
    cim:SwitchingSchedule.SwitchingSteps cim:SwitchingStep_98765 .
    
    # Switching step within the Switching Schedule
    cim:SwitchingStep_98765 a cim:SwitchingStep ;
    cim:IdentifiedObject.name "SwitchingStep1" ;
    cim:SwitchingStep.sequenceNumber 1 ;
    cim:SwitchingStep.SwitchAction cim:SwitchAction_54321 .
    
    # Switching action within the Switching Step
    cim:SwitchAction_54321 a cim:SwitchAction ;
    cim:IdentifiedObject.name "OpenSwitchAction" ;
    cim:SwitchAction.actionType "Open" ;
    cim:SwitchAction.associatedSwitch cim:Disconnector_12345 .
    
    """
    objects = build_init_struct('Disconnector', rdf_data_bad)
    print("##############################################")
    print(json.dumps(objects, indent=2))