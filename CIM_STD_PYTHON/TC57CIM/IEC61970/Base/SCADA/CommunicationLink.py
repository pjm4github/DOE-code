#######################################################
# 
# CommunicationLink.py
# Python implementation of the Class CommunicationLink
# Generated by Enterprise Architect
# Created on:      17-Dec-2023 7:17:52 PM
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.SCADA.RemoteUnit import RemoteUnit
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.PowerSystemResource import PowerSystemResource
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.ICCPConfiguration.BilateralExchangeActor import BilateralExchangeActor

class CommunicationLink(PowerSystemResource):
    """The connection to remote units is through one or more communication links.
    Reduntant links may exist. The CommunicationLink class inherit
    PowerSystemResource. The intention is to allow CommunicationLinks to have
    Measurements. These Measurements can be used to model link status as
    operational, out of service, unit failure etc.
    """
    # RTUs may be attached to communication links.
    RemoteUnits= RemoteUnit()

    BilateralExchangeActor= BilateralExchangeActor()
