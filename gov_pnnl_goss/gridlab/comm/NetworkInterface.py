import time
from enum import Enum

from gov_pnnl_goss.gridlab.climate.Climate import OBJECTDATA
from gov_pnnl_goss.gridlab.climate.CsvReader import PADDR
from gov_pnnl_goss.gridlab.comm.MpiNetwork import gl_set_parent
from gov_pnnl_goss.gridlab.comm.Network import Network
from gov_pnnl_goss.gridlab.comm.NetworkMessage import NetworkMessage
from gov_pnnl_goss.gridlab.gldcore.Globals import PA_REFERENCE
from gov_pnnl_goss.gridlab.gldcore.GridLabD import TS_NEVER, gl_create_object, gl_error, PC_BOTTOMUP, PC_POSTTOPDOWN, \
    PC_PRETOPDOWN, gl_localtime, gl_register_class, gl_publish_variable, gl_globalclock
from gov_pnnl_goss.gridlab.gldcore.Property import PROPERTYTYPE


class DXM(Enum):
    DXM_FULL_DUPLEX = 1
    DXM_HALF_DUPLEX = 2
    DXM_XMIT_ONLY = 3
    DXM_RECV_ONLY = 4

class NSM(Enum):
    NSM_UPDATE = 1
    NSM_INTERVAL = 2
    NSM_UPDATE_PERIOD = 3

class NIS(Enum):
    NIS_NONE = 1
    NIS_QUEUED = 2
    NIS_REJECTED = 3
    NIS_SENDING = 4
    NIS_COMPLETE = 5
    NIS_FAILED = 6

class NetworkInterface:
    oclass = None

    def __init__(self, mod=None):
        if NetworkInterface.oclass is None:
            NetworkInterface.oclass = self.register_class(mod)

        self.bandwidth_used = 0.0
        self.bandwidth_used_MB_per_s = 0.0
        self.buffer_size = 0
        self.curr_buffer_size = -1
        self.data_buffer = [""] * 1024  # Initialize with 1024 empty strings
        self.destination = None
        self.duplex_mode = DXM.DXM_FULL_DUPLEX  # Initialize with an appropriate default value
        self.ignore_size = False
        self.inbox = None
        self.last_message_send_time = 0.0
        self.next = None
        self.next_msg_time = 0.0
        self.outbox = None
        self.pNetwork = None
        self.parent = None
        self.prev_buffer_size = 0
        self.prev_data_buffer = [""] * 1024  # Initialize with 1024 empty strings
        self.prop_str = ""
        self.recv_rate = 0.0
        self.recv_rate_MB_per_s = 0.0
        self.recv_rate_used = 0.0
        self.recv_rate_used_MB_per_s = 0.0
        self.send_message_mode = NSM.NSM_UPDATE # Initialize with an appropriate default value
        self.send_rate = 0.0
        self.send_rate_MB_per_s = 0.0
        self.send_rate_used = 0.0
        self.send_rate_used_MB_per_s = 0.0
        self.size = 0.0
        self.size_MB = 0.0
        self.status = NIS.NIS_NONE  # Initialize with an appropriate default value
        self.target = None
        self.to = None
        self.update_rate = 0
        self.write_msg = False

    def register_class(self, mod):
        self.oclass = {
            "name": "network_interface",
            "size": 0,
            "parent_class": PC_PRETOPDOWN | PC_BOTTOMUP | PC_POSTTOPDOWN
        }
        oclass = gl_register_class(mod)
        if oclass is None:
            gl_error("unable to register object class implemented by %s" % __name__)
        if gl_publish_variable(oclass,
            PROPERTYTYPE.PT_enumeration, "duplex_mode", PADDR("duplex_mode"),
                PROPERTYTYPE.PT_KEYWORD, "FULL_DUPLEX", DXM.DXM_FULL_DUPLEX,
                PROPERTYTYPE.PT_KEYWORD, "HALF_DUPLEX", DXM.DXM_HALF_DUPLEX,
                PROPERTYTYPE.PT_KEYWORD, "TRANSMIT_ONLY", DXM.DXM_XMIT_ONLY,
                PROPERTYTYPE.PT_KEYWORD, "RECEIVE_ONLY", DXM.DXM_RECV_ONLY,
            PROPERTYTYPE.PT_object, "to", PADDR("to"),
            PROPERTYTYPE.PT_object, "destination", PADDR("destination"),
            PROPERTYTYPE.PT_double, "size_MB", PADDR("size_MB"),
            PROPERTYTYPE.PT_double, "send_rate_MB_per_s", PADDR("send_rate_MB_per_s"),
            PROPERTYTYPE.PT_double, "recv_rate_MB_per_s", PADDR("recv_rate_MB_per_s"),
            PROPERTYTYPE.PT_int64, "update_rate", PADDR("update_rate"),
            PROPERTYTYPE.PT_enumeration, "status", PADDR("status"), PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
                PROPERTYTYPE.PT_KEYWORD, "NONE", NIS.NIS_NONE,
                PROPERTYTYPE.PT_KEYWORD, "QUEUED", NIS.NIS_QUEUED,
                PROPERTYTYPE.PT_KEYWORD, "REJECTED", NIS.NIS_REJECTED,
                PROPERTYTYPE.PT_KEYWORD, "SENDING", NIS.NIS_SENDING,
                PROPERTYTYPE.PT_KEYWORD, "COMPLETE", NIS.NIS_COMPLETE,
                PROPERTYTYPE.PT_KEYWORD, "FAILED", NIS.NIS_FAILED,
            PROPERTYTYPE.PT_double, "bandwidth_used_MB_per_s", PADDR("bandwidth_used_MB_per_s"), PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
            PROPERTYTYPE.PT_double, "send_rate_used_MB_per_s", PADDR("send_rate_used_MB_per_s"), PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
            PROPERTYTYPE.PT_double, "recv_rate_used_MB_per_s", PADDR("recv_rate_used_MB_per_s"), PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
            PROPERTYTYPE.PT_int32, "buffer_size", PADDR("buffer_size"),
            PROPERTYTYPE.PT_char1024, "buffer", PADDR("data_buffer"),
            PROPERTYTYPE.PT_char32, "property", PADDR("prop_str"), PROPERTYTYPE.PT_DESCRIPTION, "the name of the property to write incoming messages to",
            PROPERTYTYPE.PT_bool, "ignore_size", PADDR("ignore_size"), PROPERTYTYPE.PT_DESCRIPTION, "informs the model that the size of the target property may not represent the number of bytes available for writing",
            PROPERTYTYPE.PT_enumeration, "send_mode", PADDR("send_message_mode"), PROPERTYTYPE.PT_DESCRIPTION, "determines when the interface will write the data buffer into a message and send it",
                PROPERTYTYPE.PT_KEYWORD, "UPDATE", NSM.NSM_UPDATE,
                PROPERTYTYPE.PT_KEYWORD, "INTERVAL", NSM.NSM_INTERVAL,
                PROPERTYTYPE.PT_KEYWORD, "UPDATE_PERIOD", NSM.NSM_UPDATE_PERIOD,
            None) < 1:
            gl_error("unable to publish properties in %s" % __name__)
        return oclass

    def get_size(self):
        return self.curr_buffer_size

    def create(self):
        return 1

    def init(self, parent):
        if self.to is None:
            raise ValueError("Network interface is not connected to a network")

        if not isinstance(self.to, Network):
            raise ValueError("Network interface is connected to a non-network object")

        if self.send_rate <= 0.0:
            raise ValueError("Network interface has a non-positive send rate")

        if self.recv_rate <= 0.0:
            raise ValueError("Network interface has a non-positive recv rate")

        if not self.prop_str:
            raise ValueError("Network interface does not specify a data destination buffer")

        self.target = parent.get_property(self.prop_str)

        if self.target is None:
            raise ValueError(f"Network interface parent does not contain property '{self.prop_str}'")

        # Note that there is no type-checking on this; the target property can be of various types.
        # All the interface does is copy data to where it's told. Note that this is "dangerous."

        self.bandwidth_used = 0.0
        self.buffer_size = 1024 if self.ignore_size else self.target.width
        self.prev_buffer_size = self.buffer_size
        self.pNetwork = self.to

        if self.pNetwork:
            self.pNetwork.attach(self)

        return 1  # Success

    @staticmethod
    def isa(classname):
        return classname == "network_interface"

    def sync(self, t0, t1):
        # You can implement your synchronization logic here
        return TS_NEVER  # Return the appropriate value based on your implementation

    def presync(self, t0, t1):
        # You can implement your presynchronization logic here
        rv = TS_NEVER
        # if self.has_inbound():
        #     rv = self.handle_inbox(t1)
        return rv  # Return the appropriate value based on your implementation

    def postsync(self, t0, t1):
        # You can implement your postsynchronization logic here
        return TS_NEVER  # Return the appropriate value based on your implementation

    def commit(self, t1, t2):
        # /**
        #  * ni::commit() is where data is pulled from its parent, copied into the interface,
        #  *	and written to a message to be sent to another interface.
        #  */
        return 1

    # /*
    # //return my->notify(update_mode, prop);
    # int network_interface::notify(int update_mode, PROPERTY *prop){
    # 	OBJECT *self = OBJECTHDR(this);
    # 	if(update_mode == NM_POSTUPDATE){
    # 		if(strcmp(prop->name, "buffer") == 0){
    # 			// new data has been received
    # 			// NOTE: network should update 'buffer_size' before updating 'buffer'
    # 			// * lock parent's destination property
    # 			// * memcpy(pTarget, data_buffer, buffer_size)
    # 			// * memset(data_buffer, 0, buffer_size)
    # 			// * buffer_size = 0;
    # 			;
    # 		}
    # 	}
    # 	return 1;
    # }*/

    def on_message(self):
        # // there isn't a good way to set_value with straight binary data, so going about it using
        # //	direct sets, and 'notify'ing with a follow-up function call.
        return 0

    def check_buffer(self):
        write_msg = False
        obj = self

        # Calculate memory addresses
        b = self.target.addr
        c = (obj.parent + 1) if obj.parent else None
        d = c + b if c else None

        # Check if it's time for an update
        time_for_update = self.last_message_send_time + self.update_rate <= gl_globalclock()

        if self.duplex_mode == DXM.DXM_RECV_ONLY:
            return 1

        if (self.send_message_mode in [NSM.NSM_INTERVAL, NSM.NSM_UPDATE_PERIOD]) and time_for_update:
            write_msg = True
        elif self.send_message_mode in [NSM.NSM_UPDATE, NSM.NSM_UPDATE_PERIOD]:
            if self.curr_buffer_size == -1:
                write_msg = True
            else:
                if self.data_buffer == d[:self.buffer_size]:
                    write_msg = False
                else:
                    write_msg = True

        if write_msg:
            self.curr_buffer_size = self.buffer_size
            self.data_buffer = d[:self.buffer_size]

            nm = NetworkMessage()
            nm.send_message(self, gl_globalclock, self.pNetwork.latency)
            nm.next = self.outbox
            self.outbox = nm
            self.last_message_send_time = gl_globalclock

        return 1


    def handle_inbox(self, t1):

        # process the messages in the inbox, in FIFO fashion, even though it's been stacked up.
        rv = self.handle_inbox_recursive(t1, self.inbox)
        self.inbox = rv
        next_msg_time = TS_NEVER
        nm = self.inbox
        while nm:
            if nm.end_time < next_msg_time:
                next_msg_time = nm.end_time
            nm = nm.next
        return next_msg_time

    def handle_inbox_recursive(self, t1, nm):
        # /**
        #  *	nm		- the message being processed (can be null)
        #  *	return	- the next message in the stack that is not ready to be processed (punted for later)
        #  *
        #  *	handle_inbox recursively checks to see if a message in the inbox is ready to be received,
        #  *		based on its 'arrival time', a function of the transmission time and network latency.
        #  *		Although messages are arranged in a stack, the function traverses to the end of the
        #  *		stack and works its way back up, returning the new stack as it processes through
        #  *		the messages.  It is possible that not all the messages marked as 'delivered' are
        #  *		ready to be processed at this point in time.
        #  */
        my = self
        rv = None

        if nm is not None:  # Check if there are messages in the inbox
            rv = self.handle_inbox(t1, nm.next)

            if rv != nm.next:
                # del nm.next
                nm.next = rv

        if nm is None:
            return None

        if t1 >= nm.rx_done_sec:
            obj = nm.from_obj
            addr = obj.parent.get_address() + self.target.addr

            self.curr_buffer_size = nm.buffer_size
            self.data_buffer = nm.message[:nm.buffer_size]

            obj.parent.lock_object()
            obj.parent.set_value(self.data_buffer, addr, 0)
            obj.parent.unlock_object()

            return nm.next

        return nm

        # my = self
        # rv = None
        #
        # if self.inbox is not None:  # Check if there are messages in the inbox
        #     rv = self.handle_inbox(t1, self.inbox.next)
        #
        #     if rv != self.inbox.next:
        #         del self.inbox.next
        #         self.inbox.next = rv
        #
        # if self.inbox is None:
        #     return None
        #
        # if t1 >= self.inbox.rx_done_sec:
        #     self = self.inbox.from_obj
        #     addr = self.parent.get_address() + self.target.addr
        #
        #     self.curr_buffer_size = self.inbox.buffer_size
        #     self.data_buffer = self.inbox.message[:self.inbox.buffer_size]
        #
        #     self.parent.lock_object()
        #     self.parent.set_value(self.data_buffer, addr, 0)
        #     self.parent.unlock_object()
        #
        #     return self.inbox.next
        #
        # return self.inbox


def create_network_interface(obj, parent):
    obj[0] = gl_create_object(NetworkInterface.oclass)
    if obj[0] is not None:
        my = OBJECTDATA(obj[0], NetworkInterface)
        gl_set_parent(obj[0], parent)
        try:
            my.create()
        except Exception as e:
            gl_error(
                "%s::%s.create(OBJECT **self={name='%s', id=%d},...): %s" %
                (obj[0].oclass.module.name, obj[0].oclass.name, obj[0].name, obj[0].id, str(e))
            )
            return 0
        return 1
    return 0


def init_network_interface(obj):
    my = OBJECTDATA(obj, NetworkInterface)
    try:
        return my.init(obj.parent)
    except Exception as e:
        gl_error(
            "%s::%s.init(OBJECT *self={name='%s', id=%d}): %s" %
            (obj.oclass.module.name, obj.oclass.name, obj.name, obj.id, str(e))
        )
        return 0

def isa_network_interface(obj, classname):
    if obj is not None and classname is not None:
        return OBJECTDATA(obj, NetworkInterface).isa(classname)
    else:
        return False


def gl_strtime(dt, ts, param):
    pass



def sync_network_interface(obj, t1, pass_config):
    my = OBJECTDATA(obj, NetworkInterface)
    try:
        t2 = TS_NEVER
        if pass_config == PC_BOTTOMUP:
            t2 = my.sync(obj.clock, t1)
        elif pass_config == PC_POSTTOPDOWN:
            pass  # Add your PC_POSTTOPDOWN logic here
        elif pass_config == PC_PRETOPDOWN:
            t2 = my.presync(obj.clock, t1)
        obj.clock = t1
        return t2
    except Exception as e:
        dt = time.time_ns()
        ts = "TIMESTAMP t1='{0}'".format(obj.clock)
        gl_localtime(t1, dt)
        ts = gl_strtime(dt, ts, len(ts))
        gl_error("{0}::{1}.init(OBJECT **self={{name='{2}', id={3}}},{4}): {5}".format(obj.oclass.module.name, obj.oclass.name, obj.name, obj.id, ts, str(e)))
        return 0

def commit_network_interface(obj, t1, t2):
    my = OBJECTDATA(obj, NetworkInterface)
    try:
        return my.commit(t1, t2)
    except Exception as e:
        dt = time.time_ns()
        ts = "TIMESTAMP t1='{0}', t2='{1}'".format(t1, t2)
        gl_error("{0}::{1}.init(OBJECT *self={{name='{2}', id={3}}},{4}): {5}".format(obj.oclass.module.name, obj.oclass.name, obj.name, obj.id, ts, str(e)))
        return 0
