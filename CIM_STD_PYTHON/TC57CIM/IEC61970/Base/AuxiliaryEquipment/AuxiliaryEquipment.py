# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 on Fri Dec 15 17:00:47 2023
from datetime import datetime
from typing import Any

class AuxiliaryEquipment:
    """
    AuxiliaryEquipment describe equipment that is not performing any primary
    functions but support for the equipment performing the primary function.
    AuxiliaryEquipment is attached to primary equipment via an association with
    Terminal.
    """
    
    def __init__(self) -> None:
        self.terminal: Any = None  # The Terminal at the equipment where the AuxiliaryEquipment is attached.
        

