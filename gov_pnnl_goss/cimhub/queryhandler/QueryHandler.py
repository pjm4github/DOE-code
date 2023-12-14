#from abc import ABC, abstractmethod
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class QueryHandler:  # (ABC):
    Q_PREFIX = f"PREFIX r: <{DistComponent.nsRDF}> PREFIX c: <{DistComponent.nsCIM}> PREFIX rdf: <{DistComponent.nsRDF}> PREFIX cim: <{DistComponent.nsCIM}> PREFIX xsd:<{DistComponent.nsXSD}> "

#    @abstractmethod
    def query(self, szQuery, szTag):
        pass

#    @abstractmethod
    def construct(self, szQuery):
        pass

#    @abstractmethod
    def add_feeder_selection(self, mRID):
        # TODO: support more than one, return False if not present
        pass

#    @abstractmethod
    def clear_feeder_selections(self):
        pass

#    @abstractmethod
    def get_feeder_selection(self):
        pass
