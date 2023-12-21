#######################################################
# 
# TypeAssetCatalogue.py
# Python implementation of the Class TypeAssetCatalogue
# Generated by Enterprise Architect
# Created on:      19-Dec-2023 2:11:56 PM
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61968.Common.Status import Status
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.IdentifiedObject import IdentifiedObject


class TypeAssetCatalogue(IdentifiedObject):
    """Catalogue of generic types of assets (TypeAsset) that may be used for design
    purposes. It is not associated with a particular manufacturer.
    """
    def __init__(self):
        super().__init__()
        self.status = Status()