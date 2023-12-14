import threading
from typing import Any, Dict

# from osgi.constants import Constants
# from osgi.interfaces import ConfigurationException, ManagedServiceFactory
#
# from pnnl.goss.core.server.datasource_builder import DataSourceBuilder
# from pnnl.goss.core.server.datasource_object import DataSourceObject
# from pnnl.goss.core.server.pooled_sql_service_impl import PooledSqlServiceImpl
# from pnnl.goss.core.server.token_identifier_map import TokenIdentifierMap

import configparser

from gov_pnnl_goss.SpecialClasses import ConfigurationException
from gov_pnnl_goss.core.server.DataSourceBuilder import DataSourceBuilder
from gov_pnnl_goss.core.server.DataSourceObject import DataSourceObject
from gov_pnnl_goss.core.server.impl.PooledSqlServiceImpl import PooledSqlServiceImpl


class ConfigurationManager:
    """
    # Example usage:
        config_manager = ConfigurationManager('config.ini')
        db_url = config_manager.get_property('database', 'url')
        if db_url:
            print(functions"Database URL: {db_url}")
        else:
            print("Database URL not found in configuration.")

        # Modify a property and save it
        config_manager.set_property('database', 'url', 'new_db_url')
        config_manager.save()
    """
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_property(self, section, key):
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def set_property(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)

    def save(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)


class PooledSqlServiceFactory(ConfigurationManager):  # ManagedServiceFactory):
    """
    Map of service pid to the actual component.  Note we use long form
    of component because it is different than the annotation component
    used on the top of the class.
    """
    def __init__(self, config_file=None):
        super().__init__(config_file)
        self.dm = None  # DependencyManager
        self.components = {}  # Map of service pid to the actual component

    def get_name(self) -> str:
        return "Pooled Sql Service Factory"

    def is_required_key(self, key: str) -> bool:
        required_keys = [
            DataSourceBuilder.DATASOURCE_USER,
            DataSourceBuilder.DATASOURCE_PASSWORD,
            DataSourceBuilder.DATASOURCE_URL,
            "name"
        ]
        return key in required_keys

    def updated(self, pid: str, properties: Dict[str, Any]) -> None:
        props = {}
        other_props = {}

        for key, value in properties.items():
            if self.is_required_key(key):
                if value is None or value == "":
                    raise ConfigurationException(functions"{key}, Must be specified!")
                props[key] = value
            else:
                if value is not None and value == "":
                    other_props[key] = value

        datasource_driver = "com.mysql.jdbc.Driver"
        if DataSourceBuilder.DATASOURCE_DRIVER in other_props:
            datasource_driver = other_props[DataSourceBuilder.DATASOURCE_DRIVER]
            del other_props[DataSourceBuilder.DATASOURCE_DRIVER]

        service = PooledSqlServiceImpl(
            props["name"],
            props[DataSourceBuilder.DATASOURCE_URL],
            props[DataSourceBuilder.DATASOURCE_USER],
            props[DataSourceBuilder.DATASOURCE_PASSWORD],
            datasource_driver,
            other_props
        )

        c = self.dm.create_component()
        c.set_interface(DataSourceObject, None)
        c.set_implementation(service)

        self.components[pid] = c
        self.dm.add(c)

    def deleted(self, pid: str) -> None:
        self.dm.remove(self.components.pop(pid))


# # Mocking DependencyManager, osgi.constants.Constants, and osgi.interfaces.ConfigurationException
class DependencyManager:
    def __init__(self):
        pass

    def create_component(self):
        return ComponentBuilder()

    def add(self, component):
        pass

    def remove(self, component):
        pass


class ComponentBuilder:
    def __init__(self):
        self.component = None

    def set_interface(self, interface, properties):
        return self

    def set_implementation(self, implementation):
        self.component = implementation
        return self

    def build(self):
        return self.component


if __name__ == "__main__":
    factory = PooledSqlServiceFactory()
    factory.dm = DependencyManager()
    factory.dm.create_component = ComponentBuilder
    factory.updated("test-pid", {
        "name": "test-datasource",
        DataSourceBuilder.DATASOURCE_URL: "jdbc:mysql://localhost:3306/test",
        DataSourceBuilder.DATASOURCE_USER: "test_user",
        DataSourceBuilder.DATASOURCE_PASSWORD: "test_password",
        DataSourceBuilder.DATASOURCE_DRIVER: "com.mysql.cj.jdbc.Driver"
    })

    # Make sure to call `deleted` to properly release resources when needed
    # factory.deleted("test-pid")
