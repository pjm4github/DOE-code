from math import floor, ceil

from gov_pnnl_goss.gridlab.climate.CsvReader import PADDR
from gov_pnnl_goss.gridlab.gldcore.GldRandom import RandomType
from gov_pnnl_goss.gridlab.gldcore.Globals import PA_REFERENCE
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error, gl_register_class, gl_publish_variable, gl_warning, \
    gl_globalclock, PC_BOTTOMUP, TS_NEVER

from gov_pnnl_goss.gridlab.comm.NetworkMessage import NetworkMessage, MSGSTATE
from enum import Enum

from gov_pnnl_goss.gridlab.gldcore.PropertyHeader import PropertyType


class QUEUERESOLUTION(Enum):
    QR_REJECT = 0  # once bandwidth capacity is met, additional messages are rejected
    QR_QUEUE = 1   # once bandwidth capacity is met, edge routers buffer messages before transmitting across the network
    QR_SCALE = 2   # once bandwidth capacity is met, transmitters are scaled back so as to not exceed network capacity


# Future idea
class TXMODE(Enum):
    TXM_SIMPLE = 0  # data is sent and received as fast as it can be
    TXM_BALANCE = 1 # the sender will not outpace the receiver


# Future idea
class MXMODE(Enum):
    MXM_FIFO = 0    # the messages are sent first-in first out and will block additional messages
    MXM_BALANCE = 1 # messages are sent at a rate proportional to the receiver's bandwidth
    MXM_CASCADE = 2 # messages are sent FIFO, but if Rx limits Tx, additional messages may try to be sent


def random_value(random_type, latency_arg1, latency_arg2):
    pass


class Network:
    def __init__(self, mod):
        self.bandwidth = 0.0  # maximum kbytes/sec that can be fed through the network
        self.bandwidth_scale = 0.0
        self.bandwidth_used = 0.0
        self.buffer_size = 0.0  # how many bytes can be stored 'in the network' when traffic exceeds network bandwidth
        self.buffer_used = 0.0  # how many bytes are stored by edge-routers before streaming across the network
        self.bytes_rejected = 0.0  # how much bandwidth was rejected by the network
        self.bytes_to_reject = 0.0
        self.first_if = None
        self.first_msg = None
        self.last_if = None
        self.last_msg = None
        self.latency = 0.0
        self.latency_arg1 = 0.0
        self.latency_arg2 = 0.0
        self.latency_last_update = 0
        self.latency_mode = ''
        self.latency_next_update = 0
        self.latency_period = 0.0
        self.next_event = 0
        self.owner_class = None
        self.queue_resolution = QUEUERESOLUTION.QR_REJECT # determines what the network does when the sum of the interface traffic wants to exceed the bandwidth
        self.random_type = RandomType  # You need to define RANDOMTYPE accordingly
        self.timeout = 0.0

        if self.owner_class is None:
            # register the class definition
            self.owner_class = gl_register_class(mod, "network", Network, PC_BOTTOMUP)
            if self.owner_class is None:
                raise ValueError("unable to register object class implemented by {}".format(__file__))
                # TROUBLESHOOT
                # The registration for the network class failed. This is usually caused
                # by a coding error in the core implementation of classes or the module implementation.
                # Please report this error to the developers.

            # publish the class properties
            if gl_publish_variable(self.owner_class,
                                   PropertyType.PT_double, "latency[s]", PADDR(self.latency),
                                   PropertyType.PT_char32, "latency_mode", PADDR(self.latency_mode),
                                   PropertyType.PT_double, "latency_period[s]", PADDR(self.latency_period),
                                   PropertyType.PT_double, "latency_arg1", PADDR(self.latency_arg1),
                                   PropertyType.PT_double, "latency_arg2", PADDR(self.latency_arg2),
                                   PropertyType.PT_double, "bandwidth[MB/s]", PADDR(self.bandwidth),
                                   PropertyType.PT_enumeration, "queue_resolution", PADDR(self.queue_resolution),
                                   PropertyType.PT_KEYWORD, "REJECT", QUEUERESOLUTION.QR_REJECT,
                                   PropertyType.PT_KEYWORD, "QUEUE", QUEUERESOLUTION.QR_QUEUE,
                                   PropertyType.PT_double, "buffer_size[MB]", PADDR(self.buffer_size),
                                   PropertyType.PT_double, "bandwidth_used[MB/s]", PADDR(self.bandwidth_used), PropertyType.PT_ACCESS,
                                   PA_REFERENCE,
                                   None) < 1:
                raise ValueError("unable to publish properties in {}".format(__file__))
                # TROUBLESHOOT
                # The registration for the network properties failed. This is usually caused
                # by a coding error in the core implementation of classes or the module implementation.
                # Please report this error to the developers.

    def create(self):
        self.random_type = RandomType.RT_INVALID
        return 1

    def update_latency(self):
        if self.random_type != RandomType.RT_INVALID:
            self.latency = random_value(self.random_type, self.latency_arg1, self.latency_arg2)
            self.latency_last_update = gl_globalclock()
            self.latency_next_update = gl_globalclock() + self.latency_period
        else:
            self.latency_next_update = "TS_NEVER"
        if self.latency < 0.0:
            gl_warning("random latency output of %f is reset to zero" % self.latency)

    # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 python
    def init(self, parent):
        hdr = self.OBJECTHDR()
        if self.latency_mode[0] != 0:
            self.random_type = self.gl_randomtype(self.latency_mode)
            if self.random_type == RandomType.RT_INVALID:
                self.GL_THROW("unrecognized random global_property_types '{}'".format(self.latency_mode))
        else:
            self.random_type = RandomType.RT_INVALID  # prevents update_latency from updating the value
        if self.latency_period < 0.0:
            gl_warning("negative latency_period was reset to zero")
            self.latency_period = 0.0
        if self.bandwidth <= 0.0:
            gl_error("non-positive bandwidth")
            return 0
        if self.queue_resolution == QUEUERESOLUTION.QR_QUEUE:
            if self.buffer_size <= 0.0:
                gl_error("non-positive buffer_size when using buffered queue_resolution")
        elif self.queue_resolution == QUEUERESOLUTION.QR_REJECT:
            pass  # requires no checks
        else:
            gl_error("unrecognized queue_resolution, defaulting to QR_REJECT")
            self.queue_resolution = QUEUERESOLUTION.QR_REJECT
        if self.timeout < 0.0:
            gl_warning("negative timeout was reset to zero")
            self.timeout = 0.0
        self.bandwidth_used = 0.0
        self.update_latency()
        self.latency_last_update = gl_globalclock()
        self.next_event = TS_NEVER
        return 1

    def isa(self, classname):
        return classname == "network"

    def sync(self, t0, t1):
        obj = self.objecthdr
        if self.latency_last_update + self.latency_period <= t1:
            self.update_latency()
        if (self.latency_period <= 0.001) or (self.next_event != TS_NEVER and
                                              self.next_event < self.latency_next_update):
            return self.next_event
        else:
            return self.latency_next_update

    def attach(self, nif):
        if nif is None:
            return 0
        if self.first_if is None:
            self.first_if = nif
            self.last_if = nif
            nif.next = None
        else:
            self.last_if.next = nif
            self.last_if = nif
            nif.next = None
        return 1

    def commit(self, t1, t2):
        obj = self  # In Python, 'self' refers to the current object
        t0 = self.clock
        net_bw = 0.0
        nif_bw = 0.0
        net_bw_used = 0.0
        netmsg = None

        # Prompt interfaces to check for data to send
        nif = self.first_if
        while nif:
            nif.check_buffer()
            nif = nif.next

        # Since we can't sync, calculate actual exchanges here
        nif = self.first_if
        while nif:
            if nif.has_outbound():
                netmsg = nif.peek_outbox()
                while netmsg:
                    self.dt = float(gl_globalclock() - netmsg.last_update)
                    netmsg.bytes_sent += netmsg.send_rate * self.dt
                    netmsg.bytes_buffered += netmsg.buffer_rate * self.dt
                    netmsg.bytes_recv += netmsg.send_rate * self.dt
                    netmsg.last_update = gl_globalclock()
                    netmsg = netmsg.next
            nif = nif.next

        # Scan interfaces for messages, determine network bandwidth requirements
        nif = self.first_if
        while nif:
            nif_bw = 0.0
            nif.bandwidth_used = 0.0
            nif.send_rate_used = 0
            if nif.has_outbound():
                netmsg = nif.peek_outbox()
                while netmsg:
                    if nif_bw + netmsg.size - netmsg.bytes_sent > nif.send_rate:
                        nif_bw = nif.send_rate
                        break
                    else:
                        nif_bw += netmsg.size - netmsg.bytes_sent
                    netmsg = netmsg.next
                net_bw += nif_bw
            nif = nif.next

        # "Send" data
        self.bandwidth_used = 0
        nif = self.first_if
        while nif:
            if nif.has_outbound():
                nif.bandwidth_used = 0
                netmsg = nif.peek_outbox()
                while netmsg:
                    netmsg.send_rate = 0.0
                    netmsg.buffer_rate = 0.0
                    if self.queue_resolution == QUEUERESOLUTION.QR_REJECT:
                        if self.bandwidth - self.bandwidth_used > nif.send_rate - nif.send_rate_used:
                            netmsg.send_rate = nif.send_rate - nif.send_rate_used
                            netmsg.msg_state = MSGSTATE.NMS_SENDING
                        else:
                            if self.bandwidth == net_bw_used:
                                netmsg.send_rate = 0
                                if netmsg.bytes_sent > 0:
                                    netmsg.msg_state = MSGSTATE.NMS_DELAYED
                                else:
                                    netmsg.msg_state = MSGSTATE.NMS_REJECTED
                            else:
                                netmsg.send_rate = self.bandwidth - self.bandwidth_used
                                netmsg.msg_state = MSGSTATE.NMS_SENDING
                    elif self.queue_resolution == QUEUERESOLUTION.QR_QUEUE:
                        if self.bandwidth - self.bandwidth_used > nif.send_rate - nif.send_rate_used:
                            netmsg.send_rate = nif.send_rate - nif.send_rate_used
                            netmsg.msg_state = MSGSTATE.NMS_SENDING
                        else:
                            if self.bandwidth == self.bandwidth_used and self.buffer_size == self.buffer_used:
                                netmsg.send_rate = 0
                                if netmsg.bytes_sent > 0:
                                    netmsg.msg_state = MSGSTATE.NMS_DELAYED
                                else:
                                    netmsg.msg_state = MSGSTATE.NMS_REJECTED
                            else:
                                netmsg.send_rate = self.bandwidth - self.bandwidth_used
                                netmsg.buffer_rate = nif.send_rate - nif.send_rate_used - netmsg.send_rate
                                netmsg.msg_state = MSGSTATE.NMS_SENDING
                    elif self.queue_resolution == QUEUERESOLUTION.QR_SCALE:
                        raise Exception("Communication network does not yet support interface transmission scaling")
                    else:
                        raise Exception("Unrecognized communication resolution mode")
                    rmn = netmsg.size - netmsg.bytes_sent
                    if rmn < netmsg.send_rate + netmsg.buffer_rate:
                        if rmn < netmsg.send_rate:
                            netmsg.send_rate = rmn
                            netmsg.buffer_rate = 0.0
                        else:
                            netmsg.buffer_rate = rmn - netmsg.send_rate
                    nif.bandwidth_used += netmsg.send_rate
                    nif.bandwidth_used += netmsg.buffer_rate
                    self.bandwidth_used += netmsg.send_rate
                    self.buffer_used += netmsg.buffer_rate
                    netmsg = netmsg.next
            nif = nif.next

        # If there's additional bandwidth, use it to unload the buffer back into the network
        if self.bandwidth_used < self.bandwidth:
            self.bandwidth_left = self.bandwidth - self.bandwidth_used
            if self.buffer_used > 0:
                nif = self.first_if
                while nif and self.bandwidth_left > 0.0:
                    if nif.has_outbound():
                        netmsg = nif.peek_outbox()
                        while netmsg and netmsg.bytes_buffered > 0.0:
                            dt = float(netmsg.last_update - gl_globalclock())
                            if netmsg.bytes_buffered > self.bandwidth_left:
                                netmsg.buffer_rate = -self.bandwidth_left
                            else:
                                netmsg.buffer_rate = -netmsg.bytes_buffered
                            netmsg.bytes_buffered += netmsg.buffer_rate * dt
                            netmsg.bytes_recv -= netmsg.buffer_rate * dt
                            self.bandwidth_left += netmsg.bytes_buffered
                            self.bandwidth_used -= netmsg.buffer_rate
                            netmsg.send_rate -= netmsg.buffer_rate
                            netmsg = netmsg.next
                    nif = nif.next

        # "Receive" the messages
        tempmsg = NetworkMessage()
        rv = TS_NEVER
        predicted_tx_sec = 0.0
        next_tx_sec = 0
        nif = self.first_if
        while nif:
            if nif.has_outbound():
                netmsg = nif.peek_outbox()
                while netmsg:
                    if netmsg.bytes_recv >= netmsg.size:
                        tempmsg.next = netmsg.next
                        netmsg.msg_state = MSGSTATE.NMS_DELIVERED
                        netmsg.rx_done_sec = gl_globalclock() + int(ceil(self.latency))
                        netmsg.end_time = gl_globalclock() + int(ceil(self.latency))
                        if netmsg.end_time < rv:
                            rv = netmsg.end_time
                        if netmsg.prev:
                            netmsg.prev.next = netmsg.next
                        if tempmsg.next:
                            tempmsg.next.prev = netmsg.prev
                        if nif.outbox == netmsg:
                            nif.outbox = tempmsg.next
                        netmsg.next = netmsg.pTo.inbox
                        if netmsg.next:
                            netmsg.next.prev = netmsg
                        netmsg.pTo.inbox = netmsg
                        netmsg = tempmsg
                    else:
                        if netmsg.send_rate > 0.0:
                            predicted_tx_sec = (netmsg.size - netmsg.bytes_recv) / netmsg.send_rate
                            if predicted_tx_sec < 1.0:
                                next_tx_sec = gl_globalclock() + 1
                            else:
                                next_tx_sec = int(floor(predicted_tx_sec)) + gl_globalclock()
                            if next_tx_sec < rv:
                                rv = next_tx_sec
                    netmsg = netmsg.next
            nif = nif.next

        # Moved to nif.presync()
        return rv

    def notify(self, update_mode, prop):
        obj = self._objecthdr
        return 1

# //////////////////////////////////////////////////////////////////////////
# // IMPLEMENTATION OF CORE LINKAGE
# //////////////////////////////////////////////////////////////////////////

def create_network(obj, parent):
    obj = obj.create_object(Network)
    if obj:
        my = obj.get_data(Network)
        obj = obj.set_parent(obj, parent)
        try:
            my.create()
        except Exception as msg:
            gl_error("%s::%s.create(OBJECT *self={name='%s', id=%d},...): %s" % (obj.owner_class.module.name, obj.owner_class.name, obj.name, obj.id, msg))
            return 0, obj
        return 1, obj
    return 0, obj


def init_network(obj):
    my = obj.get_data(Network)
    try:
        return my.init(obj.parent)
    except Exception as msg:
        gl_error("%s::%s.init(OBJECT *self={name='%s', id=%d}): %s" % (obj.owner_class.module.name, obj.owner_class.name, obj.name, obj.id, msg))
        return 0


def isa_network(obj, class_name):
    if obj != 0 and class_name != 0:
        return obj.get_data(Network).isa(class_name)
    else:
        return 0

def global_time(t1):
    pass

def str_time(dt):
    pass

def sync_network(obj, t1):
    my = obj.get_data(Network)
    try:
        t2 = my.sync(obj.exec_clock, t1)
        return t2
    except Exception as msg:
        dt = global_time(t1)
        ts = str_time(dt)
        gl_error("%s::%s.init(OBJECT *self={name='%s', id=%d},TIMESTAMP t1='%s'): %s" % (obj.owner_class.module.name, obj.owner_class.name, obj.name, obj.id, ts, msg))
        return 0


def commit_network(obj, t1, t2):
    my = obj.get_data(Network)
    rv = my.commit(t1, t2)
    obj.exec_clock = gl_globalclock()
    return rv
#
# def initialize_network_properties(owner_class, mod, latency, latency_mode, latency_period, latency_arg1, latency_arg2, bandwidth, queue_resolution, buffer_size, bandwidth_used):
#     if owner_class is None:
#         # Register the class definition
#         owner_class = gl_register_class(mod, "network", sizeof(network), PC_BOTTOMUP)
#         if owner_class is None:
#             raise BlockingIOError("unable to register object class implemented by %s" % __FILE__)
#             # TROUBLESHOOT
#             # The registration for the network class failed.   This is usually caused
#             # by a coding error in the core implementation of classes or the module implementation.
#             # Please report this error to the developers.
#
#         # Publish the class properties
#         if gl_publish_variable(
#             owner_class,
#             PropertyType.PT_double, "latency[s]", PADDR(latency),
#             PropertyType.PT_char32, "latency_mode", PADDR(latency_mode),
#             PropertyType.PT_double, "latency_period[s]", PADDR(latency_period),
#             PropertyType.PT_double, "latency_arg1", PADDR(latency_arg1),
#             PropertyType.PT_double, "latency_arg2", PADDR(latency_arg2),
#             PropertyType.PT_double, "bandwidth[MB/s]", PADDR(bandwidth),
#             PropertyType.PT_enumeration, "queue_resolution", PADDR(queue_resolution),
#             PropertyType.PT_KEYWORD, "REJECT", QUEUERESOLUTION.QR_REJECT,
#             PropertyType.PT_KEYWORD, "QUEUE", QUEUERESOLUTION.QR_QUEUE,
#             PropertyType.PT_double, "buffer_size[MB]", PADDR(buffer_size),
#             PropertyType.PT_double, "bandwidth_used[MB/s]", PADDR(bandwidth_used),
#             PropertyType.PT_ACCESS, PA_REFERENCE,
#             NULL
#         ) < 1:
#             GL_THROW("unable to publish properties in %s" % __FILE__)
#             # TROUBLESHOOT
#             # The registration for the network properties failed.   This is usually caused
#             # by a coding error in the core implementation of classes or the module implementation.
#             # Please report this error to the developers.
#
#
# # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 python
# def defaults_network(self, mod):
#     if self.owner_class is None:
#         # register the class definition
#         self.owner_class = gl_register_class(mod, "network", network, PC_BOTTOMUP)
#         if self.owner_class is None:
#             raise ValueError("unable to register object class implemented by {}".format(__file__))
#             # TROUBLESHOOT
#             # The registration for the network class failed. This is usually caused
#             # by a coding error in the core implementation of classes or the module implementation.
#             # Please report this error to the developers.
#
#         # publish the class properties
#         if gl_publish_variable(self.owner_class,
#             PropertyType.PT_double, "latency[s]", PADDR(self.latency),
#             PropertyType.PT_char32, "latency_mode", PADDR(self.latency_mode),
#             PropertyType.PT_double, "latency_period[s]", PADDR(self.latency_period),
#             PropertyType.PT_double, "latency_arg1", PADDR(self.latency_arg1),
#             PropertyType.PT_double, "latency_arg2", PADDR(self.latency_arg2),
#             PropertyType.PT_double, "bandwidth[MB/s]", PADDR(self.bandwidth),
#             PropertyType.PT_enumeration, "queue_resolution", PADDR(self.queue_resolution),
#                 PropertyType.PT_KEYWORD, "REJECT", QUEUERESOLUTION.QR_REJECT,
#                 PropertyType.PT_KEYWORD, "QUEUE", QUEUERESOLUTION.QR_QUEUE,
#             PropertyType.PT_double, "buffer_size[MB]", PADDR(self.buffer_size),
#             PropertyType.PT_double, "bandwidth_used[MB/s]", PADDR(self.bandwidth_used), PropertyType.PT_ACCESS, PA_REFERENCE,
#             NULL) < 1:
#             raise ValueError("unable to publish properties in {}".format(__file__))
#             # TROUBLESHOOT
#             # The registration for the network properties failed. This is usually caused
#             # by a coding error in the core implementation of classes or the module implementation.
#             # Please report this error to the developers.
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 





