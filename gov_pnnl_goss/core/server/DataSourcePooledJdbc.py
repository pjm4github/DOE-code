
# Assuming DataSourceObject is defined in another file
from gov_pnnl_goss.core.server.DataSourceObject import DataSourceObject


class DataSourcePooledJdbc(DataSourceObject):
    
    def get_connection(self):
        pass
