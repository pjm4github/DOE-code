from enum import Enum
from math import floor, fmod

from gov_pnnl_goss.gridlab.climate.Climate import OBJECTDATA
from gov_pnnl_goss.gridlab.climate.CsvReader import PADDR
from gov_pnnl_goss.gridlab.comm.MpiNetwork import gl_set_parent
from gov_pnnl_goss.gridlab.comm.NetworkInterface import NetworkInterface, DXM

from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_register_class, PC_BOTTOMUP, gl_publish_variable, gl_error, \
    gl_create_object, gl_object_isa, TS_NEVER, gl_name
from gov_pnnl_goss.gridlab.gldcore.Property import PROPERTYTYPE


class MSGSTATE(Enum):
    NMS_NONE = 0
    NMS_PENDING = 1
    NMS_SENDING = 2
    NMS_DELIVERED = 3
    NMS_REJECTED = 4
    NMS_FAILED = 5
    NMS_ERROR = 6
    NMS_DELAYED = 7
    NMS_TXRX = 8
    NMS_LATENT = 9


def OBJECTHDR(nif):
    pass



class NetworkMessage:
    oclass = None

    def __init__(self, mod=None):
        if NetworkMessage.oclass is None:
            NetworkMessage.oclass = self.register_class(mod)
        self.buffer_size = 0
        self.bytes_received_MB = 0.0
        self.bytes_resent_MB = 0.0
        self.bytes_sent_MB = 0.0
        self.end_time = -1
        self.end_time_frac_s = 0.0
        self.from_interface = None
        self.last_update = 0
        self.message = ""
        self.msg_state = MSGSTATE.NMS_NONE
        self.size_MB = 0.0
        self.start_time = -1
        self.start_time_frac_s = 0.0
        self.to_interface = None

    @staticmethod
    def register_class(mod):
        oclass = {
            "name": "network_message",
            "size": NetworkMessage.get_size(),
            "parent_class": PC_BOTTOMUP
        }
        oclass = gl_register_class(mod)
        if oclass is None:
            gl_error("unable to register object class implemented by %s" % __name__)
        if gl_publish_variable(oclass,
            PROPERTYTYPE.PT_object, "from_interface", PADDR("from_interface"),
            PROPERTYTYPE.PT_object, "to_interface", PADDR("to_interface"),
            PROPERTYTYPE.PT_double, "size_MB", PADDR("size_MB"),
            PROPERTYTYPE.PT_char1024, "message", PADDR("message"),
            PROPERTYTYPE.PT_int16, "buffer_size", PADDR("buffer_size"),
            PROPERTYTYPE.PT_int64, "start_time", PADDR("start_time"),
            PROPERTYTYPE.PT_int64, "end_time", PADDR("end_time"),
            PROPERTYTYPE.PT_double, "start_time_frac_s", PADDR("start_time_frac_s"),
            PROPERTYTYPE.PT_double, "end_time_frac_s", PADDR("end_time_frac_s"),
            PROPERTYTYPE.PT_double, "bytes_sent_MB", PADDR("bytes_sent_MB"),
            PROPERTYTYPE.PT_double, "bytes_resent_MB", PADDR("bytes_resent_MB"),
            PROPERTYTYPE.PT_double, "bytes_received_MB", PADDR("bytes_received_MB"),
            PROPERTYTYPE.PT_enumeration, "msg_state", PADDR("msg_state"),
                PROPERTYTYPE.PT_KEYWORD, "NONE", MSGSTATE.NMS_NONE,
                PROPERTYTYPE.PT_KEYWORD, "PENDING", MSGSTATE.NMS_PENDING,
                PROPERTYTYPE.PT_KEYWORD, "SENDING", MSGSTATE.NMS_SENDING,
                PROPERTYTYPE.PT_KEYWORD, "DELIVERED", MSGSTATE.NMS_DELIVERED,
                PROPERTYTYPE.PT_KEYWORD, "REJECTED", MSGSTATE.NMS_REJECTED,
                PROPERTYTYPE.PT_KEYWORD, "FAILED", MSGSTATE.NMS_FAILED,
                PROPERTYTYPE.PT_KEYWORD, "ERROR", MSGSTATE.NMS_ERROR,
                PROPERTYTYPE.PT_KEYWORD, "DELAYED", MSGSTATE.NMS_DELAYED,
            None) < 1:
            gl_error("unable to publish properties in %s" % __name__)
        return oclass

    @staticmethod
    def get_size():
        return 0

    # def send_message(self, nif, ts, latency):
    #     return self.send_message(OBJECTHDR(nif), nif.destination, nif.data_buffer, nif.buffer_size,
    #                               nif.size, ts, nif.bandwidth_used / nif.send_rate, latency)
    def send_message(self, f, t, m, len=None, sz=None, ts=None, frac=None, latency=None):
        f_tmp = f
        t_tmp = t
        m_tmp = m
        if len is None and  sz is None and ts is None and frac is None and latency is None:
            f = OBJECTHDR(f_tmp)
            t = f_tmp.destination
            m = f_tmp.data_buffer
            len = f_tmp.buffer_size
            sz = f_tmp.size
            ts = t_tmp
            frac = f_tmp.bandwidth_used / f_tmp.send_rate
            latency = m_tmp
        self.from_interface = f
        self.to_interface = t
        self.size_MB = sz
        self.buffer_size = len
        self.message = m
        # old
        self.start_time = ts
        self.start_time_frac_s = frac
        # new
        self.tx_start_sec = ts
        self.tx_start_frac_s = frac
        self.rx_start_sec = ts + floor(latency + frac)
        self.rx_start_frac_s = fmod(latency + frac, 1.0)
        # /new
        self.msg_state = MSGSTATE.NMS_NONE
        self.last_update = ts
        # validate to & from interfaces
        if self.from_interface is None:
            gl_error("send_message(): no 'from_interface' interface")
            self.msg_state = MSGSTATE.NMS_ERROR
            return 0
        elif gl_object_isa(self.from_interface, "network_interface"):
            pFrom = OBJECTDATA(self.from_interface, NetworkInterface)
            if pFrom.duplex_mode not in [DXM.DXM_FULL_DUPLEX, DXM.DXM_HALF_DUPLEX,
                                         DXM.DXM_XMIT_ONLY]:
                gl_error("send_message(): 'from_interface' interface '%s' not configured to send messages" %
                         gl_name(self.from_interface))
                self.msg_state = MSGSTATE.NMS_ERROR
                return 0
        else:
            gl_error("send_message(): 'from_interface' object is not a network_interface")
            self.msg_state = MSGSTATE.NMS_ERROR
            return 0

        if self.to_interface is None:
            gl_error("send_message(): no 'to_interface' interface")
            self.msg_state = MSGSTATE.NMS_ERROR
            return 0
        elif gl_object_isa(self.to_interface, "network_interface"):
            pTo = OBJECTDATA(self.to_interface, NetworkInterface)
            if pTo.duplex_mode not in [DXM.DXM_FULL_DUPLEX, DXM.DXM_HALF_DUPLEX,
                                       DXM.DXM_RECV_ONLY]:
                gl_error("send_message(): 'to_interface' interface '%s' not configured to receive messages" %
                         gl_name(self.to_interface))
                self.msg_state = MSGSTATE.NMS_ERROR
                return 0
        else:
            gl_error("send_message(): 'to_interface' object is not a network_interface")
            self.msg_state = MSGSTATE.NMS_ERROR
            return 0

        if sz < 0:
            gl_error("send_message(): size is negative")
            self.msg_state = MSGSTATE.NMS_ERROR
            return 0
        if len < 0:
            gl_error("send_message(): length is negative")
            self.msg_state = MSGSTATE.NMS_ERROR
            return 0
        if ts < 0:
            gl_error("send_message(): timestamp is nonsensical")
            self.msg_state = MSGSTATE.NMS_ERROR
            return 0
        if pTo.pNetwork != pFrom.pNetwork:
            gl_error("send_message(): network interfaces exist on different networks")
            self.msg_state = MSGSTATE.NMS_ERROR
            return 0
        return 1

    def create(self):
        gl_error("network_message is an internally used class and should not be instantiated by a model")
        return 0

    def isa(self, classname):
        return classname == "network_message"

    def notify(self, update_mode, prop):
        obj = OBJECTHDR(self)
        return 1
# //////////////////////////////////////////////////////////////////////////
# // IMPLEMENTATION OF CORE LINKAGE
# //////////////////////////////////////////////////////////////////////////

def create_network_message(obj, parent):
    obj = gl_create_object(NetworkMessage.oclass)
    if obj is not None:
        my = OBJECTDATA(obj, NetworkMessage)
        gl_set_parent(obj, parent)
        try:
            my.create()
        except Exception as e:
            gl_error("%s::%s.create(OBJECT **self={name='%s', id=%d},...): %s" % (
                obj.oclass.module.name, obj.oclass.name, obj.name, obj.id, str(e)))
            return 0
        return 1
    return 0

def sync_network_message(obj, t1, passconfig):
    obj.clock = t1
    return TS_NEVER

def isa_network_message(obj, classname):
    if obj is not None and classname is not None:
        return OBJECTDATA(obj, NetworkMessage).isa(classname)
    else:
        return 0

def notify_network_message(obj, update_mode, prop):
    my = OBJECTDATA(obj, NetworkMessage)
    return my.notify(update_mode, prop)
