
from collections import defaultdict
from typing import Dict, Set

from pyparsing import ParseException

from gov_pnnl_goss.SpecialClasses import PermissionResolverAware, UnauthTokenBasedRealm
from gov_pnnl_goss.core.GossCoreConstants import GossCoreConstants
from gov_pnnl_goss.core.security.GossRealm import GossRealm
from gov_pnnl_goss.core.security.impl.GossAuthorizingRealm import AuthorizingRealm, SimpleAccount
from gov_pnnl_goss.core.security.impl.SystemRealm import UsernamePasswordToken


# from org.apache.shiro.authc import AuthenticationException, AuthenticationToken
# from org.apache.shiro.authc import SimpleAccount, UsernamePasswordToken
# from org.apache.shiro.authz import AuthorizationInfo
# from org.apache.shiro.authz import PermissionResolver
# from org.apache.shiro.authz import SimpleAuthorizationInfo
# from org.apache.shiro.realm import AuthorizingRealm
# from org.apache.shiro.subject import PrincipalCollection
# from org.apache.shiro.util import PermissionResolverAware
# from org.apache.shiro.util import StringUtils
#
# from pnnl.goss.core.security import GossRealm
# from pnnl.goss.core.security.jwt import JWTAuthenticationToken
# from pnnl.goss.core.security.permission import GossPermissionResolver
# from pnnl.goss.core.security.properties import SecurityConfig
# from pnnl.goss.core.security.properties import RoleManager


import logging

from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


class UnauthTokenBasedRealm(AuthorizingRealm, GossRealm, PermissionResolverAware):
    
    CONFIG_PID = "pnnl.goss.core.security.unauthrealm"
    log = LogManager(UnauthTokenBasedRealm.__name__)
    
    def __init__(self):
        self.token_map = defaultdict(SimpleAccount)
        self.goss_permission_resolver = None
        self.security_config = None
        self.role_manager = None
    
    def updated(self, properties: Dict[str, str]):
        if properties:
            # handle updated properties
            pass
    
    def start(self):
        pass
    
    def get_authorization_info(self, principals):
        username = str(self.get_available_principal(principals))
        account = self.token_map.get(username)
        if account is None:
            self.logger.debug("No authorization info found for %s" % username)
        return account
    
    def get_authentication_info(self, token) -> SimpleAccount:
        up_token = UsernamePasswordToken.cast_(token)
        account = None
        username = up_token.get_username()
        self.logger.info("Get authentication info for %s" % username)
        pw = up_token.get_password()
        if username and len(username) > 250 and not pw:
            verified = self.security_config.validate_token(username)
            self.logger.info("Received token: %s verified: %s" % (username, verified))
            if verified:
                try:
                    # look up permissions based on roles and add them
                    permissions = set()
                    token_obj = self.security_config.parse_token(username)
                    self.logger.info("Has token roles: %s" % token_obj.get_roles())
                    if self.role_manager:
                        permissions = self.role_manager.get_role_permissions(token_obj.get_roles())
                        self.logger.debug("Permissions for user %s: %s" % (username, permissions))
                    else:
                        self.logger.warn("Role manager is null")
                    self.logger.info("Has role permissions: %s" % permissions)
                    account = SimpleAccount(username, "", self.get_name())
                    for perm in permissions:
                        account.add_string_permission(perm)
                    self.token_map[username] = account
                except (ParseException, Exception) as e:
                    print(e)
        else:
            if "system" == username:
                return None
            login_topic = "/topic/" + GossCoreConstants.PROP_TOKEN_QUEUE
            account = SimpleAccount(up_token.get_username(), up_token.get_password(), self.get_name())
            account.add_string_permission("topic:ActiveMQ.Advisory.Connection:create")
            account.add_string_permission("topic:ActiveMQ.Advisory.Queue:create")
            account.add_string_permission("topic:ActiveMQ.Advisory.Consumer.Queue.temp.token_resp." + username)
            account.add_string_permission("topic:ActiveMQ.Advisory.Consumer.Queue.temp.token_resp." + username + "-*")
            account.add_string_permission("topic:" + GossCoreConstants.PROP_TOKEN_QUEUE + ":write")
            account.add_string_permission("topic:" + GossCoreConstants.PROP_TOKEN_QUEUE + ":create")
            account.add_string_permission("queue:temp.token_resp." + username)
            account.add_string_permission("queue:temp.token_resp." + username + "-*")
            self.token_map[username] = account
        return account

    def get_permissions(self, identifier: str) -> Set[str]:
        # I don't believe this is used
        return set()

    def has_identifier(self, identifier: str) -> bool:
        return identifier in self.token_map

    def get_permission_resolver(self):
        if self.goss_permission_resolver:
            return self.goss_permission_resolver
        else:
            return super().get_permission_resolver()
