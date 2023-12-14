
# from concurrent.futures import ConcurrentHashMap
import logging
from typing import Set, Dict

from gov_pnnl_goss.core.security.GossPermissionResolver import GossPermissionResolver
from gov_pnnl_goss.core.security.GossRealm import GossRealm
from gov_pnnl_goss.core.security.SecurityConfig import SecurityConfig
from gov_pnnl_goss.core.security.impl.GossAuthorizingRealm import AuthorizingRealm, SimpleAccount
from gov_pnnl_goss.core.security.impl.SystemRealm import ConcurrentHashMap, UsernamePasswordToken
from gov_pnnl_goss.core.security.jwt.UserDefault import AuthenticationToken
from gov_pnnl_goss.core.security.ldap.GossLDAPRealm import PrincipalCollection, AuthorizationInfo, AuthenticationInfo, \
    PermissionResolver
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


# from org.apache.shiro.authc import UsernamePasswordToken, AuthenticationToken
# from org.apache.shiro.authc import AuthenticationException, AuthenticationInfo
# from org.apache.shiro.authz import AuthorizationInfo
# from org.apache.shiro.realm import AuthorizingRealm
# from org.apache.shiro.subject import PrincipalCollection
# from org.slf4j import Logger, LoggerFactory
# from pnnl.goss.core.security import GossRealm
# from pnnl.goss.core.security import SecurityConfig
# from pnnl.goss.core.security import ServiceDependency, ConfigurationDependency, Start
# from pnnl.goss.core.security import PermissionResolver, GossPermissionResolver


class SystemBasedRealm(AuthorizingRealm, GossRealm):
    
    CONFIG_PID = "pnnl.goss.core.security.systemrealm"

    def __init__(self):
        self.logger = LogManager(SystemBasedRealm.__name__)
        self.user_map: Dict[str, SimpleAccount] = ConcurrentHashMap()
        self.user_permissions: Dict[str, Set[str]] = ConcurrentHashMap()
    
    #@ServiceDependency
    goss_permission_resolver =  GossPermissionResolver
    
    #@ServiceDependency
    security_config =  SecurityConfig
    
    def on_init(self):
        super().on_init()
        perms = set()
        acnt = SimpleAccount(self.security_config.get_manager_user(), 
                             self.security_config.get_manager_password(), 
                             self.get_name())
        acnt.add_string_permission("queue:* ,topic:* ,temp-queue:* ,fusion:*:read ,fusion:*:write")
        perms.add("queue:* ,topic:* ,temp-queue:* ,fusion:*:read ,fusion:*:write")
        self.user_map[self.security_config.get_manager_user()] = acnt
        self.user_permissions[self.security_config.get_manager_user()] = perms
    
    # @Start
    def start(self):
        pass
    
    # @ConfigurationDependency(pid=CONFIG_PID)
    def updated(self, properties: Dict[str, str]):
        pass
    
    def get_authorization_info(self, principals: PrincipalCollection) -> AuthorizationInfo:
        username = self.get_available_principal(principals)
        return self.user_map.get(username)
    
    def get_authentication_info(self, token: AuthenticationToken) -> AuthenticationInfo:
        up_token = UsernamePasswordToken(token)
        up_token.set_remember_me(True)
        return self.user_map.get(up_token.get_username())
    
    def get_permissions(self, identifier: str) -> Set[str]:
        if self.has_identifier(identifier):
            return self.user_permissions.get(identifier)
        else:
            return set()
    
    def has_identifier(self, identifier: str) -> bool:
        return identifier in self.user_map
    
    def get_permission_resolver(self) -> PermissionResolver:
        if self.goss_permission_resolver is not None:
            return self.goss_permission_resolver
        else:
            return super().get_permission_resolver()
