#######################################################
# 
# DuctBank.py
# Python implementation of the Class DuctBank
# Generated by Enterprise Architect
# Created on:      19-Dec-2023 11:23:21 AM
# 
#######################################################

from CIM_STD_PYTHON.TC57CIM.IEC61968.Assets.AssetContainer import AssetContainer

class DuctBank(AssetContainer):
    """A duct contains individual wires in the layout as specified with associated
    wire spacing instances; number of them gives the number of conductors in this
    duct.
    """
    def __init__(self):
        super().__init__()
        self.circuit_count = 0