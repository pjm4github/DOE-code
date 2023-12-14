


class DataSourceRegistry:

    def get(self, key):
        """
        /**
        * Get a DataSourceObject from the registry.  If a key
        * does not exist then this call should return null.
        *
        * @param
        * @param key
        * @return
        */
        :param key:
        :return:
        """
        pass

    def add(self, key, obj):
        """
        /**
        * Adds a DataSourceObject to the registry, making it available for
        * the entire system.
        *
        * @param key
        * @param obj
        */
        :param key:
        :param obj:
        :return:
        """
        pass

    def remove(self, key):
        """
        /**
        * Remove DataSourceObject from the registry.  If the object doesn't
        * exist this function is silent.
        *
        * @param key
        */
        :param key:
        :return:
        """
        pass

    def get_available(self):
        """
        /**
        * Retrieve a map of names-> datasourcetype that can be retrieved
        * by the user to determine capabilities of datasources.
        *
        * @return
        */
        :return:
        """
        pass
