#######################################################
# 
# CalculationMethodHierarchy.py
# Python implementation of the Class CalculationMethodHierarchy
# Generated by Enterprise Architect
# Created on:      17-Dec-2023 7:05:09 PM
# Original author: herb
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.IdentifiedObject import IdentifiedObject
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Meas.MeasurementValue import MeasurementValue

class CalculationMethodHierarchy(IdentifiedObject):
    """The hierarchy of calculation methods used to derive this measurement.
    """
    MeasurementValue= MeasurementValue()
