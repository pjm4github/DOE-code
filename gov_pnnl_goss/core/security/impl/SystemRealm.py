
# from collections import ConcurrentHashMap
# from org.apache.shiro.authc import UsernamePasswordToken
# from org.apache.shiro.authc import AuthenticationToken
# from org.apache.shiro.authc import AuthenticationException
# from org.apache.shiro.authc import SimpleAccount
# from org.apache.shiro.authc import AuthorizationInfo
# from org.apache.shiro.authc import PrincipalCollection
# from org.apache.shiro.realm import AuthorizingRealm
# from org.apache.shiro.realm import Realm
from gov_pnnl_goss.SpecialClasses import UsernamePasswordToken
from gov_pnnl_goss.core.security.impl.GossAuthorizingRealm import AuthorizingRealm, Realm, SimpleAccount


class ConcurrentHashMap(dict):
    def __init__(self, d=None):
        super().__init__()
        self._dict = {} if not d else d

    def put(self, k, v):
        self._dict[k] = v

    def get(self, k, default=""):
        v = self._dict.get(k,default)
        return v


class SystemRealm(AuthorizingRealm, Realm):
    
    def __init__(self, system_username, system_password):
        self.accnt_map = ConcurrentHashMap()
        if not system_password:
            raise Exception("Invalid system password")
        if not system_username:
            raise Exception("Invalid system username")
        accnt = SimpleAccount(system_username, system_password, self.getName())
        accnt.addStringPermission("*")
        self.accnt_map.put(system_username, accnt)
        
    def do_get_authorization_info(self, principals):
        username = self.getAvailablePrincipal(principals)
        if self.accnt_map.containsKey(username):
            return self.accnt_map.get(username)
        return None
        
    def do_get_authentication_info(self, token):
        up_token = UsernamePasswordToken(token)
        return self.accnt_map.get(up_token.getUsername())
