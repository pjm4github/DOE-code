from gov_pnnl_goss.gridlab.climate.Climate import OBJECTDATA
from gov_pnnl_goss.gridlab.comm.MpiNetwork import gl_set_parent
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_create_object

hvac_class = None
last_hvac = None


def create_hvac(obj, parent):
    obj.value = gl_create_object(hvac_class)
    if obj.value is not None:
        global last_hvac
        last_hvac = obj.value
        my = OBJECTDATA(obj.value, Hvac)
        gl_set_parent(obj.value, parent)
        my.create()
        return 1
    return 0


def sync_hvac(obj, t0):
    t1 = obj.hvac.sync(t0)
    obj.exec_clock = t0
    return t1


class Hvac:
    def __init__(self):
        pass
    
    def __del__(self):
        pass
    
    def create(self):
        pass

    def sync(self, t0):
        return 0  # Assuming TS_NEVER is defined as 0 in the C++ code

    def pre_update(self):
        pass
    
    def post_update(self):
        pass
    
    
