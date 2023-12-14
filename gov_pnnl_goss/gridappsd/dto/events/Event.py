# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import json
from typing import Union


class Event:
    serial_version_UID = -5940543607543814505

    def __init__(self):
        self.fault_mrid: Union[str, None] = None
        self.event_type: Union[str, None] = None
        self.occured_date_time: Union[int, None] = None
        self.stop_date_time: Union[int, None] = None

    def get_fault_mrid(self) -> Union[str, None]:
        return self.fault_mrid

    def set_fault_mrid(self, fault_mrid: Union[str, None]) -> None:
        self.fault_mrid = fault_mrid

    def get_event_type(self) -> Union[str, None]:
        return self.event_type

    def set_event_type(self, event_type: Union[str, None]) -> None:
        self.event_type = event_type

    def get_time_initiated(self) -> Union[int, None]:
        return self.occured_date_time

    def set_time_initiated(self, time_initiated: Union[int, None]) -> None:
        self.occured_date_time = time_initiated

    def get_time_cleared(self) -> Union[int, None]:
        return self.stop_date_time

    def set_time_cleared(self, time_cleared: Union[int, None]) -> None:
        self.stop_date_time = time_cleared

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string: str) -> 'Event':
        event_dict = json.loads(json_string)
        event = Event()
        for key, value in event_dict.items():
            setattr(event, key, value)

        if event.occured_date_time is None or event.stop_date_time is None:
            raise ValueError("Expected attribute timeInitiated or timeCleared is not found")

        if event.occured_date_time <= event.stop_date_time:
            raise ValueError("occuredDateTime cannot be less or equal to stopDateTime for an event")

        return event
