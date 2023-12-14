
# from py4j.overwatch import service_dependency, configuration_dependency
# from py4j.core.security import GossRealm
# from py4j.core.security import JndiLdapRealm, GossPermissionResolver
# from java.util import Set, HashSet
# from py4j.core.permissions import PermissionResolver
# from py4j.core.tokens import AuthenticationToken, AuthenticationException
# from py4j.core.authentication import SimpleAuthorizationInfo, PrincipalCollection, AuthorizationInfo, AuthenticationToken
# from java.util import Dictionary
from gov_pnnl_goss.SpecialClasses import JndiLdapRealm, JndiLdapContextFactory, PrincipalCollection, AuthorizationInfo, \
    SimpleAuthorizationInfo, AuthenticationInfo, PermissionResolver

from gov_pnnl_goss.core.security.GossPermissionResolver import GossPermissionResolver
from gov_pnnl_goss.core.security.GossRealm import GossRealm
from gov_pnnl_goss.core.security.jwt.UserDefault import AuthenticationToken


#@ConfigurationDependency(pid="pnnl.goss.core.security.ldap")


class GossLdapRealm(JndiLdapRealm, GossRealm):

    CONFIG_PID = "pnnl.goss.core.security.ldap"

    goss_permission_resolver = GossPermissionResolver

    def __init__(self):
        super().__init__()

        self.set_user_dn_template("uid={0},ou=users,ou=goss,ou=system")

        fac = JndiLdapContextFactory()
        fac.set_url("ldap://localhost:10389")
        self.set_context_factory(fac)

    def get_permissions(self, identifier: str) -> set[str]:
        return set()

    def has_identifier(self, identifier: str) -> bool:
        return False

    def do_get_authorization_info(self, principals: PrincipalCollection) -> AuthorizationInfo:
        info = super().do_get_authorization_info(principals)
        if info is None:
            info = SimpleAuthorizationInfo()
            info.add_role("user")
            info.add_string_permission("queue:*")
            info.add_string_permission("temp-queue:*")
            info.add_string_permission("topic:*")
        return info

    def set_user_dn_template(self, arg0: str):
        super().set_user_dn_template(arg0)

    def do_get_authentication_info(self, token: AuthenticationToken) -> AuthenticationInfo:
        info = super().do_get_authentication_info(token)
        return info

    def supports(self, token: AuthenticationToken) -> bool:
        return super().supports(token)

    def updated(self, properties: dict[str, str]):
        if properties is not None:
            pass  # TODO

    def get_permission_resolver(self) -> PermissionResolver:
        if self.goss_permission_resolver is not None:
            return self.goss_permission_resolver
        else:
            return super().get_permission_resolver()
