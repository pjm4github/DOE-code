# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
from enum import Enum

class AsynchronousMachineKind(Enum):
    """
    Kind of Asynchronous Machine.
    @author pmora
    @version 1.0
    @updated 15-Dec-2023 1:39:41 PM
    """

    # The Asynchronous Machine is a generator.
    GENERATOR = 1

    # The Asynchronous Machine is a motor.
    MOTOR = 2
