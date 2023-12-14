from abc import ABC, abstractmethod
from typing import List, Dict

from gov_pnnl_goss.gridappsd.dto.AppInfo import AppInfo


class AppInstance:
    def __init__(self, instance_id: str, app_id: str):
        self.instance_id = instance_id
        self.app_id = app_id


class AppManager(ABC):
    @abstractmethod
    def process(self, process_id: str, event, message) -> None:
        """
        Process application request.

        Args:
            process_id (str): The process ID.
            event: DataResponse event.
            message: Serializable message.

        Raises:
            Exception: If an error occurs during processing.
        """
        pass

    @abstractmethod
    def register_app(self, app_info: AppInfo, app_package: bytes) -> None:
        """
        Register a new app with GridAPPS-D app manager.

        Args:
            app_info (AppInfo): App info object containing app configuration.
            app_package (bytes): Byte array representing the application package.

        Raises:
            Exception: If an error occurs during registration.
        """
        pass

    @abstractmethod
    def list_apps(self) -> List[AppInfo]:
        """
        List currently registered apps.

        Returns:
            List[AppInfo]: List of AppInfo objects describing registered apps.
        """
        pass

    @abstractmethod
    def list_running_apps(self) -> List[AppInstance]:
        """
        List currently running app instances.

        Returns:
            List[AppInstance]: List of AppInstance objects representing running instances.
        """
        pass


    @abstractmethod
    def list_running_apps_by_id(self, app_id: str) -> List[AppInstance]:
        """
        List currently running instances of a specific app by its ID.

        Args:
            app_id (str): Registered ID of the desired app.

        Returns:
            List[AppInstance]: List of AppInstance objects for the specified app.
        """
        pass

    @abstractmethod
    def get_app(self, app_id: str) -> AppInfo:
        """
        Get app configuration for the requested app ID.

        Args:
            app_id (str): Registered ID of the desired app.

        Returns:
            AppInfo: AppInfo object containing app configuration.
        """
        pass

    @abstractmethod
    def get_app_id_for_instance(self, app_instance_id: str) -> str:
        """
        Get the application ID for the specified app instance ID.

        Args:
            app_instance_id (str): Instance ID of the application.

        Returns:
            str: Application ID.
        """
        pass

    @abstractmethod
    def de_register_app(self, app_id: str) -> None:
        """
        Unregister an app by its ID.

        Args:
            app_id (str): Registered ID of the app to de-register.
        """
        pass

    @abstractmethod
    def start_app(self, app_id: str, runtime_options: str, request_id: str) -> str:
        """
        Start an app instance.

        Args:
            app_id (str): Registered ID of the desired app.
            runtime_options (str): Runtime options for the app instance.
            request_id (str): Unique request ID.

        Returns:
            str: App instance ID.
        """
        pass

    @abstractmethod
    def start_app_for_simulation(self, app_id: str, runtime_options: str, simulation_context: Dict) -> str:
        """
        Start an app instance for a simulation.

        Args:
            app_id (str): Registered ID of the desired app.
            runtime_options (str): Runtime options for the app instance.
            simulation_context (Dict): Dictionary containing simulation context.

        Returns:
            str: App instance ID.
        """
        pass

    @abstractmethod
    def stop_app(self, app_id: str) -> None:
        """
        Stop all instances of the app with the specified ID.

        Args:
            app_id (str): Registered ID of the app to stop.
        """
        pass

    @abstractmethod
    def stop_app_instance(self, instance_id: str) -> None:
        """
        Stop a specific app instance by its instance ID.

        Args:
            instance_id (str): ID of the app instance to stop.
        """
        pass

    @abstractmethod
    def get_app_config_directory(self) -> str:
        """
        Get the directory where app configurations are stored.

        Returns:
            str: File location of the directory containing app configurations.
        """
        pass
