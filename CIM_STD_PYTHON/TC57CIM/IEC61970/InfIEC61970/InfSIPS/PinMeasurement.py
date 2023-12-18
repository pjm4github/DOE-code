#######################################################
# 
# PinMeasurement.py
# Python implementation of the Class PinMeasurement
# Generated by Enterprise Architect
# Created on:      17-Dec-2023 6:38:13 PM
# Original author: sveinols
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Meas.Measurement import Measurement
from CIM_STD_PYTHON.TC57CIM.IEC61970.InfIEC61970.InfSIPS.GateInputPin import GateInputPin

class PinMeasurement(GateInputPin):
    """Gate input pin that is associated with a Measurement or a calculation of
    Measurement.
    """
    Measurement= Measurement()