
class DataSourceBuilder:

    def __init__(self):
        # A convienence key that can be used to lookup from jndi or GOSS'status
        # DataSourceRegistry.
        self.DATASOURCE_NAME = "DATASOURCE_NAME"
        # The user parameter should be mapped to this property name.
        self.DATASOURCE_USER = "username"
        # The password parameter should be mapped to this property name.
        self.DATASOURCE_PASSWORD = "password"
        # The url parameter should be mapped to this property name.
        self.DATASOURCE_URL = "url"
        # The driver parameter should be mapped to this property name.
        self.DATASOURCE_DRIVER = "driverClassName"

    def create(self, ds_name, url, user=None, password=None, driver=None):
        """
        * Create a datasource and store it for lookup by dsName.
        *
        * @param dsName
        * @param url
        * @param user
        * @param password
        * @param driver
        * @throws ClassNotFoundException
        * @throws Exception
        :param ds_name:
        :param url:
        :param user:
        :param password:
        :param driver:
        :return:
        """
        if not isinstance(url, str):
            self.create_with_properties(ds_name, properties=url)
        pass

    def create_with_properties(self, ds_name, properties):
        """
        /**
        * Use properties file creation of the datasource.  The properties should have at minimum
        * at minimum a DATASOURCE_NAME, DATASOURCE_USER, DATASOURCE_PASSWORD,
        * DATASOURCE_URL, and a DATASOURCE_DRIVER or the implementor should throw an
        * Exception.
        *
        * @param properties
        * @throws ClassNotFoundException
        * @throws Exception
        */

        :param ds_name:
        :param properties:
        :return:
        """
        pass
