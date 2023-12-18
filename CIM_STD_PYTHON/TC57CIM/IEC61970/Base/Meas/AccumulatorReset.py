# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 on Fri Dec 15 17:38:50 2023
from datetime import datetime
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Meas import AccumulatorValue, Control

class AccumulatorReset(Control):

    # The accumulator value that is reset by the command.
    accumulator_value: AccumulatorValue

    def __init__(self) -> None:
        pass

    def finalize(self) -> None:
        super().finalize()

