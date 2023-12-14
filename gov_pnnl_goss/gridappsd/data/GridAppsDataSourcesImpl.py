# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
from gov_pnnl_goss.SpecialClasses import RuntimeException, SQLException
from gov_pnnl_goss.core.server.DataSourceRegistry import DataSourceRegistry
from gov_pnnl_goss.gridappsd.data.GridAppsDataSources import GridAppsDataSources
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.GridAppsDataSourcesComponentTests import \
    DataSourceBuilder

import logging


class ConnectionPoolDataSource:
    pass


class GridAppsDataSourcesImpl(GridAppsDataSources):

    CONFIG_PID = "pnnl.goss.sql.datasource.gridappsd"
    # DS_NAME = "goss.powergrids"

    def __init__(self, log=None, datasourceBuilder=None, datasourceRegistry=None, datasourceProperties=None):
        self.log = LogManager(GridAppsDataSourcesImpl.__name__)
        self.datasource_builder = datasourceBuilder if datasourceBuilder else DataSourceBuilder()
        self.datasource_registry = datasourceRegistry if datasourceRegistry else DataSourceRegistry()
        self.datasource_properties = datasourceProperties if datasourceProperties else {}

        # #  Eventually to hold more than one connection
        # #  self.pooled_map = {}
        self.pooled_data_source = ConnectionPoolDataSource()

        self.registered_datasources = []

    def get_registered_datasources(self):
        return self.registered_datasources
    
    def start(self):
        self.log.debug("Starting " + self.getClass().getName())
        self.register_data_source()
        # @ConfigurationDependency(pid=CONFIG_PID)

    def updated(self, config):
        properties = {}
        datasource_name = config.get("name")
        if not datasource_name:
            datasource_name = GridAppsDataSourcesImpl.CONFIG_PID
        properties[DataSourceBuilder.DATASOURCE_NAME] = datasource_name
        properties[DataSourceBuilder.DATASOURCE_USER] = config.get("username")
        properties[DataSourceBuilder.DATASOURCE_PASSWORD] = config.get("password")
        properties[DataSourceBuilder.DATASOURCE_URL] = config.get("url")
        properties["driverClassName"] = config.get("driver")
        if self.datasource_properties == None:
            self.datasource_properties = {}
        self.datasource_properties = properties

    def register_data_source(self):
        datasourceName = self.datasource_properties[DataSourceBuilder.DATASOURCE_NAME]
        if not datasourceName:
            raise RuntimeException("No datasource name provided when registering data source")

        if self.datasource_builder and self.registered_datasources:
            try:
                self.datasource_builder[datasourceName] = self.datasource_properties
            except Exception as e:
                # TODO Auto-generated catch block

                # TODO use logmanager to log error
                self.log.error(e)
                print(e)
            self.registered_datasources.extend(datasourceName)

    def stop(self):
        self.log.debug("Stopping " + self.__class__.__name__)
        for s in self.registered_datasources:
            self.datasource_registry.remove(s)
        self.registered_datasources.clear()
    
    def get_data_source_keys(self):
        return self.registered_datasources
    
    def get_data_source_by_key(self, datasourcekey):
        return self.datasource_registry.get(datasourcekey)
    
    def get_connection_by_key(self, key):
        conn = None
        try:
            conn = self.datasource_registry.get(key).getConnection()
        except SQLException as e:
            self.log.error(e)
            print(e)
        return conn

    def set_datasource_builder(self, datasourceBuilder):
        self.datasource_builder = datasourceBuilder

    def set_datasource_registry(self, datasourceRegistry):
        self.datasource_registry = datasourceRegistry
