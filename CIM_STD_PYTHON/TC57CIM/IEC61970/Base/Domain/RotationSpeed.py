#######################################################
# 
# RotationSpeed.py
# Python implementation of the Class RotationSpeed
# Generated by Enterprise Architect
# Created on:      16-Dec-2023 11:26:20 PM
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.UnitMultiplier import UnitMultiplier
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.UnitSymbol import UnitSymbol


class RotationSpeed:
    """Number of revolutions per second.
    """
    unit = UnitSymbol.Hz

    def __init__(self):
        self.multiplier = UnitMultiplier.none
        self.value = 0.0
