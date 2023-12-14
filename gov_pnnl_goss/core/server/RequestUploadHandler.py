
from gov_pnnl_goss.core.server.RequestHandlerInterface import RequestHandlerInterface


class RequestUploadHandler(RequestHandlerInterface):
    
    def get_handler_data_types(self):
        """
        Map all the datatypes that are handled by the handler. Ideally this
        should be full class names with perhaps version information, however this
        is not a requirement. In order for GOSS to understand how to route the
        request however it does need to be unique system-wide.
        
        Example: pnnl.gov.powergrid.Bus.getClass().getName()
        
        @return
        """
        # Returns a map of data types to handler classes
        pass
    
    def upload(self, data_type, data):
        """
        Handle the upload of data and return a response
        
        Args:
            data_type (str): The type of the data
            data (Serializable): The data to be uploaded
        
        Returns:
            Response: The response to the upload
        """
        pass
