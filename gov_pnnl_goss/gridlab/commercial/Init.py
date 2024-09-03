from gov_pnnl_goss.gridlab.gldcore.Globals import EINVAL
from gov_pnnl_goss.gridlab.gldcore.GridLabD import set_callback
from gov_pnnl_goss.gridlab.gldcore.PropertyHeader import PropertyType


class Init:
    def __init__(self, fntable, module, argc, argv):
        self.fntable = fntable
        self.module = module
        self.argc = argc
        self.argv = argv


def do_kill():
    # if global memory needs to be released, this is a good time to do it
    return 0


def check():
    return 0


def office(module):
    pass


def multizone(module):
    pass


def gl_global_create(param, PT_bool, warn_control, param1):
    pass


def init(callbacks, module, argc, argv):
    if set_callback(callbacks) is None:
        errno = EINVAL
        return None
    
    gl_global_create("commercial::warn_control", PropertyType.PT_bool, office.warn_control, None)
    gl_global_create("commercial::warn_low_temp", PropertyType, office.warn_low_temp, None)
    gl_global_create("commercial::warn_high_temp", PropertyType, office.warn_high_temp, None)
    
    office(module)
    multizone(module)

    return office.oclass

