from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error, gl_warning, gl_debug
import ctypes

from gov_pnnl_goss.gridlab.connection.Cache import Cache
from gov_pnnl_goss.gridlab.connection.Client import Client
#from gridlab.connection.FncsMsg import gld_property
from gov_pnnl_goss.gridlab.connection.Server import Server
from gov_pnnl_goss.gridlab.connection.Transport import CONNECTIONTRANSPORT

import re
import sys
from enum import Enum
import traceback

seqnum = 0
xlate_out = None
xlate_in = None
read_cache = None
write_cache = None
transport = None

# Define constants
ET_MATCHONLY = 0
ET_GROUPOPEN = 1
ET_GROUPCLOSE = 2
ETO_NONE = 0
ETO_QUOTES = 3


class ClockUpdateList:
    def __init__(self):
        self.data = None
        self.clkupdate = None
        self.next = None


class DeltaInterUpdateList:
    def __init__(self):
        self.data = None
        self.deltainterupdate = None
        self.next = None


class DeltaClockUpdateList:
    def __init__(self):
        self.data = None
        self.dclkupdate = None
        self.next = None


# Define message flags as an enum
class MESSAGEFLAG(Enum):
    MSG_CONTINUE = 0x01  # msg part of a group of message (automatically new if first in group)
    MSG_INITIATE = 0x02  # open a new message group (if current group exists then gives warning/error)
    MSG_COMPLETE = 0x04  # closes current message group
    MSG_TAG = 0x08  # element tag (followed by tag name)
    MSG_SCHEMA = 0x10  # group element is a schema (followed by VARMAP*)
    MSG_STRING = 0x20  # group element is a string (followed by "name",maxsize,"value")
    MSG_REAL = 0x40  # group element is a double (e.g. "name","%wfmt","%rfmt",ptr)
    MSG_INTEGER = 0x80  # group element is an int64 (e.g. "name","%wfmt","%rfmt",ptr)
    MSG_DATA = 0x100  # group element is gridlabd data (followed by VARMAP*)
    MSG_OPEN = 0x200  # open a subgroup (followed by "name")
    MSG_CLOSE = 0x400  # close a subgroup (nothing follows)
    MSG_CRITICAL = 0x800  # flag message as critical (must preceded MSG_INITIATE to affect incoming traffic)


# Define connection security levels as an enum
class CONNECTIONSECURITY(Enum):
    CS_NONE = 0
    CS_LOW = 1
    CS_STANDARD = 2
    CS_HIGH = 3
    CS_EXTREME = 4
    CS_PARANOID = 5


class CONNECTIONMODETYPE(Enum):
    CM_UNKNOWN = -1
    CM_NONE = 0
    CM_SERVER = 1
    CM_CLIENT = 2


class CONNECTIONTYPE(Enum):
    CM_NONE = 0
    CM_UDP = 1
    CM_TCP = 2


class DATAEXCHANGEDIRECTION(Enum):
    DXD_READ = 0
    DXD_WRITE = 1


def convert_to_python_function(count, write_cache, tag, read_cache, varlist, dxd_read, xlate, ignore_error):
    if count > 0:
        gl_debug("write cache dump...")
        write_cache.dump()
        id = 0
        # send outgoing data
        if client_initiated(
                MESSAGEFLAG.MSG_INITIATE,
                MESSAGEFLAG.MSG_TAG, "method", tag,
                MESSAGEFLAG.MSG_OPEN, "data",
                MESSAGEFLAG.MSG_DATA, write_cache,
                MESSAGEFLAG.MSG_CLOSE,
                MESSAGEFLAG.MSG_COMPLETE, id,
                None) < 0:
            return -1
        # receive incoming data
        if server_response(
                MESSAGEFLAG.MSG_INITIATE,
                MESSAGEFLAG.MSG_TAG, "result", tag,
                MESSAGEFLAG.MSG_OPEN, "data",
                MESSAGEFLAG.MSG_DATA, read_cache,
                MESSAGEFLAG.MSG_CLOSE,
                MESSAGEFLAG.MSG_COMPLETE, id,
                None) < 0:
            return ignore_error > 0
        # update local variables with incoming cache values
        count = 0
        v = varlist.getfirst()
        while v is not None:
            if not self.update(v, DATAEXCHANGEDIRECTION.DXD_READ, xlate):
                return -1
            else:
                count += 1
                v = v.next
        gl_debug("read cache dump...")
        read_cache.dump()


def process_map(map_dir, read_cache):
    if map_dir == DATAEXCHANGEDIRECTION.DXD_READ:
        item = read_cache.find_item(map)
        if item is not None:
            return item
        else:
            return read_cache.add_item(map)


def convert_to_python(map):
    if map.dir == DATAEXCHANGEDIRECTION.DXD_WRITE:
        item = write_cache.find_item(map)
        if item is not None:
            return item
        else:
            return write_cache.add_item(map)


class ConnectionMode:
    def __init__(self):
        self.ignore_error = 0
        self.msg = [''] * 1024
        self.read_cache = Cache()
        self.seqnum = 0
        self.transport = None
        self.write_cache = Cache()
        self.xlate_in = None
        self.xlate_out = None

    def set_transport(self, transport: CONNECTIONTRANSPORT):
        # ignore same transport
        if self.transport is not None and self.transport.get_transport() == transport:
            return

        # delete old transport
        if self.transport is not None:
            del self.transport

        # create new transport
        self.transport = connection_transport.new_instance(transport)

        # check result
        if self.transport is None:
            gl_warning("connection_mode::set_transport(): unable to create new instance")
        # reset sequence number
        self.seqnum = 0

    ############################################################
    def exchange(self, xlate, *args):
        # no arguments
        if len(args)==0:
            self.exchange_none(xlate)
        if len(args)==1:
            arg_type = type(args[0])
            match arg_type:
                case type(bool()):
                    self.exchange_bool(xlate, args[0])
                case type(int()):
                    self.exchange_id(xlate, args[0])


    def exchange_bool(self, xlate, critical: bool) -> int:
        pass

    def exchange_none(self, xlate) -> int:
        if not self.transport.message_continue():
            self.error("message queue continued with none open")
            return -1
        else:
            self.debug(9, "message queue control: MSG_CONTINUE")
        return 0




    def exchange_integer(self, xlate, tag, integer=None):
        """
        Exchanges an integer value, optionally based on a tag.
        """
        # Implement the logic for exchanging an integer here
        if integer is not None:
            self.debug(f"Exchanging integer for tag {tag}: {integer}")
            # Convert integer to string if necessary and call xlate



    #
    # def exchange_int(self, xlate, id: int) -> int:
    #     pass

    def exchange_id(self, xlate, id: int):
        self._exchange(xlate, "id", self.seqnum)
        if id is not None:
            id[0] = self.seqnum
        self.transport.reset_fieldcount()
        xlate(self.transport, None, None, ET_GROUPCLOSE, ETO_NONE)
        if not self.transport.message_close():
            self.error("message queue closed with none open")
            return -1
        else:
            self.debug(9, "message queue control: MSG_COMPLETE (id=%lld)" % id[0])
            return 0  # ok


    # def exchange(self, xlate, tag: str, value: str) -> int:
    #     pass

    def exchange_tag_value(self, exchange_translator, tag:str, value:str)-> int:
        return exchange_translator(transport, tag, value, 0, ETO_QUOTES)


    #
    # def exchange(self, xlate, tag: str, len: int, value: str) -> int:
    #     pass

    def exchange_tag_len_value(self, xlate, tag: str, len: int, value: str) -> int:
        return xlate(transport, tag, value, len, ETO_QUOTES)


    #
    # def exchange(self, xlate, tag: str, real: float) -> int:
    #     pass

    def exchange_tag_real(self, exchange_translator, tag: str, real: float) -> int:
        temp = str(real)
        status = exchange_translator(transport, tag, temp, len(temp), ETO_NONE)
        if status > 0:
            status = float(temp)
        return status

    #
    # def exchange(self, xlate, tag: str, integer: int) -> int:
    #     pass
    def exchange_tag_integer(self, xlate, tag: str, integer: int) -> int:
        temp = ""
        status = xlate(transport, tag, temp, len(temp), ETO_NONE)
        if status > 0:
            status = integer
        return status

    def exchange_critical(self, xlate, critical):
        if not self.transport.message_open():
            self.error("new message queue opened with unsent messages pending")
            return -1
        else:
            self.debug(9, "message queue control: MSG_INITIATE (critical=%s)" % ("yes" if critical else "no"))
        self.transport.reset_fieldcount()
        xlate(self.transport, None, None, ET_GROUPOPEN, ETO_NONE)
        self.transport.reset_fieldcount()
        return 0

    ##################################

    def exchange_string(self, xlate, tag, value=None):
        """
        Exchanges a string value, optionally based on a tag.
        """
        # Implement the logic for exchanging a string value here
        self.debug(f"Exchanging string for tag {tag}: {value}")
        # Call xlate as needed


    def exchange_real(self, xlate, tag, real=None):
        """
        Exchanges a real (float) value, optionally based on a tag.
        """
        # Implement the logic for exchanging a real number here
        if real is not None:
            self.debug(f"Exchanging real number for tag {tag}: {real}")
            # Convert real to string if necessary and call xlate


    def exchange_schema(self, xlate, list):
        status = 0
        for status in range(list.get_count()):
            item = list.get_item(status)
            map = item.get_var()
            prop = gld_property(map.obj.get_object(), map.local_name.split('.')[1])
            type = prop.get_type()
            spec = type.get_spec()
            info = f"{spec.name} {prop.get_object().name}:{prop.get_name()}"
            xlate(transport, map.remote_name, info, 256, ETO_QUOTES)
        return status

    def exchange_data(self, xlate, cache_list):
        for n in range(cache_list.get_count()):
            item = cache_list.get_item(n)
            remote_name = item.get_remote()
            item_buffer = item.get_buffer()
            if not xlate(transport, item.get_remote(), item.get_buffer(), item.get_size(), ETO_QUOTES):
                return 0
        return 1

    def exchange_open(self, exchange_translator, tag):
        status = exchange_translator(self.transport, tag, None, "ET_GROUPOPEN", "ETO_QUOTES")
        self.transport.reset_fieldcount()
        return status

    def exchange_close(self, exchange_translator):
        transport.reset_fieldcount()
        return exchange_translator(transport, None, None, ET_GROUPCLOSE, ETO_NONE)

    def send(self, buf, len):
        return int(transport.send(buf, len))

    def recv(self, buf, len):
        return int(self.transport.recv(buf, len))

    def set_translators(self, out, in_, data):
        self.xlate_out = out
        self.xlate_in = in_

    
    def get_mode(self, tag):
        if tag == "CM_SERVER":
            return CONNECTIONMODETYPE.CM_SERVER
        elif tag == "CM_CLIENT":
            return CONNECTIONMODETYPE.CM_CLIENT
        else:
            print(f"connection_mode::new_instance(char *options='{options}'): unknown connection mode '{tag}'")
            return "CM_NONE"

    def new_instance(self, options):
        next_tag = None
        tag = None
        connection = None
        temp = options
        tags = re.split(r'[,\s]+', temp)
        for tag in tags:
            if connection is None:
                e = self.get_mode(tag)
                if e == CONNECTIONMODETYPE.CM_SERVER:
                    connection = Server()
                elif e == CONNECTIONMODETYPE.CM_CLIENT:
                    connection = Client()
                else:
                    print(f"connection_mode::new_instance(char *options='{options}'): unknown connection mode '{tag}'")
                    return None
            elif self.transport is None:
                self.set_transport(self.get_transport(tag))
            else:
                cmd, arg = re.split(r'[ =]+', tag)
                if cmd == "on_error":
                    if arg == "halt":
                        connection.ignore_error = 0
                    elif arg == "ignore":
                        connection.ignore_error = 1
                    else:
                        print(f"connection_mode::new_instance(char *options='{options}'): unrecognized {cmd} value '{arg}'")
                        return None
                else:
                    print(f"connection_mode::new_instance(char *options='{options}'): unrecognized tag '{tag}'")
                    return None
                return connection
        if connection is None:
            print(f"connection_mode::new_instance(char *options='{options}'): connection mode not specified")
        if self.transport is None:
            print(f"connection_mode::new_instance(char *options='{options}'): transport not specified, using default UDP")
            self.set_transport(CT_UDP)
        return connection

    # def server_response(self, flag, *args):
    #     critical = flag == MESSAGEFLAG.MSG_CRITICAL
    #     count = None
    #     msgcount = 0
    #     id = None
    #     stop = False
    #     if self.get_mode() == CONNECTIONMODETYPE.CM_CLIENT:
    #         if self.recv() > 0:
    #             print(f"receiving message: length=[{self.transport.get_position()}] buffer=[{self.transport.get_input()}]")
    #             while not stop:
    #                 msgcount += 1
    #                 if flag == MESSAGEFLAG.MSG_CRITICAL:
    #                     critical = True
    #                     print("connection_mode::exchange() message is critical")
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_INITIATE:
    #                     if self.exchange(xlate_in, critical) < 0:
    #                         print("connection_mode::exchange(): transport status control error")
    #                         count = -msgcount
    #                         stop = True
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_CONTINUE:
    #                     if self.exchange(xlate_in) < 0:
    #                         print("connection_mode::exchange(): transport status control error")
    #                         count = -msgcount
    #                         stop = True
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_COMPLETE:
    #                     id = args.pop(0)
    #                     if self.exchange(xlate_in, id) < 0:
    #                         print("connection_mode::exchange(): transport status control error")
    #                         count = -msgcount
    #                         stop = True
    #                     msgcount = 0
    #                     count = msgcount
    #                     stop = True
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_SCHEMA:
    #                     dir = args.pop(0)
    #                     print(f"connection_mode::exchange(...) MSG_SCHEMA('{dir}',cache=0x{hex(read_cache) if dir == DATAEXCHANGEDIRECTION.DXD_READ else hex(write_cache)})")
    #                     if dir == DATAEXCHANGEDIRECTION.DXD_READ:
    #                         if self.exchange_schema(xlate_out, read_cache) < 0:
    #                             print("exchange(): schema exchange failed")
    #                             count = -msgcount
    #                             stop = True
    #                     elif dir == DATAEXCHANGEDIRECTION.DXD_WRITE:
    #                         if self.exchange_schema(xlate_out, write_cache) < 0:
    #                             print("exchange(): schema exchange failed")
    #                             count = -msgcount
    #                             stop = True
    #                     else:
    #                         print("exchange(): schema exchange failed, invalid data direction supplied")
    #                         count = -msgcount
    #                         stop = True
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_TAG:
    #                     tag = args.pop(0)
    #                     value = args.pop(0)
    #                     print(f"connection_mode::exchange(...) MSG_TAG('{tag}','{value}')")
    #                     if self.exchange(xlate_in, tag, value) < 0:
    #                         print(f"connection_mode::exchange(): tagged value exchange failed for ('{tag}','{value}')")
    #                         count = -msgcount
    #                         stop = True
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_STRING:
    #                     tag = args.pop(0)
    #                     length = args.pop(0)
    #                     buf = args.pop(0)
    #                     print(f"client_initiated(...) MSG_STRING('{tag}', {length}, '{buf}')")
    #                     if self.exchange(xlate_in, tag, length, buf) < 0:
    #                         print(f"connection_mode::exchange(): string value exchange failed for ('{tag}', {length}, '{buf}')")
    #                         count = -msgcount
    #                         stop = True
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_REAL:
    #                     tag = args.pop(0)
    #                     data = args.pop(0)
    #                     print(f"exchange(...) MSG_REAL('{tag}', 0x{hex(data)}={data})")
    #                     if self.exchange(xlate_in, tag, data) < 0:
    #                         print(f"connection_mode::exchange(): double value exchange failed for ('{tag}', 0x{hex(data)}={data})")
    #                         count = -msgcount
    #                         stop = True
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_INTEGER:
    #                     tag = args.pop(0)
    #                     data = args.pop(0)
    #                     print(f"connection_mode::exchange(...) MSG_INTEGER('{tag}', 0x{hex(data)}={data})")
    #                     if self.exchange(xlate_in, tag, data) < 0:
    #                         print(f"connection_mode::exchange(): double value exchange failed for ('{tag}', 0x{hex(data)}={data})")
    #                         count = -msgcount
    #                         stop = True
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_DATA:
    #                     data_list = args.pop(0)
    #                     print(f"connection_mode::exchange(...) MSG_DATA(cache=0x{hex(data_list)})")
    #                     if self.exchange_data(xlate_in, data_list) < 0:
    #                         print(f"connection_mode::exchange(): data exchange failed")
    #                         count = -msgcount
    #                         stop = True
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_OPEN:
    #                     tag = args.pop(0)
    #                     print(f"connection_mode::exchange(...) MSG_OPEN('{tag}')")
    #                     if self.exchange_open(xlate_in, tag) < 0:
    #                         print(f"connection_mode::exchange(): start group '{tag}' exchange failed")
    #                         count = -msgcount
    #                         stop = True
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 elif flag == MESSAGEFLAG.MSG_CLOSE:
    #                     print(f"connection_mode::exchange(...) MSG_CLOSE")
    #                     if self.exchange_close(xlate_in) < 0:
    #                         print(f"connection_mode::exchange(): end group exchange failed")
    #                         count = -msgcount
    #                         stop = True
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #                     continue
    #                 else:
    #                     print(f"connection_mode::exchange(...) unrecognized message control flag {flag} was ignored")
    #                     new_flag = args.pop(0)
    #                     if new_flag == 0:
    #                         stop = True
    #                     else:
    #                         flag = new_flag
    #
    #             if msgcount != 0:
    #                 count = msgcount if msgcount > 0 else -1
    #
    #             if count == 0:
    #                 print(f"sending message: length=[{self.transport.get_position()}] buffer=[{self.transport.get_input()}]")
    #                 return self.send() == self.transport.get_position()
    #
    #             return -1 if count < 0 and critical else 0
    #     elif self.get_mode() == CONNECTIONMODETYPE.CM_SERVER:
    #         while not stop:
    #             msgcount += 1
    #             if flag == MESSAGEFLAG.MSG_CRITICAL:
    #                 critical = True
    #                 print("connection_mode::exchange() message is critical")
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_INITIATE:
    #                 seqnum += 1
    #                 if self.exchange(xlate_out, critical) < 0:
    #                     print("connection_mode::exchange(): transport status control error")
    #                     count = -msgcount
    #                     stop = True
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_CONTINUE:
    #                 if self.exchange(xlate_out) < 0:
    #                     print("connection_mode::exchange(): transport status control error")
    #                     count = -msgcount
    #                     stop = True
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_COMPLETE:
    #                 id = args.pop(0)
    #                 if self.exchange(xlate_out, id) < 0:
    #                     print("connection_mode::exchange(): transport status control error")
    #                     count = -msgcount
    #                     stop = True
    #                 msgcount = 0
    #                 count = msgcount
    #                 stop = True
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_SCHEMA:
    #                 dir = args.pop(0)
    #                 print(f"connection_mode::exchange(...) MSG_SCHEMA('{dir}',cache=0x{hex(read_cache) if dir == DATAEXCHANGEDIRECTION.DXD_READ else hex(write_cache)})")
    #                 if dir == DATAEXCHANGEDIRECTION.DXD_READ:
    #                     if self.exchange_schema(xlate_out, read_cache) < 0:
    #                         print("exchange(): schema exchange failed")
    #                         count = -msgcount
    #                         stop = True
    #                 elif dir == DATAEXCHANGEDIRECTION.DXD_WRITE:
    #                     if self.exchange_schema(xlate_out, write_cache) < 0:
    #                         print("exchange(): schema exchange failed")
    #                         count = -msgcount
    #                         stop = True
    #                 else:
    #                     print("exchange(): schema exchange failed, invalid data direction supplied")
    #                     count = -msgcount
    #                     stop = True
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_TAG:
    #                 tag = args.pop(0)
    #                 value = args.pop(0)
    #                 print(f"connection_mode::exchange(...) MSG_TAG('{tag}','{value}')")
    #                 if self.exchange(xlate_out, tag, value) < 0:
    #                     print(f"connection_mode::exchange(): tagged value exchange failed for ('{tag}','{value}')")
    #                     count = -msgcount
    #                     stop = True
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_STRING:
    #                 tag = args.pop(0)
    #                 length = args.pop(0)
    #                 buf = args.pop(0)
    #                 print(f"client_initiated(...) MSG_STRING('{tag}', {length}, '{buf}')")
    #                 if self.exchange(xlate_out, tag, length, buf) < 0:
    #                     print(f"connection_mode::exchange(): string value exchange failed for ('{tag}', {length}, '{buf}')")
    #                     count = -msgcount
    #                     stop = True
    #                 new_flag = args.pop(0)
    #                 if new_flag== 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_REAL:
    #                 tag = args.pop(0)
    #                 data = args.pop(0)
    #                 print(f"exchange(...) MSG_REAL('{tag}', 0x{hex(data)}={data})")
    #                 if self.exchange(xlate_out, tag, data) < 0:
    #                     print(f"connection_mode::exchange(): double value exchange failed for ('{tag}', 0x{hex(data)}={data})")
    #                     count = -msgcount
    #                     stop = True
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_INTEGER:
    #                 tag = args.pop(0)
    #                 data = args.pop(0)
    #                 print(f"connection_mode::exchange(...) MSG_INTEGER('{tag}', 0x{hex(data)}={data})")
    #                 if self.exchange(xlate_out, tag, data) < 0:
    #                     print(f"connection_mode::exchange(): double value exchange failed for ('{tag}', 0x{hex(data)}={data})")
    #                     count = -msgcount
    #                     stop = True
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_DATA:
    #                 data_list = args.pop(0)
    #                 print(f"connection_mode::exchange(...) MSG_DATA(cache=0x{hex(data_list)})")
    #                 if self.exchange_data(xlate_out, data_list) < 0:
    #                     print(f"connection_mode::exchange(): data exchange failed")
    #                     count = -msgcount
    #                     stop = True
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_OPEN:
    #                 tag = args.pop(0)
    #                 print(f"connection_mode::exchange(...) MSG_OPEN('{tag}')")
    #                 if self.exchange_open(xlate_out, tag) < 0:
    #                     print(f"connection_mode::exchange(): start group '{tag}' exchange failed")
    #                     count = -msgcount
    #                     stop = True
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #                 continue
    #             elif flag == MESSAGEFLAG.MSG_CLOSE:
    #                 print(f"connection_mode::exchange(...) MSG_CLOSE")
    #                 if self.exchange_close(xlate_out) < 0:
    #                     print(f"connection_mode::exchange(): end group exchange failed")
    #                     count = -msgcount
    #                     stop = True
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #             else:
    #                 print(f"connection_mode::exchange(...) unrecognized message control flag {flag} was ignored")
    #                 new_flag = args.pop(0)
    #                 if new_flag == 0:
    #                     stop = True
    #                 else:
    #                     flag = new_flag
    #
    #         if msgcount != 0:
    #             count = msgcount if msgcount > 0 else -1
    #
    #         if count == 0:
    #             print(f"sending message: length=[{self.transport.get_position()}] buffer=[{self.transport.get_input()}]")
    #             return self.send() == self.transport.get_position()
    #
    #         return -1 if count < 0 and critical else 0

    def server_response(self, flag, *args):
        critical = flag == "MSG_CRITICAL"
        count = 0
        msgcount = 0
        id = None
        stop = False
        args_iter = iter(args)
        try:
            while not stop:
                msgcount += 1
                if flag == "MSG_CRITICAL":
                    critical = True
                    self.debug(9, "message is critical")
                    flag = next(args_iter, None)
                elif flag == "MSG_INITIATE":
                    # Handle message initiation
                    if self.get_mode() == "CM_CLIENT":
                        if self.recv() > 0:
                            self.handle_client_recv()
                            flag = next(args_iter, None)
                    elif self.get_mode() == "CM_SERVER":
                        # Server specific initiation logic here
                        flag = next(args_iter, None)
                elif flag == "MSG_CONTINUE":
                    # Handle message continuation
                    flag = next(args_iter, None)
                elif flag == "MSG_COMPLETE":
                    # Finalize message handling
                    id = next(args_iter, None)
                    flag = next(args_iter, None)
                # Additional cases (MSG_SCHEMA, MSG_TAG, etc.) as per original C++ method
                else:
                    self.warning("Unrecognized message control flag", flag)
                    flag = next(args_iter, None)
                if flag is None:
                    stop = True
        except StopIteration:
            # Handle iteration stopping, implying args were exhausted
            pass

        # Additional logic to finalize the server response
        return count

    def debug(self, level, message, args):
        # Implement debug logging
        msg = "connection/{}: {}".format(self.get_mode_name(), message)
        for a in args:
            msg += " {}".format(a)
        print(f"{level}:{msg}")

    def warning(self, message, args):
        # Implement warning logging
        msg = "connection/{}: {}".format(self.get_mode_name(), message.value)
        for a in args:
            msg += " {}".format(a)
        print(msg)

    def error(self, fmt, args):
        msg = fmt.format(args)
        print("connection/{}: {}".format(self.get_mode_name(), msg.value))

    def get_mode_name(self):
        pass
    

    def info(self, fmt, args):
        msg="connection/{}:".format(self.get_mode_name())
        for a in args:
            msg += " {}".format(a)
        print(msg)

    def exception(self, fmt, *args):
        msg_len = ctypes.c_int()
        msg = "connection/{}: ".format(self.get_mode_name())
        
        ctypes.cdll.msvcrt.sprintf(self.msg, msg.encode('utf-8'))
        msg_len.value = len(msg.encode('utf-8'))
        
        var_args = (ctypes.c_char_p*len(args))()
        for i, arg in enumerate(args):
            var_args[i] = arg.encode('utf-8')
        
        ctypes.cdll.msvcrt.vsprintf(ctypes.byref(self.msg, msg_len), fmt.encode('utf-8'), var_args)
        
        raise RuntimeError(self.msg.value.decode('utf-8'))

    def init(self):
        return self.get_transport().init()

    def option(self, target, command):
        # specifically targeted to server or client
        if target == self.get_mode_name():
            if self.get_mode() == "CM_CLIENT":
                return self.client.option(command)
            elif self.get_mode() == "CM_SERVER":
                return self.server.option(command)
            else:
                return 0

        # specifically target to udp or tcp
        if target == "transport" or target == self.transport.get_transport_name():
            return self.transport.option(command)

        # cache control options
        if target == "readcache":
            return self.read_cache.option(command)
        if target == "writecache":
            return self.write_cache.option(command)

        # local target
        if target == "connection":
            if command == "ignore":
                pass
        else:
            gl_error("connection/connection_mode::option(target='{}', command='{}'): target not recognized".format(target, command))
        return 0

    def update(self, var_map, data_exchange_direction, translator):
        target = var_map.obj
        if not target.is_valid():
            gl_error("connection_mode::update(VARMAP *var=%p, TRANSLATOR *xlate=%p): target '%s' is not valid" % (var_map, translator, var_map.local_name))
            return 0
        
        if data_exchange_direction == DATAEXCHANGEDIRECTION.DXD_READ and var_map.dir == DATAEXCHANGEDIRECTION.DXD_READ:
            if not read_cache.read(var_map, translator):
                gl_warning("connection_mode::update(VARMAP *var=%p, TRANSLATOR *xlate=%p): unable to read/translate data from %s" % (var_map, translator, var_map.remote_name))
            else:
                gl_debug("reading %s from %s" % (var_map.local_name, var_map.remote_name))
        elif data_exchange_direction == DATAEXCHANGEDIRECTION.DXD_WRITE and var_map.dir == DATAEXCHANGEDIRECTION.DXD_WRITE:
            if not write_cache.write(var_map, translator):
                gl_warning("connection_mode::update(VARMAP *var=%p, TRANSLATOR *xlate=%p): unable to write/translate data for %s" % (var_map, translator, var_map.remote_name))
            else:
                gl_debug("writing %s to %s" % (var_map.local_name, var_map.remote_name))
        
        return 1

    def update(self, var_list, tag, xlate):
        count = 0
        v = var_list.get_first()
        while v is not None:
            if not self.update_variable(v, DATAEXCHANGEDIRECTION.DXD_WRITE, xlate):
                return -1
            else:
                count += 1
            v = v.next
        if count > 0:
            print("write cache dump...")
            write_cache.dump()
            id_ = 0
            if self.client_initiated(
                'MSG_INITIATE',
                'MSG_TAG', "method", tag,
                'MSG_OPEN', "data",
                    'MSG_DATA', write_cache,
                'MSG_CLOSE',
                'MSG_COMPLETE', id_,
            ) < 0:
                return -1
            if self.server_response(
                'MSG_INITIATE',
                'MSG_TAG', "result", tag,
                'MSG_OPEN', "data",
                    'MSG_DATA', read_cache,
                'MSG_CLOSE',
                'MSG_COMPLETE', id_,
            ) < 0:
                return ignore_error > 0
            count = 0
            v = var_list.get_first()
            while v is not None:
                if not self.update_variable(v, DATAEXCHANGEDIRECTION.DXD_READ, xlate):
                    return -1
                else:
                    count += 1
                v = v.next
            print("read cache dump...")
            read_cache.dump()
        return count
    
    def client_initiated(self, flag, *args):
        critical = flag == MESSAGEFLAG.MSG_CRITICAL
        count = 0
        msgcount = 0
        id = None
        stop = False
        i = 0

        while not stop:
            msgcount += 1

            if flag == MESSAGEFLAG.MSG_CRITICAL:
                critical = True
                print("connection_mode::exchange() message is critical")
                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            if flag == MESSAGEFLAG.MSG_INITIATE:
                seqnum += 1
                if self.exchange(xlate_out, critical) < 0:
                    print("connection_mode::exchange(): transport status control error")
                    count = -msgcount
                    stop = True

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            if flag == MESSAGEFLAG.MSG_CONTINUE:
                if self.exchange(xlate_out) < 0:
                    print("connection_mode::exchange(): transport status control error")
                    count = -msgcount
                    stop = True

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            if flag == MESSAGEFLAG.MSG_COMPLETE:
                id = args[i]
                i += 1
                if self.exchange(xlate_out, id) < 0:
                    print("connection_mode::exchange(): transport status control error")
                    count = -msgcount
                    stop = True

                msgcount = 0  # signal message is complete and should be handled
                count = msgcount
                stop = True
                continue

            if flag == MESSAGEFLAG.MSG_SCHEMA:
                dir = args[i]
                i += 1
                print(f"connection_mode::exchange(...) MSG_SCHEMA('{dir}',cache=0x{hex(read_cache) if dir == DATAEXCHANGEDIRECTION.DXD_READ else hex(write_cache)})")
                if dir == DATAEXCHANGEDIRECTION.DXD_READ:
                    if self.exchange_schema(xlate_out, read_cache) < 0:
                        print("exchange(): schema exchange failed")
                        count = -msgcount
                        stop = True
                elif dir == DATAEXCHANGEDIRECTION.DXD_WRITE:
                    if self.exchange_schema(xlate_out, write_cache) < 0:
                        print("exchange(): schema exchange failed")
                        count = -msgcount
                        stop = True
                else:
                    print("exchange(): schema exchange failed, invalid data direction supplied")
                    count = -msgcount
                    stop = True

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            if flag == MESSAGEFLAG.MSG_TAG:
                tag = args[i]
                i += 1
                value = args[i]
                i += 1
                print(f"connection_mode::exchange(...) MSG_TAG('{tag}','{value}')")
                if self.exchange(xlate_out, tag, value) < 0:
                    print(f"connection_mode::exchange(): tagged value exchange failed for ('{tag}','{value}')")
                    count = -msgcount
                    stop = True

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            if flag == MESSAGEFLAG.MSG_STRING:
                tag = args[i]
                i += 1
                length = args[i]
                i += 1
                buf = args[i]
                i += 1
                print(f"client_initiated(...) MSG_STRING('{tag}', {length}, '{buf}')")
                if self.exchange(xlate_out, tag, length, buf) < 0:
                    print(f"connection_mode::exchange(): string value exchange failed for ('{tag}', {length}, '{buf}')")
                    count = -msgcount
                    stop = True

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            if flag == MESSAGEFLAG.MSG_REAL:
                tag = args[i]
                i += 1
                data = args[i]
                i += 1
                print(f"exchange(...) MSG_REAL('{tag}', 0x{hex(data)}={data})")
                if self.exchange(xlate_out, tag, data) < 0:
                    print(f"connection_mode::exchange(): double value exchange failed for ('{tag}', 0x{hex(data)}={data})")
                    count = -msgcount
                    stop = True

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            if flag == MESSAGEFLAG.MSG_INTEGER:
                tag = args[i]
                i += 1
                data = args[i]
                i += 1
                print(f"connection_mode::exchange(...) MSG_INTEGER('{tag}', 0x{hex(data)}={data})")
                if self.exchange(xlate_out, tag, data) < 0:
                    print(f"connection_mode::exchange(): double value exchange failed for ('{tag}', 0x{hex(data)}={data})")
                    count = -msgcount
                    stop = True

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            if flag == MESSAGEFLAG.MSG_DATA:
                cache_list = args[i]
                i += 1
                print(f"connection_mode::exchange(...) MSG_DATA(cache=0x{hex(cache_list)})")
                if self.exchange_data(xlate_out, cache_list) < 0:
                    print("connection_mode::exchange(): data exchange failed")
                    count = -msgcount
                    stop = True

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            if flag == MESSAGEFLAG.MSG_OPEN:
                tag = args[i]
                i += 1
                print(f"connection_mode::exchange(...) MSG_OPEN('{tag}')")
                if self.exchange_open(xlate_out, tag) < 0:
                    print(f"connection_mode::exchange(): start group '{tag}' exchange failed")
                    count = -msgcount
                    stop = True

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            if flag == MESSAGEFLAG.MSG_CLOSE:
                print("connection_mode::exchange(...) MSG_CLOSE")
                if self.exchange_close(xlate_out) < 0:
                    print("connection_mode::exchange(): end group exchange failed")
                    count = -msgcount
                    stop = True

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag
                continue

            else:
                print(f"connection_mode::exchange(...) unrecognized message control flag {flag} was ignored")

                new_flag = args[i]
                i += 1
                if new_flag == 0:
                    stop = True
                else:
                    flag = new_flag

        if msgcount != 0:
            count = msgcount if msgcount > 0 else -1

        if count == 0:
            print(f"sending message: length=[{transport.get_position()}] buffer=[{transport.get_input()}]")
            return self.send() == transport.get_position()

        return -1 if count < 0 and critical else 0

    def create_cache(self, var_map: VARMAP) -> cacheitem:
        if var_map.dir == DATAEXCHANGEDIRECTION.DXD_READ:
            item = self.read_cache.find_item(var_map)
            if item is not None:
                return item
            else:
                return self.read_cache.add_item(var_map)
        elif var_map.dir == DATAEXCHANGEDIRECTION.DXD_WRITE:
            item = self.write_cache.find_item(var_map)
            if item is not None:
                return item
            else:
                return self.write_cache.add_item(var_map)
        else:
            return None
    


