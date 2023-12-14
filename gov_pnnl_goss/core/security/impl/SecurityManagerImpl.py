
import logging

from gov_pnnl_goss.SpecialClasses import SystemException
from gov_pnnl_goss.core.security.GossSecurityManager import GossSecurityManager
from gov_pnnl_goss.core.security.impl.SystemRealm import SystemRealm
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


# from java.util import Dictionary
# from java.util import HashSet
# from java.util import Set
# from org.apache.shiro import SecurityUtils
# from org.apache.shiro.realm import Realm
# from org.slf4j import LoggerFactory
# from pnnl.goss.core.security.api import GossSecurityManager
# from pnnl.goss.core.security.internal import DefaultActiveMqSecurityManager
# from pnnl.goss.core.security.internal import SystemRealm
# from pnnl.goss.core.exception import SystemException


class DefaultActiveMqSecurityManager:
    pass


class SecurityUtils:
    pass


class SecurityManagerImpl(DefaultActiveMqSecurityManager, GossSecurityManager):
    def __init__(self):
        self.logger = LogManager(SecurityManagerImpl.__name__)
        self.properties = None

    def updated(self, properties):
        if properties is not None:
            self.properties = properties

            system_manager = self.get_property("PROP_SYSTEM_MANAGER", None)
            system_manager_password = self.get_property("PROP_SYSTEM_MANAGER_PASSWORD", None)

            try:
                default_realm = SystemRealm(system_manager, system_manager_password)
                realms = set()
                realms.add(default_realm)
                self.set_realms(realms)
                SecurityUtils.set_security_manager(self)
            except Exception as e:
                print(e)
        else:
            self.logger.error("No core config properties received by security activator")
            raise SystemException("No security config properties received by activator", None)

    def get_property(self, key, default_value):
        ret_value = default_value
        if key is not None and key and self.properties.get(key):
            value = self.properties.get(key).toString()
            if not value.startswith("${"):
                ret_value = value

        return ret_value
