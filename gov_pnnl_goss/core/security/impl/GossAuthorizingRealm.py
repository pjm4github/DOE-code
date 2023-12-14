
from collections import defaultdict
# from java.lang import String
# from org.apache.shiro.authc import AuthenticationException, AuthenticationToken, UsernamePasswordToken
# from org.apache.shiro.authz import AuthorizationInfo
# from org.apache.shiro.realm import AuthorizingRealm
# from org.apache.shiro.subject import PrincipalCollection
# from org.apache.shiro.authc import SimpleAccount
# from org.apache.shiro.realm import Realm
# from org.osgi.service.component.annotations import Component, ServiceDependency

class SimpleAccount:
    pass


class AuthorizingRealm:
    pass


class Realm:
    pass


class GossAuthorizingRealm(AuthorizingRealm, Realm):

    DEFAULT_SYSTEM_USER = "system"
    account_cache = defaultdict(SimpleAccount)

    def set_security_manager(self, securityManager):
        self.security_manager = securityManager

    def set_security_config(self, securityConfig):
        self.security_config = securityConfig

    def get_permissions_by_role(self, role):
        permissions = set()
        if role == "users":
            permissions.add("queue:*")
            permissions.add("temp-queue:*")
        elif role == "advisory":
            permissions.add("topic:*")  # ctiveMQ.Advisory.*")
        return permissions

    def get_account(self, username, password):
        system_user_name = self.DEFAULT_SYSTEM_USER
        if self.security_config is not None:
            system_user_name = self.security_config.get_manager_user()

        account = None
        default_roles = {"users", "advisory"}

        if username == system_user_name:
            account = SimpleAccount(username, password, self.get_name())
            account.add_role(system_user_name)
            account.add_string_permissions(self.get_permissions_by_role(system_user_name))

        if account is None:
            print(f"Couldn't authenticate on realm: {self.get_name()} for user: {username}")
            return None

        for role in default_roles:
            account.add_role(role)
            account.add_string_permissions(self.get_permissions_by_role(role))

        return account

    def get_authorization_info(self, principals):
        username = str(principals.get_primary())
        return self.account_cache.get(username)

    def get_authentication_info(self, token):
        up_token = token
        return self.get_account(up_token.get_username(), str(up_token.get_password()))

    def is_permitted(self, principals, permission):
        return False
