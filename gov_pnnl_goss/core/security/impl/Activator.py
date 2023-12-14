
# from org.osgi.service.component import ComponentContext
# from org.osgi.service.component import ComponentConstants
# from org.osgi.service.component import DependencyActivatorBase
# from org.osgi.service.component import ServiceComponent
# from org.osgi.service.component import ServiceComponentFactory
import logging

from gov_pnnl_goss.core.security.SecurityConfig import SecurityConfig
from gov_pnnl_goss.core.security.impl.SecurityConfigImpl import SecurityConfigImpl
from gov_pnnl_goss.core.security.impl.SecurityManagerImpl import SecurityManagerImpl
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class DependencyActivatorBase:
    pass


class SecurityManager:
    pass


class Activator(DependencyActivatorBase):

    def __init__(self, context, manager):
        self.init(context, manager)

    def init(self, context, manager):
        self.manager = manager
        self.logger = LogManager(Activator.__name__)
        self.config_pid = "pnnl.goss.security"
        
        security_config = self.manager.createComponent()
        security_config.setInterface(SecurityConfig.getclass.getName(), None)
        security_config.setImplementation(SecurityConfigImpl)
        security_config.add(self.manager.createConfigurationDependency().setPid(self.config_pid))

        security_manager = self.manager.createComponent()
        security_manager.setInterface(SecurityManager.get_class.getName(), None)
        security_manager.setImplementation(SecurityManagerImpl)
        security_manager.add(self.manager.createConfigurationDependency().setPid(self.config_pid))

        self.manager.add(security_config)
        self.manager.add(security_manager)

    def destroy(self, context, manager):
        raise NotImplementedError
