#######################################################
# 
# GateInputPin.py
# Python implementation of the Class GateInputPin
# Generated by Enterprise Architect
# Created on:      17-Dec-2023 3:52:36 PM
# Original author: sveinols
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.IdentifiedObject import IdentifiedObject


class GateInputPin(IdentifiedObject):
    """Input pin for a logical gate. The condition described in the input pin will
    give a logical true or false. Result from measurement and calculation are
    converted to a true or false.
    """
    def __init__(self):
        super().__init__()

