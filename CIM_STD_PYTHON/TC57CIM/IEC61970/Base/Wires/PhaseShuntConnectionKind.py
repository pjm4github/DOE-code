# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
from enum import Enum

class PhaseShuntConnectionKind(Enum):
    """
    The configuration of phase connections for a single terminal device such as a
    load or capacitor.
    """
    
    D = "Delta connection."
    Y = "Wye connection."
    Yn = "Wye, with neutral brought out for grounding."
    I = "Independent winding, for single-phase connections."
    G = "Ground connection; use when explicit connection to ground needs to be expressed in combination with the phase code, such as for electrical wire/cable or for meters."

