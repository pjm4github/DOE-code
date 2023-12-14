


class EventsList:
    serial_version_UID = -2783212735188372776

    def __init__(self):
        self.events_list = set()

    def get_events_list(self):
        return self.events_list

    def set_events_list(self, events_list):
        self.events_list = events_list

    def add_event(self, event):
        self.events_list.add(event)
