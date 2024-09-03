import sys

from gov_pnnl_goss.gridlab.climate.CsvReader import PADDR, gl_create_object
from gov_pnnl_goss.gridlab.comm.MpiNetwork import gl_set_parent
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_register_class, gl_publish_variable, TS_NEVER, gl_error, \
    gl_object_isa
from gov_pnnl_goss.gridlab.gldcore.PropertyHeader import PropertyType
from gridlab.gldcore.Class import PASSCONFIG
from gridlab.gldcore.Globals import TECHNOLOGYREADINESSLEVEL
from gridlab.gldcore.Object import Object
from gridlab.gldcore.TimeStamp import TS_SECOND


class MultiZone:

    def create_multi_zone(obj, parent):
        try:
            obj = gl_create_object(MultiZone.oclass)
            if obj != None:
                pass
            else:
                return 0
        except:
            pass


    def init_multi_zone(obj, parent):
        pass


    def sync_multi_zone(obj, t1, passconfig):
        t2 = "TS_NEVER"
        my = Object(obj, MultiZone)
        try:
            # switch statement implementation
            if passconfig == MultiZone.clockpass:
                obj.exec_clock = t1
            return t2
        except:
            pass


    def initialize_class(self, owner_class, module, multizone, passconfig, from_addr, to_addr, ua_addr):
        if owner_class is None:
            self.owner_class = gl_register_class(module, "multizone", sys.getsizeof(multizone), passconfig)
            if owner_class is None:
                raise Exception("unable to register class multizone")
            else:
                owner_class.trl = TECHNOLOGYREADINESSLEVEL.TRL_INTEGRATED

            if (gl_publish_variable(owner_class,
                                    # TODO: add your published properties here
                                    PropertyType.PT_object, "from", PADDR(from_addr),
                                    PropertyType.PT_object, "to", PADDR(to_addr),
                                    PropertyType.PT_double, "ua", PADDR(ua_addr),
                                    None) < 1):
                raise Exception("unable to publish properties in {}".format(__file__))

            self.defaults = owner_class
            # TODO: set the default values all properties here
            owner_class = initialize_multizone()

        return owner_class


    def initialize_multizone():
        multizone = {}
        multizone['from'] = None
        multizone['to'] = None
        multizone['ua'] = 0.0
        return multizone


    def heat_transfer(t0, t1, ua, from_office, to_office):
        if t1 > t0 and t0 > 0:
            p_from = object_data(from_office, office)
            p_to = object_data(to_office, office)
            dT = p_from.zone.current.air_temperature - p_to.zone.current.air_temperature
            ddT = p_from.zone.current.temperature_change - p_to.zone.current.temperature_change
            DT = dT + ddT / 2
            dQ = ua * DT * (t1 -t0) / TS_SECOND / 3600
            x = dQ * (t1 - t0)
            locked(from_office, p_from, Qz -= x)
            locked(to_office, p_to, Qz += dQ)
            if ddT != 0:
                return t1 + abs( 1 /ddT) * 3600 * TS_SECOND
            else:
                return TS_NEVER



    def check_if_not_null(obj, parent):
        if obj is not None:
            my = obj.get_data(MultiZone)
            gl_set_parent(obj, parent)
            return my.create()



    def init_multizone(obj, parent):
        try:
            if obj is not None:
                return obj.multizone.init(parent)
            else:
                return 0
        except:
            raise Exception("multizone")


    def process_data(pass_, my, obj, t1):
        if pass_ == PASSCONFIG.PC_PRETOPDOWN:
            t2 = my.presync(obj.exec_clock, t1)
        elif pass_ == PASSCONFIG.PC_BOTTOMUP:
            t2 = my.sync(obj.exec_clock, t1)
        elif pass_ == PASSCONFIG.PC_POSTTOPDOWN:
            t2 = my.postsync(obj.exec_clock, t1)
        else:
            # GL_THROW should be implemented separately
            raise Exception("invalid pass request ({})".format(pass_))

        return t2


    def gl_set_rank(from_, param):
        pass


    def object_data(from_, office):
        pass



class MultiZone:
    owner_class = None
    defaults = None
    passconfig = "PC_BOTTOMUP"
    clockpass = "PC_BOTTOMUP"
    def __init__(self, module):
        self.from_ = None  # Renamed 'from' to 'from_' to avoid Python keyword conflict
        self.to = None
        self.ua = 0.0
        self.name = ""

        if self.owner_class is None:
            self.owner_class = gl_register_class(module, "multizone", sys.getsizeof(self), self.passconfig)
            if self.owner_class is None:
                raise "unable to register class multizone"
            else:
                self.owner_class.trl = TECHNOLOGYREADINESSLEVEL.TRL_INTEGRATED

            if gl_publish_variable(
                self.owner_class,
                # TODO: add your published properties here
                PropertyType.PT_object, "from", PADDR(self.from_),
                PropertyType.PT_object, "to", PADDR(self.to),
                PropertyType.PT_double, "ua", PADDR(self.ua),
                None
            ) < 1:
                gl_error("unable to publish properties in %s" % __file__)
            MultiZone.defaults = self
            # TODO: set the default values of all properties here
            # ctypes.memset(ctypes.by_ref(self), 0, sys.getsizeof(self))

            self.oclass = gl_set_parent(self)

    def create(self):
        # self.__dict__ = MultiZone.defaults.copy()
        return 1  # return 1 on success, 0 on failure

    def init(self, parent):
        obj = self
        if self.from_ is None:
            gl_error(
                "{0} (multizone:{1}): from zone is not specified".format(obj.name if obj.name else "unnamed", obj.id))
        elif not gl_object_isa(self.from_, "office"):
            gl_error("{0} (multizone:{1}): from object is not an commercial office space".format(
                obj.name if obj.name else "unnamed", obj.id))
        if self.to is None:
            gl_error(
                "{0} (multizone:{1}): to zone is not specified".format(obj.name if obj.name else "unnamed", obj.id))
        elif not gl_object_isa(self.to, "office"):
            gl_error("{0} (multizone:{1}): to object is not an commercial office space".format(
                obj.name if obj.name else "unnamed", obj.id))
        if self.ua <= 0:
            gl_error("{0} (multizone:{1}): ua must be positive (value is {2:.2f})".format(
                obj.name if obj.name else "unnamed", obj.id, self.ua))
        gl_set_rank(self.from_, obj.rank + 1)
        gl_set_rank(self.to, obj.rank + 1)
        return 1  # return 1 on success, 0 on failure

    def presync(self, t0, t1):
        t2 = float('inf')
        return t2  # return t2>t1 on success, t2=t1 for retry, t2<t1 on failure

    def sync(self, t0, t1):
        if t1 > t0 and t0 > 0:
            p_from = object_data(self.from_, office)
            p_to = object_data(to, office)

            # initial delta T
            dT = p_from.zone.current.air_temperature - p_to.zone.current.air_temperature

            # rate of change of delta T
            ddT = p_from.zone.current.temperature_change - p_to.zone.current.temperature_change

            # mean delta T
            DT = dT + ddT / 2

            # mean heat transfer
            dQ = ua * DT * (t1 - t0) / TS_SECOND / 3600

            x = dQ * (t1 - t0)
            locked(self.from_, p_from.Qz -= x)
            locked(to, p_to.Qz += dQ)

            if ddT != 0:
                # time for 1 deg temperature change
                return t1 + abs(1 / ddT) * 3600 * TS_SECOND
            else:
                return TS_NEVER

        return TS_NEVER  # return t2>t1 on success, t2=t1 for retry, t2<t1 on failure

    def post_sync(self, t0, t1):
        t2 = float('inf')
        return t2  # return t2>t1 on success, t2=t1 for retry, t2<t1 on failure

