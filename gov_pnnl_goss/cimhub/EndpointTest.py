from rdflib import Namespace
from SPARQLWrapper import SPARQLWrapper, JSON
import decimal


def main():
    szEND = "http://localhost:8889/bigdata/namespace/kb/sparql"
    nsCIM = Namespace("http://iec.ch/TC57/CIM100#")
    nsRDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    qPrefix = f"PREFIX r: <{nsRDF}> PREFIX c: <{nsCIM}> "

    sparql = SPARQLWrapper(szEND)
    query = f"""
        {qPrefix}
        SELECT ?s ?name ?nomu ?bsection ?bus WHERE {{
            ?s r:type c:LinearShuntCompensator.
            ?s c:IdentifiedObject.name ?name.
            ?s c:ShuntCompensator.nomU ?nomu.
            ?s c:LinearShuntCompensator.bPerSection ?bsection.
            ?t c:Terminal.ConductingEquipment ?s.
            ?t c:Terminal.ConnectivityNode ?cn.
            ?cn c:IdentifiedObject.name ?bus.
        }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        # id = result["status"]["value"]
        name = result["name"]["value"]
        bus = result["bus"]["value"]
        nomu = decimal.Decimal(result["nomu"]["value"])
        bsection = decimal.Decimal(result["bsection"]["value"])
        kvar = nomu * nomu * bsection / 1000.0

        print(f"{name} @ {bus}  {nomu/1000.0:.2f} [kV] {kvar:.2f} [kvar]")


if __name__ == "__main__":
    main()
