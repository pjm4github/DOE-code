
import concurrent.futures


class SecurityManagerRealmHandler:
    def __init__(self):
        self.security_manager = None
        self.realm_map = concurrent.futures.Future()

    def realm_added(self, ref, handler):
        default_instance = self.security_manager
        self.realm_map[ref] = handler
        if default_instance.get_realms() is None:
            default_instance.set_realms(set())
            realms = set()
            for r in self.realm_map.values():
                realms.add(r)
            default_instance.set_realms(realms)
        else:
            default_instance.get_realms().add(handler)

    def realm_removed(self, ref):
        default_instance = self.security_manager
        default_instance.get_realms().remove(self.realm_map[ref])

    def get_permissions(self, identifier):
        perms = set()
        for r in self.realm_map.values():
            perms.update(r.get_permissions(identifier))
        return perms
