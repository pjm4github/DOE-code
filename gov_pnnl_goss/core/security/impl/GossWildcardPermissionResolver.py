
from gov_pnnl_goss.core.security.GossPermissionResolver import GossPermissionResolver


class WildcardPermissionResolver:
    pass


class ActiveMQWildcardPermission:
    pass


class WildcardPermission:
    pass


class GossWildcardPermissionResolver(WildcardPermissionResolver, GossPermissionResolver):

    # Returns case-sensitive permissions (before it was converting them to lower case)
    '''
    Returns a new WildcardPermission instance constructed based on the specified
    <tt>permission_string</tt>.

    @param permission_string the permission string to convert to a Permission instance.
    @return a new WildcardPermission instance constructed based on the specified
        <tt>permission_string</tt>
    '''
    def resolve_permission(self, permission_string):
        if permission_string is not None and (permission_string.startswith("topic:") or permission_string.startswith("queue:")
                or permission_string.startswith("temp-queue:")):
            return ActiveMQWildcardPermission(permission_string)
        else:
            return WildcardPermission(permission_string, True)
