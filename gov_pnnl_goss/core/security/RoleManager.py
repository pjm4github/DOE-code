
# role_manager.py

from typing import List, Set

class RoleManager:
    
    def get_role_permissions(self, role_name: str) -> Set[str]:
        raise NotImplementedError

    def get_role_permissions_bulk(self, role_names: List[str]) -> Set[str]:
        raise NotImplementedError

    def get_all_roles(self) -> Set[str]:
        raise NotImplementedError

    # def get_roles(self, user_name: str) -> List[str]:
    #     raise NotImplementedError
    
    # def has_role(self, user_name: str, role_name: str) -> bool:
    #     raise NotImplementedError
    
    # def add_role(self, user:str, role:str):
    #     # TODO
    #     pass
    
    # def remove_role(self, user:str, role:str):
    #     # TODO
    #     pass
