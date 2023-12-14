class ModelState:
    def __init__(self, synchronous_machines=None, switches=None):
        if synchronous_machines is None:
            synchronous_machines = []
        if switches is None:
            switches = []
        self.synchronous_machines = synchronous_machines
        self.switches = switches

    def get_synchronous_machines(self):
        return self.synchronous_machines

    def set_synchronous_machines(self, synchronous_machines):
        self.synchronous_machines = synchronous_machines

    def get_switches(self):
        return self.switches

    def set_switches(self, switches):
        self.switches = switches
