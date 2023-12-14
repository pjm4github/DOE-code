

from gov_pnnl_goss.core import Client, ClientFactory
from gov_pnnl_goss.core.client.GossClient import Protocol


class ClientCommands:

    def __init__(self, factory: ClientFactory):
        self.factory = factory

    def make_openwire(self):
        try:
            print("Making openwire client")
            client = self.factory.create(Protocol.OPENWIRE, None, False)
            print("Client is null? ", client is None)
            client.close()
        except Exception as e:
            print(f"Openwire client creation failed: {e}")

    def make_stomp(self):
        try:
            print("Making stomp client")
            client = self.factory.create(Protocol.STOMP, None, False)
            print("Client is null? ", client is None)
            client.close()
        except Exception as e:
            print(f"Stomp client creation failed: {e}")

    def list(self):
        client_map = self.factory.list()
        for it in client_map.keySet().iterator():
            key = it.next()
            print("ClientId: ", key, "; protocol: ", client_map.get(key))
