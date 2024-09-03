

# network.py
import random
import time

from gov_pnnl_goss.gridlab.climate.Climate import OBJECTDATA
from gov_pnnl_goss.gridlab.climate.CsvReader import PADDR
from gov_pnnl_goss.gridlab.gldcore.Globals import PA_REFERENCE
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error, gl_publish_variable, gl_register_class, PC_BOTTOMUP, \
    gl_globalclock
from gov_pnnl_goss.gridlab.gldcore.PropertyHeader import PropertyType


def gl_set_parent(obj, parent):
    pass


def create_mpi_network(obj, parent):
    obj = MpiNetwork.owner_class()
    if obj is not None:
        my = obj
        gl_set_parent(obj, parent)
        try:
            my.create()
        except Exception as msg:
            error_msg = "({}): {}"
            print(error_msg.format(type(obj).__name__, msg))
            return 0
        return 1
    return 0

def init_mpi_network(obj):
    my = type(obj).__name__
    try:
        return my.init(obj.parent)
    except Exception as msg:
        error_msg = "({}): {}"
        print(error_msg.format(type(obj).__name__, msg))
        return 0

def isa_mpi_network(obj, classname):
    if obj and classname:
        return OBJECTDATA(obj, MpiNetwork).isa(classname)
    else:
        return 0

def sync_mpi_network(obj, t1):
    my = type(obj).__name__
    try:
        t2 = my.sync(obj.exec_clock, t1)
        return t2
    except Exception as msg:
        dt = time.localtime(t1)
        ts = time.strftime('%Y-%m-%d %H:%M:%S', dt)
        error_msg = "({}: {}) {}: {}"
        print(error_msg.format(obj.owner_class.module.name, obj.owner_class.name, obj.name, obj.id, ts, msg))
        return 0

def commit_mpi_network(obj, t1, t2):
    my = type(obj).__name__
    rv = my.commit(t1, t2)
    obj.exec_clock = gl_globalclock
    return rv

def notify_mpi_network(obj, update_mode, prop):
    my = type(obj).__name__
    return my.notify(update_mode, prop)


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def register_class_definition(owner_class, mod, class_name, size, policy):
    if owner_class is None:
        # register the class definition
        owner_class = gl_register_class(mod, class_name, size, policy)
        if owner_class is None:
            raise Exception("unable to register object class implemented by %s" % __file__)
            # TROUBLESHOOT
            # The registration for the class failed.   This is usually caused
            # by a coding error in the core implementation of classes or the module implementation.
            # Please report this error to the developers.

        # publish the class properties
        if gl_publish_variable(owner_class, PropertyType.PT_int64, "interval", PADDR(owner_class.interval), PropertyType.PT_int32, "mpi_target", PADDR(owner_class.mpi_target),
                               PropertyType.PT_int64, "reply_time", PADDR(owner_class.reply_time), PropertyType.PT_ACCESS, PA_REFERENCE, None) < 1:
            raise Exception("unable to publish properties in %s" % __file__)
            # TROUBLESHOOT
            # The registration for the network properties failed.   This is usually caused
            # by a coding error in the core implementation of classes or the module implementation.
            # Please report this error to the developers.


class MPI_Send:
    pass

MPI_LONG_LONG = 0

MPI_COMM_WORLD = 1


class MPI_Recv:
    pass


class MpiNetwork:
    owner_class = None

    def __init__(self, mod):

        self.interval = 0
        self.reply_time = 0
        self.mpi_target = 0

        self.last_time = 0
        self.next_time = 0
        self.their_time = 0

        if MpiNetwork.owner_class is None:
            MpiNetwork.owner_class = gl_register_class(mod, "mpi_network", MpiNetwork.__sizeof__(), PC_BOTTOMUP)
            if MpiNetwork.owner_class is None:
                raise Exception("unable to register object class implemented by {}".format(__name__))
                # TROUBLESHOOT
                # The registration for the mpi_network class failed. This is usually caused
                # by a coding error in the core implementation of classes or the module implementation.
                # Please report this error to the developers.

            if gl_publish_variable(MpiNetwork.owner_class,
                                   PropertyType.PT_int64, "interval", PADDR(MpiNetwork.interval),
                                   PropertyType.PT_int32, "mpi_target", PADDR(MpiNetwork.mpi_target),
                                   PropertyType.PT_int64, "reply_time", PADDR(MpiNetwork.reply_time),
                                   PropertyType.PT_ACCESS, PA_REFERENCE,
                                   None) < 1:
                raise Exception("unable to publish properties in {}".format(__name__))
                # TROUBLESHOOT
                # The registration for the network properties failed. This is usually caused
                # by a coding error in the core implementation of classes or the module implementation.
                # Please report this error to the developers.

    # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
    def create(self):
        self.mpi_target = 1
        self.interval = 60
        self.reply_time = self.last_time = self.next_time = self.their_time = 0
        return 1

    def init(self, parent):
        hdr = self.objecthdr()

        # input validation checks
        if self.mpi_target < 0:
            gl_error("mpi_network init(): target is negative")
            return 0
        if self.mpi_target == 0:
            gl_error("mpi_network init(): target is 0, which is assumed to be GridLAB-D")
            return 0

        if self.interval < 1:
            gl_error("mpi_network init(): interval is not greater than zero")
            return 0

        # success
        return 1

    def isa(self, classname):
        return classname == "mpi_network"

    def sync(self, t0, t1):
        obj = self._objecthdr
        status = None
        rv = 0

        if t0 == 0:
            self.last_time = self.next_time = t1

        if self.next_time >= t1:
            self.last_time = t1
            rv = MPI_Send(self.last_time, len(self.last_time), MPI_LONG_LONG,
                          self.mpi_target, 0, MPI_COMM_WORLD)
            self.next_time += self.interval

        if rv == 0:
            pass

        rv = MPI_Recv(self.their_time, len(self.their_time), MPI_LONG_LONG,
                      self.mpi_target, 0, MPI_COMM_WORLD, status)
        if rv == 0:
            pass

        if self.their_time != self.last_time:
            gl_error("mpi_network::sync(): epic fail due to mismatched timestamp")

        self.reply_time = self.their_time
        return self.next_time

    def commit(self, t1, t2):
        obj = self.objecthdr()
        t0 = obj.exec_clock
        return None

    def notify(self, update_mode, prop):
        obj = self.objecthdr
        return 1
