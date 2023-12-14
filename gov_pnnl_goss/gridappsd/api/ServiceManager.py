from abc import ABC, abstractmethod
from msilib.schema import File
from typing import Dict, List


class ServiceInfo:
    # Define the ServiceInfo class as needed, including attributes for service configuration
    pass


class ServiceInstance:
    # Define the ServiceInstance class as needed, including attributes for service instances
    pass


class SimulationContext:
    # Define the SimulationContext class as needed, including attributes for simulation context
    pass


class UserOptions:
    # Define the UserOptions class as needed, including attributes for user options
    pass


class ServiceManager(ABC):

    @abstractmethod
    def register_service(self, service_info: ServiceInfo, service_package) -> None:
        """
        Register a new service with GridAPPS-D Service manager.

        Args:
            service_info (ServiceInfo): Service info object with service configuration.
            service_package (Serializable): Serializable service package.
        """
        pass

    @abstractmethod
    def list_services(self) -> List[ServiceInfo]:
        """
        List the currently registered services.

        Returns:
            List[ServiceInfo]: List of ServiceInfo objects describing the configurations of the registered services.
        """
        pass

    @abstractmethod
    def get_service(self, service_id: str) -> ServiceInfo:
        """
        Get service configuration for the requested service ID.

        Args:
            service_id (str): Registered ID of the desired service.

        Returns:
            ServiceInfo: ServiceInfo object containing service configuration.
        """
        pass

    @abstractmethod
    def get_service_id_for_instance(self, service_instance_id: str) -> str:
        """
        Get service ID for a service instance ID.

        Args:
            service_instance_id (str): Instance ID of a running or ran service.

        Returns:
            str: Service ID for the passed instance ID.
        """
        pass

    @abstractmethod
    def de_register_service(self, service_id: str) -> None:
        """
        Unregister a service with the requested ID.

        Args:
            service_id (str): Registered ID of the service to de-register.
        """
        pass

    @abstractmethod
    def start_service(self, service_id: str, runtime_options: Dict[str, any]) -> str:
        """
        Start a service instance.

        Args:
            service_id (str): Registered ID of the desired service.
            runtime_options (Dict[str, any]): Runtime options for the service instance.

        Returns:
            str: String containing the service instance ID or None if the service is already started for that simulation.
        """
        pass

    @abstractmethod
    def start_service_for_simulation(self, service_id: str, runtime_options: Dict[str, any], simulation_context: Dict[str, any]) -> str:
        """
        Start a service instance for a simulation.

        Args:
            service_id (str): Registered ID of the desired service.
            runtime_options (Dict[str, any]): Runtime options for the service instance.
            simulation_context (Dict[str, any]): Simulation context.

        Returns:
            str: String containing the service instance ID or None if the service is already started for that simulation.
        """
        pass

    @abstractmethod
    def stop_service(self, service_id: str) -> None:
        """
        Stops all instances of the service with the requested service ID.

        Args:
            service_id (str): Registered ID of the service to stop.
        """
        pass

    @abstractmethod
    def list_running_services(self) -> List[ServiceInstance]:
        """
        List currently running service instances.

        Returns:
            List[ServiceInstance]: List of ServiceInstance objects.
        """
        pass

    @abstractmethod
    def list_running_services_for_simulation(self, service_id: str, simulation_id: str) -> List[ServiceInstance]:
        """
        List currently running service instances for the requested service ID and simulation ID.

        Args:
            service_id (str): Registered ID of the service to list.
            simulation_id (str): ID of the simulation.

        Returns:
            List[ServiceInstance]: List of ServiceInstance objects.
        """
        pass

    @abstractmethod
    def stop_service_instance(self, instance_id: str) -> None:
        """
        Stop a service instance.

        Args:
            instance_id (str): ID of the service instance to stop.
        """
        pass

    @abstractmethod
    def get_service_config_directory(self) -> File:
        """
        Get the directory where the service configurations are stored.

        Returns:
            File: File location of the directory containing service configurations.
        """
        pass
