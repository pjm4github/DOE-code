#######################################################
# 
# EnergyComponent.py
# Python implementation of the Class EnergyComponent
# Generated by Enterprise Architect
# Created on:      17-Dec-2023 11:54:29 PM
# Original author: selaost1
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61970.InfIEC61970.EnergyArea.EnergyGroup import EnergyGroup
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.IdentifiedObject import IdentifiedObject

class EnergyComponent(IdentifiedObject):
    m_EnergyGroup= EnergyGroup()