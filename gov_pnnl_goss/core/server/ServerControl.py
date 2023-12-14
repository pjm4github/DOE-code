
from gov_pnnl_goss.core.client.GossClient import SystemException


class ServerControl:
    
    def start(self):
        """
        Start the server. During the execution of this method the
        implementor should initialize all properties such that the
        server can receive Request objects and route them to their
        appropriate handlers.
        
        Throws SystemException
        """
        raise SystemException
    
    def stop(self):
        """
        Stop the server. During the execution of this method the
        system should shutdown its method of transport, stop all
        routing, release any tcp resources that it has available
        and change the status of the server to not running.
        
        Throws SystemException
        """
        raise SystemException
    
    def is_running(self):
        """
        A plain status of whether the server is able to route Request
        objects currently.
        
        Returns a boolean
        """
        pass
