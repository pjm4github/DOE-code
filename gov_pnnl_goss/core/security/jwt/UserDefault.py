
from collections import abc

from gov_pnnl_goss.SpecialClasses import AuthenticationToken


class UserDefault(AuthenticationToken):
    
    def get_roles(self):
        roles = set()
        roles.add("default")
        return roles
