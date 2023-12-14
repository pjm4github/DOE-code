
class RequestSimulationResponse:
    serial_version_UID = 6306119544266941758

    def __init__(self):
        self.simulation_id = None
        self.events = None
        
    def get_simulation_id(self):
        return self.simulation_id
        
    def set_simulation_id(self, simulation_id):
        self.simulation_id = simulation_id
        
    def get_events(self):
        return self.events
        
    def set_events(self, events):
        self.events = events
