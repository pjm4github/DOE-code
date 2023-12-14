from rdflib import Graph
import json

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
    # Create an RDF graph and parse the RDF data
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


    # print(json.dumps(l1_objects, indent=2))


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

    # print(json.dumps(l2_objects, indent=2))

    # Now remove the sub-objects
    # For any object that references another existing name, this will be a subclass that is extracted

    l3_objects = {}
    for o in l2_objects:
        l3_objects[o] = l2_objects[o]['subobjects']

    process_dict(l3_objects)

    print(json.dumps(l3_objects, indent=2))

    # Now walk down the keys to the third object and look for a subfield
    # Look for the root_name in the dictionary and for any objects that are part of the CIM types
    # make them into class calls with parameters that meet the external call requirement with the example values.

    return l3_objects



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

    objects = build_init_struct('PowerTransformer', rdf_data)

    print(json.dumps(objects, indent=2))