# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 on Fri Dec 15 17:22:57 2023
from typing import Optional

from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.DC.ACDCConverter import ACDCConverter
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.DC.CsOperatingModeKind import CsOperatingModeKind
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.DC.CsPpccControlKind import CsPpccControlKind
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.AngleDegrees import AngleDegrees
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.CurrentFlow import CurrentFlow


class CsConverter(ACDCConverter):
    """
    DC side of the current source converter (CSC).
    @author T. Kostic
    @version 1.0
    @created 15-Dec-2023 4:38:26 PM
    """

    def __init__(self) -> None:
        """
        This constructor is empty in the original code and is represented here for consistency.
        """
        super().__init__()

        self.alpha: Optional[AngleDegrees] = None  #: Firing angle, typical value between 10 and 18 degrees for a rectifier. CSC state variable, result from power flow.
        self.gamma: Optional[AngleDegrees] = None  #: Extinction angle. CSC state variable, result from power flow.
        self.max_alpha: Optional[AngleDegrees] = None  #: Maximum firing angle. CSC configuration data used in power flow.
        self.max_gamma: Optional[AngleDegrees] = None  #: Maximum extinction angle. CSC configuration data used in power flow.
        self.max_idc: Optional[CurrentFlow] = None  #: The maximum direct current (Id) on the DC side at which the converter should operate. Converter configuration data use in power flow.
        self.min_alpha: Optional[AngleDegrees] = None  #: Minimum firing angle. CSC configuration data used in power flow.
        self.min_gamma: Optional[AngleDegrees] = None  #: Minimum extinction angle. CSC configuration data used in power flow.
        self.min_idc: Optional[CurrentFlow] = None  #: The minimum direct current (Id) on the DC side at which the converter should operate. CSC configuration data used in power flow.
        self.operating_mode: Optional[CsOperatingModeKind] = None  #: Indicates whether the DC pole is operating as an inverter or as a rectifier. CSC control variable used in power flow.
        self.ppcc_control: Optional[CsPpccControlKind] = None
        self.rated_idc: Optional[CurrentFlow] = None  #: Rated converter DC current, also called IdN. Converter configuration data used in power flow.
        self.target_alpha: Optional[AngleDegrees] = None  #: Target firing angle. CSC control variable used in power flow.
        self.target_gamma: Optional[AngleDegrees] = None  #: Target extinction angle. CSC control variable used in power flow.
        self.target_idc: Optional[CurrentFlow] = None  #: DC current target value. CSC control variable used in power flow.

