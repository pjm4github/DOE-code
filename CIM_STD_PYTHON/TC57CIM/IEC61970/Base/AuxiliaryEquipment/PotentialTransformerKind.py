# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 on Fri Dec 15 17:00:47 2023
from enum import Enum
from typing import List

class PotentialTransformerKind(Enum):
    inductive = 1  # The potential transformer is using induction coils to create secondary voltage.
    capacitive_coupling = 2  # The potential transformer is using capacitive coupling to create secondary voltage.
