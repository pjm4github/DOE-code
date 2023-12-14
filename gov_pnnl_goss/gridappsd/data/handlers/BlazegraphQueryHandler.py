from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON


class BlazegraphQueryHandler:
    DEFAULT_ENDPOINT = "http://blazegraph:8080/bigdata/namespace/kb/sparql"
    nsCIM = "http://iec.ch/TC57/CIM100#"
    nsRDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    nsXSD = "http://www.w3.org/2001/XMLSchema#"

    def __init__(self, endpoint, log_manager, process_id, username):
        self.endpoint = endpoint
        self.use_mRID = False
        self.logger = log_manager
        self.process_id = process_id
        self.username = username
        self.mRID = None

    def get_endpoint(self):
        return self.endpoint

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def get_log_manager(self):
        return self.logger

    def set_log_manager(self, log_manager):
        self.logger = log_manager

    def query(self, sz_query, sz_tag):
        self.logger.debug("RUNNING", self.process_id, f"Executing query {sz_query}")

        start = datetime.now()
        if self.mRID is not None and len(self.mRID.strip()) > 0:
            insertion_point = "WHERE {"
            idx = sz_query.rfind(insertion_point)
            if idx >= 0:
                buf = (
                    f"{sz_query[:idx]}{insertion_point} VALUES ?fdrid {{\"{self.mRID}\"}} "
                    f"{sz_query[idx + len(insertion_point):]}"
                )
                sz_query = f"{buf}"
            else:
                sz_query = f"{sz_query}"
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(sz_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        end = datetime.now()
        self.logger.debug("RUNNING", self.process_id,
                               f"Query execution took: {(end - start).total_seconds() * 1000} ms")
        return results

    def construct(self, sz_query):
        self.logger.debug("RUNNING", self.process_id, f"Executing query {sz_query}")

        start = datetime.now()
        if self.mRID is not None and len(self.mRID.strip()) > 0:
            insertion_point = "WHERE {"
            idx = sz_query.rfind(insertion_point)
            if idx >= 0:
                buf = (
                    f"{sz_query[:idx]}{insertion_point} VALUES ?fdrid {{\"{self.mRID}\"}} "
                    f"{sz_query[idx + len(insertion_point):]}"
                )
                sz_query = f"{buf}"
            else:
                sz_query = f"{sz_query}"
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(sz_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        end = datetime.now()
        self.logger.debug("RUNNING", self.process_id,
                               f"Query execution took: {(end - start).total_seconds() * 1000} ms")
        return results

    def add_feeder_selection(self, mRID):
        self.mRID = mRID
        self.use_mRID = True
        return self.use_mRID

    def clear_feeder_selections(self):
        self.use_mRID = False
        return self.use_mRID

    def get_feeder_selection(self):
        return self.mRID
