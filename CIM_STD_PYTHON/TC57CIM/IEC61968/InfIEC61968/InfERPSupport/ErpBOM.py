#######################################################
# 
# ErpBOM.py
# Python implementation of the Class ErpBOM
# Generated by Enterprise Architect
# Created on:      19-Dec-2023 4:08:01 PM
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61968.InfIEC61968.InfERPSupport.ErpDocument import ErpDocument


class ErpBOM(ErpDocument):
    """Information that generally describes the Bill of Material Structure and its
    contents for a utility.
    
      This is used by ERP systems to transfer Bill of Material information between
    two business applications.
    """
    def __init__(self):
        super().__init__()
