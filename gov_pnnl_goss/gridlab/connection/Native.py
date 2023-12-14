import re
from enum import Enum

from gov_pnnl_goss.gridlab.connection.Connection import CONNECTIONMODETYPE
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error, TS_ZERO, gl_verbose, PC_PRETOPDOWN, PC_BOTTOMUP, \
    PC_POSTTOPDOWN, gl_warning
from gov_pnnl_goss.gridlab.gldcore.Property import PROPERTYTYPE


class FUNCTIONRELAY:
    def __init__(self, localclass, localcall, remoteclass, remotename, route, xlate, drtn, ctype):
        self.localclass = localclass
        self.localcall = localcall
        self.remoteclass = remoteclass
        self.remotename = remotename
        self.route = route
        self.xlate = xlate
        self.next = None
        self.drtn = drtn
        self.ctype = ctype

def add_relay_function(route, fclass, flocal, rclass, rname, xlate, direction):
    # Implementation of add_relay_function
    # Replace with actual code as needed
    pass

def find_relay_function(rname, rclass):
    # Implementation of find_relay_function
    # Replace with actual code as needed
    pass


# # Constants
# _NONE = 0
# _ALLOW = 1
# _FORBID = 2
# _INIT = 3
# _PRECOMMIT = 4
# _PRESYNC = 5
# _SYNC = 6
# _POSTSYNC = 7
# _COMMIT = 8
# _PRENOTIFY = 9
# _POSTNOTIFY = 10
# _FINALIZE = 11
# _PLC = 12
# _TERM = 13
# _NUMVMI = 14
# _FIRST = _INIT
# _LAST = _TERM


class VARMAPINDEX(Enum):
    NONE = 0
    ALLOW = 1
    FORBID = 2
    INIT = 3
    PRECOMMIT = 4
    PRESYNC = 5
    SYNC = 6
    POSTSYNC = 7
    COMMIT = 8
    PRENOTIFY = 9
    POSTNOTIFY = 10
    FINALIZE = 11
    PLC = 12
    TERM = 13
    NUMVMI = 14
    FIRST=INIT
    LAST=TERM


class connection_mode:
    @staticmethod
    def new_instance(command):
        # Implementation of new_instance
        # Replace with actual code as needed
        pass

class CLASS:
    pass


def add_function(spec, local_class):
    if local_class is None:
        gl_error("native::add_function(const char *spec='%s'): local class '%s' does not exist" % (spec, local_class))
        return 0
    # rest of the function implementation goes here


# #
# def create_native_class(oclass, module):
#     if oclass is None:
#         oclass = gld_class.create(module, "native", sizeof(native),
#                                   PC_AUTOLOCK | PC_PRETOPDOWN | PC_BOTTOMUP |
#                                   PC_POSTTOPDOWN | PC_OBSERVER)
#         if oclass is None:
#             raise Exception("connection/native::native(MODULE*): unable to register class connection:native")
#         else:
#             oclass.trl = TRL_UNKNOWN
#
#         defaults = self
#         if ( gl_publish_variable(oclass,
#                 PROPERTYTYPE.PT_enumeration, "mode", get_mode_offset(),
#                 PROPERTYTYPE.PT_DESCRIPTION, "connection mode",
#                 PROPERTYTYPE.PT_KEYWORD, "SERVER", CONNECTIONMODETYPE.CM_SERVER,
#                 PROPERTYTYPE.PT_KEYWORD, "CLIENT", CONNECTIONMODETYPE.CM_CLIENT,
#                 PROPERTYTYPE.PT_KEYWORD, "NONE", CONNECTIONMODETYPE.CM_NONE,
#                 PROPERTYTYPE.PT_enumeration, "transport", get_transport_offset(),
#                 PROPERTYTYPE.PT_DESCRIPTION, "connection transport",
#                 PROPERTYTYPE.PT_KEYWORD, "UDP", CONNECTIONTYPE.CM_UDP,
#                 PROPERTYTYPE.PT_KEYWORD, "TCP", CONNECTIONTYPE.CM_TCP,
#                 PROPERTYTYPE.PT_KEYWORD, "NONE", CONNECTIONTYPE.CM_NONE,
#                 PROPERTYTYPE.PT_double, "timestep", get_timestep_offset(),
#                 PROPERTYTYPE.PT_DESCRIPTION, "timestep between updates",
#                 PROPERTYTYPE.PT_UNITS, "s",
#                 None) < 1 ):
#             raise Exception("connection/native::native(MODULE*): unable to publish properties of connection:native")
#
#         if not gl_publish_loadmethod(oclass, "link",
#                                      reinterpret_cast<int(*)(void *, char *)>(loadmethod_native_link)):
#             raise Exception("connection/native::native(MODULE*): unable to publish link method of connection:native")
#         if not gl_publish_loadmethod(oclass, "option",
#                                      reinterpret_cast<int(*)(void *, char *)>(loadmethod_native_option)):
#             raise Exception("connection/native::native(MODULE*): unable to publish option method of connection:native")
#         mode = 0
#         transport = 0
#         memset(map, 0, sizeof(map))

#
# def convert_to_snake_case(self):
#     for n in range(ALLOW, _NUMVMI):
#         self.map[n].resolve()
#
#         if n >= _FIRST and n <= _LAST:
#             self.map[n].linkcache(get_connection(), (void *) xlate)
#


def hex_converter(c):
    if c < 10:
        return str(c)
    elif c < 16:
        return chr(c - 10 + ord('A'))
    else:
        return '?'


def unhex(h):
    if '0' <= h <= '9':
        return ord(h) - ord('0')
    elif 'A' <= h <= 'F':
        return ord(h) - ord('A') + 10
    elif 'a' <= h <= 'f':
        return ord(h) - ord('a') + 10
    return ord(h) - ord(' ')


def convert_to_hex(out, max_size, _in, length):
    def hex(char):
        if char < 10:
            return chr(char + ord('0'))
        else:
            return chr((char - 10) + ord('A'))
    
    hlen = 0
    n = 0
    while n < length:
        byte = _in[n]
        lo = byte & 0xf
        hi = (byte >> 4) & 0xf
        out.append(hex(lo))
        out.append(hex(hi))
        hlen += 2
        n += 1
        if hlen >= max_size:
            return -1
    out.append('\0')
    return hlen


def convert_from_hex(buf, len, hex, hexlen):
    p = bytearray(buf)
    lo = 0
    hi = 0
    c = 0
    n = 0
    for n in range(hexlen):
        if hex[n:n+2] == '':
            break
        c = unhex(hex[n])
        if c == -1:
            return -1
        lo = c & 0x0f
        c = unhex(hex[n+1])
        hi = (c << 4) & 0xf0
        if c == -1:
            return -1
        p.append(hi | lo)
        n += 2
        if n >= len:
            return -1
    return n


class Native:
    def __init__(self, module):
        super().__init__(module)
        self.mode = 0  # GL_ATOMIC(enumeration,mode)
        self.transport = 0  # GL_ATOMIC(enumeration,transport)
        self.timestep = 0.0  # GL_ATOMIC(double,timestep)
        self.m = None
        self.map = [None] * VARMAPINDEX.NUMVMI
        self.oclass = None

        if self.oclass is None:
            self.oclass = gld_class.create(module, "native", 0, PC_AUTOLOCK|PC_PRETOPDOWN|PC_BOTTOMUP|PC_POSTTOPDOWN|PC_OBSERVER)
            if self.oclass is None:
                raise "connection/native::__init__(MODULE*): unable to register class connection:native"
            else:
                self.oclass.trl = TRL_UNKNOWN

            self.defaults = self
            if not gl_publish_variable(self.oclass, PROPERTYTYPE.PT_enumeration, "mode", self.get_mode_offset(),
                    PROPERTYTYPE.PT_DESCRIPTION, "connection mode",
                    PROPERTYTYPE.PT_KEYWORD, "SERVER", CONNECTIONMODETYPE.CM_SERVER,
                    PROPERTYTYPE.PT_KEYWORD, "CLIENT", CONNECTIONMODETYPE.CM_CLIENT,
                    PROPERTYTYPE.PT_KEYWORD, "NONE", CONNECTIONMODETYPE.CM_NONE,
                PROPERTYTYPE.PT_enumeration, "transport", self.get_transport_offset(),
                    PROPERTYTYPE.PT_DESCRIPTION, "connection transport",
                    PROPERTYTYPE.PT_KEYWORD, "UDP", CONNECTIONTYPE.CM_UDP,
                    PROPERTYTYPE.PT_KEYWORD, "TCP", CONNECTIONTYPE.CM_TCP,
                    PROPERTYTYPE.PT_KEYWORD, "NONE", CONNECTIONTYPE.CM_NONE,
                PROPERTYTYPE.PT_double, "timestep", self.get_timestep_offset(),
                    PROPERTYTYPE.PT_DESCRIPTION, "timestep between updates",
                    PROPERTYTYPE.PT_UNITS, "s",
                None) < 1:
                raise "connection/native::__init__(MODULE*): unable to publish properties of connection:native"

            if not gl_publish_loadmethod(self.oclass, "link", getattr(int, "(void *, char *)>(loadmethod_native_link))") :
                gl_error("connection/native::__init__(MODULE*): unable to publish link method of connection:native")
            if not gl_publish_loadmethod(self.oclass, "option", getattr(int, "(void *, char *)>(loadmethod_native_option))"):
                gl_error("connection/native::__init__(MODULE*): unable to publish option method of connection:native")
            self.mode = 0
            self.transport = 0
            self.map =  [0] * len(self.map)

    def get_connection(self):
        return self.m

    def set_connection(self, p):
        if self.m:
            del self.m
        self.m = p

    def new_connection(self, command):
        if self.m:
            del self.m
        self.m = connection_mode.new_instance(command)

    def get_varmapindex(self, name):
        varmap_name = ["",
                       "allow",
                       "forbid",
                       "init",
                       "precommit",
                       "presync",
                       "sync",
                       "postsync",
                       "commit",
                       "prenotify",
                       "postnotify",
                       "finalize",
                       "plc",
                       "term"]
        for n in range(1, len(varmap_name)):
            if varmap_name[n] == name:
                return n
        return 0

    def parse_function(self, specs):
        local_class = [64]
        local_name = [64]
        direction = [8]
        remote_class = [64]
        remote_name = [64]
        m = re.match("%[^/]/%[^-<>\t ]%*[\t ]%[-<>]%*[\t ]%[^/]/%[^\n]", specs)
        if m:
            if len(m.groupdict()) != 5:
                gl_error("native::add_function(const char *spec='%s'): specification is invalid", specs)
            local_class = m.group(0)
            local_name = m.group(0)
            direction = m.group(0)
            remote_class = m.group(0)
            remote_name = m.group(0)

        if direction == '->':
            f_class = callback.class_getname(local_class)
            if f_class == None:
                gl_error("native::add_function(const char *spec='%s'): local class '%s' does not exist", specs,
                         local_class)
                return 0

            f_local = callback.function.get(local_class, local_name)
            if f_local != None:
                gl_warning(
                    "native::add_function(const char *spec='%s'): outgoing call definition of '%s' overwrites existing function definition in class '%s'",
                    specs, local_name, local_class)

            f_local = add_relay_function(self, local_class, "", remote_class, remote_name, None, DXD_WRITE)
            if f_local == None:
                return 0

            return callback.function.define(f_class, local_name, f_local) != None
        elif direction == '<-':
            gl_error("native::add_function(const char *spec='%s'): incoming calls not implemented", specs)
            return 0
        else:
            gl_error("native::add_function(const char *spec='%s'): bidirection calls not implemented", specs)
            return 0

    def create(self):
        self.mode = 'CM_CLIENT'
        self.transport = 'CT_TCP'
        self.timestep = 1.0

        for n in range(ALLOW, _NUMVMI):
            self.map[n] = varmap()

        return 1

    def init(self, parent, xlate):
        for n in range(ALLOW, _NUMVMI):
            self.map[n].resolve()
            if n >= _FIRST and n <= _LAST:
                self.map[n].linkcache(get_connection(), xlate)
                return 1

    def precommit(self, t, xlate):
        if self.get_connection().update(map["precommit"], "precommit", xlate) < 0:
            gl_error("connection/native::precommit(TIMESTAMP t=%lld, TRANSLATOR *xltr=%p): update failed", t,xlate)
            return 0
        else:
            return 1

    def presync(self, timestamp, xlate=None):
        # Implementation of presync
        # Replace with actual code as needed
        pass

    def sync(self, timestamp, xlate=None):
        # Implementation of sync
        # Replace with actual code as needed
        pass

    def postsync(self, timestamp, xlate=None):
        # Implementation of postsync
        # Replace with actual code as needed
        pass

    def commit(self, t_0, t_1, xlate):
        if self.get_connection().update(self.map[COMMIT], "commit", xlate) < 0:
            gl_error("connection/native::commit(TIMESTAMP t0=%lld, TIMESTAMP t1=%lld, TRANSLATOR *xltr=%p): update failed", t_0, t_1, xlate)
            return TS_ZERO
        else:
            return t_0 + self.timestep

    def prenotify(self, property, value, translator):
        if self.get_connection().update(self.map["prenotify"], "prenotify", translator) < 0:
            gl_error("connection/native::prenotify(PROPERTY *p={name='%s'}, char *v='%s', TRANSLATOR *xltr=%p): update failed", property.name, value, translator)
            return 0
        else:
            return 1

    def postnotify(self, property, value, translator):
        if self.get_connection().update(self.map['postnotify'], "postnotify", translator) < 0:
            gl_error("connection/native::postnotify(PROPERTY *p={name='%s'}, char *v='%s', TRANSLATOR *xltr=%p): update failed", property.name, value, translator)
            return 0
        else:
            return 1

    def finalize(self, xlate):
        if self.get_connection().update(self.map['finalize'], "finalize", xlate) < 0:
            gl_error("connection/native::finalize(TRANSLATOR *xltr=%p): update failed", xlate)
            return 0
        else:
            return 1

    def plc(self, timestamp, xlate=None):
        if self.get_connection().update(self.map["PLC"], "plc", xlate) < 0:
            gl_error("connection/native::plc(TIMESTAMP t=%lld, TRANSLATOR *xltr=%p): update failed", timestamp, xlate)
            return 0
        else:
            return timestamp + self.timestepv

    def term(self, timestamp, xlate=None):
        if self.get_connection().update(self.map["term"], "term", xlate) < 0:
            gl_error("connection/native::sync(TIMESTAMP t=%lld, TRANSLATOR *xltr=%p): update failed",timestamp, xlate)

    def function(self, remotename, functionname, data, datalen, xlate_out=None, xlate_in=None):
        # Implementation of function
        # Replace with actual code as needed
        pass

    def link(self, value):
        command = value[0: value.index(':')]
        argument = value[value.index(':') + 1:]

        if len(value.split(':')) == 2:
            gl_verbose("connection/native::link(char *value='%s') parsed ok", value)

            if command == "function":
                return self.parse_function(argument)
            else:
                n = self.get_varmapindex(command)
                if n != None:
                    return self.map[n].add(argument, CONNECTIONMODETYPE.CM_UNKNOWN)
                else:
                    gl_error("connection/native::link(char *value='%s') map '%s' not recognized", value, command)
                    return 0
        else:
            gl_error("connection/native::link(char *value='%s'): unable to parse link argument", value)
            return 0

    def option(self, target_or_value, command=None):
        if not command:
            value = target_or_value
            value_parts = value.split(':', 1)  # Split the value into two parts at the first ':' encountered
            if len(value_parts) == 2:
                target, command = value_parts
                gl_verbose("connection/native::option(char *value='%s') parsed ok", value)
                return self.option(target, command)
            else:
                gl_error("connection/native::option(char *value='%s'): unable to parse option argument", value)
                return 0
        else:
            target = target_or_value
            if target == "connection":
                if self.get_connection() == None:
                    self.new_connection(command)
                    if self.m == None:
                        gl_error(
                            "connection/native::option(char *target='%s', char *command='%s'): connection with options '%s' failed" % (
                                target, command, command))
                        return 0
                    else:
                        return 1
                elif not self.get_connection().option(command):
                    gl_error(
                        "connection/native::option(char *target='%s', char *command='%s'): connection mode already set" % (
                            target, command))
                return 0
            elif self.get_connection() == None:
                gl_error("option(char *target='%s', char *command='%s'): connection mode hasn't be established" % (
                    target, command))
                return 0
            else:
                return self.get_connection().option(target, command)

    def get_firstmap(self):
        return _FIRST

    def get_lastmap(self):
        return _LAST

    def get_varmap(self, n):
        return self.map[n].getfirst()

    def get_initmap(self):
        return self.map[INIT]

    def outgoing_route_function(self, from_str, to_str, func_name, func_class, data, len):
        result = -1
        rclass = func_class
        lclass = from_str
        hexlen = 0
        relay = self.find_relay_function(func_name, rclass)
        if relay is None:
            raise ValueError(
                "native::outgoing_route_function: the relay function for function name {} could not be found.".format(
                    func_name))
        message = ""

        connection = relay.route.get_connection()
        transport = connection.get_transport()
        msglen = 0

        if to_str is None or from_str is None:
            raise ValueError("from objects and to objects must be named.")

        connection.xlate_out(transport, "to", to_str, 0, ETO_QUOTES)
        connection.xlate_out(transport, "class", relay.remoteclass, 0, ETO_QUOTES)
        connection.xlate_out(transport, "function", relay.remotename, 0, ETO_QUOTES)
        connection.xlate_out(transport, "from", from_str, 0, ETO_QUOTES)

        message = convert_to_hex(message, len(data), data, len)
        if hexlen > 0:
            connection.xlate_out(transport, "data", message, 0, ETO_QUOTES)

        if transport.send(message, msglen) < 0:
            raise ValueError("Message failed to be sent.")

    def add_relay_function(self, route, f_class, f_local, r_class, r_name, xlate, direction):
        relay = find_relay_function(r_name, r_class)
        if relay is not None:
            gl_error(
                "connection_transport::create_relay_function(rclass='{}', rname='{}') a relay function is already defined for '{}/{}'".format(
                    r_class, r_name, r_class, r_name))
            return 0

        relay = FUNCTIONRELAY()
        if relay is None:
            gl_error(
                "connection_transport::create_relay_function(rclass='{}', rname='{}') memory allocation failed".format(
                    r_class, r_name))
            return 0

        relay.local_class = f_class
        relay.local_call = f_local
        relay.remoteclass = r_class[:len(relay.remoteclass) - 1]
        relay.remotename = r_name[:len(relay.remotename) - 1]
        relay.drtn = direction
        relay.next = self.first_relayfunction
        relay.xlate = xlate

        relay.route = route
        first_relayfunction = relay

        return outgoing_route_function

    def find_relay_function(self, r_name, r_class):
        relay = self.first_relay_function
        while relay:
            if relay.remoteclass == r_class and relay.remotename == r_name:
                return relay
            relay = relay.next
        return None








    def presync_native(self, timestamp, xlate):
        if self.get_connection().update(self.map["presync"], "presync", xlate) < 0:
            gl_error("connection/native::presync(timestamp=%s, xlate=%s): update failed" % (timestamp, xlate))
            return 0
        else:
            return timestamp + int(self.timestep)

    def timestamp_native_sync(self, timestamp, xlate):
        if self.get_connection().update(self.map['sync'], "sync", xlate) < 0:
            gl_error("connection/native::sync(timestamp t=%lld, TRANSLATOR *xltr=%p): update failed", timestamp, xlate)
            return 0
        else:
            return timestamp + self.timestep

    def native_postsync(self, t, xlate):
        if self.get_connection().update(self.map['POSTSYNC'], "postsync", xlate) < 0:
            gl_error("connection/native::postsync(TIMESTAMP t=%lld, TRANSLATOR *xltr=%p): update failed", t, xlate)
            return 0
        else:
            return t + self.timestep




