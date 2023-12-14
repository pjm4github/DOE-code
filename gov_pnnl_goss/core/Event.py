
from enum import Enum

class Event:
    serial_version_UID = -1962993549035537429

    class SeverityType(Enum):
        HIGH = 1
        MEDIUM = 2
        LOW = 3

    def __init__(self):
        self.id = 0
        self.status = ""  # Active, Closed
        self.severity = None
        self.event_type = ""
        self.description = ""
        self.related_event_id = 0

    def get_severity_types(self):
        return [severity_type for severity_type in self.SeverityType]

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_severity(self):
        return self.severity

    def set_severity(self, severity):
        self.severity = severity

    def get_event_type(self):
        return self.event_type

    def set_event_type(self, event_type):
        self.event_type = event_type

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_related_event_id(self):
        return self.related_event_id

    def set_related_event_id(self, related_event_id):
        self.related_event_id = related_event_id
