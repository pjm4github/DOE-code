# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 on Fri Dec 15 17:35:24 2023
from enum import Enum

class PhaseConnectedFaultKind(Enum):
    line_to_ground = 1  # The fault connects the indicated phases to ground
    line_to_line = 2  # The fault connects the specified phases together without a connection to ground
    line_to_line_to_ground = 3  # The fault connects the indicated phases to ground and to each other
