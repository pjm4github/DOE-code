
from collections import defaultdict

from gov_pnnl_goss.SpecialClasses import ServiceDependency
from gov_pnnl_goss.core.security.impl.GossAuthorizingRealm import AuthorizingRealm, Realm, SimpleAccount

# from java.util import HashSet
# from java.util.concurrent import ConcurrentHashMap
# from org.apache.shiro.authc import AuthenticationException, UsernamePasswordToken
# from org.apache.shiro.authc import AuthenticationToken
# from org.apache.shiro.authc import SimpleAccount
# from org.apache.shiro.realm import AuthorizingRealm
# from org.apache.shiro.subject import PrincipalCollection
# from org.apache.shiro.authz import AuthorizationInfo
# from org.apache.shiro.authz.permission import PermissionResolver
# from org.apache.shiro.permission import Permission
# from org.apache.shiro.realm import Realm
# from org.apache.shiro.subject import PrincipalCollection
# from org.slf4j import Logger, LoggerFactory
# from osgi.annotation import Component, ConfigurationDependency, ServiceDependency
# from java.util import Dictionary
# from java.lang import String
# from java.util import Set, Enumeration

import logging

from gov_pnnl_goss.core.security.impl.SystemRealm import ConcurrentHashMap, UsernamePasswordToken
from gov_pnnl_goss.core.security.jwt.UserDefault import AuthenticationToken
from gov_pnnl_goss.core.security.ldap.GossLDAPRealm import PrincipalCollection, AuthorizationInfo, AuthenticationInfo, \
    PermissionResolver
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class PropertyBasedRealm(AuthorizingRealm, Realm):
    
    CONFIG_PID = "pnnl.goss.core.security.propertyfile"

    def __init__(self):
        self.logger = LogManager(PropertyBasedRealm.__name__)

        self.user_map = ConcurrentHashMap()
        self.user_permissions = ConcurrentHashMap()

        self.goss_permission_resolver = ServiceDependency()

    def doGetAuthorizationInfo(self, principals: PrincipalCollection) -> AuthorizationInfo:
        username = principals.primary_principal
        return self.user_map.get(username)

    def doGetAuthenticationInfo(self, token: AuthenticationToken) -> AuthenticationInfo:
        up_token = UsernamePasswordToken.cast(token)
        return self.user_map.get(up_token.username)

    # @ConfigurationDependency(pid=CONFIG_PID)
    def updated(self, properties: dict[str, object]):
        if properties:
            self.logger.debug("Updating PropertyBasedRealm")
            self.user_map.clear()
            self.user_permissions.clear()
            
            keys = properties.keys()
            for k in keys:
                v = properties.get(k)
                cred_and_permissions = v.split(',')

                acnt = SimpleAccount(k, cred_and_permissions[0], self.get_name())
                perms = set()
                for i in range(1, len(cred_and_permissions)):
                    acnt.add_string_permission(cred_and_permissions[i])
                    perms.add(cred_and_permissions[i])

                self.user_map.put(k, acnt)
                self.user_permissions.put(k, perms)

    def get_permissions(self, identifier: str) -> set[str]:
        if self.has_identifier(identifier):
            return self.user_permissions.get(identifier)
        else:
            return set()

    def has_identifier(self, identifier: str) -> bool:
        return self.user_map.contains_key(identifier)

    def get_permission_resolver(self) -> PermissionResolver:
        if self.goss_permission_resolver:
            return self.goss_permission_resolver
        else:
            return super().get_permission_resolver()
