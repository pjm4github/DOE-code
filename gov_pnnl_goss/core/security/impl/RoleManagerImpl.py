
import logging
# from java.util import Map
# from java.util import Set
# from java.util import HashSet
# from java.util import ConcurrentHashMap
# from java.util import Dictionary
# from org.apache.felix.cm.impl import ConfigurationDependency
import logging

from gov_pnnl_goss.core.security.RoleManager import RoleManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class RoleManagerImpl(RoleManager):
    CONFIG_PID = "pnnl.goss.core.security.rolefile"

    def __init__(self):
        self.logger = LogManager(RoleManagerImpl.__name__)
        self.role_permissions = {}

    # @ConfigurationDependency(pid=CONFIG_PID)
    def updated(self, properties):
        if self.properties is not None:
            self.logger.debug("Updating RoleManagerImpl")
            self.role_permissions.clear()

            keys = properties.keys()
            perms = set()
            for k in keys:
                v = properties.get(k)
                cred_and_permissions = v.split(",")

                for i in range(cred_and_permissions.length):
                    perms.add(cred_and_permissions[i])

                self.role_permissions[k] = perms

    def get_role_permissions(self, role_name):
        if isinstance(role_name, str):
            if role_name in self.role_permissions.keys():
                return self.role_permissions.get(role_name)
            else:
                return None
        else:
            perms = set()
            for role in self.role_names:
                role_perms = self.role_permissions.get(role)
                for p in role_perms:
                    if p not in perms:
                        perms.add(p)

            return perms

    def get_all_roles(self):
        return self.role_permissions.keys()
