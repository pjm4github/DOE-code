#######################################################
# 
# ProtectiveActionCollection.py
# Python implementation of the Class ProtectiveActionCollection
# Generated by Enterprise Architect
# Created on:      17-Dec-2023 6:44:05 PM
# Original author: sveinols
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61970.InfIEC61970.InfSIPS.StageTrigger import StageTrigger
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.IdentifiedObject import IdentifiedObject
from CIM_STD_PYTHON.TC57CIM.IEC61970.InfIEC61970.InfSIPS.ProtectiveAction import ProtectiveAction

class ProtectiveActionCollection(IdentifiedObject):
    """
    A collection of protective actions to protect the integrity of the power system.
    """

    def __init__(self):
        super().__init__()
        self.stage_trigger = StageTrigger()
        self.protective_action = ProtectiveAction()
