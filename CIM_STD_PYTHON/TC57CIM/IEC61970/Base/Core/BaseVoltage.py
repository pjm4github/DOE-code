#######################################################
# 
# BaseVoltage.py
# Python implementation of the Class BaseVoltage
# Generated by Enterprise Architect
# Created on:      16-Dec-2023 4:33:33 PM
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.Voltage import Voltage
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.ConductingEquipment import ConductingEquipment
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.IdentifiedObject import IdentifiedObject

class BaseVoltage(IdentifiedObject):
    """Defines a system base voltage which is referenced.
    """
    # All conducting equipment with this base voltage.  Use only when there is no
    # voltage level container used and only one base voltage applies.  For example,
    # not used for transformers.
    ConductingEquipment= ConductingEquipment()
    def __init__(self):
        super().__init__()
        self.nominal_voltage = Voltage()
