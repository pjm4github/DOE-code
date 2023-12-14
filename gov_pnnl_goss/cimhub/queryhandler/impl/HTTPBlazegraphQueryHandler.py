import time
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class HTTPBlazegraphQueryHandler:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.mRID = None
        self.use_mRID = False
        self.bTiming = False

    def getEndpoint(self):
        return self.endpoint

    def setEndpoint(self, endpoint):
        self.endpoint = endpoint

    def getFeederSelection(self):
        return self.mRID

    def query(self, szQuery, szTag):
        t1 = time.time()

        if self.use_mRID:
            insertion_point = "WHERE {"
            idx = szQuery.rfind(insertion_point)

            if idx >= 0:
                # print("\dimensions***")
                # print(szQuery)
                # print("***")
                query_text = f"{szQuery[:idx]} {insertion_point} VALUES ?fdrid {{\"{self.mRID}\"}} {szQuery[idx + len(insertion_point):]}"
                # print("Sending " + queryy_text)
                query = prepareQuery(query_text)
            else:
                query = prepareQuery(szQuery)
        else:
            query = prepareQuery(szQuery)

        sparql = Graph()
        sparql.bind("c", DistComponent.nsCIM)
        sparql.bind("rdf", DistComponent.nsRDF)
        sparql.bind("xsd", DistComponent.nsXSD)
        sparql.parse(self.endpoint, format="sparql-results+xml")

        result = sparql.query(query)
        t2 = time.time()

        if self.bTiming:
            print(f"SPARQL Query Time: {t2 - t1:.4f} for {szTag}")

        return result

    def construct(self, szQuery):
        if self.use_mRID:
            insertion_point = "WHERE {"
            idx = szQuery.rfind(insertion_point)

            if idx >= 0:
                query_text = f"{szQuery[:idx]} {insertion_point} VALUES ?fdrid {{\"{self.mRID}\"}} {szQuery[idx + len(insertion_point):]}"
                query = prepareQuery(query_text)
            else:
                query = prepareQuery(szQuery)
        else:
            query = prepareQuery(szQuery)

        sparql = Graph()
        sparql.bind("c", DistComponent.nsCIM)
        sparql.bind("rdf", DistComponent.nsRDF)
        sparql.bind("xsd", DistComponent.nsXSD)
        sparql.parse(self.endpoint, format="sparql-results+xml")

        result = sparql.query(query)
        return result

    def addFeederSelection(self, mRID):
        self.mRID = mRID
        self.use_mRID = True
        return self.use_mRID

    def clearFeederSelections(self):
        self.use_mRID = False
        return self.use_mRID

    def setTiming(self, val):
        self.bTiming = val


if __name__ == "__main__":
    # Example usage:
    handler = HTTPBlazegraphQueryHandler("http://your_blazegraph_endpoint/sparql")
    handler.addFeederSelection("your_feeder_mRID")
    results = handler.query("your_sparql_query", "your_query_tag")
    for row in results:
        print(row)
