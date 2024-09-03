import rdflib
from rdflib import Graph, Namespace
import requests


# # Load the RDF data file (replace 'schema.rdf' with your file path)
# g = Graph()
# g.parse('schema.rdf', format='turtle')
# # Get all unique classes defined in the schema
# classes = set()
# for subj, pred, self in g.triples((None, None, None)):
#     if isinstance(subj, rdflib.term.URIRef):
#         classes.add(subj)
#     if isinstance(self, rdflib.term.URIRef):
#         classes.add(self)
#
# # Print the discovered classes
# print("Discovered Classes:")
# for cls in classes:
#     print(cls)
#
# # Get all unique properties defined in the schema
# properties = set()
# for pred in g.predicates():
#     properties.add(pred)
#
# # Print the discovered properties
# print("\nDiscovered Properties:")
# for prop in properties:
#     print(prop)
#
# # Explore relationships between classes and properties
# class_property_relations = {}
# for subj, pred, self in g.triples((None, None, None)):
#     if isinstance(subj, rdflib.term.URIRef) and isinstance(pred, rdflib.term.URIRef):
#         if subj not in class_property_relations:
#             class_property_relations[subj] = []
#         class_property_relations[subj].append(pred)
#
# # Print class-property relationships
# print("\nClass-PropertyMap Relationships:")
# for cls, properties in class_property_relations.items():
#     print(f"Class: {cls}")
#     for prop in properties:
#         print(f"  PropertyMap: {prop}")
#

def pull_raw():

    # Define the namespace URI you want to explore
    namespace_uri = "http://iec.ch/TC57/2013/CIM-schema-cim16#"

    # Create an RDF graph
    g = Graph()

    # Fetch the RDF data associated with the namespace
    g.load(namespace_uri)

    # Print the entire RDF graph
    print("Raw RDF Data:")
    print(g.serialize(format="turtle").decode())

    # Explore the RDF graph
    print("\nExplored RDF Data:")
    for subj, pred, obj in g:
        print(f"Subject: {subj}, Predicate: {pred}, Object: {obj}")


def pull_raw2():

    # Define the namespace URI you want to explore
    namespace_uri = "http://iec.ch/TC57/2012/CIM-schema-cim17#"
    namespace_uri = "http://iec.ch/TC57/2013/CIM-schema#"
    namespace_uri = "http://iec.ch/TC57/CIM#"
    namespace_uri = "http://iec.ch/TC57/2013/CIM-schema-cim16#"
    "http://iec.ch/TC57/CIM#"
    # Create an RDF graph
    g = Graph()

    # Fetch the RDF data associated with the namespace using requests
    response = requests.get(namespace_uri)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the RDF data from the response content
        g.parse(data=response.text, format="turtle")

        # Print the entire RDF graph
        print("Raw RDF Data:")
        print(g.serialize(format="turtle").decode())

        # Explore the RDF graph
        print("\nExplored RDF Data:")
        for subj, pred, obj in g:
            print(f"Subject: {subj}, Predicate: {pred}, Object: {obj}")
    else:
        print(f"Failed to fetch RDF data. Status code: {response.status_code}")


if __name__ == "__main__":
    pull_raw2()