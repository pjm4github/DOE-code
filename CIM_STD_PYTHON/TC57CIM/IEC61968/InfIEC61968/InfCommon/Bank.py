#######################################################
# 
# Bank.py
# Python implementation of the Class Bank
# Generated by Enterprise Architect
# Created on:      19-Dec-2023 6:12:52 PM
# 
#######################################################
from CIM_STD_PYTHON.TC57CIM.IEC61968.Common.OrganisationRole import OrganisationRole


class Bank(OrganisationRole):
    """Organisation that is a commercial bank, agency, or other institution that
    offers a similar service.
    """
    def __init__(self):

        super().__init__()
        # Bank identifier code as defined in ISO 9362; for use in countries wher IBAN is not yet in operation.
        self.bic = ""
        # International bank account number defined in ISO 13616;
        # for countries where IBAN is not in operation, the existing BIC or SWIFT
        # codes may be used instead (see ISO 9362).
        self.ban = ""
