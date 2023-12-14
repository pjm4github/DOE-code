
from typing import Set

from gov_pnnl_goss.core.security.impl.GossAuthorizingRealm import Realm


class GossRealm(Realm):
    
    def get_permissions(self, identifier: str) -> Set[str]:
        pass
    
    def has_identifier(self, identifier: str) -> bool:
        pass
