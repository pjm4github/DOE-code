# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 on Fri Dec 15 17:22:57 2023
from enum import Enum

class DcPolarityKind(Enum):
    """
    Polarity for DC circuits.
    @author T. Kostic
    @version 1.0
    @created 15-Dec-2023 4:38:27 PM
    """

    # Positive pole.
    positive = 1

    # Middle pole, potentially grounded.
    middle = 2

    # Negative pole.
    negative = 3
