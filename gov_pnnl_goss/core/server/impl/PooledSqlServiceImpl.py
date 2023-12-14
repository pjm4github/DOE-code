
import logging
import os
from typing import Dict

from gov_pnnl_goss.SpecialClasses import SQLException
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class PooledSqlServiceImpl:

    def __init__(self, datasource_name: str, url: str, username: str, password: str, driver: str, other_properties: Dict[str, str]):
        self.logger = LogManager(PooledSqlServiceImpl.__name__)
        self.name = datasource_name
        self.url = url
        self.password = password
        self.driver_class = driver
        self.username = username
        self.customizations = other_properties
        self.create_data_source()
        self.data_source = None  # DataSource()

    def create_data_source(self):
        properties_for_data_source = {
            "username": self.username,
            "password": self.password,
            "url": self.url,
            "driverClassName": self.driver_class
        }
        properties_for_data_source.update(self.customizations)

        if "maxOpenPreparedStatements" not in properties_for_data_source:
            properties_for_data_source["maxOpenPreparedStatements"] = "10"

        self.logger.debug("Creating datasource: %status, User: %status, URL: %status", self.name, self.username, self.url)

        try:
            if not isinstance(properties_for_data_source["driverClassName"], classmethod):
                raise Exception("Non existent class")
            # self.data_source = BasicDataSourceFactory.createDataSource(properties_for_data_source)
            self.data_source = properties_for_data_source
        except Exception as e:
            self.data_source = None

    def get_name(self) -> str:
        return self.name

    def get_data_source_type(self):
        return "DS_TYPE_JDBC"

    def get_connection(self):
        if self.data_source is None:
            raise SQLException("Invalid datasource.")
        return self.data_source.getConnection()
