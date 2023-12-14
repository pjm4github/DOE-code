
# DataSourceObject.py


class DataSourceObject:
    """
    /**
    * The DataSourceObject interface allows the creation of arbitrary objects
    * to be retrieved by name from the DataSourceRegistry.
    *
    * @author Craig Allwardt
    *
    */
    """
    def get_name(self):
        """
        /**
        * The name of the datasource is how the registry will be able to
        * retrieve it from the datastore.
        *
        * @return
        */
        :return:
        """
        pass
    
    def get_data_source_type(self):
        """
        /**
        * Some special handling is available for datasources that are
        * jdbc compliant.  For instance they can have pooled connections
        * by default.
        *
        * @return
        */
        :return:
        """
        pass
