from abc import ABC, abstractmethod


class RoleManager(ABC):
    @abstractmethod
    def get_roles(self, user_name):
        pass

    @abstractmethod
    def has_role(self, user_name, role_name):
        pass

    # TODO
    # def add_role(self, user, role)
    #     pass
    # def remove_role(self, user, role)
    #     pass
