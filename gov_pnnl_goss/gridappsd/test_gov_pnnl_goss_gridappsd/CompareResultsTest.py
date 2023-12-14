import unittest
import logging
from unittest.mock import Mock, patch
import json
import mockito as Mockito
from gov_pnnl_goss.gridappsd.api.AppManager import AppManager
from gov_pnnl_goss.gridappsd.api.ConfigurationManager import ConfigurationManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.simulation.SimulationEvent import ClientFactory
from logging import getLogger


str_output_1 = '''
{
    "output": {
        "ieee8500": {
            "cap_capbank0a": {
                "capacitor_A": 400000.0,
                "control": "MANUAL",
                "control_level": "BANK",
                "dwell_time": 100.0,
                "phases": "AN",
                "phases_connected": "NA",
                "pt_phase": "A",
                "switchA": "CLOSED"
            },
            "cap_capbank0b": {
                "capacitor_B": 400000.0,
                "control": "MANUAL",
                "control_level": "BANK",
                "dwell_time": 101.0,
                "phases": "BN",
                "phases_connected": "NB",
                "pt_phase": "B",
                "switchB": "CLOSED"
            },
            "cap_capbank0c": {
                "capacitor_C": 400000.0,
                "control": "MANUAL",
                "control_level": "BANK",
                "dwell_time": 102.0,
                "phases": "CN",
                "phases_connected": "NC",
                "pt_phase": "C",
                "switchC": "CLOSED"
            },
            "cap_capbank1a": {
                "capacitor_A": 300000.0,
                "control": "MANUAL",
                "control_level": "BANK",
                "dwell_time": 100.0,
                "phases": "AN",
                "phases_connected": "NA",
                "pt_phase": "A",
                "switchA": "CLOSED"
            },
            "cap_capbank1b": {
                "capacitor_B": 300000.0,
                "control": "MANUAL",
                "control_level": "BANK",
                "dwell_time": 101.0,
                "phases": "BN",
                "phases_connected": "NB",
                "pt_phase": "B",
                "switchB": "CLOSED"
            },
            "cap_capbank1c": {
                "capacitor_C": 300000.0,
                "control": "MANUAL",
                "control_level": "BANK",
                "dwell_time": 102.0,
                "phases": "CN",
                "phases_connected": "NC",
                "pt_phase": "C",
                "switchC": "CLOSED"
            },
            "cap_capbank2a": {
                "capacitor_A": 300000.0,
                "control": "MANUAL",
                "control_level": "BANK",
                "dwell_time": 100.0,
                "phases": "AN",
                "phases_connected": "NA",
                "pt_phase": "A",
                "switchA": "CLOSED"
            },
            "cap_capbank2b": {
                "capacitor_B": 300000.0,
                "control": "MANUAL",
                "control_level": "BANK",
                "dwell_time": 101.0,
                "phases": "BN",
                "phases_connected": "NB",
                "pt_phase": "B",
                "switchB": "CLOSED"
            },
            "cap_capbank2c": {
                "capacitor_C": 300000.0,
                "control": "MANUAL",
                "control_level": "BANK",
                "dwell_time": 102.0,
                "phases": "CN",
                "phases_connected": "NC",
                "pt_phase": "C",
                "switchC": "CLOSED"
            },
            "cap_capbank3": {
                "capacitor_A": 300000.0,
                "capacitor_B": 300000.0,
                "capacitor_C": 300000.0,
                "control": "MANUAL",
                "control_level": "INDIVIDUAL",
                "dwell_time": 0.0,
                "phases": "ABCN",
                "phases_connected": "NCBA",
                "pt_phase": "",
                "switchA": "CLOSED",
                "switchB": "CLOSED",
                "switchC": "CLOSED"
            },
            "nd_190-7361": {
                "voltage_A": "6410.387412-4584.456974j V",
                "voltage_B": "-7198.592139-3270.308373j V",
                "voltage_C": "642.547265+7539.531175j V"
            },
            "nd_190-8581": {
                "voltage_A": "6485.244723-4692.686497j V",
                "voltage_B": "-7183.641236-3170.693325j V",
                "voltage_C": "544.875721+7443.341013j V"
            },
            "nd_190-8593": {
                "voltage_A": "6723.279163-5056.725836j V",
                "voltage_B": "-7494.205738-3101.034603j V",
                "voltage_C": "630.475858+7534.534976j V"
            },
            "nd__hvmv_sub_lsb": {
                "voltage_A": "6261.474438-3926.148203j V",
                "voltage_B": "-6529.409296-3466.545236j V",
                "voltage_C": "247.131623+7348.295282j V"
            },
            "nd_l2673313": {
                "voltage_A": "6569.522313-5003.052614j V",
                "voltage_B": "-7431.486583-3004.840141j V",
                "voltage_C": "644.553332+7464.115913j V"
            },
            "nd_l2876814": {
                "voltage_A": "6593.064916-5014.031802j V",
                "voltage_B": "-7430.572725-3003.995539j V",
                "voltage_C": "643.473398+7483.558764j V"
            },
            "nd_l2955047": {
                "voltage_A": "5850.305847-4217.166594j V",
                "voltage_B": "-6729.652722-2987.617377j V",
                "voltage_C": "535.302084+7395.127354j V"
            },
            "nd_l3160107": {
                "voltage_A": "5954.507575-4227.423005j V",
                "voltage_B": "-6662.357613-3055.346880j V",
                "voltage_C": "600.213658+7317.832959j V"
            },
            "nd_l3254238": {
                "voltage_A": "6271.490549-4631.254028j V",
                "voltage_B": "-7169.987847-3099.952684j V",
                "voltage_C": "751.609656+7519.062259j V"
            },
            "nd_m1047574": {
                "voltage_A": "6306.632407-4741.568925j V",
                "voltage_B": "-7214.626338-2987.055915j V",
                "voltage_C": "622.058712+7442.125123j V"
            },
            "rcon_FEEDER_REG": {
                "Control": "MANUAL",
                "PT_phase": "CBA",
                "band_center": 126.5,
                "band_width": 2.0,
                "connect_type": "WYE_WYE",
                "control_level": "INDIVIDUAL",
                "dwell_time": 15.0,
                "lower_taps": 16,
                "raise_taps": 16,
                "regulation": 0.1
            },
            "rcon_VREG2": {
                "Control": "MANUAL",
                "PT_phase": "CBA",
                "band_center": 125.0,
                "band_width": 2.0,
                "connect_type": "WYE_WYE",
                "control_level": "INDIVIDUAL",
                "dwell_time": 15.0,
                "lower_taps": 16,
                "raise_taps": 16,
                "regulation": 0.1
            },
            "rcon_VREG3": {
                "Control": "MANUAL",
                "PT_phase": "CBA",
                "band_center": 125.0,
                "band_width": 2.0,
                "connect_type": "WYE_WYE",
                "control_level": "INDIVIDUAL",
                "dwell_time": 15.0,
                "lower_taps": 16,
                "raise_taps": 16,
                "regulation": 0.1
            },
            "rcon_VREG4": {
                "Control": "MANUAL",
                "PT_phase": "CBA",
                "band_center": 125.0,
                "band_width": 2.0,
                "connect_type": "WYE_WYE",
                "control_level": "INDIVIDUAL",
                "dwell_time": 15.0,
                "lower_taps": 16,
                "raise_taps": 16,
                "regulation": 0.1
            },
            "reg_FEEDER_REG": {
                "configuration": "rcon_FEEDER_REG",
                "phases": "ABC",
                "tap_A": 2,
                "tap_B": 2,
                "tap_C": 1,
                "to": "nd__hvmv_sub_lsb"
            },
            "reg_VREG2": {
                "configuration": "rcon_VREG2",
                "phases": "ABC",
                "tap_A": 10,
                "tap_B": 6,
                "tap_C": 2,
                "to": "nd_190-8593"
            },
            "reg_VREG3": {
                "configuration": "rcon_VREG3",
                "phases": "ABC",
                "tap_A": 16,
                "tap_B": 10,
                "tap_C": 1,
                "to": "nd_190-8581"
            },
            "reg_VREG4": {
                "configuration": "rcon_VREG4",
                "phases": "ABC",
                "tap_A": 12,
                "tap_B": 12,
                "tap_C": 5,
                "to": "nd_190-7361"
            },
            "xf_hvmv_sub": {
                "power_in_A": "1739729.120858-774784.929430j VA",
                "power_in_B": "1659762.622463-785218.730666j VA",
                "power_in_C": "1709521.679515-849734.584043j VA"
            }
        }
    },
    "command": "nextTimeStep"
}
'''

str_output_2 = '''
{
   "output": {
      "ieee8500": {
         "cap_capbank0a": {
            "capacitor_A": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
         },
         "cap_capbank0b": {
            "capacitor_B": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
         },
         "cap_capbank0c": {
            "capacitor_C": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
         },
         "cap_capbank1a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
         },
         "cap_capbank1b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
         },
         "cap_capbank1c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
         },
         "cap_capbank2a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
         },
         "cap_capbank2b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
         },
         "cap_capbank2c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
         },
         "cap_capbank3": {
            "capacitor_A": 300000.0,
            "capacitor_B": 300000.0,
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 0.0,
            "phases": "ABCN",
            "phases_connected": "NCBA",
            "pt_phase": "",
            "switchA": "CLOSED",
            "switchB": "CLOSED",
            "switchC": "CLOSED"
         },
         "nd_190-7361": {
            "voltage_A": "6410.387412-4584.456974j V",
            "voltage_B": "-7198.592139-3270.308373j V",
            "voltage_C": "642.547265+7539.531175j V"
         },
         "nd_190-8581": {
            "voltage_A": "6485.244723-4692.686497j V",
            "voltage_B": "-7183.641236-3170.693325j V",
            "voltage_C": "544.875721+7443.341013j V"
         },
         "nd_190-8593": {
            "voltage_A": "6723.279163-5056.725836j V",
            "voltage_B": "-7494.205738-3101.034603j V",
            "voltage_C": "630.475858+7534.534976j V"
         },
         "nd__hvmv_sub_lsb": {
            "voltage_A": "6261.474438-3926.148203j V",
            "voltage_B": "-6529.409296-3466.545236j V",
            "voltage_C": "247.131623+7348.295282j V"
         },
         "nd_l2673313": {
            "voltage_A": "6569.522313-5003.052614j V",
            "voltage_B": "-7431.486583-3004.840141j V",
            "voltage_C": "644.553332+7464.115913j V"
         },
         "nd_l2876814": {
            "voltage_A": "6593.064916-5014.031802j V",
            "voltage_B": "-7430.572725-3003.995539j V",
            "voltage_C": "643.473398+7483.558764j V"
         },
         "nd_l2955047": {
            "voltage_A": "5850.305847-4217.166594j V",
            "voltage_B": "-6729.652722-2987.617377j V",
            "voltage_C": "535.302084+7395.127354j V"
         },
         "nd_l3160107": {
            "voltage_A": "5954.507575-4227.423005j V",
            "voltage_B": "-6662.357613-3055.346880j V",
            "voltage_C": "600.213658+7317.832959j V"
         },
         "nd_l3254238": {
            "voltage_A": "6271.490549-4631.254028j V",
            "voltage_B": "-7169.987847-3099.952684j V",
            "voltage_C": "751.609656+7519.062259j V"
         },
         "nd_m1047574": {
            "voltage_A": "6306.632407-4741.568925j V",
            "voltage_B": "-7214.626338-2987.055915j V",
            "voltage_C": "622.058712+7442.125123j V"
         },
         "rcon_FEEDER_REG": {
            "Control": "MANUAL",
            "PT_phase": "CBA",
            "band_center": 126.5,
            "band_width": 2.0,
            "connect_type": "WYE_WYE",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "raise_taps": 16,
            "regulation": 0.10000000000000001
         },
         "rcon_VREG2": {
            "Control": "MANUAL",
            "PT_phase": "CBA",
            "band_center": 125.0,
            "band_width": 2.0,
            "connect_type": "WYE_WYE",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "raise_taps": 16,
            "regulation": 0.10000000000000001
         },
         "rcon_VREG3": {
            "Control": "MANUAL",
            "PT_phase": "CBA",
            "band_center": 125.0,
            "band_width": 2.0,
            "connect_type": "WYE_WYE",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "raise_taps": 16,
            "regulation": 0.10000000000000001
         },
         "rcon_VREG4": {
            "Control": "MANUAL",
            "PT_phase": "CBA",
            "band_center": 125.0,
            "band_width": 2.0,
            "connect_type": "WYE_WYE",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "raise_taps": 16,
            "regulation": 0.10000000000000001
         },
         "reg_FEEDER_REG": {
            "configuration": "rcon_FEEDER_REG",
            "phases": "ABC",
            "tap_A": 2,
            "tap_B": 2,
            "tap_C": 1,
            "to": "nd__hvmv_sub_lsb"
         },
         "reg_VREG2": {
            "configuration": "rcon_VREG2",
            "phases": "ABC",
            "tap_A": 10,
            "tap_B": 6,
            "tap_C": 2,
            "to": "nd_190-8593"
         },
         "reg_VREG3": {
            "configuration": "rcon_VREG3",
            "phases": "ABC",
            "tap_A": 16,
            "tap_B": 10,
            "tap_C": 1,
            "to": "nd_190-8581"
         },
         "reg_VREG4": {
            "configuration": "rcon_VREG4",
            "phases": "ABC",
            "tap_A": 12,
            "tap_B": 12,
            "tap_C": 5,
            "to": "nd_190-7361"
         },
         "xf_hvmv_sub": {
            "power_in_A": "1739729.120858-774784.929430j VA",
            "power_in_B": "1659762.622463-785218.730666j VA",
            "power_in_C": "1709521.679515-849734.584043j VA"
         }
      }
   },
   "command": "nextTimeStep"
}
'''

str_output_3 = '''
{
    "ieee8500": {
        "cap_capbank0a": {
            "capacitor_A": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank0b": {
            "capacitor_B": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank0c": {
            "capacitor_C": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank1a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank1b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank1c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank2a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank2b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank2c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank3": {
            "capacitor_A": 300000.0,
            "capacitor_B": 300000.0,
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 0.0,
            "phases": "ABCN",
            "phases_connected": "NCBA",
            "pt_phase": "",
            "switchA": "CLOSED",
            "switchB": "CLOSED",
            "switchC": "CLOSED"
        },
        "nd__hvmv_sub_lsb": {
            "voltage_A": "6064.561531-3845.670872j V",
            "voltage_B": "-6352.552616-3361.611246j V",
            "voltage_C": "276.907035+7179.756939j V"
        },
        "nd_190-7361": {
            "voltage_A": "4842.574414-4476.685135j V",
            "voltage_B": "-6188.665591-1939.201088j V",
            "voltage_C": "1439.949634+6505.686314j V"
        },
        "nd_190-8581": {
            "voltage_A": "4424.594642-4708.594628j V",
            "voltage_B": "-6385.646674-1373.465974j V",
            "voltage_C": "1432.367017+6738.674800j V"
        },
        "nd_190-8593": {
            "voltage_A": "3865.232090-4967.366914j V",
            "voltage_B": "-6370.129537-674.013552j V",
            "voltage_C": "1761.647771+6618.414315j V"
        },
        "nd_l2673313": {
            "voltage_A": "3275.878235-4690.132443j V",
            "voltage_B": "-6029.444705-334.685065j V",
            "voltage_C": "1841.889119+6312.023852j V"
        },
        "nd_l2876814": {
            "voltage_A": "3363.715891-4748.790707j V",
            "voltage_B": "-6029.028036-333.125572j V",
            "voltage_C": "1838.833944+6392.625299j V"
        },
        "nd_l2955047": {
            "voltage_A": "4044.821661-4235.230437j V",
            "voltage_B": "-5999.032872-1350.673043j V",
            "voltage_C": "1397.787047+6704.224553j V"
        },
        "nd_l3160107": {
            "voltage_A": "4563.436097-4171.693807j V",
            "voltage_B": "-5799.391956-1855.560373j V",
            "voltage_C": "1375.873489+6381.975365j V"
        },
        "nd_l3254238": {
            "voltage_A": "4354.789075-4256.496985j V",
            "voltage_B": "-5786.125160-1559.849666j V",
            "voltage_C": "1503.404100+6306.629422j V"
        },
        "nd_m1047574": {
            "voltage_A": "3637.596498-4661.598410j V",
            "voltage_B": "-6139.105151-656.801735j V",
            "voltage_C": "1736.935824+6543.527751j V"
        },
        "rcon_FEEDER_REG": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG2": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG3": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG4": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "reg_FEEDER_REG": {
            "configuration": "rcon_FEEDER_REG",
            "phases": "ABC",
            "tap_A": 2,
            "tap_B": 2,
            "tap_C": 1,
            "to": "nd__hvmv_sub_lsb"
        },
        "reg_VREG2": {
            "configuration": "rcon_VREG2",
            "phases": "ABC",
            "tap_A": 10,
            "tap_B": 6,
            "tap_C": 2,
            "to": "nd_190-8593"
        },
        "reg_VREG3": {
            "configuration": "rcon_VREG3",
            "phases": "ABC",
            "tap_A": 16,
            "tap_B": 10,
            "tap_C": 1,
            "to": "nd_190-8581"
        },
        "reg_VREG4": {
            "configuration": "rcon_VREG4",
            "phases": "ABC",
            "tap_A": 12,
            "tap_B": 12,
            "tap_C": 5,
            "to": "nd_190-7361"
        },
        "xf_hvmv_sub": {
            "power_in_A": "6998344.830459+2349122.052855j VA",
            "power_in_B": "6434344.730717+1458655.626184j VA",
            "power_in_C": "7487531.138704+1415431.538127j VA"
        }
    }
}
'''

str_output_4 = '''
{
   "ieee8500": {
      "cap_capbank0a": {
         "capacitor_A": 400000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 100.0,
         "phases": "AN",
         "phases_connected": "NA",
         "pt_phase": "A",
         "switchA": "CLOSED"
      },
      "cap_capbank0b": {
         "capacitor_B": 400000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 101.0,
         "phases": "BN",
         "phases_connected": "NB",
         "pt_phase": "B",
         "switchB": "CLOSED"
      },
      "cap_capbank0c": {
         "capacitor_C": 400000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 102.0,
         "phases": "CN",
         "phases_connected": "NC",
         "pt_phase": "C",
         "switchC": "CLOSED"
      },
      "cap_capbank1a": {
         "capacitor_A": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 100.0,
         "phases": "AN",
         "phases_connected": "NA",
         "pt_phase": "A",
         "switchA": "CLOSED"
      },
      "cap_capbank1b": {
         "capacitor_B": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 101.0,
         "phases": "BN",
         "phases_connected": "NB",
         "pt_phase": "B",
         "switchB": "CLOSED"
      },
      "cap_capbank1c": {
         "capacitor_C": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 102.0,
         "phases": "CN",
         "phases_connected": "NC",
         "pt_phase": "C",
         "switchC": "CLOSED"
      },
      "cap_capbank2a": {
         "capacitor_A": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 100.0,
         "phases": "AN",
         "phases_connected": "NA",
         "pt_phase": "A",
         "switchA": "CLOSED"
      },
      "cap_capbank2b": {
         "capacitor_B": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 101.0,
         "phases": "BN",
         "phases_connected": "NB",
         "pt_phase": "B",
         "switchB": "CLOSED"
      },
      "cap_capbank2c": {
         "capacitor_C": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 102.0,
         "phases": "CN",
         "phases_connected": "NC",
         "pt_phase": "C",
         "switchC": "CLOSED"
      },
      "cap_capbank3": {
         "capacitor_A": 300000.0,
         "capacitor_B": 300000.0,
         "capacitor_C": 300000.0,
         "control": "MANUAL",
         "control_level": "INDIVIDUAL",
         "dwell_time": 0.0,
         "phases": "ABCN",
         "phases_connected": "NCBA",
         "pt_phase": "",
         "switchA": "CLOSED",
         "switchB": "CLOSED",
         "switchC": "CLOSED"
      },
      "nd_190-7361": {
         "voltage_A": "4880.420881-4552.087189j V",
         "voltage_B": "-6270.772434-1918.625385j V",
         "voltage_C": "1480.382908+6582.002027j V"
      },
      "nd_190-8581": {
         "voltage_A": "4425.740568-4760.070519j V",
         "voltage_B": "-6466.587127-1333.944616j V",
         "voltage_C": "1478.923270+6818.080038j V"
      },
      "nd_190-8593": {
         "voltage_A": "3873.637297-5061.524827j V",
         "voltage_B": "-6493.216700-618.093256j V",
         "voltage_C": "1826.776774+6735.529317j V"
      },
      "nd__hvmv_sub_lsb": {
         "voltage_A": "6097.897641-3876.216603j V",
         "voltage_B": "-6395.084564-3374.206473j V",
         "voltage_C": "285.588913+7223.679479j V"
      },
      "nd_l2673313": {
         "voltage_A": "3273.560830-4785.348257j V",
         "voltage_B": "-6147.877528-271.060340j V",
         "voltage_C": "1908.494726+6423.602576j V"
      },
      "nd_l2876814": {
         "voltage_A": "3363.317124-4843.946549j V",
         "voltage_B": "-6147.462115-269.296512j V",
         "voltage_C": "1905.220695+6505.698493j V"
      },
      "nd_l2955047": {
         "voltage_A": "4046.892500-4281.190101j V",
         "voltage_B": "-6034.905167-1307.288347j V",
         "voltage_C": "1433.878539+6740.744179j V"
      },
      "nd_l3160107": {
         "voltage_A": "4569.997316-4213.224832j V",
         "voltage_B": "-5837.296662-1826.602764j V",
         "voltage_C": "1405.199210+6416.227554j V"
      },
      "nd_l3254238": {
         "voltage_A": "4383.776858-4331.404601j V",
         "voltage_B": "-5865.206491-1529.444197j V",
         "voltage_C": "1544.903143+6380.370107j V"
      },
      "nd_m1047574": {
         "voltage_A": "3621.597751-4718.220426j V",
         "voltage_B": "-6217.145451-599.360367j V",
         "voltage_C": "1789.768136+6617.268110j V"
      },
      "rcon_FEEDER_REG": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "rcon_VREG2": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "rcon_VREG3": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "rcon_VREG4": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "reg_FEEDER_REG": {
         "configuration": "rcon_FEEDER_REG",
         "phases": "ABC",
         "tap_A": 3,
         "tap_B": 3,
         "tap_C": 2,
         "to": "nd__hvmv_sub_lsb"
      },
      "reg_VREG2": {
         "configuration": "rcon_VREG2",
         "phases": "ABC",
         "tap_A": 11,
         "tap_B": 7,
         "tap_C": 3,
         "to": "nd_190-8593"
      },
      "reg_VREG3": {
         "configuration": "rcon_VREG3",
         "phases": "ABC",
         "tap_A": 16,
         "tap_B": 11,
         "tap_C": 2,
         "to": "nd_190-8581"
      },
      "reg_VREG4": {
         "configuration": "rcon_VREG4",
         "phases": "ABC",
         "tap_A": 13,
         "tap_B": 13,
         "tap_C": 6,
         "to": "nd_190-7361"
      },
      "xf_hvmv_sub": {
         "power_in_A": "7208010.474000+2375848.659577j VA",
         "power_in_B": "6619686.765355+1504448.106935j VA",
         "power_in_C": "7668524.439602+1430626.309647j VA"
      }
   }
}
'''

str_output_5 = '''
{
   "ieee8500": {
      "cap_capbank0a": {
         "capacitor_A": 400000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 100.0,
         "phases": "AN",
         "phases_connected": "NA",
         "pt_phase": "A",
         "switchA": "CLOSED"
      },
      "cap_capbank0b": {
         "capacitor_B": 400000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 101.0,
         "phases": "BN",
         "phases_connected": "NB",
         "pt_phase": "B",
         "switchB": "CLOSED"
      },
      "cap_capbank0c": {
         "capacitor_C": 400000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 102.0,
         "phases": "CN",
         "phases_connected": "NC",
         "pt_phase": "C",
         "switchC": "CLOSED"
      },
      "cap_capbank1a": {
         "capacitor_A": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 100.0,
         "phases": "AN",
         "phases_connected": "NA",
         "pt_phase": "A",
         "switchA": "CLOSED"
      },
      "cap_capbank1b": {
         "capacitor_B": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 101.0,
         "phases": "BN",
         "phases_connected": "NB",
         "pt_phase": "B",
         "switchB": "CLOSED"
      },
      "cap_capbank1c": {
         "capacitor_C": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 102.0,
         "phases": "CN",
         "phases_connected": "NC",
         "pt_phase": "C",
         "switchC": "CLOSED"
      },
      "cap_capbank2a": {
         "capacitor_A": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 100.0,
         "phases": "AN",
         "phases_connected": "NA",
         "pt_phase": "A",
         "switchA": "CLOSED"
      },
      "cap_capbank2b": {
         "capacitor_B": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 101.0,
         "phases": "BN",
         "phases_connected": "NB",
         "pt_phase": "B",
         "switchB": "CLOSED"
      },
      "cap_capbank2c": {
         "capacitor_C": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 102.0,
         "phases": "CN",
         "phases_connected": "NC",
         "pt_phase": "C",
         "switchC": "CLOSED"
      },
      "cap_capbank3": {
         "capacitor_A": 300000.0,
         "capacitor_B": 300000.0,
         "capacitor_C": 300000.0,
         "control": "MANUAL",
         "control_level": "INDIVIDUAL",
         "dwell_time": 0.0,
         "phases": "ABCN",
         "phases_connected": "NCBA",
         "pt_phase": "",
         "switchA": "CLOSED",
         "switchB": "CLOSED",
         "switchC": "CLOSED"
      },
      "nd_190-7361": {
         "voltage_A": "4842.574443-4476.685167j V",
         "voltage_B": "-6188.665651-1939.201083j V",
         "voltage_C": "1439.949619+6505.686246j V"
      },
      "nd_190-8581": {
         "voltage_A": "4424.594669-4708.594658j V",
         "voltage_B": "-6385.646736-1373.465960j V",
         "voltage_C": "1432.367000+6738.674737j V"
      },
      "nd_190-8593": {
         "voltage_A": "3865.232110-4967.366940j V",
         "voltage_B": "-6370.129604-674.013526j V",
         "voltage_C": "1761.647748+6618.414260j V"
      },
      "nd__hvmv_sub_lsb": {
         "voltage_A": "6064.561584-3845.670912j V",
         "voltage_B": "-6352.552659-3361.611265j V",
         "voltage_C": "276.907045+7179.756854j V"
      },
      "nd_l2673313": {
         "voltage_A": "3275.878250-4690.132464j V",
         "voltage_B": "-6029.444772-334.685033j V",
         "voltage_C": "1841.889094+6312.023802j V"
      },
      "nd_l2876814": {
         "voltage_A": "3363.715906-4748.790729j V",
         "voltage_B": "-6029.028102-333.125542j V",
         "voltage_C": "1838.833919+6392.625249j V"
      },
      "nd_l2955047": {
         "voltage_A": "4044.821686-4235.230465j V",
         "voltage_B": "-5999.032930-1350.673031j V",
         "voltage_C": "1397.787032+6704.224490j V"
      },
      "nd_l3160107": {
         "voltage_A": "4563.436125-4171.693838j V",
         "voltage_B": "-5799.391956-1855.560373j V",
         "voltage_C": "1375.873489+6381.975365j V"
      },
      "nd_l3254238": {
         "voltage_A": "4354.789100-4256.497015j V",
         "voltage_B": "-5786.125219-1559.849657j V",
         "voltage_C": "1503.404081+6306.629357j V"
      },
      "nd_m1047574": {
         "voltage_A": "3637.596517-4661.598435j V",
         "voltage_B": "-6139.105216-656.801711j V",
         "voltage_C": "1736.935802+6543.527697j V"
      },
      "rcon_FEEDER_REG": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "rcon_VREG2": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "rcon_VREG3": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "rcon_VREG4": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "reg_FEEDER_REG": {
         "configuration": "rcon_FEEDER_REG",
         "phases": "ABC",
         "tap_A": 2,
         "tap_B": 2,
         "tap_C": 1,
         "to": "nd__hvmv_sub_lsb"
      },
      "reg_VREG2": {
         "configuration": "rcon_VREG2",
         "phases": "ABC",
         "tap_A": 10,
         "tap_B": 6,
         "tap_C": 2,
         "to": "nd_190-8593"
      },
      "reg_VREG3": {
         "configuration": "rcon_VREG3",
         "phases": "ABC",
         "tap_A": 16,
         "tap_B": 10,
         "tap_C": 1,
         "to": "nd_190-8581"
      },
      "reg_VREG4": {
         "configuration": "rcon_VREG4",
         "phases": "ABC",
         "tap_A": 12,
         "tap_B": 12,
         "tap_C": 5,
         "to": "nd_190-7361"
      },
      "xf_hvmv_sub": {
         "power_in_A": "6998345.011202+2349120.682358j VA",
         "power_in_B": "6434345.874127+1458655.968384j VA",
         "power_in_C": "7487530.317505+1415431.857709j VA"
      }
   }
}
'''

str_output_6 = '''
{
   "ieee8500": {
      "cap_capbank0a": {
         "capacitor_A": 400000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 100.0,
         "phases": "AN",
         "phases_connected": "NA",
         "pt_phase": "A",
         "switchA": "CLOSED"
      },
      "cap_capbank0b": {
         "capacitor_B": 400000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 101.0,
         "phases": "BN",
         "phases_connected": "NB",
         "pt_phase": "B",
         "switchB": "CLOSED"
      },
      "cap_capbank0c": {
         "capacitor_C": 400000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 102.0,
         "phases": "CN",
         "phases_connected": "NC",
         "pt_phase": "C",
         "switchC": "CLOSED"
      },
      "cap_capbank1a": {
         "capacitor_A": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 100.0,
         "phases": "AN",
         "phases_connected": "NA",
         "pt_phase": "A",
         "switchA": "CLOSED"
      },
      "cap_capbank1b": {
         "capacitor_B": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 101.0,
         "phases": "BN",
         "phases_connected": "NB",
         "pt_phase": "B",
         "switchB": "CLOSED"
      },
      "cap_capbank1c": {
         "capacitor_C": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 102.0,
         "phases": "CN",
         "phases_connected": "NC",
         "pt_phase": "C",
         "switchC": "CLOSED"
      },
      "cap_capbank2a": {
         "capacitor_A": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 100.0,
         "phases": "AN",
         "phases_connected": "NA",
         "pt_phase": "A",
         "switchA": "CLOSED"
      },
      "cap_capbank2b": {
         "capacitor_B": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 101.0,
         "phases": "BN",
         "phases_connected": "NB",
         "pt_phase": "B",
         "switchB": "CLOSED"
      },
      "cap_capbank2c": {
         "capacitor_C": 300000.0,
         "control": "MANUAL",
         "control_level": "BANK",
         "dwell_time": 102.0,
         "phases": "CN",
         "phases_connected": "NC",
         "pt_phase": "C",
         "switchC": "CLOSED"
      },
      "cap_capbank3": {
         "capacitor_A": 300000.0,
         "capacitor_B": 300000.0,
         "capacitor_C": 300000.0,
         "control": "MANUAL",
         "control_level": "INDIVIDUAL",
         "dwell_time": 0.0,
         "phases": "ABCN",
         "phases_connected": "NCBA",
         "pt_phase": "",
         "switchA": "CLOSED",
         "switchB": "CLOSED",
         "switchC": "CLOSED"
      },
      "nd_190-7361": {
         "voltage_A": "4880.420881-4552.087189j V",
         "voltage_B": "-6270.772434-1918.625385j V",
         "voltage_C": "1480.382908+6582.002027j V"
      },
      "nd_190-8581": {
         "voltage_A": "4425.740568-4760.070519j V",
         "voltage_B": "-6466.587127-1333.944616j V",
         "voltage_C": "1478.923270+6818.080038j V"
      },
      "nd_190-8593": {
         "voltage_A": "3873.637297-5061.524827j V",
         "voltage_B": "-6493.216700-618.093256j V",
         "voltage_C": "1826.776774+6735.529317j V"
      },
      "nd__hvmv_sub_lsb": {
         "voltage_A": "6097.897641-3876.216603j V",
         "voltage_B": "-6395.084564-3374.206473j V",
         "voltage_C": "285.588913+7223.679479j V"
      },
      "nd_l2673313": {
         "voltage_A": "3273.560830-4785.348257j V",
         "voltage_B": "-6147.877528-271.060340j V",
         "voltage_C": "1908.494726+6423.602576j V"
      },
      "nd_l2876814": {
         "voltage_A": "3363.317124-4843.946549j V",
         "voltage_B": "-6147.462115-269.296512j V",
         "voltage_C": "1905.220695+6505.698493j V"
      },
      "nd_l2955047": {
         "voltage_A": "4046.892500-4281.190101j V",
         "voltage_B": "-6034.905167-1307.288347j V",
         "voltage_C": "1433.878539+6740.744179j V"
      },
      "nd_l3160107": {
         "voltage_A": "4569.997316-4213.224832j V",
         "voltage_B": "-5837.296662-1826.602764j V",
         "voltage_C": "1405.199210+6416.227554j V"
      },
      "nd_l3254238": {
         "voltage_A": "4383.776858-4331.404601j V",
         "voltage_B": "-5865.206491-1529.444197j V",
         "voltage_C": "1544.903143+6380.370107j V"
      },
      "nd_m1047574": {
         "voltage_A": "3621.597751-4718.220426j V",
         "voltage_B": "-6217.145451-599.360367j V",
         "voltage_C": "1789.768136+6617.268110j V"
      },
      "rcon_FEEDER_REG": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "rcon_VREG2": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "rcon_VREG3": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "rcon_VREG4": {
         "Control": "MANUAL",
         "PT_phase": "CBA",
         "band_center": 0.0,
         "band_width": 0.0,
         "connect_type": "WYE_WYE",
         "control_level": "INDIVIDUAL",
         "dwell_time": 15.0,
         "lower_taps": 16,
         "raise_taps": 16,
         "regulation": 0.10000000000000001
      },
      "reg_FEEDER_REG": {
         "configuration": "rcon_FEEDER_REG",
         "phases": "ABC",
         "tap_A": 3,
         "tap_B": 3,
         "tap_C": 2,
         "to": "nd__hvmv_sub_lsb"
      },
      "reg_VREG2": {
         "configuration": "rcon_VREG2",
         "phases": "ABC",
         "tap_A": 11,
         "tap_B": 7,
         "tap_C": 3,
         "to": "nd_190-8593"
      },
      "reg_VREG3": {
         "configuration": "rcon_VREG3",
         "phases": "ABC",
         "tap_A": 16,
         "tap_B": 11,
         "tap_C": 2,
         "to": "nd_190-8581"
      },
      "reg_VREG4": {
         "configuration": "rcon_VREG4",
         "phases": "ABC",
         "tap_A": 13,
         "tap_B": 13,
         "tap_C": 6,
         "to": "nd_190-7361"
      },
      "xf_hvmv_sub": {
         "power_in_A": "7208010.474000+2375848.659577j VA",
         "power_in_B": "6619686.765355+1504448.106935j VA",
         "power_in_C": "7668524.439602+1430626.309647j VA"
      }
   }
}
'''

str_output_7 = '''
{
    "command": "nextTimeStep",
    "output": {
        "message": {
            "measurements": [
                {
                    "angle": -36.1531349344702,
                    "magnitude": 137.140261868117,
                    "measurement_mrid": "_53b4e410-ab61-4e57-964e-2e69f1015c91"
                },
                {
                    "angle": -36.1752589638468,
                    "magnitude": 137.614214480546,
                    "measurement_mrid": "_ce21c543-b611-44e9-8cd1-e52e5703f67d"
                },
                {
                    "angle": 86.7585177891221,
                    "magnitude": 120.837457337809,
                    "measurement_mrid": "_11f1b07b-3650-45e5-afcb-45cd0c6640e3"
                },
                {
                    "angle": 86.7469450807509,
                    "magnitude": 121.054921286902,
                    "measurement_mrid": "_5c7f812c-3682-4b2f-b7ad-07f005f516d2"
                },
                {
                    "angle": 87.0184958940396,
                    "magnitude": 7377.71886915975,
                    "measurement_mrid": "_edbff185-8930-4a86-a413-827e2529d6a4"
                },
                {
                    "angle": -155.735680325771,
                    "magnitude": 125.831711138923,
                    "measurement_mrid": "_2e6fe682-1695-4b80-9f2d-f038d2a2c6d5"
                },
                {
                    "angle": -155.762156065794,
                    "magnitude": 126.351609160319,
                    "measurement_mrid": "_765d4b1a-1d5e-4c78-b8b5-b0f3d77f6a72"
                },
                {
                    "angle": 86.4187656829769,
                    "magnitude": 7380.80103329454,
                    "measurement_mrid": "_aeb7e914-897e-413d-a43f-b68381b9deb3"
                },
                {
                    "angle": -153.732488777407,
                    "magnitude": 7272.79746213391,
                    "measurement_mrid": "_6ca51f24-179a-48f5-815a-8f38a260ca89"
                },
                {
                    "angle": -33.6283815900164,
                    "magnitude": 7297.5519012062,
                    "measurement_mrid": "_bf946254-a877-4381-8007-6b598f286aa0"
                },
                {
                    "angle": 86.7961241349245,
                    "magnitude": 7264.87109896409,
                    "measurement_mrid": "_fb78f0e6-80f7-4e52-9b05-d11844671db4"
                },
                {
                    "angle": 85.859768459708,
                    "magnitude": 121.382240168411,
                    "measurement_mrid": "_3647ac9f-1f11-45b7-9336-2ab930ab2220"
                },
                {
                    "angle": 85.859768459708,
                    "magnitude": 121.382240168411,
                    "measurement_mrid": "_b3428f0a-0d8b-451f-b876-e76ede273b57"
                },
                {
                    "angle": 86.7409752260658,
                    "magnitude": 120.046834338623,
                    "measurement_mrid": "_39aff029-b414-4358-a119-60b8863eb2d0"
                },
                {
                    "angle": 86.7409752260658,
                    "magnitude": 120.046834338623,
                    "measurement_mrid": "_cf9ce649-b683-4d8d-94be-9809c1e05cc3"
                },
                {
                    "angle": -35.2932939483041,
                    "magnitude": 128.261464920435,
                    "measurement_mrid": "_32b6c140-0b7b-463e-acd1-2a3e7cfab65c"
                },
                {
                    "angle": -35.2695416100777,
                    "magnitude": 127.787515404521,
                    "measurement_mrid": "_9761f31b-38ef-4f03-8419-10bd02a42843"
                },
                {
                    "angle": 86.105081458176,
                    "magnitude": 7324.57086658997,
                    "measurement_mrid": "_9d287880-cc77-4b3b-b237-ad7dd0e0cdec"
                },
                {
                    "angle": 86.4239545649662,
                    "magnitude": 7374.41062825274,
                    "measurement_mrid": "_116b765d-8524-49c9-b068-e8e8f540c1ca"
                },
                {
                    "angle": -155.09779139072,
                    "magnitude": 7712.93493587313,
                    "measurement_mrid": "_57eab3f2-5617-49b4-92e7-8ad49b23a877"
                },
                {
                    "angle": -34.5228705281378,
                    "magnitude": 8008.23690972783,
                    "measurement_mrid": "_6b94267e-1231-4bf7-9d69-d6e59dd69432"
                },
                {
                    "angle": -155.239735157386,
                    "magnitude": 7649.54345918876,
                    "measurement_mrid": "_046cf2ad-49e3-4ff7-b139-d87eb3c8b43a"
                },
                {
                    "angle": 88.4131158039047,
                    "magnitude": 119.626090938265,
                    "measurement_mrid": "_2e88fcce-3efa-4f53-b6a8-d3a6816449e8"
                },
                {
                    "angle": 88.4131158039047,
                    "magnitude": 119.626090938265,
                    "measurement_mrid": "_ea7e6405-9837-46f8-bd2e-e9986ac85de0"
                },
                {
                    "angle": -36.1285086600748,
                    "magnitude": 136.466592302218,
                    "measurement_mrid": "_2597d1da-cd8b-4f41-bdea-162aeebac609"
                },
                {
                    "angle": -36.1285086600748,
                    "magnitude": 136.466592302218,
                    "measurement_mrid": "_3d020b1c-abdd-473d-b03d-ef174c5c05f6"
                },
                {
                    "angle": 86.263077551756,
                    "magnitude": 7412.48287276562,
                    "measurement_mrid": "_144dc36b-9ece-498b-a3ef-7b446649b3d4"
                },
                {
                    "angle": -156.455122030355,
                    "magnitude": 7945.71628549772,
                    "measurement_mrid": "_404b1cbe-d154-4f7f-8359-b801d8bc91b2"
                },
                {
                    "angle": 86.4201594805088,
                    "magnitude": 7382.55768991261,
                    "measurement_mrid": "_ac9af5b6-d9f1-4f51-88dc-15e094415618"
                },
                {
                    "angle": -155.111060126725,
                    "magnitude": 7706.00994419159,
                    "measurement_mrid": "_b9c7e719-17ee-4d06-a904-630c4f651294"
                },
                {
                    "angle": 86.2379353759375,
                    "magnitude": 7399.47112515952,
                    "measurement_mrid": "_cc2a04f9-e8a6-4171-b417-f5b06b42eee0"
                },
                {
                    "angle": -36.2751279128198,
                    "magnitude": 136.558556422072,
                    "measurement_mrid": "_4add96bc-c118-4bf3-a661-d1a46371f3c2"
                },
                {
                    "angle": -36.2528376891608,
                    "magnitude": 136.084601348743,
                    "measurement_mrid": "_d1cc71c5-206b-4221-b628-2a8142c0419f"
                },
                {
                    "angle": -35.7846914304408,
                    "magnitude": 8294.71716734643,
                    "measurement_mrid": "_18fcbb2f-3f1b-45af-b26b-41d47a140a0d"
                },
                {
                    "angle": 86.4504993558852,
                    "magnitude": 7351.61039559488,
                    "measurement_mrid": "_0f62515b-e9a1-490c-ae22-2fc29de9e3d8"
                },
                {
                    "angle": -156.141244397816,
                    "magnitude": 7984.95318724635,
                    "measurement_mrid": "_362cae8d-8963-4f74-a73a-fda6a9369726"
                },
                {
                    "angle": -35.6290748703649,
                    "magnitude": 8308.85775489796,
                    "measurement_mrid": "_87223e4d-5216-4100-bb24-82e4c3a4642d"
                },
                {
                    "angle": -35.6289110261716,
                    "magnitude": 8308.96401737695,
                    "measurement_mrid": "_3d2bab60-d623-4a49-8514-22931691ba17"
                },
                {
                    "angle": -156.141275980127,
                    "magnitude": 7984.96227120749,
                    "measurement_mrid": "_5b29544e-eda3-406e-b513-4c0e321ac2f4"
                },
                {
                    "angle": 86.4504268233541,
                    "magnitude": 7351.67539447603,
                    "measurement_mrid": "_e36e1183-9994-4b4f-acca-4c69c3b0a703"
                },
                {
                    "angle": -156.140867784101,
                    "magnitude": 7984.84490251392,
                    "measurement_mrid": "_a341333e-7046-45ab-96d3-a214085f9a27"
                },
                {
                    "angle": -35.6310280556835,
                    "magnitude": 8307.59109724027,
                    "measurement_mrid": "_c1e32ec0-3b6b-412f-9d3a-ec75f54e272b"
                },
                {
                    "angle": 86.4513641780244,
                    "magnitude": 7350.83559890111,
                    "measurement_mrid": "_f3df1617-76e3-4526-bb87-1aa43aec2e10"
                },
                {
                    "angle": -35.785957343364,
                    "magnitude": 8293.99273340112,
                    "measurement_mrid": "_b12df2e9-4f53-4092-82bf-2888a60620dc"
                },
                {
                    "angle": -156.880947702603,
                    "magnitude": 130.19632683713,
                    "measurement_mrid": "_2bbbb8fc-ae0d-4478-913c-f2ef0e850c64"
                },
                {
                    "angle": -156.880947702603,
                    "magnitude": 130.19632683713,
                    "measurement_mrid": "_df157edd-fb06-4169-8996-d6d9661defa0"
                },
                {
                    "angle": 87.2528574531494,
                    "magnitude": 7267.41824288174,
                    "measurement_mrid": "_c0b50f63-c367-4b56-a73b-a882777e3054"
                },
                {
                    "angle": -156.833568027363,
                    "magnitude": 130.24142663495,
                    "measurement_mrid": "_329ba467-8cfa-4872-b5fd-d34834d38019"
                },
                {
                    "angle": -156.859186638752,
                    "magnitude": 130.761315165659,
                    "measurement_mrid": "_391dd3dc-3402-4303-9127-815e798a134d"
                },
                {
                    "angle": -156.359515312672,
                    "magnitude": 7913.54988188704,
                    "measurement_mrid": "_319b88cb-7a2a-4da0-a3bf-a3a03335ab37"
                },
                {
                    "angle": -35.5903644208874,
                    "magnitude": 8312.62564156332,
                    "measurement_mrid": "_71afb3bf-f9dd-4906-9d91-42fc589672b2"
                },
                {
                    "angle": 86.1065444412095,
                    "magnitude": 7324.99232870222,
                    "measurement_mrid": "_fd8c3c86-3e1a-498b-bbef-7408670290c3"
                },
                {
                    "angle": -156.451839918168,
                    "magnitude": 7946.16134650139,
                    "measurement_mrid": "_fdd0e3a6-eec2-453a-9739-3cb6ae3ef5db"
                },
                {
                    "angle": 85.8300446332486,
                    "magnitude": 121.126502789976,
                    "measurement_mrid": "_01ffe4e3-9bfb-4836-83b7-c4fb4e2e8392"
                },
                {
                    "angle": 85.8300446332486,
                    "magnitude": 121.126502789976,
                    "measurement_mrid": "_b3ece1ab-b9be-467e-a463-f297937ae9bb"
                },
                {
                    "angle": -156.428177041138,
                    "magnitude": 7888.17263296137,
                    "measurement_mrid": "_0cd45572-d9ab-4e79-be0e-07dd16515a87"
                },
                {
                    "angle": -156.426327373547,
                    "magnitude": 7889.19337622942,
                    "measurement_mrid": "_44dbc652-056e-416c-b41f-710ac49c9e40"
                },
                {
                    "angle": -35.8876021163184,
                    "magnitude": 138.704555388311,
                    "measurement_mrid": "_cd3a8c27-48dd-462b-a774-780cd2a1620b"
                },
                {
                    "angle": -35.8876021163184,
                    "magnitude": 138.704555388311,
                    "measurement_mrid": "_dc83a9d2-6054-470b-a80d-0471b00101fe"
                },
                {
                    "angle": -36.0995575668958,
                    "magnitude": 136.749661143093,
                    "measurement_mrid": "_07ca595f-39ca-4882-8a12-5ff173f57156"
                },
                {
                    "angle": -36.0995575668958,
                    "magnitude": 136.749661143093,
                    "measurement_mrid": "_a58557bc-4201-4cce-9669-c2658fd2859d"
                },
                {
                    "angle": 85.9144707555136,
                    "magnitude": 121.482322824347,
                    "measurement_mrid": "_46a316d1-09dd-46d1-b286-c384ce32d373"
                },
                {
                    "angle": 85.8857836466651,
                    "magnitude": 122.02572481312,
                    "measurement_mrid": "_e6081723-2bba-4b93-8b63-e3564ec0bc76"
                },
                {
                    "angle": 85.9555064912139,
                    "magnitude": 121.214395814405,
                    "measurement_mrid": "_b90b37cb-8219-41e4-b578-f7ada802ef5c"
                },
                {
                    "angle": 85.9843842657493,
                    "magnitude": 120.67099412604,
                    "measurement_mrid": "_d58c9b5f-9d37-4c77-8c22-6556283fb022"
                },
                {
                    "angle": -156.454259047368,
                    "magnitude": 7948.48969678809,
                    "measurement_mrid": "_a15f8813-a829-4f4e-bdd8-54ac8b8a3a85"
                },
                {
                    "angle": -36.0133142358284,
                    "magnitude": 137.70365448232,
                    "measurement_mrid": "_2a94f866-6e1f-4eed-8133-06d257f2014c"
                },
                {
                    "angle": -36.0133142358284,
                    "magnitude": 137.70365448232,
                    "measurement_mrid": "_3f04e28b-819d-4c80-81aa-30d8bd65aedf"
                },
                {
                    "angle": 86.4057960880848,
                    "magnitude": 7370.23554962674,
                    "measurement_mrid": "_7b71f22d-abed-4c31-9edf-3b41357db720"
                },
                {
                    "angle": -36.1882827565635,
                    "magnitude": 136.542082538688,
                    "measurement_mrid": "_002d94f4-a99a-40cf-bba5-22869993959e"
                },
                {
                    "angle": -36.2105004094553,
                    "magnitude": 137.016037324613,
                    "measurement_mrid": "_a0195103-0e21-42bf-a770-c35d94f40a89"
                },
                {
                    "angle": 85.7099253012797,
                    "magnitude": 121.210316328732,
                    "measurement_mrid": "_6ffac2c6-ad6f-42ab-830a-5bd6ed47e7d8"
                },
                {
                    "angle": 85.7099253012797,
                    "magnitude": 121.210316328732,
                    "measurement_mrid": "_a4568951-be5b-4f12-aa6d-b8f195e682e7"
                },
                {
                    "angle": -156.863161726317,
                    "magnitude": 130.348881823284,
                    "measurement_mrid": "_940b8caa-2061-4846-af3e-c72cab270627"
                },
                {
                    "angle": -156.863161726317,
                    "magnitude": 130.348881823284,
                    "measurement_mrid": "_e0c74393-4a34-403a-94cd-fa56577a2df2"
                },
                {
                    "angle": -154.136405685201,
                    "magnitude": 7771.95466249389,
                    "measurement_mrid": "_b28ae39a-3dd2-4e86-b1a5-bb0da12e5716"
                },
                {
                    "angle": -155.713479412674,
                    "magnitude": 126.61398448082,
                    "measurement_mrid": "_2e0aba75-792f-4f68-abf2-ffa603e79c90"
                },
                {
                    "angle": -155.697619735985,
                    "magnitude": 126.301942590556,
                    "measurement_mrid": "_6ae5201f-ce89-4eea-b8d3-2c97af10b936"
                },
                {
                    "angle": 88.4265364209536,
                    "magnitude": 119.348722667855,
                    "measurement_mrid": "_49574975-d226-44e9-84e5-03eee888cf5b"
                },
                {
                    "angle": 88.3973397612128,
                    "magnitude": 119.892124693479,
                    "measurement_mrid": "_d00dc049-ed6e-4e2d-b01b-88add9f6ac1c"
                },
                {
                    "angle": -156.186737590564,
                    "magnitude": 127.944733010269,
                    "measurement_mrid": "_568fcc92-b337-4fe8-8d2a-a257199adeb2"
                },
                {
                    "angle": -156.186737590564,
                    "magnitude": 127.944733010269,
                    "measurement_mrid": "_9edd5204-12b0-4523-b5fb-2c3c8433bdd2"
                },
                {
                    "angle": 86.7459852486903,
                    "magnitude": 120.085576502523,
                    "measurement_mrid": "_24791703-77a0-4654-b6b9-5317d305c2bf"
                },
                {
                    "angle": 86.7459852486903,
                    "magnitude": 120.085576502523,
                    "measurement_mrid": "_4caa2fc9-2790-4a38-862d-dbcfd1fa270a"
                },
                {
                    "angle": -35.788329190591,
                    "magnitude": 8282.41223539825,
                    "measurement_mrid": "_464c3a83-5be8-4891-8b68-6c837de282d0"
                },
                {
                    "angle": -156.45363779794,
                    "magnitude": 7950.00053057462,
                    "measurement_mrid": "_93cf34a3-1b0e-4316-8200-a0b0e5abcedc"
                },
                {
                    "angle": 86.3892701297855,
                    "magnitude": 7366.01006619001,
                    "measurement_mrid": "_bc5f96cc-6a7f-4901-a501-c6494f7fa6eb"
                },
                {
                    "angle": 87.4234247404682,
                    "magnitude": 120.84289624634,
                    "measurement_mrid": "_52654f75-6c5e-45b4-8cdf-fa35b12becfd"
                },
                {
                    "angle": 87.4408000875996,
                    "magnitude": 120.516965294611,
                    "measurement_mrid": "_e4263a51-2b32-4fd0-9f6f-8d260dc06025"
                },
                {
                    "angle": -34.0986889399555,
                    "magnitude": 121.156359688762,
                    "measurement_mrid": "_1dd06a18-a583-4b32-acb9-b59e6d7fd0ae"
                },
                {
                    "angle": -34.0483680174117,
                    "magnitude": 120.208440983216,
                    "measurement_mrid": "_5c91080c-da2c-4db7-a1d8-3ddd857e4a4f"
                },
                {
                    "angle": -154.194412274123,
                    "magnitude": 119.659883772738,
                    "measurement_mrid": "_20b9be68-0088-4615-a715-578c7ef05c1b"
                },
                {
                    "angle": -154.249860133198,
                    "magnitude": 120.699164559692,
                    "measurement_mrid": "_f7c66770-7910-4328-ac47-f8870a0bff50"
                },
                {
                    "angle": 86.25449217281,
                    "magnitude": 120.543831840314,
                    "measurement_mrid": "_45e82fec-e9b3-4b94-8c00-856ded4999fa"
                },
                {
                    "angle": 86.3125713480882,
                    "magnitude": 119.456997445597,
                    "measurement_mrid": "_ee2902b3-63b6-46d8-853c-cace5bea0126"
                },
                {
                    "angle": 88.4383599749097,
                    "magnitude": 119.752084748982,
                    "measurement_mrid": "_3798c108-c967-442b-84bc-9fb24fb78723"
                },
                {
                    "angle": 88.4383599749097,
                    "magnitude": 119.752084748982,
                    "measurement_mrid": "_d2a7cb37-3f97-40df-8267-d546b7a31568"
                },
                {
                    "angle": 86.8470641207101,
                    "magnitude": 121.368290554073,
                    "measurement_mrid": "_309a8d84-3d92-46cb-9a79-ee74a13b0e96"
                },
                {
                    "angle": 86.9047506226958,
                    "magnitude": 120.28145750987,
                    "measurement_mrid": "_c8110d3f-a6ef-42dc-a86c-15951b5b9938"
                },
                {
                    "angle": -35.5026904856496,
                    "magnitude": 8313.55917505573,
                    "measurement_mrid": "_e4185434-3ae3-4452-9a79-fd709d45521f"
                },
                {
                    "angle": -35.8872802141707,
                    "magnitude": 137.467324207617,
                    "measurement_mrid": "_2433763b-ff85-458e-bdfe-8623681c45c4"
                },
                {
                    "angle": -35.9005372711051,
                    "magnitude": 137.751586907052,
                    "measurement_mrid": "_bbc3a14b-4c9e-4e44-b591-c26ce80f5f60"
                },
                {
                    "angle": 87.7575483628137,
                    "magnitude": 120.684295056581,
                    "measurement_mrid": "_15bfbec8-8ede-4b24-b0a3-93d62c4551b7"
                },
                {
                    "angle": 87.7749466385228,
                    "magnitude": 120.35836395916,
                    "measurement_mrid": "_779635b5-5025-45b7-b00f-0360559c5240"
                },
                {
                    "angle": -156.658865104426,
                    "magnitude": 132.364106658584,
                    "measurement_mrid": "_9045c8ee-1c5e-4fdd-bdcc-b41ace0e94fa"
                },
                {
                    "angle": -156.648745266547,
                    "magnitude": 132.156262239432,
                    "measurement_mrid": "_cfc779d8-9b76-4d59-bab4-78e506019a0b"
                },
                {
                    "angle": -35.5657418683169,
                    "magnitude": 8329.08508974619,
                    "measurement_mrid": "_d649a64f-dfb1-4065-af01-24af0fc8aa66"
                },
                {
                    "angle": -35.7362890467811,
                    "magnitude": 131.888882388851,
                    "measurement_mrid": "_304d0f6e-a8eb-40c7-ab16-275fad1e7f54"
                },
                {
                    "angle": -35.7131947640955,
                    "magnitude": 131.414931445526,
                    "measurement_mrid": "_df31bc0d-5735-4c46-9db1-1055322acdbd"
                },
                {
                    "angle": 86.0762931206185,
                    "magnitude": 7417.34233253246,
                    "measurement_mrid": "_600de2ae-e035-4495-81f5-0c5eecaa78d2"
                },
                {
                    "angle": -154.547981562359,
                    "magnitude": 7751.46272290608,
                    "measurement_mrid": "_7c1f46cb-f9ec-49cb-b076-3ae31e488bb6"
                },
                {
                    "angle": -34.3891884236563,
                    "magnitude": 7785.07600470549,
                    "measurement_mrid": "_fea9bf6c-eb05-4bd6-8c7e-b2fd08d1f34a"
                },
                {
                    "angle": -34.6301515339752,
                    "magnitude": 8002.03072708617,
                    "measurement_mrid": "_c8925011-1d85-4d47-a494-fcb0f011aeae"
                },
                {
                    "angle": -33.7096030801453,
                    "magnitude": 7292.33659641616,
                    "measurement_mrid": "_c08790c1-4b7c-488e-9455-f24aa5644591"
                },
                {
                    "angle": -35.5911896799108,
                    "magnitude": 8307.86514971213,
                    "measurement_mrid": "_189060bb-d2f2-40f7-8965-4c8c34cb00d2"
                },
                {
                    "angle": -156.868115042734,
                    "magnitude": 130.313447603663,
                    "measurement_mrid": "_01d26467-b73e-4845-9096-79be3a8d0f1f"
                },
                {
                    "angle": -156.868115042734,
                    "magnitude": 130.313447603663,
                    "measurement_mrid": "_5cb8cc41-e2f9-41ef-a117-92cacf0360fa"
                },
                {
                    "angle": -36.1735387210608,
                    "magnitude": 136.965772541834,
                    "measurement_mrid": "_4e612005-dcdd-4c8a-a7b3-95caa98aeee5"
                },
                {
                    "angle": -36.1824224921022,
                    "magnitude": 137.155459143258,
                    "measurement_mrid": "_fed32b31-70f0-40bd-9b28-16299cea4dea"
                },
                {
                    "angle": -35.981194069823,
                    "magnitude": 137.598840778391,
                    "measurement_mrid": "_9417944a-49d0-4548-a485-1aad3159a499"
                },
                {
                    "angle": -35.981194069823,
                    "magnitude": 137.598840778391,
                    "measurement_mrid": "_fc1bb8b8-8734-4048-a337-6b3832e5f5e8"
                },
                {
                    "angle": -32.2654292184108,
                    "magnitude": 7315.45919036085,
                    "measurement_mrid": "_b56a9290-1811-46eb-925e-a7e044d89d10"
                },
                {
                    "angle": -35.949017564382,
                    "magnitude": 137.731487533207,
                    "measurement_mrid": "_c4a753f0-9121-4d61-b2d0-1e016eb5fa4c"
                },
                {
                    "angle": -35.962249737419,
                    "magnitude": 138.015750458144,
                    "measurement_mrid": "_f8cf78f0-4165-4703-ad01-7b30989d7fdb"
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.005787,
                    "measurement_mrid": "_52bb868b-8e4d-4115-b835-46502b42303c"
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.005787,
                    "measurement_mrid": "_534d5cde-9061-45d4-8382-8275f40b201d"
                },
                {
                    "measurement_mrid": "_74653361-3b39-41af-8592-def0653ea623",
                    "value": 1
                },
                {
                    "angle": 89.0716051928,
                    "magnitude": 7284.22092205347,
                    "measurement_mrid": "_8bed3180-1516-446a-a6b2-58fe3a51edc7"
                },
                {
                    "measurement_mrid": "_8f100920-469e-45c1-b9c7-55c0d601b0e7",
                    "value": 1
                },
                {
                    "angle": 89.0716051928,
                    "magnitude": 7284.22092205347,
                    "measurement_mrid": "_9a9f6ec8-0567-4072-9688-b72f12d4f062"
                },
                {
                    "angle": -155.776693650601,
                    "magnitude": 125.854618425625,
                    "measurement_mrid": "_ce5cba0f-80bb-4dbd-8243-7f1f3ab696c6"
                },
                {
                    "angle": -155.776693650601,
                    "magnitude": 125.854618425625,
                    "measurement_mrid": "_eb35a389-ac6b-4680-b4a0-e4876d081bcd"
                },
                {
                    "angle": -154.714262907507,
                    "magnitude": 7781.20482511892,
                    "measurement_mrid": "_5fc4a5fc-39df-4933-b1ee-c652d8bafecb"
                },
                {
                    "angle": -156.876309920811,
                    "magnitude": 129.863270126894,
                    "measurement_mrid": "_0b64d82a-99f3-45a6-861d-03074719d8a6"
                },
                {
                    "angle": -156.902001898475,
                    "magnitude": 130.383158156948,
                    "measurement_mrid": "_da786cbb-c245-42c7-882b-a68d8fd180b3"
                },
                {
                    "angle": -34.8614668508525,
                    "magnitude": 7738.18876689047,
                    "measurement_mrid": "_a234b9c1-e2a3-4f49-b949-3532b5893196"
                },
                {
                    "angle": 85.7351516084312,
                    "magnitude": 122.245791178657,
                    "measurement_mrid": "_28745873-5abd-48d7-8885-6e2efb6b6b3c"
                },
                {
                    "angle": 85.7351516084312,
                    "magnitude": 122.245791178657,
                    "measurement_mrid": "_87a89512-1493-4732-9ef8-1c1882d745bd"
                },
                {
                    "angle": -35.9927650819684,
                    "magnitude": 137.648375985387,
                    "measurement_mrid": "_9ee167d6-886e-44d6-b9b6-5be227f45607"
                },
                {
                    "angle": -35.9927650819684,
                    "magnitude": 137.648375985387,
                    "measurement_mrid": "_f0794f5b-7627-4667-81d7-ecad135439dc"
                },
                {
                    "angle": -156.960561598691,
                    "magnitude": 131.149360069696,
                    "measurement_mrid": "_1a31f5df-bb7d-41f2-8edb-00522f2300a3"
                },
                {
                    "angle": -156.945228615829,
                    "magnitude": 130.837324095259,
                    "measurement_mrid": "_44835eb7-900e-4a38-88e9-a346fecbdde9"
                },
                {
                    "angle": -154.270149897109,
                    "magnitude": 120.419084383871,
                    "measurement_mrid": "_0c36bb80-33c8-49fe-9d3f-ea84ba0eb3d4"
                },
                {
                    "angle": -154.297845884321,
                    "magnitude": 120.938974461043,
                    "measurement_mrid": "_d6596735-091c-42c7-96c0-2f07e689f68e"
                },
                {
                    "angle": -35.2823922221916,
                    "magnitude": 127.985142633703,
                    "measurement_mrid": "_8e354815-6ea9-4223-a923-6eb22d5d7138"
                },
                {
                    "angle": -35.2585905436205,
                    "magnitude": 127.51119199374,
                    "measurement_mrid": "_a0bc5553-75d6-4e60-a623-5bba073e89b3"
                },
                {
                    "angle": 86.6692233462928,
                    "magnitude": 119.478198326243,
                    "measurement_mrid": "_f5846495-16b1-4cda-be73-fc75264ca108"
                },
                {
                    "angle": 86.6692233462928,
                    "magnitude": 119.478198326243,
                    "measurement_mrid": "_f97cf10a-a8b6-4abf-b55e-8f2f4d6a1324"
                },
                {
                    "angle": 86.257904691111,
                    "magnitude": 7410.10572463766,
                    "measurement_mrid": "_a74f9978-3cbe-4421-8c8b-e00c5caf870d"
                },
                {
                    "angle": -152.211392429993,
                    "magnitude": 120.973305727118,
                    "measurement_mrid": "_d0072a66-07bb-47b9-bddc-dc5abea421a5"
                },
                {
                    "angle": -152.211392429993,
                    "magnitude": 120.973305727118,
                    "measurement_mrid": "_d9677600-fe25-4775-83bf-14797b53df80"
                },
                {
                    "angle": 87.197550156306,
                    "magnitude": 7240.17241572385,
                    "measurement_mrid": "_cbed4660-c050-4186-80f5-74c469f908a9"
                },
                {
                    "angle": 86.2521167787449,
                    "magnitude": 7406.70694431399,
                    "measurement_mrid": "_a5bfce44-2eb0-41e3-af27-91c83d2fd867"
                },
                {
                    "angle": 87.2126649788578,
                    "magnitude": 120.824375994318,
                    "measurement_mrid": "_0b87dbcc-e3ff-4a41-9371-eb0f058cd410"
                },
                {
                    "angle": 87.2300433253246,
                    "magnitude": 120.498445618716,
                    "measurement_mrid": "_916ea6cd-c525-47bc-806b-ff4c00fe4b34"
                },
                {
                    "angle": 86.873779221495,
                    "magnitude": 120.881931411859,
                    "measurement_mrid": "_13c9a185-fef7-4834-a596-1fc8a0622c5d"
                },
                {
                    "angle": 86.873779221495,
                    "magnitude": 120.881931411859,
                    "measurement_mrid": "_4bfcf32e-0749-4934-ba81-868f9e7e8dcd"
                },
                {
                    "angle": 85.6424439619478,
                    "magnitude": 7416.84372183783,
                    "measurement_mrid": "_5c9f6b4d-7e2f-4207-bf1c-05f12a4e6bdc"
                },
                {
                    "angle": -34.8497726444752,
                    "magnitude": 7721.53470631293,
                    "measurement_mrid": "_9794b033-d017-4f51-8388-cdb1c519a70b"
                },
                {
                    "angle": -155.193795046867,
                    "magnitude": 7672.52703854408,
                    "measurement_mrid": "_faf13c0c-2e19-4c4c-8198-a69b33c602f8"
                },
                {
                    "angle": 86.4251275606952,
                    "magnitude": 7386.76985703925,
                    "measurement_mrid": "_f533003b-e6ec-4284-83d1-b494e5447b1c"
                },
                {
                    "angle": -34.3646813353404,
                    "magnitude": 7780.78048128974,
                    "measurement_mrid": "_9763b1a5-ad16-4724-b018-35da148e48f3"
                },
                {
                    "angle": -34.3676606528027,
                    "magnitude": 7779.6708020838,
                    "measurement_mrid": "_2bba7f28-ed5b-48bc-9286-a5f1771d2315"
                },
                {
                    "angle": -154.83734240368,
                    "magnitude": 7734.60429252533,
                    "measurement_mrid": "_c9bf6e2f-35b5-4b16-8e47-58737916fbc9"
                },
                {
                    "angle": 85.8040290441444,
                    "magnitude": 121.368371764645,
                    "measurement_mrid": "_3de6f985-62a2-4366-90a7-d6e692c196cd"
                },
                {
                    "angle": 85.8040290441444,
                    "magnitude": 121.368371764645,
                    "measurement_mrid": "_63143caa-08f1-40a8-b957-f74bf68b8973"
                },
                {
                    "angle": 86.252130871605,
                    "magnitude": 7406.71381191705,
                    "measurement_mrid": "_5bf966d2-16f1-4ce0-8300-f38842a22c23"
                },
                {
                    "angle": -34.8396997710569,
                    "magnitude": 7709.76188388698,
                    "measurement_mrid": "_6a75cbca-a02e-4ed0-80d9-d7d59c70f3d1"
                },
                {
                    "angle": -155.227501323749,
                    "magnitude": 7656.16571907675,
                    "measurement_mrid": "_b5e5bda4-aa49-45f3-b0df-7d660268479e"
                },
                {
                    "angle": 85.65426161238,
                    "magnitude": 7419.02034608262,
                    "measurement_mrid": "_d80034c0-88b9-4fcd-a3b5-a7d581e6022c"
                },
                {
                    "angle": -156.900857007785,
                    "magnitude": 131.508208516257,
                    "measurement_mrid": "_1a74a3d3-3e04-43ca-bc2a-64ddc81e491b"
                },
                {
                    "angle": -156.900857007785,
                    "magnitude": 131.508208516257,
                    "measurement_mrid": "_1c96dc09-36bd-4206-a6ac-10b0e136d3c1"
                },
                {
                    "angle": -31.5014507437741,
                    "magnitude": 7322.42598018032,
                    "measurement_mrid": "_3a394d26-71f4-465a-bd13-87eb7235cdb7"
                },
                {
                    "angle": 88.7382336409631,
                    "magnitude": 7289.12325446211,
                    "measurement_mrid": "_54fcc61a-08f6-4a04-befb-473040d81c06"
                },
                {
                    "angle": -151.514039505143,
                    "magnitude": 7323.11777516358,
                    "measurement_mrid": "_746ab98c-2b9a-4924-bb28-f2b045b8d599"
                },
                {
                    "angle": -155.573145734577,
                    "magnitude": 127.39894294256,
                    "measurement_mrid": "_4ca53ca6-49ea-4f6d-b86a-9c6e294d6b26"
                },
                {
                    "angle": -155.573145734577,
                    "magnitude": 127.39894294256,
                    "measurement_mrid": "_703eb3c2-07d3-426e-be44-8e9a454576b9"
                },
                {
                    "angle": 86.6660170195117,
                    "magnitude": 119.451927514773,
                    "measurement_mrid": "_f205fcde-1595-42c6-82f6-64448f27fb60"
                },
                {
                    "angle": 86.6660170195117,
                    "magnitude": 119.451927514773,
                    "measurement_mrid": "_f5ac5554-7114-48d7-9fe7-530846d94d35"
                },
                {
                    "angle": -35.5032062978139,
                    "magnitude": 8313.2667898424,
                    "measurement_mrid": "_e05a5256-a5bb-4c91-b88e-70a91212f5a9"
                },
                {
                    "angle": 86.1124419505821,
                    "magnitude": 7326.00097682663,
                    "measurement_mrid": "_c12672ff-607b-4eb9-8233-00ab1b073518"
                },
                {
                    "angle": -33.1993097003794,
                    "magnitude": 120.924237132861,
                    "measurement_mrid": "_66bc371a-2f0e-401c-ae5e-19e77a7538b6"
                },
                {
                    "angle": -33.1993097003794,
                    "magnitude": 120.924237132861,
                    "measurement_mrid": "_a7bf2c10-963f-441b-a848-9be1dd843abf"
                },
                {
                    "angle": 88.3494897845153,
                    "magnitude": 119.184267152541,
                    "measurement_mrid": "_0f1633c7-ebfb-4d39-918b-24aa1379bb4f"
                },
                {
                    "angle": 88.3494897845153,
                    "magnitude": 119.184267152541,
                    "measurement_mrid": "_1280da5d-20b6-4e39-94bd-47358520930f"
                },
                {
                    "angle": -156.158750131369,
                    "magnitude": 127.962061473882,
                    "measurement_mrid": "_b3d73d7c-73b7-44dc-915c-a0dd803d0c84"
                },
                {
                    "angle": -156.17442632276,
                    "magnitude": 128.274097309962,
                    "measurement_mrid": "_dbd68627-bdef-4d91-883f-3f6b5ccdd3b5"
                },
                {
                    "angle": -35.5337481919123,
                    "magnitude": 8321.19480294457,
                    "measurement_mrid": "_dc26f0d4-4f03-4290-99d9-146defa558d4"
                },
                {
                    "angle": 87.1987458921388,
                    "magnitude": 7240.7647705193,
                    "measurement_mrid": "_05984a53-df38-40f5-9de8-774447484475"
                },
                {
                    "angle": -156.282055278034,
                    "magnitude": 7943.05231117492,
                    "measurement_mrid": "_761bbbca-ea96-4e4e-9259-c7db1e19411c"
                },
                {
                    "angle": -156.959888991154,
                    "magnitude": 131.155252665308,
                    "measurement_mrid": "_20f6e6d8-9383-403d-8c3a-95b8a0d76b5b"
                },
                {
                    "angle": -156.944556877977,
                    "magnitude": 130.843216456332,
                    "measurement_mrid": "_63fee0b3-2209-44bd-a3a4-2aa7a8f2b9ab"
                },
                {
                    "angle": -156.378857608402,
                    "magnitude": 7900.41298988753,
                    "measurement_mrid": "_9dd17878-033e-4443-836f-04f342019754"
                },
                {
                    "angle": 86.2643335468851,
                    "magnitude": 7413.11897870248,
                    "measurement_mrid": "_411c29a0-d8f4-49e1-a413-451bac00777c"
                },
                {
                    "angle": -36.1262364183512,
                    "magnitude": 137.122395275739,
                    "measurement_mrid": "_7728dbde-88fc-4945-b988-4490de7521e1"
                },
                {
                    "angle": -36.15935698749,
                    "magnitude": 137.833066047756,
                    "measurement_mrid": "_9741534e-bffb-44bb-b094-d0f3c19b80f4"
                },
                {
                    "angle": -156.468334909891,
                    "magnitude": 7872.40436809056,
                    "measurement_mrid": "_484b4eda-2c83-4a21-97e5-925ff315646b"
                },
                {
                    "angle": -35.7438020594816,
                    "magnitude": 8239.41888362173,
                    "measurement_mrid": "_931d1038-670e-4d66-9a7e-d4e7305a8feb"
                },
                {
                    "angle": -36.2682784866875,
                    "magnitude": 136.475717891825,
                    "measurement_mrid": "_27f6fc56-2f48-4222-8c08-7168a8e16b6c"
                },
                {
                    "angle": -36.2549013238203,
                    "magnitude": 136.191454206736,
                    "measurement_mrid": "_ee3560af-cbea-4eb6-bb25-146f030e4578"
                },
                {
                    "angle": -36.0582987976386,
                    "magnitude": 137.128123498755,
                    "measurement_mrid": "_3ac38553-674b-4d76-93e1-dd066bc3812d"
                },
                {
                    "angle": -36.0582987976386,
                    "magnitude": 137.128123498755,
                    "measurement_mrid": "_a25fdd5f-6b38-4fd9-8cf3-8ced79f4da82"
                },
                {
                    "angle": -35.0364747604735,
                    "magnitude": 132.419503290391,
                    "measurement_mrid": "_057d4d8e-1dc0-4017-9354-2c1f6274f35a"
                },
                {
                    "angle": -35.0364747604735,
                    "magnitude": 132.419503290391,
                    "measurement_mrid": "_6f0e776f-0d8a-404a-861f-b181a3c5b484"
                },
                {
                    "angle": 85.9603849893731,
                    "magnitude": 121.20510121616,
                    "measurement_mrid": "_4e7e387e-cf0c-4910-a0ab-b9e03d70a28a"
                },
                {
                    "angle": 85.9603849893731,
                    "magnitude": 121.20510121616,
                    "measurement_mrid": "_bde48b06-8054-4e29-b74c-1546d567908e"
                },
                {
                    "angle": -156.581747697437,
                    "magnitude": 132.006217921153,
                    "measurement_mrid": "_2a459b34-c51e-4a38-bfcd-1c7574094d40"
                },
                {
                    "angle": -156.581748095723,
                    "magnitude": 132.006217523712,
                    "measurement_mrid": "_564dfed5-24c5-4833-bfa8-f9f133635c23"
                },
                {
                    "angle": -152.968840988029,
                    "magnitude": 7316.84409097005,
                    "measurement_mrid": "_4569c5a7-4a14-40e2-8ac6-7208b500b702"
                },
                {
                    "angle": -35.5888659948943,
                    "magnitude": 8339.29180149239,
                    "measurement_mrid": "_b582bf3c-f9b6-43db-8344-bbc7b50901da"
                },
                {
                    "angle": 86.4241389982512,
                    "magnitude": 7386.20412350394,
                    "measurement_mrid": "_b810a538-55ee-457a-b252-f283e4edf3fc"
                },
                {
                    "angle": -156.232510257165,
                    "magnitude": 7979.7925860335,
                    "measurement_mrid": "_fba96deb-b347-4cfe-b4f1-9f3681d40ff6"
                },
                {
                    "angle": -36.142311897768,
                    "magnitude": 137.484319321006,
                    "measurement_mrid": "_6114b247-86f9-41fa-914c-b5ea954bb4ad"
                },
                {
                    "angle": -36.142311897768,
                    "magnitude": 137.484319321006,
                    "measurement_mrid": "_c68e5f54-a376-4780-9158-01ae227e0935"
                },
                {
                    "angle": 87.6915020954083,
                    "magnitude": 7308.24059678297,
                    "measurement_mrid": "_f04b5102-ff89-4785-91da-9511d633b4b5"
                },
                {
                    "angle": 87.6803686813741,
                    "magnitude": 7307.78680736688,
                    "measurement_mrid": "_745211c9-ea64-4784-9c79-daf10e56ef71"
                },
                {
                    "angle": 89.0115086456467,
                    "magnitude": 7279.40214968047,
                    "measurement_mrid": "_c018258d-929a-4300-9118-8d0127dab824"
                },
                {
                    "angle": -153.737493401454,
                    "magnitude": 7304.05986511064,
                    "measurement_mrid": "_da481a51-48e0-43f5-9051-6905416f4673"
                },
                {
                    "angle": -32.8052401410082,
                    "magnitude": 7316.06985821152,
                    "measurement_mrid": "_1a08023a-c27b-4b5b-af19-a41d71a9bcba"
                },
                {
                    "angle": 87.7142907929222,
                    "magnitude": 7304.79066211876,
                    "measurement_mrid": "_f2b67bf8-ca2c-4c04-bb70-1013f822ffee"
                },
                {
                    "angle": -152.894176699674,
                    "magnitude": 7320.39149347294,
                    "measurement_mrid": "_fa91ae9c-d004-4f10-a943-36dc28185207"
                },
                {
                    "angle": 86.4437089699867,
                    "magnitude": 120.033259398348,
                    "measurement_mrid": "_6909475d-0d1b-4f61-a74b-4cb783db1e6a"
                },
                {
                    "angle": 86.4262636609731,
                    "magnitude": 120.359189763625,
                    "measurement_mrid": "_cac90669-2c21-4228-988e-3df8370e8b6f"
                },
                {
                    "angle": -32.1937890557968,
                    "magnitude": 120.763039538177,
                    "measurement_mrid": "_0ac61ab1-ddca-45f4-8666-2b146d41cdd0"
                },
                {
                    "angle": -32.0859326610789,
                    "magnitude": 121.259875069123,
                    "measurement_mrid": "_36742f29-5b46-471c-96a5-dda85668be07"
                },
                {
                    "angle": -156.880392640303,
                    "magnitude": 130.200399140863,
                    "measurement_mrid": "_4c4049d0-dd55-4ed8-96d8-a9393946103a"
                },
                {
                    "angle": -156.880392640303,
                    "magnitude": 130.200399140863,
                    "measurement_mrid": "_50ca552c-00bb-4554-a5f1-3e68e0646cf9"
                },
                {
                    "angle": 87.7518548225269,
                    "magnitude": 120.795153224249,
                    "measurement_mrid": "_2b408559-b0a7-4e96-b8d1-0616a16ccb63"
                },
                {
                    "angle": 87.7808343616684,
                    "magnitude": 120.251751450688,
                    "measurement_mrid": "_3bef4189-d3ab-4413-a23b-be3a5f363801"
                },
                {
                    "angle": -36.2696265283217,
                    "magnitude": 136.291266491561,
                    "measurement_mrid": "_79fd5579-ec69-4eaa-9423-972c57078037"
                },
                {
                    "angle": -36.2696265283217,
                    "magnitude": 136.291266491561,
                    "measurement_mrid": "_95b6906e-b710-42aa-96c6-50dc9c098a14"
                },
                {
                    "angle": 87.2503415708071,
                    "magnitude": 7266.33560707766,
                    "measurement_mrid": "_b2382b48-bd63-4d51-89a1-d007fda812aa"
                },
                {
                    "angle": 88.9193731914327,
                    "magnitude": 7240.16966925713,
                    "measurement_mrid": "_f6272e8d-3b12-4f9f-a118-fa97fe8f0ed8"
                },
                {
                    "angle": -154.60330388726,
                    "magnitude": 128.428187814348,
                    "measurement_mrid": "_5becd64e-8358-4fe5-bc04-42c8532e00cb"
                },
                {
                    "angle": -154.60330388726,
                    "magnitude": 128.428187814348,
                    "measurement_mrid": "_cc5bdb4a-5406-43be-9f38-66092fd67a36"
                },
                {
                    "angle": -34.6938008159626,
                    "magnitude": 119.486830794355,
                    "measurement_mrid": "_5c7c0f1f-272a-4ae7-86ce-f527e0668e97"
                },
                {
                    "angle": -34.6785032168403,
                    "magnitude": 119.202571319025,
                    "measurement_mrid": "_6b1438ec-ca43-4f99-ad2b-52028618451d"
                },
                {
                    "angle": 87.0333997739867,
                    "magnitude": 120.779628970232,
                    "measurement_mrid": "_04d9f2d2-1055-42cd-8364-ba1a297392b2"
                },
                {
                    "angle": 87.0333997739867,
                    "magnitude": 120.779628970232,
                    "measurement_mrid": "_e97f5827-721a-430e-87d4-f3caf0db94c7"
                },
                {
                    "angle": -35.7984280767598,
                    "magnitude": 8267.75765582576,
                    "measurement_mrid": "_81c7f36f-b2aa-4309-8fec-d5ea357ea84b"
                },
                {
                    "angle": -153.171068626897,
                    "magnitude": 7319.87072137761,
                    "measurement_mrid": "_682dd689-dbd7-4b2f-830a-3fc1b613f716"
                },
                {
                    "angle": 87.2504751222577,
                    "magnitude": 7266.37341610977,
                    "measurement_mrid": "_e08299ad-f814-4817-ab43-a979a1ca9ae3"
                },
                {
                    "angle": -156.889618698669,
                    "magnitude": 131.180581809641,
                    "measurement_mrid": "_53593fd1-bcf8-4c69-b180-6a54347ee8a4"
                },
                {
                    "angle": -156.915059037694,
                    "magnitude": 131.700468910171,
                    "measurement_mrid": "_e175a76b-4b6f-4067-8009-f741d5d27653"
                },
                {
                    "angle": -155.267610546205,
                    "magnitude": 7634.98662604366,
                    "measurement_mrid": "_765c2911-ddfa-495b-bd45-2588a4641517"
                },
                {
                    "angle": -156.40120151643,
                    "magnitude": 7888.41767488622,
                    "measurement_mrid": "_73cd39ad-131a-441d-ad51-edf48a5b0c37"
                },
                {
                    "angle": -156.864510560166,
                    "magnitude": 130.120575311576,
                    "measurement_mrid": "_af1b9853-0df2-4ce5-ae66-8ecd25d54610"
                },
                {
                    "angle": -156.879925499354,
                    "magnitude": 130.43261240724,
                    "measurement_mrid": "_b304fe76-e887-4e65-b81f-636e05ceea58"
                },
                {
                    "angle": -31.6763101519408,
                    "magnitude": 121.143480005965,
                    "measurement_mrid": "_0119759a-4bb4-4b92-9ac2-bcb87213cb85"
                },
                {
                    "angle": -31.6763101519408,
                    "magnitude": 121.143480005965,
                    "measurement_mrid": "_1df7f74b-a04a-476a-b9ae-c9675183b5fd"
                },
                {
                    "angle": -156.436654571839,
                    "magnitude": 7869.39661289034,
                    "measurement_mrid": "_c88ca80f-fd86-4c76-bfc0-c8cd1c0c3748"
                },
                {
                    "angle": -35.5922988464151,
                    "magnitude": 8311.90049401963,
                    "measurement_mrid": "_2e6ef20c-25e3-4178-954a-1295ba91482f"
                },
                {
                    "angle": -156.86664176658,
                    "magnitude": 131.265164811463,
                    "measurement_mrid": "_4cabd27c-78da-4eba-b9ac-85d3da2d22ea"
                },
                {
                    "angle": -156.904688657318,
                    "magnitude": 132.044739486032,
                    "measurement_mrid": "_cd5522e3-1739-4eac-b7b3-429eb2667378"
                },
                {
                    "angle": 87.25853283818,
                    "magnitude": 7270.25061102252,
                    "measurement_mrid": "_fddb7b54-894c-4748-8c93-0cf57b2c00c3"
                },
                {
                    "angle": -34.8344761499715,
                    "magnitude": 7709.1501680413,
                    "measurement_mrid": "_cc660270-1e9d-42c4-911d-4499b34a3a17"
                },
                {
                    "angle": -35.4584065579848,
                    "magnitude": 8390.39943826068,
                    "measurement_mrid": "_da156e2e-0581-4cb8-bd40-cde151866760"
                },
                {
                    "angle": 87.0628377920045,
                    "magnitude": 120.501687163856,
                    "measurement_mrid": "_2fda55bc-835a-48ba-a760-77135afbf64d"
                },
                {
                    "angle": 87.0339171320411,
                    "magnitude": 121.045088157687,
                    "measurement_mrid": "_d19b5c85-dd73-4052-a128-041ee9081b6e"
                },
                {
                    "angle": 86.3773752364482,
                    "magnitude": 7355.48754649096,
                    "measurement_mrid": "_6656c7ed-121f-45e2-95b6-8c5db8bdcbf9"
                },
                {
                    "angle": -156.452138173287,
                    "magnitude": 7952.12415263758,
                    "measurement_mrid": "_a79a5cf5-77b0-4ff9-8a3b-d38c8b8c6836"
                },
                {
                    "angle": -35.8145765280236,
                    "magnitude": 8265.8713601451,
                    "measurement_mrid": "_bff55576-e657-4f1e-abc2-ba81007de1eb"
                },
                {
                    "angle": -36.1163656247169,
                    "magnitude": 136.973912273676,
                    "measurement_mrid": "_6dd9540a-c1f4-46ee-aed8-55e259da89a5"
                },
                {
                    "angle": -36.0941411544983,
                    "magnitude": 136.499958471856,
                    "measurement_mrid": "_ca4400cc-f26f-4433-95ca-4b25758f3efc"
                },
                {
                    "angle": -35.5045301905186,
                    "magnitude": 8312.52964285814,
                    "measurement_mrid": "_527db624-9f9b-444d-94d8-22b6ad11ddc4"
                },
                {
                    "angle": -34.3612528646249,
                    "magnitude": 7782.67961365307,
                    "measurement_mrid": "_20c07da5-8791-46f4-aaef-c3a3ea5ff93d"
                },
                {
                    "angle": -34.8540216993312,
                    "magnitude": 7702.03660904552,
                    "measurement_mrid": "_601fc727-2db6-4fd7-95d7-240399da806b"
                },
                {
                    "angle": -34.6252630831084,
                    "magnitude": 7773.23434758661,
                    "measurement_mrid": "_fe908b6e-fe50-46f1-92a6-fd4eb5c73fd9"
                },
                {
                    "angle": -156.897085039205,
                    "magnitude": 130.29295380134,
                    "measurement_mrid": "_220a4be0-c75e-4dbd-993c-d60340e7a121"
                },
                {
                    "angle": -156.897085039205,
                    "magnitude": 130.29295380134,
                    "measurement_mrid": "_81cbb1dd-c27c-490a-a599-249876f26110"
                },
                {
                    "angle": 85.8835321735492,
                    "magnitude": 121.410035569528,
                    "measurement_mrid": "_57cdb2d2-b33c-4e0b-8912-c46d728a5b61"
                },
                {
                    "angle": 85.8662848179847,
                    "magnitude": 121.735965461135,
                    "measurement_mrid": "_c19a2eae-b4d1-440a-a9c0-08050f4893fa"
                },
                {
                    "angle": -154.128578640485,
                    "magnitude": 7775.86420713267,
                    "measurement_mrid": "_a7f7427a-3b84-4987-89bd-c3e2cfef53fc"
                },
                {
                    "angle": 85.6432326032375,
                    "magnitude": 7416.81235619201,
                    "measurement_mrid": "_e52601a7-f127-4920-892d-2ffb860760fa"
                },
                {
                    "angle": -155.705854048053,
                    "magnitude": 7749.60657977401,
                    "measurement_mrid": "_8a92d626-6c11-4126-82d4-81a8c4abb91c"
                },
                {
                    "angle": 86.7167702828925,
                    "magnitude": 119.854036701487,
                    "measurement_mrid": "_16624e27-e498-4513-9e09-c1dff87654e5"
                },
                {
                    "angle": 86.7167702828925,
                    "magnitude": 119.854036701487,
                    "measurement_mrid": "_b85dd707-6370-4f2d-8767-57429e4384f3"
                },
                {
                    "angle": 88.9491231409949,
                    "magnitude": 7248.66323773064,
                    "measurement_mrid": "_0659ce9b-02c3-41b1-a321-71955f0ab549"
                },
                {
                    "angle": -151.722179256344,
                    "magnitude": 7321.69751339997,
                    "measurement_mrid": "_ae219728-4077-433b-881e-a043e6f39d09"
                },
                {
                    "angle": 86.6754433618889,
                    "magnitude": 119.757852080379,
                    "measurement_mrid": "_5e506f55-a09e-46ff-892a-efb04f1e009e"
                },
                {
                    "angle": 86.6929766813147,
                    "magnitude": 119.431921659626,
                    "measurement_mrid": "_954070ea-b941-4d11-a7ce-28d5d870f7ca"
                },
                {
                    "angle": 86.4266773122006,
                    "magnitude": 7387.39912607476,
                    "measurement_mrid": "_0d21ddb7-d63b-4096-9723-0e7221945c12"
                },
                {
                    "angle": -35.6112005422995,
                    "magnitude": 8345.06171983328,
                    "measurement_mrid": "_9bbe0d5f-731d-4a60-9b02-aecfcdabbaea"
                },
                {
                    "angle": -156.211049169377,
                    "magnitude": 7997.35708610944,
                    "measurement_mrid": "_df9344b7-1613-4580-9dac-c0e740889491"
                },
                {
                    "angle": -35.6683106817057,
                    "magnitude": 131.949569910161,
                    "measurement_mrid": "_0804173c-251e-4e0d-9562-7da38b2ed80c"
                },
                {
                    "angle": -35.6544650098015,
                    "magnitude": 131.665309057046,
                    "measurement_mrid": "_312f54df-d688-480f-a86b-dd674dcfd622"
                },
                {
                    "angle": 86.9635480315931,
                    "magnitude": 120.818959450277,
                    "measurement_mrid": "_1d0ea2f8-862a-4a5c-85ad-265b646e2119"
                },
                {
                    "angle": 86.9635480315931,
                    "magnitude": 120.818959450277,
                    "measurement_mrid": "_1f4355d4-e02c-4d64-a657-b8d62ebd3321"
                },
                {
                    "angle": -35.7050712099688,
                    "magnitude": 8262.0989650043,
                    "measurement_mrid": "_2e20cbfd-cf58-4375-a70f-8253d587a3d2"
                },
                {
                    "angle": -156.182515403719,
                    "magnitude": 8002.29874660939,
                    "measurement_mrid": "_5cb4f8cd-9159-47a1-9966-8928b4d943bc"
                },
                {
                    "angle": 86.4347091324698,
                    "magnitude": 7389.93773050918,
                    "measurement_mrid": "_963a80ce-8e3a-48fd-91ef-b2c1c00a04fe"
                },
                {
                    "angle": -35.5911285907268,
                    "magnitude": 8351.58461263084,
                    "measurement_mrid": "_c3f9882b-eea5-40f2-8bd4-ac58fddffa85"
                },
                {
                    "angle": -35.5766125885451,
                    "magnitude": 8356.9164759066,
                    "measurement_mrid": "_3f968ea7-803c-43df-996d-30daa7f0fe5b"
                },
                {
                    "angle": 86.4421822243934,
                    "magnitude": 7391.81205251574,
                    "measurement_mrid": "_43c29252-a414-482e-b2c5-54e46f1c9662"
                },
                {
                    "angle": -156.156382473695,
                    "magnitude": 8006.93042406074,
                    "measurement_mrid": "_79a70779-eb30-4649-a795-d43f1b6d1bf7"
                },
                {
                    "angle": 86.487679017363,
                    "magnitude": 7404.53834313711,
                    "measurement_mrid": "_3ae814e0-a361-404f-8978-b1a923b3f3aa"
                },
                {
                    "angle": -35.4997711997771,
                    "magnitude": 8378.9908617934,
                    "measurement_mrid": "_4d5becc5-f001-4b36-a0ff-bbc0f12e5c91"
                },
                {
                    "angle": -156.101866646891,
                    "magnitude": 8017.69227478115,
                    "measurement_mrid": "_10a741b4-d569-43bb-9d3f-74cc44a138c7"
                },
                {
                    "angle": 86.4695059436458,
                    "magnitude": 7399.38132466939,
                    "measurement_mrid": "_b95d460e-0cec-46bd-9483-bc6238081a87"
                },
                {
                    "angle": -35.5304231045359,
                    "magnitude": 8370.40739845822,
                    "measurement_mrid": "_c30e1124-3e04-4930-b860-755213d1af17"
                },
                {
                    "angle": 88.9435953951856,
                    "magnitude": 7247.08374190283,
                    "measurement_mrid": "_3770272d-07ba-4a53-98ef-6f85865a4ce2"
                },
                {
                    "angle": -36.0252962763291,
                    "magnitude": 138.083481049195,
                    "measurement_mrid": "_375e58a0-1536-4ccd-8342-466a45b585eb"
                },
                {
                    "angle": -35.9922343111329,
                    "magnitude": 137.372810181965,
                    "measurement_mrid": "_f3ae0fae-b079-4e7b-bfb4-6bd7c50310fa"
                },
                {
                    "angle": -156.886508225286,
                    "magnitude": 130.377132614096,
                    "measurement_mrid": "_c4327586-3899-487b-a4e7-a926c1e2f541"
                },
                {
                    "angle": -156.871086594002,
                    "magnitude": 130.065096042602,
                    "measurement_mrid": "_f7c8e221-fa3e-408c-9b7e-5fbe120c4668"
                },
                {
                    "angle": -35.2434755984363,
                    "magnitude": 128.441898048377,
                    "measurement_mrid": "_4c116919-30b6-477c-9894-2accada8912c"
                },
                {
                    "angle": -35.2434755984363,
                    "magnitude": 128.441898048377,
                    "measurement_mrid": "_a7312580-c237-48a3-a38c-75d09f9ab31c"
                },
                {
                    "angle": -35.7018288288715,
                    "magnitude": 8262.61492879399,
                    "measurement_mrid": "_ee17f02a-071e-4660-bd02-a750a6ab8c16"
                },
                {
                    "angle": -156.776664759791,
                    "magnitude": 131.321653674215,
                    "measurement_mrid": "_0b8b9fae-aca4-4027-aa02-62289374b039"
                },
                {
                    "angle": -156.761352665398,
                    "magnitude": 131.009616878699,
                    "measurement_mrid": "_fde04352-5549-4a29-b8c2-ef42ab31cd72"
                },
                {
                    "angle": -34.824654360315,
                    "magnitude": 7763.42776513952,
                    "measurement_mrid": "_859dcb69-7451-4301-8b4d-da526dd0dcc7"
                },
                {
                    "angle": -32.8742361422878,
                    "magnitude": 7319.63988903765,
                    "measurement_mrid": "_8519d404-e45b-4ba8-9877-5681d4aefa07"
                },
                {
                    "angle": -36.0889685611514,
                    "magnitude": 136.510046007935,
                    "measurement_mrid": "_36682dab-b8ee-4759-a66b-d2fb1aa5576e"
                },
                {
                    "angle": -36.1111916680058,
                    "magnitude": 136.984000185463,
                    "measurement_mrid": "_84ee2756-1d2f-42c7-911d-699bbfe2fbd2"
                },
                {
                    "angle": -35.6976597168114,
                    "magnitude": 8264.91873437151,
                    "measurement_mrid": "_2a0cb96a-e7b1-4720-a292-bab6c9da0671"
                },
                {
                    "angle": -35.709396495158,
                    "magnitude": 8260.86714389413,
                    "measurement_mrid": "_9d7fd0cd-9d08-4698-a3d4-f7b4de4e1290"
                },
                {
                    "angle": -34.8399539047931,
                    "magnitude": 7709.62539045648,
                    "measurement_mrid": "_80a05162-b2e3-4a6e-96d3-047ee54e4bed"
                },
                {
                    "angle": -34.861527751472,
                    "magnitude": 7744.14193796017,
                    "measurement_mrid": "_cfebd9c5-798e-4727-aad4-eda72163811a"
                },
                {
                    "angle": -155.083343605351,
                    "magnitude": 7720.50012132911,
                    "measurement_mrid": "_bb519f05-81ce-4fb6-a543-224084ccf1de"
                },
                {
                    "angle": -36.1000992470195,
                    "magnitude": 136.747020929168,
                    "measurement_mrid": "_147be7a6-1a41-43b3-ab91-ea138cfec5ea"
                },
                {
                    "angle": -36.1000992470195,
                    "magnitude": 136.747020929168,
                    "measurement_mrid": "_4c947a22-f59f-49aa-9923-0001fcd3c7e9"
                },
                {
                    "angle": -35.8705609585806,
                    "magnitude": 8235.63138052193,
                    "measurement_mrid": "_df77144d-ea83-47b2-8cf7-db4b11fd043f"
                },
                {
                    "angle": -155.73638903532,
                    "magnitude": 7733.46660303379,
                    "measurement_mrid": "_f7167113-d57a-4d6a-bc3d-e8326a1f4a1c"
                },
                {
                    "angle": -35.2811202562445,
                    "magnitude": 127.836040658735,
                    "measurement_mrid": "_c5e1278f-ef4a-42dd-8418-12605996f302"
                },
                {
                    "angle": -35.2906441704772,
                    "magnitude": 128.025725517241,
                    "measurement_mrid": "_d6e01114-7223-482e-a373-e484cf0b9fb1"
                },
                {
                    "angle": 86.5052344078395,
                    "magnitude": 122.042932514586,
                    "measurement_mrid": "_95b44a8c-8d89-4fdf-97ba-b1da07bbd064"
                },
                {
                    "angle": 86.5224394607339,
                    "magnitude": 121.717001905155,
                    "measurement_mrid": "_e5df4078-a856-4da7-a830-2e6e8c677f86"
                },
                {
                    "angle": -155.546928752656,
                    "magnitude": 127.251552780936,
                    "measurement_mrid": "_2314cd94-cfdf-46a5-9a2f-8d1a2d06e416"
                },
                {
                    "angle": -155.57311922315,
                    "magnitude": 127.771447276091,
                    "measurement_mrid": "_cc33efcb-f673-4ebd-afe2-12d8f6c516d8"
                },
                {
                    "angle": -35.2682919010216,
                    "magnitude": 127.487763773258,
                    "measurement_mrid": "_1ee682bf-5a20-4185-a4e8-00f7f4d5a069"
                },
                {
                    "angle": -35.2682919010216,
                    "magnitude": 127.487763773258,
                    "measurement_mrid": "_a61c5fb7-69f8-43a8-bade-5f3093f69c5b"
                },
                {
                    "angle": -35.8019331927993,
                    "magnitude": 8265.73425800683,
                    "measurement_mrid": "_235be630-4e17-4d34-bf04-3f412c4feee8"
                },
                {
                    "angle": -35.8004352872469,
                    "magnitude": 8266.59863045792,
                    "measurement_mrid": "_3be3728b-f550-4d8c-9c56-eff572e9f963"
                },
                {
                    "angle": 85.9527009023026,
                    "magnitude": 121.678072948158,
                    "measurement_mrid": "_73621e06-3047-4831-827c-59076996eb3d"
                },
                {
                    "angle": 85.9240598020335,
                    "magnitude": 122.221473525028,
                    "measurement_mrid": "_cd2c185d-b061-4ef3-a044-afd42466aa18"
                },
                {
                    "angle": -153.732448278922,
                    "magnitude": 7272.84747573803,
                    "measurement_mrid": "_b479e0a7-ffb5-4a8c-aa1b-7740cc2b39a2"
                },
                {
                    "angle": -33.6282717035885,
                    "magnitude": 7297.6016221693,
                    "measurement_mrid": "_ce9551ca-39f9-4f5b-982b-39a73ab31307"
                },
                {
                    "angle": 86.7962489490255,
                    "magnitude": 7264.93723585064,
                    "measurement_mrid": "_e7b86678-f05f-4f19-ac69-cbb52eab1652"
                },
                {
                    "angle": -34.8133671646232,
                    "magnitude": 128.949476023397,
                    "measurement_mrid": "_23de4223-96d4-43ec-bf49-dfbc4947ed18"
                },
                {
                    "angle": -34.7991927749018,
                    "magnitude": 128.665216120965,
                    "measurement_mrid": "_61094b8a-b482-436a-b124-f8c4cb635160"
                },
                {
                    "angle": -36.1369597372243,
                    "magnitude": 136.388732964541,
                    "measurement_mrid": "_799fe909-76fa-4280-8982-fd79065e1778"
                },
                {
                    "angle": -36.1369597372243,
                    "magnitude": 136.388732964541,
                    "measurement_mrid": "_bf7f6dbf-5653-48ba-98b9-67fa936b20c9"
                },
                {
                    "angle": -153.537260584563,
                    "magnitude": 121.044808230109,
                    "measurement_mrid": "_0c597b34-a6f6-421b-af9b-38514885e8bd"
                },
                {
                    "angle": -153.526199183852,
                    "magnitude": 120.836962646425,
                    "measurement_mrid": "_8eda41af-2c95-429e-9275-562de325b597"
                },
                {
                    "angle": -155.605164604387,
                    "magnitude": 127.186011382851,
                    "measurement_mrid": "_733f9823-541b-46a9-9d03-fc5ecad179d8"
                },
                {
                    "angle": -155.605164604387,
                    "magnitude": 127.186011382851,
                    "measurement_mrid": "_dc3e4a73-38b7-4fab-b1ce-ef97e8f50f9e"
                },
                {
                    "angle": -35.7094113543838,
                    "magnitude": 8260.85929089339,
                    "measurement_mrid": "_8e6a9cb9-3268-467e-9fb6-44eee4e4af52"
                },
                {
                    "angle": -35.7860757626676,
                    "magnitude": 8293.95354852825,
                    "measurement_mrid": "_96a21f5a-719b-4990-be45-9bf32ecbfcbf"
                },
                {
                    "angle": -35.5910369980172,
                    "magnitude": 8312.51461151329,
                    "measurement_mrid": "_135df015-a472-4a94-ab28-b3effb82309c"
                },
                {
                    "angle": 86.8020308530217,
                    "magnitude": 120.612252376574,
                    "measurement_mrid": "_bc4641cd-4c7a-4645-89b6-0f4c5904882a"
                },
                {
                    "angle": 86.8020308530217,
                    "magnitude": 120.612252376574,
                    "measurement_mrid": "_ee1285d6-a09b-4fa3-b42d-e2580390d9c4"
                },
                {
                    "angle": -35.9070490352493,
                    "magnitude": 137.679751994693,
                    "measurement_mrid": "_26ce565e-c166-462c-8c48-d2d3a60c1c42"
                },
                {
                    "angle": -35.9070490352493,
                    "magnitude": 137.679751994693,
                    "measurement_mrid": "_f6061b60-b3e7-45d9-8c18-3122d9ec2773"
                },
                {
                    "angle": 85.7291251641003,
                    "magnitude": 122.198144752305,
                    "measurement_mrid": "_651dd713-5973-41e1-8a9d-04cbcab7d8db"
                },
                {
                    "angle": 85.7291251641003,
                    "magnitude": 122.198144752305,
                    "measurement_mrid": "_82056806-f735-4c5c-8aa1-ea8bb07d784b"
                },
                {
                    "angle": 86.3885984814797,
                    "magnitude": 7365.0327318838,
                    "measurement_mrid": "_f64be9e5-2718-49ba-a3cc-51d9e0444416"
                },
                {
                    "angle": -156.798445039229,
                    "magnitude": 131.635431939265,
                    "measurement_mrid": "_a321b954-ba5b-4466-8a02-6eb620e9e366"
                },
                {
                    "angle": -156.823797860118,
                    "magnitude": 132.155318684811,
                    "measurement_mrid": "_e94affb0-bf0f-4420-a130-ddc1bf54c5ef"
                },
                {
                    "angle": -156.438026748895,
                    "magnitude": 7882.82107507421,
                    "measurement_mrid": "_16e7d6e6-77ce-4bd1-981d-ecb3f2568f4b"
                },
                {
                    "angle": -35.8664000227336,
                    "magnitude": 8237.11293262118,
                    "measurement_mrid": "_2556d12d-44d7-45c9-919f-e023d780ad41"
                },
                {
                    "angle": -156.955013473522,
                    "magnitude": 130.974646257429,
                    "measurement_mrid": "_3b2d14b6-a222-4bc5-8c56-bd2f381d0de3"
                },
                {
                    "angle": -156.955013473522,
                    "magnitude": 130.974646257429,
                    "measurement_mrid": "_c3eca978-1eba-4c0a-9378-af5ee32e766d"
                },
                {
                    "angle": -35.697469608202,
                    "magnitude": 8264.29317127553,
                    "measurement_mrid": "_d9700d4f-7c5f-476a-a6c2-027f3781b01f"
                },
                {
                    "angle": -35.2426457974602,
                    "magnitude": 128.448833856034,
                    "measurement_mrid": "_9412511e-5404-4ad0-9293-4bbe288c4907"
                },
                {
                    "angle": -35.2426457974602,
                    "magnitude": 128.448833856034,
                    "measurement_mrid": "_e30c1d0d-a9aa-42f1-a7aa-b38c6335248e"
                },
                {
                    "angle": -35.7517538724644,
                    "magnitude": 8305.31920492224,
                    "measurement_mrid": "_e9cd4eb2-45e7-4ccd-955b-4343e02590e6"
                },
                {
                    "angle": -152.206103598637,
                    "magnitude": 120.803395848296,
                    "measurement_mrid": "_328c9038-8b95-478b-bd66-49325dec87d2"
                },
                {
                    "angle": -152.222699662245,
                    "magnitude": 121.11543354899,
                    "measurement_mrid": "_a4b25ac4-2a59-496f-8d72-75af594ea835"
                },
                {
                    "angle": -156.849068757862,
                    "magnitude": 130.473882421248,
                    "measurement_mrid": "_5f9cf33c-53b4-42fc-aab6-cd6d20446fd0"
                },
                {
                    "angle": -156.849068757862,
                    "magnitude": 130.473882421248,
                    "measurement_mrid": "_af749739-0ab1-4c19-bfc2-f67736866676"
                },
                {
                    "angle": -156.87954643744,
                    "magnitude": 130.215189106829,
                    "measurement_mrid": "_d96a1d95-2f9f-4fd4-a47e-f7a5fdb9bb06"
                },
                {
                    "angle": -156.87954643744,
                    "magnitude": 130.215189106829,
                    "measurement_mrid": "_df3fac33-9ce2-4159-baf4-e293b5957b6b"
                },
                {
                    "angle": 86.6514305469479,
                    "magnitude": 119.723632818541,
                    "measurement_mrid": "_1e8e00e4-9a55-41d6-aa90-1d27feb5607c"
                },
                {
                    "angle": 86.6806700270043,
                    "magnitude": 119.180230986542,
                    "measurement_mrid": "_7d58b8ef-c7b4-4817-95be-d38372ac3858"
                },
                {
                    "angle": -154.5557951142,
                    "magnitude": 120.419441067525,
                    "measurement_mrid": "_49488b7f-92d0-486d-b416-2e784b08f537"
                },
                {
                    "angle": -154.5557951142,
                    "magnitude": 120.419441067525,
                    "measurement_mrid": "_5aad7845-6d02-4863-a64e-1b6fc2c50722"
                },
                {
                    "angle": -156.127076166856,
                    "magnitude": 7980.01298124122,
                    "measurement_mrid": "_8a18c876-3f27-4d46-bd24-a25fd856d7a5"
                },
                {
                    "angle": -34.7810494612611,
                    "magnitude": 7993.93663869212,
                    "measurement_mrid": "_f392b800-1c48-44a7-8354-7a17ea49de99"
                },
                {
                    "angle": -34.1062155415576,
                    "magnitude": 119.94047305198,
                    "measurement_mrid": "_7f8d965d-33f4-4b33-b686-f2a433481137"
                },
                {
                    "angle": -34.1062155415576,
                    "magnitude": 119.94047305198,
                    "measurement_mrid": "_bbc6f710-f7f9-4219-9a01-e926db31e429"
                },
                {
                    "angle": -156.910227373321,
                    "magnitude": 131.595059827907,
                    "measurement_mrid": "_53647cf9-6333-481d-a535-1f7a9fd88065"
                },
                {
                    "angle": -156.894945921377,
                    "magnitude": 131.28302424754,
                    "measurement_mrid": "_90482f1e-fdc9-4a93-8f7b-0f8208d24afd"
                },
                {
                    "angle": -156.167376994089,
                    "magnitude": 128.109201737897,
                    "measurement_mrid": "_14493df4-cd14-4ed1-8528-334ac99142f5"
                },
                {
                    "angle": -156.167376994089,
                    "magnitude": 128.109201737897,
                    "measurement_mrid": "_5a59441e-9ea2-452e-90fe-7ba00b66276b"
                },
                {
                    "angle": 86.3890457281449,
                    "magnitude": 7363.37715800422,
                    "measurement_mrid": "_e7b8894c-fee0-44b9-9dfc-34451dea1e0d"
                },
                {
                    "angle": -156.903602287977,
                    "magnitude": 130.259580234925,
                    "measurement_mrid": "_735d86e9-2616-4046-a27b-af99a0d27728"
                },
                {
                    "angle": -156.903602287977,
                    "magnitude": 130.259580234925,
                    "measurement_mrid": "_d443520d-3919-4b29-a9ba-740e650caa88"
                },
                {
                    "angle": 85.7521077708576,
                    "magnitude": 122.385544019205,
                    "measurement_mrid": "_0a83cb5a-8031-43e9-8fc2-f683881634a4"
                },
                {
                    "angle": 85.7521077708576,
                    "magnitude": 122.385544019205,
                    "measurement_mrid": "_78892fe1-f749-45d4-a9e4-d58f3e56b8d7"
                },
                {
                    "angle": 86.7096523936174,
                    "magnitude": 119.79782971854,
                    "measurement_mrid": "_9dd022f8-1c6c-4f7a-8190-21653d21670e"
                },
                {
                    "angle": 86.7096523936174,
                    "magnitude": 119.79782971854,
                    "measurement_mrid": "_e7b5387a-5256-4329-b120-d72d74372928"
                },
                {
                    "angle": 86.275046258446,
                    "magnitude": 7338.66808463636,
                    "measurement_mrid": "_32c0fd7f-3377-4ce1-9f74-46248a026988"
                },
                {
                    "angle": 86.2567029434777,
                    "magnitude": 7409.24684064154,
                    "measurement_mrid": "_2f984474-3d4f-4e9a-8567-0cdfffe6ba4c"
                },
                {
                    "angle": -34.9383458569089,
                    "magnitude": 7985.32957379416,
                    "measurement_mrid": "_0cc4aece-85bd-4934-bc65-d3b9a98f0d05"
                },
                {
                    "angle": 86.7938243565427,
                    "magnitude": 7389.69277236099,
                    "measurement_mrid": "_dc2805c7-16af-4cba-b508-304195cd237f"
                },
                {
                    "angle": -155.466337799588,
                    "magnitude": 7770.23960027583,
                    "measurement_mrid": "_f211e7ea-fffd-4f68-9919-c0dfc849ad1b"
                },
                {
                    "angle": 85.9451355614802,
                    "magnitude": 121.445165957555,
                    "measurement_mrid": "_069908f4-a7f0-4648-b1d0-42b61d0564fb"
                },
                {
                    "angle": 85.9278928300376,
                    "magnitude": 121.771095632562,
                    "measurement_mrid": "_db727a88-a3df-41a7-b966-e90cb0e06418"
                },
                {
                    "angle": -153.795456633498,
                    "magnitude": 7303.17504181127,
                    "measurement_mrid": "_650cd116-b933-4702-a239-84de1d08668e"
                },
                {
                    "angle": -35.9966206425932,
                    "magnitude": 137.894369874036,
                    "measurement_mrid": "_be01371a-51c1-40bf-84b2-94bfcc917a63"
                },
                {
                    "angle": -35.9635158307074,
                    "magnitude": 137.183697871447,
                    "measurement_mrid": "_cbff4427-fefb-494d-9864-5bd18784eacf"
                },
                {
                    "angle": 85.9345306675397,
                    "magnitude": 121.743673649998,
                    "measurement_mrid": "_81d23449-a055-47f7-a034-077bc3fe382f"
                },
                {
                    "angle": 85.9345306675397,
                    "magnitude": 121.743673649998,
                    "measurement_mrid": "_cf622143-712d-4f96-91cb-ccc8eb09aff5"
                },
                {
                    "angle": 71.5085689699087,
                    "magnitude": 9.14551698507307,
                    "measurement_mrid": "_bc66f0c1-8928-4e65-95ae-2e510ef11ee4"
                },
                {
                    "angle": -153.736944448986,
                    "magnitude": 7304.33576863755,
                    "measurement_mrid": "_0c708c0e-97bb-43ea-aa58-2765f706a395"
                },
                {
                    "angle": -33.5185617769328,
                    "magnitude": 7262.06772884729,
                    "measurement_mrid": "_1fc6a3b1-c372-4b00-9876-7e6a1d2602a4"
                },
                {
                    "angle": 87.4782668762778,
                    "magnitude": 7313.83632607301,
                    "measurement_mrid": "_ec380b8a-5aed-4db9-9f02-8c5ed990e419"
                },
                {
                    "angle": -33.5471559415158,
                    "magnitude": 7260.24907780113,
                    "measurement_mrid": "_545dfb6f-9820-4a9a-bfe6-dd4ec1ef7e57"
                },
                {
                    "angle": -153.77044417723,
                    "magnitude": 7303.82615086959,
                    "measurement_mrid": "_a045678b-8304-4068-8309-d2d24985c03d"
                },
                {
                    "angle": 87.4670559944174,
                    "magnitude": 7314.23246890413,
                    "measurement_mrid": "_da317a9e-62d4-4844-ab65-354bb8f47e98"
                },
                {
                    "angle": -156.894297522777,
                    "magnitude": 131.549950432948,
                    "measurement_mrid": "_239ab03e-5b35-40f3-bc39-1a21fe584d2a"
                },
                {
                    "angle": -156.894297522777,
                    "magnitude": 131.549950432948,
                    "measurement_mrid": "_a6cc599a-c720-4548-bd6e-7360ea0cf22a"
                },
                {
                    "angle": -155.568717300813,
                    "magnitude": 7768.85038077686,
                    "measurement_mrid": "_04bb7ec6-9c4d-4b7d-833e-676882297428"
                },
                {
                    "angle": 86.7510688097989,
                    "magnitude": 7392.31566138373,
                    "measurement_mrid": "_c74ffdd1-0a5a-48af-9558-bce0ed6f1937"
                },
                {
                    "angle": -35.0112176179124,
                    "magnitude": 7981.21706830896,
                    "measurement_mrid": "_cfc6851a-19dc-48bd-9ad2-b8cb13822d13"
                },
                {
                    "angle": 86.2538178711689,
                    "magnitude": 7407.78553600702,
                    "measurement_mrid": "_a9ec548c-aef0-42a1-b2fa-68c9c14eac23"
                },
                {
                    "angle": 86.2541004458831,
                    "magnitude": 7407.92868389906,
                    "measurement_mrid": "_2373b3b6-738a-44df-bebb-457d761f7e08"
                },
                {
                    "angle": -35.9990421382979,
                    "magnitude": 137.841613081465,
                    "measurement_mrid": "_1fdade60-f99b-4095-8f1b-fec8f872e4ef"
                },
                {
                    "angle": -35.9769543166521,
                    "magnitude": 137.367660004877,
                    "measurement_mrid": "_487db7e7-a838-436e-8a50-1882ff039c99"
                },
                {
                    "angle": -34.7809699747549,
                    "magnitude": 7993.98241494171,
                    "measurement_mrid": "_6a3b0635-af90-4471-a800-ceccc7b50b41"
                },
                {
                    "angle": -36.1045697064431,
                    "magnitude": 136.738023795708,
                    "measurement_mrid": "_3872f1ca-3b67-4c19-8e07-cae695871efb"
                },
                {
                    "angle": -36.1045697064431,
                    "magnitude": 136.738023795708,
                    "measurement_mrid": "_737bda1a-6984-4ca5-9bcf-7ab9d37e1ead"
                },
                {
                    "angle": -154.583762020898,
                    "magnitude": 128.038404206185,
                    "measurement_mrid": "_7fcb0ed3-8b80-4fb6-9d8d-acee115669f8"
                },
                {
                    "angle": -154.622727680563,
                    "magnitude": 128.817987175486,
                    "measurement_mrid": "_f54a9db1-983c-4b67-9a9e-cb36024693f3"
                },
                {
                    "angle": 87.1710031198735,
                    "magnitude": 120.715586654643,
                    "measurement_mrid": "_e563f7b1-c624-4034-a6de-5e06d86bec89"
                },
                {
                    "angle": 87.1710031198735,
                    "magnitude": 120.715586654643,
                    "measurement_mrid": "_f73ff9ff-4e8e-471c-9718-cec9e540bf5f"
                },
                {
                    "angle": -156.454972609304,
                    "magnitude": 7945.76365476333,
                    "measurement_mrid": "_628d8e68-1f09-43bc-857b-ce0d939ba6b4"
                },
                {
                    "angle": 86.3470040602399,
                    "magnitude": 7335.10449920914,
                    "measurement_mrid": "_2559e2a6-286c-476e-a55d-ee879b70c868"
                },
                {
                    "angle": 86.7751274676899,
                    "magnitude": 120.317293946806,
                    "measurement_mrid": "_5a5b0b7f-cd73-4f66-a62f-582fd7e594f2"
                },
                {
                    "angle": 86.7751274676899,
                    "magnitude": 120.317293946806,
                    "measurement_mrid": "_7b633a26-30c1-4e02-8719-c7712872eab6"
                },
                {
                    "angle": 85.7639134981127,
                    "magnitude": 122.330056127602,
                    "measurement_mrid": "_618e9108-a6cb-4b6f-8965-57dd4bba1402"
                },
                {
                    "angle": 85.7524823172734,
                    "magnitude": 122.547520647046,
                    "measurement_mrid": "_7469705b-c153-4293-96b0-41c0170cd642"
                },
                {
                    "angle": -156.452912831197,
                    "magnitude": 7946.39813350474,
                    "measurement_mrid": "_1d23ff0a-e095-4085-aa34-1b94aaf1c58e"
                },
                {
                    "angle": -35.8368482113838,
                    "magnitude": 8253.6268044316,
                    "measurement_mrid": "_7bc1bd2b-3f09-4fe2-9c75-250124b7a843"
                },
                {
                    "angle": 86.3616976845167,
                    "magnitude": 7343.86541540056,
                    "measurement_mrid": "_e113f1af-1a54-4be4-8093-ae792a3a1693"
                },
                {
                    "angle": -35.8349454424778,
                    "magnitude": 8255.11309762966,
                    "measurement_mrid": "_62079bf0-089a-40dd-b19a-9820f1790c40"
                },
                {
                    "angle": 86.3631661611484,
                    "magnitude": 7345.04660343817,
                    "measurement_mrid": "_c39b1389-daff-42ef-86c9-bf3e6e400426"
                },
                {
                    "angle": -156.453350001694,
                    "magnitude": 7946.81278628021,
                    "measurement_mrid": "_f6c9981b-bee2-4a35-bb37-6cfd8eab8fb8"
                },
                {
                    "angle": 86.2771619892498,
                    "magnitude": 7339.28305286827,
                    "measurement_mrid": "_1b2089d6-a11a-499a-97ec-cf4a8607e834"
                },
                {
                    "angle": 85.8421521167958,
                    "magnitude": 121.424861529573,
                    "measurement_mrid": "_30cae738-381d-4f48-b382-db36bcafb495"
                },
                {
                    "angle": 85.8594438267873,
                    "magnitude": 121.098930363751,
                    "measurement_mrid": "_f62fd8ac-d18a-4cd0-8d7c-f06ac0c63055"
                },
                {
                    "angle": -35.2741449140694,
                    "magnitude": 127.641772365149,
                    "measurement_mrid": "_ac895ba9-5f2b-49a7-b79d-248e8ca910ec"
                },
                {
                    "angle": -35.2598316619252,
                    "magnitude": 127.35751168263,
                    "measurement_mrid": "_eef60ded-68db-4c3d-a0e3-9ad92dff5976"
                },
                {
                    "angle": -156.359615790481,
                    "magnitude": 7913.55595459193,
                    "measurement_mrid": "_071f072c-2daf-4b72-a862-02581514dfca"
                },
                {
                    "angle": -35.5903416543088,
                    "magnitude": 8312.61309319243,
                    "measurement_mrid": "_d2ec1b2f-9c99-4403-a572-3a854a204602"
                },
                {
                    "angle": 86.1067284230958,
                    "magnitude": 7325.02490579807,
                    "measurement_mrid": "_f3a63c50-185f-4812-b56e-b739b52bff56"
                },
                {
                    "angle": -155.605612653019,
                    "magnitude": 127.180882736175,
                    "measurement_mrid": "_a694979f-e689-4cbb-adda-e5593b307b4b"
                },
                {
                    "angle": -155.605612653019,
                    "magnitude": 127.180882736175,
                    "measurement_mrid": "_cbfe37b2-ebb6-4eb3-b22a-b50a268fdb3b"
                },
                {
                    "angle": 86.7220645669218,
                    "magnitude": 7397.64093599658,
                    "measurement_mrid": "_5273f714-5989-4bd2-ae9b-d832259f271d"
                },
                {
                    "angle": -35.88379745866,
                    "magnitude": 8231.36038160113,
                    "measurement_mrid": "_5227261b-9349-45dc-b2a2-ca4dadcead46"
                },
                {
                    "angle": -35.8455147633213,
                    "magnitude": 138.895596035091,
                    "measurement_mrid": "_4ea675ae-04d2-4fae-8b81-9466da204132"
                },
                {
                    "angle": -35.8455147633213,
                    "magnitude": 138.895596035091,
                    "measurement_mrid": "_8ca61757-d942-43a7-8191-9713e16927a9"
                },
                {
                    "angle": -33.2062070188831,
                    "magnitude": 121.369220075298,
                    "measurement_mrid": "_525fd6c8-a71f-4279-987a-320ed61831df"
                },
                {
                    "angle": -33.1559509630567,
                    "magnitude": 120.421307130235,
                    "measurement_mrid": "_d7b7da65-f24e-4bb3-8e82-2137d11e5423"
                },
                {
                    "angle": -35.816946209943,
                    "magnitude": 8264.12919761296,
                    "measurement_mrid": "_84cfe785-be54-4d0b-92a8-0ef2c5ef5eb3"
                },
                {
                    "angle": -35.833711346209,
                    "magnitude": 8256.07588920135,
                    "measurement_mrid": "_335106b0-543e-4ed5-9cbd-360d7c8d3ba9"
                },
                {
                    "angle": 86.3641184108642,
                    "magnitude": 7345.81174912389,
                    "measurement_mrid": "_40e60a5f-4496-4ff7-afc3-5f75ffb93807"
                },
                {
                    "angle": -156.453632016891,
                    "magnitude": 7947.08131565571,
                    "measurement_mrid": "_95bfdf04-6f49-41d6-9a54-827bb9730ba8"
                },
                {
                    "angle": -35.833711346209,
                    "magnitude": 8256.07588920135,
                    "measurement_mrid": "_b34b0fc4-3ac9-4753-86ae-05365c7edbe8"
                },
                {
                    "angle": 86.3641184108642,
                    "magnitude": 7345.81174912389,
                    "measurement_mrid": "_dcb8e63f-d7fb-40a7-ad4f-c03f748f55df"
                },
                {
                    "angle": -156.453632016891,
                    "magnitude": 7947.08131565571,
                    "measurement_mrid": "_e10f68c4-75be-4840-8466-d16d7bab1a78"
                },
                {
                    "angle": -34.3672977696761,
                    "magnitude": 7779.78332772396,
                    "measurement_mrid": "_95f38c79-63d3-411e-98b7-6092b18d545e"
                },
                {
                    "angle": -35.7898941014361,
                    "magnitude": 8293.24206237765,
                    "measurement_mrid": "_1b69bc9f-c0a6-454e-ba38-448287d62886"
                },
                {
                    "angle": -35.9703552654793,
                    "magnitude": 137.290496968658,
                    "measurement_mrid": "_0c968d8c-3834-44ad-94ec-0d0dc9c4e4be"
                },
                {
                    "angle": -35.9924547411529,
                    "magnitude": 137.764450011721,
                    "measurement_mrid": "_870fd429-e0ca-4e9d-997a-5b3d6c234598"
                },
                {
                    "angle": -153.445716972548,
                    "magnitude": 121.110055466869,
                    "measurement_mrid": "_5f7f984d-f974-4797-b244-6fbf52556e42"
                },
                {
                    "angle": -153.429119391984,
                    "magnitude": 120.798016927941,
                    "measurement_mrid": "_84c239e7-c2a1-43bc-9672-618d3df4fee4"
                },
                {
                    "angle": 86.3897156350602,
                    "magnitude": 7367.24623264624,
                    "measurement_mrid": "_9ece7f51-8aef-48dd-a44e-94d367af1908"
                },
                {
                    "angle": -33.6304393711931,
                    "magnitude": 7296.80345397057,
                    "measurement_mrid": "_28284432-f19c-473d-bc60-5c21bc3b0ec7"
                },
                {
                    "angle": 85.7700547760272,
                    "magnitude": 122.150828086641,
                    "measurement_mrid": "_267a3927-8236-40c7-a8ad-ee3e7aa9e107"
                },
                {
                    "angle": 85.7415257616359,
                    "magnitude": 122.694229597593,
                    "measurement_mrid": "_9a766e14-1551-46c0-88ac-5655d44ebf5c"
                },
                {
                    "angle": 85.8427259900363,
                    "magnitude": 121.199782130853,
                    "measurement_mrid": "_2e768dcd-1767-4155-885b-bebf340b7b2a"
                },
                {
                    "angle": 85.8427259900363,
                    "magnitude": 121.199782130853,
                    "measurement_mrid": "_3bc2f0c0-a6d9-4703-84ff-81f980dadd8b"
                },
                {
                    "angle": 86.4872514821436,
                    "magnitude": 7404.41226136648,
                    "measurement_mrid": "_6d3def07-d294-4da7-a487-3a9c8e397d15"
                },
                {
                    "angle": -156.116975847844,
                    "magnitude": 7980.9052434539,
                    "measurement_mrid": "_62b5f019-e3dd-477f-b9c7-926b631cc854"
                },
                {
                    "angle": -35.7116661572596,
                    "magnitude": 8260.92735945936,
                    "measurement_mrid": "_76ffe4d6-1f09-4041-8d1b-1ccafbb20238"
                },
                {
                    "angle": 86.4723582874266,
                    "magnitude": 7316.53190559938,
                    "measurement_mrid": "_e4c96ad2-8620-4684-adba-87b67400e53e"
                },
                {
                    "angle": -35.9241298976328,
                    "magnitude": 137.741052144073,
                    "measurement_mrid": "_05b08e6a-b2c7-4c49-b42f-c6772b3a5516"
                },
                {
                    "angle": -35.9241298976328,
                    "magnitude": 137.741052144073,
                    "measurement_mrid": "_b49fd36a-3adf-4e2d-9f93-fb3ec9e61d1c"
                },
                {
                    "angle": -156.348116369855,
                    "magnitude": 7924.10862371247,
                    "measurement_mrid": "_669f9d69-055d-43cb-a5fd-6e3ddf35a3d0"
                },
                {
                    "angle": -35.5922709191012,
                    "magnitude": 8311.81455358739,
                    "measurement_mrid": "_9ffe9035-d2a8-40f7-9cea-74f35596d46e"
                },
                {
                    "angle": 86.1796511656023,
                    "magnitude": 7334.7797454264,
                    "measurement_mrid": "_c93bd207-c875-41dd-a11f-83320f5fb5ae"
                },
                {
                    "angle": -156.208505799417,
                    "magnitude": 7997.74885457501,
                    "measurement_mrid": "_a8c46002-5e0c-426d-92ce-ca79fda6cf6b"
                },
                {
                    "angle": -35.7932789474155,
                    "magnitude": 8290.75637124407,
                    "measurement_mrid": "_a00d11ab-7203-4603-82e4-3f26da9d4e9f"
                },
                {
                    "angle": -156.210067138269,
                    "magnitude": 127.745953301443,
                    "measurement_mrid": "_9f88ddf7-f31d-4d2b-8f90-6877caad6526"
                },
                {
                    "angle": -156.210067138269,
                    "magnitude": 127.745953301443,
                    "measurement_mrid": "_d04cd3d3-403e-4ab7-ad4e-67f9025bd869"
                },
                {
                    "angle": -156.136012089333,
                    "magnitude": 128.010367849534,
                    "measurement_mrid": "_5f829fbb-1f2a-4d7b-9c16-37ee5635c59c"
                },
                {
                    "angle": -156.16207781196,
                    "magnitude": 128.530254897668,
                    "measurement_mrid": "_e45117bb-a0bd-4e5b-a2c2-5c0f29bf7b0e"
                },
                {
                    "angle": 86.4203469988195,
                    "magnitude": 7382.65341306889,
                    "measurement_mrid": "_b98910f3-5135-470e-8b9d-10bd670b32dc"
                },
                {
                    "angle": -33.7788809289687,
                    "magnitude": 7238.98244003725,
                    "measurement_mrid": "_012d290c-6b77-44bc-b134-aa7adcf5187d"
                },
                {
                    "angle": -154.056100224856,
                    "magnitude": 7292.42242657988,
                    "measurement_mrid": "_1c2b23b3-c425-4c37-b490-1ace1f0196fe"
                },
                {
                    "angle": 87.3861557365995,
                    "magnitude": 7316.82268513338,
                    "measurement_mrid": "_5621afb8-b9f5-4386-9d97-de0747675949"
                },
                {
                    "angle": -154.057467903964,
                    "magnitude": 7289.44754910853,
                    "measurement_mrid": "_29f49a69-a1ea-4580-b8f3-168d8f2f6e4d"
                },
                {
                    "angle": -33.7789604952406,
                    "magnitude": 7236.46031261739,
                    "measurement_mrid": "_d8aabf1f-d92c-4945-9f1f-555441f1548f"
                },
                {
                    "angle": 87.3850656628647,
                    "magnitude": 7314.37693409412,
                    "measurement_mrid": "_f49ef3d8-e82f-4633-a947-d3839522fbc2"
                },
                {
                    "angle": 87.3833699790771,
                    "magnitude": 7313.55960725078,
                    "measurement_mrid": "_3c672e38-95f9-4d37-9ee6-9a6ca16ef142"
                },
                {
                    "angle": -33.7796682213003,
                    "magnitude": 7235.53313537747,
                    "measurement_mrid": "_8f89b6cc-f6dc-403f-9746-2c2aaab2a7aa"
                },
                {
                    "angle": -154.059069681734,
                    "magnitude": 7288.47508324442,
                    "measurement_mrid": "_dd8b47cd-f4fb-4a1b-970b-46522addbeb3"
                },
                {
                    "angle": -36.1682082552261,
                    "magnitude": 137.351536328747,
                    "measurement_mrid": "_7d17e180-13c9-412d-9b2d-3a022326ce5b"
                },
                {
                    "angle": -36.1682082552261,
                    "magnitude": 137.351536328747,
                    "measurement_mrid": "_b2e865c1-8021-41cf-9f97-810dc56890a1"
                },
                {
                    "angle": -34.853920827416,
                    "magnitude": 7702.0905514298,
                    "measurement_mrid": "_ec4108c6-e8b0-46dc-a220-b70903393d59"
                },
                {
                    "angle": -152.949991398253,
                    "magnitude": 7319.58271294819,
                    "measurement_mrid": "_484f017f-c3ea-4fe8-8706-9dece57ece0d"
                },
                {
                    "angle": -36.0135930588297,
                    "magnitude": 137.079011106104,
                    "measurement_mrid": "_a1a895f3-4609-4833-96a3-8de38337687e"
                },
                {
                    "angle": -36.0467235504253,
                    "magnitude": 137.789681981547,
                    "measurement_mrid": "_aa3eb8fb-efac-467d-a924-f9a9b1a80ef2"
                },
                {
                    "angle": 86.6849451463797,
                    "magnitude": 119.44839115148,
                    "measurement_mrid": "_68298419-86b9-4c3f-a896-fdaaebb7b23a"
                },
                {
                    "angle": 86.6732381057731,
                    "magnitude": 119.665855443517,
                    "measurement_mrid": "_7bb1d56c-91ca-4537-bc81-7388fa5eae37"
                },
                {
                    "angle": 85.7145695741068,
                    "magnitude": 121.227319290874,
                    "measurement_mrid": "_0e814566-0f99-4a13-a83b-ed5f01cbd972"
                },
                {
                    "angle": 85.7145695741068,
                    "magnitude": 121.227319290874,
                    "measurement_mrid": "_7cee0673-2188-4d45-80d1-95b9af50cb9b"
                },
                {
                    "angle": -156.378934880814,
                    "magnitude": 7900.38860228701,
                    "measurement_mrid": "_06595329-9917-4fde-bb05-bc94cb573fe6"
                },
                {
                    "angle": -156.399300265819,
                    "magnitude": 7889.49102972379,
                    "measurement_mrid": "_6e060c6f-a7ef-4850-9ded-948be23ac070"
                },
                {
                    "angle": -36.1791955249918,
                    "magnitude": 137.274648706098,
                    "measurement_mrid": "_01968b83-bfc2-4366-b6da-c9c80af75977"
                },
                {
                    "angle": -36.1791955249918,
                    "magnitude": 137.274648706098,
                    "measurement_mrid": "_250e014d-0b65-43f8-926f-5478e4d0876b"
                },
                {
                    "angle": -35.8030821113168,
                    "magnitude": 8265.12344931429,
                    "measurement_mrid": "_168b5470-98e8-4205-878e-0a2667f869e8"
                },
                {
                    "angle": -36.1110873236824,
                    "magnitude": 136.984963173489,
                    "measurement_mrid": "_da29a3fc-8917-4f94-b006-ae8b12b13d97"
                },
                {
                    "angle": -36.0888649369065,
                    "magnitude": 136.511009462624,
                    "measurement_mrid": "_eedcdee6-e7e2-4b47-af8d-20c689ec1407"
                },
                {
                    "angle": 85.6462430772034,
                    "magnitude": 7416.81023412138,
                    "measurement_mrid": "_cf379733-86de-4b65-be28-38c515256412"
                },
                {
                    "angle": -155.08821528907,
                    "magnitude": 7717.94688024611,
                    "measurement_mrid": "_1a3702c9-d800-4155-aeda-db9c43af760e"
                },
                {
                    "angle": -32.3472429289914,
                    "magnitude": 7315.59653857137,
                    "measurement_mrid": "_9c3162cb-41cb-4a41-8bf8-f79e98e8faa1"
                },
                {
                    "angle": 86.4171409018617,
                    "magnitude": 7380.84405918731,
                    "measurement_mrid": "_cf49f7a2-0b5c-4110-863c-3086f31071e1"
                },
                {
                    "angle": -155.708307318779,
                    "magnitude": 7748.26156698485,
                    "measurement_mrid": "_a948c9e9-9c37-41b5-84f1-aa9474e85cd2"
                },
                {
                    "angle": -156.906146631186,
                    "magnitude": 130.246575039941,
                    "measurement_mrid": "_317af547-685f-4bc1-a24f-3ae6a319970b"
                },
                {
                    "angle": -156.906146631186,
                    "magnitude": 130.246575039941,
                    "measurement_mrid": "_cbd2e9b6-f9b5-4faf-b397-ce4646ca9054"
                },
                {
                    "angle": -156.914941222596,
                    "magnitude": 131.336099791241,
                    "measurement_mrid": "_90243f67-9a63-41d3-b699-8604f4bda472"
                },
                {
                    "angle": -156.914941222596,
                    "magnitude": 131.336099791241,
                    "measurement_mrid": "_9ef0b2c5-2c78-4a83-a19a-4bd9ae0012de"
                },
                {
                    "angle": -156.926618717471,
                    "magnitude": 130.142292561645,
                    "measurement_mrid": "_c43bbc08-8c30-4e34-a7b9-8ac564d37d99"
                },
                {
                    "angle": -156.926618717471,
                    "magnitude": 130.142292561645,
                    "measurement_mrid": "_c5f0a228-ba2b-4110-a8e3-f1250144f3ea"
                },
                {
                    "angle": 85.9181431689283,
                    "magnitude": 122.011416433355,
                    "measurement_mrid": "_45b1b4a0-b1a7-486e-b922-135b198361b8"
                },
                {
                    "angle": 85.9181431689283,
                    "magnitude": 122.011416433355,
                    "measurement_mrid": "_ffc78137-1319-41b1-b567-1051245a8e82"
                },
                {
                    "angle": -155.281323997906,
                    "magnitude": 7627.83043616574,
                    "measurement_mrid": "_87cf73e9-cdd7-4a0b-8ba1-fd15926ce1fb"
                },
                {
                    "angle": -155.297559234184,
                    "magnitude": 7619.37614890372,
                    "measurement_mrid": "_2eb13d1e-2a63-4ef7-8e18-c880bae5e134"
                },
                {
                    "angle": -32.2643569792895,
                    "magnitude": 7315.99463979675,
                    "measurement_mrid": "_fee0c8b0-494c-49d1-b7c4-7419c742b393"
                },
                {
                    "angle": -36.168106607692,
                    "magnitude": 137.037674969507,
                    "measurement_mrid": "_04c53d37-9030-4a5b-b146-9aec51653dd3"
                },
                {
                    "angle": -36.1902465590949,
                    "magnitude": 137.511628157331,
                    "measurement_mrid": "_f97f2367-0744-44a8-a1b0-89dfbd20ddf2"
                },
                {
                    "angle": -151.726931136225,
                    "magnitude": 7319.84080151003,
                    "measurement_mrid": "_1cdd8d9d-4e4a-431b-ba74-d1e313b4b5e2"
                },
                {
                    "angle": -36.0335821650982,
                    "magnitude": 137.037322894356,
                    "measurement_mrid": "_30863d79-be95-48c3-b368-6f62cb76192a"
                },
                {
                    "angle": -36.055722237007,
                    "magnitude": 137.511276868028,
                    "measurement_mrid": "_7f2f8aa6-2c35-452d-900f-272dc18a7587"
                },
                {
                    "angle": -156.116238373287,
                    "magnitude": 7980.87752704903,
                    "measurement_mrid": "_27b3a489-389d-46ce-bb28-0105b6a2ce59"
                },
                {
                    "angle": 86.4716855227943,
                    "magnitude": 7316.04575468105,
                    "measurement_mrid": "_b95ef492-89c3-480b-b4f2-057f36d1bfba"
                },
                {
                    "angle": -35.7119059930396,
                    "magnitude": 8260.91464015638,
                    "measurement_mrid": "_f402da68-b6af-46d7-8631-7c808384c7ac"
                },
                {
                    "angle": -156.149028433993,
                    "magnitude": 127.707872598589,
                    "measurement_mrid": "_187730e3-ae94-4075-9417-8b7a9248e86e"
                },
                {
                    "angle": -156.188126086114,
                    "magnitude": 128.487447148252,
                    "measurement_mrid": "_459916dc-a810-4b2f-ab93-dcb4c8b79f66"
                },
                {
                    "angle": -34.0747462720107,
                    "magnitude": 120.675457695637,
                    "measurement_mrid": "_58ec7141-447c-4467-8744-ce227c317f58"
                },
                {
                    "angle": -34.0747462720107,
                    "magnitude": 120.675457695637,
                    "measurement_mrid": "_d9dc639d-4b4c-4af2-8d80-4b7209a5bdf2"
                },
                {
                    "angle": -156.498719353286,
                    "magnitude": 7924.08630069303,
                    "measurement_mrid": "_d51a1cac-95ff-469b-933d-d0b13589e0a7"
                },
                {
                    "angle": 87.2484515333448,
                    "magnitude": 120.701929525435,
                    "measurement_mrid": "_698e7469-59f8-4b3e-b039-1547b2654e4f"
                },
                {
                    "angle": 87.2484515333448,
                    "magnitude": 120.701929525435,
                    "measurement_mrid": "_f7362ada-881c-4781-b942-820f9968280f"
                },
                {
                    "angle": 87.7317035798281,
                    "magnitude": 7304.92177852957,
                    "measurement_mrid": "_a0c3f9e9-5de3-4c54-95c4-5b6842251652"
                },
                {
                    "angle": 88.6504903808143,
                    "magnitude": 7290.65870970995,
                    "measurement_mrid": "_00fe5fe9-cf6b-41cf-b796-6e7e278227c6"
                },
                {
                    "angle": -151.639064375704,
                    "magnitude": 7322.7191704605,
                    "measurement_mrid": "_92752b7e-457f-4984-971e-6fa67c77970c"
                },
                {
                    "angle": -31.6182487236927,
                    "magnitude": 7321.18991932422,
                    "measurement_mrid": "_ba161540-5b4d-478b-a001-0d66be9e026b"
                },
                {
                    "angle": -156.198910176483,
                    "magnitude": 127.617832455285,
                    "measurement_mrid": "_19775fe8-b4cc-4f57-87f4-c23ca1c3e169"
                },
                {
                    "angle": -156.214628164073,
                    "magnitude": 127.929868869247,
                    "measurement_mrid": "_6212b07a-cf9c-4546-bedf-aeae9bf7c775"
                },
                {
                    "angle": 86.6341974466078,
                    "magnitude": 121.281546895239,
                    "measurement_mrid": "_520dc5f9-87e5-4f47-b1a7-13b944a10a9d"
                },
                {
                    "angle": 86.6630615250001,
                    "magnitude": 120.738145800298,
                    "measurement_mrid": "_9a2faded-c158-418a-8bc8-d9348539ec18"
                },
                {
                    "angle": -155.142491751978,
                    "magnitude": 7693.09979072197,
                    "measurement_mrid": "_1659d1c2-ceed-41e6-8b91-f07ba29933a1"
                },
                {
                    "angle": -35.6994514053181,
                    "magnitude": 8322.52464213405,
                    "measurement_mrid": "_d934fab7-5a38-42a0-99c7-e18c2a2ee720"
                },
                {
                    "angle": 88.913121782668,
                    "magnitude": 7237.01508089541,
                    "measurement_mrid": "_6d500a8f-97b0-4208-b2c4-4a5ddb7a536a"
                },
                {
                    "angle": -35.43990929199,
                    "magnitude": 132.000687012994,
                    "measurement_mrid": "_49e230f7-51a0-4993-9890-32b2d12168a4"
                },
                {
                    "angle": -35.43990929199,
                    "magnitude": 132.000687012994,
                    "measurement_mrid": "_c8d839da-a170-4b24-a081-b2cb7dd52758"
                },
                {
                    "angle": 85.5830855021634,
                    "magnitude": 120.892322912433,
                    "measurement_mrid": "_08b1d5f7-a232-40b0-b6a9-11731e8dab0d"
                },
                {
                    "angle": 85.5830855021634,
                    "magnitude": 120.892322912433,
                    "measurement_mrid": "_aa10090d-3819-4b87-8b51-ba801ebdc76a"
                },
                {
                    "angle": 86.4325742067966,
                    "magnitude": 7389.40418627781,
                    "measurement_mrid": "_4453f393-3beb-4bc9-9ede-238b5990c3cd"
                },
                {
                    "angle": -35.5952562368617,
                    "magnitude": 8350.0678966926,
                    "measurement_mrid": "_7ebbe54b-733f-46c1-989c-e4ed19373849"
                },
                {
                    "angle": -156.189963375415,
                    "magnitude": 8000.97892170272,
                    "measurement_mrid": "_c5533b95-01af-4b74-8934-1905e13fbf98"
                },
                {
                    "angle": -35.7995546834154,
                    "magnitude": 8284.12117604202,
                    "measurement_mrid": "_81579f40-20e9-42a3-98d7-667b4bf2b4bd"
                },
                {
                    "angle": 86.3879374577706,
                    "magnitude": 7365.73393254547,
                    "measurement_mrid": "_8850781e-3667-4055-8857-b71f83d93484"
                },
                {
                    "angle": -156.440887410641,
                    "magnitude": 7959.91772269223,
                    "measurement_mrid": "_8fb31ab5-d80b-43d2-a302-84f9ab479e0a"
                },
                {
                    "angle": -33.07114849585,
                    "magnitude": 7339.18356618839,
                    "measurement_mrid": "_1dbbeab9-76a5-49ee-98b9-627af069e330"
                },
                {
                    "angle": -153.152480753452,
                    "magnitude": 7319.60752265416,
                    "measurement_mrid": "_e4b397d4-3c6d-4346-8ff5-b74e16d415f0"
                },
                {
                    "angle": 87.2994822275653,
                    "magnitude": 7302.34719431392,
                    "measurement_mrid": "_f194c01e-cec9-4b32-aaf7-0d28a08a5bcc"
                },
                {
                    "angle": -36.2032076139857,
                    "magnitude": 136.944680508592,
                    "measurement_mrid": "_27eb3a54-df29-490e-a5d7-5fe9bb58ad97"
                },
                {
                    "angle": -36.189874836042,
                    "magnitude": 136.660416590693,
                    "measurement_mrid": "_6d379e79-4875-4b78-9c58-30855a413e02"
                },
                {
                    "angle": -156.89920820505,
                    "magnitude": 131.39606627643,
                    "measurement_mrid": "_4168a6d1-9ab4-41dc-8e83-5bd86896cb38"
                },
                {
                    "angle": -156.89920820505,
                    "magnitude": 131.39606627643,
                    "measurement_mrid": "_9cdeba7e-253c-4e06-9d9a-52999707d76c"
                },
                {
                    "angle": 86.8882237657786,
                    "magnitude": 120.533206090501,
                    "measurement_mrid": "_33895d72-5395-4569-8dda-1b425bd0fa48"
                },
                {
                    "angle": 86.8593105881668,
                    "magnitude": 121.07660740624,
                    "measurement_mrid": "_e87f5daf-1762-4727-8c06-2aeb4bb70bee"
                },
                {
                    "angle": -154.56211820807,
                    "magnitude": 120.691836534104,
                    "measurement_mrid": "_7350186c-5672-435a-95b4-5a5a4f51f113"
                },
                {
                    "angle": -154.534365241387,
                    "magnitude": 120.171946317313,
                    "measurement_mrid": "_d48f5f4b-04af-459f-97fe-3531da5cfbad"
                },
                {
                    "angle": -34.2414183102713,
                    "magnitude": 119.879665595013,
                    "measurement_mrid": "_80de0e68-b1c2-4398-be16-c5b6667a0fdc"
                },
                {
                    "angle": -34.2159911884794,
                    "magnitude": 119.405718028595,
                    "measurement_mrid": "_dc233a58-8482-43db-8856-40cc172a3785"
                },
                {
                    "angle": -156.263560941712,
                    "magnitude": 7961.51879321164,
                    "measurement_mrid": "_5aa1bab0-871e-4ffc-a279-ce2b8cb38f4b"
                },
                {
                    "angle": -35.5722242000748,
                    "magnitude": 8331.56040465429,
                    "measurement_mrid": "_83bc807d-3edc-4edb-b851-7dfef66f07f8"
                },
                {
                    "angle": 86.4274618838507,
                    "magnitude": 7388.16171692697,
                    "measurement_mrid": "_8cf86716-3414-4ad7-bee3-2e16a0d32b1a"
                },
                {
                    "angle": -156.507535618032,
                    "magnitude": 7919.89990224521,
                    "measurement_mrid": "_2ab066e2-1504-47c0-af09-1dd485e11590"
                },
                {
                    "angle": 86.6510128887753,
                    "magnitude": 119.720359207382,
                    "measurement_mrid": "_15b6d356-5380-4eac-9c7c-471cc358daf8"
                },
                {
                    "angle": 86.6802531875086,
                    "magnitude": 119.176956698817,
                    "measurement_mrid": "_23fa0c57-7f7c-4252-a9cc-afc054c4f373"
                },
                {
                    "angle": -36.1808304929039,
                    "magnitude": 137.09433630133,
                    "measurement_mrid": "_a47ba881-ee39-4ee9-96dc-7bc6cc64ca99"
                },
                {
                    "angle": -36.1808304929039,
                    "magnitude": 137.09433630133,
                    "measurement_mrid": "_ffa25d2c-a1c8-4012-bf80-ff5d5eb35184"
                },
                {
                    "angle": -155.61908859964,
                    "magnitude": 127.234380304918,
                    "measurement_mrid": "_ddde81aa-dc3d-49a3-814f-646b58b55b3d"
                },
                {
                    "angle": -155.61908859964,
                    "magnitude": 127.234380304918,
                    "measurement_mrid": "_ef3c46d9-2ba2-4b32-85ed-1780eeb3843c"
                },
                {
                    "angle": -33.8611481472529,
                    "magnitude": 7282.76353986701,
                    "measurement_mrid": "_2779da9a-b513-45c8-851f-77ab9278f8f8"
                },
                {
                    "angle": 86.5816507044342,
                    "magnitude": 7250.5921950296,
                    "measurement_mrid": "_be784093-b880-459e-b7db-87970014bf3d"
                },
                {
                    "angle": -153.97611964073,
                    "magnitude": 7254.14735986892,
                    "measurement_mrid": "_c46ce78d-f550-4c0c-a9f6-022dd218d8cd"
                },
                {
                    "angle": -156.488494885278,
                    "magnitude": 7928.84785617113,
                    "measurement_mrid": "_5afcd8e6-155d-4125-a26e-a41648204903"
                },
                {
                    "angle": 86.2564201975672,
                    "magnitude": 7408.9409731845,
                    "measurement_mrid": "_b4e65c00-880b-46fd-a0d8-8b4d201d8876"
                },
                {
                    "angle": -156.888984767486,
                    "magnitude": 130.124922687996,
                    "measurement_mrid": "_aaba5ed1-bb14-477c-91e9-80977e3e4d7d"
                },
                {
                    "angle": -156.888984767486,
                    "magnitude": 130.124922687996,
                    "measurement_mrid": "_f57b0e5e-cf6f-4ad5-b104-66bbdb28df40"
                },
                {
                    "angle": 87.0183477184906,
                    "magnitude": 7377.67599655906,
                    "measurement_mrid": "_edf62e8b-fd9b-440f-a45e-19ee5fbf9a7e"
                },
                {
                    "angle": -34.2287471462353,
                    "magnitude": 119.648600489612,
                    "measurement_mrid": "_986bc836-9064-4679-9f81-068c9c90943b"
                },
                {
                    "angle": -34.2287471462353,
                    "magnitude": 119.648600489612,
                    "measurement_mrid": "_d9930d91-82e0-435c-97c9-1de8aa324030"
                },
                {
                    "angle": -156.167025161626,
                    "magnitude": 128.111303861412,
                    "measurement_mrid": "_b01b91f9-657f-41da-99d3-149cae7cbb64"
                },
                {
                    "angle": -156.167025161626,
                    "magnitude": 128.111303861412,
                    "measurement_mrid": "_e2f582a0-02d4-42db-bd2b-b4576a8295b2"
                },
                {
                    "angle": -155.105778463413,
                    "magnitude": 120.568825924013,
                    "measurement_mrid": "_10bf365b-c000-494e-a48c-8939f39bfd61"
                },
                {
                    "angle": -155.105778463413,
                    "magnitude": 120.568825924013,
                    "measurement_mrid": "_4b18b78b-1484-4709-8f58-c8f8a1089a4f"
                },
                {
                    "angle": -35.9245273772584,
                    "magnitude": 137.739574773889,
                    "measurement_mrid": "_78713537-d843-4a7c-b5a6-423b978c560d"
                },
                {
                    "angle": -35.9245273772584,
                    "magnitude": 137.739574773889,
                    "measurement_mrid": "_fe6827e7-cf88-47aa-a554-9f38d6ec9d3a"
                },
                {
                    "angle": -35.8620864589601,
                    "magnitude": 8239.54783118191,
                    "measurement_mrid": "_693df8b1-55f3-4703-8c4b-1b47fb0ae51b"
                },
                {
                    "angle": 86.6806442401228,
                    "magnitude": 119.33432861985,
                    "measurement_mrid": "_7d29f7c2-063a-4a16-9170-9cd022759b06"
                },
                {
                    "angle": 86.6630968958173,
                    "magnitude": 119.660258940863,
                    "measurement_mrid": "_af340144-eac4-49e6-82f0-73086b4559d3"
                },
                {
                    "angle": 85.9479588822373,
                    "magnitude": 121.122794100951,
                    "measurement_mrid": "_59d745b0-0d44-491e-826b-901034b7ceab"
                },
                {
                    "angle": 85.9768581947425,
                    "magnitude": 120.579392437836,
                    "measurement_mrid": "_7739b221-0f76-4920-9c9f-bb12891a379f"
                },
                {
                    "angle": -156.855863306011,
                    "magnitude": 130.635489462629,
                    "measurement_mrid": "_88b73600-b863-4e6d-b80c-4c60d92b7c54"
                },
                {
                    "angle": -156.84047208152,
                    "magnitude": 130.323451587829,
                    "measurement_mrid": "_8c78704c-be7b-4cd2-bddc-d61d61af6e68"
                },
                {
                    "angle": -156.957240936073,
                    "magnitude": 130.963871436792,
                    "measurement_mrid": "_a0e7c313-6dad-4836-983f-21159fbe548e"
                },
                {
                    "angle": -156.957240936073,
                    "magnitude": 130.963871436792,
                    "measurement_mrid": "_fc62b0ca-6d82-4a24-9431-37abf34d349e"
                },
                {
                    "angle": -156.452104497236,
                    "magnitude": 7952.85418755872,
                    "measurement_mrid": "_6353877a-3619-41cd-aee0-c5d4d5bb9753"
                },
                {
                    "angle": -156.774722814701,
                    "magnitude": 131.456052284926,
                    "measurement_mrid": "_9fbfcc3f-e9c3-4dfc-91b0-2a1d43c97d85"
                },
                {
                    "angle": -156.749237449092,
                    "magnitude": 130.936165447928,
                    "measurement_mrid": "_cbdaee40-7283-416c-9262-02381c944495"
                },
                {
                    "angle": -154.714635469173,
                    "magnitude": 7781.08630780398,
                    "measurement_mrid": "_9578b160-1d87-4bd3-ad52-6bfd1dce1e95"
                },
                {
                    "angle": -156.421530200311,
                    "magnitude": 7877.88052703035,
                    "measurement_mrid": "_51164081-4abe-4457-9ddf-1a04012585ff"
                },
                {
                    "angle": -35.591197271914,
                    "magnitude": 8307.86032634498,
                    "measurement_mrid": "_d2e7c3bd-2c8c-45ea-b4d3-a35a25688cf4"
                },
                {
                    "angle": -50.0190648881554,
                    "magnitude": 1.95267578708807,
                    "measurement_mrid": "_3ded0f01-7fb8-4ea3-b165-9f18741a0b28"
                },
                {
                    "angle": 71.820701477217,
                    "magnitude": 4.47722858609799,
                    "measurement_mrid": "_b28c6f8b-1d67-4336-b59e-9c4f5f9b5e53"
                },
                {
                    "angle": -65.4858398673867,
                    "magnitude": 0.0220188022380873,
                    "measurement_mrid": "_c63a5fbc-9fbc-410e-91e8-d1b3321d4267"
                },
                {
                    "angle": -34.7843250867118,
                    "magnitude": 128.721646206708,
                    "measurement_mrid": "_744b058a-591c-40ee-a2a4-d8b16b65c537"
                },
                {
                    "angle": -34.7843250867118,
                    "magnitude": 128.721646206708,
                    "measurement_mrid": "_9e25d335-505b-4e6d-930d-03d9db1b1bfb"
                },
                {
                    "angle": -154.142045279962,
                    "magnitude": 7769.08245491704,
                    "measurement_mrid": "_f387e535-cbfb-41c2-8949-9ad9521ccb1d"
                },
                {
                    "angle": -156.95948285313,
                    "magnitude": 131.158882046848,
                    "measurement_mrid": "_6ac24967-9a1a-472c-8b37-f9c3bd4d298b"
                },
                {
                    "angle": -156.944151002524,
                    "magnitude": 130.846845303274,
                    "measurement_mrid": "_c74a7679-d3a3-4466-8e7e-1f4ab0b12edc"
                },
                {
                    "angle": -35.5903699566743,
                    "magnitude": 8308.33056946084,
                    "measurement_mrid": "_c31820bf-2a7a-4067-9664-a3ced77f8393"
                },
                {
                    "angle": 87.1796972304307,
                    "magnitude": 7231.30182195803,
                    "measurement_mrid": "_2f99908e-aee4-4cb9-a240-ccbe8b9cca8f"
                },
                {
                    "angle": -35.8089987280195,
                    "magnitude": 8261.61237525443,
                    "measurement_mrid": "_a25533e5-85ec-4a23-8bc0-0b6f4b65833a"
                },
                {
                    "angle": 86.2537552739932,
                    "magnitude": 7407.75370277318,
                    "measurement_mrid": "_01919f2d-d5c4-40b6-ae6e-5908b281527e"
                },
                {
                    "angle": -156.192678507558,
                    "magnitude": 128.636889117084,
                    "measurement_mrid": "_1b1afdd6-f726-4174-8d53-1f590f87b3c0"
                },
                {
                    "angle": -156.140617884494,
                    "magnitude": 127.597621178067,
                    "measurement_mrid": "_56baa240-268f-45ad-8d55-4f3ad7a78635"
                },
                {
                    "angle": -156.937487172758,
                    "magnitude": 131.116166717771,
                    "measurement_mrid": "_2de260b5-c5b2-4682-b56e-c6909c5a4dfc"
                },
                {
                    "angle": -156.937487172758,
                    "magnitude": 131.116166717771,
                    "measurement_mrid": "_735dcb76-e6de-4ee0-94c6-ea33b2f7d4b5"
                },
                {
                    "angle": -36.245561102768,
                    "magnitude": 136.47849035827,
                    "measurement_mrid": "_3a8cfa9f-1b5c-4d13-be99-061bf3672fdd"
                },
                {
                    "angle": -36.245561102768,
                    "magnitude": 136.47849035827,
                    "measurement_mrid": "_aacbcd09-2590-40a1-a2e8-6b787f098125"
                },
                {
                    "angle": -35.6389808804445,
                    "magnitude": 8302.35766557932,
                    "measurement_mrid": "_10613e01-80aa-4c66-9d85-d221fa7a70a4"
                },
                {
                    "angle": 86.4552510944297,
                    "magnitude": 7347.84117990129,
                    "measurement_mrid": "_93401ccc-7fcc-47f7-b0ed-8dfaf769f43f"
                },
                {
                    "angle": -156.139653946933,
                    "magnitude": 7984.41270005667,
                    "measurement_mrid": "_be076d69-f6c3-4350-8caf-c27cf7e4e111"
                },
                {
                    "angle": -35.6378996440866,
                    "magnitude": 8303.07603439564,
                    "measurement_mrid": "_0e531d1f-3dad-4413-8049-312ef5fea7b5"
                },
                {
                    "angle": -156.139813508857,
                    "magnitude": 7984.48109273755,
                    "measurement_mrid": "_9483b45f-99a3-4f16-96aa-356c3cf8e1c9"
                },
                {
                    "angle": 86.4547287718668,
                    "magnitude": 7348.25561386707,
                    "measurement_mrid": "_a8319cd3-88ac-408d-a30e-bab9a7a98668"
                },
                {
                    "angle": 86.3109138129119,
                    "magnitude": 7347.04847290933,
                    "measurement_mrid": "_dfadca1f-651c-4472-9c92-0ce5a49433bd"
                },
                {
                    "angle": -35.6359959305043,
                    "magnitude": 8304.32664777439,
                    "measurement_mrid": "_3c378c5b-6114-48fe-8ad5-25c2ddc61b8f"
                },
                {
                    "angle": -156.140105910613,
                    "magnitude": 7984.5818818033,
                    "measurement_mrid": "_6da939b2-41d9-4b7a-b2e9-0d15b9016dff"
                },
                {
                    "angle": 86.4537962142169,
                    "magnitude": 7348.97024301008,
                    "measurement_mrid": "_ac934015-2149-4031-b60a-46c0706b24cf"
                },
                {
                    "angle": 86.4547175862714,
                    "magnitude": 7348.24995675039,
                    "measurement_mrid": "_061f6ba2-7eb5-4270-877f-0358d316ac87"
                },
                {
                    "angle": 85.7770800921361,
                    "magnitude": 122.205525768471,
                    "measurement_mrid": "_0f6e04ef-483c-4801-a12f-5426828d8f2f"
                },
                {
                    "angle": 85.7485633957278,
                    "magnitude": 122.748927956418,
                    "measurement_mrid": "_38669957-8036-4250-aa4b-8fc361b9894f"
                },
                {
                    "angle": -35.6357482550112,
                    "magnitude": 8304.48937061706,
                    "measurement_mrid": "_18b46d3c-5abe-464f-8ae4-1d9614a80bef"
                },
                {
                    "angle": -156.140143933483,
                    "magnitude": 7984.5949940518,
                    "measurement_mrid": "_91b7d027-ba7d-4559-9c9b-eb5f59635a54"
                },
                {
                    "angle": 86.4536749070213,
                    "magnitude": 7349.06322547422,
                    "measurement_mrid": "_bad45dff-1218-47f0-a736-d9b10a1c954d"
                },
                {
                    "angle": -156.502006464614,
                    "magnitude": 7922.31699479356,
                    "measurement_mrid": "_844f710a-17a6-410a-ab7e-974918419f60"
                },
                {
                    "angle": -35.2754444653406,
                    "magnitude": 127.629868567561,
                    "measurement_mrid": "_34eff655-1356-485a-9b16-118e63afc5f5"
                },
                {
                    "angle": -35.2611295328412,
                    "magnitude": 127.345606964547,
                    "measurement_mrid": "_3d05e0d1-777c-4833-9f93-b93aaaf82c2c"
                },
                {
                    "angle": -155.309336413739,
                    "magnitude": 7613.1685741799,
                    "measurement_mrid": "_e1005b19-3cf1-41e0-b8f6-064b1caa2214"
                },
                {
                    "angle": 88.8594540284672,
                    "magnitude": 7212.99864852664,
                    "measurement_mrid": "_e418ae2a-6faa-4906-8bb9-fb505f82f967"
                },
                {
                    "angle": 86.6026311531284,
                    "magnitude": 7252.00334970962,
                    "measurement_mrid": "_9a2d5e73-090c-4d0c-9ea7-0dd207a84b84"
                },
                {
                    "angle": -33.8385060345923,
                    "magnitude": 7284.17010901714,
                    "measurement_mrid": "_c1fb0fde-c8ec-46b0-b20e-cabfee5d3ccf"
                },
                {
                    "angle": -153.952442785914,
                    "magnitude": 7255.95473557036,
                    "measurement_mrid": "_d7845650-947a-44dc-85ef-c934492e7570"
                },
                {
                    "angle": -153.702792060399,
                    "magnitude": 7304.89409632402,
                    "measurement_mrid": "_3f7f0bb6-cadf-48b8-a0c6-3ce78866e76c"
                },
                {
                    "angle": -33.4898989931216,
                    "magnitude": 7263.90705689509,
                    "measurement_mrid": "_baae25e1-e855-4cba-a180-dcce3407aa9b"
                },
                {
                    "angle": 87.489732157236,
                    "magnitude": 7313.41830349652,
                    "measurement_mrid": "_d127b532-f7f2-438f-9eb2-9ebd66e000e4"
                },
                {
                    "angle": -153.049799079135,
                    "magnitude": 7316.58531847503,
                    "measurement_mrid": "_4ec45905-1619-4e14-a137-1ac284acab07"
                },
                {
                    "angle": 87.1704729208812,
                    "magnitude": 120.660958191606,
                    "measurement_mrid": "_18fec281-96f2-4ef8-a03a-4ec915be0faa"
                },
                {
                    "angle": 87.1704729208812,
                    "magnitude": 120.660958191606,
                    "measurement_mrid": "_252f2998-a10c-4ab2-b397-3de0bc73ff5b"
                },
                {
                    "angle": 85.7769731881603,
                    "magnitude": 121.323786604297,
                    "measurement_mrid": "_2c1fd570-3136-4156-9e01-8ed565113a49"
                },
                {
                    "angle": 85.7769731881603,
                    "magnitude": 121.323786604297,
                    "measurement_mrid": "_d6021128-d22e-4baa-8388-7074f634bb8b"
                },
                {
                    "angle": -154.589489733972,
                    "magnitude": 128.173813205744,
                    "measurement_mrid": "_1a4d856c-ad69-46cb-ade3-d6236d5fb366"
                },
                {
                    "angle": -154.615501175457,
                    "magnitude": 128.693706163121,
                    "measurement_mrid": "_ca93a8cd-15b1-4ff7-9754-bc745fab2f76"
                },
                {
                    "angle": -36.1741894408278,
                    "magnitude": 136.996511311382,
                    "measurement_mrid": "_02fc0b27-037f-470f-823e-25d081c9ceff"
                },
                {
                    "angle": -36.1963356167742,
                    "magnitude": 137.470465340991,
                    "measurement_mrid": "_bb84d2e9-ec48-4983-8b62-b9350eba3569"
                },
                {
                    "angle": 85.8810598027244,
                    "magnitude": 121.625101251363,
                    "measurement_mrid": "_c6eb6de3-94b3-42fe-9b06-8d1a5275a9b6"
                },
                {
                    "angle": 85.8810598027244,
                    "magnitude": 121.625101251363,
                    "measurement_mrid": "_d103de23-b49a-4b84-ad81-f403626efb90"
                },
                {
                    "angle": -156.573528395046,
                    "magnitude": 131.964840737583,
                    "measurement_mrid": "_58490b01-958d-4822-bafb-a7fc3d659988"
                },
                {
                    "angle": -156.573528395046,
                    "magnitude": 131.964840737583,
                    "measurement_mrid": "_a768b249-ed5e-4343-85db-4baacb5f9a33"
                },
                {
                    "angle": -156.85681525252,
                    "magnitude": 130.415014808958,
                    "measurement_mrid": "_9f9ee68b-ca23-463c-9cd5-bbde1fa62317"
                },
                {
                    "angle": -156.872196458502,
                    "magnitude": 130.727051079502,
                    "measurement_mrid": "_d5bb6f03-69f0-4be0-9ca1-5c16aa6260d3"
                },
                {
                    "angle": -156.468307367085,
                    "magnitude": 7872.41303256402,
                    "measurement_mrid": "_25cd3f0d-2e9d-45d9-b57f-ddafaef2b783"
                },
                {
                    "angle": 85.6370358224535,
                    "magnitude": 7418.91681428246,
                    "measurement_mrid": "_976378b7-9329-41b2-b07e-b71dedc9ab7a"
                },
                {
                    "angle": -34.8602102633338,
                    "magnitude": 7734.27048764159,
                    "measurement_mrid": "_b60ed403-be25-4efc-9fd7-93db696b3392"
                },
                {
                    "angle": -155.162738268884,
                    "magnitude": 7691.71139400474,
                    "measurement_mrid": "_e0cbb17f-47f0-4e33-ad43-f8422a83024a"
                },
                {
                    "angle": -36.2115255552729,
                    "magnitude": 137.006703717353,
                    "measurement_mrid": "_84064465-0903-46e3-9fc0-857919fac1fe"
                },
                {
                    "angle": -36.1893064233069,
                    "magnitude": 136.532749281272,
                    "measurement_mrid": "_a8f3cd57-5a0f-429e-837c-ee4b34758219"
                },
                {
                    "angle": -36.1486931845477,
                    "magnitude": 137.423258094981,
                    "measurement_mrid": "_5f8e63ea-cd32-42aa-a2f7-9bd5a5e10a53"
                },
                {
                    "angle": -36.1486931845477,
                    "magnitude": 137.423258094981,
                    "measurement_mrid": "_a0e7ee83-197b-41c4-b276-afb9efe794ce"
                },
                {
                    "angle": 85.8292348363253,
                    "magnitude": 121.122647076293,
                    "measurement_mrid": "_e4a1b181-4646-4420-92c6-2a7f3ebcaf97"
                },
                {
                    "angle": 85.8292348363253,
                    "magnitude": 121.122647076293,
                    "measurement_mrid": "_f6002a55-0b12-43a5-bea6-591a24860d48"
                },
                {
                    "angle": -34.8529211854704,
                    "magnitude": 7725.30076745992,
                    "measurement_mrid": "_38e29a8a-5a32-4e8d-8c29-29ebd3e4fa55"
                },
                {
                    "angle": 85.6396535383046,
                    "magnitude": 7416.74870691403,
                    "measurement_mrid": "_54d6acd3-fb66-4d04-a413-2a44246c3d4e"
                },
                {
                    "angle": -155.183743316949,
                    "magnitude": 7677.961814282,
                    "measurement_mrid": "_6ab2bf7a-e95e-4894-a5b5-5948546867d2"
                },
                {
                    "angle": -156.178765063595,
                    "magnitude": 127.789701112744,
                    "measurement_mrid": "_0e8b3379-a383-44e5-8360-9c0e852463ba"
                },
                {
                    "angle": -156.194462108161,
                    "magnitude": 128.101737380797,
                    "measurement_mrid": "_a3c4adbc-1d3f-4a04-bd3a-4350226e65d7"
                },
                {
                    "angle": -155.176163880534,
                    "magnitude": 7682.1575456109,
                    "measurement_mrid": "_14add867-ec3e-4258-9104-652d8f10b55f"
                },
                {
                    "angle": 85.6376407898667,
                    "magnitude": 7416.78719885176,
                    "measurement_mrid": "_8696643f-04f7-4f5e-bb6d-10ca624ca545"
                },
                {
                    "angle": -34.8552552835729,
                    "magnitude": 7728.22326228753,
                    "measurement_mrid": "_e3212f3e-2465-4178-b8c3-5a2c2b0def3d"
                },
                {
                    "angle": -155.640006549231,
                    "magnitude": 127.000245136934,
                    "measurement_mrid": "_0d0de564-838c-4960-a896-da69b927c421"
                },
                {
                    "angle": -155.640006549231,
                    "magnitude": 127.000245136934,
                    "measurement_mrid": "_dfe3f9b5-0ddb-48b0-8f87-cd3a88a5cb78"
                },
                {
                    "angle": 86.4715327233769,
                    "magnitude": 7315.97497927184,
                    "measurement_mrid": "_12fa0197-7424-4737-bfb8-841ee3ffb00c"
                },
                {
                    "angle": -156.116142196809,
                    "magnitude": 7980.86907649931,
                    "measurement_mrid": "_877899b6-1418-49d4-87b7-41ce81ff44b8"
                },
                {
                    "angle": -35.7119243175721,
                    "magnitude": 8260.93392330099,
                    "measurement_mrid": "_c4376df3-4a3a-40fa-a4ef-cc5e70dde9a8"
                },
                {
                    "angle": -156.184011919445,
                    "magnitude": 127.597179419686,
                    "measurement_mrid": "_413d109c-c06f-42d0-adf3-7f079bcb5ca7"
                },
                {
                    "angle": -156.210161368598,
                    "magnitude": 128.117067688619,
                    "measurement_mrid": "_fd05a8f3-3f1f-4294-974d-17b7700c09ae"
                },
                {
                    "angle": -36.2668025814129,
                    "magnitude": 136.010694889115,
                    "measurement_mrid": "_3ed9e6cc-3595-46f1-aabf-ac84b3c16f4d"
                },
                {
                    "angle": -36.289104430928,
                    "magnitude": 136.484648896688,
                    "measurement_mrid": "_779e3950-371d-4b16-ad33-98ddccb30362"
                },
                {
                    "angle": -154.127363196807,
                    "magnitude": 7776.4718854115,
                    "measurement_mrid": "_f84a8f51-4025-427d-8a5b-44153f079b00"
                },
                {
                    "angle": -156.908722072292,
                    "magnitude": 131.663144609457,
                    "measurement_mrid": "_08bd87bb-a574-44c6-8529-3bc1c8f37a33"
                },
                {
                    "angle": -156.8934485175,
                    "magnitude": 131.351108648901,
                    "measurement_mrid": "_cf700977-eeaf-4d13-81db-1faac8f41cf3"
                },
                {
                    "angle": -154.607886131361,
                    "magnitude": 128.393537696982,
                    "measurement_mrid": "_42a461a3-57b1-4057-bc70-200b85e5403f"
                },
                {
                    "angle": -154.607886131361,
                    "magnitude": 128.393537696982,
                    "measurement_mrid": "_b74866d4-8d97-4cb6-b67e-f19c7b0427b2"
                },
                {
                    "angle": -35.7297073556414,
                    "magnitude": 8247.22604635686,
                    "measurement_mrid": "_57f43c63-b308-4ff5-bc0d-c2d5d56c051b"
                },
                {
                    "angle": -35.6976590308431,
                    "magnitude": 8323.11863146045,
                    "measurement_mrid": "_6bcc0803-2b70-43c0-91c4-75f65143c657"
                },
                {
                    "angle": -153.795988931669,
                    "magnitude": 7302.90810468835,
                    "measurement_mrid": "_75e5140d-78e2-4d62-8d0b-1640b5c747e5"
                },
                {
                    "angle": 86.6235234430829,
                    "magnitude": 121.747954161572,
                    "measurement_mrid": "_48cacd8a-54d9-47f7-947b-ac2d810c097f"
                },
                {
                    "angle": 86.6235234430829,
                    "magnitude": 121.747954161572,
                    "measurement_mrid": "_78966c64-f6c6-43a3-8587-2d15103e3d57"
                },
                {
                    "angle": -156.127014372954,
                    "magnitude": 7980.03138162496,
                    "measurement_mrid": "_1ba67db6-8a06-411b-b416-fd9602dcc46c"
                },
                {
                    "angle": -35.6985347647928,
                    "magnitude": 8263.62750237754,
                    "measurement_mrid": "_3ddf0dfd-0630-4ffc-9507-d2fd0adb0b1f"
                },
                {
                    "angle": 86.4785833196758,
                    "magnitude": 7322.41730729635,
                    "measurement_mrid": "_9e7a8787-0d31-4132-a314-bb0dbdb2001b"
                },
                {
                    "angle": -36.1451245285809,
                    "magnitude": 137.45727582057,
                    "measurement_mrid": "_061aa936-5751-4794-b26d-eb391c9db61e"
                },
                {
                    "angle": -36.1451245285809,
                    "magnitude": 137.45727582057,
                    "measurement_mrid": "_f0048a80-630c-4193-96ab-3cd38be9aa46"
                },
                {
                    "angle": -156.901344210962,
                    "magnitude": 131.501707632279,
                    "measurement_mrid": "_6f78fc5c-dca0-40e6-af05-6bd21833c256"
                },
                {
                    "angle": -156.901344210962,
                    "magnitude": 131.501707632279,
                    "measurement_mrid": "_b317b197-2dbe-4dbb-bc3f-f3ebab0844f4"
                },
                {
                    "angle": -36.0986076076214,
                    "magnitude": 136.75478010853,
                    "measurement_mrid": "_211b5026-27c3-48e5-b09b-749c70e6e9e1"
                },
                {
                    "angle": -36.0986076076214,
                    "magnitude": 136.75478010853,
                    "measurement_mrid": "_2fae2ea6-721b-466e-8343-3954b32bfdcf"
                },
                {
                    "angle": -35.7460293860305,
                    "magnitude": 8308.56962409706,
                    "measurement_mrid": "_eacfa94e-77f9-4623-ad4a-29e05d84cdb6"
                },
                {
                    "angle": -156.449256345914,
                    "magnitude": 7953.11934200211,
                    "measurement_mrid": "_35f159db-0a1f-49f9-9842-b22d7c55f149"
                },
                {
                    "angle": 86.3894743529215,
                    "magnitude": 7366.53722206602,
                    "measurement_mrid": "_45ba394b-9fe8-4cc4-8f60-20abbdc4a2ef"
                },
                {
                    "angle": -35.790356874201,
                    "magnitude": 8284.09073337506,
                    "measurement_mrid": "_f5e41cf2-0fca-4624-91e2-7c98db95ac81"
                },
                {
                    "angle": -154.225146411492,
                    "magnitude": 120.701222572418,
                    "measurement_mrid": "_40ca6996-7d79-411c-814b-d9f9f74b2962"
                },
                {
                    "angle": -154.225146411492,
                    "magnitude": 120.701222572418,
                    "measurement_mrid": "_e04277af-ff67-4be0-a675-e7a208370eca"
                },
                {
                    "angle": -35.7884846623039,
                    "magnitude": 8293.70585994721,
                    "measurement_mrid": "_8f7b982d-2427-47fe-ad73-d700606e764d"
                },
                {
                    "angle": -36.1998092153515,
                    "magnitude": 136.770701563592,
                    "measurement_mrid": "_4bea5012-15c5-485c-8926-10740825081c"
                },
                {
                    "angle": -36.1998092153515,
                    "magnitude": 136.770701563592,
                    "measurement_mrid": "_9fd8cedd-d108-4784-95d1-96ee155c8e0c"
                },
                {
                    "angle": 87.2105609938191,
                    "magnitude": 7246.56898558244,
                    "measurement_mrid": "_8be9024c-2401-47e7-8250-bfc7894c795c"
                },
                {
                    "angle": -156.231017752614,
                    "magnitude": 7958.43418917046,
                    "measurement_mrid": "_95167b89-825c-48e6-94c1-40ce52de43c4"
                },
                {
                    "angle": -35.6091279798419,
                    "magnitude": 8319.42025931139,
                    "measurement_mrid": "_b6044230-c9a3-4f65-bada-cf68eed710b5"
                },
                {
                    "angle": 86.3115391440289,
                    "magnitude": 7347.3643563022,
                    "measurement_mrid": "_b8370778-8ff9-49f6-8112-3816c9d8c9fd"
                },
                {
                    "angle": -156.458043275862,
                    "magnitude": 7875.60504951675,
                    "measurement_mrid": "_90063b8c-9c17-4ecf-b2f6-fde2a67d97ec"
                },
                {
                    "angle": -35.6526657948032,
                    "magnitude": 8293.2719102226,
                    "measurement_mrid": "_9c41204f-dd3d-4b66-9f9e-25ff5efd2473"
                },
                {
                    "angle": -155.097738577874,
                    "magnitude": 7712.96305584932,
                    "measurement_mrid": "_40db9d15-7cb1-41a5-a565-fa5178b6fbec"
                },
                {
                    "angle": 86.7527262195222,
                    "magnitude": 120.946188196383,
                    "measurement_mrid": "_17cb14ed-6420-4524-a665-bf5741312909"
                },
                {
                    "angle": 86.7527262195222,
                    "magnitude": 120.946188196383,
                    "measurement_mrid": "_ee4d6364-a956-4d24-980a-c5a6a6f7cc14"
                },
                {
                    "angle": -155.117349459688,
                    "magnitude": 7702.90906974778,
                    "measurement_mrid": "_299844dc-3bb6-4c3c-a13f-156db0ea9fd6"
                },
                {
                    "angle": 86.1050568981757,
                    "magnitude": 7324.55880299678,
                    "measurement_mrid": "_1806110b-7b1a-4c70-b87d-1d9e6aacdecd"
                },
                {
                    "angle": -156.399345041209,
                    "magnitude": 7889.56411097007,
                    "measurement_mrid": "_83e63450-e90e-4fec-9e1a-17d2f46032e8"
                },
                {
                    "angle": -155.283520235528,
                    "magnitude": 7772.87920595567,
                    "measurement_mrid": "_660253a0-b662-462e-9955-961183555de4"
                },
                {
                    "angle": -34.8075599316903,
                    "magnitude": 7992.5836245791,
                    "measurement_mrid": "_a77f53a8-b30d-45cc-b06a-852f1c81184a"
                },
                {
                    "angle": 86.8728477779896,
                    "magnitude": 7385.18928320609,
                    "measurement_mrid": "_d3e9a39c-0bf0-4a08-ad8f-3b0b30fc2f4c"
                },
                {
                    "angle": -35.2813311547652,
                    "magnitude": 128.123426865265,
                    "measurement_mrid": "_4fdee19a-74e3-4614-90e8-9bf6d5a5ee55"
                },
                {
                    "angle": -35.2813311547652,
                    "magnitude": 128.123426865265,
                    "measurement_mrid": "_ba0f8595-db46-4276-a03f-a379b63be885"
                },
                {
                    "angle": -36.1947913568203,
                    "magnitude": 136.685414451686,
                    "measurement_mrid": "_2729e831-56a4-4515-b199-7952a75effe3"
                },
                {
                    "angle": -36.2036927180317,
                    "magnitude": 136.875101118905,
                    "measurement_mrid": "_eae5386b-8bde-4ffd-95b0-df2bf63762d3"
                },
                {
                    "angle": 86.6749949269248,
                    "magnitude": 119.522303918213,
                    "measurement_mrid": "_7bf4c7d0-b0f3-4be6-aea4-172654d3b92c"
                },
                {
                    "angle": 86.6749949269248,
                    "magnitude": 119.522303918213,
                    "measurement_mrid": "_df3b3462-278c-49ea-8df7-27c1af712a31"
                },
                {
                    "angle": -35.1759821902256,
                    "magnitude": 132.050440195344,
                    "measurement_mrid": "_490d6b6d-f98d-4207-aaa9-a193aafa402a"
                },
                {
                    "angle": -35.1989721619616,
                    "magnitude": 132.524389299541,
                    "measurement_mrid": "_61750221-17fe-4fa8-a5ef-0a68ccb2fd57"
                },
                {
                    "angle": -156.700933248005,
                    "magnitude": 131.167665727088,
                    "measurement_mrid": "_a3cecfa0-110b-463e-a5c9-16fdb685f28f"
                },
                {
                    "angle": -156.726374406194,
                    "magnitude": 131.687552936002,
                    "measurement_mrid": "_c8db6e60-f46c-48ea-bcf1-be62a07ee363"
                },
                {
                    "angle": 87.6812692941211,
                    "magnitude": 7308.04716123253,
                    "measurement_mrid": "_2fdfa219-ec22-4af9-aa73-1a102aa214c2"
                },
                {
                    "angle": 86.9261916784798,
                    "magnitude": 120.681442949108,
                    "measurement_mrid": "_8d7f3fed-c912-4fde-bf3f-e297074ca3bb"
                },
                {
                    "angle": 86.9088397564091,
                    "magnitude": 121.00737350148,
                    "measurement_mrid": "_d9e8fa2f-cd3f-477a-b2c3-79c74d97676a"
                },
                {
                    "angle": -155.142960820838,
                    "magnitude": 7692.95534410719,
                    "measurement_mrid": "_dc269c8e-2cc5-4a79-aea0-98d45b75bece"
                },
                {
                    "angle": -34.8467362681192,
                    "magnitude": 7718.4082443782,
                    "measurement_mrid": "_648132a5-7078-4cc1-8d19-14a255e168b4"
                },
                {
                    "angle": -155.202764630296,
                    "magnitude": 7667.84294110855,
                    "measurement_mrid": "_6cbe6024-f58a-4e5d-8ec2-be0757d000dc"
                },
                {
                    "angle": 85.6449683901007,
                    "magnitude": 7417.15861611616,
                    "measurement_mrid": "_f595ad1f-5620-4360-9d9b-15bde7b57d1e"
                },
                {
                    "angle": 85.753711336666,
                    "magnitude": 122.399993014121,
                    "measurement_mrid": "_025bdfa8-f701-412a-a641-cb15a9f4a42a"
                },
                {
                    "angle": 85.753711336666,
                    "magnitude": 122.399993014121,
                    "measurement_mrid": "_f25d06c0-a003-47e8-985c-77f4c6403165"
                },
                {
                    "angle": -35.9795109610759,
                    "magnitude": 137.587386948058,
                    "measurement_mrid": "_39350ee4-ae66-416f-b199-b64facb22788"
                },
                {
                    "angle": -35.9795109610759,
                    "magnitude": 137.587386948058,
                    "measurement_mrid": "_39437e06-1700-4dc2-a517-549bbec0f4db"
                },
                {
                    "angle": 85.7331915719741,
                    "magnitude": 122.231311113401,
                    "measurement_mrid": "_4733d62a-f303-430b-a42f-d62337b282a2"
                },
                {
                    "angle": 85.7331915719741,
                    "magnitude": 122.231311113401,
                    "measurement_mrid": "_e12e428f-acb3-4c6d-a16d-6b54bf5abd06"
                },
                {
                    "angle": 88.3682434722508,
                    "magnitude": 119.293821342548,
                    "measurement_mrid": "_08da2a12-c0f0-4cd2-a435-2951eb31ee6a"
                },
                {
                    "angle": 88.3682434722508,
                    "magnitude": 119.293821342548,
                    "measurement_mrid": "_ce744d0d-1c4f-4573-9ce4-b25664fb903a"
                },
                {
                    "angle": -156.428172239969,
                    "magnitude": 7873.9784108764,
                    "measurement_mrid": "_b333af96-4573-4716-83ac-4c31f824c4d4"
                },
                {
                    "angle": -156.118895576191,
                    "magnitude": 7980.94714112254,
                    "measurement_mrid": "_177f4103-e899-4cdc-b214-26050caecfa1"
                },
                {
                    "angle": -35.7108294691295,
                    "magnitude": 8261.082235074,
                    "measurement_mrid": "_6b81790d-a4e2-42e3-9e85-da60a3bc47b3"
                },
                {
                    "angle": 86.4739085862228,
                    "magnitude": 7317.81591396501,
                    "measurement_mrid": "_6d76ead9-558e-4ca6-805f-010d52c2c41b"
                },
                {
                    "angle": -156.901624514076,
                    "magnitude": 131.402877272809,
                    "measurement_mrid": "_303bbff1-866b-4007-afd0-d60fc8c5c7c1"
                },
                {
                    "angle": -156.901624514076,
                    "magnitude": 131.402877272809,
                    "measurement_mrid": "_595664bc-c5b1-445f-b0a8-363818bc4579"
                },
                {
                    "angle": 86.261756819985,
                    "magnitude": 7411.81438065108,
                    "measurement_mrid": "_aafe7a65-d36d-4d71-bba3-790bc1a74400"
                },
                {
                    "angle": -35.7586746927119,
                    "magnitude": 8301.38040807547,
                    "measurement_mrid": "_150af6ab-4682-462e-88b2-6862469b81fe"
                },
                {
                    "angle": -35.5729996448312,
                    "magnitude": 8331.30378043599,
                    "measurement_mrid": "_ab308a07-8799-4b5a-8f72-750272ddd831"
                },
                {
                    "angle": 86.2333887696977,
                    "magnitude": 7397.10644978196,
                    "measurement_mrid": "_ec642f41-96db-469a-90b9-36d0267b73df"
                },
                {
                    "angle": 87.7870461887561,
                    "magnitude": 7306.63729614266,
                    "measurement_mrid": "_0b02e358-357b-47c2-be0f-a6c8f52ba36d"
                },
                {
                    "angle": -152.919015209852,
                    "magnitude": 7319.54927468328,
                    "measurement_mrid": "_6933dd04-e647-4854-a602-25ccdc7cd964"
                },
                {
                    "angle": -32.816820999688,
                    "magnitude": 7305.63299261015,
                    "measurement_mrid": "_70c298c5-7807-4711-b11d-a0a17eafb09d"
                },
                {
                    "angle": -33.3599527964811,
                    "magnitude": 120.715970165696,
                    "measurement_mrid": "_5501c3d3-bf8c-47cd-ba10-fbbed54ababf"
                },
                {
                    "angle": -33.3599527964811,
                    "magnitude": 120.715970165696,
                    "measurement_mrid": "_9fb6ecec-e0ca-4077-9c0e-b551a434afcf"
                },
                {
                    "angle": 86.3885469192977,
                    "magnitude": 7365.01755724502,
                    "measurement_mrid": "_cde9bb94-dd41-407a-84a5-a1b945d431ea"
                },
                {
                    "angle": 86.2681393859117,
                    "magnitude": 7415.04428711344,
                    "measurement_mrid": "_a717a9b8-5b76-48f0-849e-5871dcb3c3e1"
                },
                {
                    "angle": -155.176174998308,
                    "magnitude": 7682.10896619471,
                    "measurement_mrid": "_335ae28c-7609-4afd-950f-a11c7c72b02b"
                },
                {
                    "angle": -34.8552639653082,
                    "magnitude": 7728.18290057226,
                    "measurement_mrid": "_b9a90ec9-19dd-499a-96ab-4bc520bdfb68"
                },
                {
                    "angle": 85.6376089214219,
                    "magnitude": 7416.73953755889,
                    "measurement_mrid": "_ef7c9394-990d-4b36-813c-d88d8f9c3d13"
                },
                {
                    "angle": -36.1940727292193,
                    "magnitude": 136.625266877903,
                    "measurement_mrid": "_823b10ef-b9ba-402d-87a8-53a586b177ac"
                },
                {
                    "angle": -36.2074089872482,
                    "magnitude": 136.909529883346,
                    "measurement_mrid": "_9dedc0e6-54f8-4f2c-9aeb-51f5e4076ac9"
                },
                {
                    "angle": -156.6970075071,
                    "magnitude": 132.160912088924,
                    "measurement_mrid": "_37ce5da3-89d4-4c08-98fa-549853a1e191"
                },
                {
                    "angle": -156.6970075071,
                    "magnitude": 132.160912088924,
                    "measurement_mrid": "_47b6ece6-42ac-4623-8dea-c03ef031a661"
                },
                {
                    "angle": -34.0808728868334,
                    "magnitude": 120.763891680924,
                    "measurement_mrid": "_8e516928-0e41-4df0-9520-a27432316c14"
                },
                {
                    "angle": -34.0707696803955,
                    "magnitude": 120.5742086138,
                    "measurement_mrid": "_d6995a93-90f2-4010-b2f8-df5a18dca696"
                },
                {
                    "angle": 86.339708259705,
                    "magnitude": 7332.97801159544,
                    "measurement_mrid": "_3d53d3d2-04ae-4e75-9dcb-edb4279e54b0"
                },
                {
                    "angle": -35.6085025286666,
                    "magnitude": 8319.06833733887,
                    "measurement_mrid": "_a9c0b53e-7c28-4704-9a8b-28378f965deb"
                },
                {
                    "angle": -151.010588043094,
                    "magnitude": 7324.39760974954,
                    "measurement_mrid": "_994bae95-3e38-4012-8cf1-82d97dcd1602"
                },
                {
                    "angle": -31.0224423540609,
                    "magnitude": 7326.75166910148,
                    "measurement_mrid": "_c4bc45a1-4dd5-495f-992b-842511247f2c"
                },
                {
                    "angle": 89.1027706077792,
                    "magnitude": 7283.43190032694,
                    "measurement_mrid": "_e79a1f9a-7238-49f0-b0f5-698629463bce"
                },
                {
                    "angle": 86.2754000134006,
                    "magnitude": 7338.77092532205,
                    "measurement_mrid": "_d081b4ca-caac-461a-9810-3f945bcb34f3"
                },
                {
                    "angle": -156.485616488268,
                    "magnitude": 7930.45111100045,
                    "measurement_mrid": "_f93581dd-5fe4-4768-9949-e207057ec07d"
                },
                {
                    "angle": -155.308645529469,
                    "magnitude": 7613.54006029128,
                    "measurement_mrid": "_80b8bf87-5318-44c7-a2e1-60b03151ada8"
                },
                {
                    "angle": -34.367736485646,
                    "magnitude": 7779.64724649697,
                    "measurement_mrid": "_ba5054c6-70ca-4eec-b680-0d993505a534"
                },
                {
                    "angle": -35.7342535940774,
                    "magnitude": 8244.71073607089,
                    "measurement_mrid": "_f42df6da-1066-413a-83f6-2749176be0bb"
                },
                {
                    "angle": -35.2898983398046,
                    "magnitude": 128.649657875784,
                    "measurement_mrid": "_9cbe2efc-2875-4886-bd7b-ef368b8b21a2"
                },
                {
                    "angle": -35.2662154583962,
                    "magnitude": 128.175709046828,
                    "measurement_mrid": "_d39596da-cf2b-4f31-b7b3-924d7eaefee7"
                },
                {
                    "angle": 86.8120328863595,
                    "magnitude": 120.600931109792,
                    "measurement_mrid": "_18e7e841-01ba-44fa-b179-a1569660e90f"
                },
                {
                    "angle": 86.8120328863595,
                    "magnitude": 120.600931109792,
                    "measurement_mrid": "_b332db5a-a510-4216-b74b-223acf4c1a38"
                },
                {
                    "angle": 87.5286073149504,
                    "magnitude": 7311.84546399282,
                    "measurement_mrid": "_54dcc73b-5287-4f2b-b1b7-01423addf015"
                },
                {
                    "angle": -156.597219301873,
                    "magnitude": 132.056793920423,
                    "measurement_mrid": "_0b481cc6-4e0a-44fe-99ae-d6a666628282"
                },
                {
                    "angle": -156.597219301873,
                    "magnitude": 132.056793920423,
                    "measurement_mrid": "_c20e884b-2f14-4136-b52d-697b0cae6b91"
                },
                {
                    "angle": -32.2650506648418,
                    "magnitude": 7315.64512353015,
                    "measurement_mrid": "_faafe3c5-fe10-41d4-ae7b-c62449dafcc5"
                },
                {
                    "angle": 87.1468363709918,
                    "magnitude": 7371.89369315284,
                    "measurement_mrid": "_6a424d46-d13d-4767-af35-a0d7fc2e04bd"
                },
                {
                    "angle": -154.67727969277,
                    "magnitude": 7781.92431259375,
                    "measurement_mrid": "_6bb996f7-88a5-4b75-b4bb-9697e6a762c7"
                },
                {
                    "angle": -34.3580303430175,
                    "magnitude": 8017.35341054063,
                    "measurement_mrid": "_6c126676-8de1-4bdb-a82b-b07ecefa50d3"
                },
                {
                    "angle": 86.4787344427695,
                    "magnitude": 7321.51693621406,
                    "measurement_mrid": "_ec8ebce2-73af-419c-a7c4-81725dec0d30"
                },
                {
                    "angle": -156.899709879083,
                    "magnitude": 131.393477302898,
                    "measurement_mrid": "_1bf31f85-52db-45f1-958a-0e35735efde4"
                },
                {
                    "angle": -156.899709879083,
                    "magnitude": 131.393477302898,
                    "measurement_mrid": "_5966a233-dc8b-4df1-b90c-b42bde88203d"
                },
                {
                    "angle": 85.1458288177543,
                    "magnitude": 122.227729274421,
                    "measurement_mrid": "_2e45d94d-3017-48a2-a99b-3f1c5ac8f45a"
                },
                {
                    "angle": 85.1173175714429,
                    "magnitude": 122.771131107322,
                    "measurement_mrid": "_a7325908-e455-4740-be77-bcbab3d35f6c"
                },
                {
                    "angle": -155.712158569756,
                    "magnitude": 126.401708616877,
                    "measurement_mrid": "_63f0a04e-71f5-4b14-9517-fadebfd0cd7b"
                },
                {
                    "angle": -155.712158569756,
                    "magnitude": 126.401708616877,
                    "measurement_mrid": "_f91d6ba7-72cf-4c1c-85cc-8d5d6c576bfd"
                },
                {
                    "angle": -156.413647014786,
                    "magnitude": 7881.73702612292,
                    "measurement_mrid": "_4c9fbbf0-e144-48fc-a6af-782aab16d017"
                },
                {
                    "angle": 85.8320284058538,
                    "magnitude": 121.136804153212,
                    "measurement_mrid": "_32c6bf59-cee9-4e5c-9184-c3a7015bac90"
                },
                {
                    "angle": 85.8320284058538,
                    "magnitude": 121.136804153212,
                    "measurement_mrid": "_fa02095d-20c6-4fd8-ac14-b97261bcfa3b"
                },
                {
                    "angle": -35.905271995695,
                    "magnitude": 137.844647986221,
                    "measurement_mrid": "_00b2b398-be4e-4eb3-b85c-9c2d936320c6"
                },
                {
                    "angle": -35.8831839260208,
                    "magnitude": 137.37069557224,
                    "measurement_mrid": "_966e184f-3579-4188-815d-d9e3e44fa85f"
                },
                {
                    "angle": -36.0798430166063,
                    "magnitude": 136.554675512483,
                    "measurement_mrid": "_54d90566-0fff-4394-8949-18a913854fbc"
                },
                {
                    "angle": -36.1020583812829,
                    "magnitude": 137.028629676144,
                    "measurement_mrid": "_d86eac06-7684-4c9e-98bf-28ce5915629a"
                },
                {
                    "angle": -155.560050386595,
                    "magnitude": 127.511496449766,
                    "measurement_mrid": "_05ac4c3e-e0a3-4429-9b76-6fff30361eaa"
                },
                {
                    "angle": -155.560050386595,
                    "magnitude": 127.511496449766,
                    "measurement_mrid": "_f128df46-37ae-4319-8771-762c8bd9e53a"
                },
                {
                    "angle": -156.841363381965,
                    "magnitude": 130.317865107856,
                    "measurement_mrid": "_495023d5-7562-49d1-96d6-a0b47b8d904e"
                },
                {
                    "angle": -156.856755324534,
                    "magnitude": 130.629902481785,
                    "measurement_mrid": "_cc2f6c38-d237-4ffa-9b98-f9b68523e0ef"
                },
                {
                    "angle": -156.505210487248,
                    "magnitude": 7920.59714714939,
                    "measurement_mrid": "_97afaf5e-e45a-4835-af83-bf3003b78d43"
                },
                {
                    "angle": 87.3118270555533,
                    "magnitude": 7301.58662361358,
                    "measurement_mrid": "_7763c95c-8958-4878-a96f-0322cb0f5dbc"
                },
                {
                    "angle": -152.213997045145,
                    "magnitude": 121.097955775014,
                    "measurement_mrid": "_94749643-c6e6-4ffc-ae05-4903a5a7c7f6"
                },
                {
                    "angle": -152.2029405433,
                    "magnitude": 120.89011013681,
                    "measurement_mrid": "_b2c74bc4-d49d-4ec1-ba74-0633402434ce"
                },
                {
                    "angle": -35.6999830357449,
                    "magnitude": 8263.6338652586,
                    "measurement_mrid": "_8ebed0b9-b454-485c-9088-c40a24d2c37b"
                },
                {
                    "angle": -154.292129387223,
                    "magnitude": 120.837245693325,
                    "measurement_mrid": "_11593f3f-9bed-422c-ad02-3be4f9e2c50d"
                },
                {
                    "angle": -154.275491791274,
                    "magnitude": 120.525207562621,
                    "measurement_mrid": "_6f919bec-04cb-4c38-8673-ed6b46373130"
                },
                {
                    "angle": -156.168723630606,
                    "magnitude": 128.098399092796,
                    "measurement_mrid": "_46698330-1570-4dbe-b6be-ba1cf12446e7"
                },
                {
                    "angle": -156.168723630606,
                    "magnitude": 128.098399092796,
                    "measurement_mrid": "_d063c646-c5a1-42d9-bcd3-cf1d8fa320c3"
                },
                {
                    "angle": 87.7837051570736,
                    "magnitude": 7306.67565919774,
                    "measurement_mrid": "_2e150e81-7759-494f-b026-d08a739773ef"
                },
                {
                    "angle": -152.92724804627,
                    "magnitude": 7319.37714440136,
                    "measurement_mrid": "_41fc24a5-f85e-426a-a1da-0b93c2277877"
                },
                {
                    "angle": -32.8241058771796,
                    "magnitude": 7305.17579033183,
                    "measurement_mrid": "_a70a10a8-84f0-478f-8645-7f8876c40585"
                },
                {
                    "angle": 87.9420193223681,
                    "magnitude": 7305.85040147311,
                    "measurement_mrid": "_cb883212-3284-452a-8a55-71bbf186a452"
                },
                {
                    "angle": -35.96297017325,
                    "magnitude": 137.910317770881,
                    "measurement_mrid": "_14e9a15c-0d9d-42cd-9926-ba4645c208e6"
                },
                {
                    "angle": -35.96297017325,
                    "magnitude": 137.910317770881,
                    "measurement_mrid": "_ed47bda7-ecf4-4b19-bdd0-d2a37d5d2f98"
                },
                {
                    "angle": -35.8936844647815,
                    "magnitude": 137.611513691597,
                    "measurement_mrid": "_67270017-715c-40ec-a2ee-26dc93c3a9af"
                },
                {
                    "angle": -35.8936844647815,
                    "magnitude": 137.611513691597,
                    "measurement_mrid": "_a4a16e36-a0b5-426a-9c25-fd3469137f96"
                },
                {
                    "angle": -35.7873493008615,
                    "magnitude": 8293.23646291907,
                    "measurement_mrid": "_f88c4cdc-bf09-4f52-93eb-d5a7a7305419"
                },
                {
                    "angle": -35.2857514904759,
                    "magnitude": 127.931090712262,
                    "measurement_mrid": "_b3c3fe65-ff6c-4d1b-9459-22af54b49dce"
                },
                {
                    "angle": -35.2857514904759,
                    "magnitude": 127.931090712262,
                    "measurement_mrid": "_e7d49ead-a269-4f9d-bbcc-d04ff38c56a9"
                },
                {
                    "angle": -155.777666354138,
                    "magnitude": 125.848484797243,
                    "measurement_mrid": "_24b99b74-f321-488f-a8a7-5709e09c30e8"
                },
                {
                    "angle": -155.777666354138,
                    "magnitude": 125.848484797243,
                    "measurement_mrid": "_df283132-cd75-473a-aedd-0eb40c9195c9"
                },
                {
                    "angle": -35.4288108811055,
                    "magnitude": 131.75977097577,
                    "measurement_mrid": "_0ebaf889-9c48-4ab3-8194-645e3026a660"
                },
                {
                    "angle": -35.4518482886291,
                    "magnitude": 132.233721232024,
                    "measurement_mrid": "_da781e33-cba0-491e-9199-7addd032e92c"
                },
                {
                    "angle": -32.8543054870854,
                    "magnitude": 7303.30869143814,
                    "measurement_mrid": "_b4effecb-66ab-41ea-83d2-796704afac38"
                },
                {
                    "angle": 87.7580649580852,
                    "magnitude": 7307.06285858708,
                    "measurement_mrid": "_27e3015c-9bdf-4f2c-93cb-54d6dc4661f5"
                },
                {
                    "angle": -32.9149626637252,
                    "magnitude": 7299.58216535037,
                    "measurement_mrid": "_6d85cacd-2111-4711-b3e6-020d99d294d1"
                },
                {
                    "angle": 87.6825622316956,
                    "magnitude": 7308.42048227425,
                    "measurement_mrid": "_2172aeb4-eb7a-49d9-b6bb-5ce890bffaab"
                },
                {
                    "angle": -156.947943075637,
                    "magnitude": 131.033971171033,
                    "measurement_mrid": "_326550d4-8431-4fbd-941a-850909864494"
                },
                {
                    "angle": -156.947943075637,
                    "magnitude": 131.033971171033,
                    "measurement_mrid": "_a0f43a44-eefe-495b-98e3-18e3f584df70"
                },
                {
                    "angle": -153.046084225836,
                    "magnitude": 7318.06051369709,
                    "measurement_mrid": "_282863c2-9451-458e-a43f-065f909589e6"
                },
                {
                    "angle": 86.2655101308848,
                    "magnitude": 7413.7152971498,
                    "measurement_mrid": "_62275f14-acc6-457b-a2ac-32dddad8fb61"
                },
                {
                    "angle": -154.607923219786,
                    "magnitude": 128.533795742676,
                    "measurement_mrid": "_7565ad35-236b-4abb-b6a0-ab246e6d9d63"
                },
                {
                    "angle": -154.597510820132,
                    "magnitude": 128.325948688747,
                    "measurement_mrid": "_fab3bb53-63d2-4f61-9e55-51756792b5a1"
                },
                {
                    "angle": -31.3214257111165,
                    "magnitude": 7324.44257093349,
                    "measurement_mrid": "_030e40a7-15ec-4854-82f2-b915e4f52d40"
                },
                {
                    "angle": 88.8728315981541,
                    "magnitude": 7286.81441753279,
                    "measurement_mrid": "_5b06cc2a-a7be-4d97-9f28-37dbcf4736ab"
                },
                {
                    "angle": -151.321918903206,
                    "magnitude": 7323.75152109764,
                    "measurement_mrid": "_eba1dff6-46a4-435c-a0a6-b8d7ee930dcf"
                },
                {
                    "angle": -156.768847063635,
                    "magnitude": 131.166546250368,
                    "measurement_mrid": "_03e99a19-ccf9-4d46-96b9-b137c9507bae"
                },
                {
                    "angle": -156.768847063635,
                    "magnitude": 131.166546250368,
                    "measurement_mrid": "_823bffdf-ebfc-4a25-a140-621ac5c5fe25"
                },
                {
                    "angle": -156.168456239912,
                    "magnitude": 128.100211138122,
                    "measurement_mrid": "_c64f5db9-eafb-48af-a916-e9bb9d2e8aff"
                },
                {
                    "angle": -156.168456239912,
                    "magnitude": 128.100211138122,
                    "measurement_mrid": "_e5b4b0c0-eede-4a37-9fc3-3cfac58c0850"
                },
                {
                    "angle": -36.0992481565634,
                    "magnitude": 136.752321914302,
                    "measurement_mrid": "_5fc88f70-4830-4eca-a6bf-56f1264c2d0c"
                },
                {
                    "angle": -36.0992481565634,
                    "magnitude": 136.752321914302,
                    "measurement_mrid": "_8477c285-af19-4572-8561-ce48ff927d9a"
                },
                {
                    "angle": 86.6879256909788,
                    "magnitude": 119.045277659633,
                    "measurement_mrid": "_5eb651e4-547e-42dc-a7c0-ccfdeab09a82"
                },
                {
                    "angle": 86.6441027499224,
                    "magnitude": 119.860659147088,
                    "measurement_mrid": "_de7bbf33-466f-4c88-94c4-36b2501f6346"
                },
                {
                    "angle": -31.4047622489129,
                    "magnitude": 7323.5000138786,
                    "measurement_mrid": "_1bfab61e-1115-44ab-8f63-712dfedbe504"
                },
                {
                    "angle": 88.8105041616378,
                    "magnitude": 7287.87844039747,
                    "measurement_mrid": "_65ec202b-0efe-4690-852e-54cfbd1be839"
                },
                {
                    "angle": -151.410863614332,
                    "magnitude": 7323.44796209246,
                    "measurement_mrid": "_78619f55-1ba3-4fc5-8daa-828b7a78cabb"
                },
                {
                    "angle": -35.8065101057169,
                    "magnitude": 8263.09357891699,
                    "measurement_mrid": "_b19c681d-ce01-4d61-8901-81ec9b712642"
                },
                {
                    "angle": -31.2338834799187,
                    "magnitude": 7324.74523477187,
                    "measurement_mrid": "_9416094e-9e12-4781-898f-64fcc060adb8"
                },
                {
                    "angle": 87.1937885587363,
                    "magnitude": 7238.34684338915,
                    "measurement_mrid": "_88afb6b4-ef61-414f-9e85-60aa9afc2461"
                },
                {
                    "angle": -35.7432370526074,
                    "magnitude": 8310.14601863366,
                    "measurement_mrid": "_b65bd4f4-fde6-45be-a02a-69c2d8d5152e"
                },
                {
                    "angle": -156.852090927853,
                    "magnitude": 130.445180134167,
                    "measurement_mrid": "_00b7eafb-c41a-492a-a67a-e79e107bdbef"
                },
                {
                    "angle": -156.852090927853,
                    "magnitude": 130.445180134167,
                    "measurement_mrid": "_17514ac3-409b-4ed6-ad9d-b0e271416770"
                },
                {
                    "angle": -155.281787407898,
                    "magnitude": 7627.58876624893,
                    "measurement_mrid": "_abdffd2c-bd3d-43d4-ac86-7e76a6e893e1"
                },
                {
                    "angle": 85.6463754944428,
                    "magnitude": 7416.8777156019,
                    "measurement_mrid": "_f909c89e-e390-4c24-86f0-39626828284c"
                },
                {
                    "angle": -156.860400743201,
                    "magnitude": 130.157430849427,
                    "measurement_mrid": "_5174e947-3f72-447e-b46b-066413c44570"
                },
                {
                    "angle": -156.875811468781,
                    "magnitude": 130.46946724149,
                    "measurement_mrid": "_f7cd69d2-a98e-4c36-b270-1f81f3835853"
                },
                {
                    "angle": 85.8172598872189,
                    "magnitude": 121.405797022256,
                    "measurement_mrid": "_2e9c436a-e5c6-44e0-9c36-ce1d03189390"
                },
                {
                    "angle": 85.8460922543193,
                    "magnitude": 120.862394830286,
                    "measurement_mrid": "_d4883750-247d-46bf-a3d3-d11eba76a615"
                },
                {
                    "angle": -36.1492365323128,
                    "magnitude": 137.178847764469,
                    "measurement_mrid": "_c4ff7db6-f58b-4105-a23d-08b9e6bd6472"
                },
                {
                    "angle": -36.1713544044696,
                    "magnitude": 137.652801762096,
                    "measurement_mrid": "_eb394f9f-5495-400a-82c9-248907cb6b57"
                },
                {
                    "angle": -154.059416334669,
                    "magnitude": 7287.99089003097,
                    "measurement_mrid": "_43f86e18-f820-4147-a813-c4d155bcd76f"
                },
                {
                    "angle": 87.3829433403245,
                    "magnitude": 7313.1607316295,
                    "measurement_mrid": "_822529da-6723-4b85-9f69-7a24aab82e96"
                },
                {
                    "angle": -33.7797410707634,
                    "magnitude": 7235.17783140926,
                    "measurement_mrid": "_e142feec-4eeb-49cf-be5e-af28b365328d"
                },
                {
                    "angle": -36.2615968783002,
                    "magnitude": 136.333585120324,
                    "measurement_mrid": "_9c97c510-2ba2-4374-8eff-5c284ef8da5a"
                },
                {
                    "angle": -36.2615968783002,
                    "magnitude": 136.333585120324,
                    "measurement_mrid": "_a0f7ceec-a595-4818-981c-73416ee02a01"
                },
                {
                    "angle": 88.8653444440895,
                    "magnitude": 7215.90214947745,
                    "measurement_mrid": "_fcc4e00f-9b09-4631-a6c0-fb48f68d668c"
                },
                {
                    "angle": -155.745446921466,
                    "magnitude": 7728.68725988424,
                    "measurement_mrid": "_511a13b9-adf7-4006-8215-6e97a16f101a"
                },
                {
                    "angle": 85.7657254931556,
                    "magnitude": 122.112789388051,
                    "measurement_mrid": "_448a7df1-b70a-4898-bd64-cce80d0573d9"
                },
                {
                    "angle": 85.7371874695769,
                    "magnitude": 122.656191564843,
                    "measurement_mrid": "_d0660749-4d37-4c0d-bdcf-620a0e8820d0"
                },
                {
                    "angle": -156.951826344431,
                    "magnitude": 131.002862766839,
                    "measurement_mrid": "_c1f7abee-5cc4-4bef-b80e-9575d63d6926"
                },
                {
                    "angle": -156.951826344431,
                    "magnitude": 131.002862766839,
                    "measurement_mrid": "_e5879ffb-567c-42ae-bf5e-f69742d16ae0"
                },
                {
                    "angle": 85.730244296329,
                    "magnitude": 122.205011080198,
                    "measurement_mrid": "_299baffe-3442-46e2-a755-5fb65a060ada"
                },
                {
                    "angle": 85.730244296329,
                    "magnitude": 122.205011080198,
                    "measurement_mrid": "_8dc6fe5c-1a04-488b-a271-baaa184145bb"
                },
                {
                    "angle": 85.969912941153,
                    "magnitude": 120.942691129883,
                    "measurement_mrid": "_d64399be-01ef-4476-b495-a160e321f9b2"
                },
                {
                    "angle": 85.969912941153,
                    "magnitude": 120.942691129883,
                    "measurement_mrid": "_d7419d7f-cd02-4180-b24f-d3f34aadc4da"
                },
                {
                    "angle": -155.086008386348,
                    "magnitude": 120.966444769,
                    "measurement_mrid": "_90b1ab9a-f792-433d-b9f9-f09417fbc7aa"
                },
                {
                    "angle": -155.044484415476,
                    "magnitude": 120.186866541081,
                    "measurement_mrid": "_f86f2b86-bec4-4aa0-a113-1da2075bc668"
                },
                {
                    "angle": 86.0945043981192,
                    "magnitude": 7319.43961822749,
                    "measurement_mrid": "_16f68846-7b10-49d8-bf9c-2d468b86e2fb"
                },
                {
                    "angle": 85.9136641467747,
                    "magnitude": 122.202396248907,
                    "measurement_mrid": "_bc30b79e-999c-4207-89f5-4909f79ae4be"
                },
                {
                    "angle": 85.9308462581606,
                    "magnitude": 121.876465680893,
                    "measurement_mrid": "_dbd0b214-7adb-4c00-b8e6-37da188e9e50"
                },
                {
                    "angle": 88.9893686713031,
                    "magnitude": 7268.46790762381,
                    "measurement_mrid": "_acea0403-288b-406f-9449-d668416bd03b"
                },
                {
                    "angle": -36.1360529638552,
                    "magnitude": 137.540767684435,
                    "measurement_mrid": "_25765495-048f-4c5d-a8a5-ca54d7b05de9"
                },
                {
                    "angle": -36.1360529638552,
                    "magnitude": 137.540767684435,
                    "measurement_mrid": "_da299d5f-a315-49cc-9913-df9a81e286b3"
                },
                {
                    "angle": -155.707208405091,
                    "magnitude": 7748.83306463363,
                    "measurement_mrid": "_a733f553-80d3-4679-85a3-83886153d43f"
                },
                {
                    "angle": -34.8342816507034,
                    "magnitude": 7709.20989165953,
                    "measurement_mrid": "_53858bb9-80d7-4ee0-bc64-2777a975226a"
                },
                {
                    "angle": -155.602528052936,
                    "magnitude": 127.199260943767,
                    "measurement_mrid": "_155022ec-6f6d-4e05-9768-53c2a11e3fd7"
                },
                {
                    "angle": -155.602528052936,
                    "magnitude": 127.199260943767,
                    "measurement_mrid": "_5715b837-65f5-4ae4-9b1d-688ead698dcb"
                },
                {
                    "angle": -156.843290804654,
                    "magnitude": 130.299794165889,
                    "measurement_mrid": "_46606172-3674-4226-8098-bb8d1f5911c1"
                },
                {
                    "angle": -156.858684650572,
                    "magnitude": 130.611830627052,
                    "measurement_mrid": "_f20c5961-3c5f-4479-93a7-007b45c02383"
                },
                {
                    "angle": -156.123855045538,
                    "magnitude": 7980.85633777961,
                    "measurement_mrid": "_6690aafa-0dd8-476b-9e53-67b1c1adb3cd"
                },
                {
                    "angle": 86.478672004826,
                    "magnitude": 7320.71318377527,
                    "measurement_mrid": "_88550dc5-676a-41f9-806b-7c8be6c0c62f"
                },
                {
                    "angle": -35.7061058233009,
                    "magnitude": 8261.88140859824,
                    "measurement_mrid": "_be14fa01-98db-43f8-9a0c-9d4a42e29e48"
                },
                {
                    "angle": 88.4272765753412,
                    "magnitude": 119.352190649474,
                    "measurement_mrid": "_2b3c99ad-d75a-45dc-a4df-b75eebf7df65"
                },
                {
                    "angle": 88.3980802849462,
                    "magnitude": 119.895592720834,
                    "measurement_mrid": "_b768822b-0ed5-487a-af36-c4401c49fe02"
                },
                {
                    "angle": 86.3887850954006,
                    "magnitude": 7363.24510044544,
                    "measurement_mrid": "_f3067ff6-d579-498f-9e8a-70eb14cdba87"
                },
                {
                    "angle": -156.465838182862,
                    "magnitude": 7941.59264542169,
                    "measurement_mrid": "_d467db65-0660-486a-b315-ffa92cb3cfc2"
                },
                {
                    "angle": -156.879239444867,
                    "magnitude": 130.209727380247,
                    "measurement_mrid": "_9047df8c-d6bd-414a-93a3-17a0a6aa9db2"
                },
                {
                    "angle": -156.879239444867,
                    "magnitude": 130.209727380247,
                    "measurement_mrid": "_d8a2c29b-3596-41a5-993b-3c0b129b6f9d"
                },
                {
                    "angle": 88.4126452800963,
                    "magnitude": 119.623888302245,
                    "measurement_mrid": "_f978ffc5-3f93-4ae7-a5c0-08e251100098"
                },
                {
                    "angle": 88.4126452800963,
                    "magnitude": 119.623888302245,
                    "measurement_mrid": "_fdb0c65d-2979-417b-90dd-7c7a8cc0d685"
                },
                {
                    "angle": 86.2583025074762,
                    "magnitude": 7410.22295380221,
                    "measurement_mrid": "_f465d26d-c220-46ec-993f-f603a6dc31c4"
                },
                {
                    "angle": -156.376100861373,
                    "magnitude": 7901.89609204361,
                    "measurement_mrid": "_455cb532-5f2b-4e89-bed9-a154c1df4677"
                },
                {
                    "angle": -36.090035523753,
                    "magnitude": 137.762237575564,
                    "measurement_mrid": "_3b241686-d959-49fe-bb47-d7cb229d8d9f"
                },
                {
                    "angle": -36.090035523753,
                    "magnitude": 137.762237575564,
                    "measurement_mrid": "_3fc3a9cd-9fb4-4f76-be39-04722183376d"
                },
                {
                    "angle": -154.283039701946,
                    "magnitude": 120.686844309329,
                    "measurement_mrid": "_003aaefe-2ee1-489a-9c7b-85fec2fe7f98"
                },
                {
                    "angle": -154.283039701946,
                    "magnitude": 120.686844309329,
                    "measurement_mrid": "_5fb583ae-7259-4c4c-9bd5-8c02969f4859"
                },
                {
                    "angle": 87.2303953596401,
                    "magnitude": 120.501291166105,
                    "measurement_mrid": "_4f69bde8-6daa-47ac-85cd-0925ffe0eda2"
                },
                {
                    "angle": 87.2130174200877,
                    "magnitude": 120.827221219766,
                    "measurement_mrid": "_7893a2f8-1de6-47a5-8114-f32b0ae0d722"
                },
                {
                    "angle": -35.8792396780739,
                    "magnitude": 8232.83986082649,
                    "measurement_mrid": "_2a2928c7-dacc-4468-adfd-87d5cf443843"
                },
                {
                    "angle": -35.7850792266526,
                    "magnitude": 8294.50173064589,
                    "measurement_mrid": "_74e5f8a8-2517-484d-9145-4ec03dd7fc91"
                },
                {
                    "angle": 86.2885296399863,
                    "magnitude": 7344.72968638533,
                    "measurement_mrid": "_1692c300-3235-4015-bfed-0c29bab06c34"
                },
                {
                    "angle": -35.6111281411618,
                    "magnitude": 8319.97071583119,
                    "measurement_mrid": "_df2dbd15-5ba6-45d6-8e1d-d55d32be26a1"
                },
                {
                    "angle": -156.451597587428,
                    "magnitude": 7945.64545139187,
                    "measurement_mrid": "_a0a7c5fe-be15-4a96-9c61-c9c42453530e"
                },
                {
                    "angle": -35.6084140053995,
                    "magnitude": 8319.12077220277,
                    "measurement_mrid": "_da908a0f-8c6c-4b35-b69f-3f0b43c7a9eb"
                },
                {
                    "angle": -35.6957142260021,
                    "magnitude": 8265.48852425058,
                    "measurement_mrid": "_1880e410-49dd-4dd6-ba35-d772d2e0895e"
                },
                {
                    "angle": -156.128326324727,
                    "magnitude": 7980.56588395915,
                    "measurement_mrid": "_23e55684-aa74-49f7-aeb8-4560b372b4f3"
                },
                {
                    "angle": 86.4788488556349,
                    "magnitude": 7324.40560852382,
                    "measurement_mrid": "_f8833e6e-e04c-4566-b5c9-41d804ebcc4b"
                },
                {
                    "angle": -34.8656099188241,
                    "magnitude": 7732.51135484791,
                    "measurement_mrid": "_501f333b-86be-4518-b9c3-2b36394cd71e"
                },
                {
                    "angle": 88.9057972006425,
                    "magnitude": 120.180103913376,
                    "measurement_mrid": "_39845e37-8673-4452-bc5b-a67c6731d8bb"
                },
                {
                    "angle": 88.9057972006425,
                    "magnitude": 120.180103913376,
                    "measurement_mrid": "_91da49ab-fbbf-4916-8e48-069c43d63a8b"
                },
                {
                    "angle": -156.910420506376,
                    "magnitude": 130.22483722272,
                    "measurement_mrid": "_8d692f95-ce07-4045-812a-43cd6eaa4428"
                },
                {
                    "angle": -156.910420506376,
                    "magnitude": 130.22483722272,
                    "measurement_mrid": "_e073a678-9607-48f3-ac92-2e91ee4013d1"
                },
                {
                    "angle": 85.7297503996285,
                    "magnitude": 122.201552914374,
                    "measurement_mrid": "_109f74c1-a18f-4363-8689-4c7f0042e6a3"
                },
                {
                    "angle": 85.7297503996285,
                    "magnitude": 122.201552914374,
                    "measurement_mrid": "_fe086d77-d0f9-4206-b5dd-a23cefcfed0d"
                },
                {
                    "angle": 105.497301946502,
                    "magnitude": 99.9990985901608,
                    "measurement_mrid": "_030aa799-2e7e-4557-b9d7-26695b723d1b"
                },
                {
                    "angle": -144.377024046064,
                    "magnitude": 130.28565314534,
                    "measurement_mrid": "_9531d966-f178-4af3-ac34-985b505f2d6f"
                },
                {
                    "angle": -22.7302237227328,
                    "magnitude": 129.220334546801,
                    "measurement_mrid": "_a9c9ed1d-4b1c-45fd-b647-a15636c2c686"
                },
                {
                    "angle": -155.771048063824,
                    "magnitude": 125.753991048603,
                    "measurement_mrid": "_e32ff3bf-142f-45b7-9f7e-9166b1b6da72"
                },
                {
                    "angle": -155.781665528694,
                    "magnitude": 125.961839647532,
                    "measurement_mrid": "_e9184386-a319-42d1-8627-e92dc79b3c0b"
                },
                {
                    "angle": -36.2094418510515,
                    "magnitude": 136.796927723647,
                    "measurement_mrid": "_273e5148-424a-4771-93df-b42f7c5ba299"
                },
                {
                    "angle": -36.2094418510515,
                    "magnitude": 136.796927723647,
                    "measurement_mrid": "_95ca1f56-490e-4950-bdf3-89b9a66506be"
                },
                {
                    "angle": -36.1888572954577,
                    "magnitude": 137.524850282538,
                    "measurement_mrid": "_13266f8d-c3e3-4353-b5d5-b6d5834e098f"
                },
                {
                    "angle": -36.1667196869861,
                    "magnitude": 137.050897235086,
                    "measurement_mrid": "_41676ed5-c88d-4add-82b8-d2431891967f"
                },
                {
                    "angle": 88.8587337006265,
                    "magnitude": 7212.71379862176,
                    "measurement_mrid": "_693d9386-612b-44ee-995b-e3cdcffd5494"
                },
                {
                    "angle": 86.9796878735345,
                    "magnitude": 121.072733931308,
                    "measurement_mrid": "_9dcf9374-178a-44c8-bf74-a5e072e02fe4"
                },
                {
                    "angle": 87.0086015949317,
                    "magnitude": 120.529332619334,
                    "measurement_mrid": "_cff95e7a-c617-4375-9fd4-b889a3ab5d48"
                },
                {
                    "angle": 86.8189749522464,
                    "magnitude": 7388.15248388477,
                    "measurement_mrid": "_6fff2586-2572-451e-8346-b01039ef4ccb"
                },
                {
                    "angle": -155.406166144967,
                    "magnitude": 7771.06756784207,
                    "measurement_mrid": "_a456eb63-3c39-4ac3-87cd-3dea6b8c0d9e"
                },
                {
                    "angle": -34.8955391987089,
                    "magnitude": 7987.75302197952,
                    "measurement_mrid": "_f1e58637-e369-428e-8b8c-f2cb3930adcc"
                },
                {
                    "angle": 85.9145571479073,
                    "magnitude": 121.482739833749,
                    "measurement_mrid": "_a893ffd4-ac2a-4180-b947-4e59ebb6f508"
                },
                {
                    "angle": 85.8858706553314,
                    "magnitude": 122.026140589846,
                    "measurement_mrid": "_e80ee1c6-2460-4d94-87c5-8af0f961fb5b"
                },
                {
                    "angle": 86.1057645504494,
                    "magnitude": 7324.61476575436,
                    "measurement_mrid": "_f15b87b6-6052-4136-a7af-4e3edc4006f5"
                },
                {
                    "angle": -36.1305160965563,
                    "magnitude": 136.243944980828,
                    "measurement_mrid": "_2fd409fd-5fa7-470e-a28e-4d3dc0e97a4f"
                },
                {
                    "angle": -36.1438885737101,
                    "magnitude": 136.528209175105,
                    "measurement_mrid": "_abc32826-c02e-4505-95d2-3938b3dc20d3"
                },
                {
                    "angle": 85.7823009030036,
                    "magnitude": 121.1819281937,
                    "measurement_mrid": "_926bc78f-0cc1-4ae9-9243-aea5740f2865"
                },
                {
                    "angle": 85.7707615693059,
                    "magnitude": 121.399391771433,
                    "measurement_mrid": "_d7cfba11-fecf-433e-b0d2-bfadeed5170e"
                },
                {
                    "angle": -35.7085927680919,
                    "magnitude": 8261.12314144432,
                    "measurement_mrid": "_2c880097-9444-4e31-95ab-552d90f3465a"
                },
                {
                    "angle": -34.7137428752376,
                    "magnitude": 119.639062273981,
                    "measurement_mrid": "_c2f1b0cd-0d14-4ed0-8cc5-680290ad6e8a"
                },
                {
                    "angle": -34.6882699459698,
                    "magnitude": 119.165113129099,
                    "measurement_mrid": "_f678d8a5-92fb-4a45-b314-db9873179367"
                },
                {
                    "angle": -35.7098385843861,
                    "magnitude": 8260.62658929542,
                    "measurement_mrid": "_f178275a-110e-4dce-accb-520d224c0dbd"
                },
                {
                    "angle": -156.739706972402,
                    "magnitude": 131.304138523981,
                    "measurement_mrid": "_5407f5c2-7bac-49e4-91a5-23335b058fa8"
                },
                {
                    "angle": -156.739706972402,
                    "magnitude": 131.304138523981,
                    "measurement_mrid": "_8495cb9e-d2a3-4153-80d0-94194433e9f2"
                },
                {
                    "angle": -34.2272231765717,
                    "magnitude": 7221.7034081561,
                    "measurement_mrid": "_d06fbc50-ef1b-4765-af97-b8a76595544f"
                },
                {
                    "angle": -35.7313913528596,
                    "magnitude": 8246.2931201509,
                    "measurement_mrid": "_c6787497-11f6-4a87-90a4-4c3cc2fc0a3e"
                },
                {
                    "angle": -36.1609576098777,
                    "magnitude": 137.271863392003,
                    "measurement_mrid": "_111f02f1-5a98-4cda-84c3-102d71b49489"
                },
                {
                    "angle": -36.1698222237095,
                    "magnitude": 137.461549412887,
                    "measurement_mrid": "_4b79623c-d6eb-4e3f-b6e8-f041f0662d46"
                },
                {
                    "angle": -156.948534871952,
                    "magnitude": 131.031499898902,
                    "measurement_mrid": "_6e3634f7-5920-4845-bf39-2e324495ef27"
                },
                {
                    "angle": -156.948534871952,
                    "magnitude": 131.031499898902,
                    "measurement_mrid": "_be0af756-8af7-406d-96e9-ab6050101122"
                },
                {
                    "angle": -156.394126933031,
                    "magnitude": 7892.45740311383,
                    "measurement_mrid": "_86265f9d-9fad-4b3b-8461-7a313f3139a4"
                },
                {
                    "angle": -156.887009204246,
                    "magnitude": 130.37257639826,
                    "measurement_mrid": "_8121f055-3f58-4f7e-91e8-80d43c3bb2af"
                },
                {
                    "angle": -156.871587251345,
                    "magnitude": 130.060539386067,
                    "measurement_mrid": "_949371cd-2057-4295-8f59-d84e48a30581"
                },
                {
                    "angle": -35.9990066604309,
                    "magnitude": 137.791877833495,
                    "measurement_mrid": "_20e29d02-9ca9-4bbf-80b3-91516b290a2b"
                },
                {
                    "angle": -35.9857542207987,
                    "magnitude": 137.507615094052,
                    "measurement_mrid": "_bc2f3465-01be-4f61-b947-40572949c0eb"
                },
                {
                    "angle": -156.886585135205,
                    "magnitude": 130.522710507523,
                    "measurement_mrid": "_a3c3bebd-455d-4562-b1f3-9ca0652d7d66"
                },
                {
                    "angle": -156.860920320898,
                    "magnitude": 130.002822338508,
                    "measurement_mrid": "_faece4f8-9220-4c54-8310-a9c1feb1fa8a"
                },
                {
                    "angle": -35.619710737718,
                    "magnitude": 8343.04070992615,
                    "measurement_mrid": "_023836c0-66b2-4b65-a6e7-a935cfdfdfed"
                },
                {
                    "angle": 86.4250844788663,
                    "magnitude": 7386.33794191124,
                    "measurement_mrid": "_6fb01f2d-6449-4cc9-ab29-c52c8646f30d"
                },
                {
                    "angle": -156.216471211132,
                    "magnitude": 7996.51461837311,
                    "measurement_mrid": "_cb8939f3-f57f-4397-9740-98752a3665c6"
                },
                {
                    "angle": 86.7087572081218,
                    "magnitude": 119.79264561105,
                    "measurement_mrid": "_a74efad8-98ce-440d-bd1d-9f41707f1f8f"
                },
                {
                    "angle": 86.7087572081218,
                    "magnitude": 119.79264561105,
                    "measurement_mrid": "_db3d40e9-b522-49ff-80d9-1ee3fab7e21c"
                },
                {
                    "angle": -34.7594548385835,
                    "magnitude": 7995.20157483917,
                    "measurement_mrid": "_3fbcf1ef-8840-43e8-883a-f92b3b6aab1b"
                },
                {
                    "angle": -155.217469095149,
                    "magnitude": 7773.86222002666,
                    "measurement_mrid": "_6bd608bb-704f-43de-9f2d-79cb28b38678"
                },
                {
                    "angle": 86.902482951349,
                    "magnitude": 7383.66919321658,
                    "measurement_mrid": "_a7b8ea0e-7bed-4257-a1bc-42e6ffb200a3"
                },
                {
                    "angle": -154.057929828019,
                    "magnitude": 7291.54203288927,
                    "measurement_mrid": "_088e9979-21ce-448a-8785-9b6744b7276a"
                },
                {
                    "angle": -156.408752729882,
                    "magnitude": 7898.81708953913,
                    "measurement_mrid": "_6c55f9c6-3c56-4e05-b538-97e6b034a0fe"
                },
                {
                    "angle": -155.705266921841,
                    "magnitude": 7749.92304161791,
                    "measurement_mrid": "_9e9fb023-8b42-4831-ace1-45a4d3fe1ba1"
                },
                {
                    "angle": -36.1501026885136,
                    "magnitude": 137.41120723281,
                    "measurement_mrid": "_580b6649-4bee-4667-8862-3c1743185aab"
                },
                {
                    "angle": -36.1501026885136,
                    "magnitude": 137.41120723281,
                    "measurement_mrid": "_a9fa44e1-4b42-4607-80fa-8699a6e8927c"
                },
                {
                    "angle": -154.673457185155,
                    "magnitude": 7295.63249834471,
                    "measurement_mrid": "_2ba21ee5-5457-4d7c-b1e8-844aa2c22001"
                },
                {
                    "angle": -34.3551564866554,
                    "magnitude": 7215.76232393905,
                    "measurement_mrid": "_50f1b07f-1e6d-4786-b83f-020496214409"
                },
                {
                    "angle": 87.1487950939664,
                    "magnitude": 7325.76050582115,
                    "measurement_mrid": "_aab6e776-d738-4ee6-ae4b-3d8f3e66b7e7"
                },
                {
                    "angle": -36.1553547754809,
                    "magnitude": 137.255545868987,
                    "measurement_mrid": "_2cbd4976-9e73-4545-b4ad-11b80ab5b2b0"
                },
                {
                    "angle": -36.1686317253559,
                    "magnitude": 137.539808602071,
                    "measurement_mrid": "_a1bdb48c-f173-454e-8055-2f94d50e9226"
                },
                {
                    "angle": -34.7630636040861,
                    "magnitude": 128.563398808862,
                    "measurement_mrid": "_8667f759-a07f-4467-84ed-621f9aedb0fa"
                },
                {
                    "angle": -34.7866801598742,
                    "magnitude": 129.037347218664,
                    "measurement_mrid": "_ea0bce89-5ded-4750-a004-c8a66e4da54b"
                },
                {
                    "angle": 86.6748426230602,
                    "magnitude": 119.287741447226,
                    "measurement_mrid": "_4138db0d-5bde-4fde-b588-f369c926d7b8"
                },
                {
                    "angle": 86.6572883054403,
                    "magnitude": 119.6136714038,
                    "measurement_mrid": "_414b5287-0362-49d1-8a89-5412724df79b"
                },
                {
                    "angle": -155.736429280829,
                    "magnitude": 7733.53336853478,
                    "measurement_mrid": "_15d0089b-ef06-4055-8768-2eb64d997ac4"
                },
                {
                    "angle": 85.9287870977461,
                    "magnitude": 121.852406865145,
                    "measurement_mrid": "_718f2841-ed16-4a2a-b08f-5f2b2438983f"
                },
                {
                    "angle": 85.940284069466,
                    "magnitude": 121.634942728715,
                    "measurement_mrid": "_b91b4340-0345-4517-a3d4-05dc08ebaec5"
                },
                {
                    "angle": 85.9383484464287,
                    "magnitude": 121.949769427488,
                    "measurement_mrid": "_6fe124fa-e652-4968-a730-8bdde807b8e8"
                },
                {
                    "angle": 85.9383484464287,
                    "magnitude": 121.949769427488,
                    "measurement_mrid": "_9f1e0cee-74e4-4485-a3e1-b7c260be6522"
                },
                {
                    "angle": 85.8942212380054,
                    "magnitude": 7420.93743466575,
                    "measurement_mrid": "_9332e268-7dcf-4dd4-9992-c8b336b728e1"
                },
                {
                    "angle": -154.77670835838,
                    "magnitude": 7738.1269503807,
                    "measurement_mrid": "_9a8768e3-5bd3-4fbe-8a7d-33b2f5c57209"
                },
                {
                    "angle": -34.576252801427,
                    "magnitude": 7775.65528928983,
                    "measurement_mrid": "_dfbceaf5-16ad-49c8-a430-b6bb053cfaea"
                },
                {
                    "angle": -154.83727295264,
                    "magnitude": 7734.64555449471,
                    "measurement_mrid": "_2559802e-ba97-4059-9246-53ee95f05a7f"
                },
                {
                    "angle": 85.8467018736895,
                    "magnitude": 7422.13397698488,
                    "measurement_mrid": "_3228c5ca-d59f-4249-93ab-7e00640b2177"
                },
                {
                    "angle": -34.6252350687686,
                    "magnitude": 7773.24980590662,
                    "measurement_mrid": "_f93be60b-7e3c-4a98-9019-9b0dab1ff257"
                },
                {
                    "angle": 85.91154883309,
                    "magnitude": 121.928018584196,
                    "measurement_mrid": "_37e1ff33-0dc0-4b86-811c-0f82e336dd1e"
                },
                {
                    "angle": 85.91154883309,
                    "magnitude": 121.928018584196,
                    "measurement_mrid": "_f7111a02-8ca1-4a14-ad04-0d907eb2ecea"
                },
                {
                    "angle": 85.9533472323106,
                    "magnitude": 7419.55199506047,
                    "measurement_mrid": "_2fb40f42-f967-48aa-8775-23e950ae45a7"
                },
                {
                    "angle": -34.5152724327858,
                    "magnitude": 7778.70655932862,
                    "measurement_mrid": "_71c49590-0c74-4067-9d64-1c37968cc415"
                },
                {
                    "angle": -154.701647120505,
                    "magnitude": 7742.45749152655,
                    "measurement_mrid": "_874fc795-87e0-43a8-8cd3-1939353d4101"
                },
                {
                    "angle": 86.6718583634888,
                    "magnitude": 119.497292408362,
                    "measurement_mrid": "_1a6f9abb-0e8e-4b48-b591-787791b76bae"
                },
                {
                    "angle": 86.6718583634888,
                    "magnitude": 119.497292408362,
                    "measurement_mrid": "_e93a4226-a3a1-4750-a9b1-607f51477a0c"
                },
                {
                    "angle": 87.5453461531765,
                    "magnitude": 7311.47483410132,
                    "measurement_mrid": "_c2510b63-18b6-4a2c-ac5a-981e68600f79"
                },
                {
                    "angle": 85.941207282907,
                    "magnitude": 121.50288578393,
                    "measurement_mrid": "_94179a07-a9dc-4848-b25e-1338962b6ccc"
                },
                {
                    "angle": 85.9988248008776,
                    "magnitude": 120.416051764347,
                    "measurement_mrid": "_e48a2c29-7a6c-47a1-821d-7a6e6431611a"
                },
                {
                    "angle": 86.2866164038809,
                    "magnitude": 7343.74901557946,
                    "measurement_mrid": "_d542ab9c-913d-4c89-b88a-2c9efeddc4df"
                },
                {
                    "angle": 85.7721378757532,
                    "magnitude": 121.254148505079,
                    "measurement_mrid": "_18b2af1f-022a-46a5-b209-7e663f1d4dea"
                },
                {
                    "angle": 85.7721378757532,
                    "magnitude": 121.254148505079,
                    "measurement_mrid": "_4ebfcc4c-635f-493f-a212-f87ff38bbb7b"
                },
                {
                    "angle": -34.7809429615574,
                    "magnitude": 7993.99697659894,
                    "measurement_mrid": "_8b7594e6-8b22-45f4-a772-69413e1f55ea"
                },
                {
                    "angle": 86.2843237264306,
                    "magnitude": 7344.42955986267,
                    "measurement_mrid": "_6c535bea-2f4d-4040-a456-c4a97486c03c"
                },
                {
                    "angle": -35.6064241653897,
                    "magnitude": 8318.47933084658,
                    "measurement_mrid": "_b5b8ca03-493d-4e31-a067-ddd6d58532c4"
                },
                {
                    "angle": -156.248659055464,
                    "magnitude": 7952.36403210411,
                    "measurement_mrid": "_d7fdf9b2-4d88-42ff-bc01-70bd4e5ace69"
                },
                {
                    "angle": -36.131262151659,
                    "magnitude": 136.237188538119,
                    "measurement_mrid": "_794a54f6-fb91-4652-ad71-f8e6a44f359d"
                },
                {
                    "angle": -36.1446351575974,
                    "magnitude": 136.521451903667,
                    "measurement_mrid": "_7c6c0285-24d6-4172-8d0b-983d880dd740"
                },
                {
                    "angle": -35.7779844196709,
                    "magnitude": 8297.33962694725,
                    "measurement_mrid": "_e1217f25-9c2d-4d01-81ba-530aaba626ee"
                },
                {
                    "angle": -35.652725761426,
                    "magnitude": 8293.23793537389,
                    "measurement_mrid": "_509d2eb6-f30f-4a8d-95d5-1d97f29361ec"
                },
                {
                    "angle": 86.277992797951,
                    "magnitude": 7339.52465323394,
                    "measurement_mrid": "_9b545e6b-c654-49a9-8a3d-13ddb429fc09"
                },
                {
                    "angle": 85.737523825735,
                    "magnitude": 122.265479343612,
                    "measurement_mrid": "_24bf0bd0-394f-4736-86ad-32d497926c23"
                },
                {
                    "angle": 85.737523825735,
                    "magnitude": 122.265479343612,
                    "measurement_mrid": "_c5390d6d-269c-48c7-a722-837ccbf17c98"
                },
                {
                    "angle": -156.413455450465,
                    "magnitude": 7882.1341744939,
                    "measurement_mrid": "_adfe19c1-33bf-4844-9fc0-6737fe3e3a28"
                },
                {
                    "angle": 86.367801320413,
                    "magnitude": 7348.61638039094,
                    "measurement_mrid": "_06aa3584-9df0-4778-9594-dae74eec1fa2"
                },
                {
                    "angle": -35.828907369781,
                    "magnitude": 8259.35751068181,
                    "measurement_mrid": "_7b1ffad2-b43e-4b2d-bf17-568e6beaecb4"
                },
                {
                    "angle": -156.454006726099,
                    "magnitude": 7948.28763555365,
                    "measurement_mrid": "_99e1434b-7ff9-4f29-88eb-e4b731b84120"
                },
                {
                    "angle": -153.328077709157,
                    "magnitude": 7307.11524507565,
                    "measurement_mrid": "_00dcef02-0989-4a11-bae0-3b9789204707"
                },
                {
                    "angle": -33.2367887794406,
                    "magnitude": 7328.58454642759,
                    "measurement_mrid": "_49f9488d-6c30-4aa8-82d1-1ab8f84271b3"
                },
                {
                    "angle": 87.1485673760899,
                    "magnitude": 7292.58334298745,
                    "measurement_mrid": "_52aebcf6-d6f7-45c2-b7d4-e2135b229319"
                },
                {
                    "angle": -156.453785200771,
                    "magnitude": 7947.52986143935,
                    "measurement_mrid": "_69701ea5-a321-4d86-8e64-444e1d57208d"
                },
                {
                    "angle": 86.3654715470025,
                    "magnitude": 7346.85708107763,
                    "measurement_mrid": "_8e3612f7-55bc-4a4a-881b-d6afec7e258c"
                },
                {
                    "angle": -35.8321318540784,
                    "magnitude": 8257.43340906079,
                    "measurement_mrid": "_cd2658a6-4a6c-446b-835a-f27e66139786"
                },
                {
                    "angle": -156.41571166987,
                    "magnitude": 7881.0165801607,
                    "measurement_mrid": "_5cbc4454-2a2f-47ad-bc86-530c1caa3a9f"
                },
                {
                    "angle": -36.1699432672245,
                    "magnitude": 137.042432390197,
                    "measurement_mrid": "_7c7c6f8e-b975-48cd-bb95-72cbf19de195"
                },
                {
                    "angle": -36.1920828637762,
                    "magnitude": 137.516385483353,
                    "measurement_mrid": "_f63f2bc3-e24a-40fe-96f3-7eca13a26b68"
                },
                {
                    "angle": -33.7832459135077,
                    "magnitude": 7238.22748097006,
                    "measurement_mrid": "_e20425c4-c77f-47ff-bdb0-3c8dc7c574de"
                },
                {
                    "angle": 87.1816515076383,
                    "magnitude": 7232.3362783335,
                    "measurement_mrid": "_17b10a65-b68e-498e-919e-93f4e3660508"
                },
                {
                    "angle": 85.7172014843715,
                    "magnitude": 122.510071259148,
                    "measurement_mrid": "_d1094ec7-f755-4ccb-80fa-54488e387d37"
                },
                {
                    "angle": 85.7172014843715,
                    "magnitude": 122.510071259148,
                    "measurement_mrid": "_e74b080f-1275-429a-b963-88f9c67659f8"
                },
                {
                    "angle": -156.68939937441,
                    "magnitude": 132.004895378977,
                    "measurement_mrid": "_04e6f574-b977-4712-84ce-5681c51d60d6"
                },
                {
                    "angle": -156.704597869195,
                    "magnitude": 132.316932042166,
                    "measurement_mrid": "_7ff3491c-822b-4b35-8565-3c614efea1ea"
                },
                {
                    "angle": -33.4746653992499,
                    "magnitude": 121.332846522725,
                    "measurement_mrid": "_1f159cca-dd4b-4a09-9fce-2f9afbf931de"
                },
                {
                    "angle": -33.4746653992499,
                    "magnitude": 121.332846522725,
                    "measurement_mrid": "_a5141811-48df-481c-b79c-0e89bc4c509c"
                },
                {
                    "angle": -154.386467477426,
                    "magnitude": 120.664997194304,
                    "measurement_mrid": "_4b0d7501-642f-48b8-a20a-f6b28210bcdb"
                },
                {
                    "angle": -154.386467477426,
                    "magnitude": 120.664997194304,
                    "measurement_mrid": "_78de6237-4351-4cab-ab0c-ee08d0c5092c"
                },
                {
                    "angle": 86.9169925192942,
                    "magnitude": 120.844969170618,
                    "measurement_mrid": "_3b1bb2c1-d2ba-4c32-96bd-22c2701cb15b"
                },
                {
                    "angle": 86.9169925192942,
                    "magnitude": 120.844969170618,
                    "measurement_mrid": "_78299589-c67f-4893-aa22-203441b4a60f"
                },
                {
                    "angle": -155.706411315392,
                    "magnitude": 7749.31742045724,
                    "measurement_mrid": "_6329fc3d-4183-406b-85a7-9b401be10a01"
                },
                {
                    "angle": -32.8756406193266,
                    "magnitude": 7318.92666216312,
                    "measurement_mrid": "_02847ec1-f46c-4455-8185-8cfc35fa8b2f"
                },
                {
                    "angle": -155.706931549449,
                    "magnitude": 7748.98520630807,
                    "measurement_mrid": "_ba4150a2-fca5-4ff0-afb8-3de95dc4adc7"
                },
                {
                    "angle": -35.0314317843309,
                    "magnitude": 7976.85283217601,
                    "measurement_mrid": "_35ae0314-1a24-4e15-b57d-92771f30c927"
                },
                {
                    "angle": -155.681183473457,
                    "magnitude": 7762.75009776862,
                    "measurement_mrid": "_514cacd9-2c73-4a2f-8a56-7946cb7694a1"
                },
                {
                    "angle": 86.7223148950672,
                    "magnitude": 7397.62791969298,
                    "measurement_mrid": "_ca87a3c7-fb17-4696-a1f4-d3ee870bd380"
                },
                {
                    "angle": -156.811161314811,
                    "magnitude": 130.969672754449,
                    "measurement_mrid": "_1487e9ce-01da-4f3d-a794-b699e8f7ea2a"
                },
                {
                    "angle": -156.811161314811,
                    "magnitude": 130.969672754449,
                    "measurement_mrid": "_f8c2babc-d909-4961-a474-476ab16d0060"
                },
                {
                    "angle": -155.704980922064,
                    "magnitude": 7750.07897656656,
                    "measurement_mrid": "_bd067bf0-73bb-46d0-ab63-89c69dd77ef1"
                },
                {
                    "angle": -156.299114884401,
                    "magnitude": 7942.00102256642,
                    "measurement_mrid": "_079562bb-13b7-4d02-8ab9-341cfd3d5652"
                },
                {
                    "angle": -36.1030721169385,
                    "magnitude": 136.742707200654,
                    "measurement_mrid": "_50d2e444-5680-461d-97e4-70cef380e918"
                },
                {
                    "angle": -36.1030721169385,
                    "magnitude": 136.742707200654,
                    "measurement_mrid": "_859f92b1-b681-42f1-a7f9-bfd920ee6c9c"
                },
                {
                    "angle": -33.3604656281685,
                    "magnitude": 7272.16965168586,
                    "measurement_mrid": "_3fe90bd0-b9d3-48ac-9ac8-97c57c7891e0"
                },
                {
                    "angle": 87.5427143320977,
                    "magnitude": 7311.64422636505,
                    "measurement_mrid": "_492d0df8-de1b-4574-a6a9-f439feb4fd77"
                },
                {
                    "angle": -153.549042606613,
                    "magnitude": 7307.50281800608,
                    "measurement_mrid": "_628cc659-ffe2-4106-86e0-056e58b71f98"
                },
                {
                    "angle": -155.707599582454,
                    "magnitude": 7748.63380421994,
                    "measurement_mrid": "_b4b12a2a-9c7e-4df5-aefe-5922f75b0588"
                },
                {
                    "angle": -35.249079075714,
                    "magnitude": 127.144930222008,
                    "measurement_mrid": "_5971deb7-db1a-4029-9652-43df9f669e9e"
                },
                {
                    "angle": -35.2848007470713,
                    "magnitude": 127.855598928416,
                    "measurement_mrid": "_f5a52355-94bc-4590-a64a-2c6412a499c3"
                },
                {
                    "angle": -156.166241340257,
                    "magnitude": 128.121744397964,
                    "measurement_mrid": "_35bfb3cb-efd3-4a46-8825-c1947bafa57b"
                },
                {
                    "angle": -156.166241340257,
                    "magnitude": 128.121744397964,
                    "measurement_mrid": "_52a529fb-6a45-4db1-a128-9aff01043920"
                },
                {
                    "angle": 85.1153092581152,
                    "magnitude": 122.758556795263,
                    "measurement_mrid": "_2deae955-b74e-4859-8955-d16ab286e23e"
                },
                {
                    "angle": 85.143823542757,
                    "magnitude": 122.215155200048,
                    "measurement_mrid": "_f4dfedb4-1c57-4a25-854f-ca86650be754"
                },
                {
                    "angle": 87.1870874316917,
                    "magnitude": 7235.04552466851,
                    "measurement_mrid": "_19b77ccc-eb3e-4e91-9e03-baca3cd5582d"
                },
                {
                    "angle": 87.1805389752275,
                    "magnitude": 7231.78117676771,
                    "measurement_mrid": "_c1cc7b6d-8ff2-49ee-af1a-5baf4392b9a8"
                },
                {
                    "angle": -34.6302511006072,
                    "magnitude": 8001.96269688426,
                    "measurement_mrid": "_5c998da0-0684-491b-8fe5-d024aa087483"
                },
                {
                    "angle": 85.9222217174738,
                    "magnitude": 122.042864121917,
                    "measurement_mrid": "_8de9eb5c-a013-4b61-b482-919cc4bb3be2"
                },
                {
                    "angle": 85.9222217174738,
                    "magnitude": 122.042864121917,
                    "measurement_mrid": "_e2fd64c7-bd96-4ade-9d53-b4dae04813ff"
                },
                {
                    "angle": 86.2785363246748,
                    "magnitude": 7339.62159822517,
                    "measurement_mrid": "_cda62481-cbc6-44a7-802b-ae531ef0f999"
                },
                {
                    "angle": 85.1878258473161,
                    "magnitude": 122.686257067137,
                    "measurement_mrid": "_815a5995-94ce-4eac-ad0e-4e00e7ea496a"
                },
                {
                    "angle": 85.1878258473161,
                    "magnitude": 122.686257067137,
                    "measurement_mrid": "_8e022a95-bbc5-4634-b1f0-a79fcf82e1c1"
                },
                {
                    "angle": 86.2648527212155,
                    "magnitude": 7413.32959987484,
                    "measurement_mrid": "_e20e6163-a50e-42c4-b30a-f949b27e8bee"
                },
                {
                    "angle": -154.602521682277,
                    "magnitude": 128.433755923952,
                    "measurement_mrid": "_1c408443-3802-42d5-b70f-85f920e271bd"
                },
                {
                    "angle": -154.602521682277,
                    "magnitude": 128.433755923952,
                    "measurement_mrid": "_7bc77142-889d-4bb7-8345-46fea6859b7a"
                },
                {
                    "angle": 86.2773814243295,
                    "magnitude": 7343.83156991211,
                    "measurement_mrid": "_2ac93d0c-4bbe-44e3-b2c6-cfe3583a25de"
                },
                {
                    "angle": -156.256047160733,
                    "magnitude": 7950.36127396821,
                    "measurement_mrid": "_60bfbb90-92a3-47a3-9724-f6be27f598ac"
                },
                {
                    "angle": -35.6053765923596,
                    "magnitude": 8317.96189424385,
                    "measurement_mrid": "_7b9c94c1-6850-4251-bd8f-3c5bd32db6ca"
                },
                {
                    "angle": 85.7532996238218,
                    "magnitude": 122.400504545911,
                    "measurement_mrid": "_2cf7fb4c-0d22-438f-a2de-6c5d63c9ebd2"
                },
                {
                    "angle": 85.7532996238218,
                    "magnitude": 122.400504545911,
                    "measurement_mrid": "_40e76ea7-3a8f-49df-92fe-a02127e8b72c"
                },
                {
                    "angle": -156.704063069063,
                    "magnitude": 131.471149575888,
                    "measurement_mrid": "_3549ebb8-e307-4608-ba78-1d8d96cce476"
                },
                {
                    "angle": -156.704063069063,
                    "magnitude": 131.471149575888,
                    "measurement_mrid": "_fe8d4fa6-081c-4294-ac5e-bcb7f8dc8ff5"
                },
                {
                    "angle": -155.11928142691,
                    "magnitude": 7701.7085693038,
                    "measurement_mrid": "_0141f6e7-8e96-4b54-8ab7-8f46a685c89c"
                },
                {
                    "angle": -36.2606651443586,
                    "magnitude": 136.340891888875,
                    "measurement_mrid": "_0080d28e-9ebf-464d-8585-170b5734dd6c"
                },
                {
                    "angle": -36.2606651443586,
                    "magnitude": 136.340891888875,
                    "measurement_mrid": "_2a405f53-12fd-4262-b9ff-629d27da65c6"
                },
                {
                    "angle": -154.143618675456,
                    "magnitude": 7768.32576522532,
                    "measurement_mrid": "_8c4c3c10-39a4-4786-bc46-de369503f690"
                },
                {
                    "angle": 87.3831984490284,
                    "magnitude": 7313.48489094552,
                    "measurement_mrid": "_5384cbbe-6e51-4f00-9b98-03ba4f02fdda"
                },
                {
                    "angle": -154.059235590774,
                    "magnitude": 7288.37730229096,
                    "measurement_mrid": "_a56d7c9e-545a-4e1c-94ad-79abf5f19ea7"
                },
                {
                    "angle": -33.7797385715407,
                    "magnitude": 7235.46507749408,
                    "measurement_mrid": "_a946685f-edce-47cd-abe0-d2a2a8efb286"
                },
                {
                    "angle": -156.498812756183,
                    "magnitude": 7924.03536442556,
                    "measurement_mrid": "_8c3a6104-1467-42dc-a00d-88d629e324fb"
                },
                {
                    "angle": -33.7796901331625,
                    "magnitude": 7235.34732101393,
                    "measurement_mrid": "_2708f342-7e6a-4daf-9f4d-dfd2d94e1c11"
                },
                {
                    "angle": -154.059364226842,
                    "magnitude": 7288.19541585042,
                    "measurement_mrid": "_642790d2-2b66-4f18-9813-76c753e09fbc"
                },
                {
                    "angle": 87.3830948582935,
                    "magnitude": 7313.36291845557,
                    "measurement_mrid": "_b325c98a-2a1d-49ab-a08b-2601490c0b97"
                },
                {
                    "angle": -156.453219453304,
                    "magnitude": 7952.24989619403,
                    "measurement_mrid": "_00d8cea1-eff0-4858-987c-f5084cf64432"
                },
                {
                    "angle": -33.7894636474413,
                    "magnitude": 7235.25548589158,
                    "measurement_mrid": "_3e469613-5f71-49c5-a01c-ab867636d8d0"
                },
                {
                    "angle": 86.4192779749874,
                    "magnitude": 7381.90042565576,
                    "measurement_mrid": "_3295d3bf-59fd-4b4d-a3ad-44ca68465c58"
                },
                {
                    "angle": 87.1809421509091,
                    "magnitude": 7231.97762253858,
                    "measurement_mrid": "_db18e0a8-65e7-483c-b645-abd5c6993626"
                },
                {
                    "angle": -156.856572489029,
                    "magnitude": 130.406048405781,
                    "measurement_mrid": "_3ff6d97a-5b5b-4c34-8a62-d1df97e9c1d7"
                },
                {
                    "angle": -156.856572489029,
                    "magnitude": 130.406048405781,
                    "measurement_mrid": "_76c2e59e-b7d7-4d67-9b12-1757a7c16477"
                },
                {
                    "angle": 87.250023263007,
                    "magnitude": 7266.02650978857,
                    "measurement_mrid": "_b7829a80-b926-48a7-a325-ad7ac818b9d3"
                },
                {
                    "angle": -155.211017712854,
                    "magnitude": 7663.66035656169,
                    "measurement_mrid": "_7a1e4db3-12b7-483c-b672-afd9967bc537"
                },
                {
                    "angle": 85.6476260712843,
                    "magnitude": 7417.51219601606,
                    "measurement_mrid": "_be1ff982-261c-444e-ba06-ea4487401de0"
                },
                {
                    "angle": -34.8442188810597,
                    "magnitude": 7715.44806413021,
                    "measurement_mrid": "_cc2f9da4-2a66-4aeb-b35e-7ac911698391"
                },
                {
                    "angle": -153.470526962371,
                    "magnitude": 121.168253363371,
                    "measurement_mrid": "_ae433522-93b7-484f-a978-7396d8ecbee8"
                },
                {
                    "angle": -153.442887846936,
                    "magnitude": 120.648362350523,
                    "measurement_mrid": "_f8d75fc5-34bc-4862-975c-92942e7049b8"
                },
                {
                    "angle": 87.7762091650956,
                    "magnitude": 120.36846963091,
                    "measurement_mrid": "_40e03d89-c80f-4eb5-a215-9fcbe36b53e8"
                },
                {
                    "angle": 87.7588127315076,
                    "magnitude": 120.6943996096,
                    "measurement_mrid": "_5303942e-ae11-4898-8992-57a88800b8ea"
                },
                {
                    "angle": 85.9549345283912,
                    "magnitude": 121.024307632485,
                    "measurement_mrid": "_0668a05f-70b1-4a20-baac-bb8177d21292"
                },
                {
                    "angle": 85.9722825997097,
                    "magnitude": 120.698377282496,
                    "measurement_mrid": "_95df5ff3-7d08-44ac-8169-c823241e28d0"
                },
                {
                    "angle": 85.6472527034743,
                    "magnitude": 7417.32284928225,
                    "measurement_mrid": "_c17772a4-0e74-48e5-8786-674da536a43d"
                },
                {
                    "angle": -35.9307454380835,
                    "magnitude": 137.883185043993,
                    "measurement_mrid": "_05c9494c-324b-4ab3-8e9d-48be97eed74b"
                },
                {
                    "angle": -35.9175007831741,
                    "magnitude": 137.59892248075,
                    "measurement_mrid": "_7ae60cf1-7421-4dff-a23d-1e9f302d467d"
                },
                {
                    "angle": -34.0763344616941,
                    "magnitude": 120.663923313988,
                    "measurement_mrid": "_3b171ac4-800f-4d84-9748-092316e65429"
                },
                {
                    "angle": -34.0763344616941,
                    "magnitude": 120.663923313988,
                    "measurement_mrid": "_a90659bd-d222-422e-8c40-4c6b57cee221"
                },
                {
                    "angle": -155.707478279492,
                    "magnitude": 7748.68621030231,
                    "measurement_mrid": "_ee7e8beb-12ef-43a0-93ba-1d4a2802241a"
                },
                {
                    "angle": 87.4639495626191,
                    "magnitude": 7313.12097848669,
                    "measurement_mrid": "_c770aefb-e429-4990-9365-dc2ed3ddeeb1"
                },
                {
                    "angle": -36.2153971191835,
                    "magnitude": 136.944613402807,
                    "measurement_mrid": "_afb9ba24-6d1a-4e4b-b356-223b8751f00c"
                },
                {
                    "angle": -36.2020646511839,
                    "magnitude": 136.660349808275,
                    "measurement_mrid": "_f477c3c9-c495-4ac9-be96-7f0ad2e2d3d9"
                },
                {
                    "angle": -155.297598677977,
                    "magnitude": 7619.35534839787,
                    "measurement_mrid": "_ecbf4d5e-6ae1-4797-8d7f-61a7040eeefe"
                },
                {
                    "angle": 86.4732974866615,
                    "magnitude": 7317.30141333012,
                    "measurement_mrid": "_3ca88d69-0ded-4850-a4b1-9b47a5e83a17"
                },
                {
                    "angle": -35.7111706963909,
                    "magnitude": 8261.01537473813,
                    "measurement_mrid": "_53564b4f-6455-43e6-894e-db5d9304f296"
                },
                {
                    "angle": -156.118125950348,
                    "magnitude": 7980.93148156015,
                    "measurement_mrid": "_bf3cc1c7-cd5e-4f8d-bf42-41f922a9f68e"
                },
                {
                    "angle": -35.7051427622511,
                    "magnitude": 8260.7855346767,
                    "measurement_mrid": "_09909ed0-9e19-4d90-88fd-e4890e6e81f9"
                },
                {
                    "angle": -34.8609584353301,
                    "magnitude": 7735.05270354779,
                    "measurement_mrid": "_50990581-1df4-41ba-9f49-98e4a529f6b9"
                },
                {
                    "angle": -35.7091379958835,
                    "magnitude": 8260.95129928873,
                    "measurement_mrid": "_5379d0fb-f381-4488-bcb5-21ef6c8d6ded"
                },
                {
                    "angle": -35.7025546904254,
                    "magnitude": 8262.21469633928,
                    "measurement_mrid": "_8fa4eb70-f8d8-44ee-8fec-980ab2185cea"
                },
                {
                    "angle": -34.8430748445383,
                    "magnitude": 7714.02877220538,
                    "measurement_mrid": "_41b5e161-6296-4809-aafa-59c8f2313618"
                },
                {
                    "angle": -155.215154910657,
                    "magnitude": 7661.77826756854,
                    "measurement_mrid": "_64dba087-166f-45f8-ab35-c83d63a98014"
                },
                {
                    "angle": 85.6492820994706,
                    "magnitude": 7417.89230236982,
                    "measurement_mrid": "_72968f4f-2c4e-4019-8637-ddb8ded4d73d"
                },
                {
                    "angle": 86.1046461438044,
                    "magnitude": 7324.08483707523,
                    "measurement_mrid": "_522f533c-3210-4ab9-99d1-0d674656da96"
                },
                {
                    "angle": -151.721735498786,
                    "magnitude": 7321.82490789899,
                    "measurement_mrid": "_c64e8d73-4eb2-4022-9866-d001a2a90a32"
                },
                {
                    "angle": 88.5927959649451,
                    "magnitude": 7291.5524338795,
                    "measurement_mrid": "_c8575867-de52-4267-b70f-45c6a69885b3"
                },
                {
                    "angle": -31.6910445868955,
                    "magnitude": 7320.16365392048,
                    "measurement_mrid": "_eea9cfe5-b619-4057-a623-6e027a2ad334"
                },
                {
                    "angle": -34.3642516948006,
                    "magnitude": 120.377332145343,
                    "measurement_mrid": "_c4766cf2-f406-4743-8d5c-b4179c3ecbef"
                },
                {
                    "angle": -34.3642516948006,
                    "magnitude": 120.377332145343,
                    "measurement_mrid": "_f90dbded-2a66-4a7e-9776-9b8b10af0dd4"
                },
                {
                    "angle": -151.72065849002,
                    "magnitude": 7321.93938306187,
                    "measurement_mrid": "_1e053e03-43af-4e1b-90b1-ac87102ce442"
                },
                {
                    "angle": 88.5932080277478,
                    "magnitude": 7291.51231116518,
                    "measurement_mrid": "_6630805c-6c11-4799-8801-d2023310f43c"
                },
                {
                    "angle": -31.691305878909,
                    "magnitude": 7320.1939955355,
                    "measurement_mrid": "_e18a8905-c55f-4005-be4f-32920c07aaa7"
                },
                {
                    "angle": -151.721660838958,
                    "magnitude": 7321.83284628085,
                    "measurement_mrid": "_a5494373-1f79-4bb4-84fa-b1ff55e73620"
                },
                {
                    "angle": 88.5928245269689,
                    "magnitude": 7291.54965477813,
                    "measurement_mrid": "_aa60311d-aca3-4c55-8909-1e8b166528f1"
                },
                {
                    "angle": -31.6910627088416,
                    "magnitude": 7320.16575912617,
                    "measurement_mrid": "_aafb7bdf-2207-498d-b4f2-1e43d44343b6"
                },
                {
                    "angle": -151.674055675168,
                    "magnitude": 7322.60934829694,
                    "measurement_mrid": "_1c5a0e58-3576-4016-877e-105931666a21"
                },
                {
                    "angle": 88.6259104375587,
                    "magnitude": 7291.09319445805,
                    "measurement_mrid": "_8fab5e7f-3e47-4806-9887-59ce8cc18132"
                },
                {
                    "angle": -31.6508841589066,
                    "magnitude": 7320.85497626818,
                    "measurement_mrid": "_d1da73e7-d200-4885-acdf-eb4075b3339e"
                },
                {
                    "angle": -34.2305849166999,
                    "magnitude": 7220.08736712792,
                    "measurement_mrid": "_18de5ef0-117f-4335-b947-8273888f6033"
                },
                {
                    "angle": -34.3887951601121,
                    "magnitude": 119.421495008122,
                    "measurement_mrid": "_1a9581d7-73b2-4364-8314-ba9219d63e5a"
                },
                {
                    "angle": -34.4142174413129,
                    "magnitude": 119.895442968962,
                    "measurement_mrid": "_cea3c7eb-504e-4ce8-931c-eaf1870c143a"
                },
                {
                    "angle": -36.1017084873035,
                    "magnitude": 136.741024443227,
                    "measurement_mrid": "_1b2d3ab6-f366-4fe4-89cb-4fbc8f72a8be"
                },
                {
                    "angle": -36.1017084873035,
                    "magnitude": 136.741024443227,
                    "measurement_mrid": "_76735a93-ba1e-4ee5-9b0a-66ee809c1faa"
                },
                {
                    "angle": -35.7268077536096,
                    "magnitude": 8248.81388250087,
                    "measurement_mrid": "_19e41663-3bc1-429a-8f72-bbaf0491234a"
                },
                {
                    "angle": -156.939335566969,
                    "magnitude": 130.402829458667,
                    "measurement_mrid": "_55f34146-85d7-4e8c-b3fb-413fc4cf684e"
                },
                {
                    "angle": -156.913646284468,
                    "magnitude": 129.882941376708,
                    "measurement_mrid": "_5de5512f-6e3b-494c-ae95-a4a7526ed01c"
                },
                {
                    "angle": -155.138307278191,
                    "magnitude": 7694.38399620624,
                    "measurement_mrid": "_f2a51d57-fa1b-4851-ad4d-48b7c2719fe1"
                },
                {
                    "angle": 86.4421650314937,
                    "magnitude": 7361.3420463087,
                    "measurement_mrid": "_91adc0fc-8b77-4ff7-b0ef-f614abe8a00e"
                },
                {
                    "angle": -35.601064625117,
                    "magnitude": 8323.7501914568,
                    "measurement_mrid": "_de57fcc1-97d5-4705-83b7-d5944e094bf1"
                },
                {
                    "angle": -156.145861000725,
                    "magnitude": 7986.05231541392,
                    "measurement_mrid": "_ef1e41df-fcaf-45fc-b67f-570a78dbf75f"
                },
                {
                    "angle": -155.139202200252,
                    "magnitude": 7694.10965024913,
                    "measurement_mrid": "_78ea9d75-583e-47a0-b2a6-22eb80a9f857"
                },
                {
                    "angle": 87.7918257304918,
                    "magnitude": 7306.57303235378,
                    "measurement_mrid": "_3b67d570-7bac-4936-939e-e5c5eeacf144"
                },
                {
                    "angle": -32.806426608104,
                    "magnitude": 7306.26710705647,
                    "measurement_mrid": "_5e5dcac6-a5a4-426f-a5ed-af2a3edb0db3"
                },
                {
                    "angle": -152.90728125417,
                    "magnitude": 7319.78077469105,
                    "measurement_mrid": "_a43b31e9-5552-41db-95da-67b83f1d8252"
                },
                {
                    "angle": -35.5050692414352,
                    "magnitude": 8312.29572617745,
                    "measurement_mrid": "_9022cdd3-54f8-42e8-9171-3d7c5d682a96"
                },
                {
                    "angle": 86.2407970340585,
                    "magnitude": 7400.90880904634,
                    "measurement_mrid": "_79f65ab8-66d7-47a6-bfe0-272fafe4bc38"
                },
                {
                    "angle": -36.0297036044935,
                    "magnitude": 137.436503526984,
                    "measurement_mrid": "_5398cbec-c9b6-4d34-ada1-d5fdf2c0d690"
                },
                {
                    "angle": -36.0297036044935,
                    "magnitude": 137.436503526984,
                    "measurement_mrid": "_75d55992-3167-4f1e-b6e1-d78a21a41df3"
                },
                {
                    "angle": -156.394976151599,
                    "magnitude": 7892.1978368348,
                    "measurement_mrid": "_b5eb4b7c-f022-4b40-abe9-4e983d5cc224"
                },
                {
                    "angle": -156.427991022749,
                    "magnitude": 7874.07370667997,
                    "measurement_mrid": "_62b4701c-1b38-40fd-a166-8868a23307aa"
                },
                {
                    "angle": -153.045166888319,
                    "magnitude": 7318.53957292583,
                    "measurement_mrid": "_60326e70-ade2-43a7-9595-cb91b21d6c15"
                },
                {
                    "angle": -155.771046324749,
                    "magnitude": 125.905952462841,
                    "measurement_mrid": "_b6b0ad3b-a1c1-49b9-8bb9-d44af5f1a0ce"
                },
                {
                    "angle": -155.771046324749,
                    "magnitude": 125.905952462841,
                    "measurement_mrid": "_e5efa4c0-7a35-4f84-a251-8668502ac22f"
                },
                {
                    "angle": -36.141606269944,
                    "magnitude": 137.284924524252,
                    "measurement_mrid": "_3798054e-aa79-4c9d-a6b6-8ecff9878491"
                },
                {
                    "angle": -36.1548804306266,
                    "magnitude": 137.569188066841,
                    "measurement_mrid": "_48fbfff9-4443-4dc2-b238-e1fa2f908575"
                },
                {
                    "angle": -35.8079468684136,
                    "magnitude": 8262.62783125092,
                    "measurement_mrid": "_e58767dc-7b09-4894-9336-72748c19b710"
                },
                {
                    "angle": -155.680604939487,
                    "magnitude": 127.022450900516,
                    "measurement_mrid": "_391fea8e-a044-4f05-8535-4179f034f9b2"
                },
                {
                    "angle": -155.654265114619,
                    "magnitude": 126.502554180977,
                    "measurement_mrid": "_7a816a8d-e437-4e40-b5a1-f9dbd80954bd"
                },
                {
                    "angle": 85.1350602044829,
                    "magnitude": 122.558304288214,
                    "measurement_mrid": "_87c4e072-7727-474f-85ea-01a1b7b9c946"
                },
                {
                    "angle": 85.1350602044829,
                    "magnitude": 122.558304288214,
                    "measurement_mrid": "_e271f6cc-e6a0-4ba0-8756-488f6d5e00fd"
                },
                {
                    "angle": -35.032442048734,
                    "magnitude": 7976.74431907319,
                    "measurement_mrid": "_e61a0443-2b6c-4f8d-bfde-5a66e6fc4943"
                },
                {
                    "angle": -34.8652474440458,
                    "magnitude": 7732.69820525647,
                    "measurement_mrid": "_f39aa430-5ed2-4ae5-91ed-67f800bbf152"
                },
                {
                    "angle": -155.185485068241,
                    "magnitude": 128.909524198527,
                    "measurement_mrid": "_05dee23e-13e5-47d0-8654-09c7322266f6"
                },
                {
                    "angle": -155.159498349867,
                    "magnitude": 128.389636312887,
                    "measurement_mrid": "_6a683628-3b03-40c0-b42a-fab205b84a75"
                },
                {
                    "angle": -152.209940293195,
                    "magnitude": 120.981082081298,
                    "measurement_mrid": "_819a0027-061d-4740-a5a7-31c86ba8ad25"
                },
                {
                    "angle": -152.209940293195,
                    "magnitude": 120.981082081298,
                    "measurement_mrid": "_83350271-9149-4c17-9b55-d68d0e7f933f"
                },
                {
                    "angle": -156.9574927092,
                    "magnitude": 130.962580155329,
                    "measurement_mrid": "_632aa19d-5b7e-4770-b675-f2ac683c5efb"
                },
                {
                    "angle": -156.9574927092,
                    "magnitude": 130.962580155329,
                    "measurement_mrid": "_f77c94f5-3ecc-4fda-a7e4-2091977b6989"
                },
                {
                    "angle": -33.6310459107256,
                    "magnitude": 7296.50213584563,
                    "measurement_mrid": "_b26d59fd-db94-4982-b46a-7c41ba147dfd"
                },
                {
                    "angle": -156.257474411423,
                    "magnitude": 7964.89737671194,
                    "measurement_mrid": "_46bbf3e6-3b16-4564-ba05-92d7b0959673"
                },
                {
                    "angle": 86.4267863468087,
                    "magnitude": 7387.60991166453,
                    "measurement_mrid": "_6f8ea0ac-8bd3-4277-921a-adc05d507959"
                },
                {
                    "angle": -35.575776913755,
                    "magnitude": 8332.94851816874,
                    "measurement_mrid": "_da400f90-677f-4548-aa07-07244f809e42"
                },
                {
                    "angle": -155.60408022119,
                    "magnitude": 127.190201746632,
                    "measurement_mrid": "_00197b00-91de-46ef-b17f-5e17bc3bfe1d"
                },
                {
                    "angle": -155.60408022119,
                    "magnitude": 127.190201746632,
                    "measurement_mrid": "_e1043ac0-800e-46e5-ae39-4f01085de608"
                },
                {
                    "angle": -33.6283537468529,
                    "magnitude": 7297.70426350695,
                    "measurement_mrid": "_f159365a-6501-441d-889f-b7e2188abb1b"
                },
                {
                    "angle": 86.796324732711,
                    "magnitude": 7264.96794382267,
                    "measurement_mrid": "_1bac9ff5-2f6b-4a70-8247-21d4d590bf7d"
                },
                {
                    "angle": -153.732349405825,
                    "magnitude": 7272.89833726892,
                    "measurement_mrid": "_2e2e83cc-6a20-4447-b1ec-5db9ef5b822a"
                },
                {
                    "angle": -33.62825654781,
                    "magnitude": 7297.63273851303,
                    "measurement_mrid": "_fe29ee7c-a5a6-4e76-8f5c-3c3368fa8364"
                },
                {
                    "angle": -32.6965912559218,
                    "magnitude": 120.745541807648,
                    "measurement_mrid": "_05a2106b-7604-4043-93a9-75ba5295bdde"
                },
                {
                    "angle": -32.7217568269659,
                    "magnitude": 121.219485306064,
                    "measurement_mrid": "_c5480186-7c82-4e2c-b980-715546a2d53f"
                },
                {
                    "angle": -35.7315490195082,
                    "magnitude": 8246.20605391946,
                    "measurement_mrid": "_41d72c5a-15b2-41d6-8b63-f4f0d07d730b"
                },
                {
                    "angle": 86.7966828634157,
                    "magnitude": 7265.12795220313,
                    "measurement_mrid": "_63a4bc58-42df-45a8-9160-1acf29d197a3"
                },
                {
                    "angle": -153.732004938329,
                    "magnitude": 7273.10384800272,
                    "measurement_mrid": "_8e98307a-cccf-4f2c-aa55-99c6fa7b7484"
                },
                {
                    "angle": -33.6280988030812,
                    "magnitude": 7297.77757282967,
                    "measurement_mrid": "_e9cf5a18-76ad-4027-8358-92bf90b376da"
                },
                {
                    "angle": 86.6790773745994,
                    "magnitude": 119.321710431919,
                    "measurement_mrid": "_2268e1e1-dd06-4366-841c-d810e9fd5e4e"
                },
                {
                    "angle": 86.6615280897857,
                    "magnitude": 119.647640280359,
                    "measurement_mrid": "_a6396691-627b-4209-836c-14e215d82e2a"
                },
                {
                    "angle": -156.192165134051,
                    "magnitude": 128.64139151429,
                    "measurement_mrid": "_33698c49-2adc-4738-b9b6-5d25c5f3654d"
                },
                {
                    "angle": -156.140106407612,
                    "magnitude": 127.602123723836,
                    "measurement_mrid": "_d4e4912b-6505-41b2-a77d-52adbafb2c05"
                },
                {
                    "angle": -156.179678310706,
                    "magnitude": 128.228541433987,
                    "measurement_mrid": "_261a6c4a-0ff2-49e1-a80d-7cb142553daf"
                },
                {
                    "angle": -156.163996475539,
                    "magnitude": 127.916504148055,
                    "measurement_mrid": "_bc2db712-4361-4e76-89d5-f320b5a2d755"
                },
                {
                    "angle": -36.146236237396,
                    "magnitude": 136.643183776957,
                    "measurement_mrid": "_80c285bf-5c27-479e-8fbe-1e9d7ace4d8a"
                },
                {
                    "angle": -36.123959310804,
                    "magnitude": 136.169228936982,
                    "measurement_mrid": "_a0577e99-d7b0-46e6-9f34-24689b1ba326"
                },
                {
                    "angle": -155.748195162176,
                    "magnitude": 7727.22421201021,
                    "measurement_mrid": "_b7e741da-c5f3-46cd-bc10-59b1c2cfd7a7"
                },
                {
                    "angle": -156.899865168761,
                    "magnitude": 131.500447383046,
                    "measurement_mrid": "_fdad2908-8249-4b9b-8b83-a0b52161ba5b"
                },
                {
                    "angle": -156.899865168761,
                    "magnitude": 131.500447383046,
                    "measurement_mrid": "_fdae5a5f-9b58-4fbf-b8a9-c8e514060792"
                },
                {
                    "angle": -36.1491908616565,
                    "magnitude": 137.419742397204,
                    "measurement_mrid": "_93f21fc9-b42b-49c0-ad38-9a06f343e733"
                },
                {
                    "angle": -36.1491908616565,
                    "magnitude": 137.419742397204,
                    "measurement_mrid": "_e11d6806-5ab4-4059-b377-3f8bc288f552"
                },
                {
                    "angle": 86.2834261984774,
                    "magnitude": 120.001011996912,
                    "measurement_mrid": "_b2b87154-29c7-4306-bdeb-dbcf42e0d846"
                },
                {
                    "angle": 86.2834261984774,
                    "magnitude": 120.001011996912,
                    "measurement_mrid": "_c6e9b976-3fa6-4370-90f6-7cfe9df5c459"
                },
                {
                    "angle": -35.9741795311475,
                    "magnitude": 137.358705146917,
                    "measurement_mrid": "_18ded4c8-796e-40d8-8461-c5e6cde3045a"
                },
                {
                    "angle": -35.9962683666643,
                    "magnitude": 137.832658024701,
                    "measurement_mrid": "_7d3736af-22c1-4d4e-8d16-72a6f1d07bef"
                },
                {
                    "angle": -35.0324132998657,
                    "magnitude": 7976.75360118163,
                    "measurement_mrid": "_3f5665c2-ce0b-4473-828f-2cedea0bd7a2"
                },
                {
                    "angle": 86.7228435595982,
                    "magnitude": 7397.59894799655,
                    "measurement_mrid": "_cfdc1452-0728-4ba2-9a79-c8ac649a57a6"
                },
                {
                    "angle": -155.681209720164,
                    "magnitude": 7762.82981476674,
                    "measurement_mrid": "_fa2cba54-5dc3-481e-b6ff-150b7b97415e"
                },
                {
                    "angle": -156.133384022641,
                    "magnitude": 7982.02700442259,
                    "measurement_mrid": "_0397d4ee-c653-44a1-917a-69c29a692372"
                },
                {
                    "angle": -35.6764627380883,
                    "magnitude": 8277.89178187701,
                    "measurement_mrid": "_46c33863-0907-45f6-a72c-2bd882220cbe"
                },
                {
                    "angle": 86.4722783997533,
                    "magnitude": 7333.20748612223,
                    "measurement_mrid": "_9267cf4b-2f6c-454d-af94-11a3a64a637c"
                },
                {
                    "angle": -35.7297060282457,
                    "magnitude": 8247.22589412872,
                    "measurement_mrid": "_b46780a0-3ee5-455d-8623-a656455108db"
                },
                {
                    "angle": -35.5056507017034,
                    "magnitude": 8315.28639729362,
                    "measurement_mrid": "_5fc0d157-d430-4a97-8b13-5ca4f6385d3a"
                },
                {
                    "angle": -156.369077351453,
                    "magnitude": 7905.56109324658,
                    "measurement_mrid": "_7b1a2992-c12d-458d-bdf9-9536d6a60f47"
                },
                {
                    "angle": 86.4324382274585,
                    "magnitude": 7400.20792589339,
                    "measurement_mrid": "_a258cb88-90d2-4668-96d9-134530f89c4f"
                },
                {
                    "angle": -156.167963254849,
                    "magnitude": 128.101700475848,
                    "measurement_mrid": "_429ceab2-be81-4f71-a1d5-7e88eb976391"
                },
                {
                    "angle": -156.167963254849,
                    "magnitude": 128.101700475848,
                    "measurement_mrid": "_eb014a45-e8fc-4a57-921d-f7b2f43633d6"
                },
                {
                    "angle": -35.6821719166484,
                    "magnitude": 8327.44123111895,
                    "measurement_mrid": "_8b70df26-ca8c-4174-8028-2d66d7564b2b"
                },
                {
                    "angle": 86.4230952508446,
                    "magnitude": 7380.13137183807,
                    "measurement_mrid": "_9d3b998a-70ea-4338-baf1-24214379a89c"
                },
                {
                    "angle": -156.261039947029,
                    "magnitude": 7990.75518460995,
                    "measurement_mrid": "_fc1793e7-7385-407d-8972-f32da2ebd2f0"
                },
                {
                    "angle": -36.1273893660099,
                    "magnitude": 137.415866133499,
                    "measurement_mrid": "_2fe139b9-0a75-4aef-8b00-76e920407263"
                },
                {
                    "angle": -36.1406509099926,
                    "magnitude": 137.700128469848,
                    "measurement_mrid": "_b6c6ced9-33b0-4106-8c2a-ae1edecc0630"
                },
                {
                    "angle": 85.7289608673772,
                    "magnitude": 122.428445414941,
                    "measurement_mrid": "_9dbd976e-5b1b-44cf-a35d-60ec88af018e"
                },
                {
                    "angle": 85.7461096064722,
                    "magnitude": 122.10251501323,
                    "measurement_mrid": "_b9f6747e-9cb1-44a0-867e-5dcd0a57c03b"
                },
                {
                    "angle": -32.5445030665606,
                    "magnitude": 7314.67059858852,
                    "measurement_mrid": "_8e7d62b5-24f4-446c-9352-b1ddfe8a6945"
                },
                {
                    "angle": -36.0966502924036,
                    "magnitude": 137.904369963827,
                    "measurement_mrid": "_2df27dad-e7d1-42a9-aa1d-36146f8b5964"
                },
                {
                    "angle": -36.0834074283479,
                    "magnitude": 137.620107616232,
                    "measurement_mrid": "_cc286029-af2e-4ac1-b0a5-5135dc2dfbe8"
                },
                {
                    "angle": -34.8247494669125,
                    "magnitude": 7763.37679097179,
                    "measurement_mrid": "_69db8669-a86d-4a39-84af-d5d95731b8bb"
                },
                {
                    "angle": -35.2138426051942,
                    "magnitude": 132.265591337741,
                    "measurement_mrid": "_d88750b1-df7b-415e-9dff-9d356d05314a"
                },
                {
                    "angle": -35.2138426051942,
                    "magnitude": 132.265591337741,
                    "measurement_mrid": "_f5c645a9-e51f-4f0b-b0ae-ac991dca8e5c"
                },
                {
                    "angle": 85.7292719160142,
                    "magnitude": 122.430510652241,
                    "measurement_mrid": "_40f16fcb-b382-4dfc-963b-06018ef61bc5"
                },
                {
                    "angle": 85.7464207273775,
                    "magnitude": 122.104580523542,
                    "measurement_mrid": "_8aa4c2ec-a47a-47c1-b1b8-f4ed9fabeb91"
                },
                {
                    "angle": 87.2210853652927,
                    "magnitude": 120.66157035207,
                    "measurement_mrid": "_0508527c-3c83-4faf-a4b7-6abbd1d0e7ff"
                },
                {
                    "angle": 87.2210853652927,
                    "magnitude": 120.66157035207,
                    "measurement_mrid": "_ac9dae07-50e3-414d-8ea2-cf7e05250517"
                },
                {
                    "angle": -34.0736274250658,
                    "magnitude": 120.682388285952,
                    "measurement_mrid": "_091e9e03-9a74-487a-8ba4-cd76b5d53313"
                },
                {
                    "angle": -34.0736274250658,
                    "magnitude": 120.682388285952,
                    "measurement_mrid": "_e01f8d1f-f841-4a47-a39c-d8108c6f98d3"
                },
                {
                    "angle": -156.426302219564,
                    "magnitude": 7875.40819240814,
                    "measurement_mrid": "_760c7342-8501-4bcf-8d87-059f798fac1d"
                },
                {
                    "angle": -33.4442577660289,
                    "magnitude": 121.063509488985,
                    "measurement_mrid": "_6f9a6b34-dded-4f27-b23a-2700734b64b2"
                },
                {
                    "angle": -33.4693483507236,
                    "magnitude": 121.53745434156,
                    "measurement_mrid": "_e4f50b03-d353-4837-b8ad-62386ad0a038"
                },
                {
                    "angle": -35.8067787086902,
                    "magnitude": 8262.9039776597,
                    "measurement_mrid": "_fe21c8cd-5105-46eb-a17d-0630f9921acb"
                },
                {
                    "angle": -151.724518553398,
                    "magnitude": 7320.05816050106,
                    "measurement_mrid": "_5b6b9311-8bab-4876-927d-b8496202762e"
                },
                {
                    "angle": -31.6947914357242,
                    "magnitude": 7318.52733962267,
                    "measurement_mrid": "_5c4ee494-d4fb-419e-9828-3c24d52db969"
                },
                {
                    "angle": 88.5895709134842,
                    "magnitude": 7289.53350791556,
                    "measurement_mrid": "_693b3308-ed2f-4409-a000-c9daa95eae1e"
                },
                {
                    "angle": 87.1969084551341,
                    "magnitude": 7324.00923454143,
                    "measurement_mrid": "_42cb1a2f-63be-4cb7-8c99-a3ae64a562a9"
                },
                {
                    "angle": -34.2511350896006,
                    "magnitude": 7220.7393872999,
                    "measurement_mrid": "_49e1c2a7-a155-4fc4-bade-8cfc93db4724"
                },
                {
                    "angle": 87.1969084551341,
                    "magnitude": 7324.00923454143,
                    "measurement_mrid": "_a6ab7201-1582-46af-a804-6d2c09a13ae5"
                },
                {
                    "angle": -154.552108124989,
                    "magnitude": 7296.94090974836,
                    "measurement_mrid": "_b9cdc9e9-f896-44de-a1d0-be98ef9edea1"
                },
                {
                    "angle": -34.2511350896006,
                    "magnitude": 7220.7393872999,
                    "measurement_mrid": "_ca63865b-e979-4ddc-bc6b-03e4dc74c068"
                },
                {
                    "angle": -154.552108124989,
                    "magnitude": 7296.94090974836,
                    "measurement_mrid": "_de304f26-67a4-4550-a7f9-3cd0c8e875af"
                },
                {
                    "angle": -34.8653126971806,
                    "magnitude": 7732.668509027,
                    "measurement_mrid": "_a2cc752f-5674-4724-911a-866f6b67d5ba"
                },
                {
                    "angle": 86.6961544330898,
                    "magnitude": 119.691780628926,
                    "measurement_mrid": "_431117e6-77fd-4215-a792-b245731f1e56"
                },
                {
                    "angle": 86.6961544330898,
                    "magnitude": 119.691780628926,
                    "measurement_mrid": "_44a23d4a-e318-439a-8056-9877bf93ce94"
                },
                {
                    "angle": -155.303202493547,
                    "magnitude": 7616.44552585904,
                    "measurement_mrid": "_b25d7cdc-dba6-4f6c-b7ad-5ab1a5b92abe"
                },
                {
                    "angle": -156.165910381499,
                    "magnitude": 128.269622591671,
                    "measurement_mrid": "_4bc0bab3-4830-4e16-b41a-71115a5f2d86"
                },
                {
                    "angle": -156.155468221065,
                    "magnitude": 128.061777544018,
                    "measurement_mrid": "_c226fee6-abb3-4ab3-bd7d-53896cdf34fb"
                },
                {
                    "angle": -35.5789939186124,
                    "magnitude": 8334.17839145533,
                    "measurement_mrid": "_56c3c7ef-d184-467d-bf22-e3360e108b3a"
                },
                {
                    "angle": -156.423238624074,
                    "magnitude": 7876.60528227175,
                    "measurement_mrid": "_95911e86-c087-4351-938c-9ec48db3d110"
                },
                {
                    "angle": -156.428274381251,
                    "magnitude": 7873.91042260294,
                    "measurement_mrid": "_bc6b9d85-c98d-4727-95ab-ff4ae39cbf48"
                },
                {
                    "angle": -156.38635335683,
                    "magnitude": 7896.40505220717,
                    "measurement_mrid": "_2db8cbbf-b831-49c0-89e8-bd63e861c742"
                },
                {
                    "angle": -35.5715377620127,
                    "magnitude": 8357.59779786777,
                    "measurement_mrid": "_2e1b88db-08d7-4df6-a5ec-f4d2f9bcdb48"
                },
                {
                    "angle": -156.145215107635,
                    "magnitude": 8007.72153438669,
                    "measurement_mrid": "_938527cf-ee0c-40b6-9004-9549ca7c838e"
                },
                {
                    "angle": 86.4450179004076,
                    "magnitude": 7391.10820804078,
                    "measurement_mrid": "_c92a196f-e11e-4dcd-b803-5c7d86cbfc21"
                },
                {
                    "angle": -35.8163092714641,
                    "magnitude": 8264.49412365607,
                    "measurement_mrid": "_1c43e10e-1386-4e57-b2ac-9006002c4145"
                },
                {
                    "angle": -35.7220703687255,
                    "magnitude": 8251.41709964469,
                    "measurement_mrid": "_f3d90bbc-5abb-4af9-885c-7b91e40dc336"
                },
                {
                    "angle": 85.6332376867099,
                    "magnitude": 7414.56890638342,
                    "measurement_mrid": "_7ef94586-dd3c-4dde-af19-fc67c9dfe157"
                },
                {
                    "angle": -156.850438432285,
                    "magnitude": 130.693502626798,
                    "measurement_mrid": "_9dba6cd6-fa14-46b8-bd82-d8205c84bba9"
                },
                {
                    "angle": -156.850438432285,
                    "magnitude": 130.693502626798,
                    "measurement_mrid": "_e44fc60e-5a2c-455a-8a12-fbac81517514"
                },
                {
                    "angle": 85.8973734235474,
                    "magnitude": 121.402016148246,
                    "measurement_mrid": "_896eff0e-bc96-44f1-8f56-b7ded646897f"
                },
                {
                    "angle": 85.868667584266,
                    "magnitude": 121.945416880521,
                    "measurement_mrid": "_e99f558f-b711-4418-b3ee-4732939dc648"
                },
                {
                    "angle": -36.1994108749922,
                    "magnitude": 136.779058059567,
                    "measurement_mrid": "_0aea858b-e7d7-4553-81fc-19a9406eaec3"
                },
                {
                    "angle": -36.1994108749922,
                    "magnitude": 136.779058059567,
                    "measurement_mrid": "_9ac11307-51b8-43cd-8d0f-494f50e55c22"
                },
                {
                    "angle": -155.160948805278,
                    "magnitude": 7693.02778143307,
                    "measurement_mrid": "_86ef8072-f4c7-4033-8d5f-476652b5364d"
                },
                {
                    "angle": 85.6370294422084,
                    "magnitude": 7419.23821250235,
                    "measurement_mrid": "_921139a6-7034-4b1a-a6f9-f1cec2db3311"
                },
                {
                    "angle": -34.8609018849123,
                    "magnitude": 7735.08321053117,
                    "measurement_mrid": "_ec0f7e51-c09f-4390-a203-ad658f747210"
                },
                {
                    "angle": -34.8610373536874,
                    "magnitude": 7735.01027759531,
                    "measurement_mrid": "_bd182fc8-7661-45ab-b33e-ee9530bf3090"
                },
                {
                    "angle": 85.8537650507898,
                    "magnitude": 122.178202290581,
                    "measurement_mrid": "_0b39bd37-2ff0-4dcf-87ec-9b8604cef05e"
                },
                {
                    "angle": 85.9110663588835,
                    "magnitude": 121.091369160959,
                    "measurement_mrid": "_6d4a3135-f0eb-480c-887c-1031f8689430"
                },
                {
                    "angle": -34.8612643067129,
                    "magnitude": 7738.29645360379,
                    "measurement_mrid": "_a6c1e6b7-84d2-49c2-93a5-1e0223dbf011"
                },
                {
                    "angle": -155.155744883912,
                    "magnitude": 7696.59386396967,
                    "measurement_mrid": "_d7e6b2de-25dd-4dee-a802-ff6b3d4ac485"
                },
                {
                    "angle": 85.6355864034004,
                    "magnitude": 7420.25218942022,
                    "measurement_mrid": "_e997d0aa-8d3c-4825-8aa2-4b1d4b067b84"
                },
                {
                    "angle": -36.1001590039897,
                    "magnitude": 136.516339396137,
                    "measurement_mrid": "_9e50b738-a13b-4caf-8402-3222dda2af28"
                },
                {
                    "angle": -36.1135057830538,
                    "magnitude": 136.800603455613,
                    "measurement_mrid": "_ad1e104b-c40f-4c1f-aa55-c41be7fd366f"
                },
                {
                    "angle": -34.8610120096244,
                    "magnitude": 7735.02380564721,
                    "measurement_mrid": "_50a54d0a-768c-4ad9-a3fc-cd3a233020b6"
                },
                {
                    "angle": -153.533850795584,
                    "magnitude": 120.923498998525,
                    "measurement_mrid": "_07aaf3bb-45d0-4ee4-a527-8e9da8326f69"
                },
                {
                    "angle": -153.533850795584,
                    "magnitude": 120.923498998525,
                    "measurement_mrid": "_44a03991-c11e-4f96-a766-aa41651c9a6f"
                },
                {
                    "angle": -156.43626084216,
                    "magnitude": 7869.60948979175,
                    "measurement_mrid": "_830513ab-cca3-4052-9866-01bdbe684fcc"
                },
                {
                    "angle": -35.7896149636079,
                    "magnitude": 8293.33408558023,
                    "measurement_mrid": "_45d96979-4c92-4057-b423-0c51cdcb2ef5"
                },
                {
                    "angle": -35.7896085499671,
                    "magnitude": 8293.33619745815,
                    "measurement_mrid": "_918d2059-43ba-4c08-82ea-b7f68a90b793"
                },
                {
                    "angle": -156.654453860503,
                    "magnitude": 132.257691645783,
                    "measurement_mrid": "_a67be095-f7f6-4695-9ea0-1f6027422e6c"
                },
                {
                    "angle": -156.654453860503,
                    "magnitude": 132.257691645783,
                    "measurement_mrid": "_b7a23769-aefd-433c-a2b0-2684ca5ff21a"
                },
                {
                    "angle": 88.3619262420167,
                    "magnitude": 119.264416588937,
                    "measurement_mrid": "_ae493e9f-fddd-4c0f-9369-775652bf333c"
                },
                {
                    "angle": 88.3619262420167,
                    "magnitude": 119.264416588937,
                    "measurement_mrid": "_c63a8019-ed7c-4828-b8c9-81e9c0f74e17"
                },
                {
                    "angle": -156.141120890731,
                    "magnitude": 128.341157334537,
                    "measurement_mrid": "_bb69f411-b125-4458-bebb-0bdcb3e418f4"
                },
                {
                    "angle": -156.141120890731,
                    "magnitude": 128.341157334537,
                    "measurement_mrid": "_f1c6568c-c9a7-401b-a3b4-96a407629509"
                },
                {
                    "angle": -156.468497652681,
                    "magnitude": 7872.35330836554,
                    "measurement_mrid": "_b4cbefba-3465-4df3-8ecd-e2ab912b4685"
                },
                {
                    "angle": -156.945137375629,
                    "magnitude": 131.272185978931,
                    "measurement_mrid": "_add6959e-9f7e-4d76-bcdb-37bf1fbf5432"
                },
                {
                    "angle": -156.929818741898,
                    "magnitude": 130.96014979971,
                    "measurement_mrid": "_cd1cb8c0-df32-4b3d-8f3f-9160d75a4439"
                },
                {
                    "angle": -35.7897626321618,
                    "magnitude": 8293.28554820296,
                    "measurement_mrid": "_1168df0d-16a0-4d07-960c-cefea86dd02f"
                },
                {
                    "angle": 86.3887872160936,
                    "magnitude": 7365.34831938642,
                    "measurement_mrid": "_07837698-43c9-425e-b5b1-91b48707a74b"
                },
                {
                    "angle": -156.459235896625,
                    "magnitude": 7945.97651381798,
                    "measurement_mrid": "_546fb469-f321-416d-8fe1-38e794edd3ff"
                },
                {
                    "angle": -35.7854928793616,
                    "magnitude": 8280.40066603082,
                    "measurement_mrid": "_91d23397-74c0-44f4-ae92-75197f7fefef"
                },
                {
                    "angle": -30.6100806796505,
                    "magnitude": 7320.98107944179,
                    "measurement_mrid": "_46635082-2301-45da-acfa-26fa2a38b0c9"
                },
                {
                    "angle": 89.4491869881552,
                    "magnitude": 7274.94333533874,
                    "measurement_mrid": "_640963be-ae4c-4e96-86d0-9ec4d06f34c4"
                },
                {
                    "angle": -150.590854089272,
                    "magnitude": 7319.93308767497,
                    "measurement_mrid": "_f8603588-b9f5-4497-bd56-c28d10d33186"
                },
                {
                    "angle": -35.599902433235,
                    "magnitude": 8315.11820224787,
                    "measurement_mrid": "_4c1ac865-fc5f-40f0-8a5b-08e2437dc5e1"
                },
                {
                    "angle": -154.316763340883,
                    "magnitude": 7298.77063370587,
                    "measurement_mrid": "_54f05f08-4d8d-4e30-8951-8d3b632400be"
                },
                {
                    "angle": -34.0390596578182,
                    "magnitude": 7231.63249667713,
                    "measurement_mrid": "_675c7015-ba34-447e-b413-d50067e25728"
                },
                {
                    "angle": 87.2835198058325,
                    "magnitude": 7320.92582071386,
                    "measurement_mrid": "_b261f818-2536-4e48-8986-556ed8a8493d"
                },
                {
                    "angle": 87.0282167482347,
                    "magnitude": 120.620263600573,
                    "measurement_mrid": "_0fcd2373-fe2e-432d-be4a-f0af93b2fc2c"
                },
                {
                    "angle": 87.0108559743982,
                    "magnitude": 120.946193393036,
                    "measurement_mrid": "_d4b28b20-e903-42fb-8cc9-09e371076b33"
                },
                {
                    "angle": -154.125616053372,
                    "magnitude": 7300.03199178404,
                    "measurement_mrid": "_24c13611-728a-4583-8083-b9b12d69485c"
                },
                {
                    "angle": -33.8614657295086,
                    "magnitude": 7240.95668567166,
                    "measurement_mrid": "_9ef7e3d8-9b6c-4f28-9885-440b11e02929"
                },
                {
                    "angle": 87.3530666548922,
                    "magnitude": 7318.70645598924,
                    "measurement_mrid": "_c36fcea7-059a-47e2-91d4-b5b13047f43d"
                },
                {
                    "angle": -155.290275749832,
                    "magnitude": 127.718616525942,
                    "measurement_mrid": "_41ce3e5e-51dc-4f0f-8bb3-cc017c524b86"
                },
                {
                    "angle": -155.305965621726,
                    "magnitude": 128.030657425927,
                    "measurement_mrid": "_d9fadd47-9909-40e7-8536-3809713b0bd1"
                },
                {
                    "angle": 87.3850600956787,
                    "magnitude": 7314.3713236769,
                    "measurement_mrid": "_28b2bc36-057e-431b-b532-29e488bb113d"
                },
                {
                    "angle": -154.057468960376,
                    "magnitude": 7289.44230041858,
                    "measurement_mrid": "_a1c32b71-b60a-4df5-86a3-5a99455de35d"
                },
                {
                    "angle": -33.7789643128313,
                    "magnitude": 7236.45594065856,
                    "measurement_mrid": "_c1c916d9-de26-42eb-85da-48bf60e349b8"
                },
                {
                    "angle": -34.8408653442714,
                    "magnitude": 7709.25522214953,
                    "measurement_mrid": "_d2575f29-86a7-4ed3-ab16-de9cedd60dda"
                },
                {
                    "angle": 86.34028091045,
                    "magnitude": 7333.14528215358,
                    "measurement_mrid": "_cc46ab94-02be-4986-977b-068f28c13947"
                },
                {
                    "angle": -155.556734124286,
                    "magnitude": 127.317573108062,
                    "measurement_mrid": "_1e3a75f9-80b2-439e-8a0f-7438569a3f12"
                },
                {
                    "angle": -155.572471633924,
                    "magnitude": 127.629614316461,
                    "measurement_mrid": "_d4f686ea-a4c0-4f3d-97d8-718dd4e29806"
                },
                {
                    "angle": 86.6794243827058,
                    "magnitude": 119.5574122957,
                    "measurement_mrid": "_08d27a06-58f7-4f82-b6ef-7d69e42d7a00"
                },
                {
                    "angle": 86.6794243827058,
                    "magnitude": 119.5574122957,
                    "measurement_mrid": "_428f207c-63cb-4927-994c-464d174822da"
                },
                {
                    "angle": 88.864017472335,
                    "magnitude": 7215.25072673089,
                    "measurement_mrid": "_e3d8f51f-32c5-4e20-a5bf-ded96fea3453"
                },
                {
                    "angle": 86.6813866637803,
                    "magnitude": 119.340335169531,
                    "measurement_mrid": "_21a8e8e8-6972-495a-b44d-f38bece02c01"
                },
                {
                    "angle": 86.6638401179089,
                    "magnitude": 119.666265782194,
                    "measurement_mrid": "_2a62b155-846f-4986-9df1-81ecb8184cd7"
                },
                {
                    "angle": -35.7968701968585,
                    "magnitude": 8268.63509124246,
                    "measurement_mrid": "_dfdbf9bb-085f-4f0c-9853-98448701d2a1"
                },
                {
                    "angle": -156.918495498894,
                    "magnitude": 130.183712721573,
                    "measurement_mrid": "_67d223a6-1e3a-412a-8535-23ac48ccb85d"
                },
                {
                    "angle": -156.918495498894,
                    "magnitude": 130.183712721573,
                    "measurement_mrid": "_87daa2ab-3919-492c-aaec-bc573621f46f"
                },
                {
                    "angle": -155.547050556676,
                    "magnitude": 127.62149067145,
                    "measurement_mrid": "_436b040d-ad40-45be-8638-f15fe501733d"
                },
                {
                    "angle": -155.547050556676,
                    "magnitude": 127.62149067145,
                    "measurement_mrid": "_d60820b5-d18e-4ad7-8a14-80b1cd38b8dc"
                },
                {
                    "angle": -156.41303703371,
                    "magnitude": 7882.06555281085,
                    "measurement_mrid": "_73a248b9-b0cb-4317-a07b-a98fd8034649"
                },
                {
                    "angle": -36.2730528095651,
                    "magnitude": 136.569469043529,
                    "measurement_mrid": "_724930f6-5abc-4803-a1cd-206ee460f7cc"
                },
                {
                    "angle": -36.2507645477262,
                    "magnitude": 136.095513903709,
                    "measurement_mrid": "_cb2a8382-b048-44f5-bc03-3e5d9d126cb6"
                },
                {
                    "angle": -156.167815606335,
                    "magnitude": 128.10296028019,
                    "measurement_mrid": "_433b9192-8e9e-457b-b8e8-dd7c70cba026"
                },
                {
                    "angle": -156.167815606335,
                    "magnitude": 128.10296028019,
                    "measurement_mrid": "_6d22b344-2b2c-4de8-b2d0-9c8e3715cf9d"
                },
                {
                    "angle": -36.2692237768005,
                    "magnitude": 136.470749195093,
                    "measurement_mrid": "_239f0cee-884d-4fe1-a204-e4119e3381ea"
                },
                {
                    "angle": -36.2558459955083,
                    "magnitude": 136.186485038061,
                    "measurement_mrid": "_6dab1e9f-b0b5-4354-a232-d344e1f51d79"
                },
                {
                    "angle": -156.886628960675,
                    "magnitude": 131.647476369965,
                    "measurement_mrid": "_7a123aaa-4386-424b-9829-d1390ff0b2eb"
                },
                {
                    "angle": -156.886628960675,
                    "magnitude": 131.647476369965,
                    "measurement_mrid": "_e08ce091-8abb-4e06-aa4f-ee706f4f4375"
                },
                {
                    "angle": -156.399709452734,
                    "magnitude": 7903.70715583565,
                    "measurement_mrid": "_9c8d546d-6111-4712-8a2e-10d640219b59"
                },
                {
                    "angle": -156.453740176104,
                    "magnitude": 7876.94649633309,
                    "measurement_mrid": "_1f067a67-19d7-4d65-8468-6766ddd11205"
                },
                {
                    "angle": -35.7436322163981,
                    "magnitude": 8239.51562035261,
                    "measurement_mrid": "_a28fb31a-1ebc-43c3-8704-bf5144f0d4cd"
                },
                {
                    "angle": -34.7769571003742,
                    "magnitude": 128.781857836834,
                    "measurement_mrid": "_2bf32773-c0ae-4fd7-bc5c-52a1e4812587"
                },
                {
                    "angle": -34.7769571003742,
                    "magnitude": 128.781857836834,
                    "measurement_mrid": "_99d110f8-5e53-4922-835a-287a35c28441"
                },
                {
                    "angle": 86.2450651993971,
                    "magnitude": 7403.06048115109,
                    "measurement_mrid": "_bdd7c4d8-e764-4201-aca0-6b561bf0caa2"
                },
                {
                    "angle": -34.1766264912896,
                    "magnitude": 119.867496403087,
                    "measurement_mrid": "_060a9bdc-10f0-4269-bf06-9b7b5a9720b8"
                },
                {
                    "angle": -34.1766264912896,
                    "magnitude": 119.867496403087,
                    "measurement_mrid": "_6e02ea0e-3337-4eae-836b-e79c081d994b"
                },
                {
                    "angle": -156.42842021108,
                    "magnitude": 7873.84578948057,
                    "measurement_mrid": "_72eef66f-db7b-4afe-a079-d23136215d18"
                },
                {
                    "angle": -155.124418290221,
                    "magnitude": 7699.00953880372,
                    "measurement_mrid": "_1849e5c3-fafa-40cc-942e-c6dd413ad836"
                },
                {
                    "angle": 86.3381488152821,
                    "magnitude": 7332.52461327009,
                    "measurement_mrid": "_4d000528-f40e-4348-9b7a-f69c78b46f75"
                },
                {
                    "angle": -36.2783819521519,
                    "magnitude": 136.245476250242,
                    "measurement_mrid": "_4c638a22-85c9-4a07-aaba-59d712e51418"
                },
                {
                    "angle": -36.2783819521519,
                    "magnitude": 136.245476250242,
                    "measurement_mrid": "_ec0b37e9-8c8d-4e89-8ac8-8ad0ca253102"
                },
                {
                    "angle": 86.2329850245194,
                    "magnitude": 7396.91469088361,
                    "measurement_mrid": "_a10ac35a-8d11-4957-a371-9145167ae90b"
                },
                {
                    "angle": 87.0192624387258,
                    "magnitude": 120.783736542117,
                    "measurement_mrid": "_db183215-123b-4fbe-97d9-44249ba078f3"
                },
                {
                    "angle": 87.0192624387258,
                    "magnitude": 120.783736542117,
                    "measurement_mrid": "_e34f1b84-2f61-4d75-94ac-421a619ad2e3"
                },
                {
                    "angle": 85.762710290919,
                    "magnitude": 122.476835116947,
                    "measurement_mrid": "_67c30687-3cbc-402c-ba07-ef45c96a4c6c"
                },
                {
                    "angle": 85.762710290919,
                    "magnitude": 122.476835116947,
                    "measurement_mrid": "_aabc5504-4a3f-42e7-a87a-9b84ae9e0d80"
                },
                {
                    "angle": 85.9699076934791,
                    "magnitude": 120.943387630636,
                    "measurement_mrid": "_8b813a91-2bdd-44b3-ac2f-24086db03d52"
                },
                {
                    "angle": 85.9699076934791,
                    "magnitude": 120.943387630636,
                    "measurement_mrid": "_b14f2577-8e41-4565-a9a4-3f114079db17"
                },
                {
                    "angle": 86.8494414063429,
                    "magnitude": 7386.01742478737,
                    "measurement_mrid": "_1fc9b794-080a-475b-b1ac-636a740fa277"
                },
                {
                    "angle": -34.8616667843473,
                    "magnitude": 7753.07326440758,
                    "measurement_mrid": "_ae6332c7-d4d0-486d-93ba-b959cff99f02"
                },
                {
                    "angle": 85.7568661686701,
                    "magnitude": 121.518228306801,
                    "measurement_mrid": "_8181039a-470f-4e89-9c4c-0647a4744ddd"
                },
                {
                    "angle": 85.7856724276387,
                    "magnitude": 120.974825978106,
                    "measurement_mrid": "_953604aa-9cfa-4270-84dd-97daa9b97990"
                },
                {
                    "angle": -156.401861428405,
                    "magnitude": 7888.37730950277,
                    "measurement_mrid": "_f8052941-bfc9-4043-b206-4da377ea7b88"
                },
                {
                    "angle": 86.2840810482733,
                    "magnitude": 7344.35915084079,
                    "measurement_mrid": "_8822f760-84f3-4f1b-896f-76d202150d8e"
                },
                {
                    "angle": 86.2172696503968,
                    "magnitude": 7337.43414031429,
                    "measurement_mrid": "_30a14c1a-d411-45f1-96bd-1baa6a8aec63"
                },
                {
                    "angle": -154.714645213919,
                    "magnitude": 7781.08327497853,
                    "measurement_mrid": "_8f258cab-a0e9-4b7b-bcd6-4a20982154b1"
                },
                {
                    "angle": 85.9244564355948,
                    "magnitude": 122.086777772156,
                    "measurement_mrid": "_41adf921-e95d-479a-b691-749315fcc47e"
                },
                {
                    "angle": 85.9244564355948,
                    "magnitude": 122.086777772156,
                    "measurement_mrid": "_db1412b5-c916-4dc7-b66b-45c0ffc1171e"
                },
                {
                    "angle": -35.7872692248362,
                    "magnitude": 8293.2629006258,
                    "measurement_mrid": "_9996e810-7a5c-40de-b4e6-1b71e53d2dbb"
                },
                {
                    "angle": -156.165572522921,
                    "magnitude": 128.126225943229,
                    "measurement_mrid": "_5e97a23a-8c37-4f29-ad9d-d78d16bad438"
                },
                {
                    "angle": -156.165572522921,
                    "magnitude": 128.126225943229,
                    "measurement_mrid": "_c32748ec-5779-4a0e-ab4c-af9d4597b8c1"
                },
                {
                    "angle": 85.6032955496002,
                    "magnitude": 121.014985338003,
                    "measurement_mrid": "_017990d4-d4d0-4974-a2d4-ce72539184c7"
                },
                {
                    "angle": 85.6032955496002,
                    "magnitude": 121.014985338003,
                    "measurement_mrid": "_d05a55af-4697-4bab-920e-669a0d11d868"
                },
                {
                    "angle": -156.876588150832,
                    "magnitude": 130.603339856311,
                    "measurement_mrid": "_b86b6a75-949b-4ded-ba6c-ee3e0b220bd0"
                },
                {
                    "angle": -156.850938623208,
                    "magnitude": 130.083451986124,
                    "measurement_mrid": "_f159731c-976c-41e3-94ec-473cf2c41780"
                },
                {
                    "angle": -152.950538609863,
                    "magnitude": 7319.34767174946,
                    "measurement_mrid": "_f9c1cb0b-68a5-454a-86ef-25ebfe79441d"
                },
                {
                    "angle": -34.0735045140018,
                    "magnitude": 120.684643401393,
                    "measurement_mrid": "_6302c845-408b-4d5f-98b4-0357f15f1bd8"
                },
                {
                    "angle": -34.0735045140018,
                    "magnitude": 120.684643401393,
                    "measurement_mrid": "_a8801ab7-a010-4605-8ad1-131e18ce098a"
                },
                {
                    "angle": -153.536742588026,
                    "magnitude": 120.908629078964,
                    "measurement_mrid": "_3cc44514-4401-443a-a62f-4c3c18edb54c"
                },
                {
                    "angle": -153.536742588026,
                    "magnitude": 120.908629078964,
                    "measurement_mrid": "_adae7fd5-133a-4828-9553-726217632712"
                },
                {
                    "angle": -35.6530040508404,
                    "magnitude": 8293.10516467995,
                    "measurement_mrid": "_b98f7733-e104-4a59-93fd-f6e337469f0c"
                },
                {
                    "angle": 6.19492891697346,
                    "magnitude": 56.8808758056035,
                    "measurement_mrid": "_15f0587a-f1d0-46e6-a5c7-fe93df414242"
                },
                {
                    "angle": 109.426487866016,
                    "magnitude": 70.3508195865027,
                    "measurement_mrid": "_58b400b5-9121-482c-839f-e72aec7d7144"
                },
                {
                    "angle": -117.963014209926,
                    "magnitude": 59.5019421388615,
                    "measurement_mrid": "_c026a215-f733-4099-ac24-6daa47001297"
                },
                {
                    "angle": -155.705664152067,
                    "magnitude": 126.457084421661,
                    "measurement_mrid": "_1f6fdb31-be90-40a0-9486-c416c4abc43f"
                },
                {
                    "angle": -155.705664152067,
                    "magnitude": 126.457084421661,
                    "measurement_mrid": "_a9b9c8ad-46b2-4186-8eef-60f8ecd9c476"
                },
                {
                    "angle": -156.452537371646,
                    "magnitude": 7952.71764511939,
                    "measurement_mrid": "_9cf91233-761e-4d5f-80d9-c142eff6c062"
                },
                {
                    "angle": -155.24369895978,
                    "magnitude": 7647.47212262604,
                    "measurement_mrid": "_978ce7da-1a1b-4e36-95e8-6b2f8e67aa23"
                },
                {
                    "angle": -156.842663864096,
                    "magnitude": 130.897817536548,
                    "measurement_mrid": "_580b289e-ea37-4a02-b9d8-99fbb1ae2a8f"
                },
                {
                    "angle": -156.817071399402,
                    "magnitude": 130.377929107674,
                    "measurement_mrid": "_e4094f13-dc72-478e-a873-260118c7943d"
                },
                {
                    "angle": -33.9327903648285,
                    "magnitude": 7237.16546258269,
                    "measurement_mrid": "_cca8f649-8b68-4975-a035-a4ee6461cbe8"
                },
                {
                    "angle": 87.3257427196207,
                    "magnitude": 7319.57634928661,
                    "measurement_mrid": "_d50964f0-f4ac-4833-980b-e7fbaa5c5f44"
                },
                {
                    "angle": -154.201819724421,
                    "magnitude": 7299.56541953055,
                    "measurement_mrid": "_e86abd1f-dc84-4a56-852b-6c401c16f7e8"
                },
                {
                    "angle": 87.1863702234596,
                    "magnitude": 7234.68509423281,
                    "measurement_mrid": "_6c975425-6f97-4d22-b107-108bbf854240"
                },
                {
                    "angle": 86.6903124967857,
                    "magnitude": 119.800512931138,
                    "measurement_mrid": "_3f8bb792-b927-4b38-9e86-fc35c574fc64"
                },
                {
                    "angle": 86.7020064871324,
                    "magnitude": 119.583048632484,
                    "measurement_mrid": "_cb013ed7-f8dc-4641-9ae7-0b1239444f39"
                },
                {
                    "angle": 72.7110439799412,
                    "magnitude": 4.97527119617273,
                    "measurement_mrid": "_006b6011-da10-42f8-a69b-0091fe164e5b"
                },
                {
                    "angle": -168.715989859589,
                    "magnitude": 17.0662586550874,
                    "measurement_mrid": "_3816ad8e-208f-4a6e-bf7c-449ab743dd14"
                },
                {
                    "angle": -48.3725909846481,
                    "magnitude": 12.2052324448863,
                    "measurement_mrid": "_df68598c-5790-4ab6-b0d9-b4147d1f886e"
                },
                {
                    "angle": -156.865173858527,
                    "magnitude": 131.307375544796,
                    "measurement_mrid": "_ab0c99fb-f6d2-4089-9c9b-801f2241e286"
                },
                {
                    "angle": -156.814173763144,
                    "magnitude": 130.268108021109,
                    "measurement_mrid": "_dbc25ea3-1289-4dde-a72e-6d41a5d45c9e"
                },
                {
                    "angle": 85.9889534674125,
                    "magnitude": 122.854271367159,
                    "measurement_mrid": "_2e6291d8-f44a-4322-980f-a8a6a200d6a1"
                },
                {
                    "angle": 86.0317087016444,
                    "magnitude": 122.038890971653,
                    "measurement_mrid": "_3007ee9c-495d-431d-9105-b1cb9bf0f29c"
                },
                {
                    "angle": -156.400868531486,
                    "magnitude": 7903.08081189332,
                    "measurement_mrid": "_c3a7c114-1881-456a-b4c6-b3944d83454b"
                },
                {
                    "angle": -34.6813971374084,
                    "magnitude": 119.179441580905,
                    "measurement_mrid": "_2f1602d3-0f3b-47d3-aa9b-10ff58b18ca4"
                },
                {
                    "angle": -34.6966976068737,
                    "magnitude": 119.463701526155,
                    "measurement_mrid": "_a69169ee-a67c-4e88-87b7-9257bad427a1"
                },
                {
                    "angle": -34.2725116525492,
                    "magnitude": 120.384173683582,
                    "measurement_mrid": "_54ace696-7809-4d35-9b34-f69866574430"
                },
                {
                    "angle": -34.196583002109,
                    "magnitude": 118.962792054166,
                    "measurement_mrid": "_b53d57b5-b2b2-4494-8a25-6cc21a6e55fc"
                },
                {
                    "angle": 87.0196241936629,
                    "magnitude": 120.784055320012,
                    "measurement_mrid": "_83409941-d0e9-45a8-a34c-5f1d407ed01b"
                },
                {
                    "angle": 87.0196241936629,
                    "magnitude": 120.784055320012,
                    "measurement_mrid": "_9f69f3ee-b5fa-45f1-9a79-deb9b0a44219"
                },
                {
                    "angle": -35.7552131901404,
                    "magnitude": 8303.35399271618,
                    "measurement_mrid": "_d8ead74a-c385-4d3f-8184-132949b7b764"
                },
                {
                    "angle": -36.1015344956373,
                    "magnitude": 136.908017826933,
                    "measurement_mrid": "_1a6121c1-5e5e-48ae-90cb-28247f7a0029"
                },
                {
                    "angle": -36.0881980949328,
                    "magnitude": 136.623754021856,
                    "measurement_mrid": "_673883c7-2524-4e4d-a204-70ea65ca397b"
                },
                {
                    "angle": 86.7458970720653,
                    "magnitude": 120.084862842196,
                    "measurement_mrid": "_b04eb537-933f-43f2-9c58-4d86075fc76d"
                },
                {
                    "angle": 86.7458970720653,
                    "magnitude": 120.084862842196,
                    "measurement_mrid": "_c61724a8-5920-441a-a186-ebd127a8bc38"
                },
                {
                    "angle": 86.9450172630188,
                    "magnitude": 120.352334502839,
                    "measurement_mrid": "_cfb6eca5-f560-49f7-8ff5-da49f4e9933a"
                },
                {
                    "angle": 86.9160605658167,
                    "magnitude": 120.89573642467,
                    "measurement_mrid": "_dad1e607-d52c-4710-8def-d13578ecbe29"
                },
                {
                    "angle": 85.748173845424,
                    "magnitude": 122.514018315236,
                    "measurement_mrid": "_39207a0d-5294-4299-8e53-6e9fc7b4d2fc"
                },
                {
                    "angle": 85.7596085432023,
                    "magnitude": 122.296553693317,
                    "measurement_mrid": "_606c2669-9e82-4324-9fb4-85eca771796d"
                },
                {
                    "angle": -156.502630509643,
                    "magnitude": 7921.97578876716,
                    "measurement_mrid": "_3f6b7fda-1ae6-4c5b-9a4e-5828254f420e"
                },
                {
                    "angle": -34.8615080862145,
                    "magnitude": 7748.94316107246,
                    "measurement_mrid": "_3f0c43e1-3390-4576-ba60-ec67626602cd"
                },
                {
                    "angle": 85.9057449606299,
                    "magnitude": 122.167516995738,
                    "measurement_mrid": "_074b42c2-bf22-4134-8cd1-b585c356da88"
                },
                {
                    "angle": 85.934398764962,
                    "magnitude": 121.624114653604,
                    "measurement_mrid": "_3e4dc7f9-c1e5-406c-8db6-f0f828bae986"
                },
                {
                    "angle": -153.794950451067,
                    "magnitude": 7303.44272539689,
                    "measurement_mrid": "_c0a314ff-9b6b-4593-92f2-53465036a3f2"
                },
                {
                    "angle": 87.4669869040222,
                    "magnitude": 7314.19831832684,
                    "measurement_mrid": "_ddbc486d-0f3a-482b-acd1-e06113e74734"
                },
                {
                    "angle": -153.736981213328,
                    "magnitude": 7304.31743854763,
                    "measurement_mrid": "_de77d349-5376-449d-9b20-015cd41b0ddb"
                },
                {
                    "angle": -153.553461103835,
                    "magnitude": 121.323313542882,
                    "measurement_mrid": "_41e8ff41-b3ce-4f59-b4ae-210473676ab4"
                },
                {
                    "angle": -153.512070411451,
                    "magnitude": 120.5437325207,
                    "measurement_mrid": "_f6ca439d-b657-426d-9abf-27a4d5182393"
                },
                {
                    "angle": -153.737292847339,
                    "magnitude": 7304.16113232743,
                    "measurement_mrid": "_e6c94c1d-3cb8-41dd-8f26-ded63d2fa3d5"
                },
                {
                    "angle": 85.7341272029794,
                    "magnitude": 122.239719919455,
                    "measurement_mrid": "_b19a668a-cb38-4898-a8a3-90e5e17dfc0a"
                },
                {
                    "angle": 85.7341272029794,
                    "magnitude": 122.239719919455,
                    "measurement_mrid": "_b6e1961b-4967-48eb-8141-fb27acac6a1b"
                },
                {
                    "angle": 87.7310556283796,
                    "magnitude": 7304.59693094993,
                    "measurement_mrid": "_e21cd70a-5149-4f44-a10a-d02fa5a5d29c"
                },
                {
                    "angle": -155.579680910176,
                    "magnitude": 127.348239532493,
                    "measurement_mrid": "_71c1bfa5-bb0c-4a71-be30-e0c558f9e5e4"
                },
                {
                    "angle": -155.579680910176,
                    "magnitude": 127.348239532493,
                    "measurement_mrid": "_bbacc8ef-b644-45c1-9726-758cec8b6e16"
                },
                {
                    "angle": -36.2187623004967,
                    "magnitude": 137.104687298321,
                    "measurement_mrid": "_91b8f9bf-6d47-4007-83cd-97d5a28a24c3"
                },
                {
                    "angle": -36.185470642175,
                    "magnitude": 136.394015061907,
                    "measurement_mrid": "_ecaa04c5-43ce-4186-9925-2efa5edefd71"
                },
                {
                    "angle": -156.961396663437,
                    "magnitude": 131.142299897747,
                    "measurement_mrid": "_164ce66e-f1c7-4965-8efe-fcdf16a045c9"
                },
                {
                    "angle": -156.946062889929,
                    "magnitude": 130.830263138186,
                    "measurement_mrid": "_512eefde-c3fb-4d46-858a-e4c7de077480"
                },
                {
                    "angle": -31.1800534730597,
                    "magnitude": 7326.11366887921,
                    "measurement_mrid": "_227983b5-93ad-4160-a7cb-c8c693909b9d"
                },
                {
                    "angle": 88.9780196205029,
                    "magnitude": 7285.08923998937,
                    "measurement_mrid": "_2a43d025-599b-4991-9097-07ab1ef8baa0"
                },
                {
                    "angle": -151.171954048081,
                    "magnitude": 7324.25931794418,
                    "measurement_mrid": "_2e1a96ec-dbbc-498d-a7ec-e9c67dd697b1"
                },
                {
                    "angle": 88.8727263488081,
                    "magnitude": 7286.76221975596,
                    "measurement_mrid": "_9dceac23-2d62-4e7d-8ceb-458bcfb3e04f"
                },
                {
                    "angle": -155.745092832901,
                    "magnitude": 7728.92689844519,
                    "measurement_mrid": "_9e95cff4-d1b9-4154-984a-f7b425a387be"
                },
                {
                    "angle": -35.0325093928149,
                    "magnitude": 7976.72291284967,
                    "measurement_mrid": "_99f04f18-551c-4bfb-a959-226ac45b3fed"
                },
                {
                    "angle": 85.6341459793707,
                    "magnitude": 120.795491686799,
                    "measurement_mrid": "_4be2bdbd-0b87-43dc-9c39-03c53ee242eb"
                },
                {
                    "angle": 85.6052971071085,
                    "magnitude": 121.338893665702,
                    "measurement_mrid": "_8e8ebd42-1ade-496d-adf7-105691ce423d"
                },
                {
                    "angle": -31.232551249454,
                    "magnitude": 7325.44924807582,
                    "measurement_mrid": "_4181d7da-663d-4e39-bd28-3511ff2462a8"
                },
                {
                    "angle": -151.227159851334,
                    "magnitude": 7324.10192096326,
                    "measurement_mrid": "_7a9e0bd9-be87-47a6-94c7-0627f67b1253"
                },
                {
                    "angle": 88.9395364882342,
                    "magnitude": 7285.70753979034,
                    "measurement_mrid": "_f0ba6c9b-5628-407d-9cf8-43204f250bbe"
                },
                {
                    "angle": 88.9073109426842,
                    "magnitude": 7286.24102087176,
                    "measurement_mrid": "_12884bdb-d7ca-41c9-b4f5-f8c18975e07c"
                },
                {
                    "angle": -31.275480629764,
                    "magnitude": 7324.96077386717,
                    "measurement_mrid": "_45223bc5-da98-4ee7-9786-e99c65560d80"
                },
                {
                    "angle": -151.272933787482,
                    "magnitude": 7323.93017534753,
                    "measurement_mrid": "_63dc251f-cb71-48c6-8bab-7c230d59a309"
                },
                {
                    "angle": 86.1130640083415,
                    "magnitude": 7326.17785354319,
                    "measurement_mrid": "_012c6441-7f00-4834-8d2e-6b19999a948d"
                },
                {
                    "angle": -156.363140089589,
                    "magnitude": 7913.74990546838,
                    "measurement_mrid": "_7cb7e22b-7ad1-49da-84b9-fc5d788faea3"
                },
                {
                    "angle": -35.5893208903925,
                    "magnitude": 8312.21281478926,
                    "measurement_mrid": "_e5d5ab70-8edc-4a7f-b3e0-10300b509634"
                },
                {
                    "angle": 86.4400939698727,
                    "magnitude": 7369.56866043942,
                    "measurement_mrid": "_8858ae3a-15b4-4c66-a387-dcb065debe2d"
                },
                {
                    "angle": -156.406909851169,
                    "magnitude": 7885.57624006266,
                    "measurement_mrid": "_5543d0f7-d50d-4a00-a2f0-35d93ec51213"
                },
                {
                    "angle": -31.2333153055643,
                    "magnitude": 7325.03094965465,
                    "measurement_mrid": "_5544a08e-da5f-4627-b7fa-f97b84239449"
                },
                {
                    "angle": -155.726141036337,
                    "magnitude": 7738.87648690857,
                    "measurement_mrid": "_5cd4a8fa-7cb0-4f56-9139-93524f3fe66f"
                },
                {
                    "angle": -155.705613115997,
                    "magnitude": 7749.74507465316,
                    "measurement_mrid": "_4ea0af65-769e-4069-996b-ca0b5998f7c8"
                },
                {
                    "angle": 87.7309344153163,
                    "magnitude": 7304.53602901589,
                    "measurement_mrid": "_dff74d59-785e-4073-b411-24cccfc54914"
                },
                {
                    "angle": -151.727384669986,
                    "magnitude": 7319.71535283843,
                    "measurement_mrid": "_614789c7-a977-4888-a0a9-1f8a82ea0f7e"
                },
                {
                    "angle": -35.9852426795302,
                    "magnitude": 137.595679140292,
                    "measurement_mrid": "_1a841dc2-0093-4904-8b70-35be469fa2dc"
                },
                {
                    "angle": -35.9852426795302,
                    "magnitude": 137.595679140292,
                    "measurement_mrid": "_6399f004-28e2-498f-a0db-e1377cf291e9"
                },
                {
                    "angle": 85.9121849783196,
                    "magnitude": 121.933086968635,
                    "measurement_mrid": "_6015aff3-3aab-41be-8e25-59450b32fbed"
                },
                {
                    "angle": 85.9121849783196,
                    "magnitude": 121.933086968635,
                    "measurement_mrid": "_a64b4e75-671e-4e5e-b8e1-04decfedf8d5"
                },
                {
                    "angle": 86.1058612829446,
                    "magnitude": 7324.66017074833,
                    "measurement_mrid": "_06cf9475-9919-46b9-8bf9-a37f4f71118a"
                },
                {
                    "angle": -35.5909804488011,
                    "magnitude": 8312.54050107199,
                    "measurement_mrid": "_efc240c8-e57d-4d80-aaa1-76b587bfe9a5"
                },
                {
                    "angle": 86.425149059403,
                    "magnitude": 7386.79507328316,
                    "measurement_mrid": "_abfba786-14ea-489e-8377-3f45f367b285"
                },
                {
                    "angle": -156.242215508069,
                    "magnitude": 7974.31083042556,
                    "measurement_mrid": "_7cf1c697-7451-46cb-93c0-3fe74a78b682"
                },
                {
                    "angle": 86.4250369575796,
                    "magnitude": 7386.73216704139,
                    "measurement_mrid": "_b4715d7f-7583-4513-8957-be7e232f394d"
                },
                {
                    "angle": -35.5838544642936,
                    "magnitude": 8336.87046801196,
                    "measurement_mrid": "_eb66cd0e-04d9-4d91-aa76-29edbc2d61dc"
                },
                {
                    "angle": 86.4237937926029,
                    "magnitude": 7386.10552721556,
                    "measurement_mrid": "_773de9ad-9bdb-48b2-9d31-37d86b4c3783"
                },
                {
                    "angle": 86.4202922124602,
                    "magnitude": 7382.62548834422,
                    "measurement_mrid": "_f7f8f935-2e2b-4a34-a9da-68d6ca42e53c"
                },
                {
                    "angle": -35.2817733435547,
                    "magnitude": 128.196667790316,
                    "measurement_mrid": "_52445f94-8115-4470-b4d9-546b61683dc6"
                },
                {
                    "angle": -35.2817733435547,
                    "magnitude": 128.196667790316,
                    "measurement_mrid": "_f92819b1-8327-47b6-9490-7ed583df6641"
                },
                {
                    "angle": -156.713678786231,
                    "magnitude": 131.427606290115,
                    "measurement_mrid": "_1e2ac115-3c85-4fe7-9033-6ccd792943a5"
                },
                {
                    "angle": -156.713678786231,
                    "magnitude": 131.427606290115,
                    "measurement_mrid": "_c94b8410-f637-4c4c-8c3f-65aab48c0cc9"
                },
                {
                    "angle": -156.900182489346,
                    "magnitude": 131.39103528787,
                    "measurement_mrid": "_40ddd5c9-c8b2-45ae-9fa1-198e501f4df4"
                },
                {
                    "angle": -156.900182489346,
                    "magnitude": 131.39103528787,
                    "measurement_mrid": "_a4e93833-2f32-430d-b1bd-cee995443a16"
                },
                {
                    "angle": -156.445812470261,
                    "magnitude": 127.963698421555,
                    "measurement_mrid": "_9cc0ff86-256e-4a46-8cd3-9c0a3a3571aa"
                },
                {
                    "angle": -156.445812470261,
                    "magnitude": 127.963698421555,
                    "measurement_mrid": "_f5d7f74e-e7e5-49e8-8ff8-10a86a43fa19"
                },
                {
                    "angle": -36.1036965938691,
                    "magnitude": 136.84716540262,
                    "measurement_mrid": "_9ccf2e5f-0f11-4568-9838-ecfeb6c03af1"
                },
                {
                    "angle": -36.0947932976463,
                    "magnitude": 136.657480059508,
                    "measurement_mrid": "_a0263059-38c8-4de0-b85f-493c83aa8207"
                },
                {
                    "angle": -35.5786934185588,
                    "magnitude": 8334.27808601892,
                    "measurement_mrid": "_fe486007-17b9-4ce6-86ab-b30d266547e8"
                },
                {
                    "angle": -35.5821420370424,
                    "magnitude": 8335.82908479868,
                    "measurement_mrid": "_27237ac8-a414-468e-a160-6b5408f49a75"
                },
                {
                    "angle": -156.245946042207,
                    "magnitude": 7971.9137253468,
                    "measurement_mrid": "_2bdf15b0-7322-4280-bffe-d00239b0a0bb"
                },
                {
                    "angle": 86.4255834791434,
                    "magnitude": 7386.90525265202,
                    "measurement_mrid": "_5a68bb40-09d1-44bf-8118-af6d78669e72"
                },
                {
                    "angle": -156.87630631941,
                    "magnitude": 130.605805214486,
                    "measurement_mrid": "_3dcef02b-4682-4219-8484-fab895afcaf1"
                },
                {
                    "angle": -156.85065753968,
                    "magnitude": 130.085917371747,
                    "measurement_mrid": "_67f71ebd-9116-4ef0-899e-d2421f1e0d4e"
                },
                {
                    "angle": -156.125280431728,
                    "magnitude": 7980.61107850878,
                    "measurement_mrid": "_1a8212c1-b207-4e57-b398-940ba1897275"
                },
                {
                    "angle": 86.478809945534,
                    "magnitude": 7321.64354265817,
                    "measurement_mrid": "_1c520587-9e84-44c5-98a1-9d0e6283f200"
                },
                {
                    "angle": -35.7025007516561,
                    "magnitude": 8262.80058901206,
                    "measurement_mrid": "_e9d9b166-d8d5-4979-bd80-bba3e4ffcb3a"
                },
                {
                    "angle": -35.7574487190761,
                    "magnitude": 8302.0851383743,
                    "measurement_mrid": "_9578f213-cf75-4997-9e85-f022f676a6e2"
                },
                {
                    "angle": -34.3537947836492,
                    "magnitude": 7786.65055982384,
                    "measurement_mrid": "_6d56bc63-4ee1-4410-8ff3-92279415185a"
                },
                {
                    "angle": 86.4202891253268,
                    "magnitude": 7381.55967968198,
                    "measurement_mrid": "_4d22c1d0-571d-4faa-9f5d-18d3b9b4fc26"
                },
                {
                    "angle": 86.4788531704907,
                    "magnitude": 7322.6228842173,
                    "measurement_mrid": "_bd984957-6c14-4c0a-a73b-a33ad69ea6b2"
                },
                {
                    "angle": 86.478716745686,
                    "magnitude": 7323.74071348341,
                    "measurement_mrid": "_268b55a5-0c04-4f84-9d6b-0bfde81fbc7f"
                },
                {
                    "angle": -35.6964752715088,
                    "magnitude": 8264.86192919979,
                    "measurement_mrid": "_8e95b533-9f12-472e-9eee-8912cd471582"
                },
                {
                    "angle": -156.128018798038,
                    "magnitude": 7980.27268953954,
                    "measurement_mrid": "_a6f9e76c-f026-47d0-b180-f6397869f1aa"
                },
                {
                    "angle": -156.127973177679,
                    "magnitude": 7980.39941080506,
                    "measurement_mrid": "_0cbaef9d-c401-40d4-bcae-e154f2c620e1"
                },
                {
                    "angle": 86.4786983950294,
                    "magnitude": 7323.8405640662,
                    "measurement_mrid": "_366f634b-8c2b-4aa6-84a8-cb5a8cf7424e"
                },
                {
                    "angle": 85.9229214310413,
                    "magnitude": 121.768858722186,
                    "measurement_mrid": "_937240f1-6f97-4622-9063-aaaee4b0a237"
                },
                {
                    "angle": 85.9057244352742,
                    "magnitude": 122.094788511615,
                    "measurement_mrid": "_f6c3dc2f-f46b-42fa-a0f5-b9631e1a047f"
                },
                {
                    "angle": 86.4787215337687,
                    "magnitude": 7322.49759896421,
                    "measurement_mrid": "_0e20cfd1-191b-4fa4-8188-72d590d12124"
                },
                {
                    "angle": -156.126900904744,
                    "magnitude": 7980.14001801068,
                    "measurement_mrid": "_559c40e1-901a-419a-92b1-8cd2d8bf1c03"
                },
                {
                    "angle": -35.6985047989078,
                    "magnitude": 8263.70135556433,
                    "measurement_mrid": "_c5793ac4-886d-43c3-afd2-0af2538668b6"
                },
                {
                    "angle": -35.6967709857167,
                    "magnitude": 8264.52049019537,
                    "measurement_mrid": "_62bdfa5b-f096-41cf-a161-f1a2b0f78a97"
                },
                {
                    "angle": -156.126800619911,
                    "magnitude": 7980.29229194432,
                    "measurement_mrid": "_5433774f-4ec1-4533-8819-6967e5fcdef7"
                },
                {
                    "angle": -35.6985714809933,
                    "magnitude": 8263.78330748232,
                    "measurement_mrid": "_a8da8805-be4e-477e-9a25-f9634bf0ed53"
                },
                {
                    "angle": 86.4788270044248,
                    "magnitude": 7322.59245616095,
                    "measurement_mrid": "_f0a2ea64-800f-4d8d-ab46-3eaaf1e5b740"
                },
                {
                    "angle": 85.6344062320043,
                    "magnitude": 7415.15677857509,
                    "measurement_mrid": "_87f227ad-7a10-4cee-b8b0-e1ae03d3a222"
                },
                {
                    "angle": -34.8623248495234,
                    "magnitude": 7748.48316405479,
                    "measurement_mrid": "_7ade7a79-d274-4c56-a85b-7ab875d3af03"
                },
                {
                    "angle": -36.1850584822799,
                    "magnitude": 136.570440788126,
                    "measurement_mrid": "_8cd0987c-a2e7-4dd3-8f08-c534eee708f9"
                },
                {
                    "angle": -36.2072717434995,
                    "magnitude": 137.044394494501,
                    "measurement_mrid": "_f5c70432-105a-4009-95cc-fc0f6b12efc6"
                },
                {
                    "angle": -156.591049177822,
                    "magnitude": 132.252220151656,
                    "measurement_mrid": "_ea582162-d35a-4b56-91eb-50944036a04b"
                },
                {
                    "angle": -156.565715287602,
                    "magnitude": 131.732333343226,
                    "measurement_mrid": "_f235cbd7-b343-4be8-b753-585b25319bab"
                },
                {
                    "angle": -36.2023565047129,
                    "magnitude": 136.749296333097,
                    "measurement_mrid": "_643f9b9c-8608-4bf4-b70b-0ce2cf2e6c70"
                },
                {
                    "angle": -36.2023565047129,
                    "magnitude": 136.749296333097,
                    "measurement_mrid": "_6911c85f-a17c-4793-af32-ef81a5108c07"
                },
                {
                    "angle": -34.239258103152,
                    "magnitude": 7215.77756776161,
                    "measurement_mrid": "_756e06cd-fec0-4d06-b149-4ad5fa81a3f9"
                },
                {
                    "angle": -35.7792289249237,
                    "magnitude": 8296.93293901239,
                    "measurement_mrid": "_f4c9b31b-9fc2-4216-829c-0433929254f7"
                },
                {
                    "angle": 87.2066391076866,
                    "magnitude": 120.932510088616,
                    "measurement_mrid": "_343e1d4c-fc22-4dbf-8aa6-7ed81d6d6eb0"
                },
                {
                    "angle": 87.2355867435772,
                    "magnitude": 120.389108543898,
                    "measurement_mrid": "_c77ba072-f531-402f-acc1-d60d64f28d3b"
                },
                {
                    "angle": 85.7557586106269,
                    "magnitude": 122.422525048116,
                    "measurement_mrid": "_8ca0f0d8-860c-46c0-92cf-a9b098b9656b"
                },
                {
                    "angle": 85.7557586106269,
                    "magnitude": 122.422525048116,
                    "measurement_mrid": "_e0c01d7a-10e5-4680-b84b-e9bd8a3f46b2"
                },
                {
                    "angle": -152.208752818675,
                    "magnitude": 120.993843077971,
                    "measurement_mrid": "_e377c867-0ed7-4a16-b4c1-447731fdbf6e"
                },
                {
                    "angle": -152.208752818675,
                    "magnitude": 120.993843077971,
                    "measurement_mrid": "_fc30a29c-3430-4e68-b912-84ce38266a0e"
                },
                {
                    "angle": -156.206595682538,
                    "magnitude": 127.774750241416,
                    "measurement_mrid": "_197767e8-fa9b-44a1-b4ac-56c0af9af2e9"
                },
                {
                    "angle": -156.206595682538,
                    "magnitude": 127.774750241416,
                    "measurement_mrid": "_d784a363-0c0a-475d-a3ef-3565e0bc5925"
                },
                {
                    "angle": 86.3892661041539,
                    "magnitude": 7363.48891917447,
                    "measurement_mrid": "_264e468d-c62f-45c1-a495-8b6f5451d413"
                },
                {
                    "angle": 87.0183670564489,
                    "magnitude": 7377.65353563054,
                    "measurement_mrid": "_92722898-0f79-4ed9-98ba-7d7eff3a7023"
                },
                {
                    "angle": -36.1176827635587,
                    "magnitude": 136.56500325965,
                    "measurement_mrid": "_0ad056d5-e1cf-4bdb-a3b2-9865d6f2cae8"
                },
                {
                    "angle": -36.1176827635587,
                    "magnitude": 136.56500325965,
                    "measurement_mrid": "_e9735476-e859-4380-9ce0-287b52dc4027"
                },
                {
                    "angle": 87.1997377961427,
                    "magnitude": 7241.25482561171,
                    "measurement_mrid": "_0593b8a5-069d-4e53-812f-5d2441309545"
                },
                {
                    "angle": 85.9531438599175,
                    "magnitude": 7419.44782987469,
                    "measurement_mrid": "_ca4de9f2-e3c7-4e62-ad46-0a0d98473ec8"
                },
                {
                    "angle": -155.126477295645,
                    "magnitude": 7698.00312585782,
                    "measurement_mrid": "_2540db13-54eb-4fbc-823c-2a5d8aed2507"
                },
                {
                    "angle": -35.8047643397162,
                    "magnitude": 8264.10029301093,
                    "measurement_mrid": "_45a65fa2-8939-4fa2-819b-fb30cd790e2a"
                },
                {
                    "angle": -36.1466567394836,
                    "magnitude": 136.502908739317,
                    "measurement_mrid": "_5b9fcd84-8392-4097-8a79-822933707fe2"
                },
                {
                    "angle": -36.1332816778916,
                    "magnitude": 136.218645186375,
                    "measurement_mrid": "_7bdebb2a-89f5-4af4-949c-73827a7c7f19"
                },
                {
                    "angle": 87.1859781765894,
                    "magnitude": 7234.48695046226,
                    "measurement_mrid": "_e96e182e-734f-48ff-9e65-c042f755474b"
                },
                {
                    "angle": -33.7894636474413,
                    "magnitude": 7235.25548589158,
                    "measurement_mrid": "_b3a08a3f-dca7-40ca-9eff-44bfa9376ecd"
                },
                {
                    "angle": -36.0897264787059,
                    "magnitude": 137.764455496902,
                    "measurement_mrid": "_4fe9072b-5e4f-49db-8a54-47a420f31792"
                },
                {
                    "angle": -36.0897264787059,
                    "magnitude": 137.764455496902,
                    "measurement_mrid": "_b8b5ef2a-abc7-405d-98f0-b088574a1dd6"
                },
                {
                    "angle": 86.6379005011782,
                    "magnitude": 121.476257073584,
                    "measurement_mrid": "_3b289cb7-a88d-4aff-ab8d-3b7aa21eef17"
                },
                {
                    "angle": 86.6092108804555,
                    "magnitude": 122.019658822058,
                    "measurement_mrid": "_a2163a5e-9012-4824-ac18-7f1179dade8d"
                },
                {
                    "angle": -156.223126197271,
                    "magnitude": 128.005900982593,
                    "measurement_mrid": "_f7ca4ebf-7324-45c3-832d-ec2db0af9749"
                },
                {
                    "angle": -156.196954413148,
                    "magnitude": 127.486012687244,
                    "measurement_mrid": "_ff7807b5-0481-4ed2-bf4a-4121bd7df422"
                },
                {
                    "angle": -156.881334672509,
                    "magnitude": 130.414726455174,
                    "measurement_mrid": "_4fd305c9-073a-4094-be2b-0fdbb7573b23"
                },
                {
                    "angle": -156.865917407989,
                    "magnitude": 130.102689801077,
                    "measurement_mrid": "_c087b03c-779f-4d18-9219-1a7798441b24"
                },
                {
                    "angle": -154.545880462532,
                    "magnitude": 120.470806308946,
                    "measurement_mrid": "_4f079d76-0366-4674-8b2d-36575758fd67"
                },
                {
                    "angle": -154.545880462532,
                    "magnitude": 120.470806308946,
                    "measurement_mrid": "_cc0e9e23-5aa0-4692-a244-27cef9f4e115"
                },
                {
                    "angle": -35.6224862740711,
                    "magnitude": 8319.00250221087,
                    "measurement_mrid": "_3dc74074-3a25-4d5d-8bc6-35c9a4079db3"
                },
                {
                    "angle": -36.1333808726,
                    "magnitude": 136.422313581759,
                    "measurement_mrid": "_10305600-5107-462d-ad7a-ffd1ee046ab0"
                },
                {
                    "angle": -36.1333808726,
                    "magnitude": 136.422313581759,
                    "measurement_mrid": "_9569c7ea-078c-4a26-97be-d0e69175e9c6"
                },
                {
                    "angle": 86.5138254318767,
                    "magnitude": 121.879965836119,
                    "measurement_mrid": "_07598b5a-2c8f-45cd-99af-db373d12bfe6"
                },
                {
                    "angle": 86.5138254318767,
                    "magnitude": 121.879965836119,
                    "measurement_mrid": "_ceba6fc5-b0bc-4a77-a1c7-1800fbaca195"
                },
                {
                    "angle": 85.6387050314688,
                    "magnitude": 7416.76537310411,
                    "measurement_mrid": "_2e57dc9f-5c6c-4b50-885a-b89c329a5754"
                },
                {
                    "angle": -34.8541009273895,
                    "magnitude": 7726.70621297648,
                    "measurement_mrid": "_8cdc091b-dffe-4c7a-90f8-a1a61b35325a"
                },
                {
                    "angle": -155.180044178207,
                    "magnitude": 7680.01557435989,
                    "measurement_mrid": "_9dbc0a9e-d985-4554-85c4-345fc526ba30"
                },
                {
                    "angle": 85.9200399286713,
                    "magnitude": 121.895812013873,
                    "measurement_mrid": "_6c49438e-c17b-44f4-83fe-d438fe4267c0"
                },
                {
                    "angle": 85.9200399286713,
                    "magnitude": 121.895812013873,
                    "measurement_mrid": "_c089416b-a588-40f1-85d2-c1c836bb81a8"
                },
                {
                    "angle": -156.937943738956,
                    "magnitude": 131.111702671065,
                    "measurement_mrid": "_3caca942-e43a-4e19-8113-589f814e8719"
                },
                {
                    "angle": -156.937943738956,
                    "magnitude": 131.111702671065,
                    "measurement_mrid": "_b521c1f0-848f-4c74-91ad-0a28198575e7"
                },
                {
                    "angle": -35.8838990758783,
                    "magnitude": 8231.32700242904,
                    "measurement_mrid": "_65f5347b-0531-4d69-8442-f57a9c89ae7e"
                },
                {
                    "angle": -35.9477373911704,
                    "magnitude": 138.858465789408,
                    "measurement_mrid": "_a056d609-310f-413d-ab6c-3f8b0798b458"
                },
                {
                    "angle": -35.9148549490421,
                    "magnitude": 138.147796892433,
                    "measurement_mrid": "_f32917bf-6c0f-43e6-8cba-453aa82140b8"
                },
                {
                    "angle": -35.965675804505,
                    "magnitude": 137.238446978125,
                    "measurement_mrid": "_30596292-6709-49b3-af0d-09fb605915bf"
                },
                {
                    "angle": -35.9987677086685,
                    "magnitude": 137.949118342985,
                    "measurement_mrid": "_4fd915b1-b9fd-4162-9b0e-f6baeb1a642f"
                },
                {
                    "angle": 87.2217792110525,
                    "magnitude": 120.666449253279,
                    "measurement_mrid": "_3e20838c-bf9e-4594-9da2-265e8f01da38"
                },
                {
                    "angle": 87.2217792110525,
                    "magnitude": 120.666449253279,
                    "measurement_mrid": "_42358a61-5b60-4802-8eb3-4a1c3160a03d"
                },
                {
                    "angle": -34.2104113581611,
                    "magnitude": 119.19091266705,
                    "measurement_mrid": "_2a119d05-8168-41da-8cf9-c9812f3db468"
                },
                {
                    "angle": -34.2611546368047,
                    "magnitude": 120.138832557814,
                    "measurement_mrid": "_376301e5-073c-4a63-a381-b2763006f271"
                },
                {
                    "angle": -153.537196429825,
                    "magnitude": 121.045325862331,
                    "measurement_mrid": "_202d2aea-fd9a-45f2-b90a-aaa7f4b1fa17"
                },
                {
                    "angle": -153.526135390585,
                    "magnitude": 120.837479859014,
                    "measurement_mrid": "_db26d1af-6dfc-499e-9f82-eaa7d58d61f1"
                },
                {
                    "angle": -36.1620002406369,
                    "magnitude": 137.397675909621,
                    "measurement_mrid": "_03f8fe9c-d376-4e4c-8b98-00e96f8c50dd"
                },
                {
                    "angle": -36.1620002406369,
                    "magnitude": 137.397675909621,
                    "measurement_mrid": "_10793aa7-c7cd-44b3-9331-12b3e241d08f"
                },
                {
                    "angle": -152.949934397013,
                    "magnitude": 7319.60995452139,
                    "measurement_mrid": "_d69c346c-eacc-42c9-8b4b-a0c0f389efd3"
                },
                {
                    "angle": -156.162735093928,
                    "magnitude": 127.997778139887,
                    "measurement_mrid": "_00397e4f-f6b0-41e6-8866-9ba5dad81e8a"
                },
                {
                    "angle": -156.173182759387,
                    "magnitude": 128.205622961923,
                    "measurement_mrid": "_9837a8fd-8667-4e40-8230-8a640dc3ba7f"
                },
                {
                    "angle": 85.7724462995904,
                    "magnitude": 121.256657212638,
                    "measurement_mrid": "_4fd0b546-c5d9-417d-893d-76664d199974"
                },
                {
                    "angle": 85.7724462995904,
                    "magnitude": 121.256657212638,
                    "measurement_mrid": "_60f845d5-a955-49e1-b693-010df439093c"
                },
                {
                    "angle": 85.152546671657,
                    "magnitude": 122.258576754543,
                    "measurement_mrid": "_59810713-9286-40f4-b27b-d3abfbe1c5df"
                },
                {
                    "angle": 85.1240421982159,
                    "magnitude": 122.801979131567,
                    "measurement_mrid": "_c7bb8ef3-ce63-4ba4-894a-a47db73091be"
                },
                {
                    "angle": 87.5452165402849,
                    "magnitude": 7311.40783501564,
                    "measurement_mrid": "_8680f28b-b6ea-4d52-9497-264305ccc133"
                },
                {
                    "angle": -156.503404751256,
                    "magnitude": 7921.55402905314,
                    "measurement_mrid": "_b9662a5b-ddbf-4d98-bfc3-eab65364834a"
                },
                {
                    "angle": -31.677547538549,
                    "magnitude": 121.134336686566,
                    "measurement_mrid": "_989b62b2-00ea-4ada-af15-287552bc04f8"
                },
                {
                    "angle": -31.677547538549,
                    "magnitude": 121.134336686566,
                    "measurement_mrid": "_a523be9f-125d-4638-b59f-4e3952d7326d"
                },
                {
                    "angle": -34.1553297256343,
                    "magnitude": 120.594297624969,
                    "measurement_mrid": "_377bacf1-1e22-4987-a24c-a59f5d901eb8"
                },
                {
                    "angle": -34.1553297256343,
                    "magnitude": 120.594297624969,
                    "measurement_mrid": "_45d9d8f1-472c-44f3-9325-d33298d40739"
                },
                {
                    "angle": -32.7094536960577,
                    "magnitude": 120.980544291352,
                    "measurement_mrid": "_5c74c7b7-2bcb-4e1d-a132-465878c9d4d4"
                },
                {
                    "angle": -32.7094536960577,
                    "magnitude": 120.980544291352,
                    "measurement_mrid": "_e9594e6a-fc53-463b-a2f1-b5c2c9af836c"
                },
                {
                    "angle": -156.876228568702,
                    "magnitude": 130.458873090589,
                    "measurement_mrid": "_4374cced-7344-44b4-a61b-68747cf141a6"
                },
                {
                    "angle": -156.860816201208,
                    "magnitude": 130.1468367028,
                    "measurement_mrid": "_8ad9e95e-73c5-4829-aa7b-a632a0961bc6"
                },
                {
                    "angle": -156.957579573046,
                    "magnitude": 130.962142525162,
                    "measurement_mrid": "_15acda76-15e0-411a-97de-5443033443ff"
                },
                {
                    "angle": -156.957579573046,
                    "magnitude": 130.962142525162,
                    "measurement_mrid": "_e8b2947a-1b9d-42e8-8d9d-ac8923dda01f"
                },
                {
                    "angle": -152.95091518617,
                    "magnitude": 7319.13794788429,
                    "measurement_mrid": "_25d54bb2-d57e-402d-8b6a-9fc042741c71"
                },
                {
                    "angle": -32.7008928939611,
                    "magnitude": 120.845077208316,
                    "measurement_mrid": "_25d1861a-3ed4-456e-91d3-5fa51cbedb58"
                },
                {
                    "angle": -32.7159976532878,
                    "magnitude": 121.129333672161,
                    "measurement_mrid": "_72b0e277-8d37-4f7b-b819-8e6f100de553"
                },
                {
                    "angle": -155.736025014241,
                    "magnitude": 7733.65771979483,
                    "measurement_mrid": "_8dd8864f-302f-45db-9f8e-080db5cf2e3f"
                },
                {
                    "angle": -153.370450110322,
                    "magnitude": 7310.84037720291,
                    "measurement_mrid": "_1fff7739-9a60-4232-961a-6c02e4315d1b"
                },
                {
                    "angle": -33.2078229116777,
                    "magnitude": 7281.54194958927,
                    "measurement_mrid": "_8a77ed01-f7d1-42ca-8fc6-f4c5eb5b10d0"
                },
                {
                    "angle": 87.610731738131,
                    "magnitude": 7310.05418833072,
                    "measurement_mrid": "_9a1e60e9-49ad-485e-b32b-aa9548a22e46"
                },
                {
                    "angle": -153.47401053959,
                    "magnitude": 7308.88895084063,
                    "measurement_mrid": "_7b97ad2b-ce4c-4f76-8e95-11566cd0dce3"
                },
                {
                    "angle": 87.5710959562106,
                    "magnitude": 7310.96166435345,
                    "measurement_mrid": "_9ad2b18d-8380-4319-8dd6-2dd50bc43208"
                },
                {
                    "angle": -33.2963779100599,
                    "magnitude": 7276.10764586015,
                    "measurement_mrid": "_f38d5356-c692-4be3-af2f-15d9a797e148"
                },
                {
                    "angle": -35.6567937215927,
                    "magnitude": 131.839148217172,
                    "measurement_mrid": "_47639622-33c3-4d4d-839b-806b477f2a01"
                },
                {
                    "angle": -35.6567937215927,
                    "magnitude": 131.839148217172,
                    "measurement_mrid": "_f2ba0321-f81a-4d5e-b635-3bb820b1921a"
                },
                {
                    "angle": -36.198702173078,
                    "magnitude": 136.556310784129,
                    "measurement_mrid": "_4a12ee42-59ea-4bdf-a7e5-cbf3e4fa3c1f"
                },
                {
                    "angle": -36.2209173079468,
                    "magnitude": 137.030264818524,
                    "measurement_mrid": "_7940692c-2d7f-4aa0-b2d1-eda0fc661185"
                },
                {
                    "angle": -36.1032333523439,
                    "magnitude": 136.732660551852,
                    "measurement_mrid": "_771574f3-8fcb-42b8-a501-eb37b518f81a"
                },
                {
                    "angle": -36.1032333523439,
                    "magnitude": 136.732660551852,
                    "measurement_mrid": "_df52d1c0-ffab-4231-9961-27283c2f8c30"
                },
                {
                    "angle": -156.868013165786,
                    "magnitude": 130.313971772353,
                    "measurement_mrid": "_65ad0eef-d1ae-40c8-87c0-1f9eb85c9898"
                },
                {
                    "angle": -156.868013165786,
                    "magnitude": 130.313971772353,
                    "measurement_mrid": "_d15bca5f-012b-4768-9764-01a6b8898dbb"
                },
                {
                    "angle": -156.453495373747,
                    "magnitude": 7946.2178976093,
                    "measurement_mrid": "_acfcf7cf-4b31-43e6-8319-72ccc480c2e2"
                },
                {
                    "angle": -156.20886953038,
                    "magnitude": 7997.61175755033,
                    "measurement_mrid": "_0fa8946a-394b-4bb8-b5a4-c95dfb088752"
                },
                {
                    "angle": -35.638992281227,
                    "magnitude": 8302.71587895182,
                    "measurement_mrid": "_509b2d23-57a7-4bd3-bd0e-5e6ec2dcf05f"
                },
                {
                    "angle": 85.6541151777179,
                    "magnitude": 7419.49370992443,
                    "measurement_mrid": "_2d90e4b9-4d7c-4480-990e-752314dd726b"
                },
                {
                    "angle": -155.231216768695,
                    "magnitude": 7654.1399827025,
                    "measurement_mrid": "_346ee7f3-8240-44e0-b439-5bca03954688"
                },
                {
                    "angle": -34.8365971149523,
                    "magnitude": 7709.4562328329,
                    "measurement_mrid": "_fc8ef8f0-a27a-441b-812a-cc0ebf5297d6"
                },
                {
                    "angle": -155.277980153229,
                    "magnitude": 7629.56865626247,
                    "measurement_mrid": "_ddd79c83-679b-4451-8ae5-fc6d83b5c737"
                },
                {
                    "angle": -34.8512953929681,
                    "magnitude": 7703.51857547293,
                    "measurement_mrid": "_b1cf0e65-e6ce-4e69-bb39-ed9e8f9516bd"
                },
                {
                    "angle": -35.7417055146847,
                    "magnitude": 8311.01014105113,
                    "measurement_mrid": "_160a1b58-a0c0-47d0-9cd4-8141cdd1f18a"
                },
                {
                    "angle": 86.4785515015816,
                    "magnitude": 7321.42783280868,
                    "measurement_mrid": "_423f52b8-36a6-48d0-8efc-54a509d086d9"
                },
                {
                    "angle": 86.4791158020503,
                    "magnitude": 7325.78734479697,
                    "measurement_mrid": "_86f258a7-f129-4c5d-b054-e3405d974fb9"
                },
                {
                    "angle": -35.693913690976,
                    "magnitude": 8266.70674940136,
                    "measurement_mrid": "_ada28217-17c6-4db2-a423-fcb7f6ab4a69"
                },
                {
                    "angle": -156.12929865563,
                    "magnitude": 7980.9546163902,
                    "measurement_mrid": "_fe31b323-c57d-43e6-85ce-5255191ac5b5"
                },
                {
                    "angle": -156.228691801794,
                    "magnitude": 128.142239041335,
                    "measurement_mrid": "_8dc33aef-bc09-46d1-947f-940640282071"
                },
                {
                    "angle": -156.189489611409,
                    "magnitude": 127.362664491121,
                    "measurement_mrid": "_e9cf39e7-fe03-46fe-9868-d56eb6b9f7cb"
                },
                {
                    "angle": 86.338664500863,
                    "magnitude": 7332.67492936433,
                    "measurement_mrid": "_c00c15dc-0060-4f64-a876-3ac4dda4777b"
                },
                {
                    "angle": -153.171172480246,
                    "magnitude": 7319.81987282722,
                    "measurement_mrid": "_cbf89143-b758-4362-ab54-8dc8e535290d"
                },
                {
                    "angle": -33.3787809107131,
                    "magnitude": 121.07130649223,
                    "measurement_mrid": "_a7066933-4a37-4052-9bff-00f91aef42b3"
                },
                {
                    "angle": -33.3410131155074,
                    "magnitude": 120.360646402173,
                    "measurement_mrid": "_dbe3baf7-5c62-447b-b061-b45201a35df5"
                },
                {
                    "angle": -34.0768494189005,
                    "magnitude": 120.65989287548,
                    "measurement_mrid": "_bc3a0f92-f9fd-4de4-852b-316c559159fb"
                },
                {
                    "angle": -34.0768494189005,
                    "magnitude": 120.65989287548,
                    "measurement_mrid": "_f8d54628-1d0b-4431-9a6b-8cd467f2473e"
                },
                {
                    "angle": -154.284027933448,
                    "magnitude": 120.679025680752,
                    "measurement_mrid": "_129c07ce-a988-4c08-9206-5451dae895bc"
                },
                {
                    "angle": -154.284027933448,
                    "magnitude": 120.679025680752,
                    "measurement_mrid": "_841d965f-eaee-4d86-926e-916edd9056e8"
                },
                {
                    "angle": -154.652670954451,
                    "magnitude": 7295.84228568178,
                    "measurement_mrid": "_85dc0aa9-10be-4d19-a6b9-28a65c0ca257"
                },
                {
                    "angle": 87.1569508337196,
                    "magnitude": 7325.45783796256,
                    "measurement_mrid": "_8b4eda15-ec14-4300-b37e-d5bdc3777480"
                },
                {
                    "angle": -34.3372454456532,
                    "magnitude": 7216.61978737616,
                    "measurement_mrid": "_ed82d053-e9a9-4b2d-94db-d9b73e99c238"
                },
                {
                    "angle": -35.9522866802046,
                    "magnitude": 138.233559844677,
                    "measurement_mrid": "_92fe0d14-0ce3-4a9e-8b0d-eb4d9ddfe75a"
                },
                {
                    "angle": -35.9654723627476,
                    "magnitude": 138.517822858351,
                    "measurement_mrid": "_9d54eac3-0cc0-4880-bd36-f01a6987a0ee"
                },
                {
                    "angle": -35.274102991945,
                    "magnitude": 127.981112775145,
                    "measurement_mrid": "_5897f2be-a161-4fcb-9180-79fef89997f6"
                },
                {
                    "angle": -35.288349077534,
                    "magnitude": 128.265374047613,
                    "measurement_mrid": "_61eb953f-1d86-4354-b166-eb40ec3e7ba0"
                },
                {
                    "angle": -156.453165473906,
                    "magnitude": 7946.31975176775,
                    "measurement_mrid": "_39a12353-6989-4de5-b8e5-c42467af20c2"
                },
                {
                    "angle": 85.6953671126513,
                    "magnitude": 121.481148112775,
                    "measurement_mrid": "_219d8a6c-a824-4a49-bfe4-4c03d0d7e188"
                },
                {
                    "angle": 85.7241823152923,
                    "magnitude": 120.937746201463,
                    "measurement_mrid": "_bd4257ed-3a7e-4f80-9874-76f7ea4da4f4"
                },
                {
                    "angle": 88.2792934421309,
                    "magnitude": 7297.68721830376,
                    "measurement_mrid": "_b1dd9f67-fc56-41af-b799-f092324d08a5"
                },
                {
                    "angle": 87.5576854930381,
                    "magnitude": 7311.26947828574,
                    "measurement_mrid": "_61cbe0f0-4259-44e9-a050-a5878d82461b"
                },
                {
                    "angle": -33.3263749756792,
                    "magnitude": 7274.27251165573,
                    "measurement_mrid": "_90a5c113-a1eb-41a3-a513-c2828c8f2129"
                },
                {
                    "angle": -153.509068135871,
                    "magnitude": 7308.23389498903,
                    "measurement_mrid": "_feada251-a910-456e-8376-e932adb2c68b"
                },
                {
                    "angle": -155.743684424223,
                    "magnitude": 7729.61572471008,
                    "measurement_mrid": "_9f783a4d-871d-4399-a940-dd5f5419865c"
                },
                {
                    "angle": -36.1766081025856,
                    "magnitude": 137.297282032569,
                    "measurement_mrid": "_4d401b5b-502c-4305-9622-2c29ba204ebf"
                },
                {
                    "angle": -36.1766081025856,
                    "magnitude": 137.297282032569,
                    "measurement_mrid": "_6e325375-b163-4851-a798-26faac90327f"
                },
                {
                    "angle": -36.0904337894047,
                    "magnitude": 136.793853335101,
                    "measurement_mrid": "_69fd5846-38e8-4623-b042-2388a8624714"
                },
                {
                    "angle": -36.0904337894047,
                    "magnitude": 136.793853335101,
                    "measurement_mrid": "_fc71710d-b350-4e0d-a3c2-dc9c2e00dd49"
                },
                {
                    "angle": -156.914116636901,
                    "magnitude": 129.880525851017,
                    "measurement_mrid": "_317f735c-81e7-4bd0-865e-d331f71ae002"
                },
                {
                    "angle": -156.939806309193,
                    "magnitude": 130.400413764563,
                    "measurement_mrid": "_68cf1254-8ac6-49df-a4f5-1239df6a610e"
                },
                {
                    "angle": -32.9739425770388,
                    "magnitude": 7330.87798304497,
                    "measurement_mrid": "_255536e7-66e4-498e-ac60-0acad3cc571d"
                },
                {
                    "angle": -153.059077434488,
                    "magnitude": 7318.72321641929,
                    "measurement_mrid": "_c339ace1-67b3-4fd3-bedf-8e36cc99e6cb"
                },
                {
                    "angle": 87.4404707647893,
                    "magnitude": 7302.3079702354,
                    "measurement_mrid": "_cc485283-dd4e-4b6a-b254-eb29e7ae8bb0"
                },
                {
                    "angle": -152.950089531662,
                    "magnitude": 7319.5661577401,
                    "measurement_mrid": "_0c48ecbd-5d4b-4772-9523-1e176f5bca09"
                },
                {
                    "angle": -36.1156494613281,
                    "magnitude": 136.579271606597,
                    "measurement_mrid": "_72b21f91-5d55-42fa-8247-8e4a3a3ac5fb"
                },
                {
                    "angle": -36.1156494613281,
                    "magnitude": 136.579271606597,
                    "measurement_mrid": "_c48e8eb4-ada9-438e-b0ef-7c107af8f448"
                },
                {
                    "angle": -34.1575603670672,
                    "magnitude": 119.512171263024,
                    "measurement_mrid": "_c3a71cf9-453e-42cc-bc2a-9b956f2eade0"
                },
                {
                    "angle": -34.1955795172862,
                    "magnitude": 120.222834176034,
                    "measurement_mrid": "_f82608c0-a7c9-40f5-8255-17c0f222a238"
                },
                {
                    "angle": -32.1260116865731,
                    "magnitude": 120.794680916036,
                    "measurement_mrid": "_aca01a9e-5906-4510-86e4-925081d3d435"
                },
                {
                    "angle": -32.1511732380422,
                    "magnitude": 121.268622820171,
                    "measurement_mrid": "_dc711c7f-8649-4e9c-8014-4ca52e0891b0"
                },
                {
                    "angle": -155.769290471628,
                    "magnitude": 125.696892865345,
                    "measurement_mrid": "_1d7f5895-aa32-47c8-a42a-a994e86c258f"
                },
                {
                    "angle": -155.785224017585,
                    "magnitude": 126.008935447731,
                    "measurement_mrid": "_e4a01a47-15ee-4055-8794-79c77f2cacdf"
                },
                {
                    "angle": -156.913916004319,
                    "magnitude": 130.207029667753,
                    "measurement_mrid": "_30e5c53f-9c16-44c3-95a0-e3ba64ceafe9"
                },
                {
                    "angle": -156.913916004319,
                    "magnitude": 130.207029667753,
                    "measurement_mrid": "_882b48e6-79b5-4440-8ee4-42810646e4b9"
                },
                {
                    "angle": 86.4474456973881,
                    "magnitude": 7355.36489428815,
                    "measurement_mrid": "_f28f86c4-5a4f-4164-9087-84c2c5dfae62"
                },
                {
                    "angle": -35.7461889710931,
                    "magnitude": 8308.51709692676,
                    "measurement_mrid": "_b3fed364-52af-4140-b191-83195736c591"
                },
                {
                    "angle": -34.8406902502649,
                    "magnitude": 7710.72535182962,
                    "measurement_mrid": "_71cbb064-4faa-445c-9a64-075fb26da9c0"
                },
                {
                    "angle": -156.132046974442,
                    "magnitude": 7981.65900152229,
                    "measurement_mrid": "_5a6e19e7-e8c4-4a56-9b2d-ad17821926f5"
                },
                {
                    "angle": -35.6833698800999,
                    "magnitude": 8273.47236507454,
                    "measurement_mrid": "_7b8b7738-2833-4aa7-a29b-a96f44a786b4"
                },
                {
                    "angle": 86.4752792739434,
                    "magnitude": 7330.49104778831,
                    "measurement_mrid": "_7ba0418a-4535-4fbf-942b-59eed066837a"
                },
                {
                    "angle": -156.431143547962,
                    "magnitude": 7886.53540927523,
                    "measurement_mrid": "_b781d415-6607-4550-b6af-bc378ad652cf"
                },
                {
                    "angle": -156.922085851024,
                    "magnitude": 130.878926927228,
                    "measurement_mrid": "_2ded48e3-0910-4d9d-9b1b-a88d6453dc37"
                },
                {
                    "angle": -156.947583616481,
                    "magnitude": 131.39881384842,
                    "measurement_mrid": "_47b3a6f6-f5ba-4f09-b301-747b0975de4f"
                },
                {
                    "angle": 87.2502133185534,
                    "magnitude": 7266.1220054216,
                    "measurement_mrid": "_5e0b9faa-09a9-4202-a310-5c1ad42040b2"
                },
                {
                    "angle": 87.230067322369,
                    "magnitude": 7256.17857088229,
                    "measurement_mrid": "_38aa480a-df5a-4c96-8a6a-1af05cf58bc1"
                },
                {
                    "angle": -156.126945331259,
                    "magnitude": 7980.08603961477,
                    "measurement_mrid": "_c4f339b9-88fc-4c7b-988b-707f5f6e7475"
                },
                {
                    "angle": 85.587662573728,
                    "magnitude": 120.928143707348,
                    "measurement_mrid": "_40af84d4-75ef-4f26-85cb-8d7d0d34c12f"
                },
                {
                    "angle": 85.587662573728,
                    "magnitude": 120.928143707348,
                    "measurement_mrid": "_942250db-dbad-42e4-80be-a27630048265"
                },
                {
                    "angle": -155.726112415831,
                    "magnitude": 7738.89170228993,
                    "measurement_mrid": "_2555a9d4-95e7-4779-9669-a05f681cee1c"
                },
                {
                    "angle": -35.6141448133757,
                    "magnitude": 8321.76463308175,
                    "measurement_mrid": "_4d042ad2-650a-4472-bbc5-a3ed3c6621aa"
                },
                {
                    "angle": -36.0190598613043,
                    "magnitude": 137.849990670723,
                    "measurement_mrid": "_000014c6-137b-4a82-b579-2d85573163ba"
                },
                {
                    "angle": -36.0058119568473,
                    "magnitude": 137.565727932587,
                    "measurement_mrid": "_3fe500c7-e8c5-4f42-b98f-18ebc550929f"
                },
                {
                    "angle": -35.5722644576676,
                    "magnitude": 8331.54714328177,
                    "measurement_mrid": "_0ac5df71-54f1-4f72-b862-30aa6c9c935e"
                },
                {
                    "angle": -36.1134527075622,
                    "magnitude": 136.600383879211,
                    "measurement_mrid": "_22ccd304-0659-4597-9550-f0178d7078cf"
                },
                {
                    "angle": -36.1134527075622,
                    "magnitude": 136.600383879211,
                    "measurement_mrid": "_625d36ee-5386-4cc0-a239-eb3fe41fdb61"
                },
                {
                    "angle": -156.945802613213,
                    "magnitude": 130.532088074868,
                    "measurement_mrid": "_a3fd0f1a-12da-47c5-9205-f8b8af691703"
                },
                {
                    "angle": -156.907320140831,
                    "magnitude": 129.752512253447,
                    "measurement_mrid": "_ec9aa13a-de75-4f6d-85b5-002909d39b05"
                },
                {
                    "angle": -155.72310286905,
                    "magnitude": 7740.48575711715,
                    "measurement_mrid": "_8de94525-2520-4a30-b473-21b4665287c7"
                },
                {
                    "angle": -154.592955958989,
                    "magnitude": 128.293192136867,
                    "measurement_mrid": "_66c5033c-4d6f-4cff-b88d-2e60a3fda0ed"
                },
                {
                    "angle": -154.608579277714,
                    "magnitude": 128.605231360401,
                    "measurement_mrid": "_89509924-3c4d-410b-a567-309bc348ae28"
                },
                {
                    "angle": -36.2895135823956,
                    "magnitude": 136.482456508148,
                    "measurement_mrid": "_3cebc735-aa24-47b3-b57a-5923abecc367"
                },
                {
                    "angle": -36.2672115309813,
                    "magnitude": 136.008501152994,
                    "measurement_mrid": "_d9e2d5dc-cc04-4c9b-9f85-5603807b9891"
                },
                {
                    "angle": -35.5915048867775,
                    "magnitude": 8312.28262683302,
                    "measurement_mrid": "_b9ded100-a4a5-4ad8-84f0-08f8d1abf55d"
                },
                {
                    "angle": 85.871998862774,
                    "magnitude": 121.900014506765,
                    "measurement_mrid": "_98522cc0-5232-4015-a3e4-38984afceb18"
                },
                {
                    "angle": 85.9007155566393,
                    "magnitude": 121.356613564732,
                    "measurement_mrid": "_f63d95cf-6996-4f7e-90f2-1771e847bca1"
                },
                {
                    "angle": -35.8658919740096,
                    "magnitude": 8237.40130299065,
                    "measurement_mrid": "_229553be-a221-4037-a7b5-4c8618f94fac"
                },
                {
                    "angle": -35.7993088512337,
                    "magnitude": 8284.49064896876,
                    "measurement_mrid": "_751f3a0e-ea4a-44b7-8a64-56826278fe17"
                },
                {
                    "angle": -156.428292247924,
                    "magnitude": 7873.94104919438,
                    "measurement_mrid": "_cc954157-7900-4624-83d5-e8d1e6b28464"
                },
                {
                    "angle": 85.6327988347996,
                    "magnitude": 120.126114393855,
                    "measurement_mrid": "_43b29f67-4b11-44e7-94d5-8e0c94fa65de"
                },
                {
                    "angle": 85.5465231786458,
                    "magnitude": 121.756946224727,
                    "measurement_mrid": "_9131c1fb-4006-4bef-8c86-c580ef621dc2"
                },
                {
                    "angle": -155.705570690026,
                    "magnitude": 7749.75864867915,
                    "measurement_mrid": "_db6b52a5-03be-48d2-a010-a1609b76a684"
                },
                {
                    "angle": 87.2362848426925,
                    "magnitude": 120.394752372683,
                    "measurement_mrid": "_600e5a2d-369f-4221-bda6-5282385aa3db"
                },
                {
                    "angle": 87.2073387563756,
                    "magnitude": 120.938153833308,
                    "measurement_mrid": "_c78cb6b8-a7dc-420f-a80e-0b419590d544"
                },
                {
                    "angle": -156.426771891999,
                    "magnitude": 7875.13926639065,
                    "measurement_mrid": "_663dd641-b4cc-43db-8424-b15cdaf80143"
                },
                {
                    "angle": 85.8036847434855,
                    "magnitude": 121.368831362182,
                    "measurement_mrid": "_09ed4736-42da-4410-882f-c651df1419a8"
                },
                {
                    "angle": 85.8036847434855,
                    "magnitude": 121.368831362182,
                    "measurement_mrid": "_72f2fba9-4857-43f0-8959-6b27e8e959bf"
                },
                {
                    "angle": -155.74561662478,
                    "magnitude": 7728.59083273955,
                    "measurement_mrid": "_c7ad6bb0-8c9e-4899-b899-d6234a192ac0"
                },
                {
                    "angle": -156.57581230108,
                    "magnitude": 131.980089138709,
                    "measurement_mrid": "_2657d79f-a50c-497b-b237-500da0b53c62"
                },
                {
                    "angle": -156.57581230108,
                    "magnitude": 131.980089138709,
                    "measurement_mrid": "_9c73f433-634c-465d-843c-3f2eab6fdd67"
                },
                {
                    "angle": 87.4662714963758,
                    "magnitude": 7313.84420589024,
                    "measurement_mrid": "_304cdf54-ca02-474a-b7bc-7af3f2071ae1"
                },
                {
                    "angle": 86.790792614636,
                    "magnitude": 120.433115521741,
                    "measurement_mrid": "_76878191-7c09-4c94-8ca2-4c52e430a303"
                },
                {
                    "angle": 86.790792614636,
                    "magnitude": 120.433115521741,
                    "measurement_mrid": "_a1decae3-866e-4cf2-8fac-346b23c34694"
                },
                {
                    "angle": -35.8619337326468,
                    "magnitude": 8239.59799487713,
                    "measurement_mrid": "_b3a74970-3f6e-4094-b4c2-0438f196f109"
                },
                {
                    "angle": 86.7183189723894,
                    "magnitude": 119.632642156807,
                    "measurement_mrid": "_3c18ed2f-4f81-4d79-98a7-0d8d6f0ceb64"
                },
                {
                    "angle": 86.7008149830115,
                    "magnitude": 119.958572101468,
                    "measurement_mrid": "_dc620ca2-e332-4404-9f75-bd2323e9a5a1"
                },
                {
                    "angle": -35.9653160427094,
                    "magnitude": 138.216689694888,
                    "measurement_mrid": "_18e4b20e-f0ce-4ffe-9cdf-f58bbcead4ca"
                },
                {
                    "angle": -35.9741215722044,
                    "magnitude": 138.406375757316,
                    "measurement_mrid": "_f2b95156-1594-4c47-b54c-39f3de6ea8d0"
                },
                {
                    "angle": -156.895581629292,
                    "magnitude": 131.404119559112,
                    "measurement_mrid": "_636acd0e-a07d-4a92-b17e-516e8ecc8b6a"
                },
                {
                    "angle": -156.905759151255,
                    "magnitude": 131.611964588846,
                    "measurement_mrid": "_7bdba3ea-8371-416d-bcf6-547bfcc6c325"
                },
                {
                    "angle": -156.451447401227,
                    "magnitude": 7877.66172076848,
                    "measurement_mrid": "_7a34bbcd-6c7a-40e0-8308-bd360f509d05"
                },
                {
                    "angle": -156.858725588292,
                    "magnitude": 130.613048982067,
                    "measurement_mrid": "_329a2642-c25d-4dfe-a4a3-39a1ca53c7d6"
                },
                {
                    "angle": -156.843331407135,
                    "magnitude": 130.301011969601,
                    "measurement_mrid": "_95df48e6-b519-47f3-9a3c-634461786dd3"
                },
                {
                    "angle": 85.7491760942168,
                    "magnitude": 122.363351980165,
                    "measurement_mrid": "_3de8e502-b13c-4274-8ef2-3a2de67441a0"
                },
                {
                    "angle": 85.7491760942168,
                    "magnitude": 122.363351980165,
                    "measurement_mrid": "_79bb0571-44bd-4ad0-9a2b-620755a7fe29"
                },
                {
                    "angle": 88.8830613283238,
                    "magnitude": 7222.26529008854,
                    "measurement_mrid": "_93aa033e-8644-446d-b93e-1e79497daacb"
                },
                {
                    "angle": -156.393244226859,
                    "magnitude": 7892.69605737817,
                    "measurement_mrid": "_ad4e5c30-8335-41e1-b66e-d87ba2396a8e"
                },
                {
                    "angle": -156.393820251679,
                    "magnitude": 7892.55370999947,
                    "measurement_mrid": "_d1a2c329-b511-4b6d-a934-ac05f998b361"
                },
                {
                    "angle": 86.4737363645068,
                    "magnitude": 7317.67165971374,
                    "measurement_mrid": "_5cbdc0ff-2341-49f6-86d4-11800ea7719c"
                },
                {
                    "angle": -156.118679808372,
                    "magnitude": 7980.94264801818,
                    "measurement_mrid": "_6d92c5f3-1d17-4962-949c-7fb276973d38"
                },
                {
                    "angle": -35.7109245713538,
                    "magnitude": 8261.06390896486,
                    "measurement_mrid": "_6fbe7ac4-f040-4be9-8b37-c6e5da07dd86"
                },
                {
                    "angle": -35.7597664045193,
                    "magnitude": 131.497468620813,
                    "measurement_mrid": "_7289ef0b-58ce-49ff-bc21-42a261485180"
                },
                {
                    "angle": -35.7597664045193,
                    "magnitude": 131.497468620813,
                    "measurement_mrid": "_bcd6ffbe-83a9-4224-9ad2-7ef732f86f54"
                },
                {
                    "angle": -153.535185031518,
                    "magnitude": 120.915424966098,
                    "measurement_mrid": "_71575a4b-7ef8-4482-8e00-9e014c9bf8a2"
                },
                {
                    "angle": -153.535185031518,
                    "magnitude": 120.915424966098,
                    "measurement_mrid": "_b070b8fb-d76d-43ed-a9ad-892b120833cb"
                },
                {
                    "angle": -31.9448315857521,
                    "magnitude": 121.09688020192,
                    "measurement_mrid": "_1ccdbb38-d19b-440f-b4ac-22c67694287e"
                },
                {
                    "angle": -31.9448315857521,
                    "magnitude": 121.09688020192,
                    "measurement_mrid": "_d689a383-7d4f-4f08-af2d-ea63b8e453fc"
                },
                {
                    "angle": -35.6973634982083,
                    "magnitude": 8265.08253114011,
                    "measurement_mrid": "_a8dcc195-0457-429f-89b1-e7820d7fb87f"
                },
                {
                    "angle": 86.5279878563285,
                    "magnitude": 7415.96628758313,
                    "measurement_mrid": "_6d753f23-5193-43d3-a25f-f3906d6e2322"
                },
                {
                    "angle": -35.4334372364592,
                    "magnitude": 8397.37098966342,
                    "measurement_mrid": "_79164559-bec7-4074-a32f-0378aa4b089c"
                },
                {
                    "angle": -155.999707657775,
                    "magnitude": 8038.61246338996,
                    "measurement_mrid": "_97f1bfb0-59ab-46d3-9b89-3dc88c64f279"
                },
                {
                    "angle": -34.2267689299051,
                    "magnitude": 7221.92712121118,
                    "measurement_mrid": "_9d01d36b-9d84-4fb6-8a5e-8cd19a70d729"
                },
                {
                    "angle": 87.2081541408372,
                    "magnitude": 7323.58628772446,
                    "measurement_mrid": "_bc575fc2-a353-4135-bfd6-f381aff55a9d"
                },
                {
                    "angle": -154.523432234095,
                    "magnitude": 7297.26642986552,
                    "measurement_mrid": "_fcdba4d8-9215-4b20-99a9-3e64feab9428"
                },
                {
                    "angle": -34.2273825474473,
                    "magnitude": 7221.62502365769,
                    "measurement_mrid": "_c6578f52-482c-49fc-bc1d-d5e0efaa5d95"
                },
                {
                    "angle": -34.230492188333,
                    "magnitude": 7220.11401849111,
                    "measurement_mrid": "_2e155dc7-d144-44f6-a5d0-4048beb2e23b"
                },
                {
                    "angle": -154.510047055621,
                    "magnitude": 7297.36161619826,
                    "measurement_mrid": "_0b92a151-da08-4d7a-a8f9-4efd47b1e125"
                },
                {
                    "angle": 87.2130118167679,
                    "magnitude": 7323.41062611946,
                    "measurement_mrid": "_347e8fca-9c09-40bf-a0f0-5cb72d4561bb"
                },
                {
                    "angle": -34.2146357091557,
                    "magnitude": 7222.55260835138,
                    "measurement_mrid": "_e265e742-8338-46a4-bd1b-2986b7d58925"
                },
                {
                    "angle": -34.229129574737,
                    "magnitude": 7220.76547417432,
                    "measurement_mrid": "_58da73a1-6351-4e41-ae9f-3d817abd1eb1"
                },
                {
                    "angle": 85.814296408393,
                    "magnitude": 121.391703598991,
                    "measurement_mrid": "_76287cbc-6a0f-4284-a045-8644393d60bb"
                },
                {
                    "angle": 85.8431322248951,
                    "magnitude": 120.84830120681,
                    "measurement_mrid": "_cbfa944f-1bca-4696-a4bb-786fe8c43c2f"
                },
                {
                    "angle": -152.828226448762,
                    "magnitude": 7321.35907842657,
                    "measurement_mrid": "_82bb6fbd-9247-42bb-9281-b3fa7ab7275f"
                },
                {
                    "angle": -32.7363173124997,
                    "magnitude": 7310.535801218,
                    "measurement_mrid": "_a5694d33-9178-407a-a5d0-995ce77d1b13"
                },
                {
                    "angle": 87.824303207031,
                    "magnitude": 7306.16109804968,
                    "measurement_mrid": "_eb0eb10b-5288-438f-a60c-2f73eb96cd92"
                },
                {
                    "angle": -153.049838673423,
                    "magnitude": 7316.57378100033,
                    "measurement_mrid": "_297388f3-226d-405f-9b63-8e0867ff8b24"
                },
                {
                    "angle": 87.0181250724063,
                    "magnitude": 7377.61259502117,
                    "measurement_mrid": "_b1295b7c-866d-4ddb-9825-96ab21134686"
                },
                {
                    "angle": -156.50239990435,
                    "magnitude": 7922.09925023716,
                    "measurement_mrid": "_16b9206e-f66e-496c-ae4e-aa9afb4e1e3f"
                },
                {
                    "angle": -153.531670450446,
                    "magnitude": 120.941402520105,
                    "measurement_mrid": "_4f07496f-8ee7-44f3-9ce8-a38e5ef3e4e4"
                },
                {
                    "angle": -153.531670450446,
                    "magnitude": 120.941402520105,
                    "measurement_mrid": "_e82b15cc-644c-4d55-992c-04deb321b5db"
                },
                {
                    "angle": 85.8356229559285,
                    "magnitude": 121.153034889645,
                    "measurement_mrid": "_63a7ab27-0193-43ec-84f6-8aec4a7ba831"
                },
                {
                    "angle": 85.8356229559285,
                    "magnitude": 121.153034889645,
                    "measurement_mrid": "_df477b9c-250d-462d-8247-edaab4cba2be"
                },
                {
                    "angle": 87.682047719092,
                    "magnitude": 7308.27214496893,
                    "measurement_mrid": "_0f21488d-c2ed-43e9-9a10-a28d7791fb94"
                },
                {
                    "angle": -156.498632450574,
                    "magnitude": 7924.13348863298,
                    "measurement_mrid": "_1ebef15d-ad9d-481f-be46-3270043550eb"
                },
                {
                    "angle": -34.7970349043853,
                    "magnitude": 128.953971254158,
                    "measurement_mrid": "_803ea0c3-11fd-46fa-958b-6b9a14892385"
                },
                {
                    "angle": -34.7734035329276,
                    "magnitude": 128.480022744806,
                    "measurement_mrid": "_8a8d07b4-330d-4ff8-af90-100b1afe8f86"
                },
                {
                    "angle": 87.1689499880168,
                    "magnitude": 120.387016214245,
                    "measurement_mrid": "_89cb9c25-fc82-4936-bbc0-4ccae4712d42"
                },
                {
                    "angle": 87.1400022033994,
                    "magnitude": 120.93041754393,
                    "measurement_mrid": "_eab8b26a-165a-4903-917c-cd5c3f3c131f"
                },
                {
                    "angle": -155.580334353393,
                    "magnitude": 127.343146473489,
                    "measurement_mrid": "_87ebf6ae-585c-4411-b035-dd096336e737"
                },
                {
                    "angle": -155.580334353393,
                    "magnitude": 127.343146473489,
                    "measurement_mrid": "_9a5f9baa-1579-4688-9ba5-d4674636e05d"
                },
                {
                    "angle": 86.6377299714394,
                    "magnitude": 121.475439870943,
                    "measurement_mrid": "_1254cc48-c4bf-4e0a-ad86-21aa49dc2776"
                },
                {
                    "angle": 86.609040421518,
                    "magnitude": 122.018840861455,
                    "measurement_mrid": "_fe48fb1d-8faf-417e-8abd-0193acfe8016"
                },
                {
                    "angle": 86.6233531696904,
                    "magnitude": 121.747136051414,
                    "measurement_mrid": "_811076c2-624c-4602-9764-254a6374bb00"
                },
                {
                    "angle": 86.6233531696904,
                    "magnitude": 121.747136051414,
                    "measurement_mrid": "_d393625c-7a03-45b8-914b-3ab33ba3136f"
                },
                {
                    "angle": -153.049683470816,
                    "magnitude": 7316.61908204754,
                    "measurement_mrid": "_b06976f8-1d11-401d-a24e-6543569b45b1"
                },
                {
                    "angle": -35.5787314763774,
                    "magnitude": 8334.26547827412,
                    "measurement_mrid": "_efaa5d0b-67dd-4b01-8a44-895b7f792035"
                },
                {
                    "angle": 86.4262013025362,
                    "magnitude": 7387.31834041598,
                    "measurement_mrid": "_7258d92e-ad06-4c65-9bb9-7cfb56248268"
                },
                {
                    "angle": -156.25206496767,
                    "magnitude": 7968.38836230335,
                    "measurement_mrid": "_b2caf253-476b-4751-a993-041e4639f551"
                },
                {
                    "angle": -35.5786241921887,
                    "magnitude": 8334.30100355422,
                    "measurement_mrid": "_f79075f4-81a1-4164-ae0f-97960e4b42b2"
                },
                {
                    "angle": -154.225166484566,
                    "magnitude": 120.700167183931,
                    "measurement_mrid": "_2e80a749-ab5b-46ff-bbe9-975e0e162d88"
                },
                {
                    "angle": -154.225166484566,
                    "magnitude": 120.700167183931,
                    "measurement_mrid": "_66e76a36-63ff-46dd-bc14-04465189afda"
                },
                {
                    "angle": -156.389096424557,
                    "magnitude": 7909.45049876697,
                    "measurement_mrid": "_e6ccf802-051d-40ba-8c19-f62e24e0e8a1"
                },
                {
                    "angle": -33.0467125684258,
                    "magnitude": 7338.09413243614,
                    "measurement_mrid": "_37c27fdb-efea-4b51-8f9c-10005c576b2d"
                },
                {
                    "angle": 87.3220656143656,
                    "magnitude": 7301.00246515419,
                    "measurement_mrid": "_48504f4e-e8e3-4c31-b95a-c0a3c91317f2"
                },
                {
                    "angle": -153.120711754759,
                    "magnitude": 7318.88731556374,
                    "measurement_mrid": "_c66cabe0-bc43-48a9-8720-ce2d26540829"
                },
                {
                    "angle": 86.6830391474688,
                    "magnitude": 119.587142439713,
                    "measurement_mrid": "_7d731b5e-7695-4cd0-9c40-df8441e46915"
                },
                {
                    "angle": 86.6830391474688,
                    "magnitude": 119.587142439713,
                    "measurement_mrid": "_bddf747b-045b-402d-87e8-ac9642b9ccd7"
                },
                {
                    "angle": -36.2715277665617,
                    "magnitude": 136.458596911231,
                    "measurement_mrid": "_0f29d9e7-0877-4a76-ab65-5ee067960487"
                },
                {
                    "angle": -36.2581488959793,
                    "magnitude": 136.174333192925,
                    "measurement_mrid": "_6e57d755-f42f-4f42-9613-cb3b0316a298"
                },
                {
                    "angle": 87.2232882821818,
                    "magnitude": 7252.82533141332,
                    "measurement_mrid": "_47110fe8-fb92-4404-8c2b-ab25fb39234a"
                },
                {
                    "angle": -35.7196725322338,
                    "magnitude": 8252.74870470661,
                    "measurement_mrid": "_1d8d53cc-1206-48d4-bd82-6376afd9e386"
                },
                {
                    "angle": -155.778487716794,
                    "magnitude": 126.214397316761,
                    "measurement_mrid": "_6a063ce4-3a00-4176-a47a-8eee838dc10b"
                },
                {
                    "angle": -155.751984201841,
                    "magnitude": 125.694500066829,
                    "measurement_mrid": "_f6603449-191f-4632-aa21-f6543c19142e"
                },
                {
                    "angle": -36.0090481857758,
                    "magnitude": 137.855331061346,
                    "measurement_mrid": "_6d813dbd-0293-4cba-a243-eb3665144683"
                },
                {
                    "angle": -35.9958012357963,
                    "magnitude": 137.571068722441,
                    "measurement_mrid": "_76c5edc5-8e26-4485-8181-de0e7e03b5b8"
                },
                {
                    "angle": 87.0030220836857,
                    "magnitude": 120.222729367322,
                    "measurement_mrid": "_a042ffad-17be-464d-8449-d708a4249ce3"
                },
                {
                    "angle": 86.9596242976011,
                    "magnitude": 121.038110489666,
                    "measurement_mrid": "_b20a9f26-72c9-4010-b132-b8e774dfad2d"
                },
                {
                    "angle": -154.34484436785,
                    "magnitude": 119.88541864269,
                    "measurement_mrid": "_039d0dbd-685a-4805-bffb-5c4fc5578ef5"
                },
                {
                    "angle": -154.427555764892,
                    "magnitude": 121.444639040295,
                    "measurement_mrid": "_9276b40e-6a80-4023-9b9c-f5335a3156d3"
                },
                {
                    "angle": -33.3102613359148,
                    "magnitude": 120.908387290897,
                    "measurement_mrid": "_5e9114da-1b78-46c2-ad5c-83c226cf52cc"
                },
                {
                    "angle": -33.3253538847277,
                    "magnitude": 121.192644426654,
                    "measurement_mrid": "_9a07a1ab-0880-42ca-9e95-9f995a9fe363"
                },
                {
                    "angle": -35.9734024963268,
                    "magnitude": 137.851106954659,
                    "measurement_mrid": "_3ba98227-c3da-417d-aa47-763b7b625ad9"
                },
                {
                    "angle": -35.9954156988321,
                    "magnitude": 138.325059665484,
                    "measurement_mrid": "_3bb9252f-1b68-466a-a7d6-85d7150cfdd3"
                },
                {
                    "angle": -34.0679376049164,
                    "magnitude": 119.228851587938,
                    "measurement_mrid": "_35f39403-a012-4a97-b6c0-9dd746be02f2"
                },
                {
                    "angle": -34.1437046983367,
                    "magnitude": 120.650231622438,
                    "measurement_mrid": "_79b96051-6ce2-42bb-9290-d237d72fa0b7"
                },
                {
                    "angle": 85.7677356688296,
                    "magnitude": 121.231506948905,
                    "measurement_mrid": "_e9003075-1139-4c90-8323-3661cc1d4bae"
                },
                {
                    "angle": 85.7677356688296,
                    "magnitude": 121.231506948905,
                    "measurement_mrid": "_f3f2102a-3168-438e-af8f-b73b6a874d96"
                },
                {
                    "angle": 87.5281929513254,
                    "magnitude": 7311.78399217514,
                    "measurement_mrid": "_78ae6cd8-2df0-447c-8cdf-87063bae2e67"
                },
                {
                    "angle": -156.197077190735,
                    "magnitude": 127.856007532844,
                    "measurement_mrid": "_42cbc266-e63a-4893-b607-9b3a6eefebe3"
                },
                {
                    "angle": -156.197077190735,
                    "magnitude": 127.856007532844,
                    "measurement_mrid": "_afc76b37-cfe4-4c15-beef-1aa477545492"
                },
                {
                    "angle": -156.20207205683,
                    "magnitude": 128.55410583044,
                    "measurement_mrid": "_0a56578f-16ee-4349-8889-dd6627ebb966"
                },
                {
                    "angle": -156.149978350741,
                    "magnitude": 127.514837635434,
                    "measurement_mrid": "_60e8b0f1-a7a3-438d-ba3a-0952ceaa5183"
                },
                {
                    "angle": -156.221226674921,
                    "magnitude": 128.021229264219,
                    "measurement_mrid": "_3e092dd2-fb34-4849-aac5-bbcc9d0898f0"
                },
                {
                    "angle": -156.195057958635,
                    "magnitude": 127.501341937602,
                    "measurement_mrid": "_f187b21c-6225-46dd-8dee-8b1ee2dc24a3"
                },
                {
                    "angle": -156.852844991631,
                    "magnitude": 130.438368958344,
                    "measurement_mrid": "_7ceab293-ecea-4bc1-a646-e02ec3998981"
                },
                {
                    "angle": -156.852844991631,
                    "magnitude": 130.438368958344,
                    "measurement_mrid": "_b224fe1d-dc9c-491a-b9c4-df01b8622394"
                },
                {
                    "angle": -156.868512221862,
                    "magnitude": 130.676518547511,
                    "measurement_mrid": "_3bfe48fe-7eb2-49f2-8b62-3f5fc96397ee"
                },
                {
                    "angle": -156.842877230331,
                    "magnitude": 130.156630303155,
                    "measurement_mrid": "_cabf31db-26a8-43ed-97cb-ec5529db740e"
                },
                {
                    "angle": -156.208517864169,
                    "magnitude": 7997.74527500715,
                    "measurement_mrid": "_2c44089a-0d0c-4030-856b-43dc92baea0d"
                },
                {
                    "angle": -153.469566882766,
                    "magnitude": 121.172713970473,
                    "measurement_mrid": "_222d21ac-b2f3-4241-81e6-5f18f5a3ec2d"
                },
                {
                    "angle": -153.441928687462,
                    "magnitude": 120.652823043221,
                    "measurement_mrid": "_b76ac636-5472-4dff-8f2d-f9f9175f4450"
                },
                {
                    "angle": -153.255174814648,
                    "magnitude": 120.608892590988,
                    "measurement_mrid": "_61f95ec0-68f9-4598-9387-408e1f7c0a22"
                },
                {
                    "angle": -153.296545269279,
                    "magnitude": 121.388473271627,
                    "measurement_mrid": "_c6084805-d7d3-44f5-b66f-51eb57f5e709"
                },
                {
                    "angle": -33.3004619874248,
                    "magnitude": 120.683493490294,
                    "measurement_mrid": "_c9e8303c-358c-4562-b362-fdb9143d31ed"
                },
                {
                    "angle": -33.3381302138985,
                    "magnitude": 121.394152955357,
                    "measurement_mrid": "_e5bb801c-62a5-4a32-9fe0-6c933f09438e"
                },
                {
                    "angle": -156.605728152746,
                    "magnitude": 131.82462189137,
                    "measurement_mrid": "_10d01ea8-01b5-4b15-a451-f3af42948e31"
                },
                {
                    "angle": -156.620946775565,
                    "magnitude": 132.136658691847,
                    "measurement_mrid": "_5b88c6b7-5bc2-447a-a56c-642b9d6b55c6"
                },
                {
                    "angle": 88.3695177173191,
                    "magnitude": 118.957341589833,
                    "measurement_mrid": "_11774453-d942-460f-aa6a-1e0db3e0714d"
                },
                {
                    "angle": 88.3402253739494,
                    "magnitude": 119.500744563116,
                    "measurement_mrid": "_5a2fbd45-7564-4b25-b921-53ed7e0c5e9e"
                },
                {
                    "angle": -32.7369525422019,
                    "magnitude": 7310.2638637885,
                    "measurement_mrid": "_146bb954-8277-4e5d-86f1-ca372628077e"
                },
                {
                    "angle": 87.8062305703189,
                    "magnitude": 7306.37963963569,
                    "measurement_mrid": "_2209db46-d97a-407a-aec6-cd3e875c6672"
                },
                {
                    "angle": -32.7751115235176,
                    "magnitude": 7308.17958209003,
                    "measurement_mrid": "_8558ddd8-979f-45d8-8169-59fe9a8fa42f"
                },
                {
                    "angle": -152.871922693087,
                    "magnitude": 7320.4802790538,
                    "measurement_mrid": "_aadc5db7-3ebd-4fa1-98bd-8cb32907a35f"
                },
                {
                    "angle": -152.976107000425,
                    "magnitude": 7319.40708932158,
                    "measurement_mrid": "_61e00f91-6ac9-47f0-a749-8971c3e8b75b"
                },
                {
                    "angle": -32.8879460942593,
                    "magnitude": 7322.50911991697,
                    "measurement_mrid": "_b1950e2f-2018-4423-b5df-c05559534dd7"
                },
                {
                    "angle": 87.5856064322928,
                    "magnitude": 7303.56172377058,
                    "measurement_mrid": "_b3be03f8-cc46-4b0e-a579-d9e068b4eda1"
                },
                {
                    "angle": 87.1808520117653,
                    "magnitude": 7231.93348670183,
                    "measurement_mrid": "_45410209-8e20-4da3-b8c3-26aea501c9c8"
                },
                {
                    "angle": 87.2227967869808,
                    "magnitude": 7252.58492631421,
                    "measurement_mrid": "_b948c1b6-fe6c-44d6-b7e0-c10f6467f7bb"
                },
                {
                    "angle": -156.426786419825,
                    "magnitude": 7875.134725923,
                    "measurement_mrid": "_daf7c682-c65b-4d4f-94f8-16e03c14e1af"
                },
                {
                    "angle": -35.7413309733481,
                    "magnitude": 8240.79003337869,
                    "measurement_mrid": "_93cfc1aa-292e-493c-b33d-db7a14697e1f"
                },
                {
                    "angle": -35.5431141035305,
                    "magnitude": 8366.85698874056,
                    "measurement_mrid": "_47c81e2e-ab14-49b6-a82d-46a9d223cf1b"
                },
                {
                    "angle": -36.0258692854881,
                    "magnitude": 137.932434911471,
                    "measurement_mrid": "_8e74c866-6706-4a3e-9a77-c04cc52adb0a"
                },
                {
                    "angle": -36.0037953384996,
                    "magnitude": 137.458482382871,
                    "measurement_mrid": "_b5949ddb-8d65-4b0c-9dc2-7de0f6ae100e"
                },
                {
                    "angle": -156.859913595956,
                    "magnitude": 130.611230366841,
                    "measurement_mrid": "_6b81181a-a4b8-482e-b1fe-f0947a671f6f"
                },
                {
                    "angle": -156.859913595956,
                    "magnitude": 130.611230366841,
                    "measurement_mrid": "_b77643d2-7839-4d85-a1fd-4421c6acdaa5"
                },
                {
                    "angle": -156.432721496886,
                    "magnitude": 127.70375782175,
                    "measurement_mrid": "_01384b49-ac83-44bc-88b3-b3fd2a7da394"
                },
                {
                    "angle": -156.458850775417,
                    "magnitude": 128.223645275005,
                    "measurement_mrid": "_2ffaff2e-e63b-4352-bbf8-7043be8e1c83"
                },
                {
                    "angle": -156.427815854713,
                    "magnitude": 7874.1651476842,
                    "measurement_mrid": "_664ad789-693b-47e9-81dc-3bc5b7ee5f2e"
                },
                {
                    "angle": -155.705559357983,
                    "magnitude": 126.457962324535,
                    "measurement_mrid": "_20769a3f-c173-4e7b-bb6f-6768473b6aca"
                },
                {
                    "angle": -155.705559357983,
                    "magnitude": 126.457962324535,
                    "measurement_mrid": "_2321d611-ecf3-4ea4-a516-d26af0cf7ae8"
                },
                {
                    "angle": -34.0663691010738,
                    "magnitude": 120.539750567123,
                    "measurement_mrid": "_bda5df88-df5e-4f13-a693-53160fef7a9c"
                },
                {
                    "angle": -34.0815021721,
                    "magnitude": 120.824009728616,
                    "measurement_mrid": "_d8a72d76-2f02-4aa9-aa2f-4d234babba84"
                },
                {
                    "angle": -35.7904842859941,
                    "magnitude": 8292.33605929288,
                    "measurement_mrid": "_e91559b0-bcab-4ad7-9fe4-9586b3ea191d"
                },
                {
                    "angle": -34.3389323679422,
                    "magnitude": 119.903383540178,
                    "measurement_mrid": "_4e4d483c-7942-448e-a03c-3bb49759aa01"
                },
                {
                    "angle": -34.3893730836345,
                    "magnitude": 120.851303813077,
                    "measurement_mrid": "_f75e359e-29d6-4e70-8bf3-1e2fec15f03c"
                },
                {
                    "angle": -155.777382465007,
                    "magnitude": 125.851342200344,
                    "measurement_mrid": "_41e072b5-3ab9-487e-9c99-d96a3cd3e6e5"
                },
                {
                    "angle": -155.777382465007,
                    "magnitude": 125.851342200344,
                    "measurement_mrid": "_b4b2a18b-b40c-4207-803f-4679dbc7ef62"
                },
                {
                    "angle": -35.5724223127459,
                    "magnitude": 8331.49496371403,
                    "measurement_mrid": "_d62344bc-d323-4b78-9365-77c6a2d09e2d"
                },
                {
                    "angle": -34.8615551456882,
                    "magnitude": 7744.1336328993,
                    "measurement_mrid": "_11160709-cc0f-4e3f-9782-b000c7da1e82"
                },
                {
                    "angle": 86.3897765916562,
                    "magnitude": 7367.27714343868,
                    "measurement_mrid": "_66450606-34aa-492a-a310-3319fe58aab9"
                },
                {
                    "angle": -34.8614741129267,
                    "magnitude": 7743.87855663831,
                    "measurement_mrid": "_0047340d-44e9-476e-9f73-a32fe9c7369d"
                },
                {
                    "angle": -155.147020084463,
                    "magnitude": 7702.49867583798,
                    "measurement_mrid": "_d46956ae-3bce-4a5b-915c-fa77d8540842"
                },
                {
                    "angle": 85.6328101980702,
                    "magnitude": 7421.95715636759,
                    "measurement_mrid": "_e348e4b7-a9dd-4987-9688-7f0b2b0d70f7"
                },
                {
                    "angle": -34.7853181448044,
                    "magnitude": 128.716602696871,
                    "measurement_mrid": "_243aa19a-bc4b-44f4-8ea3-a55747ec5e67"
                },
                {
                    "angle": -34.7853181448044,
                    "magnitude": 128.716602696871,
                    "measurement_mrid": "_8bda6f37-bee0-4620-ad8b-7c79c7c159e0"
                },
                {
                    "angle": -34.861645784138,
                    "magnitude": 7744.10580528932,
                    "measurement_mrid": "_cee1f195-1f0b-4385-b38f-2a4942d03ed7"
                },
                {
                    "angle": -156.400839598439,
                    "magnitude": 7888.77405763717,
                    "measurement_mrid": "_a21a03c4-c2df-4092-9d74-29a377070426"
                },
                {
                    "angle": -35.7883536125327,
                    "magnitude": 8282.4042193332,
                    "measurement_mrid": "_c493b3a7-b1e2-4b89-acc9-64b82903e657"
                },
                {
                    "angle": 87.3199009127371,
                    "magnitude": 7299.92777558772,
                    "measurement_mrid": "_e75f52e8-bfcd-470b-a42d-a812d5c7f8a1"
                },
                {
                    "angle": -35.7417733992777,
                    "magnitude": 8310.97299477606,
                    "measurement_mrid": "_27627c1a-f9b2-41cc-b55a-0e234d6ecfcb"
                },
                {
                    "angle": 86.4261644660942,
                    "magnitude": 7375.89081233299,
                    "measurement_mrid": "_106cef38-6ec9-4a7e-9310-e3432c7f344d"
                },
                {
                    "angle": -35.7356548636477,
                    "magnitude": 8312.83559133536,
                    "measurement_mrid": "_7608c2f7-2b86-40da-bdd4-d45d0b834e7d"
                },
                {
                    "angle": -156.309353179254,
                    "magnitude": 7984.82193740906,
                    "measurement_mrid": "_e4d46996-7c2f-452a-acb6-e7c9d78b3eed"
                },
                {
                    "angle": -156.902818437674,
                    "magnitude": 131.396855378514,
                    "measurement_mrid": "_213cd2c1-df28-447b-8570-1e76727ee6b3"
                },
                {
                    "angle": -156.902818437674,
                    "magnitude": 131.396855378514,
                    "measurement_mrid": "_dcb00d97-1dfa-496f-99b4-9d60f812e640"
                },
                {
                    "angle": -156.141858114067,
                    "magnitude": 128.339372913025,
                    "measurement_mrid": "_542f2b2b-4a83-4d95-a4e6-e4aa5cc07fc8"
                },
                {
                    "angle": -156.141858114067,
                    "magnitude": 128.339372913025,
                    "measurement_mrid": "_c7ef3592-7740-4fca-978d-7333e038d63c"
                },
                {
                    "angle": 86.425212951057,
                    "magnitude": 7377.70200596038,
                    "measurement_mrid": "_8a057884-64be-4551-99d9-02abf7c4ad0f"
                },
                {
                    "angle": -35.7129621144313,
                    "magnitude": 8319.13353404221,
                    "measurement_mrid": "_8fdce6e0-9249-4d40-9a52-14f37d2af0d6"
                },
                {
                    "angle": -156.28787336634,
                    "magnitude": 7987.53279140103,
                    "measurement_mrid": "_abbac46c-f61d-4f54-9c3d-8d7aabea011a"
                },
                {
                    "angle": 86.7458134028372,
                    "magnitude": 120.086429322438,
                    "measurement_mrid": "_1213a0dc-e65e-417e-a4bb-cb36c0ebd449"
                },
                {
                    "angle": 86.7458134028372,
                    "magnitude": 120.086429322438,
                    "measurement_mrid": "_f6832f57-a926-4c37-8785-ea0948c1dcca"
                },
                {
                    "angle": -35.7415582910169,
                    "magnitude": 8311.09450471311,
                    "measurement_mrid": "_5145b824-c87b-42c5-a6f3-5d8e711d0468"
                },
                {
                    "angle": -35.2780788802934,
                    "magnitude": 128.412680310667,
                    "measurement_mrid": "_5c9e270a-1c9d-47df-829e-f4458a8c7abb"
                },
                {
                    "angle": -35.2780788802934,
                    "magnitude": 128.412680310667,
                    "measurement_mrid": "_cf561b58-2c85-4c3e-97e3-b64efb84f4b5"
                },
                {
                    "angle": -156.349946974082,
                    "magnitude": 7978.59752576002,
                    "measurement_mrid": "_3729160f-fdbf-40f7-9241-52977c2bdaa1"
                },
                {
                    "angle": 86.4209285395355,
                    "magnitude": 7372.91322366833,
                    "measurement_mrid": "_57fb4cf4-acf2-481e-a930-a356f166cf68"
                },
                {
                    "angle": -35.7665192862843,
                    "magnitude": 8303.11458709888,
                    "measurement_mrid": "_d5777a29-a003-46b3-81c2-84e39fc71d44"
                },
                {
                    "angle": -32.6901511091803,
                    "magnitude": 120.627754974677,
                    "measurement_mrid": "_9cffa207-5e2a-4b0d-9db2-01888f5391e7"
                },
                {
                    "angle": -32.7278475745075,
                    "magnitude": 121.338411299016,
                    "measurement_mrid": "_ea86e7ad-3b67-4009-9a4c-beab6c4b2785"
                },
                {
                    "angle": -156.436451456946,
                    "magnitude": 7869.50676716144,
                    "measurement_mrid": "_53865be2-c3e7-490d-9c3d-29903adc8d19"
                },
                {
                    "angle": -35.7511131060239,
                    "magnitude": 8308.09291272084,
                    "measurement_mrid": "_84bb1a59-84e2-4ab4-bffb-7ef6474beb13"
                },
                {
                    "angle": -156.328495247804,
                    "magnitude": 7981.93902328216,
                    "measurement_mrid": "_acdb69dc-94a9-40c7-9acc-abf0de38175a"
                },
                {
                    "angle": 86.4239770326036,
                    "magnitude": 7374.41725178145,
                    "measurement_mrid": "_c560c5d8-6ca6-48fd-8710-38213b0e1353"
                },
                {
                    "angle": 85.9450686922946,
                    "magnitude": 121.454395083249,
                    "measurement_mrid": "_6975d53d-4bde-4f45-96b4-be919a4bcd88"
                },
                {
                    "angle": 85.8879356552292,
                    "magnitude": 122.54122813165,
                    "measurement_mrid": "_6ab59fce-7e57-4abb-9e2f-6614a7674b06"
                },
                {
                    "angle": -156.472851664618,
                    "magnitude": 7871.00184973425,
                    "measurement_mrid": "_b0a5de6d-cb7b-4fa5-8b2a-37478aabf154"
                },
                {
                    "angle": -35.2432143796982,
                    "magnitude": 128.445464907515,
                    "measurement_mrid": "_629d81fa-835d-4731-9e30-4750bec7affe"
                },
                {
                    "angle": -35.2432143796982,
                    "magnitude": 128.445464907515,
                    "measurement_mrid": "_e406ab93-30cc-4d82-b9e9-e95822fdbaaf"
                },
                {
                    "angle": -155.309111938693,
                    "magnitude": 7613.28990312032,
                    "measurement_mrid": "_1f4e7a39-694d-4ab4-85bc-dd523e8eba82"
                },
                {
                    "angle": -35.4998559651996,
                    "magnitude": 8378.96249788986,
                    "measurement_mrid": "_19ae5ad8-4e31-4ded-833d-cdab5d27310e"
                },
                {
                    "angle": 87.1937347257339,
                    "magnitude": 7238.33132574143,
                    "measurement_mrid": "_dd5508a7-f400-4dd0-aa2a-b0d3a52bde49"
                },
                {
                    "angle": -156.471757197808,
                    "magnitude": 7871.34185617986,
                    "measurement_mrid": "_1741fcac-5a2e-4538-83a5-b1d76ea0bdf9"
                },
                {
                    "angle": -33.575375792996,
                    "magnitude": 7301.90645769993,
                    "measurement_mrid": "_19293ee5-3cf1-4cec-b710-f90e9e005294"
                },
                {
                    "angle": 86.8438208118199,
                    "magnitude": 7268.71378941374,
                    "measurement_mrid": "_23afef7e-6556-4068-897f-f9b16236bb34"
                },
                {
                    "angle": -153.677575241393,
                    "magnitude": 7277.58555265654,
                    "measurement_mrid": "_4e245cbf-f1a3-48dc-b64a-9948c4d6b866"
                },
                {
                    "angle": 85.7530574671634,
                    "magnitude": 121.500880612008,
                    "measurement_mrid": "_4509cf04-7bb0-4175-b6c3-c43711ba5cab"
                },
                {
                    "angle": 85.7818679976894,
                    "magnitude": 120.957478558553,
                    "measurement_mrid": "_6f3555b8-74e0-43d5-89d2-48359357ceee"
                },
                {
                    "angle": -35.7073862430424,
                    "magnitude": 8261.58455135742,
                    "measurement_mrid": "_b56f9476-bc83-490b-a1bb-cb587904c22a"
                },
                {
                    "angle": -156.123183235382,
                    "magnitude": 7980.92992360399,
                    "measurement_mrid": "_e409000a-c846-4628-be65-e51620ae0515"
                },
                {
                    "angle": 86.4783425288435,
                    "magnitude": 7320.30119353617,
                    "measurement_mrid": "_e5056f54-a182-43f4-9c71-4a23ec8bb0d6"
                },
                {
                    "angle": -35.6033966137235,
                    "magnitude": 8316.38885853415,
                    "measurement_mrid": "_53ed12c4-e0df-46fe-8a44-ab68b57a2cd8"
                },
                {
                    "angle": 88.3450968166624,
                    "magnitude": 119.149458186304,
                    "measurement_mrid": "_22412cc5-cbdd-4552-b68a-bb1566bed887"
                },
                {
                    "angle": 88.3450968166624,
                    "magnitude": 119.149458186304,
                    "measurement_mrid": "_4d069740-0a1f-4b25-8340-398fb8dd515d"
                },
                {
                    "angle": 86.4794122699565,
                    "magnitude": 7327.25504884496,
                    "measurement_mrid": "_27ee4607-548d-47b5-aac8-224530d33c20"
                },
                {
                    "angle": -35.692056084938,
                    "magnitude": 8268.01652391194,
                    "measurement_mrid": "_869d5844-992f-426b-9f6b-46c9c21cbf9d"
                },
                {
                    "angle": -156.130250569215,
                    "magnitude": 7981.42023362433,
                    "measurement_mrid": "_ee07545e-7277-4c0f-b17a-a14ffede5245"
                },
                {
                    "angle": -156.399256627494,
                    "magnitude": 7889.56753995141,
                    "measurement_mrid": "_194aa090-1a0f-43f4-aeb4-cda54bb71eb8"
                },
                {
                    "angle": -156.953377165588,
                    "magnitude": 130.989186006013,
                    "measurement_mrid": "_0c0ae57c-b90b-44a8-b45b-64e227b6204e"
                },
                {
                    "angle": -156.953377165588,
                    "magnitude": 130.989186006013,
                    "measurement_mrid": "_4546b081-39b0-48af-97e5-e3aa8e2085ad"
                },
                {
                    "angle": -154.14356253987,
                    "magnitude": 7768.55721171982,
                    "measurement_mrid": "_87e27bf3-9cd1-4bcf-9088-11515367ce8e"
                },
                {
                    "angle": -156.098226074964,
                    "magnitude": 128.128562713654,
                    "measurement_mrid": "_cbda6f25-7034-4fef-a2ff-f41f4d5fcc09"
                },
                {
                    "angle": -156.124267992789,
                    "magnitude": 128.648450208569,
                    "measurement_mrid": "_d6d4d7b5-a97c-4fe5-944b-e47f7b737594"
                },
                {
                    "angle": 87.2792484423705,
                    "magnitude": 7321.07164352194,
                    "measurement_mrid": "_d9cea8be-cf97-4b85-b08b-d0e35038dc31"
                },
                {
                    "angle": -154.328509181188,
                    "magnitude": 7298.68846931597,
                    "measurement_mrid": "_eb09e8cc-8075-4127-a10a-bae46470ff56"
                },
                {
                    "angle": -34.0498234707017,
                    "magnitude": 7231.07161665665,
                    "measurement_mrid": "_f87221a7-f55f-43de-8526-c597887318ac"
                },
                {
                    "angle": -33.9891843857087,
                    "magnitude": 7234.19069455701,
                    "measurement_mrid": "_b6519181-fca5-4d2f-b148-0190c4b04c1e"
                },
                {
                    "angle": -154.147089431477,
                    "magnitude": 7766.86328852048,
                    "measurement_mrid": "_cee317dc-d4a5-49da-92a0-e70d4811a8e8"
                },
                {
                    "angle": -156.145114906787,
                    "magnitude": 8008.92051135565,
                    "measurement_mrid": "_0189c729-eccc-47de-b41f-43fffb264c5b"
                },
                {
                    "angle": 86.4453550443897,
                    "magnitude": 7392.61819045685,
                    "measurement_mrid": "_63b2cf20-9735-4b1a-a145-b2a66cb3bfe8"
                },
                {
                    "angle": -35.5703336609511,
                    "magnitude": 8359.22364667218,
                    "measurement_mrid": "_a43f40d1-fbc9-4241-ae3c-e599cf019521"
                },
                {
                    "angle": -156.115467617913,
                    "magnitude": 8014.94317715009,
                    "measurement_mrid": "_48d6c11a-c036-452e-8e97-b302921721ff"
                },
                {
                    "angle": -35.5430886255614,
                    "magnitude": 8366.86583646119,
                    "measurement_mrid": "_af1866d9-ee3c-4d15-9bca-16f1594723cb"
                },
                {
                    "angle": 86.4619874605921,
                    "magnitude": 7397.24973331682,
                    "measurement_mrid": "_e2f8d7d8-34ae-4c9c-a27d-280c2072a8d9"
                },
                {
                    "angle": -36.1585258907757,
                    "magnitude": 137.10703849731,
                    "measurement_mrid": "_68d52ae0-dc74-4bbd-bb0d-06241acae14e"
                },
                {
                    "angle": -36.1806549131285,
                    "magnitude": 137.580992166006,
                    "measurement_mrid": "_b7ed7cd6-2f08-47e5-8e01-31a715cd8b7d"
                },
                {
                    "angle": 86.4428536480628,
                    "magnitude": 7391.9819710337,
                    "measurement_mrid": "_102c25a2-a1ce-4f73-9645-e26c177b79ac"
                },
                {
                    "angle": -35.5752913635729,
                    "magnitude": 8357.40065377496,
                    "measurement_mrid": "_15b01fe3-1704-4e5e-8b9b-bf67b47666ca"
                },
                {
                    "angle": -156.154017920736,
                    "magnitude": 8007.34904089459,
                    "measurement_mrid": "_a9ffcb1d-220e-40d3-903f-c2c95355ebb5"
                },
                {
                    "angle": -35.7515280248926,
                    "magnitude": 8305.44873990899,
                    "measurement_mrid": "_17931870-159b-4918-b06f-e92dd929a4be"
                },
                {
                    "angle": 86.7282923626387,
                    "magnitude": 120.182802579896,
                    "measurement_mrid": "_caf6cbfc-5a97-4f5b-8bf7-567f9487451a"
                },
                {
                    "angle": 86.7457636132642,
                    "magnitude": 119.856872079666,
                    "measurement_mrid": "_f037841b-8b50-4085-957f-b995466a7240"
                },
                {
                    "angle": -156.863788963457,
                    "magnitude": 130.34339265601,
                    "measurement_mrid": "_638d60af-c71b-4330-ad1c-5e578524a6dc"
                },
                {
                    "angle": -156.863788963457,
                    "magnitude": 130.34339265601,
                    "measurement_mrid": "_88b1cd64-48b2-4973-8b21-d9fcdf92ef7d"
                },
                {
                    "angle": -156.940861425467,
                    "magnitude": 130.875482678657,
                    "measurement_mrid": "_31a0907e-2324-42a6-9955-48b79f05d343"
                },
                {
                    "angle": -156.956190066718,
                    "magnitude": 131.187519463792,
                    "measurement_mrid": "_c2415234-ae4f-418e-bbbf-78fe8fb7275a"
                },
                {
                    "angle": -156.453446477215,
                    "magnitude": 7949.99060526192,
                    "measurement_mrid": "_6cff6808-1aeb-48fa-9e72-77ed2e99f9c0"
                },
                {
                    "angle": -35.8220700123436,
                    "magnitude": 8262.12289666972,
                    "measurement_mrid": "_8b93c1c6-6a3f-436c-a90d-83617671520f"
                },
                {
                    "angle": 86.3723618576585,
                    "magnitude": 7351.8105590263,
                    "measurement_mrid": "_b429c5b8-eb9b-4d2d-9270-b5cc9672495f"
                },
                {
                    "angle": -36.1795288703345,
                    "magnitude": 137.286832565219,
                    "measurement_mrid": "_44817d78-1c92-4562-ab4d-a71404ea25c1"
                },
                {
                    "angle": -36.1795288703345,
                    "magnitude": 137.286832565219,
                    "measurement_mrid": "_b4205dbf-10e8-4ce6-b4ba-222330b4b128"
                },
                {
                    "angle": -32.2646574637753,
                    "magnitude": 7315.84281835101,
                    "measurement_mrid": "_bb7ae530-d94f-4e8b-a437-1f200f402d56"
                },
                {
                    "angle": -35.6592966462582,
                    "magnitude": 131.818871686516,
                    "measurement_mrid": "_1e828a9c-d039-420e-b425-ed756f8c50b7"
                },
                {
                    "angle": -35.6592966462582,
                    "magnitude": 131.818871686516,
                    "measurement_mrid": "_5933eae7-ae2b-428a-b0eb-14252261e963"
                },
                {
                    "angle": -155.7210618968,
                    "magnitude": 125.954998383518,
                    "measurement_mrid": "_a924f7df-27d3-4bcc-a38f-f5a13f759148"
                },
                {
                    "angle": -155.747512661497,
                    "magnitude": 126.474895502868,
                    "measurement_mrid": "_bb17a26d-a46c-4786-8513-8f58f4fb2e0f"
                },
                {
                    "angle": 87.0273571180305,
                    "magnitude": 120.938254322255,
                    "measurement_mrid": "_02b70d3d-e657-43e4-8fe5-ed39010dee55"
                },
                {
                    "angle": 87.0447191121355,
                    "magnitude": 120.612323914025,
                    "measurement_mrid": "_4b3927c0-1f80-4b29-9a23-ef7f48ea5d2a"
                },
                {
                    "angle": 87.9420937661436,
                    "magnitude": 7305.88786476117,
                    "measurement_mrid": "_c8bbc6e5-dd8e-4f60-b6ed-b870a9dac6a1"
                },
                {
                    "angle": -156.881015150417,
                    "magnitude": 130.195076223697,
                    "measurement_mrid": "_86fc82fc-dedf-404e-9089-770d1c200dc4"
                },
                {
                    "angle": -156.881015150417,
                    "magnitude": 130.195076223697,
                    "measurement_mrid": "_aab28982-6dc3-452c-8d43-368b6e2ad680"
                },
                {
                    "angle": -156.624085276198,
                    "magnitude": 131.928947056443,
                    "measurement_mrid": "_0e74f72b-0e38-451c-a63e-33eefb6a6fdc"
                },
                {
                    "angle": -156.624085276198,
                    "magnitude": 131.928947056443,
                    "measurement_mrid": "_d9921f99-99de-4833-b220-63df636f1066"
                },
                {
                    "angle": -34.235883622325,
                    "magnitude": 119.664860466809,
                    "measurement_mrid": "_157e6837-5a34-4cbe-a71c-97bb29421d03"
                },
                {
                    "angle": -34.235883622325,
                    "magnitude": 119.664860466809,
                    "measurement_mrid": "_8cffd146-06b9-4217-8f80-6403093bc763"
                },
                {
                    "angle": -32.8702849285222,
                    "magnitude": 121.119541208748,
                    "measurement_mrid": "_2f850834-7c44-4a15-85cc-dfe70ef0b416"
                },
                {
                    "angle": -32.8551799243993,
                    "magnitude": 120.835285249663,
                    "measurement_mrid": "_8a448daf-69b7-4b6b-b483-4f8b90030f32"
                },
                {
                    "angle": 85.7726878213961,
                    "magnitude": 121.258620875885,
                    "measurement_mrid": "_5b9b483e-dac2-47b0-b4f3-4aeea0771874"
                },
                {
                    "angle": 85.7726878213961,
                    "magnitude": 121.258620875885,
                    "measurement_mrid": "_99e6dd17-c7f5-4921-8b88-1e5de576295d"
                },
                {
                    "angle": 88.3359434725656,
                    "magnitude": 119.236862283245,
                    "measurement_mrid": "_b260cf59-45e3-4b55-a416-2924d6a3a7c3"
                },
                {
                    "angle": 88.3476921251548,
                    "magnitude": 119.019398365815,
                    "measurement_mrid": "_f80c9c7c-ae75-4c3d-9bb0-4b1fda106683"
                },
                {
                    "angle": -32.2652980891673,
                    "magnitude": 7315.52934082143,
                    "measurement_mrid": "_39ddf07e-fae9-465b-a871-ec78608b6556"
                },
                {
                    "angle": 86.4792697615719,
                    "magnitude": 7243.76204004948,
                    "measurement_mrid": "_3f513feb-12e2-4762-b292-694080af679d"
                },
                {
                    "angle": -33.9709545227851,
                    "magnitude": 7276.1225786005,
                    "measurement_mrid": "_f6c61278-d6b6-4108-b838-16d6a0b7b630"
                },
                {
                    "angle": -154.091332948236,
                    "magnitude": 7245.33246442863,
                    "measurement_mrid": "_fee64ec7-dd1d-427a-bd3f-723b780c4b74"
                },
                {
                    "angle": -35.7872288988549,
                    "magnitude": 8293.27611407237,
                    "measurement_mrid": "_1282111d-1341-434e-a75f-72a86df84b7a"
                },
                {
                    "angle": -156.954170109938,
                    "magnitude": 130.981995471304,
                    "measurement_mrid": "_0ecc5c26-3108-4e66-a237-04d8bab38fcb"
                },
                {
                    "angle": -156.954170109938,
                    "magnitude": 130.981995471304,
                    "measurement_mrid": "_1610bbb8-df47-41a9-b201-10ae5c42c4f2"
                },
                {
                    "angle": -156.427134187688,
                    "magnitude": 7875.02582985351,
                    "measurement_mrid": "_064ef02e-9b4c-46ea-898c-da0ca871d937"
                },
                {
                    "angle": -35.5967341948188,
                    "magnitude": 8313.10814730971,
                    "measurement_mrid": "_9d569c74-7c72-47e0-b995-b3c00a7fc300"
                },
                {
                    "angle": 87.2226495611059,
                    "magnitude": 7252.50831531016,
                    "measurement_mrid": "_a9f81423-39f9-4b05-adb7-d2953b296d5b"
                },
                {
                    "angle": 87.1842089803266,
                    "magnitude": 7233.59556977436,
                    "measurement_mrid": "_6a7ebfff-e20d-4be7-960d-80a7d36eee81"
                },
                {
                    "angle": 87.2579130088307,
                    "magnitude": 7269.94137315265,
                    "measurement_mrid": "_97f71228-55e4-4f52-aac4-0074017f2d81"
                },
                {
                    "angle": 87.2582133091406,
                    "magnitude": 7270.09153127047,
                    "measurement_mrid": "_195deaa9-a677-4927-bd56-2b31560b149e"
                },
                {
                    "angle": -156.255417612394,
                    "magnitude": 7966.43552809004,
                    "measurement_mrid": "_7b58304f-c93e-44af-b123-8600c5b8cafd"
                },
                {
                    "angle": 86.4264113248206,
                    "magnitude": 7387.5522092743,
                    "measurement_mrid": "_80bf22b5-a05f-4dba-918a-09962de5828a"
                },
                {
                    "angle": -35.5765672501084,
                    "magnitude": 8333.53881455168,
                    "measurement_mrid": "_eca00bd4-b157-4275-a3d4-58951d6a3414"
                },
                {
                    "angle": 85.896248341347,
                    "magnitude": 122.415507213679,
                    "measurement_mrid": "_474ce3d4-b9ac-4859-8079-cb1563a80bcb"
                },
                {
                    "angle": 85.9391561368913,
                    "magnitude": 121.600126866845,
                    "measurement_mrid": "_7df486c3-02cf-473e-94ca-65da0b17a576"
                },
                {
                    "angle": -35.7064668066025,
                    "magnitude": 8261.64142926745,
                    "measurement_mrid": "_c33cfe26-d8f4-47a9-b649-075325b3ea95"
                },
                {
                    "angle": 86.4452587347277,
                    "magnitude": 7358.02236309753,
                    "measurement_mrid": "_02bf82c7-5689-4356-b442-a82b51ad8ff4"
                },
                {
                    "angle": -156.143981652447,
                    "magnitude": 7985.63252951992,
                    "measurement_mrid": "_52c1254c-af0b-4a09-9571-6911b16ccf20"
                },
                {
                    "angle": -35.6089532137092,
                    "magnitude": 8318.71171511937,
                    "measurement_mrid": "_6f44f2b5-9744-430e-9786-12b2978efe4f"
                },
                {
                    "angle": 86.1355867060116,
                    "magnitude": 7330.33948131739,
                    "measurement_mrid": "_6b8ab664-9f28-4943-81c4-285a21e21ba5"
                },
                {
                    "angle": -35.5852140861692,
                    "magnitude": 8310.85374203044,
                    "measurement_mrid": "_8774789c-c3bf-459b-a297-a33f20bc3d97"
                },
                {
                    "angle": -156.375790665692,
                    "magnitude": 7914.40860025464,
                    "measurement_mrid": "_907fac33-820c-4299-a5a1-5a8579d83a2e"
                },
                {
                    "angle": -35.2500504521507,
                    "magnitude": 7966.52200287632,
                    "measurement_mrid": "_b356df3e-063e-4c08-9b74-6189d2ead940"
                },
                {
                    "angle": -36.2062921655372,
                    "magnitude": 136.918656977624,
                    "measurement_mrid": "_125b028a-908a-476f-9118-d71e25687889"
                },
                {
                    "angle": -36.1929570666647,
                    "magnitude": 136.634392920013,
                    "measurement_mrid": "_570de679-ec2c-4201-b386-f77ecee3be0d"
                },
                {
                    "angle": -154.067641466027,
                    "magnitude": 7286.90629294969,
                    "measurement_mrid": "_b5daac22-c342-4e53-9446-f4f2832db8d2"
                },
                {
                    "angle": 86.8738461999981,
                    "magnitude": 120.809960604338,
                    "measurement_mrid": "_8df10786-f6be-4ed5-b4f0-e0ee01691a39"
                },
                {
                    "angle": 86.8738461999981,
                    "magnitude": 120.809960604338,
                    "measurement_mrid": "_b0e320f4-49c4-4f71-9ecc-3f38f4c90221"
                },
                {
                    "angle": -154.547940779986,
                    "magnitude": 120.438528831342,
                    "measurement_mrid": "_7d42874a-b74c-4d2c-9be8-250f80c4cee5"
                },
                {
                    "angle": -154.547940779986,
                    "magnitude": 120.438528831342,
                    "measurement_mrid": "_a2397542-e43a-409c-bc2a-a1ffb7a76e58"
                },
                {
                    "angle": 85.6098999071062,
                    "magnitude": 120.709409213526,
                    "measurement_mrid": "_3a4f1a65-4b26-4791-83f5-2ef0362e47fa"
                },
                {
                    "angle": 85.5810306719708,
                    "magnitude": 121.252810513612,
                    "measurement_mrid": "_f09aad93-69c9-4a93-81ef-faaefcce5453"
                },
                {
                    "angle": 87.1848564508911,
                    "magnitude": 7233.92795171894,
                    "measurement_mrid": "_c42cb23f-2ffc-439c-ada5-a57ed6fd4676"
                },
                {
                    "angle": -31.2329014535523,
                    "magnitude": 7325.2389807059,
                    "measurement_mrid": "_e0eaf097-38a7-4387-8a9d-9b171aba1e30"
                },
                {
                    "angle": 85.738518056404,
                    "magnitude": 122.039216124145,
                    "measurement_mrid": "_29baa693-2233-4c0a-bb3e-957aac68ec47"
                },
                {
                    "angle": 85.7213603100979,
                    "magnitude": 122.365146598412,
                    "measurement_mrid": "_d285f9c3-4e3e-4daa-8c28-2ccbf08ca3bb"
                },
                {
                    "angle": -170.234012033072,
                    "magnitude": 0.595751170238045,
                    "measurement_mrid": "_6bef8eab-59cd-4ce0-9ea0-86dd8723d9c8"
                },
                {
                    "angle": -35.7843163709402,
                    "magnitude": 8294.93093104658,
                    "measurement_mrid": "_2d61ded1-ee54-4b4a-83af-b645b22e4700"
                },
                {
                    "angle": -36.0030507370133,
                    "magnitude": 137.753022705918,
                    "measurement_mrid": "_0e57d630-1793-4882-882e-3e5a23046de4"
                },
                {
                    "angle": -36.0030507370133,
                    "magnitude": 137.753022705918,
                    "measurement_mrid": "_774747a6-b516-47e7-9bc0-3a5c35c4e83e"
                },
                {
                    "angle": -35.6161730127704,
                    "magnitude": 8321.09287847883,
                    "measurement_mrid": "_84e31f5c-4879-432b-b2bd-1e25a36e8ac6"
                },
                {
                    "angle": -35.618430125097,
                    "magnitude": 8320.34542038539,
                    "measurement_mrid": "_bc1fcc26-24e4-4da4-8f14-ec0623a34bcf"
                },
                {
                    "angle": -155.065313833959,
                    "magnitude": 120.576647981362,
                    "measurement_mrid": "_1004a5b7-25b5-44f9-ad49-924384f1fd3e"
                },
                {
                    "angle": -155.065313833959,
                    "magnitude": 120.576647981362,
                    "measurement_mrid": "_c46e2835-8860-438b-84f9-ded00709d936"
                },
                {
                    "angle": -35.2638792340673,
                    "magnitude": 127.186254336097,
                    "measurement_mrid": "_a25b0880-7df4-4c32-ba29-a426af1b440a"
                },
                {
                    "angle": -35.2877395920854,
                    "magnitude": 127.660205999238,
                    "measurement_mrid": "_b70e35af-b231-4480-94d6-98ad694a583d"
                },
                {
                    "angle": 88.8838483446096,
                    "magnitude": 7222.49026664706,
                    "measurement_mrid": "_28cba426-37b4-40ec-94de-cc3b3060153d"
                },
                {
                    "angle": -153.455777494233,
                    "magnitude": 120.912764989994,
                    "measurement_mrid": "_5ced2b99-0c16-4337-b882-9aac0e42d7ba"
                },
                {
                    "angle": -153.455777494233,
                    "magnitude": 120.912764989994,
                    "measurement_mrid": "_63a69145-8137-4044-ab03-2a70c35f7dd7"
                },
                {
                    "angle": -154.149537015949,
                    "magnitude": 7765.60224659585,
                    "measurement_mrid": "_d5e7084e-bc89-4736-85e2-a12380773656"
                },
                {
                    "angle": 86.9465213079682,
                    "magnitude": 7276.62326249786,
                    "measurement_mrid": "_60e84990-eeda-4cd7-93fc-db46b071ab5d"
                },
                {
                    "angle": -33.4607853480084,
                    "magnitude": 7310.90112157476,
                    "measurement_mrid": "_dbf4c676-a791-449c-9c6f-77d774869bc1"
                },
                {
                    "angle": -153.559342757223,
                    "magnitude": 7287.40723688689,
                    "measurement_mrid": "_e26a3cd2-6e54-48d2-b5cb-ae37bee44f5a"
                },
                {
                    "angle": -32.2647648397545,
                    "magnitude": 7315.78376732275,
                    "measurement_mrid": "_6a56c3fd-1325-4d69-bac0-6e80923eb06d"
                },
                {
                    "angle": -156.463556502729,
                    "magnitude": 7873.8899323145,
                    "measurement_mrid": "_c186b580-fc60-4b61-90d2-2eac096a562c"
                },
                {
                    "angle": -156.65620320158,
                    "magnitude": 131.744960253551,
                    "measurement_mrid": "_c41de98e-d3af-4866-8246-4bdc534693c8"
                },
                {
                    "angle": -156.65620320158,
                    "magnitude": 131.744960253551,
                    "measurement_mrid": "_e654a2bb-f530-4a32-b9c9-56813fd234b4"
                },
                {
                    "angle": -156.873903935198,
                    "magnitude": 131.387536765496,
                    "measurement_mrid": "_166644f5-5e60-4f35-9866-69f84bac63c4"
                },
                {
                    "angle": -156.899304003531,
                    "magnitude": 131.907423362243,
                    "measurement_mrid": "_9dbb28fd-40af-423c-aa6b-843ae8710010"
                },
                {
                    "angle": -155.139258483031,
                    "magnitude": 7694.09244979647,
                    "measurement_mrid": "_579226ae-5ad9-4f0d-baba-6e719fd8c37a"
                },
                {
                    "angle": -35.0428360948553,
                    "magnitude": 132.56515337857,
                    "measurement_mrid": "_70989b62-2e97-43c2-89e2-24af75be38f9"
                },
                {
                    "angle": -35.0290499743687,
                    "magnitude": 132.280893075332,
                    "measurement_mrid": "_f2f6841d-95f1-4e66-af4f-0b82cc16686f"
                },
                {
                    "angle": -33.785280341304,
                    "magnitude": 7237.25755318358,
                    "measurement_mrid": "_fb2855e3-5728-47a3-97d5-236859ca9738"
                },
                {
                    "angle": 88.3545330987557,
                    "magnitude": 119.226598902288,
                    "measurement_mrid": "_b7f15a2e-5247-4c22-b979-e47f3b80aa1e"
                },
                {
                    "angle": 88.3545330987557,
                    "magnitude": 119.226598902288,
                    "measurement_mrid": "_df4e00ba-dec7-4ed0-9a79-d6b562f8b025"
                },
                {
                    "angle": -156.502359086849,
                    "magnitude": 7922.12228016553,
                    "measurement_mrid": "_33702016-94de-4025-a181-012dc5620aff"
                },
                {
                    "angle": -155.617152697214,
                    "magnitude": 127.265631360122,
                    "measurement_mrid": "_ce3a3cbd-3b0c-4873-be1f-cfb5290b84ba"
                },
                {
                    "angle": -155.617152697214,
                    "magnitude": 127.265631360122,
                    "measurement_mrid": "_f185c98d-1f4e-49e9-9c8d-f89f2cd8569d"
                },
                {
                    "angle": -35.9590195052876,
                    "magnitude": 138.375406184687,
                    "measurement_mrid": "_24ecabc6-c831-4b2a-8e8b-7eed6ac0a28c"
                },
                {
                    "angle": -35.9590195052876,
                    "magnitude": 138.375406184687,
                    "measurement_mrid": "_b341b03e-1dda-4dfb-bd4b-fd05e5db886c"
                },
                {
                    "angle": -36.0900152314083,
                    "magnitude": 137.762885099638,
                    "measurement_mrid": "_8f883146-4428-4b1a-abc8-4ab822911a27"
                },
                {
                    "angle": -36.0900152314083,
                    "magnitude": 137.762885099638,
                    "measurement_mrid": "_c444283a-a031-4506-8e8f-c1c99e1b4a3e"
                },
                {
                    "angle": -156.496066129602,
                    "magnitude": 7925.57271891404,
                    "measurement_mrid": "_1d7cc1ea-6ab2-4843-98c3-6210ed33cc64"
                },
                {
                    "angle": -155.172179589916,
                    "magnitude": 128.651230829165,
                    "measurement_mrid": "_53ad2c97-7a8d-43d0-b0dd-effad1990979"
                },
                {
                    "angle": -155.172179589916,
                    "magnitude": 128.651230829165,
                    "measurement_mrid": "_ea772142-6b9d-41cd-a621-6d2446b7a475"
                },
                {
                    "angle": -156.950680796757,
                    "magnitude": 131.370950327598,
                    "measurement_mrid": "_28d4926c-0379-4aa9-a7dd-38b1f4e81925"
                },
                {
                    "angle": -156.925178060274,
                    "magnitude": 130.851063079298,
                    "measurement_mrid": "_c15c351d-3c35-4021-8508-9ca2e86e6652"
                },
                {
                    "measurement_mrid": "_4cb1b7aa-7a19-49a0-9261-2d6dc340292d",
                    "value": 1
                },
                {
                    "measurement_mrid": "_5daba227-ee21-4266-b00c-76d693f5c436",
                    "value": 10
                },
                {
                    "measurement_mrid": "_652a49a1-96ea-48a2-9906-8c170abcba7f",
                    "value": 16
                },
                {
                    "measurement_mrid": "_6909db32-a7cb-41e6-8244-2f1250bdfe9e",
                    "value": 16
                },
                {
                    "measurement_mrid": "_ae7627a8-6078-4d98-b28e-4331e16d3260",
                    "value": 1
                },
                {
                    "measurement_mrid": "_f8305ddf-391c-4002-aea9-00160603c0c3",
                    "value": 10
                },
                {
                    "angle": -35.7111954443917,
                    "magnitude": 8261.00129510266,
                    "measurement_mrid": "_87d6f7e9-e2eb-4ef0-9e38-773fbfd507e7"
                },
                {
                    "angle": -156.159549325506,
                    "magnitude": 7983.10319184673,
                    "measurement_mrid": "_0ca9049a-7970-4f39-93b2-efeaaccb3ab1"
                },
                {
                    "angle": -35.5990507579291,
                    "magnitude": 8326.63868978629,
                    "measurement_mrid": "_2e720b12-9bd9-4cd5-a307-28d775f823b5"
                },
                {
                    "angle": 86.4256845965158,
                    "magnitude": 7362.40683498406,
                    "measurement_mrid": "_cbd56d03-175a-42b0-952d-dacf7ec6cc7f"
                },
                {
                    "angle": -156.888358846014,
                    "magnitude": 130.129947989465,
                    "measurement_mrid": "_4cb4bb64-b804-4fc0-8051-78cb84d60924"
                },
                {
                    "angle": -156.888358846014,
                    "magnitude": 130.129947989465,
                    "measurement_mrid": "_f52f7373-6de1-4d98-a654-04dd26585e6e"
                },
                {
                    "angle": -32.9375255901958,
                    "magnitude": 7327.20464003034,
                    "measurement_mrid": "_e1b8addb-b20a-4e9c-b33d-d7b057ee56ef"
                },
                {
                    "angle": -32.8744521565076,
                    "magnitude": 7319.52552641203,
                    "measurement_mrid": "_7a32149c-cab1-4c51-a6cb-6138c61ea9fe"
                },
                {
                    "angle": -35.7119168434933,
                    "magnitude": 8260.91106260992,
                    "measurement_mrid": "_83f0781c-7753-4a01-b5e6-0b9b22e9ec48"
                },
                {
                    "angle": 86.4715981268163,
                    "magnitude": 7316.02036834395,
                    "measurement_mrid": "_b19252ad-89ab-4305-b499-3a94d5c40240"
                },
                {
                    "angle": 86.3807043100164,
                    "magnitude": 7359.23410958916,
                    "measurement_mrid": "_05a97217-6c1f-4cdd-a15c-e76f6fcbcd78"
                },
                {
                    "angle": -35.8083275186522,
                    "magnitude": 8272.46158749579,
                    "measurement_mrid": "_711981e0-511a-4ce7-b5fc-8ed3948965cb"
                },
                {
                    "angle": -156.449218551734,
                    "magnitude": 7954.52060449204,
                    "measurement_mrid": "_77165694-caa6-420d-a18a-4242c95a70d5"
                },
                {
                    "angle": 86.389607109993,
                    "magnitude": 7366.87498956838,
                    "measurement_mrid": "_1fcdefce-d6cc-44fa-bb17-66ae8363b68a"
                },
                {
                    "angle": -35.7916539803539,
                    "magnitude": 8285.16631138587,
                    "measurement_mrid": "_50944e43-1124-4ad5-a442-d729e2c68572"
                },
                {
                    "angle": -156.446448456325,
                    "magnitude": 7955.11793353129,
                    "measurement_mrid": "_7af830cc-5dee-4f89-8ed6-9d5475fcae49"
                },
                {
                    "angle": -156.839865291576,
                    "magnitude": 130.786558567883,
                    "measurement_mrid": "_142c1029-2f04-4627-b0b0-0c647d77a24c"
                },
                {
                    "angle": -156.839865291576,
                    "magnitude": 130.786558567883,
                    "measurement_mrid": "_91ebb7e3-9344-49bb-b8d8-16661e471070"
                },
                {
                    "angle": -36.0760743943867,
                    "magnitude": 136.946550866223,
                    "measurement_mrid": "_3ad73b0e-a924-44ef-ad7f-7efd5b6dcb9d"
                },
                {
                    "angle": -36.0760743943867,
                    "magnitude": 136.946550866223,
                    "measurement_mrid": "_3d4c5217-9607-4f48-8da4-5c6c353f163e"
                },
                {
                    "angle": -153.885518880724,
                    "magnitude": 7261.17649210074,
                    "measurement_mrid": "_1206c526-a1e7-45eb-b0b0-bd171d1e111f"
                },
                {
                    "angle": 86.6617524540471,
                    "magnitude": 7255.95675176756,
                    "measurement_mrid": "_3de81462-dc88-420e-a68b-de962b1f05af"
                },
                {
                    "angle": -33.7749153576648,
                    "magnitude": 7288.15354347553,
                    "measurement_mrid": "_51d9a113-b04d-4141-bdd6-4ee2a18da3d2"
                },
                {
                    "angle": -153.885518880724,
                    "magnitude": 7261.17649210074,
                    "measurement_mrid": "_8cb8b255-85f7-4409-8f98-2cf8b919f58e"
                },
                {
                    "angle": -33.7749153576648,
                    "magnitude": 7288.15354347553,
                    "measurement_mrid": "_8e137c08-78fe-42d8-a330-a0d5044941c9"
                },
                {
                    "angle": 86.6617524540471,
                    "magnitude": 7255.95675176756,
                    "measurement_mrid": "_c3f211fb-d893-4f9e-a800-f28514b798c6"
                },
                {
                    "angle": -156.913287717434,
                    "magnitude": 130.015032997211,
                    "measurement_mrid": "_00ffc82f-c897-4960-a208-807e66c528ed"
                },
                {
                    "angle": -156.928715965847,
                    "magnitude": 130.327069523852,
                    "measurement_mrid": "_21044967-0413-486f-9340-b73999f84e59"
                },
                {
                    "angle": 86.2406340298398,
                    "magnitude": 7400.8260684933,
                    "measurement_mrid": "_369e5952-96ef-4e67-b6c3-2346e5a96e25"
                },
                {
                    "angle": -156.465976555086,
                    "magnitude": 7873.13737814231,
                    "measurement_mrid": "_2d03715d-d4b6-4ca4-b689-956562f003b4"
                },
                {
                    "angle": 85.9399072914101,
                    "magnitude": 121.859130995636,
                    "measurement_mrid": "_a120486e-b02a-4469-ba91-79858dd321a7"
                },
                {
                    "angle": 85.9113081600736,
                    "magnitude": 122.402532798845,
                    "measurement_mrid": "_db82cb23-1739-46eb-bbfe-7a7f3fa35f87"
                },
                {
                    "angle": -156.421961054732,
                    "magnitude": 7877.66311983756,
                    "measurement_mrid": "_83150e6c-37c9-401e-8612-049135314311"
                },
                {
                    "angle": 85.7553528664312,
                    "magnitude": 122.420571854784,
                    "measurement_mrid": "_18c5dea3-c031-4eac-a776-fac88f5084e6"
                },
                {
                    "angle": 85.7553528664312,
                    "magnitude": 122.420571854784,
                    "measurement_mrid": "_6286211f-4e61-487f-944d-21d5332617cb"
                },
                {
                    "angle": 86.4232889907042,
                    "magnitude": 7385.92674638541,
                    "measurement_mrid": "_afe7948d-63a8-4bf5-b1b9-b743203906e2"
                },
                {
                    "angle": -32.9385463220278,
                    "magnitude": 7326.91379143459,
                    "measurement_mrid": "_bb872a6d-43a7-4471-81d0-8dcc4e8d02d0"
                },
                {
                    "angle": -35.9033562369702,
                    "magnitude": 137.664717655313,
                    "measurement_mrid": "_4b3cff7c-a275-4456-b8c6-44000c951c96"
                },
                {
                    "angle": -35.9033562369702,
                    "magnitude": 137.664717655313,
                    "measurement_mrid": "_87607cb7-e244-4deb-a701-bac7f4539234"
                },
                {
                    "angle": -36.0997087550714,
                    "magnitude": 136.749543081489,
                    "measurement_mrid": "_2216b226-6b3a-4506-adcd-d32c7f435acf"
                },
                {
                    "angle": -36.0997087550714,
                    "magnitude": 136.749543081489,
                    "measurement_mrid": "_57a18697-8100-4a6f-a0af-361a1fe941b4"
                },
                {
                    "angle": -151.727212109322,
                    "magnitude": 7319.76557082694,
                    "measurement_mrid": "_1532569f-c911-470e-8b8b-bec0da88aac8"
                },
                {
                    "angle": -34.6304814599054,
                    "magnitude": 8001.83598090998,
                    "measurement_mrid": "_8ac76f8d-a318-4656-a83a-1e731bfd7fda"
                },
                {
                    "angle": -36.1372093030667,
                    "magnitude": 136.386076149303,
                    "measurement_mrid": "_aba9d35c-f0a9-4ab9-886b-8ec616ed0d12"
                },
                {
                    "angle": -36.1372093030667,
                    "magnitude": 136.386076149303,
                    "measurement_mrid": "_f0e7f7d2-c8bf-4459-9d7f-c1cdb280db40"
                },
                {
                    "angle": -33.7797422608803,
                    "magnitude": 7235.46085584019,
                    "measurement_mrid": "_08152f2e-ccc6-4e18-8abe-71bab8f2b564"
                },
                {
                    "angle": 87.3831930746965,
                    "magnitude": 7313.47947461764,
                    "measurement_mrid": "_2c9ef343-b17b-44f1-b71e-9d605fc7c65f"
                },
                {
                    "angle": -154.059236605016,
                    "magnitude": 7288.37223422975,
                    "measurement_mrid": "_8a1321cf-7047-40eb-a3a9-b64d70266832"
                },
                {
                    "angle": -155.707378042277,
                    "magnitude": 7748.73964339161,
                    "measurement_mrid": "_f03e739c-1224-48b8-afef-dd808fe87081"
                },
                {
                    "angle": -155.706436203302,
                    "magnitude": 7749.42652045522,
                    "measurement_mrid": "_780dab9a-9128-4891-a02a-bafc1aaf8fc8"
                },
                {
                    "angle": -35.7408632345597,
                    "magnitude": 8241.04858328048,
                    "measurement_mrid": "_fc540ecf-5e11-41de-bf4f-e4efcb8ad342"
                },
                {
                    "angle": -156.953153148567,
                    "magnitude": 130.990592783752,
                    "measurement_mrid": "_66dfc85b-dd00-4d70-879b-b0a995f398ca"
                },
                {
                    "angle": -156.953153148567,
                    "magnitude": 130.990592783752,
                    "measurement_mrid": "_8a5d3cf2-351b-4585-9735-5dc3e2502830"
                },
                {
                    "angle": -156.901016883508,
                    "magnitude": 130.391605792176,
                    "measurement_mrid": "_29a45380-daa8-4bf0-8020-6ea56d29319b"
                },
                {
                    "angle": -156.875326399593,
                    "magnitude": 129.871718383559,
                    "measurement_mrid": "_fb23d725-bb4d-4cb4-b387-8b47c2535297"
                },
                {
                    "angle": -156.165061192689,
                    "magnitude": 7981.50229211283,
                    "measurement_mrid": "_a97aaff4-9b60-4102-aba3-6fe2ae1c59c2"
                },
                {
                    "angle": -36.099902328641,
                    "magnitude": 136.748498777692,
                    "measurement_mrid": "_82b123d1-0a24-4288-96d9-79859e39aaec"
                },
                {
                    "angle": -36.099902328641,
                    "magnitude": 136.748498777692,
                    "measurement_mrid": "_cdd0a6d9-2a4d-4562-ac78-d029d08faba5"
                },
                {
                    "angle": -156.380263173049,
                    "magnitude": 7914.23671759101,
                    "measurement_mrid": "_20119be8-be2f-4488-9b92-e17c3bb0b524"
                },
                {
                    "angle": 86.4787807792093,
                    "magnitude": 7321.53041599771,
                    "measurement_mrid": "_78acf3d7-c80f-464b-939b-ddb174351ff6"
                },
                {
                    "angle": -35.7049020015522,
                    "magnitude": 8262.15428029356,
                    "measurement_mrid": "_a50f4691-0894-4b7a-8a59-54415ea7a91f"
                },
                {
                    "angle": 86.3459697803466,
                    "magnitude": 122.022522893991,
                    "measurement_mrid": "_25d2e371-a3e1-4cd3-85b8-4688cd41a3a6"
                },
                {
                    "angle": 86.3459697803466,
                    "magnitude": 122.022522893991,
                    "measurement_mrid": "_631babdd-64e7-44bd-8378-432ecb05a360"
                },
                {
                    "angle": 86.4224873990377,
                    "magnitude": 7385.53928942944,
                    "measurement_mrid": "_40e83dc8-613e-4b71-ba53-e477337b4205"
                },
                {
                    "angle": 86.473225554156,
                    "magnitude": 7317.26441136026,
                    "measurement_mrid": "_4cb08c16-8aa4-47c1-822e-46bd9fd04713"
                },
                {
                    "angle": -156.918445369075,
                    "magnitude": 129.988838235704,
                    "measurement_mrid": "_053a1a53-1dea-4952-9b07-f174c6fd9be9"
                },
                {
                    "angle": -156.933876264519,
                    "magnitude": 130.30087508733,
                    "measurement_mrid": "_9a65ccd2-fba8-4540-8c11-4c291454b5b2"
                },
                {
                    "angle": 86.4732725750787,
                    "magnitude": 7317.2941392601,
                    "measurement_mrid": "_5c259f37-eb27-412e-8946-921f9fc708d3"
                },
                {
                    "angle": -36.0172968942189,
                    "magnitude": 137.68201392326,
                    "measurement_mrid": "_9358319e-735a-403e-b2dd-4a46d19bdd2d"
                },
                {
                    "angle": -36.0172968942189,
                    "magnitude": 137.68201392326,
                    "measurement_mrid": "_a222fc18-9527-498f-b5fe-3ba16d0cedff"
                },
                {
                    "angle": 86.3870945234388,
                    "magnitude": 7362.38810774877,
                    "measurement_mrid": "_711b2609-1aa9-443a-ab3e-6ab126ca7fe1"
                },
                {
                    "angle": -156.120682172243,
                    "magnitude": 7980.96843414081,
                    "measurement_mrid": "_0508a33b-d1f2-4bb3-bfeb-032b54c29754"
                },
                {
                    "angle": 86.4756287006842,
                    "magnitude": 7318.9124633238,
                    "measurement_mrid": "_16adc9c1-10f2-4157-8c7a-6feea6b1dfbe"
                },
                {
                    "angle": -35.709784135948,
                    "magnitude": 8261.24059908785,
                    "measurement_mrid": "_7458fd61-3e0f-482b-9cb6-7d4b88aff0b1"
                },
                {
                    "angle": -34.6803132558575,
                    "magnitude": 119.391483113542,
                    "measurement_mrid": "_5261b4d7-7bcb-49f0-83c5-7b08cf4089f7"
                },
                {
                    "angle": -34.6803132558575,
                    "magnitude": 119.391483113542,
                    "measurement_mrid": "_89b24cf9-1a3d-47d7-bb1a-bdc03a3224d5"
                },
                {
                    "angle": -156.376845921378,
                    "magnitude": 7901.49525610139,
                    "measurement_mrid": "_02875f9d-7677-4b84-a235-d2f9ce100109"
                },
                {
                    "angle": 87.0184473705277,
                    "magnitude": 7377.69440102955,
                    "measurement_mrid": "_be8d2d4e-519d-46d6-a850-a281041e43ea"
                },
                {
                    "angle": -36.1653929317239,
                    "magnitude": 137.366705292705,
                    "measurement_mrid": "_68172e95-fcd3-4f71-a01a-e9dc883854a2"
                },
                {
                    "angle": -36.1653929317239,
                    "magnitude": 137.366705292705,
                    "measurement_mrid": "_9790351d-215a-4d2f-a2b8-8a965a4803a7"
                },
                {
                    "angle": -155.176164893717,
                    "magnitude": 7682.15335651855,
                    "measurement_mrid": "_39ca007d-5acf-4224-bd4e-ff0538863695"
                },
                {
                    "angle": -34.8552560838498,
                    "magnitude": 7728.219782742,
                    "measurement_mrid": "_3b19317a-f4c6-4d64-ab4e-964cedc9b939"
                },
                {
                    "angle": 85.6376379879688,
                    "magnitude": 7416.78308853219,
                    "measurement_mrid": "_f0a59de4-30a9-417b-a0ed-af1dcea53a35"
                },
                {
                    "angle": -156.209683746078,
                    "magnitude": 128.119989801898,
                    "measurement_mrid": "_77b982bf-46cb-40c8-9cc0-24524e01edb1"
                },
                {
                    "angle": -156.183534955604,
                    "magnitude": 127.600102234559,
                    "measurement_mrid": "_b7dbbe44-6e72-4218-8c38-5ea9aee29cad"
                },
                {
                    "angle": -151.722174494149,
                    "magnitude": 7321.69990512566,
                    "measurement_mrid": "_e4a8d8de-0772-457e-827f-6e40254ca60d"
                },
                {
                    "angle": -35.8441423505878,
                    "magnitude": 8249.48907485074,
                    "measurement_mrid": "_774a6720-5aaf-4a20-9dc4-beaf392401d5"
                },
                {
                    "angle": -156.183822481811,
                    "magnitude": 127.598132973254,
                    "measurement_mrid": "_39d75fab-6b72-4064-800c-745a21c2735f"
                },
                {
                    "angle": -156.209971506254,
                    "magnitude": 128.118020941285,
                    "measurement_mrid": "_80716219-ffb1-40b5-8769-22cd717c4fac"
                },
                {
                    "angle": -36.1619361951608,
                    "magnitude": 136.924626495756,
                    "measurement_mrid": "_1208e7da-7d4c-4574-8383-43812bb63f1d"
                },
                {
                    "angle": -36.1951030326541,
                    "magnitude": 137.635297769847,
                    "measurement_mrid": "_b652c78f-912a-4b03-92b4-4b8d08a36327"
                },
                {
                    "angle": -156.717989745978,
                    "magnitude": 131.088126740923,
                    "measurement_mrid": "_59daf521-483a-46ad-88be-a7006055ecb4"
                },
                {
                    "angle": -156.743446231377,
                    "magnitude": 131.608013784053,
                    "measurement_mrid": "_ae67d833-0211-4d14-b9c3-2859ee2d2418"
                },
                {
                    "angle": -155.578387897622,
                    "magnitude": 127.502866537385,
                    "measurement_mrid": "_07c9e5e7-e382-445c-9c8d-0c2877d26182"
                },
                {
                    "angle": -155.567895235805,
                    "magnitude": 127.295019091861,
                    "measurement_mrid": "_3f15e823-524d-4ed9-9e43-c85df14473bd"
                },
                {
                    "angle": -156.381600383334,
                    "magnitude": 7898.94828987426,
                    "measurement_mrid": "_a0afe6d1-d263-4e58-9c70-e13ccee2965b"
                },
                {
                    "angle": -35.5656860108214,
                    "magnitude": 8329.11716687008,
                    "measurement_mrid": "_24bb12da-cc3f-4401-a602-d01ef0851f9c"
                },
                {
                    "angle": -154.944208377386,
                    "magnitude": 7728.6140090566,
                    "measurement_mrid": "_042f0dbd-9494-44a0-90b3-4d8193c46d43"
                },
                {
                    "angle": -34.7119207991389,
                    "magnitude": 7769.09622183581,
                    "measurement_mrid": "_b2539400-87e4-4c0e-aab2-837443e6b203"
                },
                {
                    "angle": 85.7626571721431,
                    "magnitude": 7424.23830967502,
                    "measurement_mrid": "_edc36efd-7f3e-48d0-8934-15a3feb7fb07"
                },
                {
                    "angle": -35.8034099896856,
                    "magnitude": 8264.88169136493,
                    "measurement_mrid": "_6249bfe3-6224-486d-9deb-5d09709c67c7"
                },
                {
                    "angle": -156.399209121192,
                    "magnitude": 7903.97911541891,
                    "measurement_mrid": "_0379b0d7-25f8-4982-a9c1-b13d5cf873e4"
                },
                {
                    "angle": 85.4511944291019,
                    "magnitude": 122.576741673571,
                    "measurement_mrid": "_5d8fb1b6-4acc-42bb-9196-36b06d4701d7"
                },
                {
                    "angle": 85.4511944291019,
                    "magnitude": 122.576741673571,
                    "measurement_mrid": "_ba5047be-6716-4f8a-9e26-bf51cf94825b"
                },
                {
                    "angle": -156.438329086447,
                    "magnitude": 7961.39008804098,
                    "measurement_mrid": "_79d70b82-9d32-4633-a407-3624d6e2c2f6"
                },
                {
                    "angle": 86.4207752643018,
                    "magnitude": 7384.72203186749,
                    "measurement_mrid": "_d09da49e-ca6e-4a50-81bc-5964af0082a2"
                },
                {
                    "angle": -35.7197570565358,
                    "magnitude": 8252.70049060894,
                    "measurement_mrid": "_17c47502-83b9-4c8c-bd76-f148c476df21"
                },
                {
                    "angle": -35.7892760067202,
                    "magnitude": 8293.44555714719,
                    "measurement_mrid": "_723473e2-cc75-4a03-a0e9-5a0b14560768"
                },
                {
                    "angle": 85.9416843497002,
                    "magnitude": 121.490086086572,
                    "measurement_mrid": "_73b5a7a4-8e71-4e56-96da-88838d135434"
                },
                {
                    "angle": 85.9416843497002,
                    "magnitude": 121.490086086572,
                    "measurement_mrid": "_c18fcebd-0d22-4851-b62a-e2fd5c0e0236"
                },
                {
                    "angle": -33.3726984219203,
                    "magnitude": 121.164490962588,
                    "measurement_mrid": "_776a2c5d-980e-4749-bb0e-fdffe29bd082"
                },
                {
                    "angle": -33.3726984219203,
                    "magnitude": 121.164490962588,
                    "measurement_mrid": "_f6413baf-0409-4201-98ae-5458d098f73b"
                },
                {
                    "angle": 86.2838872714361,
                    "magnitude": 7342.34889297807,
                    "measurement_mrid": "_cb89df75-65a2-41d1-87c4-d63d255403cb"
                },
                {
                    "angle": -34.7699855504392,
                    "magnitude": 128.501813393149,
                    "measurement_mrid": "_c68c58c1-2a0c-4255-949a-3d6e7f6f2d8f"
                },
                {
                    "angle": -34.7936132657676,
                    "magnitude": 128.975761537392,
                    "measurement_mrid": "_d0962a4e-330a-4fa2-8364-f27ecbb4a783"
                },
                {
                    "angle": -156.19647711708,
                    "magnitude": 128.232588928371,
                    "measurement_mrid": "_2c077dc0-3dda-4ed5-a5be-b87a63a64337"
                },
                {
                    "angle": -156.170350931065,
                    "magnitude": 127.712701713654,
                    "measurement_mrid": "_c16d829d-656b-4946-9ea2-8177efc67a6b"
                },
                {
                    "angle": -35.6585308457556,
                    "magnitude": 131.825982911037,
                    "measurement_mrid": "_98be8e9e-caba-4f93-845b-3f3fa23872f6"
                },
                {
                    "angle": -35.6585308457556,
                    "magnitude": 131.825982911037,
                    "measurement_mrid": "_ecd1fafe-df81-4c79-b358-ff3850c62414"
                },
                {
                    "angle": -32.7914700670768,
                    "magnitude": 120.981838771105,
                    "measurement_mrid": "_34c6031f-46bc-4333-a95c-1e81ee4a2dcb"
                },
                {
                    "angle": -32.7914700670768,
                    "magnitude": 120.981838771105,
                    "measurement_mrid": "_5a401a7c-adb9-4420-bdfe-6faf58210466"
                },
                {
                    "angle": -36.1810321293298,
                    "magnitude": 137.279405675856,
                    "measurement_mrid": "_2cd8a70c-bf4b-400f-b975-c0523f24b5f9"
                },
                {
                    "angle": -36.1810321293298,
                    "magnitude": 137.279405675856,
                    "measurement_mrid": "_669bd333-0cb8-4c72-8359-793d144c75b9"
                },
                {
                    "angle": -36.2611921346778,
                    "magnitude": 136.040503008782,
                    "measurement_mrid": "_7ca3bb6d-2847-4b3b-956c-beec43d5f832"
                },
                {
                    "angle": -36.2834891423988,
                    "magnitude": 136.51445750242,
                    "measurement_mrid": "_ed8d5f9e-9c7d-4e67-a3bb-06b59e03d237"
                },
                {
                    "angle": 87.0189729193997,
                    "magnitude": 121.051334391448,
                    "measurement_mrid": "_6fc1be5c-45fe-42de-9ae5-454fb8e948b9"
                },
                {
                    "angle": 87.047891707686,
                    "magnitude": 120.507932239804,
                    "measurement_mrid": "_99dcdf39-43a5-4d89-a57b-08483f7ed609"
                },
                {
                    "angle": 85.1321969833114,
                    "magnitude": 122.504749683734,
                    "measurement_mrid": "_5caddf73-9b31-4a41-98da-cc7b6863b89c"
                },
                {
                    "angle": 85.1321969833114,
                    "magnitude": 122.504749683734,
                    "measurement_mrid": "_d20e7b4e-f1d4-4b72-b946-b3d1dc9b2ad7"
                },
                {
                    "angle": 86.5994527267458,
                    "magnitude": 122.135295328866,
                    "measurement_mrid": "_64b203dc-9e80-45ee-90fe-f9238116e61d"
                },
                {
                    "angle": 86.6424601569837,
                    "magnitude": 121.319915154171,
                    "measurement_mrid": "_c6b84e5b-d593-4122-9222-21703b9a571d"
                },
                {
                    "angle": -153.551137881238,
                    "magnitude": 121.203585930346,
                    "measurement_mrid": "_53c2f04f-f2d3-4d87-b5ad-6eeff9442903"
                },
                {
                    "angle": -153.523507147566,
                    "magnitude": 120.683695691506,
                    "measurement_mrid": "_fe40c769-b8d6-4b83-a362-8263214aff87"
                },
                {
                    "angle": 86.6830040965117,
                    "magnitude": 119.587539337548,
                    "measurement_mrid": "_4b5b444d-0623-470b-905b-40a34adc8386"
                },
                {
                    "angle": 86.6830040965117,
                    "magnitude": 119.587539337548,
                    "measurement_mrid": "_e24a33e6-8644-488a-a76b-ad0211fa0127"
                },
                {
                    "angle": -35.7952579246148,
                    "magnitude": 8287.92186488895,
                    "measurement_mrid": "_3938388d-ae43-4c56-8cc3-2d5f305743db"
                },
                {
                    "angle": 86.3901789465504,
                    "magnitude": 7367.793242837,
                    "measurement_mrid": "_9171d6e2-9322-4b69-97f8-56ea8c82abc4"
                },
                {
                    "angle": -156.439048465555,
                    "magnitude": 7960.4543562735,
                    "measurement_mrid": "_afba8d10-a115-4677-8791-a852e8877ae6"
                },
                {
                    "angle": 86.2330462184765,
                    "magnitude": 7396.92912202894,
                    "measurement_mrid": "_0366c403-9660-4b7a-b81a-ed5939c1378b"
                },
                {
                    "angle": -152.215914702384,
                    "magnitude": 121.082944800704,
                    "measurement_mrid": "_78ae3961-8b0c-402d-b025-eec28fc36fd0"
                },
                {
                    "angle": -152.2048571669,
                    "magnitude": 120.875099409393,
                    "measurement_mrid": "_f45f86cf-95fc-4462-a05e-ab4c79d073a6"
                },
                {
                    "angle": -34.9036331843412,
                    "magnitude": 128.724891697662,
                    "measurement_mrid": "_01e018b6-218d-4e4a-a2e7-f8d56d00e527"
                },
                {
                    "angle": -34.9036331843412,
                    "magnitude": 128.724891697662,
                    "measurement_mrid": "_e03a9e2a-4f87-4d17-8907-10adceaa4534"
                },
                {
                    "angle": -156.41592846386,
                    "magnitude": 7880.94859913626,
                    "measurement_mrid": "_1ed2f31b-6dae-44e7-bc29-589bfa5348de"
                },
                {
                    "angle": -156.389460716611,
                    "magnitude": 7909.33549816705,
                    "measurement_mrid": "_19bc3c67-fd28-4a78-b9e1-9ea8d742513b"
                },
                {
                    "angle": 87.3833531402157,
                    "magnitude": 7313.54264969706,
                    "measurement_mrid": "_1f2020b7-203b-450d-83e9-2f4e4eeb2af2"
                },
                {
                    "angle": -33.7796797703223,
                    "magnitude": 7235.51991913654,
                    "measurement_mrid": "_2756c73a-7af5-4c8f-a341-0bba3438d2d9"
                },
                {
                    "angle": -154.059072857939,
                    "magnitude": 7288.45921911875,
                    "measurement_mrid": "_91aa7f71-3ff1-45f8-b918-98b9b5dbd089"
                },
                {
                    "angle": 85.544811157234,
                    "magnitude": 121.743594435709,
                    "measurement_mrid": "_5c97e359-1314-4d9b-b1c7-228cd8e8c566"
                },
                {
                    "angle": 85.6310958424479,
                    "magnitude": 120.112762535883,
                    "measurement_mrid": "_79e91c7c-09d2-4bfe-b993-3bd00e9380f2"
                },
                {
                    "angle": -35.8663585457594,
                    "magnitude": 8237.1365242733,
                    "measurement_mrid": "_e1ab084a-6143-496d-a6c4-0eaf4fb173f8"
                },
                {
                    "angle": -34.5763290711952,
                    "magnitude": 7775.63166933243,
                    "measurement_mrid": "_84cdd57c-c862-42e8-872c-4b51161d59c4"
                },
                {
                    "angle": -34.8249206634219,
                    "magnitude": 7763.28767403574,
                    "measurement_mrid": "_657f7eec-d5d3-45f7-9b9f-3848657170e7"
                },
                {
                    "angle": -156.403184111608,
                    "magnitude": 7887.53385826074,
                    "measurement_mrid": "_cdbaa14d-61da-4a29-8837-afca21cb005e"
                },
                {
                    "angle": 86.1049876368768,
                    "magnitude": 7324.52453529195,
                    "measurement_mrid": "_c3891170-f84c-4e26-b98e-d682b3342820"
                },
                {
                    "angle": -156.40283867452,
                    "magnitude": 7887.72080194223,
                    "measurement_mrid": "_4f65b214-1b57-48b4-b8c0-1bec3e7f4251"
                },
                {
                    "angle": -153.171755056781,
                    "magnitude": 7319.5241205013,
                    "measurement_mrid": "_b6225162-3dcf-429e-96db-75cd81f632f8"
                },
                {
                    "angle": 87.7578740921728,
                    "magnitude": 7306.96733972233,
                    "measurement_mrid": "_92d19357-a7fd-4a57-8c5d-30fe518c8732"
                },
                {
                    "angle": -32.9064510285929,
                    "magnitude": 7324.29400382875,
                    "measurement_mrid": "_0940d3ef-f90d-41f9-8d72-336ac1903f40"
                },
                {
                    "angle": 87.5541759205628,
                    "magnitude": 7303.26054110651,
                    "measurement_mrid": "_352b5e19-f319-439f-b037-20aa7743aaf0"
                },
                {
                    "angle": -152.994007861984,
                    "magnitude": 7319.21776582594,
                    "measurement_mrid": "_bf8d3012-78ed-4f74-aae8-03f5afa9b2bc"
                },
                {
                    "angle": -34.6716497033328,
                    "magnitude": 118.954823666787,
                    "measurement_mrid": "_26eaf480-d62b-4ff2-9caf-36084bbed1d8"
                },
                {
                    "angle": -34.7098356394601,
                    "magnitude": 119.665490285919,
                    "measurement_mrid": "_44e5ce9a-bb26-455a-bf2b-e34eda1a4c7a"
                },
                {
                    "angle": -34.8234887909571,
                    "magnitude": 7764.03733947755,
                    "measurement_mrid": "_37dffec4-1cda-4c90-bc25-bf3807531b2c"
                },
                {
                    "angle": -155.082809374045,
                    "magnitude": 7720.78027714592,
                    "measurement_mrid": "_7bf6dade-9527-4c64-8680-b120c83a0221"
                },
                {
                    "angle": 85.6536633657277,
                    "magnitude": 7427.11877907393,
                    "measurement_mrid": "_7e1068c0-06aa-4021-ba92-a6cc72aa3910"
                },
                {
                    "angle": -156.397997558506,
                    "magnitude": 7904.63489012184,
                    "measurement_mrid": "_e5fc914b-e7da-444b-b9c3-0763d76ec83f"
                },
                {
                    "angle": -34.8247154716164,
                    "magnitude": 7763.3951920777,
                    "measurement_mrid": "_a05fd95b-7567-4001-98a1-70a1313c9875"
                },
                {
                    "angle": -34.8246108760289,
                    "magnitude": 7763.45073405231,
                    "measurement_mrid": "_08ecea27-2ed5-474b-8eee-ba9834c370ae"
                },
                {
                    "angle": -156.866601791991,
                    "magnitude": 130.465369353796,
                    "measurement_mrid": "_18ff7a44-4a6f-4877-9058-cba40fe5def9"
                },
                {
                    "angle": -156.856336263094,
                    "magnitude": 130.257524882585,
                    "measurement_mrid": "_47c8c16b-73d9-4d5b-8c51-c74e5bcf2ac2"
                },
                {
                    "angle": 87.7870818169585,
                    "magnitude": 7306.63022843244,
                    "measurement_mrid": "_cc72ccf3-afaf-43a5-8972-ba302f6a734a"
                },
                {
                    "angle": -152.918957637541,
                    "magnitude": 7319.54051792992,
                    "measurement_mrid": "_dd7e668a-540f-4dbf-b312-07025101afef"
                },
                {
                    "angle": -32.8167612244214,
                    "magnitude": 7305.62364755347,
                    "measurement_mrid": "_e64f8955-81ab-4c1a-9f31-53e8f36d09ea"
                },
                {
                    "angle": -35.758721388739,
                    "magnitude": 8301.35438497695,
                    "measurement_mrid": "_e523ae28-938b-486c-a6aa-4b3003b86322"
                },
                {
                    "angle": -35.6933415322032,
                    "magnitude": 8324.5499209948,
                    "measurement_mrid": "_a01e94c6-263d-46fa-94ec-748d71ebd3ae"
                },
                {
                    "angle": -155.614216534515,
                    "magnitude": 127.290442415911,
                    "measurement_mrid": "_1aff5318-e24b-4184-8f8c-a1deb1d057ab"
                },
                {
                    "angle": -155.614216534515,
                    "magnitude": 127.290442415911,
                    "measurement_mrid": "_d76d5c95-3c37-47e4-9506-bdfad0744e91"
                },
                {
                    "angle": -35.8752188251001,
                    "magnitude": 8234.13515334322,
                    "measurement_mrid": "_7c09d25d-8d4e-4496-a155-4bf41124300e"
                },
                {
                    "angle": 86.4546960698029,
                    "magnitude": 7348.23905352545,
                    "measurement_mrid": "_f2ef639c-cc26-4610-a413-acb8e3289f3a"
                },
                {
                    "angle": 86.4513186488195,
                    "magnitude": 7350.8222859241,
                    "measurement_mrid": "_3823aecd-006d-474c-9037-a0321354a761"
                },
                {
                    "angle": -35.6169887372908,
                    "magnitude": 8314.16222986394,
                    "measurement_mrid": "_158f3323-6aed-4dc3-a8bc-983ad5693e80"
                },
                {
                    "angle": 86.4477299827121,
                    "magnitude": 7354.94831460778,
                    "measurement_mrid": "_bd6c86e7-ed63-461d-a561-6477a2fe9b44"
                },
                {
                    "angle": -156.142360188739,
                    "magnitude": 7985.24700492422,
                    "measurement_mrid": "_f98bb798-cd29-4eac-9acd-b2e4ae45fd0c"
                },
                {
                    "angle": 86.4475090792757,
                    "magnitude": 7355.38351889967,
                    "measurement_mrid": "_6e3f45e6-459c-44ae-bf19-6aa9c04c24ed"
                },
                {
                    "angle": 86.4202445840566,
                    "magnitude": 7381.53776721658,
                    "measurement_mrid": "_7a03507f-ef14-44e3-ba3a-269e48e06a61"
                },
                {
                    "angle": 86.4192380935908,
                    "magnitude": 7381.88465076955,
                    "measurement_mrid": "_bb35f440-d2eb-4d7a-82d6-7405e89b0a43"
                },
                {
                    "angle": 86.4190249852493,
                    "magnitude": 7381.76984146454,
                    "measurement_mrid": "_c5a86379-88a3-46cd-85e5-1d8927287c01"
                },
                {
                    "angle": -35.6380335967992,
                    "magnitude": 8303.03208729082,
                    "measurement_mrid": "_1b0cb767-100a-4103-a356-0f75ee67b12d"
                },
                {
                    "angle": -153.471838861666,
                    "magnitude": 121.162202080634,
                    "measurement_mrid": "_6d731e18-9eb2-4e61-885e-0e707270374d"
                },
                {
                    "angle": -153.444198066073,
                    "magnitude": 120.642311517113,
                    "measurement_mrid": "_aa93bda1-6e8c-41f6-9ce4-c02f5b5369fb"
                },
                {
                    "angle": 86.3366417319479,
                    "magnitude": 7332.08539262773,
                    "measurement_mrid": "_fd46a5d4-320b-42b1-9b39-443e0a647c82"
                },
                {
                    "angle": -156.874558151926,
                    "magnitude": 130.706438387969,
                    "measurement_mrid": "_3575cb20-f92a-4d3e-abad-3dd5dac6ad53"
                },
                {
                    "angle": -156.859174453982,
                    "magnitude": 130.394400790081,
                    "measurement_mrid": "_78c25488-81ae-4281-80d0-a8a499563b82"
                },
                {
                    "angle": -156.453947197479,
                    "magnitude": 7876.88138095192,
                    "measurement_mrid": "_0626e11a-bd09-4877-88fc-73f1f4df5af3"
                },
                {
                    "angle": -33.4671282758038,
                    "magnitude": 121.190718258911,
                    "measurement_mrid": "_18f22f61-2e68-4901-be7b-bba3964c0f5d"
                },
                {
                    "angle": -33.4821847521925,
                    "magnitude": 121.474975495529,
                    "measurement_mrid": "_62d7fb54-d249-47e6-9879-be6675da4b2c"
                },
                {
                    "angle": -36.1852817732366,
                    "magnitude": 137.233485359793,
                    "measurement_mrid": "_0b3d9ab6-f004-4948-90df-a554cfe1e0ab"
                },
                {
                    "angle": -36.1852817732366,
                    "magnitude": 137.233485359793,
                    "measurement_mrid": "_7de591c0-a037-4651-a5d3-34b64e9bd482"
                },
                {
                    "angle": 86.7329942448759,
                    "magnitude": 120.852501509845,
                    "measurement_mrid": "_3b8297b2-ed27-403b-be46-3afd185a1c98"
                },
                {
                    "angle": 86.7214225314206,
                    "magnitude": 121.069964884956,
                    "measurement_mrid": "_d773069e-1256-4da0-8a84-55fc264bba61"
                },
                {
                    "angle": 88.3426019046942,
                    "magnitude": 119.131820755789,
                    "measurement_mrid": "_476e7c75-64c4-4f22-a27f-629aa1c4aedf"
                },
                {
                    "angle": 88.3426019046942,
                    "magnitude": 119.131820755789,
                    "measurement_mrid": "_74f93528-2dd5-4431-985c-84d72611f659"
                },
                {
                    "angle": -36.1824439915878,
                    "magnitude": 137.260098057575,
                    "measurement_mrid": "_02be8c35-f887-4300-aac8-7b2302681aa5"
                },
                {
                    "angle": -36.1824439915878,
                    "magnitude": 137.260098057575,
                    "measurement_mrid": "_59b4b700-42d3-4e46-a1a0-929341bedf70"
                },
                {
                    "angle": -154.067633466395,
                    "magnitude": 7286.90571908562,
                    "measurement_mrid": "_36fd6a21-82eb-4c00-a630-3a0389ff70cc"
                },
                {
                    "angle": 86.3373781719651,
                    "magnitude": 7332.30043197125,
                    "measurement_mrid": "_996506a8-fd71-49d0-9aaf-46a0661f4251"
                },
                {
                    "angle": -36.0820287542587,
                    "magnitude": 136.545616725922,
                    "measurement_mrid": "_871a1804-9922-468a-86ac-79bf8f71affb"
                },
                {
                    "angle": -36.10424596007,
                    "magnitude": 137.019570656026,
                    "measurement_mrid": "_c69f6384-5909-47a0-93dd-4da62b5cd133"
                },
                {
                    "angle": 86.3887660114377,
                    "magnitude": 7365.342104737,
                    "measurement_mrid": "_57ee1ce3-072a-4ced-8351-e6d0a09d0d62"
                },
                {
                    "angle": 85.1208425577639,
                    "magnitude": 122.830008797177,
                    "measurement_mrid": "_7fd1a5d6-951a-48b8-a1d4-20be1db71f97"
                },
                {
                    "angle": 85.1493405628874,
                    "magnitude": 122.286607443972,
                    "measurement_mrid": "_a3e7af02-0fbf-44bc-b52e-5f12f72be924"
                },
                {
                    "angle": -36.1444982937416,
                    "magnitude": 136.659293679194,
                    "measurement_mrid": "_44e44717-a208-487c-92d5-9ae0488f29bb"
                },
                {
                    "angle": -36.1222241725196,
                    "magnitude": 136.185338856725,
                    "measurement_mrid": "_7443c13b-6593-4f13-ad9a-4159c7d34461"
                },
                {
                    "angle": -36.0695313621497,
                    "magnitude": 136.308716596649,
                    "measurement_mrid": "_0e3735a0-49dc-4c58-a397-48082be124cc"
                },
                {
                    "angle": -36.1138869682936,
                    "magnitude": 137.256645742923,
                    "measurement_mrid": "_839c8bcf-d983-439f-b424-80bf8f45ccff"
                },
                {
                    "angle": -156.547959254645,
                    "magnitude": 131.446284224438,
                    "measurement_mrid": "_0548873c-b145-43d8-8735-3b56a63c8938"
                },
                {
                    "angle": -156.598510442589,
                    "magnitude": 132.485550648953,
                    "measurement_mrid": "_8d0d7d1a-413e-47ef-a0f4-b8f740d56073"
                },
                {
                    "angle": -36.200990341037,
                    "magnitude": 136.766099305434,
                    "measurement_mrid": "_2025a616-4031-470c-b246-a4d7b55ba04f"
                },
                {
                    "angle": -36.200990341037,
                    "magnitude": 136.766099305434,
                    "measurement_mrid": "_648ac48c-97f7-44ff-8d3a-d73608bdb043"
                },
                {
                    "angle": -34.2206398822002,
                    "magnitude": 120.525557923044,
                    "measurement_mrid": "_77303c19-d37d-4bae-bfa3-1d7f859260ba"
                },
                {
                    "angle": -34.2206398822002,
                    "magnitude": 120.525557923044,
                    "measurement_mrid": "_b5cbca30-acfe-4651-9d4e-ffa3a1d6e29a"
                },
                {
                    "angle": 85.8923475862885,
                    "magnitude": 121.920387060651,
                    "measurement_mrid": "_600566cb-becf-40b8-80c8-5b5182221cbd"
                },
                {
                    "angle": 85.9095686086598,
                    "magnitude": 121.594456420588,
                    "measurement_mrid": "_e11eb31c-7bcd-42c2-a597-7959e7da1304"
                },
                {
                    "angle": -36.1482502145813,
                    "magnitude": 137.427055373504,
                    "measurement_mrid": "_18f713b0-9da0-4a45-b2a5-0cec654850b4"
                },
                {
                    "angle": -36.1482502145813,
                    "magnitude": 137.427055373504,
                    "measurement_mrid": "_27085e8e-78d5-4f77-a5bd-fc1bc9060af0"
                },
                {
                    "angle": -35.9850557033766,
                    "magnitude": 137.695883222763,
                    "measurement_mrid": "_2cc83a23-5a4d-4e9c-bdd9-518921d50e2b"
                },
                {
                    "angle": -35.9717938674668,
                    "magnitude": 137.411620173959,
                    "measurement_mrid": "_fd487055-d946-4397-97ce-d41df6baab41"
                },
                {
                    "angle": 86.9419565915371,
                    "magnitude": 121.226658341223,
                    "measurement_mrid": "_bf2dd0da-033c-4f15-b51e-0388c7dd0f67"
                },
                {
                    "angle": 86.9852861560544,
                    "magnitude": 120.411277780387,
                    "measurement_mrid": "_f9a5d47e-0590-45cc-8617-eced21fb16a2"
                },
                {
                    "angle": 85.9058400231508,
                    "magnitude": 122.09534434413,
                    "measurement_mrid": "_43f48b67-db3b-491b-8e9e-90a585914786"
                },
                {
                    "angle": 85.9230372497989,
                    "magnitude": 121.769414628606,
                    "measurement_mrid": "_e3f4d4f2-8a5f-41d5-9795-a96278eba9c9"
                },
                {
                    "angle": 85.9700317994236,
                    "magnitude": 120.982565088623,
                    "measurement_mrid": "_6df099bf-7cb9-4949-9246-cc9c42e6f650"
                },
                {
                    "angle": 85.9700317994236,
                    "magnitude": 120.982565088623,
                    "measurement_mrid": "_d528a776-8594-4a6a-bb1f-708119c48752"
                },
                {
                    "angle": 86.7973004837866,
                    "magnitude": 120.871856762049,
                    "measurement_mrid": "_5c0cb582-32fa-4b6f-b4a3-d8bda3586ff1"
                },
                {
                    "angle": 86.8262630760503,
                    "magnitude": 120.328456179699,
                    "measurement_mrid": "_bdc2e455-d036-4dad-ac33-588973e77435"
                },
                {
                    "angle": -155.730369216885,
                    "magnitude": 7736.64361082796,
                    "measurement_mrid": "_58b56b2b-9246-463b-a584-6262861004b2"
                },
                {
                    "angle": 86.2334170155858,
                    "magnitude": 7397.12144060626,
                    "measurement_mrid": "_a5dc7aa9-9926-4351-b1dc-5e5cd2366c79"
                },
                {
                    "angle": -156.419826035523,
                    "magnitude": 7878.78456611088,
                    "measurement_mrid": "_a2f3dc25-554c-4036-8470-4a9ee2e1664f"
                },
                {
                    "angle": 86.2333589688453,
                    "magnitude": 7397.09031267033,
                    "measurement_mrid": "_0272b502-27e3-4ae7-ac2a-eb385c26fb3a"
                },
                {
                    "angle": -156.335228499178,
                    "magnitude": 128.486284287537,
                    "measurement_mrid": "_56e76898-7794-4e2d-8c46-f6bc7fc7a32e"
                },
                {
                    "angle": -156.319577280025,
                    "magnitude": 128.174247982227,
                    "measurement_mrid": "_99b6136a-0347-416d-872b-26f0031e7ff8"
                },
                {
                    "angle": -33.7802645708668,
                    "magnitude": 7239.37029650143,
                    "measurement_mrid": "_3dc618f1-85c9-4391-93b6-6aaedf45430f"
                },
                {
                    "angle": -154.054334855954,
                    "magnitude": 7293.59339098145,
                    "measurement_mrid": "_6080f7fa-4103-4d72-8ea1-c6ab2a610c3d"
                },
                {
                    "angle": 87.3863949404569,
                    "magnitude": 7316.90635115397,
                    "measurement_mrid": "_b9530b81-28c2-4632-b0bb-719b648a92dc"
                },
                {
                    "angle": 87.386458167863,
                    "magnitude": 7316.92843493533,
                    "measurement_mrid": "_1641d88d-575c-4d44-ad97-7d64b0dedfb9"
                },
                {
                    "angle": -154.053868852078,
                    "magnitude": 7293.90249292081,
                    "measurement_mrid": "_8bfe13c7-0c5a-4519-b773-bf817cafa4f5"
                },
                {
                    "angle": -33.7806297129054,
                    "magnitude": 7239.47267858678,
                    "measurement_mrid": "_93920b56-1ce8-463a-a000-f2ca1c2cea0d"
                },
                {
                    "angle": 86.9604590693231,
                    "magnitude": 120.029588158311,
                    "measurement_mrid": "_8b1bd8c1-f923-4287-9cfb-36f669f9bf69"
                },
                {
                    "angle": 86.874109073301,
                    "magnitude": 121.660417747046,
                    "measurement_mrid": "_fd17f376-d6c0-4495-b4c4-636e26ab4d1f"
                },
                {
                    "angle": -156.840472967042,
                    "magnitude": 130.178749765657,
                    "measurement_mrid": "_0705ce9e-d441-4045-9812-d3ec48f9afae"
                },
                {
                    "angle": -156.866104087915,
                    "magnitude": 130.698637903794,
                    "measurement_mrid": "_7a6222d7-af55-433a-bdec-db92f562ad50"
                },
                {
                    "angle": 86.2511947993562,
                    "magnitude": 7406.3241859944,
                    "measurement_mrid": "_1c4e13e1-8c09-46e3-898c-27713b838880"
                },
                {
                    "angle": 86.2332250084552,
                    "magnitude": 7397.02039278894,
                    "measurement_mrid": "_609cee29-7c0a-4f2d-862d-aa4ab78c5e47"
                },
                {
                    "angle": -156.145930047058,
                    "magnitude": 8000.37579004438,
                    "measurement_mrid": "_17c6cb73-61fe-4f9a-a7dc-6c4136afc757"
                },
                {
                    "angle": -35.5790596746398,
                    "magnitude": 8347.63664535544,
                    "measurement_mrid": "_272b4f92-e76d-4b29-92db-7f0e08388e1a"
                },
                {
                    "angle": 86.4428202486024,
                    "magnitude": 7381.85637617419,
                    "measurement_mrid": "_95afd482-da0d-4146-9c7e-467a3a62d579"
                },
                {
                    "angle": 87.1973505121854,
                    "magnitude": 7240.11476627127,
                    "measurement_mrid": "_a85cc832-fc76-4786-8dc0-f00a3a4c8669"
                },
                {
                    "angle": -35.2684263360317,
                    "magnitude": 127.352430951751,
                    "measurement_mrid": "_8980707d-13e8-4043-bd08-2b840d16aaec"
                },
                {
                    "angle": -35.2779849890243,
                    "magnitude": 127.54211595881,
                    "measurement_mrid": "_a3658ef8-be54-4180-85f9-bab5d7c39fef"
                },
                {
                    "angle": -34.8655850736545,
                    "magnitude": 7732.5253478801,
                    "measurement_mrid": "_17a9fc7c-b6f5-4615-968e-7d11f25e4565"
                },
                {
                    "angle": -35.565427980789,
                    "magnitude": 8329.26425723247,
                    "measurement_mrid": "_6f21585b-3033-46c5-a76e-3cf45e2292d1"
                },
                {
                    "angle": 87.4319598394583,
                    "magnitude": 120.680312058847,
                    "measurement_mrid": "_43a72990-8dba-43e6-967a-831bbafbcd21"
                },
                {
                    "angle": 87.4319598394583,
                    "magnitude": 120.680312058847,
                    "measurement_mrid": "_9ce39adb-10ef-42eb-a889-c5f2c6b10716"
                },
                {
                    "angle": 86.7370040243269,
                    "magnitude": 120.019777783494,
                    "measurement_mrid": "_70243581-decd-42dd-ba4b-49e732f72de9"
                },
                {
                    "angle": 86.7370040243269,
                    "magnitude": 120.019777783494,
                    "measurement_mrid": "_a42716ad-3a9e-4193-b115-4895a67d7235"
                },
                {
                    "angle": -35.9879944615502,
                    "magnitude": 137.469441514781,
                    "measurement_mrid": "_202d90a5-56e8-47a5-83ce-2b94f1676197"
                },
                {
                    "angle": -36.0100666199456,
                    "magnitude": 137.943394384379,
                    "measurement_mrid": "_d177c873-f167-4471-8881-c4824c334b36"
                },
                {
                    "angle": -34.8512171911823,
                    "magnitude": 7703.56011821948,
                    "measurement_mrid": "_73944cbf-b525-4188-9109-dbd227cf9563"
                },
                {
                    "angle": 85.64663948915,
                    "magnitude": 7417.01163184235,
                    "measurement_mrid": "_53257719-24f4-4c93-94b5-90ee0122e9f2"
                },
                {
                    "angle": -156.47344409768,
                    "magnitude": 7870.816655122,
                    "measurement_mrid": "_fde6f9fe-efa8-4c7d-81d7-8af46c1b34cf"
                },
                {
                    "angle": -35.8670553162716,
                    "magnitude": 8236.75817711305,
                    "measurement_mrid": "_b8b8b604-77e7-40ea-bff6-fce6601c6d69"
                },
                {
                    "angle": -36.1379557470413,
                    "magnitude": 136.379318888403,
                    "measurement_mrid": "_05b4a1ab-065f-4f74-9c31-eee3a8aa7fc9"
                },
                {
                    "angle": -36.1379557470413,
                    "magnitude": 136.379318888403,
                    "measurement_mrid": "_9b66754a-176e-4416-a395-34ed28465afc"
                },
                {
                    "angle": -152.223721437302,
                    "magnitude": 121.241031080216,
                    "measurement_mrid": "_478e59aa-774f-4e84-a575-3557b994e4e4"
                },
                {
                    "angle": -152.196099158776,
                    "magnitude": 120.721139693527,
                    "measurement_mrid": "_919ce088-2795-424d-a885-2a1036fda864"
                },
                {
                    "angle": 86.3470071383697,
                    "magnitude": 7335.10428366374,
                    "measurement_mrid": "_8ba973af-0b9f-406d-86eb-d81e866d8a88"
                },
                {
                    "angle": -155.706730611977,
                    "magnitude": 7749.21882518221,
                    "measurement_mrid": "_fd90a53f-1aa8-475d-b27e-91d64c689ec1"
                },
                {
                    "angle": -155.713880685207,
                    "magnitude": 126.387745261012,
                    "measurement_mrid": "_b1fe3b51-68f3-4f84-8cd3-5b721c095266"
                },
                {
                    "angle": -155.713880685207,
                    "magnitude": 126.387745261012,
                    "measurement_mrid": "_b5445866-dea0-45aa-9fcd-b4653067f314"
                },
                {
                    "angle": -33.8611484391705,
                    "magnitude": 7282.7635599471,
                    "measurement_mrid": "_4872e0e1-8f30-4af8-94b0-3933214bc979"
                },
                {
                    "angle": -156.380817878992,
                    "magnitude": 7899.36771391674,
                    "measurement_mrid": "_de69918c-5c04-43b2-85bf-9ab54720cd8a"
                },
                {
                    "angle": -35.5703508192149,
                    "magnitude": 8359.2205106913,
                    "measurement_mrid": "_66160ca0-9df8-4b3e-b2c9-fca27598e0f4"
                },
                {
                    "angle": -35.7077321296734,
                    "magnitude": 8261.3960104667,
                    "measurement_mrid": "_5348cc1d-9e12-4503-a667-57382d983e18"
                },
                {
                    "angle": -36.2004352838512,
                    "magnitude": 136.769724627064,
                    "measurement_mrid": "_372b233a-d3d8-4f38-a194-738283a0a474"
                },
                {
                    "angle": -36.2004352838512,
                    "magnitude": 136.769724627064,
                    "measurement_mrid": "_d1ae4802-749a-4c56-ad10-bb90897460ef"
                },
                {
                    "angle": -34.3643110257668,
                    "magnitude": 7780.97829407959,
                    "measurement_mrid": "_9d51f704-d50d-4d35-9ebb-e45c559bf601"
                },
                {
                    "angle": 86.2334443788345,
                    "magnitude": 7397.13553798724,
                    "measurement_mrid": "_dfaf7f07-f3e5-4944-8796-09b54c579b77"
                },
                {
                    "angle": -156.207303023196,
                    "magnitude": 127.771226359818,
                    "measurement_mrid": "_336a7086-22a9-49d3-bce4-bf81ab47ce86"
                },
                {
                    "angle": -156.207303023196,
                    "magnitude": 127.771226359818,
                    "measurement_mrid": "_975fb64a-d0dc-41d3-aa2b-b3b189531060"
                },
                {
                    "angle": -156.399156941641,
                    "magnitude": 7889.5359623176,
                    "measurement_mrid": "_b8a93e79-2166-44fa-a1ae-e478d327ce29"
                },
                {
                    "angle": -156.459684223146,
                    "magnitude": 7875.09469542586,
                    "measurement_mrid": "_73c7d633-31ed-46d3-af02-c667d202bad8"
                },
                {
                    "angle": -156.232691303536,
                    "magnitude": 7979.69060799037,
                    "measurement_mrid": "_c7081c6f-91f8-41d0-b4ae-5495fc879be8"
                },
                {
                    "angle": -35.588774559055,
                    "magnitude": 8339.24544724122,
                    "measurement_mrid": "_de58aa8d-5ed5-48a0-aa79-e41310e49b8b"
                },
                {
                    "angle": 86.4241576786324,
                    "magnitude": 7386.21386326983,
                    "measurement_mrid": "_f3369317-7a53-40c0-9161-395933339ad0"
                },
                {
                    "angle": -34.2208547081463,
                    "magnitude": 119.501547152606,
                    "measurement_mrid": "_e382a68f-2ea9-45e6-8e66-db10346f25fb"
                },
                {
                    "angle": -34.2361173683913,
                    "magnitude": 119.785805793011,
                    "measurement_mrid": "_ef67ed41-21b6-4fae-92b4-8ca3f0550bcf"
                },
                {
                    "angle": -156.400913821528,
                    "magnitude": 7903.05607413227,
                    "measurement_mrid": "_decb9548-c791-429d-87a6-2c494f78e010"
                },
                {
                    "angle": 88.4101412099399,
                    "magnitude": 119.239380219779,
                    "measurement_mrid": "_3880e525-be8b-454b-b212-a8cf822ed797"
                },
                {
                    "angle": 88.3809178705593,
                    "magnitude": 119.782782028474,
                    "measurement_mrid": "_9f2eca01-27aa-42a3-8d5f-a8dfd1923a4c"
                },
                {
                    "angle": 87.4323004399073,
                    "magnitude": 120.683072689223,
                    "measurement_mrid": "_99cfeb73-f452-4477-95a7-00d5d789d016"
                },
                {
                    "angle": 87.4323004399073,
                    "magnitude": 120.683072689223,
                    "measurement_mrid": "_f6b86ddf-a59b-4b23-b523-2a814163d685"
                },
                {
                    "angle": 86.2330906177497,
                    "magnitude": 7397.01109755102,
                    "measurement_mrid": "_53f0b7e9-6d16-4ef6-abf8-84a9d19ae0f1"
                },
                {
                    "angle": 87.0182356492493,
                    "magnitude": 7377.6443723812,
                    "measurement_mrid": "_8af79a23-d6e4-4e0b-9908-201cb2913171"
                },
                {
                    "angle": -36.2606402584311,
                    "magnitude": 136.342489208858,
                    "measurement_mrid": "_3196ae6f-5b96-43e3-9e43-00aafe827064"
                },
                {
                    "angle": -36.2606402584311,
                    "magnitude": 136.342489208858,
                    "measurement_mrid": "_cb25ce1b-c53b-4891-a7cc-7b5a7b31d21a"
                },
                {
                    "angle": -155.14495702295,
                    "magnitude": 7703.87008642403,
                    "measurement_mrid": "_ae5756c8-cb1f-4292-94d9-12cc7c543c97"
                },
                {
                    "angle": 85.6320777505506,
                    "magnitude": 7422.34872314771,
                    "measurement_mrid": "_bc7bf838-2929-4b07-bc07-515a8cad31c3"
                },
                {
                    "angle": -34.8614525146652,
                    "magnitude": 7745.22183055482,
                    "measurement_mrid": "_e24476a7-7064-4db8-9c32-6a6aaaf5a37f"
                },
                {
                    "angle": 88.2777242052243,
                    "magnitude": 7296.78062912976,
                    "measurement_mrid": "_342f6e5d-9754-4d81-9944-0f13cd2e9d7d"
                },
                {
                    "angle": -33.0450257128608,
                    "magnitude": 7291.63630546353,
                    "measurement_mrid": "_3f8e45de-133d-4e1c-b964-95a4d44a5826"
                },
                {
                    "angle": 87.6826217618192,
                    "magnitude": 7308.43762625204,
                    "measurement_mrid": "_6d03ac28-094c-4666-824b-7674da2caead"
                },
                {
                    "angle": -153.181201195918,
                    "magnitude": 7314.37840728944,
                    "measurement_mrid": "_d0c10638-31b5-425c-b65e-ef5288163ad8"
                },
                {
                    "angle": -153.671589072173,
                    "magnitude": 121.223159422262,
                    "measurement_mrid": "_7837ce3c-3e71-491e-8d6f-1dc1ca03e460"
                },
                {
                    "angle": -153.64396348258,
                    "magnitude": 120.70326869055,
                    "measurement_mrid": "_95f7e62d-b10f-49b3-845a-51d8bdd12184"
                },
                {
                    "angle": 86.3897665679869,
                    "magnitude": 7367.27205650246,
                    "measurement_mrid": "_f114ae3d-c35f-40a7-b88e-6857dd37bf31"
                },
                {
                    "angle": -35.8007593648005,
                    "magnitude": 8282.35373692322,
                    "measurement_mrid": "_14f4bd57-26b7-49d1-869f-b290dd677598"
                },
                {
                    "angle": 86.386825905642,
                    "magnitude": 7364.77480704508,
                    "measurement_mrid": "_3828876c-89e0-4275-8a16-fcea3e0ea67b"
                },
                {
                    "angle": -156.44234946867,
                    "magnitude": 7959.04272358645,
                    "measurement_mrid": "_7d48973e-0f30-428c-856f-af2fcf70cb22"
                },
                {
                    "angle": -156.791983339335,
                    "magnitude": 130.579893417831,
                    "measurement_mrid": "_10a3186f-4381-4903-a858-3f8daea2275b"
                },
                {
                    "angle": -156.830225647209,
                    "magnitude": 131.359467596737,
                    "measurement_mrid": "_c4067e2e-555c-4dda-849c-ff01268eb146"
                },
                {
                    "angle": -153.158607602306,
                    "magnitude": 7314.82005354223,
                    "measurement_mrid": "_697ede4c-7766-47d0-a846-d932260d5704"
                },
                {
                    "angle": 87.6915607847169,
                    "magnitude": 7308.27095789009,
                    "measurement_mrid": "_7458d3cc-5915-40c8-85a8-fc0d2c9e71b3"
                },
                {
                    "angle": -33.0254708101012,
                    "magnitude": 7292.83161976592,
                    "measurement_mrid": "_77779613-d473-4c50-ba48-3ed764d98861"
                },
                {
                    "angle": -35.7981613884859,
                    "magnitude": 8267.91158465973,
                    "measurement_mrid": "_d769db63-47c6-4e7d-b6f3-69330345402c"
                },
                {
                    "angle": -31.6963258871082,
                    "magnitude": 7317.52074838174,
                    "measurement_mrid": "_0e714072-8177-42a6-81fe-3ec069a1eef9"
                },
                {
                    "angle": 88.5871343305255,
                    "magnitude": 7288.325943705,
                    "measurement_mrid": "_65681b0a-ee64-4b2a-bf13-dfb858eada53"
                },
                {
                    "angle": -151.726195998652,
                    "magnitude": 7318.80494338865,
                    "measurement_mrid": "_76623b25-5227-4085-add4-741430569ce7"
                },
                {
                    "angle": 85.7480170194385,
                    "magnitude": 121.647740852581,
                    "measurement_mrid": "_1a49c965-bee0-438a-8dfa-f6e9916d66a4"
                },
                {
                    "angle": 85.7911946456435,
                    "magnitude": 120.832359495948,
                    "measurement_mrid": "_77c446e5-f9ec-4fd1-9112-20b667b497f7"
                },
                {
                    "angle": -155.683420119693,
                    "magnitude": 7761.84496205545,
                    "measurement_mrid": "_0aad8b41-802e-430f-b8d2-d5c199166c47"
                },
                {
                    "angle": 86.232661902702,
                    "magnitude": 121.939526816709,
                    "measurement_mrid": "_58f8e2c4-9543-4bda-96cc-a5b720bcf2f6"
                },
                {
                    "angle": 86.204080269587,
                    "magnitude": 122.482927835259,
                    "measurement_mrid": "_8d5f0bf3-1b88-4b3c-aabc-ae0353760f1f"
                },
                {
                    "angle": -156.875313979648,
                    "magnitude": 130.093067300123,
                    "measurement_mrid": "_581b1d78-2163-4234-90ac-f9737262324e"
                },
                {
                    "angle": -156.885591932273,
                    "magnitude": 130.30091237013,
                    "measurement_mrid": "_8367e17c-a80d-4f0a-bc8d-0bc22985b520"
                },
                {
                    "angle": -154.554115897929,
                    "magnitude": 120.433959829793,
                    "measurement_mrid": "_0d7b7b2c-7907-45fe-a958-b7307cc269d7"
                },
                {
                    "angle": -154.554115897929,
                    "magnitude": 120.433959829793,
                    "measurement_mrid": "_c0ed7b6c-8ace-4db2-9d97-89e54069e5f4"
                },
                {
                    "angle": -36.1106094817212,
                    "magnitude": 136.882474908788,
                    "measurement_mrid": "_12c230eb-c9c5-44d4-9b32-ad5db3df82c8"
                },
                {
                    "angle": -36.0972706272222,
                    "magnitude": 136.598211666907,
                    "measurement_mrid": "_4c709a6a-80c8-46c5-8c25-a093b437ce76"
                },
                {
                    "angle": 85.8285961943831,
                    "magnitude": 121.11958817101,
                    "measurement_mrid": "_43487fbb-e697-43ce-845e-aade50605d9e"
                },
                {
                    "angle": 85.8285961943831,
                    "magnitude": 121.11958817101,
                    "measurement_mrid": "_d83e01f2-990c-4697-875d-fdae58e362bc"
                },
                {
                    "angle": 85.7483862732443,
                    "magnitude": 122.35755005403,
                    "measurement_mrid": "_3b754997-2247-42ad-94ae-9edd5f78600f"
                },
                {
                    "angle": 85.7483862732443,
                    "magnitude": 122.35755005403,
                    "measurement_mrid": "_8060bf6d-f556-4065-ac4b-064df7a8d3be"
                },
                {
                    "angle": 87.2107116874876,
                    "magnitude": 7246.64396290774,
                    "measurement_mrid": "_e1d900a1-40f6-48c9-8afb-c5293ef13e23"
                },
                {
                    "angle": 87.2103134468848,
                    "magnitude": 7246.45323113789,
                    "measurement_mrid": "_93faf299-eeec-43b5-be83-e0b8d54e0032"
                },
                {
                    "angle": 87.2103932551776,
                    "magnitude": 7246.49189570237,
                    "measurement_mrid": "_3d931eb6-567a-4562-bc20-e88af1b58bae"
                },
                {
                    "angle": -34.891796741968,
                    "magnitude": 128.487920250632,
                    "measurement_mrid": "_6b1354d1-db68-449d-8e60-5db1b4c82a49"
                },
                {
                    "angle": -34.915426126549,
                    "magnitude": 128.961868618135,
                    "measurement_mrid": "_828f8157-42b8-47b6-bdb5-7364f014c9ae"
                },
                {
                    "angle": -156.971475681451,
                    "magnitude": 131.386427999062,
                    "measurement_mrid": "_89c1fd06-a885-48ef-bd18-28ce48a8e4c2"
                },
                {
                    "angle": -156.933239606927,
                    "magnitude": 130.606854756584,
                    "measurement_mrid": "_8bc6bca6-618c-48d0-ad6e-a34a33d174d0"
                },
                {
                    "angle": 86.4738857696148,
                    "magnitude": 7317.79756345403,
                    "measurement_mrid": "_2af0f102-3b98-4742-ad29-95a18df5ee1b"
                },
                {
                    "angle": -156.11886799136,
                    "magnitude": 7980.94643852824,
                    "measurement_mrid": "_5bcba4e5-7052-4bda-a5c8-2bdb2bfedfd1"
                },
                {
                    "angle": -35.7108407087267,
                    "magnitude": 8261.08040731922,
                    "measurement_mrid": "_e9dca704-b106-48ee-8e9e-2da198b3e61d"
                },
                {
                    "angle": 85.7686194718412,
                    "magnitude": 121.488064275504,
                    "measurement_mrid": "_12a5df5e-3b1e-4b30-b4d6-668f9cfcb5ef"
                },
                {
                    "angle": 85.7859023007204,
                    "magnitude": 121.162133711619,
                    "measurement_mrid": "_63c700aa-b1b3-4818-9f6a-da9fe9ced2d6"
                },
                {
                    "angle": 86.4349747269583,
                    "magnitude": 120.196223157021,
                    "measurement_mrid": "_0da30c84-2a5a-4c65-9881-1155b4046c2a"
                },
                {
                    "angle": 86.4349747269583,
                    "magnitude": 120.196223157021,
                    "measurement_mrid": "_87d50156-ce03-460b-a37c-ed94e8b364a5"
                },
                {
                    "angle": 86.426171402011,
                    "magnitude": 7387.29837289457,
                    "measurement_mrid": "_1475ae07-0c0b-400e-996b-8dc412164199"
                },
                {
                    "angle": -156.251769087891,
                    "magnitude": 7968.5587790359,
                    "measurement_mrid": "_72f06453-f270-4b93-ae18-8de2d66668fd"
                },
                {
                    "angle": -35.5787943141219,
                    "magnitude": 8334.37487248968,
                    "measurement_mrid": "_d115144d-b3ff-4133-b831-b40110901eb0"
                },
                {
                    "angle": 87.1266077195233,
                    "magnitude": 7368.59636457379,
                    "measurement_mrid": "_48cbc3b3-2cdd-4b2d-bc94-df2d946bde62"
                },
                {
                    "angle": 86.5130870796594,
                    "magnitude": 121.877849434406,
                    "measurement_mrid": "_40fb67d6-384d-416b-9bad-fc1b937563dd"
                },
                {
                    "angle": 86.5130870796594,
                    "magnitude": 121.877849434406,
                    "measurement_mrid": "_576a2a3b-2dc8-409d-8238-e3d17051f061"
                },
                {
                    "angle": -36.1696096613246,
                    "magnitude": 137.344013065817,
                    "measurement_mrid": "_4c72825e-e42b-4a55-a1dd-7a62eff00f22"
                },
                {
                    "angle": -36.1696096613246,
                    "magnitude": 137.344013065817,
                    "measurement_mrid": "_dd45e097-273f-4464-a04e-9ccf17498921"
                },
                {
                    "angle": -35.8453898415525,
                    "magnitude": 8248.7949802116,
                    "measurement_mrid": "_670a7987-5c91-4d1e-a83e-bb452b10b8e0"
                },
                {
                    "angle": -35.8953838302362,
                    "magnitude": 137.597443579366,
                    "measurement_mrid": "_6229fd55-7f2c-41cf-81d5-b0c8d3ce5b8e"
                },
                {
                    "angle": -35.8953838302362,
                    "magnitude": 137.597443579366,
                    "measurement_mrid": "_9388a635-d593-4587-b189-f6e0f661aac7"
                },
                {
                    "angle": -36.2625419840828,
                    "magnitude": 136.328615784411,
                    "measurement_mrid": "_3e6af5e4-afa0-4454-85c2-66d459059236"
                },
                {
                    "angle": -36.2625419840828,
                    "magnitude": 136.328615784411,
                    "measurement_mrid": "_e38ec07c-1fed-431c-97ff-5682404e2cc9"
                },
                {
                    "angle": -36.0109031213741,
                    "magnitude": 137.716903123783,
                    "measurement_mrid": "_51c64c8b-8ae5-456f-b5de-b8fcd18df788"
                },
                {
                    "angle": -36.0109031213741,
                    "magnitude": 137.716903123783,
                    "measurement_mrid": "_60668a62-81e6-4aa7-b95a-e146bd41dd2b"
                },
                {
                    "angle": -156.762005293264,
                    "magnitude": 131.196105162356,
                    "measurement_mrid": "_27d93b0d-b199-47ce-b93c-c2c5fe437c99"
                },
                {
                    "angle": -156.762005293264,
                    "magnitude": 131.196105162356,
                    "measurement_mrid": "_77a65869-37fd-4091-8e9f-d91cdf4a77ea"
                },
                {
                    "angle": 86.8653351383052,
                    "magnitude": 120.969003569756,
                    "measurement_mrid": "_9fec91a2-e8fd-45fd-820e-d7e175f6ca9c"
                },
                {
                    "angle": 86.8826927856396,
                    "magnitude": 120.643073847421,
                    "measurement_mrid": "_fb355279-a698-4f8f-b9b9-e486c77988c3"
                },
                {
                    "angle": -35.8273448770875,
                    "magnitude": 8259.93710195728,
                    "measurement_mrid": "_2d351806-d5a0-42a0-92c5-296c3dfb7d36"
                },
                {
                    "angle": 86.368750094071,
                    "magnitude": 7349.31323238,
                    "measurement_mrid": "_73e28a1b-47c7-409b-9880-c90fe9cc2855"
                },
                {
                    "angle": -156.454076771746,
                    "magnitude": 7948.58927959243,
                    "measurement_mrid": "_e579cafd-4225-4941-9c6a-96e08c9d2a40"
                },
                {
                    "angle": -156.408108373348,
                    "magnitude": 7884.94675593161,
                    "measurement_mrid": "_8a3807db-17fb-4ae1-8c97-6afe64df6368"
                },
                {
                    "angle": -155.418142348516,
                    "magnitude": 7770.90209612277,
                    "measurement_mrid": "_461a35a6-508a-49ce-992d-ec18d353635e"
                },
                {
                    "angle": 86.8139678326145,
                    "magnitude": 7388.45897878465,
                    "measurement_mrid": "_5573ae17-3de6-489e-a9cf-41853c8617b6"
                },
                {
                    "angle": -34.9040578633469,
                    "magnitude": 7987.27029511833,
                    "measurement_mrid": "_a07d24e8-0959-4ffb-9e32-c31b468d8b05"
                },
                {
                    "angle": 87.1808521043835,
                    "magnitude": 7231.93348011889,
                    "measurement_mrid": "_5bca933a-0f18-4eb9-b3c9-5e897cf16fcd"
                },
                {
                    "angle": 87.0483449432385,
                    "magnitude": 120.773384313746,
                    "measurement_mrid": "_5cb38e45-637a-472a-9def-242ff834f6d2"
                },
                {
                    "angle": 87.0483449432385,
                    "magnitude": 120.773384313746,
                    "measurement_mrid": "_647bcdff-0ebe-44bf-a5db-b0142969cea3"
                },
                {
                    "angle": -34.6897686330292,
                    "magnitude": 119.655127200622,
                    "measurement_mrid": "_b2109ff5-06e1-4a7b-a347-6aceba771375"
                },
                {
                    "angle": -34.6642989347807,
                    "magnitude": 119.181177919609,
                    "measurement_mrid": "_c9fc5a5b-db2e-42d9-b32e-2e38a409c56c"
                },
                {
                    "angle": -156.937632131953,
                    "magnitude": 131.113938704352,
                    "measurement_mrid": "_7ac29079-edb0-4674-8cec-10c6eccccf31"
                },
                {
                    "angle": -156.937632131953,
                    "magnitude": 131.113938704352,
                    "measurement_mrid": "_eda8f4fa-542a-4211-aae0-f65ffa8ba8d5"
                },
                {
                    "angle": 86.7222238621285,
                    "magnitude": 7397.58133951093,
                    "measurement_mrid": "_8ff36373-cd54-4317-9287-b924850f2983"
                },
                {
                    "angle": -35.6220759567137,
                    "magnitude": 8319.13849561833,
                    "measurement_mrid": "_cd39ba31-7d36-4d67-91f9-41ff57fe6f8b"
                },
                {
                    "angle": -35.6226332457481,
                    "magnitude": 8318.95379334478,
                    "measurement_mrid": "_3e087cf4-eee6-4a2a-8bc2-bc75cf0984fe"
                },
                {
                    "angle": 87.9416901014339,
                    "magnitude": 7305.68478825099,
                    "measurement_mrid": "_52afa051-9266-462a-914d-117d8f0d21fd"
                },
                {
                    "angle": -36.0948731017108,
                    "magnitude": 136.765885402185,
                    "measurement_mrid": "_66566b82-0e19-4619-96f1-29cd77da530f"
                },
                {
                    "angle": -36.0948731017108,
                    "magnitude": 136.765885402185,
                    "measurement_mrid": "_c837afc8-9068-40a3-9cff-636abf757028"
                },
                {
                    "angle": 87.3829729726409,
                    "magnitude": 7313.19058907235,
                    "measurement_mrid": "_310f16c2-c66e-4f33-9a8f-3a37c41fe19f"
                },
                {
                    "angle": -33.7797208285562,
                    "magnitude": 7235.20110043903,
                    "measurement_mrid": "_ac41592b-5b42-45aa-9f6b-554d00ea4c64"
                },
                {
                    "angle": -154.05941079577,
                    "magnitude": 7288.01884693723,
                    "measurement_mrid": "_b0d0b4ec-b962-4488-9db5-4dd3cf33fb80"
                },
                {
                    "angle": -34.8623165608406,
                    "magnitude": 7748.4864683511,
                    "measurement_mrid": "_cb13d962-7c6e-4ffc-b567-27fd7aa7278a"
                },
                {
                    "angle": -156.881127048799,
                    "magnitude": 130.422380706624,
                    "measurement_mrid": "_294ee32f-6c8d-4b2d-8f8f-904197c436f3"
                },
                {
                    "angle": -156.865711003239,
                    "magnitude": 130.110343393641,
                    "measurement_mrid": "_85a8fbb1-7799-420f-baf7-5f84d79f9c58"
                },
                {
                    "angle": -156.45016964424,
                    "magnitude": 7946.09542155445,
                    "measurement_mrid": "_c16f3570-f433-4023-aec8-cae0ee5f8640"
                },
                {
                    "angle": -155.774887591067,
                    "magnitude": 125.872860577778,
                    "measurement_mrid": "_025d4a77-894d-4dc2-a354-fd0e590a934a"
                },
                {
                    "angle": -155.774887591067,
                    "magnitude": 125.872860577778,
                    "measurement_mrid": "_325de53c-d837-45e6-8f03-5138ab5f29fd"
                },
                {
                    "angle": -153.423484471143,
                    "magnitude": 120.961152852286,
                    "measurement_mrid": "_3171ac7e-0e5e-4130-9886-4909c93cf261"
                },
                {
                    "angle": -153.423484471143,
                    "magnitude": 120.961152852286,
                    "measurement_mrid": "_b239cb5c-5dc8-41ac-aedd-0b54f3bf4802"
                },
                {
                    "angle": -35.6018553857588,
                    "magnitude": 8315.65125245629,
                    "measurement_mrid": "_48d6ac1a-e628-4d78-88a3-6f47d6cd522b"
                },
                {
                    "angle": -36.1425396077839,
                    "magnitude": 137.479715612683,
                    "measurement_mrid": "_7f3e7bfd-8ba6-4d48-a049-e751d8d8c278"
                },
                {
                    "angle": -36.1425396077839,
                    "magnitude": 137.479715612683,
                    "measurement_mrid": "_df2ae10c-23af-4bab-9d1c-125a80f62b1d"
                },
                {
                    "angle": 86.4355765929595,
                    "magnitude": 7364.02858313604,
                    "measurement_mrid": "_2815e096-ce8d-4e43-8040-c0132a40726e"
                },
                {
                    "angle": -35.5948996427155,
                    "magnitude": 8328.07908177021,
                    "measurement_mrid": "_445340c7-0e01-407a-86f2-6d5eabf385e1"
                },
                {
                    "angle": -156.151074539349,
                    "magnitude": 7985.53033668872,
                    "measurement_mrid": "_64d4bc7f-7c34-42f2-ac97-e0c6c0e54106"
                },
                {
                    "angle": -35.9534993437295,
                    "magnitude": 137.795452385746,
                    "measurement_mrid": "_96bcc702-530d-4905-9805-6035f293a30d"
                },
                {
                    "angle": -35.9623313321598,
                    "magnitude": 137.985138304503,
                    "measurement_mrid": "_d4789607-25e6-423d-ac4b-280965ddca4d"
                },
                {
                    "angle": 87.1487706310424,
                    "magnitude": 7371.82497943796,
                    "measurement_mrid": "_30534f30-d073-4e5b-9234-6843e965ff56"
                },
                {
                    "angle": -34.355175097375,
                    "magnitude": 8017.50103627924,
                    "measurement_mrid": "_542dda0d-9b0f-4b84-8d62-0de752d2b766"
                },
                {
                    "angle": 87.1487706310424,
                    "magnitude": 7371.82497943796,
                    "measurement_mrid": "_b585334b-1ab7-47ab-a154-5eef87da1a54"
                },
                {
                    "angle": -154.673474329655,
                    "magnitude": 7781.99517965333,
                    "measurement_mrid": "_ec11cc94-3d87-49a8-a90b-5569ac99b794"
                },
                {
                    "angle": -154.673474329655,
                    "magnitude": 7781.99517965333,
                    "measurement_mrid": "_f5486d3b-70e2-43e5-a4c9-e9ed420ca53a"
                },
                {
                    "angle": -34.355175097375,
                    "magnitude": 8017.50103627924,
                    "measurement_mrid": "_f56ffc6b-9c11-4d87-b886-eb08c0c70395"
                },
                {
                    "angle": -35.7458495571305,
                    "magnitude": 8238.29244753687,
                    "measurement_mrid": "_0e794a02-8bbe-4732-a0d5-7f5364572ad2"
                },
                {
                    "angle": -35.9830686245631,
                    "magnitude": 137.587398457038,
                    "measurement_mrid": "_321f5a26-c59c-4c7c-a135-c84c097199c3"
                },
                {
                    "angle": -35.9830686245631,
                    "magnitude": 137.587398457038,
                    "measurement_mrid": "_768664a1-8de2-4f11-b8ad-2bff92d5a2dc"
                },
                {
                    "angle": -35.7457044359777,
                    "magnitude": 8238.33978401053,
                    "measurement_mrid": "_c483ab48-ed11-4a60-b237-013a04005aff"
                },
                {
                    "angle": 86.005325402487,
                    "magnitude": 120.03524809148,
                    "measurement_mrid": "_42694507-88c7-4b69-bb55-cc3ca1407334"
                },
                {
                    "angle": 85.9189889199529,
                    "magnitude": 121.666079618784,
                    "measurement_mrid": "_d68d9c34-83c9-4e2f-9237-24da9ee243e7"
                },
                {
                    "angle": -35.7906329299625,
                    "magnitude": 8292.2869189362,
                    "measurement_mrid": "_1a226927-199f-41e7-9d78-c02c2056cb4d"
                },
                {
                    "angle": -155.305381774285,
                    "magnitude": 7615.27972451034,
                    "measurement_mrid": "_7a4edaa3-b46a-4efb-8ffd-98153046b7b4"
                },
                {
                    "angle": -36.1235322551934,
                    "magnitude": 136.508940976546,
                    "measurement_mrid": "_79070cf6-9b7c-4693-9c2c-91cf1b9b2f0e"
                },
                {
                    "angle": -36.1235322551934,
                    "magnitude": 136.508940976546,
                    "measurement_mrid": "_822c0cfe-a04f-43ca-8f06-4f3f51928ea2"
                },
                {
                    "angle": -34.7651252362268,
                    "magnitude": 128.544885936804,
                    "measurement_mrid": "_a80640bd-1694-44e9-9c63-b024c2dd4efd"
                },
                {
                    "angle": -34.7887453889612,
                    "magnitude": 129.01883381669,
                    "measurement_mrid": "_aaf6c330-ed92-4051-aae6-1574741261eb"
                },
                {
                    "angle": 86.4787148183291,
                    "magnitude": 7321.51118938524,
                    "measurement_mrid": "_189f8d8b-4764-4b27-afc9-1226242b195b"
                },
                {
                    "angle": 87.2737858955326,
                    "magnitude": 7277.7751007123,
                    "measurement_mrid": "_49ca6c64-72d0-4fff-948e-513492290dad"
                },
                {
                    "angle": -50.3847316395819,
                    "magnitude": 0.760688072372638,
                    "measurement_mrid": "_3232dc5a-a7f3-45f5-88d2-502f2ae2c164"
                },
                {
                    "angle": -36.1253417693588,
                    "magnitude": 137.20663599454,
                    "measurement_mrid": "_c815cdce-5ea3-4d5b-b5c5-643bd3063f79"
                },
                {
                    "angle": -36.0809705430652,
                    "magnitude": 136.258705828389,
                    "measurement_mrid": "_fb21803d-22e8-4ce2-b75a-02cd8e0bdc86"
                },
                {
                    "angle": 87.2862171262166,
                    "magnitude": 7283.9152508211,
                    "measurement_mrid": "_e945fc08-3d79-4062-8c96-8b15c2a2ed4b"
                },
                {
                    "angle": -34.8649195700322,
                    "magnitude": 7732.8751219926,
                    "measurement_mrid": "_3ffd3209-f575-434b-8a6d-8449f0cc293d"
                },
                {
                    "angle": -154.443485025584,
                    "magnitude": 119.898044570861,
                    "measurement_mrid": "_39a2de23-0e92-4301-959d-8a784a42a096"
                },
                {
                    "angle": -154.443485025584,
                    "magnitude": 119.898044570861,
                    "measurement_mrid": "_7aa92735-e0b3-4f80-b70d-c4193d0eed9a"
                },
                {
                    "angle": -34.8510675465159,
                    "magnitude": 7723.08725360892,
                    "measurement_mrid": "_4fdd6dfa-2a95-4ddb-beeb-c0d52ad131b4"
                },
                {
                    "angle": 85.6412409626299,
                    "magnitude": 7416.7748153154,
                    "measurement_mrid": "_65364770-c0d5-48cb-ac37-fcd10bf13ee0"
                },
                {
                    "angle": -155.189621604548,
                    "magnitude": 7674.75292813226,
                    "measurement_mrid": "_bf09499d-dcb2-44fd-b82a-28b58270584e"
                },
                {
                    "angle": -155.139097639897,
                    "magnitude": 7707.71801105667,
                    "measurement_mrid": "_01b1950c-a9e2-4734-a40a-3c9d2fd1c0f5"
                },
                {
                    "angle": 85.6299800490172,
                    "magnitude": 7423.38580852336,
                    "measurement_mrid": "_90106686-fbdb-462a-9f06-6a6dd9da0295"
                },
                {
                    "angle": -34.8614768219037,
                    "magnitude": 7748.96127618725,
                    "measurement_mrid": "_cda4b584-ce73-4ec2-987a-bb2e9fde48ca"
                },
                {
                    "angle": 85.9144271442706,
                    "magnitude": 121.932378113275,
                    "measurement_mrid": "_112120b3-2f07-45f9-8421-811b7d0325f7"
                },
                {
                    "angle": 85.9144271442706,
                    "magnitude": 121.932378113275,
                    "measurement_mrid": "_f4bad2fc-7cbf-409c-ab7c-fa754c9e3a1a"
                },
                {
                    "angle": -156.183440443996,
                    "magnitude": 127.972642654263,
                    "measurement_mrid": "_abaf221c-5928-4a80-a1c2-731724de7a24"
                },
                {
                    "angle": -156.183440443996,
                    "magnitude": 127.972642654263,
                    "measurement_mrid": "_ad0010c5-ebe0-4e4b-8b5b-13c7b840a954"
                },
                {
                    "angle": -154.598871687666,
                    "magnitude": 128.608901134855,
                    "measurement_mrid": "_2f466206-b169-4830-ac84-e9bd11e48466"
                },
                {
                    "angle": -154.588465327716,
                    "magnitude": 128.401054405547,
                    "measurement_mrid": "_875b0ece-b9b4-486c-914f-5c7da6a06ed0"
                },
                {
                    "angle": 86.6222117507292,
                    "magnitude": 121.736779938438,
                    "measurement_mrid": "_10f7319c-6418-4c92-aff4-c19cec18abd9"
                },
                {
                    "angle": 86.6222117507292,
                    "magnitude": 121.736779938438,
                    "measurement_mrid": "_d8079df9-ea1b-4e51-8fc7-ca800945a622"
                },
                {
                    "angle": 87.2863548873557,
                    "magnitude": 7283.98370040003,
                    "measurement_mrid": "_ba9b0942-34e5-49e3-bb68-fd334e28daeb"
                },
                {
                    "angle": -156.426301393094,
                    "magnitude": 7875.4081295982,
                    "measurement_mrid": "_bebc8eb9-ea5d-4411-bfa1-51ee6f2d1984"
                },
                {
                    "angle": -36.1470830940857,
                    "magnitude": 137.777746165869,
                    "measurement_mrid": "_db7c46a8-4de6-44b5-a4b4-e0b56b5905cd"
                },
                {
                    "angle": -36.124984668243,
                    "magnitude": 137.303792920701,
                    "measurement_mrid": "_f90fbb3f-d8c3-4005-b6e8-56c010267e34"
                },
                {
                    "angle": -155.622225851632,
                    "magnitude": 126.793038226087,
                    "measurement_mrid": "_20d220cb-1a02-43f6-b109-a65c569f0b35"
                },
                {
                    "angle": -155.648507557853,
                    "magnitude": 127.312934210881,
                    "measurement_mrid": "_8253d272-4fd0-4834-ba52-5e2ea338021f"
                },
                {
                    "angle": 87.761755874055,
                    "magnitude": 120.642831977163,
                    "measurement_mrid": "_581084b1-de46-4fcd-862f-f73c11fff361"
                },
                {
                    "angle": 87.7733679518439,
                    "magnitude": 120.425367347961,
                    "measurement_mrid": "_59ce12f2-34fd-4ecc-b13a-099bd0d00399"
                },
                {
                    "angle": -35.7457848269519,
                    "magnitude": 8238.30744080875,
                    "measurement_mrid": "_5a5b18c6-3cfc-4bbd-b332-72b164f5f7bb"
                },
                {
                    "angle": -35.8532267243922,
                    "magnitude": 8244.43482248695,
                    "measurement_mrid": "_432b6072-a4ab-4d23-a26a-d397dcc18a41"
                },
                {
                    "angle": 86.422090721069,
                    "magnitude": 7385.35200016557,
                    "measurement_mrid": "_da8a3d07-7d66-4bf7-9a12-ad65286252ec"
                },
                {
                    "angle": -36.2019050760985,
                    "magnitude": 136.752353097783,
                    "measurement_mrid": "_050d37a5-3325-414c-8743-4e69cc5b4598"
                },
                {
                    "angle": -36.2019050760985,
                    "magnitude": 136.752353097783,
                    "measurement_mrid": "_be0a087f-a208-4df4-aa00-89567a9e96df"
                },
                {
                    "angle": -156.930275016655,
                    "magnitude": 130.955685085034,
                    "measurement_mrid": "_0e48e98b-242c-409d-b367-c3c49931eb2e"
                },
                {
                    "angle": -156.94559406095,
                    "magnitude": 131.267721680158,
                    "measurement_mrid": "_7daadf7b-6ce4-4521-aa80-a5a35d408c8e"
                },
                {
                    "angle": -153.587159365186,
                    "magnitude": 7306.83055354849,
                    "measurement_mrid": "_4c4ed67f-6525-4f69-871e-3de76c294632"
                },
                {
                    "angle": -33.3927685341822,
                    "magnitude": 7270.14461200827,
                    "measurement_mrid": "_9d53767c-5ebb-405e-97e8-083da7d772cf"
                },
                {
                    "angle": 87.5289875458842,
                    "magnitude": 7312.0421136467,
                    "measurement_mrid": "_b9b5853e-9821-400b-baa2-5ad464843cdf"
                },
                {
                    "angle": -33.3735286931676,
                    "magnitude": 121.032533255039,
                    "measurement_mrid": "_ca46c312-5224-450e-9288-4afe3b03ab36"
                },
                {
                    "angle": -33.3886052144267,
                    "magnitude": 121.316790731474,
                    "measurement_mrid": "_fb22d41c-f40f-48e1-bf15-b3f77622ddab"
                },
                {
                    "angle": 86.7021700602379,
                    "magnitude": 120.126241522291,
                    "measurement_mrid": "_38f9eb35-1fdd-4edf-9e39-47752fa982c5"
                },
                {
                    "angle": 86.7313117119192,
                    "magnitude": 119.582839231101,
                    "measurement_mrid": "_cd47397c-4fa4-4603-9248-e83edc51a154"
                },
                {
                    "angle": -154.072775627218,
                    "magnitude": 120.387796167866,
                    "measurement_mrid": "_7395deba-199d-447a-8af7-e46193598565"
                },
                {
                    "angle": -154.072775627218,
                    "magnitude": 120.387796167866,
                    "measurement_mrid": "_fd3d031a-36b3-4c60-92c2-4268ebe1ac3a"
                },
                {
                    "angle": -155.708710077791,
                    "magnitude": 7748.06163053343,
                    "measurement_mrid": "_d2aa71f5-90f0-4a2f-b4f5-eb8e7a338922"
                },
                {
                    "angle": -34.7703661450443,
                    "magnitude": 128.49851650537,
                    "measurement_mrid": "_499a0364-ab81-4ec0-9059-9ef2e41a2fae"
                },
                {
                    "angle": -34.7939943023609,
                    "magnitude": 128.972464500725,
                    "measurement_mrid": "_aa0b2f3b-ec7d-4b77-9ba5-74db158c1045"
                },
                {
                    "angle": -156.90012702149,
                    "magnitude": 131.391471137962,
                    "measurement_mrid": "_01ca5316-7781-418f-80e4-3536df92aab3"
                },
                {
                    "angle": -156.90012702149,
                    "magnitude": 131.391471137962,
                    "measurement_mrid": "_09891b27-6393-4387-89c1-d9a40299dce6"
                },
                {
                    "angle": -156.926169979851,
                    "magnitude": 130.14485502154,
                    "measurement_mrid": "_013e3db8-74dd-401a-acdf-3c4de72316b8"
                },
                {
                    "angle": -156.926169979851,
                    "magnitude": 130.14485502154,
                    "measurement_mrid": "_7fb4a2a1-f251-4387-bb0e-1ec1dff28050"
                },
                {
                    "angle": -35.271944469438,
                    "magnitude": 127.660348794337,
                    "measurement_mrid": "_62c6dcdd-a13f-4883-afcc-28aba15b1fc2"
                },
                {
                    "angle": -35.2576330425424,
                    "magnitude": 127.376086844314,
                    "measurement_mrid": "_cd977523-272a-4ed9-86c1-0d024349ec63"
                },
                {
                    "angle": -153.579569154832,
                    "magnitude": 7306.96415875817,
                    "measurement_mrid": "_2d8ee89c-7779-4cc9-91e1-2cf0985cca4f"
                },
                {
                    "angle": -33.3863350842925,
                    "magnitude": 7270.54764939832,
                    "measurement_mrid": "_482bd859-b286-4d26-bf3d-0fdd66aa8c36"
                },
                {
                    "angle": 87.5317206430147,
                    "magnitude": 7311.96285747046,
                    "measurement_mrid": "_cbe81b32-2dd5-4648-b9bc-d94d6f7cf134"
                },
                {
                    "angle": -34.2269434213459,
                    "magnitude": 7221.84119158681,
                    "measurement_mrid": "_bb2cbca3-f5fe-4501-b1b7-43c3d38655b2"
                },
                {
                    "angle": -152.203006704188,
                    "magnitude": 120.889570801703,
                    "measurement_mrid": "_17d07fd2-aea1-4413-8462-8887ef471602"
                },
                {
                    "angle": -152.214063141719,
                    "magnitude": 121.097416466855,
                    "measurement_mrid": "_7befa6f5-7e2b-46f5-b0f1-6f988d82fe71"
                },
                {
                    "angle": -154.486106356873,
                    "magnitude": 7297.53284211758,
                    "measurement_mrid": "_5818b523-fc82-4809-9aaa-5e61f821cf15"
                },
                {
                    "angle": 87.2217011769827,
                    "magnitude": 7323.09654081898,
                    "measurement_mrid": "_6e0adb92-d148-4439-9eca-7fd0c3ae7bb4"
                },
                {
                    "angle": -34.1929386781593,
                    "magnitude": 7223.67217974352,
                    "measurement_mrid": "_78a7d436-17c8-4f2a-98a9-28eefa4f0eb6"
                },
                {
                    "angle": -35.4997498998874,
                    "magnitude": 8378.997970307,
                    "measurement_mrid": "_74e2cbe5-4c69-4876-8fa6-33d46adf1c0d"
                },
                {
                    "angle": 86.4877229585216,
                    "magnitude": 7404.55128755931,
                    "measurement_mrid": "_b6349900-aa2c-48c9-be45-7e083b47babc"
                },
                {
                    "angle": -156.068919099488,
                    "magnitude": 8024.36111350584,
                    "measurement_mrid": "_bbf2ba0e-a73c-45f1-9636-ddbb23cb4e64"
                },
                {
                    "angle": -155.682042611913,
                    "magnitude": 7762.6083899781,
                    "measurement_mrid": "_3e8be05a-5d98-4d40-a86b-f856b5a5ce57"
                },
                {
                    "angle": 85.1454054285628,
                    "magnitude": 122.54109184068,
                    "measurement_mrid": "_b0b76fec-f714-4918-af68-bd2178d43b7e"
                },
                {
                    "angle": 85.1454054285628,
                    "magnitude": 122.54109184068,
                    "measurement_mrid": "_ed132200-d58f-4f2d-8045-73a7af3e02f5"
                },
                {
                    "angle": -155.868301871675,
                    "magnitude": 7761.9511342616,
                    "measurement_mrid": "_0405235b-059a-444c-b065-267d7e64c219"
                },
                {
                    "angle": 86.5909266915598,
                    "magnitude": 7389.4425553959,
                    "measurement_mrid": "_2d2193a7-cf42-451a-bc2a-a09aed197465"
                },
                {
                    "angle": -35.3016537642258,
                    "magnitude": 7959.64196366255,
                    "measurement_mrid": "_42e7cc3f-cd8e-498c-96bf-dc364b5fdc7d"
                },
                {
                    "angle": -34.6683487403278,
                    "magnitude": 119.148919204154,
                    "measurement_mrid": "_2b909f3e-eeba-4ae4-98f7-e4ccffc4c55a"
                },
                {
                    "angle": -34.6938251041385,
                    "magnitude": 119.62286837315,
                    "measurement_mrid": "_57743032-be0c-4639-b694-ca91096511d2"
                },
                {
                    "angle": -34.8456306778228,
                    "magnitude": 7706.60570626864,
                    "measurement_mrid": "_acfacf3d-85d2-4696-b7f0-85529ccd383c"
                },
                {
                    "angle": 85.7583184808007,
                    "magnitude": 121.530325580181,
                    "measurement_mrid": "_72cbe5bb-5f3e-4e8d-b99b-93d4d4d50bd1"
                },
                {
                    "angle": 85.7871221728677,
                    "magnitude": 120.986923759159,
                    "measurement_mrid": "_b844dcbd-e0a6-4868-9be2-39feb2311525"
                },
                {
                    "angle": 85.6282881531456,
                    "magnitude": 7424.00379671198,
                    "measurement_mrid": "_0f781cf6-06f8-4bc9-96e4-723742f35a41"
                },
                {
                    "angle": -155.135668814784,
                    "magnitude": 7710.0005334822,
                    "measurement_mrid": "_2ae2a052-eb7e-4543-a197-df89e83c8ab0"
                },
                {
                    "angle": -34.8614285259784,
                    "magnitude": 7751.38386020153,
                    "measurement_mrid": "_f08f4a9a-dfbb-4cb3-869d-be747c2ac9d2"
                },
                {
                    "angle": -34.861789168723,
                    "magnitude": 7753.007771669,
                    "measurement_mrid": "_4140a992-019a-4256-9161-325ce195e24a"
                },
                {
                    "angle": -35.9797192403635,
                    "magnitude": 137.543082629753,
                    "measurement_mrid": "_7aeee02c-0e04-4b71-9214-cfa8c470a5d8"
                },
                {
                    "angle": -35.9797192403635,
                    "magnitude": 137.543082629753,
                    "measurement_mrid": "_c3f1b43e-855a-48d2-9153-b0e8b5a65e75"
                },
                {
                    "angle": -155.736242974315,
                    "magnitude": 7733.59059990725,
                    "measurement_mrid": "_6daf5e1d-af3c-4f3f-8530-c83920b209fb"
                },
                {
                    "angle": 85.7495488428301,
                    "magnitude": 122.364173235446,
                    "measurement_mrid": "_f263ef5c-c479-4c2c-954f-d9dc9b1bb94e"
                },
                {
                    "angle": 85.7495488428301,
                    "magnitude": 122.364173235446,
                    "measurement_mrid": "_feb980b5-a34d-4b2f-93a9-d734e3fd81e4"
                },
                {
                    "angle": 85.187670923005,
                    "magnitude": 122.685511267723,
                    "measurement_mrid": "_0072dff2-70ee-4b8e-b78d-d3df08d4d2f1"
                },
                {
                    "angle": 85.187670923005,
                    "magnitude": 122.685511267723,
                    "measurement_mrid": "_d2262659-a5ab-4fca-93b7-fb9121f117fe"
                },
                {
                    "angle": -154.283999790833,
                    "magnitude": 120.679252906267,
                    "measurement_mrid": "_9c3a53f2-c7b1-4e68-8a1b-b72cccd30d85"
                },
                {
                    "angle": -154.283999790833,
                    "magnitude": 120.679252906267,
                    "measurement_mrid": "_d64e16b7-e8ad-443f-9098-d27ef74acb1e"
                },
                {
                    "angle": 87.4659899940551,
                    "magnitude": 7313.70578717638,
                    "measurement_mrid": "_cb62ee06-a3d9-447d-9e20-ebbab92ec340"
                },
                {
                    "angle": -34.0921246007818,
                    "magnitude": 121.038801660931,
                    "measurement_mrid": "_c455c4f6-d47b-42f5-94d1-0ee5bf369981"
                },
                {
                    "angle": -34.0543604170786,
                    "magnitude": 120.328139062802,
                    "measurement_mrid": "_e88a70b0-07ed-467e-83a1-b2440cb2f483"
                },
                {
                    "angle": -154.249816293832,
                    "magnitude": 120.699997383842,
                    "measurement_mrid": "_8da54582-d1bc-4dc1-a6d4-5749ec0e758a"
                },
                {
                    "angle": -154.194368648372,
                    "magnitude": 119.660717586148,
                    "measurement_mrid": "_cbab4776-fa56-4cd8-bb31-55ec52342cf5"
                },
                {
                    "angle": 86.3053120001877,
                    "magnitude": 119.593330148617,
                    "measurement_mrid": "_19b1da8f-8584-4403-a32d-c6200cbb7c61"
                },
                {
                    "angle": 86.261689077401,
                    "magnitude": 120.408711170571,
                    "measurement_mrid": "_6d546fbb-da72-4bfb-a479-48babad563c4"
                },
                {
                    "angle": 88.8856047034642,
                    "magnitude": 7223.21792895751,
                    "measurement_mrid": "_692e3858-114c-42fa-ba3e-2110e3a66e02"
                },
                {
                    "angle": -155.708450493127,
                    "magnitude": 7748.18595225773,
                    "measurement_mrid": "_131bf633-ea72-4bb2-b2b6-8acb25c4e52d"
                },
                {
                    "angle": 86.4036985411114,
                    "magnitude": 7358.71049493509,
                    "measurement_mrid": "_12dda9e6-0cda-4f82-8693-fed063e6f897"
                },
                {
                    "angle": -156.177511263966,
                    "magnitude": 7977.85899861986,
                    "measurement_mrid": "_41021f11-8b06-4ee5-b3e9-8953aaa280b1"
                },
                {
                    "angle": -35.6087811957862,
                    "magnitude": 8323.45774775929,
                    "measurement_mrid": "_cb796397-c719-44d4-8925-b23dd0ad7b4b"
                },
                {
                    "angle": 86.415625925906,
                    "magnitude": 7372.01327901004,
                    "measurement_mrid": "_43b15c73-e9d1-4a4f-a946-2408703f6926"
                },
                {
                    "angle": -156.364461451446,
                    "magnitude": 7975.84463296472,
                    "measurement_mrid": "_89699782-906f-497b-a503-9b2b0e635239"
                },
                {
                    "angle": -35.7721050622272,
                    "magnitude": 8300.62889478761,
                    "measurement_mrid": "_e0742642-5fb6-4e1c-a035-5a8b8440b940"
                },
                {
                    "angle": 86.451265788755,
                    "magnitude": 7350.80681302449,
                    "measurement_mrid": "_7a369080-2c3e-49bc-8463-157820d6f718"
                },
                {
                    "angle": -35.5854013877651,
                    "magnitude": 8310.38319331319,
                    "measurement_mrid": "_13b3b637-546e-4a9a-8d09-e720d607a9c3"
                },
                {
                    "angle": 86.1456413403828,
                    "magnitude": 7331.80925930197,
                    "measurement_mrid": "_8acb7b19-e053-4d30-92bf-8aef30340eb3"
                },
                {
                    "angle": -156.37739330275,
                    "magnitude": 7915.36995678072,
                    "measurement_mrid": "_c44f3eb0-2d87-419c-a81a-4a006c9b22e1"
                },
                {
                    "angle": -35.788547433414,
                    "magnitude": 8282.34028494726,
                    "measurement_mrid": "_2e2a31d3-2500-4394-ae2a-5ac7cb3a7c71"
                },
                {
                    "angle": -34.9783098742726,
                    "magnitude": 7983.07217838445,
                    "measurement_mrid": "_2c516ab0-0667-417f-a808-55ddbf17f473"
                },
                {
                    "angle": 86.7703672813965,
                    "magnitude": 7391.13108300783,
                    "measurement_mrid": "_6c04cdb2-0d3f-45d7-a1e2-5d6716f5c164"
                },
                {
                    "angle": -155.522492689337,
                    "magnitude": 7769.47457098959,
                    "measurement_mrid": "_dabcea3f-e7cc-4ed8-99b0-2e461078c655"
                },
                {
                    "angle": -35.570396506957,
                    "magnitude": 8359.21213896757,
                    "measurement_mrid": "_8e6fdc71-bd5e-42cc-8b88-f2309f924047"
                },
                {
                    "angle": -33.6581451166145,
                    "magnitude": 7253.0859915604,
                    "measurement_mrid": "_b1e05aed-dc7b-47b5-a10f-ad310b07121c"
                },
                {
                    "angle": -155.797255046,
                    "magnitude": 126.239677521933,
                    "measurement_mrid": "_8febcefb-ea2e-4c1e-ab51-b10534150d3e"
                },
                {
                    "angle": -155.757523825816,
                    "magnitude": 125.460086057868,
                    "measurement_mrid": "_95007bbf-cf2f-43f9-8d33-8409d4b81dc2"
                },
                {
                    "angle": 85.9265051908328,
                    "magnitude": 122.066907387543,
                    "measurement_mrid": "_2a1518af-a8be-4804-98e1-6485c0141ed6"
                },
                {
                    "angle": 85.9265051908328,
                    "magnitude": 122.066907387543,
                    "measurement_mrid": "_ab55744b-3981-4a12-9d4f-6c2577c0b166"
                },
                {
                    "angle": -34.8251898448843,
                    "magnitude": 7763.14655857902,
                    "measurement_mrid": "_be17b1ac-10aa-45ad-83b5-e36999f6bd6c"
                },
                {
                    "angle": 86.7903720397527,
                    "magnitude": 120.426602798609,
                    "measurement_mrid": "_435b7fd9-0df9-4b4d-8402-3b7399781b88"
                },
                {
                    "angle": 86.7903720397527,
                    "magnitude": 120.426602798609,
                    "measurement_mrid": "_880cd14d-f814-4194-8507-880bdd0a09e1"
                },
                {
                    "angle": -36.0167118880427,
                    "magnitude": 137.685343817705,
                    "measurement_mrid": "_72a33a55-f2b1-4e7c-9b49-66fdbd2b73dc"
                },
                {
                    "angle": -36.0167118880427,
                    "magnitude": 137.685343817705,
                    "measurement_mrid": "_e6757320-3d2d-4c45-9eb1-a0f94bd60e94"
                },
                {
                    "angle": -34.6888626840072,
                    "magnitude": 119.324171633408,
                    "measurement_mrid": "_0fbe2279-e49c-432e-aab6-5f44b46cbfbd"
                },
                {
                    "angle": -34.6888626840072,
                    "magnitude": 119.324171633408,
                    "measurement_mrid": "_e1058361-af68-4e6d-a6e0-9619e0fe66c5"
                },
                {
                    "angle": -155.580601505123,
                    "magnitude": 127.340939584236,
                    "measurement_mrid": "_32c98c55-7624-402c-be81-16a2ca600d48"
                },
                {
                    "angle": -155.580601505123,
                    "magnitude": 127.340939584236,
                    "measurement_mrid": "_ae4294dd-b392-4682-8449-06493fa15130"
                },
                {
                    "angle": -156.488826427241,
                    "magnitude": 7928.56523452977,
                    "measurement_mrid": "_f45b76d2-7a44-4cb2-a0e5-4ffd437520de"
                },
                {
                    "angle": -155.308447928004,
                    "magnitude": 7613.61323420438,
                    "measurement_mrid": "_2b6f11d9-0e9d-422a-af3c-7cd30091c9e3"
                },
                {
                    "angle": 85.830722612171,
                    "magnitude": 121.129728112236,
                    "measurement_mrid": "_8443d4f5-45a4-4cf5-a38c-7494a38db50c"
                },
                {
                    "angle": 85.830722612171,
                    "magnitude": 121.129728112236,
                    "measurement_mrid": "_9db33b02-5abb-4c66-b2a5-0ee94b1a5391"
                },
                {
                    "angle": -153.045228718631,
                    "magnitude": 7318.50850600964,
                    "measurement_mrid": "_7b48f38b-f194-4258-8563-de91a0fa0bd2"
                },
                {
                    "angle": -156.586172939919,
                    "magnitude": 132.22478746594,
                    "measurement_mrid": "_14b5169a-c487-4cb6-a971-5b52204d89ac"
                },
                {
                    "angle": -156.560833937568,
                    "magnitude": 131.704900461759,
                    "measurement_mrid": "_c07b64db-5e21-408e-b1be-1ff12b548964"
                },
                {
                    "angle": -32.2652912473232,
                    "magnitude": 7315.52885317662,
                    "measurement_mrid": "_fdc52002-ccbe-4649-adfe-3a36b39efa2f"
                },
                {
                    "angle": -152.21366926942,
                    "magnitude": 120.962708685129,
                    "measurement_mrid": "_184d124c-4d2d-429b-9dd4-bda4a0cad961"
                },
                {
                    "angle": -152.21366926942,
                    "magnitude": 120.962708685129,
                    "measurement_mrid": "_3bd7f51a-41f7-4fa2-8241-e8e391b61210"
                },
                {
                    "angle": 88.8726399660816,
                    "magnitude": 7286.71882149493,
                    "measurement_mrid": "_f46ab6a6-071f-4831-affd-7cbd940a1edc"
                },
                {
                    "angle": 71.3332005437941,
                    "magnitude": 1.92938559116445,
                    "measurement_mrid": "_3a0fea47-8c33-44a7-b0dc-36f9fa587d97"
                },
                {
                    "angle": -155.682162047684,
                    "magnitude": 7762.57768516001,
                    "measurement_mrid": "_1894bbcc-44ef-4919-afeb-2b56c10b0564"
                },
                {
                    "angle": -34.3655165823958,
                    "magnitude": 7780.33448801809,
                    "measurement_mrid": "_ea153d19-3ed1-4e24-beda-7a2f56729154"
                },
                {
                    "angle": -36.1304165430818,
                    "magnitude": 137.388719979769,
                    "measurement_mrid": "_b9db7b15-ff8d-42c8-b606-5bdbb28f4f99"
                },
                {
                    "angle": -36.1436809390054,
                    "magnitude": 137.672982999232,
                    "measurement_mrid": "_e523c7d3-cb88-4494-9a73-2bb4e302d71f"
                },
                {
                    "angle": -156.921011173779,
                    "magnitude": 130.171050540705,
                    "measurement_mrid": "_c02d7d38-2844-4bdc-9eb0-1cd005cdc503"
                },
                {
                    "angle": -156.921011173779,
                    "magnitude": 130.171050540705,
                    "measurement_mrid": "_c64ec53d-c10e-4cbb-9cea-9eb754ba308b"
                },
                {
                    "angle": -156.939639298028,
                    "magnitude": 130.401272250087,
                    "measurement_mrid": "_3aaeb6b0-49a5-4c69-b718-a4e8b52e72d2"
                },
                {
                    "angle": -156.913949532856,
                    "magnitude": 129.88138411477,
                    "measurement_mrid": "_b46b380d-8ce5-42b2-9f51-7a5d2d5896a4"
                },
                {
                    "angle": -36.0088078973131,
                    "magnitude": 137.728139184691,
                    "measurement_mrid": "_9d62317f-7ba2-4e9b-83ba-d4afdf7c20ad"
                },
                {
                    "angle": -36.0088078973131,
                    "magnitude": 137.728139184691,
                    "measurement_mrid": "_b5a370ee-a921-4168-8a7b-6606b5deeba4"
                },
                {
                    "angle": 129.996991929018,
                    "magnitude": 50.0708590275486,
                    "measurement_mrid": "_9f6c897c-4e1c-48f0-808c-8beaeceac4cc"
                },
                {
                    "angle": 13.6717539535941,
                    "magnitude": 52.4114156322228,
                    "measurement_mrid": "_c43dcea9-4147-461b-ae90-817cd801cc52"
                },
                {
                    "angle": -112.854223829377,
                    "magnitude": 55.5504787791707,
                    "measurement_mrid": "_d76630c3-aed4-42fa-b276-3cd3784b9353"
                },
                {
                    "angle": -155.138281527001,
                    "magnitude": 7694.39186981604,
                    "measurement_mrid": "_56c926e8-8aa5-43a0-bb9e-ba423156d793"
                },
                {
                    "angle": -34.5225663385719,
                    "magnitude": 119.552629393145,
                    "measurement_mrid": "_cc50f2e8-4196-4ad4-9241-bf2b7a9c5491"
                },
                {
                    "angle": -34.5225663385719,
                    "magnitude": 119.552629393145,
                    "measurement_mrid": "_d7dc3137-d5a0-480c-a2d6-b9935ec4f26d"
                },
                {
                    "angle": -33.3193511935787,
                    "magnitude": 121.038816408801,
                    "measurement_mrid": "_875b531a-591d-4042-b48d-311e65ae6484"
                },
                {
                    "angle": -33.3193511935787,
                    "magnitude": 121.038816408801,
                    "measurement_mrid": "_a49486cc-ed1d-4399-ac02-01b1cd82d62e"
                },
                {
                    "angle": 85.7435532365527,
                    "magnitude": 122.548511364918,
                    "measurement_mrid": "_05d11d4c-5fba-427a-884e-22ac0fe2b738"
                },
                {
                    "angle": 85.7606856197627,
                    "magnitude": 122.222580332317,
                    "measurement_mrid": "_15e240c5-8633-46a5-ba8a-8bbc9fbd8d62"
                },
                {
                    "measurement_mrid": "_11f91eab-070c-43bd-bfde-330f538885fa",
                    "value": 1
                },
                {
                    "angle": -32.6044416933384,
                    "magnitude": 7314.25936676222,
                    "measurement_mrid": "_1aca88af-aec3-4fa7-8e14-0a5809de9a57"
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.005787,
                    "measurement_mrid": "_304ace75-270f-433a-a256-f2f487e93da3"
                },
                {
                    "angle": -32.6044416933384,
                    "magnitude": 7314.25936676222,
                    "measurement_mrid": "_38ae7081-422f-4663-bee9-50eae38c30b5"
                },
                {
                    "measurement_mrid": "_551a5188-4850-4979-ad18-6c30091e7b57",
                    "value": 1
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.005787,
                    "measurement_mrid": "_d88480cb-f9da-48c1-960d-dcdb632b85af"
                },
                {
                    "angle": -156.702632929487,
                    "magnitude": 131.738570725626,
                    "measurement_mrid": "_395df7f6-e14d-4be3-83ee-6d4596f95d55"
                },
                {
                    "angle": -156.702632929487,
                    "magnitude": 131.738570725626,
                    "measurement_mrid": "_e3131671-c637-4b15-a12d-7182e2bdef94"
                },
                {
                    "measurement_mrid": "_267646f2-b03e-458c-ae76-0730a9cbaaf1",
                    "value": 1
                },
                {
                    "angle": 87.9198953291378,
                    "magnitude": 7306.31902598376,
                    "measurement_mrid": "_3c01f460-c96e-4677-9b0b-f3aacda2cf36"
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.005787,
                    "measurement_mrid": "_4bc507e2-1c75-4df0-9ec8-47ebbd562b11"
                },
                {
                    "angle": 87.9198953291378,
                    "magnitude": 7306.31902598376,
                    "measurement_mrid": "_564e06ce-1b60-4374-b06b-cc83d103b2ea"
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.005787,
                    "measurement_mrid": "_8afe4c0c-b171-45b9-b55c-027e4c69bc5a"
                },
                {
                    "measurement_mrid": "_c00e1902-cd87-4182-8367-c8f0ea97c552",
                    "value": 1
                },
                {
                    "measurement_mrid": "_0dcbe27c-471c-4604-8e5c-83bc52318258",
                    "value": 1
                },
                {
                    "measurement_mrid": "_42b7689a-0321-43ba-9d4a-0c257ccb23be",
                    "value": 1
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.005787,
                    "measurement_mrid": "_8750f703-ab40-4590-b253-4118bdfc5b3a"
                },
                {
                    "angle": -152.686547672593,
                    "magnitude": 7323.90059348908,
                    "measurement_mrid": "_c99e1f6f-9831-4c76-8c39-1b5e11586c2e"
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.005787,
                    "measurement_mrid": "_dac357cb-b9b5-4a03-8e21-30ab5e8a9f38"
                },
                {
                    "angle": -152.686547672593,
                    "magnitude": 7323.90059348908,
                    "measurement_mrid": "_fb778d98-e2de-478c-851f-0a3248f2b772"
                },
                {
                    "angle": -36.1405609806487,
                    "magnitude": 136.358378516523,
                    "measurement_mrid": "_4e14612f-6b97-4854-ae7b-829a38acca6a"
                },
                {
                    "angle": -36.1405609806487,
                    "magnitude": 136.358378516523,
                    "measurement_mrid": "_8c301b46-0d0b-4917-9a70-89a8ea390801"
                },
                {
                    "angle": -36.1694744763785,
                    "magnitude": 137.344059830272,
                    "measurement_mrid": "_c354b047-554d-4b55-8604-9184659e6a15"
                },
                {
                    "angle": -36.1694744763785,
                    "magnitude": 137.344059830272,
                    "measurement_mrid": "_dcfde5ae-557e-4d3c-9504-ae3a9fa7995c"
                },
                {
                    "angle": -156.811146147545,
                    "magnitude": 131.895371821227,
                    "measurement_mrid": "_249aee52-3f75-4f9f-acc7-829f268f00fe"
                },
                {
                    "angle": -156.811146147545,
                    "magnitude": 131.895371821227,
                    "measurement_mrid": "_b9a5149b-9e62-483a-8f81-7eff44d30ab1"
                },
                {
                    "angle": -156.903210687349,
                    "magnitude": 131.070005333778,
                    "measurement_mrid": "_3c2f048a-9d73-4bb1-86fe-564d08f5be38"
                },
                {
                    "angle": -156.928671943893,
                    "magnitude": 131.589892207227,
                    "measurement_mrid": "_d8162ee5-fe0f-4f2d-b842-ae1cabbcf435"
                },
                {
                    "angle": -35.2858855608785,
                    "magnitude": 127.930882357314,
                    "measurement_mrid": "_639234d5-d8f5-4db2-98b6-d7da9634bbc7"
                },
                {
                    "angle": -35.2858855608785,
                    "magnitude": 127.930882357314,
                    "measurement_mrid": "_84889cea-bfd3-42c7-a2bd-bbdd43819587"
                },
                {
                    "angle": -34.5097621886354,
                    "magnitude": 119.316346795468,
                    "measurement_mrid": "_62d5d485-2aa4-47ff-a702-98cea230fcd3"
                },
                {
                    "angle": -34.5352053179291,
                    "magnitude": 119.790294645655,
                    "measurement_mrid": "_8b3a9c8c-0eff-4aad-93a0-3f3e3d20a196"
                },
                {
                    "angle": -35.7390687629656,
                    "magnitude": 8242.04963601363,
                    "measurement_mrid": "_968513da-b275-4bbe-8e6a-4ec0ec1e29b8"
                },
                {
                    "angle": 86.2612728451096,
                    "magnitude": 7411.56949763965,
                    "measurement_mrid": "_17277bc3-3160-47e1-9296-74700c994d72"
                },
                {
                    "angle": -35.8673109151391,
                    "magnitude": 8236.67450228201,
                    "measurement_mrid": "_da94f666-d99a-4b4e-95d2-0bd14db2227a"
                },
                {
                    "angle": -36.1391898209192,
                    "magnitude": 136.367932270049,
                    "measurement_mrid": "_1afd0cf0-64ac-45d6-89b0-55dbd8b5e2e0"
                },
                {
                    "angle": -36.1391898209192,
                    "magnitude": 136.367932270049,
                    "measurement_mrid": "_4d57bf5b-8d41-4d96-b1f6-6e13de17c630"
                },
                {
                    "angle": -33.7096373103679,
                    "magnitude": 7292.32671841449,
                    "measurement_mrid": "_b0ff92aa-f8a9-4377-847b-bd9514fa94d1"
                },
                {
                    "angle": -33.6284831288651,
                    "magnitude": 7297.6670439534,
                    "measurement_mrid": "_bb2566ec-10f9-4345-9bb5-95fdfda8d59b"
                },
                {
                    "angle": -154.1478296751,
                    "magnitude": 7766.48519214046,
                    "measurement_mrid": "_b69a1eef-0144-4901-986a-be691a94e007"
                },
                {
                    "angle": 87.6799965800406,
                    "magnitude": 7307.67861372552,
                    "measurement_mrid": "_cd2d1a44-0c70-4334-b62c-d847120312fc"
                },
                {
                    "angle": -34.3667597452321,
                    "magnitude": 7779.94995295885,
                    "measurement_mrid": "_c9919c67-ccf2-4e51-ad11-6d96a01541a7"
                },
                {
                    "angle": -155.142135429877,
                    "magnitude": 7693.20990625778,
                    "measurement_mrid": "_bcaa2ed5-af5d-44b5-8d94-5f9777f3c66b"
                },
                {
                    "angle": -156.295112467941,
                    "magnitude": 7944.14725667061,
                    "measurement_mrid": "_e15fc53a-d673-4c0e-97c3-2a513fef1ec9"
                },
                {
                    "angle": -156.862725644165,
                    "magnitude": 130.957650293132,
                    "measurement_mrid": "_085711c2-5d60-4f3a-8f2f-aca531f9dfe9"
                },
                {
                    "angle": -156.837144240456,
                    "magnitude": 130.437762312336,
                    "measurement_mrid": "_9b7d810e-c866-4fd1-b135-25ddeb17f24b"
                },
                {
                    "angle": 85.9132888440257,
                    "magnitude": 121.941396658318,
                    "measurement_mrid": "_2e69f5ba-c02f-427c-aaff-d6a750914115"
                },
                {
                    "angle": 85.9132888440257,
                    "magnitude": 121.941396658318,
                    "measurement_mrid": "_5c076f96-7d6f-4883-b2cd-e5fd6510aa66"
                },
                {
                    "angle": -156.94331792748,
                    "magnitude": 131.069136484712,
                    "measurement_mrid": "_3a6ee032-c8df-43d2-9255-75732b73eea4"
                },
                {
                    "angle": -156.94331792748,
                    "magnitude": 131.069136484712,
                    "measurement_mrid": "_45bee4a2-4cc4-4a53-9b74-c11d113d022d"
                },
                {
                    "angle": 85.6277855902871,
                    "magnitude": 121.091449507333,
                    "measurement_mrid": "_a1519f69-3cd6-4690-93cb-fa41994a2b9c"
                },
                {
                    "angle": 85.6277855902871,
                    "magnitude": 121.091449507333,
                    "measurement_mrid": "_b07793f7-4be0-408a-9c47-76ed0335aea8"
                },
                {
                    "angle": -155.635393590678,
                    "magnitude": 127.05298287688,
                    "measurement_mrid": "_50ba97b3-37b7-48ad-8c78-182477861d0b"
                },
                {
                    "angle": -155.635393590678,
                    "magnitude": 127.05298287688,
                    "measurement_mrid": "_d5b4ee1c-4043-4c92-9c70-6b49bf1c12e6"
                },
                {
                    "angle": -151.725424652593,
                    "magnitude": 7320.27180131472,
                    "measurement_mrid": "_33bef13b-720f-45c1-8a7f-8186059e10b4"
                },
                {
                    "angle": -156.866412022144,
                    "magnitude": 130.104252173615,
                    "measurement_mrid": "_5e278f81-11d7-4cb2-a2f4-d5a788979af5"
                },
                {
                    "angle": -156.881828899119,
                    "magnitude": 130.416289264298,
                    "measurement_mrid": "_aa180896-72c0-4353-b895-2539f1cc75f3"
                },
                {
                    "angle": -154.32179670956,
                    "magnitude": 7763.88785353518,
                    "measurement_mrid": "_2937acf2-7dbd-41be-8847-ebe3ecd94888"
                },
                {
                    "angle": 86.2510074088552,
                    "magnitude": 7415.24766438086,
                    "measurement_mrid": "_a80cd0d3-31a9-41ae-a820-9b656d3eaea9"
                },
                {
                    "angle": -34.1945644409498,
                    "magnitude": 7799.61054293939,
                    "measurement_mrid": "_fb63b3c0-c899-4609-99a0-30fd42e95fd6"
                },
                {
                    "angle": -154.548377322721,
                    "magnitude": 120.432303276261,
                    "measurement_mrid": "_57bcaa90-60d0-4459-8c6f-3a1e367fe20a"
                },
                {
                    "angle": -154.548377322721,
                    "magnitude": 120.432303276261,
                    "measurement_mrid": "_e92d0335-9caf-4c5f-a2d0-19439c2df682"
                },
                {
                    "angle": -151.727185531055,
                    "magnitude": 7319.7731617444,
                    "measurement_mrid": "_4f6c9e7d-d399-4ec3-832d-44ce8256709b"
                },
                {
                    "angle": 87.7580822848654,
                    "magnitude": 7307.07149975911,
                    "measurement_mrid": "_1b34b1cf-bb27-4088-97bf-94fa4488f852"
                },
                {
                    "angle": -156.176285730088,
                    "magnitude": 128.256230377411,
                    "measurement_mrid": "_83049cac-ba2d-4554-9bf6-5aa1b660c362"
                },
                {
                    "angle": -156.160607654822,
                    "magnitude": 127.944194296725,
                    "measurement_mrid": "_bab588dc-7fb1-4233-b271-bf0eb4141e24"
                },
                {
                    "angle": -35.5723846951033,
                    "magnitude": 8331.5074767843,
                    "measurement_mrid": "_12a047e6-76c3-4675-bb1b-3b36c8a14991"
                },
                {
                    "angle": -35.5652594646537,
                    "magnitude": 8329.35994477194,
                    "measurement_mrid": "_c41bec46-dc0b-4901-aa1b-8dd895b55b97"
                },
                {
                    "angle": -156.466204682689,
                    "magnitude": 7941.39406564783,
                    "measurement_mrid": "_2290abbf-0e71-4d14-923e-afc74105ee8b"
                },
                {
                    "angle": -35.6016443582723,
                    "magnitude": 8315.72093556249,
                    "measurement_mrid": "_102503ec-dcef-4b5b-811a-66c49a2d6277"
                },
                {
                    "angle": 86.2193018818443,
                    "magnitude": 7338.21760226772,
                    "measurement_mrid": "_e2b1d7f3-d05a-4e7a-944d-f15ca95bbb55"
                },
                {
                    "angle": -35.2855333459461,
                    "magnitude": 127.93159377078,
                    "measurement_mrid": "_1965a414-0aab-4b68-9b59-b42ea1bef5b6"
                },
                {
                    "angle": -35.2855333459461,
                    "magnitude": 127.93159377078,
                    "measurement_mrid": "_bccf2163-3818-4cff-8115-8282acfc23be"
                },
                {
                    "angle": -155.705583376407,
                    "magnitude": 7749.75177498427,
                    "measurement_mrid": "_41b1b67e-9106-47a3-a9c5-6f1142aedeb0"
                },
                {
                    "angle": -155.773297309426,
                    "magnitude": 125.886524560765,
                    "measurement_mrid": "_001865ae-9e46-4357-a7e3-598afab252ee"
                },
                {
                    "angle": -155.773297309426,
                    "magnitude": 125.886524560765,
                    "measurement_mrid": "_7b77e248-d3a6-45de-ad44-1f96980c8380"
                },
                {
                    "angle": -33.207855292436,
                    "magnitude": 7281.53255516534,
                    "measurement_mrid": "_bfcb2869-54d8-4cf2-9348-4f3031400b30"
                },
                {
                    "angle": -35.5013302614476,
                    "magnitude": 8314.32494722026,
                    "measurement_mrid": "_963b6732-3c96-4e46-81e2-8b8e38b7f994"
                },
                {
                    "angle": -35.8870492413922,
                    "magnitude": 137.469383215048,
                    "measurement_mrid": "_9ee503f8-5541-4498-8c94-586c15d8fdb3"
                },
                {
                    "angle": -35.9003059959949,
                    "magnitude": 137.753646009865,
                    "measurement_mrid": "_c0a97c30-1fdf-4ef5-ab17-9f5ead4dd508"
                },
                {
                    "angle": -34.8542389228229,
                    "magnitude": 7701.92146248654,
                    "measurement_mrid": "_ea65452e-4498-460c-aa0e-ebc9baade21a"
                },
                {
                    "angle": -156.176553495239,
                    "magnitude": 128.254418924667,
                    "measurement_mrid": "_4dd4fcff-ab1f-4e7c-aa93-b2b9388d8e44"
                },
                {
                    "angle": -156.160875260419,
                    "magnitude": 127.942382169525,
                    "measurement_mrid": "_829a5611-499a-49f1-b8ab-9f96d0255c4e"
                },
                {
                    "angle": -35.7509456397164,
                    "magnitude": 8305.79025879264,
                    "measurement_mrid": "_38771e6d-6267-4f04-9e09-02de74eae22f"
                },
                {
                    "angle": -35.2930877277462,
                    "magnitude": 128.437266192556,
                    "measurement_mrid": "_a871c5df-d96d-4bd0-8656-b4856f01b795"
                },
                {
                    "angle": -35.2693671506548,
                    "magnitude": 127.963315459068,
                    "measurement_mrid": "_d704abb2-4a2c-4a65-b489-891fef2d1a34"
                },
                {
                    "angle": -34.8618180898031,
                    "magnitude": 7744.05263114835,
                    "measurement_mrid": "_6a1ba9af-cec8-4e1b-8c02-10c7543f8486"
                },
                {
                    "angle": 86.6209162713654,
                    "magnitude": 121.726214777516,
                    "measurement_mrid": "_00048e8e-92a4-4b16-b325-cb4ad1360eb0"
                },
                {
                    "angle": 86.6209162713654,
                    "magnitude": 121.726214777516,
                    "measurement_mrid": "_9bbc0726-3d75-472c-926f-048d525d8957"
                },
                {
                    "angle": -154.520143870206,
                    "magnitude": 119.918906182026,
                    "measurement_mrid": "_38d98219-af86-45c5-b9c2-06844624f345"
                },
                {
                    "angle": -154.575498430724,
                    "magnitude": 120.95818001382,
                    "measurement_mrid": "_c8de01b7-cf98-40bf-a2bf-ed08712791c1"
                },
                {
                    "angle": -34.2033609414948,
                    "magnitude": 119.173257793331,
                    "measurement_mrid": "_279f1afc-add4-4895-9901-202bf4fc77a3"
                },
                {
                    "angle": -34.2541111626995,
                    "magnitude": 120.121177680916,
                    "measurement_mrid": "_69ef989d-46aa-450a-a483-f68dbc248d43"
                },
                {
                    "angle": -34.2311554830943,
                    "magnitude": 7219.7677184933,
                    "measurement_mrid": "_6a9bc419-13cc-4bd3-b6cb-6971cb1365bd"
                },
                {
                    "angle": -34.806288099558,
                    "magnitude": 128.807344961637,
                    "measurement_mrid": "_122a4dc5-3f3e-421a-b1ba-01899d570da3"
                },
                {
                    "angle": -34.806288099558,
                    "magnitude": 128.807344961637,
                    "measurement_mrid": "_412a5b36-7221-464c-9b14-0f334f6bcf58"
                },
                {
                    "angle": 86.726634354781,
                    "magnitude": 120.581469550577,
                    "measurement_mrid": "_059253b1-2243-451f-ba2c-1030ca487048"
                },
                {
                    "angle": 86.726634354781,
                    "magnitude": 120.581469550577,
                    "measurement_mrid": "_e9b1d540-5d77-4278-a17f-9975a8dbee4e"
                },
                {
                    "angle": 86.4323019153007,
                    "magnitude": 7399.48020209292,
                    "measurement_mrid": "_5e3fa592-497c-49e5-a42f-7f444ac22e7c"
                },
                {
                    "angle": -35.509400481392,
                    "magnitude": 8315.98503968762,
                    "measurement_mrid": "_8918f7b3-e93e-456f-bdba-9e94edf59c61"
                },
                {
                    "angle": -156.363433378827,
                    "magnitude": 7908.50275694993,
                    "measurement_mrid": "_e53cfb9e-3975-4403-994f-fc81f2e4ad50"
                },
                {
                    "angle": -156.47431864911,
                    "magnitude": 7870.54242291666,
                    "measurement_mrid": "_8d6b252f-d2e7-4252-a445-9a99bee27fa9"
                },
                {
                    "angle": -35.0429396382738,
                    "magnitude": 132.564019364219,
                    "measurement_mrid": "_32ece54b-e6b8-4208-87ec-96ff032da880"
                },
                {
                    "angle": -35.0291530188039,
                    "magnitude": 132.279759248238,
                    "measurement_mrid": "_64255271-a0fd-4c06-8617-57296f4c8345"
                },
                {
                    "angle": -155.1465815121,
                    "magnitude": 7702.79355052557,
                    "measurement_mrid": "_7d8d87d7-d1a1-4d2d-841d-f242c63d32c1"
                },
                {
                    "angle": -34.861491566213,
                    "magnitude": 7744.15290570069,
                    "measurement_mrid": "_aa4fb231-deac-41c6-89e2-1f29c347e335"
                },
                {
                    "angle": 85.6326731880659,
                    "magnitude": 7422.03934350387,
                    "measurement_mrid": "_e8b4e306-a9e3-47dd-8224-4f8012eb261f"
                },
                {
                    "angle": 86.796254608074,
                    "magnitude": 120.253196153456,
                    "measurement_mrid": "_80de6075-a03a-4677-884a-15649c424751"
                },
                {
                    "angle": 86.7788407993147,
                    "magnitude": 120.579126211036,
                    "measurement_mrid": "_c392d6c9-f768-4bb8-bfa2-e3d02de04b11"
                },
                {
                    "angle": -35.2756418724631,
                    "magnitude": 127.858957010711,
                    "measurement_mrid": "_dadba8ba-e438-4a99-9d9f-a6c650808007"
                },
                {
                    "angle": -35.2756418724631,
                    "magnitude": 127.858957010711,
                    "measurement_mrid": "_fdd714e9-7ff3-417a-91e9-199cd9d452cb"
                },
                {
                    "angle": -156.467159144178,
                    "magnitude": 7942.00532339535,
                    "measurement_mrid": "_0724bf2f-253e-491e-84a2-1f4b81ec5825"
                },
                {
                    "angle": -35.79633044585,
                    "magnitude": 8268.6544735166,
                    "measurement_mrid": "_7ffce90c-bff4-4ce2-bfb7-c00c98e100cb"
                },
                {
                    "angle": 86.4017387320667,
                    "magnitude": 7362.79451984964,
                    "measurement_mrid": "_bac8dc0d-0d06-4f2a-b8c8-e97b4ab431f9"
                },
                {
                    "angle": 87.6122063167428,
                    "magnitude": 7304.3700753955,
                    "measurement_mrid": "_4cdb0a41-0a89-4e5b-a258-7be90b1f2850"
                },
                {
                    "angle": -32.8713020315884,
                    "magnitude": 7319.46371181533,
                    "measurement_mrid": "_603fee2b-834c-486d-9c08-da4a70e6a025"
                },
                {
                    "angle": -152.967758849411,
                    "magnitude": 7317.15445173736,
                    "measurement_mrid": "_a96d290a-75ea-4edb-885b-d44bd07e05a1"
                },
                {
                    "angle": 86.7933496733727,
                    "magnitude": 120.775219387987,
                    "measurement_mrid": "_6023a807-c575-47c8-a587-97c61d83d830"
                },
                {
                    "angle": 86.8107355500811,
                    "magnitude": 120.449289139981,
                    "measurement_mrid": "_ab256c06-d415-47a6-921e-01d0cb7d2e73"
                },
                {
                    "angle": -33.7824603876051,
                    "magnitude": 7245.14691467185,
                    "measurement_mrid": "_c7d90e1c-11f2-45e1-a524-49984fa96078"
                },
                {
                    "angle": 87.3825357588562,
                    "magnitude": 7317.77138852746,
                    "measurement_mrid": "_d4af68ec-175f-42ef-ad96-12c10e7389df"
                },
                {
                    "angle": -154.042243865723,
                    "magnitude": 7300.40404350516,
                    "measurement_mrid": "_fddcc54e-02b3-4771-8db7-855274e9d8a6"
                },
                {
                    "angle": -156.890095350662,
                    "magnitude": 130.344134647603,
                    "measurement_mrid": "_16a69972-9549-43d3-9d1e-7a99efdc0d57"
                },
                {
                    "angle": -156.890095350662,
                    "magnitude": 130.344134647603,
                    "measurement_mrid": "_fc4b7fce-5213-4178-97ab-ff86f1249ac0"
                },
                {
                    "angle": 85.7695334720593,
                    "magnitude": 121.240041530942,
                    "measurement_mrid": "_805d34bc-b8b8-493a-b329-e154cc2cb826"
                },
                {
                    "angle": 85.7695334720593,
                    "magnitude": 121.240041530942,
                    "measurement_mrid": "_c195c731-6fd5-4490-8ea8-34f7e24bade5"
                },
                {
                    "angle": -34.8641687984184,
                    "magnitude": 7733.3197755488,
                    "measurement_mrid": "_dec44423-ceac-4046-874f-fcc476b06921"
                },
                {
                    "angle": 88.9280599376796,
                    "magnitude": 7242.64517676462,
                    "measurement_mrid": "_486c71b5-5d89-405a-ba3d-f430f39e7fc7"
                },
                {
                    "angle": -155.717309926368,
                    "magnitude": 126.358903538814,
                    "measurement_mrid": "_b1a75f76-3f32-45a0-b858-0b7f305cb066"
                },
                {
                    "angle": -155.717309926368,
                    "magnitude": 126.358903538814,
                    "measurement_mrid": "_bd801f9f-9c03-48c8-9f97-5324065c7deb"
                },
                {
                    "angle": -35.2812494917481,
                    "magnitude": 128.200287671002,
                    "measurement_mrid": "_297419f2-58d6-4949-9f6f-6d673c6e1ba8"
                },
                {
                    "angle": -35.2812494917481,
                    "magnitude": 128.200287671002,
                    "measurement_mrid": "_77a4d16a-3561-4e9c-afca-ce853dba23f2"
                },
                {
                    "angle": -154.297817776236,
                    "magnitude": 120.939201672256,
                    "measurement_mrid": "_6ec6d192-0817-48d0-ae49-820b999beb8e"
                },
                {
                    "angle": -154.270122148559,
                    "magnitude": 120.419311189608,
                    "measurement_mrid": "_afa67f5f-9caf-43db-b509-ee73802ed038"
                },
                {
                    "angle": -155.784172892039,
                    "magnitude": 126.16714279754,
                    "measurement_mrid": "_05051810-380c-43fe-8a9c-ea913abb03ea"
                },
                {
                    "angle": -155.757659563169,
                    "magnitude": 125.647245292296,
                    "measurement_mrid": "_2b4e6e5d-afeb-4592-98da-6b4608afa33f"
                },
                {
                    "angle": -35.0307887125737,
                    "magnitude": 7976.90418741206,
                    "measurement_mrid": "_8a203687-1c27-407f-9111-c044030d7b61"
                },
                {
                    "angle": 86.7221399553315,
                    "magnitude": 7397.66312473891,
                    "measurement_mrid": "_c6eb6f58-62f5-410d-8559-6bff5f7a6366"
                },
                {
                    "angle": -155.681252933473,
                    "magnitude": 7762.70471981613,
                    "measurement_mrid": "_f5c38078-4190-49c0-ac08-b759b427db26"
                },
                {
                    "angle": -32.8749733020757,
                    "magnitude": 7319.26323516031,
                    "measurement_mrid": "_dfad2699-fe6e-48b8-9432-4f929bf635a3"
                },
                {
                    "angle": -35.9886770710025,
                    "magnitude": 137.600315395459,
                    "measurement_mrid": "_8204549c-a003-40c0-b578-2b46bbaa64d0"
                },
                {
                    "angle": -36.0019215401997,
                    "magnitude": 137.884577100335,
                    "measurement_mrid": "_b9f53a2d-cda6-4691-bb6f-8be1b5d65915"
                },
                {
                    "angle": -153.878716004811,
                    "magnitude": 120.660153983745,
                    "measurement_mrid": "_6bedce16-d3e3-41f9-8f88-0f931668733c"
                },
                {
                    "angle": -153.878716004811,
                    "magnitude": 120.660153983745,
                    "measurement_mrid": "_c7906f73-6ab8-4797-bbaf-ff759cfa7af6"
                },
                {
                    "angle": -35.2852717686062,
                    "magnitude": 127.935150880961,
                    "measurement_mrid": "_119b55c0-e22a-41ec-9e7a-4313ee452b66"
                },
                {
                    "angle": -35.2852717686062,
                    "magnitude": 127.935150880961,
                    "measurement_mrid": "_8e6ef919-24cc-40f6-9fc1-cdf1794a6ba6"
                },
                {
                    "angle": -35.1882018108248,
                    "magnitude": 128.496714866476,
                    "measurement_mrid": "_1d72fcef-8767-445b-9fde-3b427a91d7b2"
                },
                {
                    "angle": -35.1882018108248,
                    "magnitude": 128.496714866476,
                    "measurement_mrid": "_909cd81e-516a-446d-bd99-a4b4f2ab76cd"
                },
                {
                    "angle": 85.7257705014771,
                    "magnitude": 122.347107084462,
                    "measurement_mrid": "_55673a23-baf2-43d4-b1ee-5ce611930ee3"
                },
                {
                    "angle": 85.7086551994144,
                    "magnitude": 122.673037169596,
                    "measurement_mrid": "_d793aadd-bc21-44aa-964e-ab7714df5d9c"
                },
                {
                    "angle": -155.309604440877,
                    "magnitude": 7612.99700766409,
                    "measurement_mrid": "_6d5231be-ec89-461a-8b2e-163ec0a4cd54"
                },
                {
                    "angle": -155.306921394949,
                    "magnitude": 7614.45982621776,
                    "measurement_mrid": "_45d608d7-d331-4e31-b3b6-b4632434aca4"
                },
                {
                    "angle": -36.2064701038139,
                    "magnitude": 136.912834863212,
                    "measurement_mrid": "_301c8102-cdf6-4b76-9c75-a439c878a295"
                },
                {
                    "angle": -36.1931342208389,
                    "magnitude": 136.628570923317,
                    "measurement_mrid": "_effa8409-50dc-4c02-8334-42087a1e54e9"
                },
                {
                    "angle": 88.9101724472949,
                    "magnitude": 7235.52640150525,
                    "measurement_mrid": "_9aa712f4-d68e-498d-9733-ae0803273116"
                },
                {
                    "angle": 86.2589287124234,
                    "magnitude": 7410.38979856044,
                    "measurement_mrid": "_b7f6d50b-915e-4395-b5bb-c95c27fea1b5"
                },
                {
                    "angle": -36.1885953165085,
                    "magnitude": 136.540065137083,
                    "measurement_mrid": "_6dd36249-d6c2-4541-ba03-f8b8d6576108"
                },
                {
                    "angle": -36.2108130467961,
                    "magnitude": 137.014019189049,
                    "measurement_mrid": "_f1c052eb-a348-484f-ab58-a7d11b6a41d4"
                },
                {
                    "angle": -132.489777705813,
                    "magnitude": 245.201174382864,
                    "measurement_mrid": "_584664cb-1975-4d6c-9963-1a805065d9c3"
                },
                {
                    "angle": -12.18588273118,
                    "magnitude": 253.909503817531,
                    "measurement_mrid": "_d288b2d6-573d-400a-877e-9d8a68ed4102"
                },
                {
                    "angle": 109.257941809895,
                    "magnitude": 232.077485282085,
                    "measurement_mrid": "_eee60306-d508-404f-b9d8-845f0cfc8dd2"
                },
                {
                    "angle": -155.141736795432,
                    "magnitude": 7693.3320416011,
                    "measurement_mrid": "_94580209-cd42-40de-9024-7e40b64aa831"
                },
                {
                    "angle": -34.6779453453512,
                    "magnitude": 119.072366834043,
                    "measurement_mrid": "_843dc537-8db6-4b60-9132-38ee452213c7"
                },
                {
                    "angle": -34.7034380784685,
                    "magnitude": 119.546315465449,
                    "measurement_mrid": "_eccf7674-eb15-4410-860d-147078b3d482"
                },
                {
                    "angle": 86.2834000175683,
                    "magnitude": 120.00039926264,
                    "measurement_mrid": "_5a831715-cb60-41d5-8c98-bfc07adc534b"
                },
                {
                    "angle": 86.2834000175683,
                    "magnitude": 120.00039926264,
                    "measurement_mrid": "_e95cf294-f7e4-4c14-851c-4678c1a81888"
                },
                {
                    "angle": 86.2585982826526,
                    "magnitude": 7410.31002811726,
                    "measurement_mrid": "_7a67f33a-e98c-4273-a9bc-3fa2688d7bdd"
                },
                {
                    "angle": 85.4512249251778,
                    "magnitude": 122.576262991572,
                    "measurement_mrid": "_028f5d9f-b0b1-47e2-914d-d13df48305d3"
                },
                {
                    "angle": 85.4512249251778,
                    "magnitude": 122.576262991572,
                    "measurement_mrid": "_443e4ac1-8c62-4f79-8120-b366e5a0dd30"
                },
                {
                    "angle": 86.2313742644666,
                    "magnitude": 7339.43089958025,
                    "measurement_mrid": "_07335d3a-586c-4149-8bb9-5c290ee0b660"
                },
                {
                    "angle": -156.297959151505,
                    "magnitude": 7938.22669351849,
                    "measurement_mrid": "_52097cd6-0126-44ca-822f-e8e015319f11"
                },
                {
                    "angle": -35.5999024180184,
                    "magnitude": 8315.11820189673,
                    "measurement_mrid": "_7b10e258-8a19-4c81-8497-fd84130b860c"
                },
                {
                    "angle": 86.6841980757687,
                    "magnitude": 119.594885470077,
                    "measurement_mrid": "_b1b86cfb-ce64-474e-a306-e22822d1c194"
                },
                {
                    "angle": 86.6841980757687,
                    "magnitude": 119.594885470077,
                    "measurement_mrid": "_e9a7ca6d-da4f-4f73-826d-e790a4d023ba"
                },
                {
                    "angle": -156.840666003385,
                    "magnitude": 130.177756206795,
                    "measurement_mrid": "_0799f810-e698-436b-b761-7db436d7dddd"
                },
                {
                    "angle": -156.86629695436,
                    "magnitude": 130.697644148352,
                    "measurement_mrid": "_933889cd-f0a5-48b7-b773-069f4f25a9d3"
                },
                {
                    "angle": -156.37141448468,
                    "magnitude": 7914.18252067395,
                    "measurement_mrid": "_077b7e53-a4d1-474c-8921-8f96a632faa6"
                },
                {
                    "angle": 86.1278072544982,
                    "magnitude": 7328.8983922726,
                    "measurement_mrid": "_28690fd8-4519-49a8-8359-80e9fdb08d7d"
                },
                {
                    "angle": -35.5866553304345,
                    "magnitude": 8311.32064812809,
                    "measurement_mrid": "_c2e354da-ebf4-4a64-a7ef-80b47d3ecde3"
                },
                {
                    "angle": -32.765347594515,
                    "magnitude": 120.985476214163,
                    "measurement_mrid": "_2ab25d53-27cd-4d96-af40-ff3b04c75b78"
                },
                {
                    "angle": -32.765347594515,
                    "magnitude": 120.985476214163,
                    "measurement_mrid": "_f0d7cd2d-d0f7-4791-87f7-1698c308e2b4"
                },
                {
                    "angle": 85.7676085046942,
                    "magnitude": 122.282246263158,
                    "measurement_mrid": "_a502587f-5217-470b-9fc7-7c880f35bb96"
                },
                {
                    "angle": 85.7504844726859,
                    "magnitude": 122.608176965745,
                    "measurement_mrid": "_f092c921-5858-490a-84c4-3383abe524d6"
                },
                {
                    "angle": -154.05718203171,
                    "magnitude": 7290.32614290994,
                    "measurement_mrid": "_3cfe3d02-50f7-467b-9446-2fad2e636bde"
                },
                {
                    "angle": 87.3854019831117,
                    "magnitude": 7315.1841006743,
                    "measurement_mrid": "_addc14bb-38ed-4dea-aa5e-5e7ad3ac592e"
                },
                {
                    "angle": -33.7788036928038,
                    "magnitude": 7237.26363909016,
                    "measurement_mrid": "_f2909c23-a207-4eac-863c-082562dc0617"
                },
                {
                    "angle": -35.2505740464097,
                    "magnitude": 128.584029147323,
                    "measurement_mrid": "_afc9350a-4791-4b01-9108-540c2042c2bb"
                },
                {
                    "angle": -35.2363617879378,
                    "magnitude": 128.299769502211,
                    "measurement_mrid": "_e64729b9-2c64-45c8-a953-c564d42198a1"
                },
                {
                    "angle": -35.2558955112728,
                    "magnitude": 127.541775319002,
                    "measurement_mrid": "_56081b3d-d1b8-47dc-b6bc-a309065034e8"
                },
                {
                    "angle": -35.2558955112728,
                    "magnitude": 127.541775319002,
                    "measurement_mrid": "_815b117d-168a-412e-bb35-66b236ea4769"
                },
                {
                    "angle": -154.579213018522,
                    "magnitude": 128.405616167052,
                    "measurement_mrid": "_06e04511-673e-498e-b68e-0c4d43f70d03"
                },
                {
                    "angle": -154.594822876441,
                    "magnitude": 128.717655767536,
                    "measurement_mrid": "_5d64f86f-b1e8-4a51-96fa-da168cfd968c"
                },
                {
                    "angle": -36.1935523564981,
                    "magnitude": 136.831518089485,
                    "measurement_mrid": "_103e8fd7-7402-47c1-8f79-e0d9d0c55092"
                },
                {
                    "angle": -36.1935523564981,
                    "magnitude": 136.831518089485,
                    "measurement_mrid": "_c051d63b-5b87-4b0c-a4d8-f2492260c83a"
                },
                {
                    "angle": -156.505355885867,
                    "magnitude": 7920.55119766765,
                    "measurement_mrid": "_2b46a05b-fd5d-4ee7-85ba-78a395edddbc"
                },
                {
                    "angle": -34.5227340022629,
                    "magnitude": 8008.28030381095,
                    "measurement_mrid": "_1fc04ff3-5583-4349-8549-f9d4b4fef86a"
                },
                {
                    "angle": 86.2552729156639,
                    "magnitude": 7408.52265585882,
                    "measurement_mrid": "_c8a3403d-eafe-440f-b3e3-025959336d26"
                },
                {
                    "angle": -34.4860765434265,
                    "magnitude": 7780.14445184626,
                    "measurement_mrid": "_4e83603a-d83a-467f-a510-07fe30de24a4"
                },
                {
                    "angle": -154.665870612621,
                    "magnitude": 7744.55287258336,
                    "measurement_mrid": "_6912ebda-6852-4fbc-8bc2-9556df67fa82"
                },
                {
                    "angle": 85.9819103938567,
                    "magnitude": 7418.98779308038,
                    "measurement_mrid": "_c2dcd518-3a1e-4a1a-94ce-a00dc3926a86"
                },
                {
                    "angle": -35.7869156145581,
                    "magnitude": 8293.45201283642,
                    "measurement_mrid": "_531704b3-2382-47c4-88a6-6cddb32a7d78"
                },
                {
                    "angle": 87.3009476965421,
                    "magnitude": 7290.44700031977,
                    "measurement_mrid": "_80ad3641-7546-4458-b6f1-99933366bad6"
                },
                {
                    "angle": -35.8441420080985,
                    "magnitude": 8249.48903552721,
                    "measurement_mrid": "_78496201-4b67-4216-a79d-f6223ddc5878"
                },
                {
                    "angle": -156.449492565879,
                    "magnitude": 7946.36286250033,
                    "measurement_mrid": "_d5dbecf2-8caf-4885-8ca8-ead0ce478f35"
                },
                {
                    "angle": 86.3598192865308,
                    "magnitude": 7340.79988974597,
                    "measurement_mrid": "_e94f4c87-e5a0-4eaa-97df-9abd556e5a0a"
                },
                {
                    "angle": -156.859146518768,
                    "magnitude": 130.387908407438,
                    "measurement_mrid": "_03b33281-ff52-4501-b209-8d534082e7bc"
                },
                {
                    "angle": -156.859146518768,
                    "magnitude": 130.387908407438,
                    "measurement_mrid": "_8e50c86f-7115-4b33-9a72-5036b57fd2d0"
                },
                {
                    "angle": -152.969410067522,
                    "magnitude": 7316.68242321721,
                    "measurement_mrid": "_0a620d91-9c43-498f-816f-da3e47e73206"
                },
                {
                    "angle": -35.6931765553469,
                    "magnitude": 8324.60460653819,
                    "measurement_mrid": "_e5b39468-9cf0-4d23-97c6-b845ce3295e6"
                },
                {
                    "angle": -155.309239845192,
                    "magnitude": 7613.2233202984,
                    "measurement_mrid": "_b3467c06-6633-4046-8d10-023392e79761"
                },
                {
                    "angle": -33.0139930017592,
                    "magnitude": 7334.64123551045,
                    "measurement_mrid": "_a76fbafb-63f0-4cf8-b6a1-aa9e120984d0"
                },
                {
                    "angle": -153.635792868824,
                    "magnitude": 7281.04246992508,
                    "measurement_mrid": "_2b11c5d0-9f18-4cfe-84c8-5d9ffd42cbbb"
                },
                {
                    "angle": 86.8801234602765,
                    "magnitude": 7271.50737982591,
                    "measurement_mrid": "_3bd56d75-ebfd-4854-83bb-c8bbb2ce03f4"
                },
                {
                    "angle": -33.5348551737489,
                    "magnitude": 7305.07952943625,
                    "measurement_mrid": "_7c70e9b7-2e31-4bef-80cd-ce5c92fe9b54"
                },
                {
                    "angle": -155.723235436221,
                    "magnitude": 7740.41600232346,
                    "measurement_mrid": "_299890ae-1a30-4b95-8bd5-7f35fde43100"
                },
                {
                    "angle": -153.102461063154,
                    "magnitude": 7318.86694401021,
                    "measurement_mrid": "_6c6ac0d8-c885-4b26-a783-9b65dfdad44c"
                },
                {
                    "angle": 87.3573591524433,
                    "magnitude": 7301.37324281007,
                    "measurement_mrid": "_af7594d8-4b82-46ec-b9de-8dfc16499dc7"
                },
                {
                    "angle": -33.0255691195756,
                    "magnitude": 7335.91606873176,
                    "measurement_mrid": "_fe088e9c-2e11-424b-8eeb-2f1b656b8414"
                },
                {
                    "angle": -156.8627000156,
                    "magnitude": 129.981570172685,
                    "measurement_mrid": "_5101248f-98dc-4806-80e7-2c3d3e72d8ef"
                },
                {
                    "angle": -156.88836924191,
                    "magnitude": 130.50145847071,
                    "measurement_mrid": "_fd8d5972-2852-4a04-bc2b-19ce84b11951"
                },
                {
                    "angle": 88.3614976429797,
                    "magnitude": 119.469156808174,
                    "measurement_mrid": "_69c2bdfd-6919-41ec-97d9-b2845af6a070"
                },
                {
                    "angle": 88.3790717508647,
                    "magnitude": 119.143226220648,
                    "measurement_mrid": "_ad6b879a-e28c-4251-805c-b61aef4c5fbd"
                },
                {
                    "angle": -154.0613595442,
                    "magnitude": 7289.89917466339,
                    "measurement_mrid": "_9ec016aa-89d8-4cbe-ba3b-e9c1a9c1e024"
                },
                {
                    "angle": -156.862247017257,
                    "magnitude": 130.583005795457,
                    "measurement_mrid": "_695d8423-a33e-4507-ad39-8baca7f71149"
                },
                {
                    "angle": -156.846849172453,
                    "magnitude": 130.270969501157,
                    "measurement_mrid": "_d37fda32-5318-45f1-af12-2265402bffda"
                },
                {
                    "angle": 86.3114623021345,
                    "magnitude": 7347.32561296513,
                    "measurement_mrid": "_7ba7d9e1-6790-41a7-809d-8b35c52d9d2e"
                },
                {
                    "angle": -35.2971339107906,
                    "magnitude": 128.172128645276,
                    "measurement_mrid": "_6724cebf-5635-4a91-8d57-2e13c4a31a59"
                },
                {
                    "angle": -35.2733656002444,
                    "magnitude": 127.698178620662,
                    "measurement_mrid": "_ed0de3c8-d98c-49d9-8dd8-1e2256718b86"
                },
                {
                    "angle": -156.618469108336,
                    "magnitude": 132.276290402265,
                    "measurement_mrid": "_21542d11-3952-49bf-9722-eeb671036979"
                },
                {
                    "angle": -156.593140622479,
                    "magnitude": 131.756404138437,
                    "measurement_mrid": "_c2c0d64b-3d18-444b-8108-56c307813e90"
                },
                {
                    "angle": -35.663148449018,
                    "magnitude": 131.920825571179,
                    "measurement_mrid": "_ce19b3c0-161b-4a57-b46b-f70466f9a4bf"
                },
                {
                    "angle": -35.6539068469621,
                    "magnitude": 131.731140295802,
                    "measurement_mrid": "_f078c28d-97d5-4ac6-9380-020f473689a4"
                },
                {
                    "angle": 86.2842525801069,
                    "magnitude": 7344.40894955749,
                    "measurement_mrid": "_53b22de8-5fc4-4a60-a585-f7bf670215cd"
                },
                {
                    "angle": -35.6084293761313,
                    "magnitude": 8319.11169787083,
                    "measurement_mrid": "_bfbf01c7-cf3c-40d1-893d-3f3aaf8c0e55"
                },
                {
                    "angle": -34.238547801812,
                    "magnitude": 119.644193493454,
                    "measurement_mrid": "_26c9c15c-6774-4214-a3a3-d64f2beed70b"
                },
                {
                    "angle": -34.238547801812,
                    "magnitude": 119.644193493454,
                    "measurement_mrid": "_6b354b61-1258-44d4-8061-214c9d8010c6"
                },
                {
                    "angle": -154.573654252218,
                    "magnitude": 120.976046082273,
                    "measurement_mrid": "_143a576d-b1e6-457c-9e02-1b9d25ae75c1"
                },
                {
                    "angle": -154.518308018832,
                    "magnitude": 119.936772166874,
                    "measurement_mrid": "_d0b04346-c5ee-482a-bd7f-96059c39b832"
                },
                {
                    "angle": -34.2025228934021,
                    "magnitude": 119.189867496925,
                    "measurement_mrid": "_a6a46640-def2-4d6d-b005-bd4d1039ef53"
                },
                {
                    "angle": -34.2532667471609,
                    "magnitude": 120.137788207267,
                    "measurement_mrid": "_d6bb5478-a485-44a8-abc1-f44493a205d7"
                },
                {
                    "angle": -36.1399554460809,
                    "magnitude": 136.362240781472,
                    "measurement_mrid": "_08ce5cc3-cf7a-4a48-a978-f719b0869e4d"
                },
                {
                    "angle": -36.1399554460809,
                    "magnitude": 136.362240781472,
                    "measurement_mrid": "_ab5333a2-086d-493b-87c2-1939147ed4e9"
                },
                {
                    "angle": 85.9370415919116,
                    "magnitude": 121.553558717499,
                    "measurement_mrid": "_1ae3dbcf-98bf-4968-aa0a-9fb60c097503"
                },
                {
                    "angle": 85.894117846836,
                    "magnitude": 122.368939526854,
                    "measurement_mrid": "_e18d3ff6-785e-40a0-b92f-339204de8740"
                },
                {
                    "angle": -35.9688298296825,
                    "magnitude": 137.958224173021,
                    "measurement_mrid": "_0046c2df-ecf4-412c-980d-e732f29ac599"
                },
                {
                    "angle": -35.9688298296825,
                    "magnitude": 137.958224173021,
                    "measurement_mrid": "_62a890b8-ca90-462e-99d7-8eb655d4478e"
                },
                {
                    "angle": 86.7836931101396,
                    "magnitude": 120.153065730034,
                    "measurement_mrid": "_d44688d6-73de-4081-bdcd-48a9326e0007"
                },
                {
                    "angle": 86.7662643039625,
                    "magnitude": 120.478995877815,
                    "measurement_mrid": "_ff0aaa26-f491-4131-b0ae-c008c113ab22"
                },
                {
                    "angle": -170.885954337598,
                    "magnitude": 38.2435252876123,
                    "measurement_mrid": "_6d5ee994-2789-4981-ad9d-5e1a33c5484d"
                },
                {
                    "angle": 71.7644441595368,
                    "magnitude": 44.6217326944007,
                    "measurement_mrid": "_74bb979f-5759-45b6-b07c-3076ce066a04"
                },
                {
                    "angle": -50.1108499425359,
                    "magnitude": 50.3544850354979,
                    "measurement_mrid": "_ae9d2723-78ed-40be-bb6b-4a8e483d72f4"
                },
                {
                    "angle": 86.2385293190108,
                    "magnitude": 7399.7667004271,
                    "measurement_mrid": "_29381988-fef0-4050-9113-fc1ed4f4c2b3"
                },
                {
                    "angle": 85.7598365160478,
                    "magnitude": 122.218653493097,
                    "measurement_mrid": "_2f59fae4-7f95-46a5-b41c-ae090c013736"
                },
                {
                    "angle": 85.7427034762294,
                    "magnitude": 122.544584441382,
                    "measurement_mrid": "_b020305a-9da7-4722-a96c-026f8bc334b9"
                },
                {
                    "angle": -36.2478573847901,
                    "magnitude": 136.253961634644,
                    "measurement_mrid": "_1ef1a461-553b-42dc-8d36-94c0d5f73445"
                },
                {
                    "angle": -36.2612285827234,
                    "magnitude": 136.538224574113,
                    "measurement_mrid": "_c38586f6-8831-4fdd-860b-b50ccb5316e7"
                },
                {
                    "angle": 86.2409647413358,
                    "magnitude": 7400.99398503974,
                    "measurement_mrid": "_d5082ce6-c3d8-4920-b919-cac8f5937eb1"
                },
                {
                    "angle": 86.2328102926646,
                    "magnitude": 7396.82572573361,
                    "measurement_mrid": "_078d22f1-b4f7-4434-95d3-d21204988089"
                },
                {
                    "angle": 85.7514250193789,
                    "magnitude": 122.384486145561,
                    "measurement_mrid": "_3b366018-bed1-4d85-979c-3ce0f76de27e"
                },
                {
                    "angle": 85.7514250193789,
                    "magnitude": 122.384486145561,
                    "measurement_mrid": "_daabb836-977c-49dd-afda-006a4becfead"
                },
                {
                    "angle": -35.2732090356479,
                    "magnitude": 127.44727272315,
                    "measurement_mrid": "_3b38f393-444f-4920-8aed-30d77ca900ff"
                },
                {
                    "angle": -35.2732090356479,
                    "magnitude": 127.44727272315,
                    "measurement_mrid": "_f41f8700-8f38-4d49-9aa5-215811fb3868"
                },
                {
                    "angle": 85.9348259203131,
                    "magnitude": 121.533714929787,
                    "measurement_mrid": "_5ffe4921-20be-4cd1-9127-ce4669cb821a"
                },
                {
                    "angle": 85.8918948318594,
                    "magnitude": 122.349095573429,
                    "measurement_mrid": "_663c7288-0feb-49b0-9b43-34d4867575c2"
                },
                {
                    "angle": 86.2183390962991,
                    "magnitude": 122.211224056436,
                    "measurement_mrid": "_1cd481ff-3e45-40f8-b554-59e713ded5ef"
                },
                {
                    "angle": 86.2183390962991,
                    "magnitude": 122.211224056436,
                    "measurement_mrid": "_53bfc06b-6573-4268-88d3-6c9d3b013aeb"
                },
                {
                    "angle": 86.2335848772284,
                    "magnitude": 7397.21924723481,
                    "measurement_mrid": "_31c68f50-63dc-4843-8d9c-8bcb2fb1286a"
                },
                {
                    "angle": 86.2797776180798,
                    "magnitude": 7340.26711744587,
                    "measurement_mrid": "_c99b07da-7f49-427b-9ddb-73e0aa1214e4"
                },
                {
                    "angle": 87.2222304151318,
                    "magnitude": 7252.42189276221,
                    "measurement_mrid": "_58e78614-2a63-4812-826c-f9103b01207e"
                },
                {
                    "angle": -156.417953379535,
                    "magnitude": 7879.76761451382,
                    "measurement_mrid": "_281ecada-7b9b-4f63-9448-08bbe0f64dd7"
                },
                {
                    "angle": -155.297782618666,
                    "magnitude": 7619.25897074922,
                    "measurement_mrid": "_fffb4c05-5fd0-4da8-88f5-27f0dc72d2b7"
                },
                {
                    "angle": 88.8816760731883,
                    "magnitude": 7221.86951657912,
                    "measurement_mrid": "_5041d0de-8f09-4ba9-9a03-61310fe69f3a"
                },
                {
                    "angle": -35.8849567478773,
                    "magnitude": 137.356095885477,
                    "measurement_mrid": "_5f35deae-4ebb-49bc-8f1d-7b2fa5690e26"
                },
                {
                    "angle": -35.9070469588382,
                    "magnitude": 137.830049100378,
                    "measurement_mrid": "_6c5aec4c-bd70-4cfd-8343-89d18868d5d4"
                },
                {
                    "angle": 85.9791017716259,
                    "magnitude": 120.79857276726,
                    "measurement_mrid": "_05cd2609-a1fa-4ae3-a680-c13bee8f47bb"
                },
                {
                    "angle": 85.9617678648968,
                    "magnitude": 121.124503067426,
                    "measurement_mrid": "_c0d123cd-9885-4cb9-9c9b-9d3683f32969"
                },
                {
                    "angle": -35.870477529582,
                    "magnitude": 8235.65782390374,
                    "measurement_mrid": "_01d70c13-aae7-420b-8097-5fd677e653b1"
                },
                {
                    "angle": 86.2177573777694,
                    "magnitude": 7337.57679964542,
                    "measurement_mrid": "_ebd035d5-f10d-4025-b4ee-a714e570f843"
                },
                {
                    "angle": -35.8704367483452,
                    "magnitude": 8235.67117158094,
                    "measurement_mrid": "_5ea2cee6-4e94-429b-9d96-e8f013f08911"
                },
                {
                    "angle": -155.70852540302,
                    "magnitude": 7748.1467117375,
                    "measurement_mrid": "_d0e64b8a-f8b3-4f0a-b5c6-a8edd3d505bd"
                },
                {
                    "angle": 86.2515861646335,
                    "magnitude": 7406.43946610763,
                    "measurement_mrid": "_2800c15a-8277-4ac9-98ec-ec546dcedbc6"
                },
                {
                    "angle": 88.4296173225594,
                    "magnitude": 119.915051326148,
                    "measurement_mrid": "_3ad5f0b5-0256-45f1-8819-b10e6bbedef4"
                },
                {
                    "angle": 88.4471264546436,
                    "magnitude": 119.589120967616,
                    "measurement_mrid": "_f7169dbb-50f5-4444-856e-593ec3275238"
                },
                {
                    "angle": -35.5903644208874,
                    "magnitude": 8312.62564156332,
                    "measurement_mrid": "_4ffc5a6c-0267-44f1-8034-fd0cc0b2ffc5"
                },
                {
                    "angle": 86.1065444412095,
                    "magnitude": 7324.99232870222,
                    "measurement_mrid": "_c80b39be-28a5-4055-9b9b-346b5dabedc6"
                },
                {
                    "angle": -156.359515312672,
                    "magnitude": 7913.54988188704,
                    "measurement_mrid": "_da1bc7a2-9407-4f85-9a2e-f50034dce0b5"
                },
                {
                    "angle": -156.196821463883,
                    "magnitude": 128.229402869636,
                    "measurement_mrid": "_6d2c8e99-84d9-4bfb-930e-b5aa7c630218"
                },
                {
                    "angle": -156.170695025782,
                    "magnitude": 127.709515197114,
                    "measurement_mrid": "_f19910ed-589c-45b7-a588-d73e4d567fb8"
                },
                {
                    "angle": 86.3540809346211,
                    "magnitude": 7338.6534877612,
                    "measurement_mrid": "_43746417-bf85-4f63-a8e0-935f46fa1193"
                },
                {
                    "angle": -35.2931763286017,
                    "magnitude": 128.360405426214,
                    "measurement_mrid": "_d3060ce4-d6ce-4231-8376-ef2ec926ff48"
                },
                {
                    "angle": -35.2694421893912,
                    "magnitude": 127.886455194513,
                    "measurement_mrid": "_d6bb3b37-306c-4639-8547-2e0cc8071046"
                },
                {
                    "angle": -154.05625952559,
                    "magnitude": 7292.34583028914,
                    "measurement_mrid": "_b3e2cf95-8ec0-41c7-a5ce-e30758ee67f7"
                },
                {
                    "angle": 86.2449677027023,
                    "magnitude": 7403.01066820968,
                    "measurement_mrid": "_58c9991d-c9ab-47a4-aa87-305d88a310bd"
                },
                {
                    "angle": -156.41550582204,
                    "magnitude": 7895.16813536339,
                    "measurement_mrid": "_c9b4221c-c082-4834-b5b8-bb14a867fe23"
                },
                {
                    "angle": 87.1340121615846,
                    "magnitude": 7372.3440497235,
                    "measurement_mrid": "_8efe9e47-fa12-4976-80ca-567115a6772c"
                },
                {
                    "angle": -34.3769653008027,
                    "magnitude": 8016.36554203463,
                    "measurement_mrid": "_d6621bdb-c80c-4bbe-a1b5-b0d941c3989a"
                },
                {
                    "angle": -154.70252296197,
                    "magnitude": 7781.44679052582,
                    "measurement_mrid": "_db484048-b17b-41ff-b3c3-8916ce80af1e"
                },
                {
                    "angle": -156.159529054265,
                    "magnitude": 127.953184929077,
                    "measurement_mrid": "_575429b3-e52b-450a-b893-03a2117405be"
                },
                {
                    "angle": -156.17520602235,
                    "magnitude": 128.265221859168,
                    "measurement_mrid": "_a367f2db-ce96-4469-aa13-1444f4a891db"
                },
                {
                    "measurement_mrid": "_36df2d8b-2906-4c33-9f0d-1c42fefdda9f",
                    "value": 2
                },
                {
                    "measurement_mrid": "_3783e729-3328-4983-9db7-23f6befa3536",
                    "value": 1
                },
                {
                    "measurement_mrid": "_59f92d0d-7e9b-45dc-bf67-b17510fcc22a",
                    "value": 1
                },
                {
                    "measurement_mrid": "_a929c951-c185-4eb1-bdf7-010be27dedc6",
                    "value": 2
                },
                {
                    "measurement_mrid": "_bb1eda2e-c31d-4180-964a-3ab906b8d629",
                    "value": 2
                },
                {
                    "measurement_mrid": "_ca7585ec-e609-4eb8-b0ce-9f44dc42e918",
                    "value": 2
                },
                {
                    "angle": -34.2130711718171,
                    "magnitude": 119.170245241226,
                    "measurement_mrid": "_65eece99-f496-4354-81e1-b5a2c49fe22c"
                },
                {
                    "angle": -34.2638229871688,
                    "magnitude": 120.118164651402,
                    "measurement_mrid": "_975ae497-aa2d-4fe6-a3f8-3eaaec0590b6"
                },
                {
                    "angle": 88.2780723980007,
                    "magnitude": 7296.95295935025,
                    "measurement_mrid": "_3749eb4b-ec5c-4610-a744-938828e127ee"
                },
                {
                    "angle": -34.5669699694498,
                    "magnitude": 8005.86027971865,
                    "measurement_mrid": "_9476812a-cbce-46ce-8d81-160b577cddac"
                },
                {
                    "angle": -154.956164797957,
                    "magnitude": 7777.65490597326,
                    "measurement_mrid": "_a7f89636-1ae8-4fd0-9327-fcf431f254d0"
                },
                {
                    "angle": 87.0185805582685,
                    "magnitude": 7377.74340333267,
                    "measurement_mrid": "_b6dfffb5-cb4a-4f98-8a75-ea215aeb5a66"
                },
                {
                    "angle": -36.1175834156938,
                    "magnitude": 136.564852755605,
                    "measurement_mrid": "_2812248c-ad75-46c9-9c0d-5182e9ab9c5f"
                },
                {
                    "angle": -36.1175834156938,
                    "magnitude": 136.564852755605,
                    "measurement_mrid": "_a14bbe83-22b3-40bb-bfc3-24eb15c0e090"
                },
                {
                    "angle": 86.2579668279011,
                    "magnitude": 7409.90477373011,
                    "measurement_mrid": "_b773bd60-f765-42e0-ba6c-397e13981af6"
                },
                {
                    "angle": -35.6094237901982,
                    "magnitude": 8319.51438053203,
                    "measurement_mrid": "_8a491992-f672-49a9-ba1b-5bfe9469b16c"
                },
                {
                    "angle": 86.3156394433624,
                    "magnitude": 7347.84140031468,
                    "measurement_mrid": "_a92bb238-8a19-4c95-80b1-7493a4ae6a20"
                },
                {
                    "angle": -156.228926679967,
                    "magnitude": 7959.2588971171,
                    "measurement_mrid": "_bc662e73-7e60-4b2d-8e6b-6e10cd6a495f"
                },
                {
                    "angle": 87.7700906685692,
                    "magnitude": 7306.88644707011,
                    "measurement_mrid": "_41a5682f-f53a-44a0-bb30-742ecd04cc8e"
                },
                {
                    "angle": -152.961441191479,
                    "magnitude": 7318.71709084077,
                    "measurement_mrid": "_5c4f3d0f-d866-4e20-8e3d-1c434d859407"
                },
                {
                    "angle": -32.8542772579543,
                    "magnitude": 7303.31760149315,
                    "measurement_mrid": "_63109df3-c439-47b1-b64a-1a8c01d11a8a"
                },
                {
                    "angle": -152.991242478554,
                    "magnitude": 7318.12456328969,
                    "measurement_mrid": "_0472fccd-7309-479f-b3b0-9400200631dd"
                },
                {
                    "angle": -32.8803286566115,
                    "magnitude": 7301.72375379685,
                    "measurement_mrid": "_975ca386-0594-4431-a631-0a0288357288"
                },
                {
                    "angle": 87.7580950896269,
                    "magnitude": 7307.07788476456,
                    "measurement_mrid": "_99795c50-0e26-455b-81fd-b4cfbf3ea174"
                },
                {
                    "angle": -153.030941464518,
                    "magnitude": 7317.34967790537,
                    "measurement_mrid": "_0e7a7676-3251-40db-a183-619cb60dfcd0"
                },
                {
                    "angle": -32.9149283094521,
                    "magnitude": 7299.5916101193,
                    "measurement_mrid": "_6c077ea9-0643-49f0-a929-864cd0f76f7c"
                },
                {
                    "angle": 87.7424061768818,
                    "magnitude": 7307.3545106264,
                    "measurement_mrid": "_9ea51f8a-348e-40fa-a7fc-6c919f50ae4e"
                },
                {
                    "angle": -35.8035285309603,
                    "magnitude": 8264.84128131684,
                    "measurement_mrid": "_9af4a16a-a120-461e-8301-8a8e8f9054e1"
                },
                {
                    "angle": -31.4618028597333,
                    "magnitude": 121.172569629478,
                    "measurement_mrid": "_15ff4227-d41e-406a-a828-9aad0256eb84"
                },
                {
                    "angle": -31.4618028597333,
                    "magnitude": 121.172569629478,
                    "measurement_mrid": "_5fb85d2f-3258-48fe-9dbe-2459429b6c63"
                },
                {
                    "angle": -153.140951513444,
                    "magnitude": 7315.16766983464,
                    "measurement_mrid": "_b63b46f3-1889-4c75-9371-3686829b5727"
                },
                {
                    "angle": -33.0101752859963,
                    "magnitude": 7293.76466031859,
                    "measurement_mrid": "_c00d7b90-9329-468b-b303-a78516313a15"
                },
                {
                    "angle": 87.6985897370133,
                    "magnitude": 7308.14393760736,
                    "measurement_mrid": "_dd17704f-62f0-4418-9e6d-493e8b0637c4"
                },
                {
                    "angle": -153.109037710292,
                    "magnitude": 7315.79780829502,
                    "measurement_mrid": "_39ecdd73-831f-43be-b171-0e410883ab99"
                },
                {
                    "angle": 87.7112971030521,
                    "magnitude": 7307.91457117842,
                    "measurement_mrid": "_41d97ab9-62b9-40ec-92d0-2b498c0b239a"
                },
                {
                    "angle": -32.982534466147,
                    "magnitude": 7295.45266750672,
                    "measurement_mrid": "_d12d839c-991e-46b7-abb4-4eb199199c5c"
                },
                {
                    "angle": -34.846890122542,
                    "magnitude": 7705.89140456466,
                    "measurement_mrid": "_544a1ff4-8fa9-4f81-baa4-ce56b631e519"
                },
                {
                    "angle": -34.8455455976221,
                    "magnitude": 7706.63180659185,
                    "measurement_mrid": "_1232fe22-8ce4-46e1-85d1-c1f196e8edc1"
                },
                {
                    "angle": -35.7068238856508,
                    "magnitude": 8261.49944694273,
                    "measurement_mrid": "_52c81199-cced-4a8b-ae9f-fbf19f615480"
                },
                {
                    "angle": -155.24614105819,
                    "magnitude": 7646.19357226797,
                    "measurement_mrid": "_ba457274-7e76-4c96-b9fc-fc46cc0ac47a"
                },
                {
                    "angle": 87.2630750328983,
                    "magnitude": 120.263464427508,
                    "measurement_mrid": "_108c2fd7-13c8-499c-a11d-131315ef8df1"
                },
                {
                    "angle": 87.2196926908709,
                    "magnitude": 121.078845768871,
                    "measurement_mrid": "_ccf7cb73-067c-4493-8c93-fe8e7ad83120"
                },
                {
                    "angle": -156.209009914529,
                    "magnitude": 7966.81906237334,
                    "measurement_mrid": "_18847bff-60b4-4ab8-977e-ef460a056e6e"
                },
                {
                    "angle": 86.352338269016,
                    "magnitude": 7352.14220807781,
                    "measurement_mrid": "_4c1d63e7-fa25-45e6-826b-52982ab28072"
                },
                {
                    "angle": -35.6114689496755,
                    "magnitude": 8320.59649634019,
                    "measurement_mrid": "_7c8db235-7e03-4ea2-87a3-8bd914c5f755"
                },
                {
                    "angle": -152.68230347102,
                    "magnitude": 7323.89280782149,
                    "measurement_mrid": "_04d4f38a-5ebd-47e5-8735-f0aeeca02a5d"
                },
                {
                    "angle": -32.6005614368164,
                    "magnitude": 7314.27877229327,
                    "measurement_mrid": "_618342bf-0177-4d59-b6c3-04b3d10c4956"
                },
                {
                    "angle": 87.9227949674769,
                    "magnitude": 7306.24311738891,
                    "measurement_mrid": "_c5a6fc7b-c442-47cb-b3a6-1b18b4e8105c"
                },
                {
                    "angle": 86.4403934820813,
                    "magnitude": 7391.35939230924,
                    "measurement_mrid": "_3c6579eb-f2d5-4c8d-b49b-be6631cfe1af"
                },
                {
                    "angle": -156.162682703348,
                    "magnitude": 8005.81529880412,
                    "measurement_mrid": "_40acd3dd-998d-4616-95d6-cf16400b82d2"
                },
                {
                    "angle": -35.5801329454897,
                    "magnitude": 8355.62665292412,
                    "measurement_mrid": "_c9aea6a3-4efb-4a84-ac17-9ee6069adb16"
                },
                {
                    "angle": -36.1324956865091,
                    "magnitude": 136.225800615402,
                    "measurement_mrid": "_0cfd0892-93a9-43b1-b266-2fc47dd54762"
                },
                {
                    "angle": -36.145869924268,
                    "magnitude": 136.510064384928,
                    "measurement_mrid": "_cea31f56-9b8c-492a-827d-38e6105c497a"
                },
                {
                    "angle": -156.192951105263,
                    "magnitude": 128.63095077601,
                    "measurement_mrid": "_3dd832d1-eec3-498b-b1fa-4e8d74661c03"
                },
                {
                    "angle": -156.140888455113,
                    "magnitude": 127.591682986771,
                    "measurement_mrid": "_b27085ed-5b2e-4243-b5fd-3ef4e4574c40"
                },
                {
                    "angle": -170.08835637171,
                    "magnitude": 0.357620715756232,
                    "measurement_mrid": "_aee487c4-0da8-4a54-a944-b67e9c66ab90"
                },
                {
                    "angle": -155.578466196323,
                    "magnitude": 127.356225258596,
                    "measurement_mrid": "_4b08c099-e707-49fe-ac3e-042987f8737c"
                },
                {
                    "angle": -155.578466196323,
                    "magnitude": 127.356225258596,
                    "measurement_mrid": "_e0b0570d-7310-4919-9a7b-38587e24efdc"
                },
                {
                    "angle": 86.4261537640492,
                    "magnitude": 7387.22763107815,
                    "measurement_mrid": "_a6500456-72af-4fba-a1ee-db50def9d2df"
                },
                {
                    "angle": -154.512412997177,
                    "magnitude": 119.654380960632,
                    "measurement_mrid": "_b369f82e-ab76-4b97-bb5e-57ec5fb1a6de"
                },
                {
                    "angle": -154.595282356918,
                    "magnitude": 121.213601680537,
                    "measurement_mrid": "_fe1fa0e6-2917-43b9-860d-3782e19591c2"
                },
                {
                    "angle": 87.1869410004036,
                    "magnitude": 7234.97595328391,
                    "measurement_mrid": "_9b186b4e-a6ad-4adb-b041-c091bb6b574a"
                },
                {
                    "angle": 87.1853734073324,
                    "magnitude": 7234.18253053313,
                    "measurement_mrid": "_127f2a28-f763-4c06-a76f-ffd2b827790b"
                },
                {
                    "angle": 87.1848852948348,
                    "magnitude": 7233.96568740027,
                    "measurement_mrid": "_03667716-20e3-4c97-a4b4-6a5a23fe90c5"
                },
                {
                    "angle": -156.900978458813,
                    "magnitude": 130.273051377762,
                    "measurement_mrid": "_5d61aad1-cc54-417d-9b91-0ac3ca9c00b3"
                },
                {
                    "angle": -156.900978458813,
                    "magnitude": 130.273051377762,
                    "measurement_mrid": "_92b10ea3-a336-4cd5-9f7a-0b76d185a6bf"
                },
                {
                    "angle": 87.1871981765488,
                    "magnitude": 7235.10232783862,
                    "measurement_mrid": "_814ba679-3ec0-4782-917d-3e61afa0e9b5"
                },
                {
                    "angle": -156.953045808264,
                    "magnitude": 131.137893781975,
                    "measurement_mrid": "_76801f7f-096c-4d05-8279-006e50599b82"
                },
                {
                    "angle": -156.94283166867,
                    "magnitude": 130.930049072584,
                    "measurement_mrid": "_b6d0bc42-7c0c-4489-9805-4b650c925007"
                },
                {
                    "angle": -34.2403701225649,
                    "magnitude": 7215.23001703052,
                    "measurement_mrid": "_7e4c3ee1-2c4c-4781-9af0-05f3e149506c"
                },
                {
                    "angle": 87.1843160932867,
                    "magnitude": 7233.67719501201,
                    "measurement_mrid": "_1488e3e3-1029-44e6-a00b-2748845afa5b"
                },
                {
                    "angle": -36.1642161542365,
                    "magnitude": 137.377235210274,
                    "measurement_mrid": "_35174757-9c6e-4733-8c45-5e65d583ace9"
                },
                {
                    "angle": -36.1642161542365,
                    "magnitude": 137.377235210274,
                    "measurement_mrid": "_3683b310-d800-4c9a-b6b0-f18420ce7645"
                },
                {
                    "angle": -34.2401105278951,
                    "magnitude": 7215.35783949498,
                    "measurement_mrid": "_6d96b66a-57d9-4fb9-87a2-867974c21841"
                },
                {
                    "angle": -156.574569117126,
                    "magnitude": 131.970378178145,
                    "measurement_mrid": "_618903e6-4345-496d-8e45-d8bd2719b440"
                },
                {
                    "angle": -156.574569117126,
                    "magnitude": 131.970378178145,
                    "measurement_mrid": "_d3fe219f-8aaf-479a-9478-03904a11d7c8"
                },
                {
                    "angle": -35.996557976751,
                    "magnitude": 137.922345022528,
                    "measurement_mrid": "_34c57962-3d3e-4ec4-b776-56e11cd437e9"
                },
                {
                    "angle": -35.9634599277977,
                    "magnitude": 137.211673689681,
                    "measurement_mrid": "_d9aa091c-3b4d-4a23-a613-3faf109b4a65"
                },
                {
                    "angle": -36.1707059709813,
                    "magnitude": 137.337455083548,
                    "measurement_mrid": "_906702a0-b9d2-4488-9bb5-6b67bb280a28"
                },
                {
                    "angle": -36.1707059709813,
                    "magnitude": 137.337455083548,
                    "measurement_mrid": "_9ddce6c2-dc0b-4869-b7fe-d7d900d7bd64"
                },
                {
                    "angle": -156.406971247077,
                    "magnitude": 7885.54486009534,
                    "measurement_mrid": "_846b8444-5a36-49b6-b970-3f2b212bc54f"
                },
                {
                    "angle": -155.246679251635,
                    "magnitude": 7773.43968917738,
                    "measurement_mrid": "_1f4babe8-a0b3-4aeb-b37d-2f786d2c4b77"
                },
                {
                    "angle": 86.8894660335459,
                    "magnitude": 7384.33618378358,
                    "measurement_mrid": "_84e4ae14-63bb-47c2-9075-d8355d69a150"
                },
                {
                    "angle": -34.7808885115928,
                    "magnitude": 7994.02652515706,
                    "measurement_mrid": "_b3a721ec-9fe0-4ea5-81e0-e10f8b3eab3f"
                },
                {
                    "angle": 86.3712002203666,
                    "magnitude": 7351.00804643369,
                    "measurement_mrid": "_10e97d12-4ada-4ff2-81f0-fe47a28a05a5"
                },
                {
                    "angle": -35.8237660944973,
                    "magnitude": 8261.42051562762,
                    "measurement_mrid": "_bd719e7a-c886-4e19-9323-df3200dda426"
                },
                {
                    "angle": -156.453650190945,
                    "magnitude": 7949.54035076198,
                    "measurement_mrid": "_da5b62ae-711e-468f-b688-598354a1c18d"
                },
                {
                    "angle": -34.7580903028437,
                    "magnitude": 7995.27642998602,
                    "measurement_mrid": "_ab596d73-e6c2-4ae6-911a-2b82eca36428"
                },
                {
                    "angle": -155.215609306104,
                    "magnitude": 7773.88919065653,
                    "measurement_mrid": "_ca93f25e-34ae-490a-b76b-68070b0b2d3f"
                },
                {
                    "angle": 86.9033118558639,
                    "magnitude": 7383.62673489348,
                    "measurement_mrid": "_fb4ccd39-aaf1-44cc-91f5-f92372aa1700"
                },
                {
                    "angle": -156.952904439581,
                    "magnitude": 130.993340714088,
                    "measurement_mrid": "_1983a887-4c58-47ac-ae7c-a66914ad55b9"
                },
                {
                    "angle": -156.952904439581,
                    "magnitude": 130.993340714088,
                    "measurement_mrid": "_c15ee61f-bc55-494d-825b-5b810bba84a7"
                },
                {
                    "angle": -34.7996055589667,
                    "magnitude": 7993.01372383391,
                    "measurement_mrid": "_4be1c8a1-2d57-48d6-ab3e-4326af0a5769"
                },
                {
                    "angle": 86.877802899589,
                    "magnitude": 7384.93483200787,
                    "measurement_mrid": "_cdfcc1c6-9555-4f8c-b036-844f0ed2788d"
                },
                {
                    "angle": -155.272533755908,
                    "magnitude": 7773.04601488351,
                    "measurement_mrid": "_fb842efb-3b49-43ad-9aaf-02cc7dd808b2"
                },
                {
                    "angle": -154.377853063419,
                    "magnitude": 7760.79913638882,
                    "measurement_mrid": "_804033e8-be6f-431f-8349-1ba9328d3daa"
                },
                {
                    "angle": -34.2432142083776,
                    "magnitude": 7795.65909412437,
                    "measurement_mrid": "_98dd9836-7fac-4df2-9686-d140d209905b"
                },
                {
                    "angle": 86.2079869193627,
                    "magnitude": 7415.63556983442,
                    "measurement_mrid": "_d06c102d-aee1-4ecb-bfea-a74aac5212b8"
                },
                {
                    "angle": -34.6300924587306,
                    "magnitude": 8002.04957332865,
                    "measurement_mrid": "_42416f23-fedc-4ff8-9501-110887d063d0"
                },
                {
                    "angle": -35.6223945293592,
                    "magnitude": 8319.03297243328,
                    "measurement_mrid": "_7946bbc3-b6ae-4222-bce1-3e852a5a3082"
                },
                {
                    "angle": -35.6228670192696,
                    "magnitude": 8318.87619720845,
                    "measurement_mrid": "_9313bfba-6a4d-4359-92e8-fbdedf236a30"
                },
                {
                    "angle": -34.6015311558761,
                    "magnitude": 8003.9220047313,
                    "measurement_mrid": "_17cf1ffa-f925-4f36-95b6-ffd76c1c6b96"
                },
                {
                    "angle": -155.002646652457,
                    "magnitude": 7776.99714425356,
                    "measurement_mrid": "_a135e89d-0df5-43ef-b14f-8591256f642b"
                },
                {
                    "angle": 86.9981006681839,
                    "magnitude": 7378.78511116708,
                    "measurement_mrid": "_a71fc345-bbbd-4303-bc21-873278b064d1"
                },
                {
                    "angle": -34.6979010840676,
                    "magnitude": 7998.58392015317,
                    "measurement_mrid": "_210666ab-aad5-4ded-8324-e12a96553b4c"
                },
                {
                    "angle": 86.9398998285909,
                    "magnitude": 7381.75453993223,
                    "measurement_mrid": "_9f457613-f573-4254-a632-698d6245fb69"
                },
                {
                    "angle": -155.133553158955,
                    "magnitude": 7775.08725042808,
                    "measurement_mrid": "_fda8c61b-3f5d-45f0-8446-9f5fcad0b554"
                },
                {
                    "angle": 86.7270373476662,
                    "magnitude": 7394.43946556819,
                    "measurement_mrid": "_0ca1bba8-bf12-4bd4-8331-8c1332983a96"
                },
                {
                    "angle": -155.634165026084,
                    "magnitude": 7767.16772386355,
                    "measurement_mrid": "_b0f0ce27-4646-4043-bb78-8c399b82ff93"
                },
                {
                    "angle": -35.0471435776389,
                    "magnitude": 7978.6283312058,
                    "measurement_mrid": "_bcffe38f-0907-42e7-8cf2-b1ad6bc5e312"
                },
                {
                    "angle": -35.8832614315927,
                    "magnitude": 8231.53554862715,
                    "measurement_mrid": "_a80d18d0-9167-4049-9253-7135f7b3faf1"
                },
                {
                    "angle": -35.0360534258803,
                    "magnitude": 132.421888470194,
                    "measurement_mrid": "_2473cb09-a5cc-4bdc-a926-e6df73814371"
                },
                {
                    "angle": -35.0360534258803,
                    "magnitude": 132.421888470194,
                    "measurement_mrid": "_76440b52-9b73-4fb3-9755-365409c42657"
                },
                {
                    "angle": -34.6745942058916,
                    "magnitude": 119.099139455882,
                    "measurement_mrid": "_33091595-f4bd-4c79-901e-735ba0e62ff6"
                },
                {
                    "angle": -34.7000810585272,
                    "magnitude": 119.573088650988,
                    "measurement_mrid": "_5a37cc21-9fd5-47e5-ae7b-1c7bbcfd2493"
                },
                {
                    "angle": -155.040296305272,
                    "magnitude": 7776.46808949621,
                    "measurement_mrid": "_118f77c9-1c55-4d06-9167-3e6fed104179"
                },
                {
                    "angle": 86.9815191607038,
                    "magnitude": 7379.6293697586,
                    "measurement_mrid": "_29699ca0-708c-4baf-aa20-5a5977998f81"
                },
                {
                    "angle": -34.6295330838432,
                    "magnitude": 8002.35429785697,
                    "measurement_mrid": "_6ab41052-e89a-4827-acd6-89dd7124dfb4"
                },
                {
                    "angle": -155.08403841361,
                    "magnitude": 7775.81785703354,
                    "measurement_mrid": "_2299bec5-7236-41fe-9be8-2d238e097b1c"
                },
                {
                    "angle": -34.6615961816063,
                    "magnitude": 8000.58429017693,
                    "measurement_mrid": "_94744139-ae73-40ba-a2f5-a408fdd0ba14"
                },
                {
                    "angle": 86.9619926970921,
                    "magnitude": 7380.62583842929,
                    "measurement_mrid": "_9e0511fc-c326-4805-b34e-dbc260b657d5"
                },
                {
                    "angle": 86.8497552984002,
                    "magnitude": 7386.10973349524,
                    "measurement_mrid": "_aa04ff71-fd74-4cad-8396-e872a45fc7a5"
                },
                {
                    "angle": -33.0137789286344,
                    "magnitude": 7334.7036070336,
                    "measurement_mrid": "_45fac8d2-191e-40b8-bfe0-1a3f2d6d66cd"
                },
                {
                    "angle": -36.0129143052621,
                    "magnitude": 137.956085891168,
                    "measurement_mrid": "_614b66d4-11f7-439c-ab0d-b49a58a897bf"
                },
                {
                    "angle": -35.9908440132427,
                    "magnitude": 137.482132748036,
                    "measurement_mrid": "_bd7a895a-4d59-41c7-832b-d171621276ce"
                },
                {
                    "angle": -156.849960467845,
                    "magnitude": 130.697703505758,
                    "measurement_mrid": "_18f54d0d-3b31-4f34-84b8-f1e9d0578f89"
                },
                {
                    "angle": -156.849960467845,
                    "magnitude": 130.697703505758,
                    "measurement_mrid": "_91a0e12f-a69b-4284-ad4d-c661d74e8c7a"
                },
                {
                    "angle": 86.1032708751698,
                    "magnitude": 7323.42466080722,
                    "measurement_mrid": "_0d5fc56b-4c0b-41c2-ae82-e248f7146a95"
                },
                {
                    "angle": -33.728592132426,
                    "magnitude": 7248.6400972027,
                    "measurement_mrid": "_a0f9e5a1-9842-4ec3-9c4a-adf782d2d0b9"
                },
                {
                    "angle": 87.4018188580468,
                    "magnitude": 7316.93414096986,
                    "measurement_mrid": "_f8006efa-3c92-4dd5-a437-40fbb0acf1f5"
                },
                {
                    "angle": -153.979657989566,
                    "magnitude": 7301.23868130736,
                    "measurement_mrid": "_fb483168-04d6-48dc-a4f1-967f0dc5b0fc"
                },
                {
                    "angle": -156.467189278795,
                    "magnitude": 7941.98876004489,
                    "measurement_mrid": "_c7939c35-03a8-4569-a6ce-78a9a4d42ff1"
                },
                {
                    "angle": -35.7297017351855,
                    "magnitude": 8247.22540032739,
                    "measurement_mrid": "_c852f356-dce9-4cae-98e6-2f9064098cbe"
                },
                {
                    "angle": -35.729703497527,
                    "magnitude": 8247.22560251962,
                    "measurement_mrid": "_38470c09-b62b-4027-b5bd-7f9ba22e74be"
                },
                {
                    "angle": 85.8533221509303,
                    "magnitude": 120.727283370375,
                    "measurement_mrid": "_15aeebf3-3588-4d2e-9baa-a5426dcd2a21"
                },
                {
                    "angle": 85.81010787669,
                    "magnitude": 121.542664102753,
                    "measurement_mrid": "_d981c11a-22c8-4f39-b2c1-7ff7d6053d31"
                },
                {
                    "angle": 87.2483099734542,
                    "magnitude": 120.700786523813,
                    "measurement_mrid": "_a5fd5dbf-1c45-4a57-9352-ae1ecb92b688"
                },
                {
                    "angle": 87.2483099734542,
                    "magnitude": 120.700786523813,
                    "measurement_mrid": "_efd441ee-9bc9-4ab2-acf3-2e942e6ee267"
                },
                {
                    "angle": -156.295483722059,
                    "magnitude": 7943.9450801079,
                    "measurement_mrid": "_970bc1d2-4473-4272-a239-93a04e092114"
                },
                {
                    "angle": -35.7297071945652,
                    "magnitude": 8247.22602721444,
                    "measurement_mrid": "_4f22951f-dd17-48fa-8fb1-dfd9c9d6330d"
                },
                {
                    "angle": 85.9481006699197,
                    "magnitude": 121.389507583536,
                    "measurement_mrid": "_0aa9839e-1a36-4562-b330-618e893162a8"
                },
                {
                    "angle": 85.9481006699197,
                    "magnitude": 121.389507583536,
                    "measurement_mrid": "_e243fdc7-9cc8-4160-bc05-4b12ca0bfde4"
                },
                {
                    "angle": -34.8243826566428,
                    "magnitude": 7763.56272350626,
                    "measurement_mrid": "_cce11662-0249-4665-9e5b-fb033e6cc0aa"
                },
                {
                    "angle": 86.4786714861775,
                    "magnitude": 7323.53566167307,
                    "measurement_mrid": "_2d790dcf-7869-4daa-b07e-b0c40a541353"
                },
                {
                    "angle": -156.128136245629,
                    "magnitude": 7980.04161023803,
                    "measurement_mrid": "_beeed87d-a6c2-499c-b645-a89d82c400e4"
                },
                {
                    "angle": -35.6965698168821,
                    "magnitude": 8264.61516558117,
                    "measurement_mrid": "_fb3f4bbe-7fbd-434e-bebd-899d92e37960"
                },
                {
                    "angle": 86.3921191578493,
                    "magnitude": 7362.56765669809,
                    "measurement_mrid": "_302ce9d2-4a67-4828-a785-a4998c6c64a6"
                },
                {
                    "angle": 88.9940068052704,
                    "magnitude": 7270.75642723867,
                    "measurement_mrid": "_d0e2641e-7339-4e3e-9147-67fe18538e89"
                },
                {
                    "angle": 86.5317193612798,
                    "magnitude": 7417.05535924604,
                    "measurement_mrid": "_011451ef-0903-4cc3-83f4-ce3d2480d565"
                },
                {
                    "angle": -155.993303753009,
                    "magnitude": 8039.94595577388,
                    "measurement_mrid": "_51aefef8-35c0-46c9-ab86-69bc81fb4ebd"
                },
                {
                    "angle": 86.5317193612798,
                    "magnitude": 7417.05535924604,
                    "measurement_mrid": "_573336d8-fb20-4f5a-b4b6-0bfac2ac32d2"
                },
                {
                    "angle": -155.993303753009,
                    "magnitude": 8039.94595577388,
                    "measurement_mrid": "_719fcef8-6504-46c8-b752-d9f4fbd0dd7d"
                },
                {
                    "angle": -35.4271664447342,
                    "magnitude": 8399.11387531773,
                    "measurement_mrid": "_c15518eb-f80b-4f41-ba70-6491db5fcb6a"
                },
                {
                    "angle": -35.4271664447342,
                    "magnitude": 8399.11387531773,
                    "measurement_mrid": "_fe5dc330-6803-474c-b811-9af0a605bb1a"
                },
                {
                    "angle": -35.7055311623597,
                    "magnitude": 8261.94856690685,
                    "measurement_mrid": "_e9606034-7637-4087-8f75-ffb4c562916d"
                },
                {
                    "angle": -156.918299893046,
                    "magnitude": 130.912984532819,
                    "measurement_mrid": "_9de58448-2b75-45ab-bd5c-10fe3b9c8d22"
                },
                {
                    "angle": -156.943790682176,
                    "magnitude": 131.432871715249,
                    "measurement_mrid": "_c2719e9b-0444-44e6-a19f-6ee3319e8835"
                },
                {
                    "angle": 87.1263044519329,
                    "magnitude": 7368.4426164777,
                    "measurement_mrid": "_c4e4d971-1588-4898-80eb-216c1a5dab4e"
                },
                {
                    "angle": 86.4054563980639,
                    "magnitude": 7370.13566954421,
                    "measurement_mrid": "_51ebd81d-5cba-4e36-8af3-d676d8eefe27"
                },
                {
                    "angle": 85.1374191450209,
                    "magnitude": 122.403274491798,
                    "measurement_mrid": "_193174ec-6663-4c2f-b4af-dc6c080f29b6"
                },
                {
                    "angle": 85.1089479963806,
                    "magnitude": 122.946676103657,
                    "measurement_mrid": "_82dda207-15aa-4249-bc0b-5f79dee4517a"
                },
                {
                    "angle": -34.8655032612989,
                    "magnitude": 7732.56830633629,
                    "measurement_mrid": "_4258e4bc-7638-4fd0-abb2-87a8b6e06c02"
                },
                {
                    "angle": 85.6269552789918,
                    "magnitude": 7424.47462615913,
                    "measurement_mrid": "_21392796-2a81-483e-a8cc-b37130d131ac"
                },
                {
                    "angle": -34.8613335572316,
                    "magnitude": 7753.24891399093,
                    "measurement_mrid": "_c78bb4d0-c6cb-4e80-9fbf-e3ecbc30eebd"
                },
                {
                    "angle": -155.133072440542,
                    "magnitude": 7711.71920672502,
                    "measurement_mrid": "_ef49f71b-7c41-4205-901c-3da0b17ca3c6"
                },
                {
                    "angle": -34.8611036636393,
                    "magnitude": 7754.80689063454,
                    "measurement_mrid": "_2a396888-a8da-449b-a620-ca208273b44a"
                },
                {
                    "angle": 85.6257611976437,
                    "magnitude": 7424.85534496711,
                    "measurement_mrid": "_85dfb003-1423-417a-8d53-256e9c16c73d"
                },
                {
                    "angle": -155.131015893001,
                    "magnitude": 7713.05536267096,
                    "measurement_mrid": "_f3abe2d5-223e-4ea4-8876-85859db04569"
                },
                {
                    "angle": -156.454339033965,
                    "magnitude": 7945.95843090458,
                    "measurement_mrid": "_a4d5c076-4213-45e4-a6aa-6d3d5a143c39"
                },
                {
                    "angle": -35.6930598740171,
                    "magnitude": 8324.64328266054,
                    "measurement_mrid": "_2331b0eb-cda2-438d-a6a2-a2da0bbe9133"
                },
                {
                    "angle": 86.4246211458086,
                    "magnitude": 7379.33171580578,
                    "measurement_mrid": "_624f28f6-f168-45d8-9a3d-f800cec5e2cd"
                },
                {
                    "angle": -156.269148871582,
                    "magnitude": 7989.92259706016,
                    "measurement_mrid": "_725230d3-3ce0-4f44-93e8-b8f57ba2df03"
                },
                {
                    "angle": -34.8618941996129,
                    "magnitude": 7753.00354727549,
                    "measurement_mrid": "_23463746-798a-40b5-92de-3323a3aa3b90"
                },
                {
                    "angle": -33.3817747242893,
                    "magnitude": 121.171929641779,
                    "measurement_mrid": "_0fcb802a-d4da-41ac-9576-9ff40eae70fd"
                },
                {
                    "angle": -33.3817747242893,
                    "magnitude": 121.171929641779,
                    "measurement_mrid": "_1c3820cf-07f4-4ebe-9318-ba184061140d"
                },
                {
                    "angle": 85.7475874007263,
                    "magnitude": 122.509237129674,
                    "measurement_mrid": "_67a55ea7-798c-432e-a601-6d9379ef8b52"
                },
                {
                    "angle": 85.7590220046127,
                    "magnitude": 122.291773180912,
                    "measurement_mrid": "_f1542f02-3941-458c-a234-c4a58020dca3"
                },
                {
                    "angle": 85.7350114910438,
                    "magnitude": 122.246838311014,
                    "measurement_mrid": "_8821457e-4b0c-456b-8d20-fb5db689d638"
                },
                {
                    "angle": 85.7350114910438,
                    "magnitude": 122.246838311014,
                    "measurement_mrid": "_c7b73ef6-6058-4ed3-976c-c7f888a49e30"
                },
                {
                    "angle": -35.2972409013438,
                    "magnitude": 128.171183120293,
                    "measurement_mrid": "_1c567de7-10bc-48dc-a698-1caae98d913a"
                },
                {
                    "angle": -35.2734724455862,
                    "magnitude": 127.697232418995,
                    "measurement_mrid": "_7e8eda35-2851-4c21-8267-32a1aead25fa"
                },
                {
                    "angle": 85.9555601819243,
                    "magnitude": 121.236575037126,
                    "measurement_mrid": "_52fb24da-b3ab-422b-abbd-92e4087618a0"
                },
                {
                    "angle": 85.9268158289585,
                    "magnitude": 121.779976629335,
                    "measurement_mrid": "_fb070995-851c-4915-98d0-d93edc1d742e"
                },
                {
                    "angle": -36.1628267263137,
                    "magnitude": 137.201928331972,
                    "measurement_mrid": "_4c082232-3483-4a5f-8745-d4b1bf6b1699"
                },
                {
                    "angle": -36.176108391227,
                    "magnitude": 137.486191776177,
                    "measurement_mrid": "_9cba3162-c1f7-4c43-b6a8-679b457a12be"
                },
                {
                    "angle": -156.856329231038,
                    "magnitude": 130.642562119071,
                    "measurement_mrid": "_35a11dfb-bc0f-4007-91e9-6ee6b35648aa"
                },
                {
                    "angle": -156.856329231038,
                    "magnitude": 130.642562119071,
                    "measurement_mrid": "_ab789f62-946e-4563-bd82-d3fb2d839365"
                },
                {
                    "angle": 86.7027378257178,
                    "magnitude": 7394.30582139108,
                    "measurement_mrid": "_5f5bc488-bcad-48ad-89df-a9d8e41a41e3"
                },
                {
                    "angle": -35.1013525186745,
                    "magnitude": 7976.97600384533,
                    "measurement_mrid": "_cc44e4d5-0a58-414c-ae02-551155f4fedf"
                },
                {
                    "angle": -155.672844960281,
                    "magnitude": 7768.6486596247,
                    "measurement_mrid": "_f87b0c56-8e23-4b0b-99da-0360b7c4ff4c"
                },
                {
                    "angle": -154.554656410986,
                    "magnitude": 120.428078130809,
                    "measurement_mrid": "_1e87e27c-beae-4075-a9ff-61926ea26755"
                },
                {
                    "angle": -154.554656410986,
                    "magnitude": 120.428078130809,
                    "measurement_mrid": "_a7a44072-3c56-4e2c-8a6f-fd72e9e181cf"
                },
                {
                    "angle": -33.2992523275272,
                    "magnitude": 120.777929669436,
                    "measurement_mrid": "_61c35c6c-29ba-40b4-935a-c3d9c02c5d6b"
                },
                {
                    "angle": -33.2992523275272,
                    "magnitude": 120.777929669436,
                    "measurement_mrid": "_63f4c032-a2cf-4469-b07e-170c1c4a1efe"
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.007716,
                    "measurement_mrid": "_11504448-3435-463e-bafb-fb94a42adcdb"
                },
                {
                    "angle": -155.854966094206,
                    "magnitude": 7764.43693323095,
                    "measurement_mrid": "_2bb7454b-bc20-41a5-90da-ede54a3b52f3"
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.007716,
                    "measurement_mrid": "_48c0a8c5-54f5-4032-8a94-f64581b1c7a6"
                },
                {
                    "measurement_mrid": "_577f7bfb-2fd4-43ba-897b-c5d750a70b0c",
                    "value": 1
                },
                {
                    "measurement_mrid": "_b6419656-0eb5-4c8c-8241-93af6952868d",
                    "value": 1
                },
                {
                    "angle": -155.854966094206,
                    "magnitude": 7764.43693323095,
                    "measurement_mrid": "_e8f65eca-a767-4617-a47a-0ac813ce6eb2"
                },
                {
                    "angle": 86.597025757018,
                    "magnitude": 7391.43570304343,
                    "measurement_mrid": "_4146b85e-c4e4-440c-bc1c-6f7170c08432"
                },
                {
                    "measurement_mrid": "_453a4a6d-4b77-4ec1-ba0e-edb056ab1ac4",
                    "value": 1
                },
                {
                    "angle": 86.597025757018,
                    "magnitude": 7391.43570304343,
                    "measurement_mrid": "_a0cc8edf-f826-4138-a26c-b6bbc7045526"
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.007716,
                    "measurement_mrid": "_a605392f-a8b5-4cca-add5-7f56047be5bc"
                },
                {
                    "angle": 90.0,
                    "magnitude": 0.007716,
                    "measurement_mrid": "_ac326333-f8cd-4c51-9b62-1d8010fcbaf4"
                },
                {
                    "measurement_mrid": "_ee7c5fef-0c2d-4a1e-a073-e337dbe5b311",
                    "value": 1
                }
            ],
            "timestamp": "2018-05-18 17:07:46.403679"
        },
        "simulation_id": "1062097031"
    },
    "timestamp": 531150
}
'''

str_output_8 = '''
{
    "ieee8500": {
        "cap_capbank0a": {
            "capacitor_A": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank0b": {
            "capacitor_B": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank0c": {
            "capacitor_C": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank1a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank1b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank1c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank2a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank2b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank2c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank3": {
            "capacitor_A": 300000.0,
            "capacitor_B": 300000.0,
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 0.0,
            "phases": "ABCN",
            "phases_connected": "NCBA",
            "pt_phase": "",
            "switchA": "CLOSED",
            "switchB": "CLOSED",
            "switchC": "CLOSED"
        },
        "nd__hvmv_sub_lsb": {
            "voltage_A": "6097.897641-3876.216603j V",
            "voltage_B": "-6395.084564-3374.206473j V",
            "voltage_C": "285.588913+7223.679479j V"
        },
        "nd_190-7361": {
            "voltage_A": "4880.420881-4552.087189j V",
            "voltage_B": "-6270.772434-1918.625385j V",
            "voltage_C": "1480.382908+6582.002027j V"
        },
        "nd_190-8581": {
            "voltage_A": "4425.740568-4760.070519j V",
            "voltage_B": "-6466.587127-1333.944616j V",
            "voltage_C": "1478.923270+6818.080038j V"
        },
        "nd_190-8593": {
            "voltage_A": "3873.637297-5061.524827j V",
            "voltage_B": "-6493.216700-618.093256j V",
            "voltage_C": "1826.776774+6735.529317j V"
        },
        "nd_l2673313": {
            "voltage_A": "3273.560830-4785.348257j V",
            "voltage_B": "-6147.877528-271.060340j V",
            "voltage_C": "1908.494726+6423.602576j V"
        },
        "nd_l2876814": {
            "voltage_A": "3363.317124-4843.946549j V",
            "voltage_B": "-6147.462115-269.296512j V",
            "voltage_C": "1905.220695+6505.698493j V"
        },
        "nd_l2955047": {
            "voltage_A": "4046.892500-4281.190101j V",
            "voltage_B": "-6034.905167-1307.288347j V",
            "voltage_C": "1433.878539+6740.744179j V"
        },
        "nd_l3160107": {
            "voltage_A": "4569.997316-4213.224832j V",
            "voltage_B": "-5837.296662-1826.602764j V",
            "voltage_C": "1405.199210+6416.227554j V"
        },
        "nd_l3254238": {
            "voltage_A": "4383.776858-4331.404601j V",
            "voltage_B": "-5865.206491-1529.444197j V",
            "voltage_C": "1544.903143+6380.370107j V"
        },
        "nd_m1047574": {
            "voltage_A": "3621.597751-4718.220426j V",
            "voltage_B": "-6217.145451-599.360367j V",
            "voltage_C": "1789.768136+6617.268110j V"
        },
        "rcon_FEEDER_REG": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG2": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG3": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG4": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "reg_FEEDER_REG": {
            "configuration": "rcon_FEEDER_REG",
            "phases": "ABC",
            "tap_A": 3,
            "tap_B": 3,
            "tap_C": 2,
            "to": "nd__hvmv_sub_lsb"
        },
        "reg_VREG2": {
            "configuration": "rcon_VREG2",
            "phases": "ABC",
            "tap_A": 11,
            "tap_B": 7,
            "tap_C": 3,
            "to": "nd_190-8593"
        },
        "reg_VREG3": {
            "configuration": "rcon_VREG3",
            "phases": "ABC",
            "tap_A": 16,
            "tap_B": 11,
            "tap_C": 2,
            "to": "nd_190-8581"
        },
        "reg_VREG4": {
            "configuration": "rcon_VREG4",
            "phases": "ABC",
            "tap_A": 13,
            "tap_B": 13,
            "tap_C": 6,
            "to": "nd_190-7361"
        },
        "xf_hvmv_sub": {
            "power_in_A": "7208010.474000+2375848.659577j VA",
            "power_in_B": "6619686.765355+1504448.106935j VA",
            "power_in_C": "7668524.439602+1430626.309647j VA"
        }
    }
}
'''

str_output_9 = ''' {
    "ieee8500": {
        "cap_capbank0a": {
            "capacitor_A": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank0b": {
            "capacitor_B": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank0c": {
            "capacitor_C": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank1a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank1b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank1c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank2a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank2b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank2c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank3": {
            "capacitor_A": 300000.0,
            "capacitor_B": 300000.0,
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 0.0,
            "phases": "ABCN",
            "phases_connected": "NCBA",
            "pt_phase": "",
            "switchA": "CLOSED",
            "switchB": "CLOSED",
            "switchC": "CLOSED"
        },
        "nd__hvmv_sub_lsb": {
            "voltage_A": "6064.561584-3845.670912j V",
            "voltage_B": "-6352.552659-3361.611265j V",
            "voltage_C": "276.907045+7179.756854j V"
        },
        "nd_190-7361": {
            "voltage_A": "4842.574443-4476.685167j V",
            "voltage_B": "-6188.665651-1939.201083j V",
            "voltage_C": "1439.949619+6505.686246j V"
        },
        "nd_190-8581": {
            "voltage_A": "4424.594669-4708.594658j V",
            "voltage_B": "-6385.646736-1373.465960j V",
            "voltage_C": "1432.367000+6738.674737j V"
        },
        "nd_190-8593": {
            "voltage_A": "3865.232110-4967.366940j V",
            "voltage_B": "-6370.129604-674.013526j V",
            "voltage_C": "1761.647748+6618.414260j V"
        },
        "nd_l2673313": {
            "voltage_A": "3275.878250-4690.132464j V",
            "voltage_B": "-6029.444772-334.685033j V",
            "voltage_C": "1841.889094+6312.023802j V"
        },
        "nd_l2876814": {
            "voltage_A": "3363.715906-4748.790729j V",
            "voltage_B": "-6029.028102-333.125542j V",
            "voltage_C": "1838.833919+6392.625249j V"
        },
        "nd_l2955047": {
            "voltage_A": "4044.821686-4235.230465j V",
            "voltage_B": "-5999.032930-1350.673031j V",
            "voltage_C": "1397.787032+6704.224490j V"
        },
        "nd_l3160107": {
            "voltage_A": "4563.436125-4171.693838j V",
            "voltage_B": "-5799.392012-1855.560368j V",
            "voltage_C": "1375.873475+6381.975298j V"
        },
        "nd_l3254238": {
            "voltage_A": "4354.789100-4256.497015j V",
            "voltage_B": "-5786.125219-1559.849657j V",
            "voltage_C": "1503.404081+6306.629357j V"
        },
        "nd_m1047574": {
            "voltage_A": "3637.596517-4661.598435j V",
            "voltage_B": "-6139.105216-656.801711j V",
            "voltage_C": "1736.935802+6543.527697j V"
        },
        "rcon_FEEDER_REG": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG2": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG3": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG4": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "reg_FEEDER_REG": {
            "configuration": "rcon_FEEDER_REG",
            "phases": "ABC",
            "tap_A": 2,
            "tap_B": 2,
            "tap_C": 1,
            "to": "nd__hvmv_sub_lsb"
        },
        "reg_VREG2": {
            "configuration": "rcon_VREG2",
            "phases": "ABC",
            "tap_A": 10,
            "tap_B": 6,
            "tap_C": 2,
            "to": "nd_190-8593"
        },
        "reg_VREG3": {
            "configuration": "rcon_VREG3",
            "phases": "ABC",
            "tap_A": 16,
            "tap_B": 10,
            "tap_C": 1,
            "to": "nd_190-8581"
        },
        "reg_VREG4": {
            "configuration": "rcon_VREG4",
            "phases": "ABC",
            "tap_A": 12,
            "tap_B": 12,
            "tap_C": 5,
            "to": "nd_190-7361"
        },
        "xf_hvmv_sub": {
            "power_in_A": "6998345.011202+2349120.682358j VA",
            "power_in_B": "6434345.874127+1458655.968384j VA",
            "power_in_C": "7487530.317505+1415431.857709j VA"
        }
    }
}
'''

string_out_10 = '''
{
    "ieee8500": {
        "cap_capbank0a": {
            "capacitor_A": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank0b": {
            "capacitor_B": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank0c": {
            "capacitor_C": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank1a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank1b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank1c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank2a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank2b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank2c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank3": {
            "capacitor_A": 300000.0,
            "capacitor_B": 300000.0,
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 0.0,
            "phases": "ABCN",
            "phases_connected": "NCBA",
            "pt_phase": "",
            "switchA": "CLOSED",
            "switchB": "CLOSED",
            "switchC": "CLOSED"
        },
        "nd__hvmv_sub_lsb": {
            "voltage_A": "6064.561531-3845.670872j V",
            "voltage_B": "-6352.552616-3361.611246j V",
            "voltage_C": "276.907035+7179.756939j V"
        },
        "nd_190-7361": {
            "voltage_A": "4842.574414-4476.685135j V",
            "voltage_B": "-6188.665591-1939.201088j V",
            "voltage_C": "1439.949634+6505.686314j V"
        },
        "nd_190-8581": {
            "voltage_A": "4424.594642-4708.594628j V",
            "voltage_B": "-6385.646674-1373.465974j V",
            "voltage_C": "1432.367017+6738.674800j V"
        },
        "nd_190-8593": {
            "voltage_A": "3865.232090-4967.366914j V",
            "voltage_B": "-6370.129537-674.013552j V",
            "voltage_C": "1761.647771+6618.414315j V"
        },
        "nd_l2673313": {
            "voltage_A": "3275.878235-4690.132443j V",
            "voltage_B": "-6029.444705-334.685065j V",
            "voltage_C": "1841.889119+6312.023852j V"
        },
        "nd_l2876814": {
            "voltage_A": "3363.715891-4748.790707j V",
            "voltage_B": "-6029.028036-333.125572j V",
            "voltage_C": "1838.833944+6392.625299j V"
        },
        "nd_l2955047": {
            "voltage_A": "4044.821661-4235.230437j V",
            "voltage_B": "-5999.032872-1350.673043j V",
            "voltage_C": "1397.787047+6704.224553j V"
        },
        "nd_l3160107": {
            "voltage_A": "4563.436097-4171.693807j V",
            "voltage_B": "-5799.391956-1855.560373j V",
            "voltage_C": "1375.873489+6381.975365j V"
        },
        "nd_l3254238": {
            "voltage_A": "4354.789075-4256.496985j V",
            "voltage_B": "-5786.125160-1559.849666j V",
            "voltage_C": "1503.404100+6306.629422j V"
        },
        "nd_m1047574": {
            "voltage_A": "3637.596498-4661.598410j V",
            "voltage_B": "-6139.105151-656.801735j V",
            "voltage_C": "1736.935824+6543.527751j V"
        },
        "rcon_FEEDER_REG": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG2": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG3": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG4": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "reg_FEEDER_REG": {
            "configuration": "rcon_FEEDER_REG",
            "phases": "ABC",
            "tap_A": 2,
            "tap_B": 2,
            "tap_C": 1,
            "to": "nd__hvmv_sub_lsb"
        },
        "reg_VREG2": {
            "configuration": "rcon_VREG2",
            "phases": "ABC",
            "tap_A": 10,
            "tap_B": 6,
            "tap_C": 2,
            "to": "nd_190-8593"
        },
        "reg_VREG3": {
            "configuration": "rcon_VREG3",
            "phases": "ABC",
            "tap_A": 16,
            "tap_B": 10,
            "tap_C": 1,
            "to": "nd_190-8581"
        },
        "reg_VREG4": {
            "configuration": "rcon_VREG4",
            "phases": "ABC",
            "tap_A": 12,
            "tap_B": 12,
            "tap_C": 5,
            "to": "nd_190-7361"
        },
        "xf_hvmv_sub": {
            "power_in_A": "6998344.830459+2349122.052855j VA",
            "power_in_B": "6434344.730717+1458655.626184j VA",
            "power_in_C": "7487531.138704+1415431.538127j VA"
        }
    }
}'''

str_output_11 = '''
{
    "ieee8500": {
        "cap_capbank0a": {
            "capacitor_A": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank0b": {
            "capacitor_B": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank0c": {
            "capacitor_C": 400000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank1a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank1b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank1c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank2a": {
            "capacitor_A": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 100.0,
            "phases": "AN",
            "phases_connected": "NA",
            "pt_phase": "A",
            "switchA": "CLOSED"
        },
        "cap_capbank2b": {
            "capacitor_B": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 101.0,
            "phases": "BN",
            "phases_connected": "NB",
            "pt_phase": "B",
            "switchB": "CLOSED"
        },
        "cap_capbank2c": {
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "BANK",
            "dwell_time": 102.0,
            "phases": "CN",
            "phases_connected": "NC",
            "pt_phase": "C",
            "switchC": "CLOSED"
        },
        "cap_capbank3": {
            "capacitor_A": 300000.0,
            "capacitor_B": 300000.0,
            "capacitor_C": 300000.0,
            "control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 0.0,
            "phases": "ABCN",
            "phases_connected": "NCBA",
            "pt_phase": "",
            "switchA": "CLOSED",
            "switchB": "CLOSED",
            "switchC": "CLOSED"
        },
        "nd__hvmv_sub_lsb": {
            "voltage_A": "6064.561531-3845.670872j V",
            "voltage_B": "-6352.552616-3361.611246j V",
            "voltage_C": "276.907035+7179.756939j V"
        },
        "nd_190-7361": {
            "voltage_A": "4842.574414-4476.685135j V",
            "voltage_B": "-6188.665591-1939.201088j V",
            "voltage_C": "1439.949634+6505.686314j V"
        },
        "nd_190-8581": {
            "voltage_A": "4424.594642-4708.594628j V",
            "voltage_B": "-6385.646674-1373.465974j V",
            "voltage_C": "1432.367017+6738.674800j V"
        },
        "nd_190-8593": {
            "voltage_A": "3865.232090-4967.366914j V",
            "voltage_B": "-6370.129537-674.013552j V",
            "voltage_C": "1761.647771+6618.414315j V"
        },
        "nd_l2673313": {
            "voltage_A": "3275.878235-4690.132443j V",
            "voltage_B": "-6029.444705-334.685065j V",
            "voltage_C": "1841.889119+6312.023852j V"
        },
        "nd_l2876814": {
            "voltage_A": "3363.715891-4748.790707j V",
            "voltage_B": "-6029.028036-333.125572j V",
            "voltage_C": "1838.833944+6392.625299j V"
        },
        "nd_l2955047": {
            "voltage_A": "4044.821661-4235.230437j V",
            "voltage_B": "-5999.032872-1350.673043j V",
            "voltage_C": "1397.787047+6704.224553j V"
        },
        "nd_l3160107": {
            "voltage_A": "4563.436097-4171.693807j V",
            "voltage_B": "-5799.391956-1855.560373j V",
            "voltage_C": "1375.873489+6381.975365j V"
        },
        "nd_l3254238": {
            "voltage_A": "4354.789075-4256.496985j V",
            "voltage_B": "-5786.125160-1559.849666j V",
            "voltage_C": "1503.404100+6306.629422j V"
        },
        "nd_m1047574": {
            "voltage_A": "3637.596498-4661.598410j V",
            "voltage_B": "-6139.105151-656.801735j V",
            "voltage_C": "1736.935824+6543.527751j V"
        },
        "rcon_FEEDER_REG": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG2": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG3": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "rcon_VREG4": {
            "band_center": 0.0,
            "band_width": 0.0,
            "connect_type": "WYE_WYE",
            "Control": "MANUAL",
            "control_level": "INDIVIDUAL",
            "dwell_time": 15.0,
            "lower_taps": 16,
            "PT_phase": "CBA",
            "raise_taps": 16,
            "regulation": 0.1
        },
        "reg_FEEDER_REG": {
            "configuration": "rcon_FEEDER_REG",
            "phases": "ABC",
            "tap_A": 2,
            "tap_B": 2,
            "tap_C": 1,
            "to": "nd__hvmv_sub_lsb"
        },
        "reg_VREG2": {
            "configuration": "rcon_VREG2",
            "phases": "ABC",
            "tap_A": 10,
            "tap_B": 6,
            "tap_C": 2,
            "to": "nd_190-8593"
        },
        "reg_VREG3": {
            "configuration": "rcon_VREG3",
            "phases": "ABC",
            "tap_A": 16,
            "tap_B": 10,
            "tap_C": 1,
            "to": "nd_190-8581"
        },
        "reg_VREG4": {
            "configuration": "rcon_VREG4",
            "phases": "ABC",
            "tap_A": 12,
            "tap_B": 12,
            "tap_C": 5,
            "to": "nd_190-7361"
        },
        "xf_hvmv_sub": {
            "power_in_A": "6998344.830459+2349122.052855j VA",
            "power_in_B": "6434344.730717+1458655.626184j VA",
            "power_in_C": "7487531.138704+1415431.538127j VA"
        }
    }
}
'''




# Import your CompareResults class from the relevant module

class TestManagerImpl:
    pass

class CompareResults:
    def __init__(self, logger):
        self.log = logger

    def get_prop(self, simOut):
        for out in simOut["output_objects"]:
            print(out["name"])
            # out.getProperties()
    def get_first(self, str_output):
        data = json.loads(str_output)
        first_key = list(data.keys())[0]
        return first_key

    def get_expected_output_map(self, path):
        pass

    def get_simulation_output(self, object1):
        pass

    def get_feeder(self):
        pass

    def compare_angle(self, object1, object2):
        angle1 = object1.get("angle")
        angle2 = object2.get("angle")
        return abs(angle1 - angle2) <= 0.1

    def compare_magnitude(self, object1, object2):
        magnitude1 = object1.get("magnitude")
        magnitude2 = object2.get("magnitude")
        return abs(magnitude1 - magnitude2) <= 1e-3

    def compare_expected_with_simulation(self, object1, object2):
        pass

    def compare_expected_with_simulation_output(self, object1, object2):
        pass

class TestCompareResults(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tm = TestManagerImpl()

    def setUp(self):

        self.tm = TestManagerImpl()
        self.log = getLogger(__name__)  # Mock()
        self.appManager = AppManager()  # Mock()
        self.clientFactory = ClientFactory()  # Mock()
        self.configurationManager = ConfigurationManager()  # Mock()
        self.simulationManager = LogManager()  # Mock()
        self.logManager = Mock()
        self.provenTimeSeriesDataManager = TimeseriesDataManager()  # Mock()
        self.client = Mock()
        self.arg_captor = ""
        self.arg_captor_log_message = ""
        self.configManager =ConfigurationManager()
        # self.log = Mock()
        # self.app_manager = Mock()
        # self.client_factory = Mock()
        # self.configuration_manager = Mock()
        # self.simulation_manager = Mock()
        # self.log_manager = Mock()
        # self.provenTimeSeriesDataManager = Mock()
        # self.client = Mock()
        # self.config_manager = Mock()
        # self.testConfig = Mock()
    def info_called_when_pm_started(self):
        """
        Succeeds when info log message is called at the start of the test manager implementation with the expected message
        :return:
        """

        #     ArgumentCaptor<String> argCaptor = ArgumentCaptor.forClass(String.class);
        try:
            self.client = Mockito.when(self.clientFactory.create(Mockito.any(),  Mockito.any()))
        except Exception as e:
            print(e)
        compareResults = CompareResults(self.clientFactory, self.logManager)
        compareResults.start()
        Mockito.verify(self.logManager).log(self.arg_captor_log_message.capture())
        self.logMessage = self.arg_captor.LogMessage.getAllValues().get(0);
        assert self.logMessage.getLog_level() == logging.DEBUG
        assert self.logMessage.getLog_message() == "Starting "+ self.tm.getName()
        assert self.logMessage.getProcess_status() == ProcessStatus.RUNNING
        assert self.logMessage.getTimestamp() is not None

    def test_get_feeder(self):
        #     /**
        #      * Trying to get closer to actual output 10/31/2017
        #      */
        with patch('os.path.isfile', return_value=True):
            with patch('builtins.open', return_value=open('test', 'r')):
                compare_results = CompareResults(self.logManager)
                feeder = compare_results.get_feeder()
                self.assertEqual(feeder, "ieee8500")

    def test_compare_str_errors(self):
        str_out = '''
        { "output": {
                "ieee8500": {
                    "cap_capbank0a": {
                        "capacitor_A": 400000.0,
                        "control": "MANUAL",
                        "control_level": "BANK",
                        "dwell_time": 100.0,
                        "phases": "AN",
                        "phases_connected": "NA",
                        "pt_phase": "A",
                        "switchA": "CLOSED"
                    },
                    "cap_capbank0b": {
                        "capacitor_B": 400000.0,
                        "control": "MANUAL",
                        "control_level": "BANK",
                        "dwell_time": 101.0,
                        "phases": "BN",
                        "phases_connected": "NB",
                        "pt_phase": "B",
                        "switchB": "CLOSED"
                    },
                    "cap_capbank0c": {
                        "capacitor_C": 400000.0,
                        "control": "MANUAL",
                        "control_level": "BANK",
                        "dwell_time": 102.0,
                        "phases": "CN",
                        "phases_connected": "NC",
                        "pt_phase": "C",
                        "switchC": "CLOSED"
                    },
                    "cap_capbank1a": {
                        "capacitor_A": 300000.0,
                        "control": "MANUAL",
                        "control_level": "BANK",
                        "dwell_time": 100.0,
                        "phases": "AN",
                        "phases_connected": "NA",
                        "pt_phase": "A",
                        "switchA": "CLOSED"
                    },
                    "cap_capbank1b": {
                        "capacitor_B": 300000.0,
                        "control": "MANUAL",
                        "control_level": "BANK",
                        "dwell_time": 101.0,
                        "phases": "BN",
                        "phases_connected": "NB",
                        "pt_phase": "B",
                        "switchB": "CLOSED"
                    },
                    "cap_capbank1c": {
                        "capacitor_C": 300000.0,
                        "control": "MANUAL",
                        "control_level": "BANK",
                        "dwell_time": 102.0,
                        "phases": "CN",
                        "phases_connected": "NC",
                        "pt_phase": "C",
                        "switchC": "CLOSED"
                    },
                    "cap_capbank2a": {
                        "capacitor_A": 300000.0,
                        "control": "MANUAL",
                        "control_level": "BANK",
                        "dwell_time": 100.0,
                        "phases": "AN",
                        "phases_connected": "NA",
                        "pt_phase": "A",
                        "switchA": "CLOSED"
                    },
                    "cap_capbank2b": {
                        "capacitor_B": 300000.0,
                        "control": "MANUAL",
                        "control_level": "BANK",
                        "dwell_time": 101.0,
                        "phases": "BN",
                        "phases_connected": "NB",
                        "pt_phase": "B",
                        "switchB": "CLOSED"
                    },
                    "cap_capbank2c": {
                        "capacitor_C": 300000.0,
                        "control": "MANUAL",
                        "control_level": "BANK",
                        "dwell_time": 102.0,
                        "phases": "CN",
                        "phases_connected": "NC",
                        "pt_phase": "C",
                        "switchC": "CLOSED"
                    },
                    "cap_capbank3": {
                        "capacitor_A": 300000.0,
                        "capacitor_B": 300000.0,
                        "capacitor_C": 300000.0,
                        "control": "MANUAL",
                        "control_level": "INDIVIDUAL",
                        "dwell_time": 0.0,
                        "phases": "ABCN",
                        "phases_connected": "NCBA",
                        "pt_phase": "",
                        "switchA": "CLOSED",
                        "switchB": "CLOSED",
                        "switchC": "CLOSED"
                    },
                    "nd_190-7361": {
                        "voltage_A": "6410.387412-4584.456974j V",
                        "voltage_B": "-7198.592139-3270.308373j V",
                        "voltage_C": "642.547265+7539.531175j V"
                    },
                    "nd_190-8581": {
                        "voltage_A": "6485.244723-4692.686497j V",
                        "voltage_B": "-7183.641236-3170.693325j V",
                        "voltage_C": "544.875721+7443.341013j V"
                    },
                    "nd_190-8593": {
                        "voltage_A": "6723.279163-5056.725836j V",
                        "voltage_B": "-7494.205738-3101.034603j V",
                        "voltage_C": "630.475858+7534.534976j V"
                    },
                    "nd__hvmv_sub_lsb": {
                        "voltage_A": "6261.474438-3926.148203j V",
                        "voltage_B": "-6529.409296-3466.545236j V",
                        "voltage_C": "247.131623+7348.295282j V"
                    },
                    "nd_l2673313": {
                        "voltage_A": "6569.522313-5003.052614j V",
                        "voltage_B": "-7431.486583-3004.840141j V",
                        "voltage_C": "644.553332+7464.115913j V"
                    },
                    "nd_l2876814": {
                        "voltage_A": "6593.064916-5014.031802j V",
                        "voltage_B": "-7430.572725-3003.995539j V",
                        "voltage_C": "643.473398+7483.558764j V"
                    },
                    "nd_l2955047": {
                        "voltage_A": "5850.305847-4217.166594j V",
                        "voltage_B": "-6729.652722-2987.617377j V",
                        "voltage_C": "535.302084+7395.127354j V"
                    },
                    "nd_l3160107": {
                        "voltage_A": "5954.507575-4227.423005j V",
                        "voltage_B": "-6662.357613-3055.346880j V",
                        "voltage_C": "600.213658+7317.832959j V"
                    },
                    "nd_l3254238": {
                        "voltage_A": "6271.490549-4631.254028j V",
                        "voltage_B": "-7169.987847-3099.952684j V",
                        "voltage_C": "751.609656+7519.062259j V"
                    },
                    "nd_m1047574": {
                        "voltage_A": "6306.632407-4741.568925j V",
                        "voltage_B": "-7214.626338-2987.055915j V",
                        "voltage_C": "622.058712+7442.125123j V"
                    },
                    "rcon_FEEDER_REG": {
                        "Control": "MANUAL",
                        "PT_phase": "CBA",
                        "band_center": 126.5,
                        "band_width": 2.0,
                        "connect_type": "WYE_WYE",
                        "control_level": "INDIVIDUAL",
                        "dwell_time": 15.0,
                        "lower_taps": 16,
                        "raise_taps": 16,
                        "regulation": 0.1
                    },
                    "rcon_VREG2": {
                        "Control": "MANUAL",
                        "PT_phase": "CBA",
                        "band_center": 125.0,
                        "band_width": 2.0,
                        "connect_type": "WYE_WYE",
                        "control_level": "INDIVIDUAL",
                        "dwell_time": 15.0,
                        "lower_taps": 16,
                        "raise_taps": 16,
                        "regulation": 0.1
                    },
                    "rcon_VREG3": {
                        "Control": "MANUAL",
                        "PT_phase": "CBA",
                        "band_center": 125.0,
                        "band_width": 2.0,
                        "connect_type": "WYE_WYE",
                        "control_level": "INDIVIDUAL",
                        "dwell_time": 15.0,
                        "lower_taps": 16,
                        "raise_taps": 16,
                        "regulation": 0.1
                    },
                    "rcon_VREG4": {
                        "Control": "MANUAL",
                        "PT_phase": "CBA",
                        "band_center": 125.0,
                        "band_width": 2.0,
                        "connect_type": "WYE_WYE",
                        "control_level": "INDIVIDUAL",
                        "dwell_time": 15.0,
                        "lower_taps": 16,
                        "raise_taps": 16,
                        "regulation": 0.1
                    },
                    "reg_FEEDER_REG": {
                        "configuration": "rcon_FEEDER_REG",
                        "phases": "ABC",
                        "tap_A": 2,
                        "tap_B": 2,
                        "tap_C": 1,
                        "to": "nd__hvmv_sub_lsb"
                    },
                    "reg_VREG2": {
                        "configuration": "rcon_VREG2",
                        "phases": "ABC",
                        "tap_A": 10,
                        "tap_B": 6,
                        "tap_C": 2,
                        "to": "nd_190-8593"
                    },
                    "reg_VREG3": {
                        "configuration": "rcon_VREG3",
                        "phases": "ABC",
                        "tap_A": 16,
                        "tap_B": 10,
                        "tap_C": 1,
                        "to": "nd_190-8581"
                    },
                    "reg_VREG4": {
                        "configuration": "rcon_VREG4",
                        "phases": "ABC",
                        "tap_A": 12,
                        "tap_B": 12,
                        "tap_C": 5,
                        "to": "nd_190-7361"
                    },
                    "xf_hvmv_sub": {
                        "power_in_A": "1739729.120858-774784.929430j VA",
                        "power_in_B": "1659762.622463-785218.730666j VA",
                        "power_in_C": "1709521.679515-849734.584043j VA"
                    }
                }
            },
            "command": "nextTimeStep"
        }
        '''
        compare_results = CompareResults(self.logManager)
        expectedOutputPath = "./json/expected_output.json"
        expected_output_map = compare_results.get_expected_output_map(expectedOutputPath)

        with patch('builtins.open', return_value=open(expectedOutputPath, 'r')):
            jsonObject = json.loads(str_out)
            count = compare_results.compare_expected_with_simulation(expected_output_map, jsonObject).get_number_of_conflicts()
            self.assertEqual(count, 50)

    # Add more test methods for other test cases...
    def test_compare_str(self):
        str_out = '{"output": {"ieee8500":{"cap_capbank0a":{"capacitor_A":400000.0,"control":"MANUAL","control_level":"BANK","dwell_time":100.0,"phases":"AN","phases_connected":"NA","pt_phase":"A","switchA":"OPEN"},"cap_capbank0b":{"capacitor_B":400000.0,"control":"MANUAL","control_level":"BANK","dwell_time":101.0,"phases":"BN","phases_connected":"NB","pt_phase":"B",'
        compare_results = CompareResults(self.logManager)
        expectedOutputPath = "./json/expected_output.json"
        expected_output_map = compare_results.get_expected_output_map(expectedOutputPath)

        with patch('builtins.open', return_value=open(expectedOutputPath, 'r')):
            jsonObject = json.loads(str_out)
            count = compare_results.compare_expected_with_simulation(expected_output_map, jsonObject).get_number_of_conflicts()
            self.assertEqual(count, 0)
            
    def test_compare_str_2(self):
        #         /**
        #          * Trying to get closer to actual output 10/31/2017
        #          */
        str_output = '{"output": {"ieee8500":{"cap_capbank0a":{"capacitor_A":400000.0,"control":"MANUAL","control_level":"BANK","dwell_time":100.0,"phases":"AN","phases_connected":"NA","pt_phase":"A","switchA":"OPEN"},"cap_capbank0b":{"capacitor_B":400000.0,"control":"MANUAL","control_level":"BANK","dwell_time":101.0,"phases":"BN","phases_connected":"NB","pt_phase":"B",'
        compare_results = CompareResults(self.logManager)
        path = "./json/sim_output_object.json"
        with open(path, 'r') as file:
            sim_output_object = json.load(file)
            expected_output_path = "./json/expected_output.json"
            expected_output_map = compare_results.get_expected_output_map(expected_output_path)

            count = compare_results.compare_expected_with_simulation_output(sim_output_object['output']['ieee8500'], expected_output_map).get_number_of_conflicts()
            self.assertEqual(count, 41)

    def test_compare(self):
        str_output = '{"output": {"ieee8500":{"cap_capbank0a":{"capacitor_A":400000.0,"control":"MANUAL","control_level":"BANK","dwell_time":100.0,"phases":"AN","phases_connected":"NA","pt_phase":"A","switchA":"OPEN"},"cap_capbank0b":{"capacitor_B":400000.0,"control":"MANUAL","control_level":"BANK","dwell_time":101.0,"phases":"BN","phases_connected":"NB","pt_phase":"B",'
        compare_results = CompareResults(self.logManager)
        #  path = "/Users/jsimpson/git/adms/GOSS-GridAPPS-D/gov.pnnl.goss.gridappsd/applications/python/sim_output_object.json";
        path = "./json/sim_output_object.json"
        with open(path, 'r') as file:
            sim_output_object = json.load(file)

            expected_output = "./json/expected_output.json"
            sim_output = "./json/sim_output.json"

            count = compare_results.compare_expected_with_simulation(sim_output, expected_output, sim_output_object['output']['ieee8500']).get_number_of_conflicts()
            self.assertEqual(count, 0)
    def test_compare_error_1(self):
        compare_results = CompareResults(self.logManager)
        path = "./json/sim_output_object.json"
        with open(path, 'r') as file:
            sim_output_object = json.load(file)

            expected_output = "./json/expected_output_error1.json"
            sim_output = "./json/sim_output.json"

            count = compare_results.compare_expected_with_simulation(sim_output, expected_output, sim_output_object['output']['ieee8500']).get_number_of_conflicts()
            self.assertEqual(count, 1)

    def test_compare_load_expected(self):
        #     /**
        #      * Test if expected output series is loaded
        #      */
        compare_results = CompareResults(self.client, self.testConfig)
        expected_output = "./json/expected_output_series.json"
        expected_output_map = compare_results.get_expected_output_map("0", expected_output)
        self.assertIsNotNone(expected_output_map)

    def test_script_prop(self):
        testManager = TestManagerImpl(self.appManager, self.clientFactory,                                              self.configurationManager, self.simulationManager,
                                      self.logManager, self.provenTimeSeriesDataManager)

        testScriptPath = "./applications/python/exampleTestScript.json"
        testScript = testManager.load_test_script(testScriptPath)
        self.assertEqual(testScript.name, "VVO")

        compare_results = CompareResults(self.clientFactory, self.logManager)
        path = "./json/sim_output_object.json"
        simOutProperties = compare_results.get_output_properties(path)

        propSet = compare_results.get_matched_properties(testScript, simOutProperties)
        self.assertIsNotNone(propSet)
        self.assertEqual(len(propSet), 25)

    def test_first_series_cim1(self):
        #     /**
        #      * Trying to get closer to actual output 10/31/2017
        #      */
        compare_results = CompareResults(self.client, self.testConfig)

        str_output = '''{
            "ieee8500": {
                "cap_capbank0a": {
                    "capacitor_A": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 100.0,
                    "phases": "AN",
                    "phases_connected": "NA",
                    "pt_phase": "A",
                    "switchA": "CLOSED"
                },
                "cap_capbank0b": {
                    "capacitor_B": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 101.0,
                    "phases": "BN",
                    "phases_connected": "NB",
                    "pt_phase": "B",
                    "switchB": "CLOSED"
                },
                "cap_capbank0c": {
                    "capacitor_C": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 102.0,
                    "phases": "CN",
                    "phases_connected": "NC",
                    "pt_phase": "C",
                    "switchC": "CLOSED"
                },
                "cap_capbank1a": {
                    "capacitor_A": 300000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 100.0,
                    "phases": "AN",
                    "phases_connected": "NA",
                    "pt_phase": "A",
                    "switchA": "CLOSED"
                },
                "cap_capbank1b": {
                    "capacitor_B": 300000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 101.0,
                    "phases": "BN",
                    "phases_connected": "NB",
                    "pt_phase": "B",
                    "switchB": "CLOSED"
                }
            }
        }'''

        simOutputObject = json.loads(str_output)

        expected_output = "./json/expected_output_series.json"
        expected_output = "./json/expected_result_series_CIM_Sample_filtered_2.json"

        count = compare_results.compare_expected_with_simulation_output("0", simOutputObject["ieee8500"], expected_output).get_number_of_conflicts()
        self.assertEqual(count, 0)

    def test_first_series1(self):
        #     /**
        #      * Trying to get closer to actual output 10/31/2017
        #      */
        compare_results = CompareResults(self.logManager)

        simOutputObject = json.loads(str_output_1)

        path = "./json/sim_output_object.json"  # Replace with your actual path
        simOutProperties = compare_results.get_output_properties(path)

        self.assertIsNotNone(simOutProperties)
        # Call your get_prop method or other relevant functions here
        # Call your compareExpectedWithSimulationOutput method here if needed
        #         getProp(simOutProperties);
        #
        expected_output = "./json/expected_output_series.json"  # Replace with your actual path

        #         String expected_output = "./json/expected_output_series.json";
        # //        int count = compareResults.compareExpectedWithSimulationOutput("0",simOutputObject.getAsJsonObject(),expected_output).getNumberOfConflicts();
        # //        assertEquals(count, 41);


    def test_first_series2(self):
        #     /**
        #      * Trying to get closer to actual output 10/31/2017
        #      */
        compare_results = CompareResults(self.logManager)
        compare_results.get_feeder()

        str_output = '''{
            "ieee8500": {
                "cap_capbank0a": {
                    "capacitor_A": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 100.0,
                    "phases": "AN",
                    "phases_connected": "NA",
                    "pt_phase": "A",
                    "switchA": "CLOSED"
                },
                "cap_capbank0b": {
                    "capacitor_B": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 101.0,
                    "phases": "BN",
                    "phases_connected": "NB",
                    "pt_phase": "B",
                    "switchB": "CLOSED"
                },
                "cap_capbank0c": {
                    "capacitor_C": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 102.0,
                    "phases": "CN",
                    "phases_connected": "NC",
                    "pt_phase": "C",
                    "switchC": "CLOSED"
                }
            }
        }'''

        simOutputObject = json.loads(str_output)

        path = "./json/sim_output_object.json"
        simOutProperties = compare_results.get_output_properties(path)

        self.assertIsNotNone(simOutProperties)

        # Uncomment the lines below and adjust them as needed for your specific comparison
        # count = compare_results.compare_expected_with_simulation_output("0", simOutputObject["ieee8500"], expected_output).get_number_of_conflicts()
        # self.assertEqual(count, 41)
        # //        int count = compareResults.compareExpectedWithSimulationOutput("0",simOutputObject.getAsJsonObject(),expected_output).getNumberOfConflicts();
        # //        assertEquals(count, 41);
        # //
        # //        int count2 = compareResults.compareExpectedWithSimulationOutput("0",simOutputObject.getAsJsonObject(),expected_output).getNumberOfConflicts();
        # //        assertEquals(count2, 41);

    def test_first_series3(self):
        #     /**
        #      * Test closer to full series
        #      */
        compare_results = CompareResults(self.logManager)
        compare_results.get_feeder()

        str_output = '''{
            "ieee8500": {
                "cap_capbank0a": {
                    "capacitor_A": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 100.0,
                    "phases": "AN",
                    "phases_connected": "NA",
                    "pt_phase": "A",
                    "switchA": "CLOSED"
                },
                "cap_capbank0b": {
                    "capacitor_B": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 101.0,
                    "phases": "BN",
                    "phases_connected": "NB",
                    "pt_phase": "B",
                    "switchB": "CLOSED"
                },
                "cap_capbank0c": {
                    "capacitor_C": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 102.0,
                    "phases": "CN",
                    "phases_connected": "NC",
                    "pt_phase": "C",
                    "switchC": "CLOSED"
                }
            }
        }'''

        simOutputObject = json.loads(str_output)

        # You need to define the expected_output variable as per your test requirements
        expected_output = "./json/expected_output_series3.json"

        # Uncomment the lines below and adjust them as needed for your specific comparison
        # TestResultSeries ts = TestResultSeries()
        # test_results = compare_results.compare_expected_with_simulation_output("0", simOutputObject["ieee8500"], expected_output)
        # self.assertEqual(test_results.get_number_of_conflicts(), 3)
        # ts.add("0", test_results)

        # test_results = compare_results.compare_expected_with_simulation_output("1", simOutputObject["ieee8500"], expected_output)
        # self.assertEqual(test_results.get_number_of_conflicts(), 3)
        # ts.add("1", test_results)

        # print(ts.get_total())

    def test_get_first(self):
            compare_results = CompareResults(self.clientFactory, self.logManager)
            str_output = '''
        {
            "ieee8500": {
                "cap_capbank0a": {
                    "capacitor_A": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 100.0,
                    "phases": "AN",
                    "phases_connected": "NA",
                    "pt_phase": "A",
                    "switchA": "CLOSED"
                },
                "cap_capbank0b": {
                    "capacitor_B": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 101.0,
                    "phases": "BN",
                    "phases_connected": "NB",
                    "pt_phase": "B",
                    "switchB": "CLOSED"
                },
                "cap_capbank0c": {
                    "capacitor_C": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 102.0,
                    "phases": "CN",
                    "phases_connected": "NC",
                    "pt_phase": "C",
                    "switchC": "CLOSED"
                }
            }
        }
        '''

            first_key = CompareResults.get_first_key(str_output)
            self.assertEqual(first_key, "ieee8500")


    def test_compare_angle(self):
        # //    Magnitude : if  difference <= 1e-3
        # //    Angle : if difference <= 0.1
        # //    If value == value
        compare_results = CompareResults(self.client, self.testConfig)
        object1 = {
            "angle": 22.0
        }
        object2 = {
            "angle": 22.099
        }
    
        self.assertTrue(compare_results.compare_object_properties(object1, object1, "angle"))
        self.assertTrue(compare_results.compare_object_properties(object1, object2, "angle"))
    
        object2["angle"] = 22.1
        self.assertTrue(compare_results.compare_object_properties(object1, object2, "angle"))
    
        object2["angle"] = 22.2
        self.assertFalse(compare_results.compare_object_properties(object1, object2, "angle"))


    def test_compare_magnitude(self):
        compare_results = CompareResults(self.client, self.testConfig)
        object1 = {
            "magnitude": 7402.0
        }
        object2 = {
            "magnitude": 7402.00099
        }
    
        self.assertTrue(compare_results.compare_object_properties(object1, object1, "magnitude"))
        self.assertTrue(compare_results.compare_object_properties(object1, object2, "magnitude"))
    
        object2["magnitude"] = 7402.001
        self.assertTrue(compare_results.compare_object_properties(object1, object2, "magnitude"))
    
        object2["magnitude"] = 7402.002
        self.assertFalse(compare_results.compare_object_properties(object1, object2, "magnitude"))


if __name__ == '__main__':
    # Usage
    str_output = '''
        {
            "ieee8500": {
                "cap_capbank0a": {
                    "capacitor_A": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 100.0,
                    "phases": "AN",
                    "phases_connected": "NA",
                    "pt_phase": "A",
                    "switchA": "CLOSED"
                },
                "cap_capbank0b": {
                    "capacitor_B": 400000.0,
                    "control": "MANUAL",
                    "control_level": "BANK",
                    "dwell_time": 101.0,
                    "phases": "BN",
                    "phases_connected": "NB",
                    "pt_phase": "B",
                    "switchB": "CLOSED"
                }
            }
        }
        '''

    compare_results = CompareResults(LogManager(__name__))
    first_key = compare_results.test_get_first(str_output)
    print("First Key:", first_key)

    object1 = {"angle": 22.0}
    object2 = {"angle": 22.099}
    print("Compare Angle:", compare_results.test_compare_angle(object1, object1))
    print("Compare Angle:", compare_results.test_compare_angle(object1, object2))

    object1 = {"magnitude": 7402.0}
    object2 = {"magnitude": 7402.00099}
    print("Compare Magnitude:", compare_results.test_compare_magnitude(object1, object1))
    print("Compare Magnitude:", compare_results.test_compare_magnitude(object1, object2))


    unittest.main()
