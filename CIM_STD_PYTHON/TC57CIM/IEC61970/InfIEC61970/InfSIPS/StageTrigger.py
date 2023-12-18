#######################################################
# 
# StageTrigger.py
# Python implementation of the Class StageTrigger
# Generated by Enterprise Architect
# Created on:      17-Dec-2023 3:58:06 PM
# Original author: sveinols
# 
#######################################################
# from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.Boolean import Boolean
# from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Domain.Integer import Integer
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.IdentifiedObject import IdentifiedObject
from CIM_STD_PYTHON.TC57CIM.IEC61970.InfIEC61970.InfSIPS.Gate import Gate

class StageTrigger(IdentifiedObject):
    """Condition that is triggered either by TriggerCondition of by gate condition
    within a stage and has remedial action-s.
    """
    GateArmed= Gate()

    GateComCondition= Gate()

    GateTrigger= Gate()
