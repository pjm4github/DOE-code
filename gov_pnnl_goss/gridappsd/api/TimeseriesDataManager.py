
from abc import ABC, abstractmethod


class TimeseriesDataManager(ABC):

    @abstractmethod
    def query(self, request_timeseries_data):
        """
        Query timeseries data
        """
        pass

    @abstractmethod
    def store_simulation_output(self, simulation_id):
        """
        Store simulation output
        """
        pass

    @abstractmethod
    def store_simulation_input(self, simulation_id):
        """
        Store simulation input
        """
        pass

    @abstractmethod
    def store_service_output(self, simulation_id, service_id, instance_id):
        """
        Store service output
        """
        pass

    @abstractmethod
    def store_service_input(self, simulation_id, service_id, instance_id):
        """
        Store service input
        """
        pass

    @abstractmethod
    def store_app_output(self, simulation_id, app_id, instance_id):
        """
        Store app output
        """
        pass

    @abstractmethod
    def store_app_input(self, simulation_id, app_id, instance_id):
        """
        Store app input
        """
        pass

    @abstractmethod
    def store_all_data(self, simulation_context):
        """
        Store all data
        """
        pass
