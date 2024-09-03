# from enum import Enum
#
# from gov_pnnl_goss.gridlab.gldcore.Class import PASSCONFIG, PropertyType
# from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_publish_loadmethod, gl_globalstoptime, TS_INVALID, TS_NEVER
#
#
# def fncs_hex(c):
#     if c < 10:
#         return c + '0'
#     elif c < 16:
#         return c - 10 + 'A'
#     else:
#         return '?'
#
#
# def fncs_unhex(h):
#     if '0' <= h <= '9':
#         return ord(h) - ord('0')
#     elif 'A' <= h <= 'F':
#         return ord(h) - ord('A') + 10
#     elif 'a' <= h <= 'f':
#         return ord(h) - ord('a') + 10
#     else:
#         return '?'
#
#
# def fncs_to_hex(out, max, _in, _len):
#     hlen = 0
#     for n in range(_len):
#         byte = _in[n]
#         lo = _in[n] & 0xf
#         hi = (_in[n] >> 4) & 0xf
#         out.append(fncs_hex(lo))
#         out.append(fncs_hex(hi))
#         hlen += 2
#         if hlen >= max:
#             return -1
#     out.append('\0')
#     return hlen
#
#
# def fncs_from_hex(buf, _len, hex, hexlen):
#     p = buf
#     lo = None
#     hi = None
#     c = None
#     n = 0
#     while n < hexlen and hex != '\0':
#         c = fncs_unhex(hex)
#         if c == -1:
#             return -1
#         lo = c & 0xf
#         c = fncs_unhex(hex[1])
#         hi = (c << 4) & 0xf0
#         if c == -1:
#             return -1
#         p = hi | lo
#         p += 1
#         hex += 2
#         if ( n /2) >= _len:
#             return -1
#     return n
#
#
# def outgoing_fncs_function(_from, to, funcName, funcClass, data, length):
#     result = -1
#     rclass = funcClass
#     lclass = _from
#     hexlen = 0
#     relay = find_fncs_function(funcClass, funcName)
#     if relay is None:
#         raise Exception \
#             (f"fncs_msg::outgoing_route_function: the relay function for function name {funcName} could not be found.")
#     if relay.drtn != DXD_WRITE:
#         raise Exception \
#             (f"fncs_msg::outgoing_fncs_function: the relay function for the function name {funcName} could not be found.")
#     message = ""
#     msglen = 0
#     if to is None or _from is None:
#         raise Exception("from objects and to objects must be named.")
#     hexlen = fncs_to_hex(message, 3000, data, length)
#     if hexlen > 0:
#         payload = f'"{ {"from": "{_from}", "to": "{to}", "function" :"{funcName}", "data" :"{message}", "data length" :"{length}"} }'
#         key = str(relay.remotename)
#         if relay.ctype == CT_PUBSUB:
#             fncs.publish(key, payload)
#         elif relay.ctype == CT_ROUTE:
#             sender = str(_from)
#             recipient = str(to)
#             fncs.route(sender, recipient, key, payload)
#
#
# def fncs_clocks_update(ptr, t1):
#     my = ptr
#     return my.clk_update(t1)
#
#
# def fncs_d_interupdate(ptr, d_interval_counter, t0, dt):
#     my = fncs_msg(ptr)
#     return my.delta_inter_update(d_interval_counter, t0, dt)
#
#
# def fncs_d_clock_update(ptr, t1, timestep, sysmode):
#     my = ptr
#     return my.delta_clock_update(t1, timestep, sysmode)
#
#
# def fncs_send_die():
#     a = 0
#     exit_code = gld_global("exit_code")
#     if exit_code.get_int16() != 0:
#         die()
#
#
# def process_message(message_type, vmap):
#     if message_type == MT_GENERAL:
#         result = publish_variables(vmap[5])
#         if result == 0:
#             return "ts_invalid"
#
#         result = subscribe_variables(vmap[5])
#         if result == 0:
#             return "ts_invalid"
#
#
# def convert_to_python(message_type):
#     if message_type == MT_JSON:
#         result = subscribe_json_variables()
#         if result == 0:
#             return TS_INVALID
#
#
# def convert_message_type_to_json(t1):
#     if message_type == MT_JSON:
#         t2 = t1 + 1
#         return t2
#
#
# def convert_to_snake_case(t1, last_delta_fncs_time, initial_sim_time, sysmode, timestep):
#     if t1 > last_delta_fncs_time:
#         fncs_time = 0
#         t = 0
#         dt = 0
#         dt = (t1 - float(initial_sim_time)) * 1000000000.0
#         if sysmode == "SM_EVENT":
#             t = int((dt + (1000000000.0 / 2.0)) - ((dt + (1000000000.0 / 2.0)) % 1000000000.0))
#         else:
#             t = int((dt + (float(timestep) / 2.0)) - ((dt + (float(timestep) / 2.0)) % float(timestep)))
#         fncs.update_time_delta(int(timestep))
#         fncs_time = fncs.time_request(t)
#         if sysmode == "SM_EVENT":
#             exit_deltamode = True
#             rv = "SM_EVENT"
#         if fncs_time != t:
#             print \
#                 ("fncs_msg::delta_clock_update: Cannot return anything other than the time GridLAB-D requested in deltamode.")
#             return "SM_ERROR"
#         else:
#             last_delta_fncs_time = float(fncs_time) / 1000000000.0 + float(initial_sim_time)
#
#
# def convert_to_python(t1, gl_globalstoptime, gl_globalclock):
#     if (t1 > gl_globalstoptime and gl_globalclock < gl_globalstoptime):
#         t1 = gl_globalstoptime
#
#
#
#
# # Define the FNCSTYPE enum
# class FNCSTYPE(Enum):
#     FT_VOID = 0
#     FT_LIST = 1
#     FT_REAL = 2
#     FT_INTEGER = 3
#     FT_STRING = 4
#
# # Define the MESSAGETYPE enum
# class MESSAGETYPE(Enum):
#     MT_GENERAL = 0
#     MT_JSON = 1
#
# # Define the FNCSLIST class
# class FNCSLIST:
#     def __init__(self, type, tag, real=None, integer=None, list=None, st="", parent=None):
#         self.type = type
#         self.tag = tag
#         self.real = real
#         self.integer = integer
#         self.list = list
#         self.st = st
#         self.parent = parent
#         self.next = None
#
#     def set_real(self, real):
#         self.type = FNCSTYPE.FT_REAL
#         self.real = real
#
#     def set_integer(self, integer):
#         self.type = FNCSTYPE.FT_INTEGER
#         self.integer = integer
#
#     def set_list(self, list):
#         self.type = FNCSTYPE.FT_LIST
#         self.list = list
#
# # Usage examples:
# # fncs_type = FNCSTYPE.FT_REAL
# # message_type = MESSAGETYPE.MT_JSON
# # fncs_list = FNCSLIST(fncs_type, "example_tag")
#
#
#
# class JsonProperty:
#     def __init__(self, obj_name, obj_prop):
#         self.object_name = obj_name
#         self.object_property = obj_prop
#         self.is_header = obj_prop == "parent"
#         self.prop = None
#         self.obj = None
#         self.hdr_val = ""
#
# class FunctionsRelay:
#     def __init__(self, localclass, localcall, remoteclass, remotename, route, xlate, drtn, ctype):
#         self.localclass = localclass
#         self.localcall = localcall
#         self.remoteclass = remoteclass
#         self.remotename = remotename
#         self.route = route
#         self.xlate = xlate
#         self.next = None
#         self.drtn = drtn
#         self.ctype = ctype
#
#
#
# class LastValueBuffer:
#     def __init__(self, value):
#         self.value = value
#
#     def set(self, value):
#         self.value = value
#
#     def get_complex(self):
#         return self.value
#
#     def get_double(self):
#         return self.value
#
#     def get_integer(self):
#         return self.value
#
#     def get_string(self):
#         return self.value
#
#     def get_bool(self):
#         return self.value
#
#
# class gld_property:
#     def __init__(self, obj_name, prop_name=None):
#         self.obj_name = obj_name
#         self.prop_name = prop_name
#         self.object = None
#         self.value = None
#         self.prop = None
#
#     def is_valid(self):
#         if self.prop:
#             return True
#         elif self.prop_name:
#             self.prop = gl_property(self.obj_name, self.prop_name)
#             if self.prop.is_valid():
#                 return True
#         return False
#
#     def get_object(self):
#         if self.prop:
#             return self.prop.get_object()
#         return None
#
#     def get_value(self):
#         if self.prop:
#             self.value = self.prop.get_value()
#         return self.value
#
#
# def fncs_send_die():
#     try:
#         import fncs
#         fncs.finalize()
#     except ImportError:
#         pass
#
#
# class FncsMsg:
#
#     def __init__(self, module):
#         self.version = 0.0  # Assuming double for version
#         self.port = None  # Initialize to None, set to string later
#         self.header_version = None  # Initialize to None, set to string later
#         self.hostname = None  # Initialize to None, set to string later
#         self.configFile = ""  # Initialize as an empty string
#
#         # TODO: Add published properties here
#
#         self.inFunctionTopics = []  # Initialize as an empty list
#         self.vmap = [None] * 14  # Initialize as a list of 14 elements, set varmap objects later
#         self.last_approved_fncs_time = 0  # Assuming TIMESTAMP as an integer
#         self.initial_sim_time = 0  # Assuming TIMESTAMP as an integer
#         self.gridappsd_publish_time = 0  # Assuming TIMESTAMP as an integer
#         self.last_delta_fncs_time = 0.0  # Assuming double
#         self.exitDeltamode = False  # Initialize as False
#
#         # TODO: Add other properties here as needed
#
#         self.message_type = None  # Initialize to None, set to enumeration value later
#
#         # Implement required methods/functions here
#         self.real_time_gridappsd_publish_period = 0  # Assuming int32
#         self.aggregate_pub = False  # Initialize as False
#         self.aggregate_sub = False  # Initialize as False
#
#
#         self.subscribe_json_data = {}
#
#         self.publish_json_config = {}  # Initialize as an empty dictionary
#         self.publish_json_data = {}  # Initialize as an empty dictionary
#         self.subscribe_json_data = {}  # Initialize as an empty dictionary
#         self.publish_json_key = ""  # Initialize as an empty string
#         self.subscribe_json_key = ""  # Initialize as an empty string
#         self.vjson_publish_gld_property_name = []  # Initialize as an empty list
#
#         # NOTE: In Python, we don't have to define the data types explicitly as in C++
#         # Json::Value is not needed, you can use dictionaries and lists directly
#
#         self.fncs_step = 0  # Initialize to an appropriate value (e.g., 0)
#
#
#         self.oclass = gld_class.create(module, "fncs_msg", sizeof(fncs_msg),
#                                        PASSCONFIG.PC_AUTOLOCK | PASSCONFIG.PC_PRETOPDOWN | PASSCONFIG.PC_BOTTOMUP | PASSCONFIG.PC_POSTTOPDOWN | PASSCONFIG.PC_OBSERVER)
#         if self.oclass is None:
#             raise "connection/fncs_msg::fncs_msg(MODULE*): unable to register class connection:fncs_msg"
#         else:
#             self.oclass.trl = TRL_UNKNOWN
#
#         self.defaults = self
#         if gl_publish_variable(
#                 self.oclass,
#                 PropertyType.PT_double, "version", get_version_offset(), PropertyType.PT_DESCRIPTION, "fncs_msg version",
#                 PropertyType.PT_enumeration, "message_type", PADDR(self.message_type), PropertyType.PT_DESCRIPTION,
#                 "set the global_property_types of message format you wish to construct",
#                 PropertyType.PT_KEYWORD, "GENERAL", enumeration(MT_GENERAL), PropertyType.PT_DESCRIPTION,
#                 "use this for sending a general fncs topic/value pair",
#                 PropertyType.PT_KEYWORD, "JSON", enumeration(MT_JSON), PropertyType.PT_DESCRIPTION,
#                 "use this for wanting to send a bundled json formatted message in a single topic",
#                 PropertyType.PT_int32, "gridappd_publish_period", PADDR(self.real_time_gridappsd_publish_period), PropertyType.PT_DESCRIPTION,
#                 "use this with json bundling to set the period [s] at which data is published.",
#                 PropertyType.PT_bool, "aggregate_publications", PADDR(self.aggregate_pub), PropertyType.PT_DESCRIPTION,
#                 "enable FNCS flag to aggregate publications",
#                 PropertyType.PT_bool, "aggregate_subscriptions", PADDR(self.aggregate_sub), PropertyType.PT_DESCRIPTION,
#                 "enable FNCS flag to aggregate subscriptions",
#                 None
#         ) < 1:
#             raise "connection/fncs_msg::fncs_msg(MODULE*): unable to publish properties of connection:fncs_msg"
#         if not gl_publish_loadmethod(self.oclass, "route", loadmethod_fncs_msg_route):
#             raise "connection/fncs_msg::fncs_msg(MODULE*): unable to publish route method of connection:fncs_msg"
#         if not gl_publish_loadmethod(self.oclass, "option", loadmethod_fncs_msg_option):
#             raise "connection/fncs_msg::fncs_msg(MODULE*): unable to publish option method of connection:fncs_msg"
#         if not gl_publish_loadmethod(self.oclass, "publish", loadmethod_fncs_msg_publish):
#             raise "connection/fncs_msg::fncs_msg(MODULE*): unable to publish publish method of connection:fncs_msg"
#         if not gl_publish_loadmethod(self.oclass, "subscribe", loadmethod_fncs_msg_subscribe):
#             raise "connection/fncs_msg::fncs_msg(MODULE*): unable to publish subscribe method of connection:fncs_msg"
#         if not gl_publish_loadmethod(self.oclass, "configure", loadmethod_fncs_msg_configure):
#             raise "connection/fncs_msg::fncs_msg(MODULE*): unable to publish configure method of connection:fncs_msg"
#
#     def sync(self, t1):
#         result = 0
#         t2 = None
#         if t1 < gl_globalstoptime:
#             result = self.publish_variables(self.vmap[6])
#             if result == 0:
#                 return TS_INVALID
#             result = self.subscribe_variables(self.vmap[6])
#             if result == 0:
#                 return TS_INVALID
#         if self.message_type == MT_GENERAL:
#             return TS_NEVER
#         elif self.message_type == MT_JSON:
#             pass
#         return TS_INVALID
#
#     def postsync(self, t1):
#         pass
#
#     def prenotify(self, p, v):
#         pass
#
#     def postnotify(self, p, v):
#         pass
#
#     def delta_inter_update(self, delta_iteration_counter, t0, dt):
#         pass
#
#     def delta_clock_update(self, t1, timestep, sysmode):
#         pass
#
#     def clk_update(self, t1):
#         pass
#
#     def finalize(self):
#         nvecsize = len(self.vjson_publish_gld_property_name)
#         for isize in range(nvecsize):
#             del self.vjson_publish_gld_property_name[isize].obj
#             del self.vjson_publish_gld_property_name[isize].prop
#         return 1
#
#     def get_varmapindex(self, name):
#         pass
#
#     def fncs_link(self, value, comtype):
#         pass
#
#     def parse_fncs_function(self, value, comtype):
#         pass
#
#     def publish_fncsjson_link(self):
#         pass
#
#
#     def create_fncs_msg(self):
#         self.version = 1.0
#         self.message_type = MT_GENERAL
#         self.add_clock_update(self,fncs_clocks_update)
#         self.register_object_interupdate(self, fncs_dInterupdate)
#         self.register_object_deltaclockupdate(self, fncs_dClockupdate)
#
#         for n in range(1, 14):
#             self.vmap[n] = varmap()
#         self.port = ""
#         self.header_version = ""
#         self.hostname = ""
#         self.in_function_topics = []
#         self.real_time_gridappsd_publish_period = 3
#
#         self.aggregate_pub = False
#         self.aggregate_sub = False
#
#         return 1
#
#
#     def publish(self, value):
#         rv = 0
#         rv = fncs_link(value, CT_PUBSUB)
#         return rv
#
#     def subscribe(self, value):
#         rv = 0
#         rv = fncs_link(value, CT_PUBSUB)
#         return rv
#
#     def route(self, value):
#         rv = 0
#         rv = fncs_link(value, CT_ROUTE)
#         return rv
#
#     def precommit(self, t1):
#         result = 0
#
#         if self.message_type == 'MT_GENERAL':
#             self.incoming_fncs_function()
#
#             if t1 < self.gl_globalstoptime:
#                 result = self.publish_variables(self.vmap[4])
#                 if result == 0:
#                     return result
#
#                 result = self.subscribe_variables(self.vmap[4])
#                 if result == 0:
#                     return result
#
#         return 1
#
#     def presync(self, t1):
#         result = 0
#         if self.message_type == MT_GENERAL:
#             result = self.publish_variables(self.vmap[5])
#             if result == 0:
#                 return TS_INVALID
#             result = self.subscribe_variables(self.vmap[5])
#             if result == 0:
#                 return TS_INVALID
#         elif self.message_type == MT_JSON:
#             result = self.subscribe_json_variables()
#             if result == 0:
#                 return TS_INVALID
#         return TS_NEVER
#
#
#
#     def plc(self, t1):
#         result = 0
#         if t1 < self.gl_global_stop_time:
#             result = self.publish_variables(self.v_map[12])
#             if result == 0:
#                 return TS_INVALID
#
#             result = self.subscribe_variables(self.v_map[12])
#             if result == 0:
#                 return TS_INVALID
#         return TS_NEVER
#
#
#
#     def sync(self, t1):
#         result = 0
#         t2 = None
#         if t1 < self.gl_globalstoptime:
#             result = self.publish_variables(self.vmap[6])
#             if result == 0:
#                 return "TS_INVALID"
#
#             result = self.subscribe_variables(self.vmap[6])
#             if result == 0:
#                 return "TS_INVALID"
#
#         if self.message_type == "MT_GENERAL":
#             return "TS_NEVER"
#         elif self.message_type == "MT_JSON":
#             t2 = t1 + 1
#             return t2
#
#         return "TS_INVALID"
#
#
#
#     def post_sync(self, t1):
#         result = 0
#         if t1 < self.gl_global_stop_time:
#             result = self.publish_variables(self.v_map[7])
#             if result == 0:
#                 return TS_INVALID
#             result = self.subscribe_variables(self.v_map[7])
#             if result == 0:
#                 return TS_INVALID
#         return TS_NEVER
#
#     def prenotify(self, p, v):
#         result = 0
#         result = self.publish_variables(v_map[9])
#         if result == 0:
#             return result
#         result = self.subscribe_variables(v_map[9])
#         if result == 0:
#             return result
#         return 1
#
#     def postnotify(self, p, v):
#         result = 0
#         result = self.publish_variables(vmap[10])
#         if result == 0:
#             return result
#         result = self.subscribe_variables(vmap[10])
#         if result == 0:
#             return result
#         return 1
#
#     def delta_inter_update(self, delta_iteration_counter, t0, dt):
#         result = 0
#         dclock = gld_global("deltaclock")
#         if not dclock.is_valid():
#             gl_error("fncs_msg::deltaInterUpdate: Unable to find global deltaclock!")
#             return SM_ERROR
#         if dclock.get_int64() > 0:
#             if delta_iteration_counter == 0:
#                 result = self.publish_variables(vmap[8])
#                 if result == 0:
#                     return SM_ERROR
#                 result = self.subscribe_variables(vmap[8])
#                 if result == 0:
#                     return SM_ERROR
#                 self.incoming_fncs_function()
#                 result = self.publish_variables(vmap[4])
#                 if result == 0:
#                     return SM_ERROR
#                 result = self.subscribe_variables(vmap[4])
#                 if result == 0:
#                     return SM_ERROR
#                 return SM_DELTA_ITER
#             if delta_iteration_counter == 1:
#                 result = self.publish_variables(vmap[5])
#                 if result == 0:
#                     return SM_ERROR
#                 result = self.subscribe_variables(vmap[5])
#                 if result == 0:
#                     return SM_ERROR
#                 return SM_DELTA_ITER
#             if delta_iteration_counter == 2:
#                 result = self.publish_variables(vmap[12])
#                 if result == 0:
#                     return SM_ERROR
#                 result = self.subscribe_variables(vmap[12])
#                 if result == 0:
#                     return SM_ERROR
#                 return SM_DELTA_ITER
#             if delta_iteration_counter == 3:
#                 result = self.publish_variables(vmap[6])
#                 if result == 0:
#                     return SM_ERROR
#                 result = self.subscribe_variables(vmap[6])
#                 if result == 0:
#                     return SM_ERROR
#                 return SM_DELTA_ITER
#             if delta_iteration_counter == 4:
#                 result = self.publish_variables(vmap[7])
#                 if result == 0:
#                     return SM_ERROR
#                 result = self.subscribe_variables(vmap[7])
#                 if result == 0:
#                       return SM_ERROR
#         return SM_EVENT
#
#
#     def delta_clock_update(self, t1, timestep, sysmode):
#         rv = "SM_DELTA"
#         if t1 > self.last_delta_fncs_time:
#             fncs_time = 0
#             t = 0
#             dt = (t1 - float(self.initial_sim_time)) * 1000000000.0
#             if sysmode == "SM_EVENT":
#                 t = (dt + (1000000000.0 / 2.0)) - (dt + (1000000000.0 / 2.0)) % 1000000000.0
#             else:
#                 t = (dt + (float(timestep) / 2.0)) - (dt + (float(timestep) / 2.0)) % float(timestep)
#             fncs.update_time_delta(float(timestep))
#             fncs_time = fncs.time_request(t)
#             if sysmode == "SM_EVENT":
#                 self.exit_delta_mode = True
#                 rv = "SM_EVENT"
#             if fncs_time != t:
#                 gl_error("fncs_msg::delta_clock_update: Cannot return anything other than the time GridLAB-D requested in deltamode.")
#                 return "SM_ERROR"
#             else:
#                 self.last_delta_fncs_time = float(fncs_time) / 1000000000.0 + float(self.initial_sim_time)
#         return rv
#
#     def clk_update(self, t1):
#
#         fncs_time = 0
#         if self.exit_delta_mode:
#             if HAVE_FNCS:
#                 fncs.update_time_delta(self.fncs_step)
#             self.exit_delta_mode = False
#
#         if t1 > self.last_approved_fncs_time:
#             if self.gl_global_clock == self.gl_global_stop_time:
#                 if HAVE_FNCS:
#                     fncs.finalize()
#                 return TS_NEVER
#             elif t1 > self.gl_global_stop_time and self.gl_global_clock < self.gl_global_stop_time:
#                 t1 = self.gl_global_stop_time
#
#             if HAVE_FNCS:
#                 t = 0
#                 t = (fncs.time)((t1 - self.initial_sim_time)*1000000000)
#                 fncs_time = ((TIMESTAMP)fncs.time_request(t))/1000000000 + self.initial_sim_time
#
#             if fncs_time <= self.gl_global_clock:
#                 gl_error("fncs_msg::clock_update: Cannot return the current time or less than the current time.")
#                 return TS_INVALID
#             else:
#                 self.last_approved_fncs_time = fncs_time
#                 t1 = fncs_time
#
#         return t1
#
#     def finalize(self):
#         n_vec_size = len(self.v_json_publish_gld_property_name)
#         for i_size in range(n_vec_size):
#             del self.v_json_publish_gld_property_name[i_size].obj
#             del self.v_json_publish_gld_property_name[i_size].prop
#         return 1
#
#     def get_varmap_index(self, name):
#         varmap_name = ["", "allow", "forbid", "init", "precommit", "presync", "sync", "postsync", "commit", "prenotify", "postnotify", "finalize", "plc", "term"]
#         for n in range(1, 14):
#             if varmap_name[n] == name:
#                 return n
#         return 0
#
#     def fncs_link(self, value, comtype):
#         rv = 0
#         n = 0
#         command = ""
#         argument = ""
#         mp = None
#
#         if sscanf(value, "%[^:]:%[^\n]", command, argument) == 2:
#             if strncmp(command, "init", 4) == 0:
#                 gl_warning("fncs_msg::publish: It is not possible to pass information at init time with fncs. communication is ignored")
#                 rv = 1
#             elif strncmp(command, "function", 8) == 0:
#                 rv = parse_fncs_function(argument, comtype)
#             else:
#                 n = get_varmapindex(command)
#                 if n != 0:
#                     rv = vmap[n].add(argument, comtype)
#         else:
#             gl_error("fncs_msg::publish: Unable to parse input %s.", value)
#             rv = 0
#         return rv
#
#     def parse_fncs_function(self, value, comtype):
#         rv = 0
#         local_class = ""
#         local_func_name = ""
#         direction = ""
#         remote_class_name = ""
#         remote_func_name = ""
#         topic = ""
#         fclass = None
#         flocal = None
#
#         if sscanf(value, "%[^/]/%[^-<>\t ]%*[\t ]%[-<>]%*[\t ]%[^\n]", local_class, local_func_name, direction, topic) != 4:
#             gl_error("fncs_msg::parse_fncs_function: Unable to parse input %s.", value)
#             return rv
#
#         fclass = callback.class_getname(local_class)
#
#         if fclass is None:
#             gl_error("fncs_msg::parse_fncs_function(const char *spec='%s'): local class '%s' does not exist", value, local_class)
#             return rv
#
#         flocal = callback.function.get(local_class, local_func_name)
#
#         if direction == "->":
#             if flocal is not None:
#                 gl_warning("fncs_msg::parse_fncs_function(const char *spec='%s'): outgoing call definition of '%s' overwrites existing function definition in class '%s'", value, local_func_name, local_class)
#
#             remote_class_name, remote_func_name = sscanf(topic, "%[^/]/%[^\n]")
#
#             flocal = add_fncs_function(self, local_class, local_func_name, remote_class_name, remote_func_name, None, DXD_WRITE, comtype)
#
#             if flocal is None:
#                 return rv
#
#             rv = callback.function.define(fclass, local_func_name, flocal) != None
#             if rv == 0:
#                 gl_error("fncs_msg::parse_fncs_function(const char *spec='%s'): failed to define the function '%s' in local class '%s'.", value, local_func_name, local_class)
#                 return rv
#         elif direction == "<-":
#             if flocal is None:
#                 gl_error("fncs_msg::parse_fncs_function(const char *spec='%s'): local function '%s' is not valid.", value, local_func_name)
#                 return 0
#
#             flocal = add_fncs_function(self, local_class, local_func_name, "", topic, None, DXD_READ, comtype)
#             if flocal is None:
#                 rv = 1
#
#         return rv
#
#     def publish_fncsjson_link(self):
#         if self.publish_json_config is None:
#             gl_warning(" publish json configure is empty!!! \n")
#             return 1
#
#         self.vjson_publish_gld_property_name.clear()
#         gld_property = None
#         for it in self.publish_json_config:
#             gld_object_name = it
#             gld_property_name = ""
#             gld_obj_property_name = ""
#
#             n_size = len(self.publish_json_config[gld_object_name])
#             for i_size in range(n_size):
#                 gld_property_name = self.publish_json_config[gld_object_name][i_size]
#                 gld_property = JsonProperty(gld_object_name, gld_property_name)
#                 self.vjson_publish_gld_property_name.append(gld_property)
#
#         return 1
#
#     def subscribe_json_variables(self):
#         # In this function, need to consider the gl_property resolve problem
#
#         # Throw a warning inside subscribe_json_variables() and return 0
#         gridlabd.warning("fncs_msg::subscribeJsonVariables(): Warning message")
#
#         values = []
#         obj = gridlabd.OBJECTHDR(self)
#         buffer = [""] * 1024
#         simName = gridlabd.gl_name(obj, buffer, 1023)
#         skey = f"{simName}/fncs_input"
#
#         # Mocked values, replace with actual FNCS code
#         values = self.mock_fncs_get_values(skey)
#
#         valStream = "[" + ", ".join(values) + "]"
#         gridlabd.gl_verbose(
#             f"fncs_msg::subscribeJsonVariables(), skey: {skey}, reading json data as string: {valStream}")
#
#         for value in values:
#             if not value:
#                 continue
#
#             subscribe_json_data_full = json.loads(value)
#
#             simNameStr = str(simName)
#             if simNameStr not in subscribe_json_data_full:
#                 gridlabd.gl_warning(
#                     f"fncs_msg::subscribeJsonVariables(), the simName: {simNameStr} is not a member in the subscribed json data!!")
#                 return 1
#             else:
#                 self.subscribe_json_data = subscribe_json_data_full[simNameStr]
#
#             for gldObjectName, gldObjectProperties in self.subscribe_json_data.items():
#                 for gldPropertyName, _ in gldObjectProperties.items():
#                     gldObjPropertyName = f"{gldObjectName}.{gldPropertyName}"
#                     gldpro_obj = gridlabd.gld_property(gldObjPropertyName)
#
#                     if gldpro_obj.is_valid():
#                         sub_value = self.subscribe_json_data[gldObjectName][gldPropertyName]
#
#                         if isinstance(sub_value, int) and gldpro_obj.is_integer():
#                             gldpro_obj.setp(sub_value)
#                             gridlabd.gl_verbose(
#                                 f"fncs_msg::subscribeJsonVariables(): {gldObjPropertyName} is set value with int: {sub_value}")
#                         elif isinstance(sub_value, float) and gldpro_obj.is_double():
#                             gldpro_obj.setp(sub_value)
#                             gridlabd.gl_verbose(
#                                 f"fncs_msg::subscribeJsonVariables(): {gldObjPropertyName} is set value with double: {sub_value}")
#                         elif isinstance(sub_value, str) and (
#                                 gldpro_obj.is_complex() or gldpro_obj.is_character() or gldpro_obj.is_enumeration()):
#                             valueBuf = sub_value[:1023]  # Truncate to 1023 characters
#                             gldpro_obj.from_string(valueBuf)
#                             gridlabd.gl_verbose(
#                                 f"fncs_msg::subscribeJsonVariables(): {gldObjPropertyName} is set value with : {sub_value}")
#                         else:
#                             gridlabd.gl_error(
#                                 f"fncs_msg::fncs json subscribe: fncs global_property_types does not match property global_property_types: {gldObjPropertyName}")
#                             return 0
#                     else:
#                         gridlabd.gl_warning(
#                             f"connection: local variable '{gldObjPropertyName}' cannot be resolved. The local variable will not be updated.")
#
#         return 1
#
#     def publish_json_variables(self):
#         gldpro_obj = None
#         nsize = len(vjson_publish_gld_property_name)
#         nvecsize = len(vjson_publish_gld_property_name)
#         vecidx = 0
#
#         obj = gridlabd.OBJECTHDR(self)
#         buffer = [""] * 1024
#         simName = gridlabd.gl_name(obj, buffer, 1023)
#
#         # Clean the JSON publish data first
#         self.publish_json_data.clear()
#         self.publish_json_data[simName] = {}
#         complex_val = ""
#
#         for isize in range(nsize):
#             if vjson_publish_gld_property_name[isize].object_name not in self.publish_json_data[simName] and vjson_publish_gld_property_name[isize].prop.is_valid():
#                 self.publish_json_data[simName][vjson_publish_gld_property_name[isize].object_name] = {}
#
#             if not vjson_publish_gld_property_name[isize].is_header:
#                 gldpro_obj = vjson_publish_gld_property_name[isize].prop
#                 if gldpro_obj.is_valid():
#                     if gldpro_obj.is_double():
#                         self.publish_json_data[simName][vjson_publish_gld_property_name[isize].object_name][vjson_publish_gld_property_name[isize].object_property] = gldpro_obj.get_double()
#                     elif gldpro_obj.is_complex():
#                         real_part = gldpro_obj.get_part("real")
#                         imag_part = gldpro_obj.get_part("imag")
#                         val_unit = gldpro_obj.get_unit()
#                         complex_val = f"{real_part:.6f}"
#                         if imag_part >= 0:
#                             complex_val += f"+{abs(imag_part):.6f}j"
#                         else:
#                             complex_val += f"{imag_part:.6f}j"
#                         if val_unit is not None and val_unit.is_valid():
#                             unit_name = val_unit.get_name()
#                             complex_val += f" {unit_name}"
#                         self.publish_json_data[simName][vjson_publish_gld_property_name[isize].object_name][vjson_publish_gld_property_name[isize].object_property] = complex_val
#                     elif gldpro_obj.is_integer():
#                         self.publish_json_data[simName][vjson_publish_gld_property_name[isize].object_name][vjson_publish_gld_property_name[isize].object_property] = int(gldpro_obj.get_integer())
#                     elif gldpro_obj.is_character() or gldpro_obj.is_enumeration() or gldpro_obj.is_complex() or gldpro_obj.is_objectref() or gldpro_obj.is_set():
#                         chtmp = gldpro_obj.to_""
#                         self.publish_json_data[simName][vjson_publish_gld_property_name[isize].object_name][vjson_publish_gld_property_name[isize].object_property] = chtmp
#                     elif gldpro_obj.is_timestamp():
#                         self.publish_json_data[simName][vjson_publish_gld_property_name[isize].object_name][vjson_publish_gld_property_name[isize].object_property] = int(gldpro_obj.get_timestamp())
#                     else:
#                         gridlabd.gl_error(f"fncs_msg::publishJsonVariables(): the global_property_types of the gld_property: {vjson_publish_gld_property_name[isize].object_name}.{vjson_publish_gld_property_name[isize].object_property} is not a recognized global_property_types!")
#                         return 0
#             else:
#                 self.publish_json_data[simName][vjson_publish_gld_property_name[isize].object_name][vjson_publish_gld_property_name[isize].object_property] = vjson_publish_gld_property_name[isize].hdr_val
#
#         # Write publish_json_data to a string and publish it through FNCS API
#         pubjsonstr = json.dumps(self.publish_json_data, indent=4)
#         skey = "fncs_output"
#
#         gridlabd.gl_verbose(f"fncs_msg::publishJsonVariables() fncs_publish: key: {skey}, value: {pubjsonstr}")
#
#         # Mocked FNCS publish for testing purposes, replace with actual FNCS code
#         self.mock_fncs_publish(skey, pubjsonstr)
#
#         return 1
#
#     # Mocked fncs.publish() for testing purposes
#     def mock_fncs_publish(self, skey, pubjsonstr):
#         # Replace this with actual FNCS code
#         print(f"Published to FNCS: Key: {skey}, Value: {pubjsonstr}")
#
#     # Mocked fncs.get_values() for testing purposes
#     def mock_fncs_get_values(self, skey):
#         # Replace this with actual FNCS code
#         return ['{"test_object":{"test_property1":42, "test_property2":"hello"}}']
#
#     def subscribe_variables(self, rmap):
#         value = ""
#         valueBuf = ["" for _ in range(1024)]
#
#         for mp in rmap.get_all():
#             if mp.dir == gridlabd.DXD_READ:
#                 if mp.ctype == gridlabd.CT_PUBSUB:
#                     updated_events = self.get_updated_events()
#                     if mp.remote_name in updated_events:
#                         value = self.get_value(mp.remote_name)
#                     else:
#                         value = ""
#                     if not value:
#                         continue
#                     valueBuf[:1023] = list(value)
#                     mp.obj.from_string("".join(valueBuf))
#
#         return 1
#
#     def get_updated_events(self):
#         # Replace this with actual FNCS code to get updated events
#         updated_events = ["event1", "event2"]  # Example data
#         return updated_events
#
#     def get_value(self, remote_name):
#         # Replace this with actual FNCS code to get the value
#         return "SampleValue"  # Example data
#
#     def incoming_fncs_function(self):
#         for relay in self.first_fncsfunction:
#             if relay.drtn == gridlabd.DXD_READ:
#                 function_calls = self.get_values(relay.remotename)
#                 s = len(function_calls)
#                 if s > 0:
#                     for i in range(s):
#                         message = function_calls[i]
#                         # Parse the message
#                         msg_data = json.loads(message)
#                         from_name = msg_data["from"]
#                         to_name = msg_data["to"]
#                         func_name = msg_data["function"]
#                         payload_string = msg_data["data"]
#                         payload_length = int(msg_data["data length"])
#
#                         # Check if the function is correct
#                         if func_name != relay.localcall:
#                             raise Exception(
#                                 "fncs_msg::incoming_fncs_function: The remote side function call, {}, is not the same as the local function name, {}.".format(
#                                     func_name, relay.localcall))
#
#                         # Call local function
#                         obj = gridlabd.gl_get_object(to_name)
#                         if obj is None:
#                             raise Exception(
#                                 "fncs_msg::incoming_fncs_function: the 'to' object does not exist. {}.".format(to_name))
#
#                         func_addr = gridlabd.gl_get_function(obj, relay.localcall)
#                         if func_addr is not None:
#                             raw_payload = bytearray.fromhex(payload_string)
#                             payload_length = min(len(raw_payload), payload_length)
#                             func_addr(from_name, to_name, relay.localcall, relay.localclass, raw_payload,
#                                       payload_length)
#                         else:
#                             raise Exception("fncs_msg::incoming_fncs_function: Local function not found: {}.".format(
#                                 relay.localcall))
#
#     def get_values(self, remote_name):
#         # Replace this with actual FNCS code to get values
#         values = [
#             "{\"from\":\"source1\", \"to\":\"target1\", \"function\":\"func1\", \"data\":\"data1\", \"data length\":\"10\"}"]  # Example data
#         return values
#
#     def commit(self, t0, t1):
#         result = 0
#         if t1 < gl_globalstoptime:
#             result = self.publish_variables(vmap[8])
#             if result == 0:
#                 return TIMESTAMP('TS_INVALID')
#
#         # Publish json_configure variables, renke
#         # TODO
#         if message_type == MT_JSON:
#             if real_time_gridappsd_publish_period == 0 or t1 == gridappsd_publish_time:
#                 if real_time_gridappsd_publish_period > 0:
#                     gridappsd_publish_time = t1 + TIMESTAMP(real_time_gridappsd_publish_period)
#                 if t1 < gl_globalstoptime:
#                     result = self.publish_json_variables()
#                     if result == 0:
#                         return TIMESTAMP('TS_INVALID')
#
#         # Read commit variables from cache
#         # Put an if statement to check the message_type
#         if t1 < gl_globalstoptime:
#             result = self.subscribe_variables(vmap[8])
#             if result == 0:
#                 return TIMESTAMP('TS_INVALID')
#
#         return TIMESTAMP('TS_NEVER')
#
#     def publish_variables(self, wmap):
#         buffer = [0] * 1024
#         fromBuf = [0] * 1024
#         toBuf = [0] * 1024
#         keyBuf = [0] * 1024
#         key = ""
#         value = ""
#         fromName = ""
#         toName = ""
#         pub_value = False
#
#         for mp in wmap.getfirst():
#             pub_value = False
#             if mp.dir == CT_WRITE:
#                 if mp.obj.to_string(buffer, 1023) < 0:
#                     value = ""
#                 else:
#                     value = "".join(chr(c) for c in buffer if c != 0)
#
#                 if not value:
#                     continue
#
#                 if mp.threshold == "":
#                     pub_value = True
#                 else:
#                     if mp.obj.is_complex():
#                         cval = mp.obj.get_complex()
#                         if not mp.last_value:
#                             pub_value = True
#                             mp.last_value = LastValueBuffer(cval)
#                         else:
#                             last_val = mp.last_value.get_complex()
#                             if fabs(cval.Mag() - last_val.Mag()) > float(mp.threshold):
#                                 pub_value = True
#                                 mp.last_value.set(cval)
#                     elif mp.obj.is_double():
#                         dval = mp.obj.get_double()
#                         if not mp.last_value:
#                             pub_value = True
#                             mp.last_value = LastValueBuffer(dval)
#                         else:
#                             last_val = mp.last_value.get_double()
#                             if fabs(dval - last_val) > float(mp.threshold):
#                                 pub_value = True
#                                 mp.last_value.set(dval)
#                     elif mp.obj.is_integer():
#                         ival = mp.obj.get_integer()
#                         if not mp.last_value:
#                             pub_value = True
#                             mp.last_value = LastValueBuffer(ival)
#                         else:
#                             last_val = mp.last_value.get_integer()
#                             if fabs(ival - last_val) > float(mp.threshold):
#                                 pub_value = True
#                                 mp.last_value.set(ival)
#                     elif mp.obj.is_enumeration() or mp.obj.is_character():
#                         if not mp.last_value:
#                             pub_value = True
#                             mp.last_value = LastValueBuffer(value)
#                         else:
#                             last_val = mp.last_value.get_""
#                             if value != last_val:
#                                 pub_value = True
#                                 mp.last_value.set(value)
#                     elif mp.obj.is_bool():
#                         bval = mp.obj.get_bool()
#                         if not mp.last_value:
#                             pub_value = True
#                             mp.last_value = LastValueBuffer(bval)
#                         else:
#                             last_val = mp.last_value.get_bool()
#                             if bval != last_val:
#                                 pub_value = True
#                                 mp.last_value.set(bval)
#
#                 if pub_value:
#                     if mp.ctype == CT_PUBSUB:
#                         key = mp.remote_name
#                         gridlabd.fncs.publish(key, value)
#                     elif mp.ctype == CT_ROUTE:
#                         fromBuf = mp.local_name.split('.')[0]
#                         toBuf, keyBuf = mp.remote_name.split('/')
#                         fromName = fromBuf
#                         toName = toBuf
#                         key = keyBuf
#                         gridlabd.fncs.route(fromName, toName, key, value)
#         return 1
#
#     def init(self, parent):
#         gl_verbose("entering fncs_msg::init()")
#
#         # Check if FNCS is available
#         try:
#             import fncs
#         except ImportError:
#             gl_error("fncs_msg::init ~ FNCS was not linked with GridLAB-D at compilation. fncs_msg cannot be used if FNCS was not linked with GridLAB-D.")
#             return 0
#
#         rv = 1
#
#         # Write the ZPL file
#         zplfile = []
#         inVariableTopics = []
#         inFunctionTopics = []
#         uniqueTopic = False
#         defer = False
#         n = 0
#         i = 0
#         d = 0
#         obj = parent
#         vObj = None
#         simName = gl_name(obj)
#         dft = ""
#         type = ""
#         defaultBuf = ""
#         message_type = "MT_GENERAL"  # Assuming it is MT_GENERAL for now
#
#         hostname = "localhost"
#         port = "39036"
#
#         if not hostname:
#             hostname = "localhost"
#         if not port:
#             port = "39036"
#
#         for n in range(1, 14):
#             vmap[n].resolve()
#             for pMap in vmap[n].getfirst():
#                 vObj = pMap.obj.get_object()
#                 if (vObj.flags & OF_INIT) != OF_INIT:
#                     defer = True
#
#         if defer:
#             gl_verbose("fncs_msg::init(): %s is deferring initialization.", obj.name)
#             return 2
#
#         nsize = len(vjson_publish_gld_property_name)
#         gldpro_obj = None
#         gld_obj = None
#         for isize in range(nsize):
#             if not vjson_publish_gld_property_name[isize].is_header:
#                 gld_object_name = vjson_publish_gld_property_name[isize].object_name
#                 if gld_object_name != "globals":
#                     gld_property_name = f"{vjson_publish_gld_property_name[isize].object_name}.{vjson_publish_gld_property_name[isize].object_property}"
#                     expr1 = vjson_publish_gld_property_name[isize].object_name
#                     expr2 = vjson_publish_gld_property_name[isize].object_property
#                     bufObj = expr1
#                     bufProp = expr2
#                     vjson_publish_gld_property_name[isize].prop = gld_property(bufObj, bufProp)
#
#                     if vjson_publish_gld_property_name[isize].prop.is_valid():
#                         gl_verbose("connection: local variable '%s' resolved OK, object id %d",
#                                     gld_property_name, vjson_publish_gld_property_name[isize].prop.get_object().id)
#                     else:
#                         gl_warning("connection: local variable '%s' cannot be resolved. This local variable will not be published.", gld_property_name)
#                 else:
#                     gld_global_name = vjson_publish_gld_property_name[isize].object_property
#                     expr1 = vjson_publish_gld_property_name[isize].object_property
#                     bufProp = expr1
#                     vjson_publish_gld_property_name[isize].prop = gld_property(bufProp)
#                     if vjson_publish_gld_property_name[isize].prop.is_valid():
#                         gl_verbose("fncs_msg::init: Global variable '%s' resolved OK", vjson_publish_gld_property_name[isize].object_property)
#                     else:
#                         gl_warning("fncs_msg::init: Global variable '%s' cannot be resolved This global variable will not be published.", vjson_publish_gld_property_name[isize].object_property)
#             else:
#                 if vjson_publish_gld_property_name[isize].object_property == "parent":
#                     oName = vjson_publish_gld_property_name[isize].object_name
#                     objname = oName
#                     vjson_publish_gld_property_name[isize].obj = gl_get_object(objname)
#                     vjson_publish_gld_property_name[isize].hdr_val = vjson_publish_gld_property_name[isize].obj.parent.name
#
#         for isize in range(nsize):
#             if not vjson_publish_gld_property_name[isize].is_header:
#                 if vjson_publish_gld_property_name[isize].prop.is_valid():
#                     vObj = vjson_publish_gld_property_name[isize].prop.get_object()
#                 else:
#                     vObj = None
#             else:
#                 if vjson_publish_gld_property_name[isize].object_property == "parent":
#                     objname = vjson_publish_gld_property_name[isize].object_name
#                     vjson_publish_gld_property_name[isize].obj = gl_get_object(objname)
#
#             if vObj:
#                 if (vObj.flags & OF_INIT) != OF_INIT:
#                     gl_warning(f"{isize}, fncs_msg::init(): vjson_publish_gld_property {vjson_publish_gld_property_name[isize].object_name}.{vjson_publish_gld_property_name[isize].object_property} not initialized!:  ")
#                     defer = True
#
#         if defer:
#             gl_warning("fncs_msg::init(): %s is deferring initialization.", obj.name)
#             return 2
#
#         # Determine the fncs_step as either 1s, or the global minimum_step
#         fncs_step = 1
#         glob_min_timestep = int(gl_global_getvar("minimum_timestep"))
#         if glob_min_timestep > 1:
#             fncs_step = glob_min_timestep
#         fncs_step *= 1000000000  # seconds ==> ns
#
#         # Create ZPL file for registering with FNCS
#         if message_type == "MT_GENERAL":
#             zplfile.append(f"name = {simName}")
#             zplfile.append(f"time_delta = {fncs_step}ns")
#             zplfile.append(f"broker = tcp://{hostname}:{port}")
#             if aggregate_sub:
#                 zplfile.append("aggregate_sub = true")
#             if aggregate_pub:
#                 zplfile.append("aggregate_pub = true")
#             zplfile.append("values")
#             for n in range(1, 14):
#                 if 1 <= n <= 13:
#                     for pMap in vmap[n].getfirst():
#                         if pMap.dir == CT_READ:
#                             uniqueTopic = True
#                             for i in range(len(inVariableTopics)):
#                                 if inVariableTopics[i] == pMap.remote_name:
#                                     uniqueTopic = False
#                             if uniqueTopic:
#                                 inVariableTopics.append(pMap.remote_name)
#                                 if pMap.obj.to_string(defaultBuf, 1024) < 0:
#                                     dft = "NA"
#                                 else:
#                                     dft = defaultBuf
#                                 zplfile.append(f"    {pMap.remote_name}")
#                                 zplfile.append(f"        topic = {pMap.remote_name}")
#                                 if dft:
#                                     zplfile.append(f"        default = {dft}")
#                                 if type:
#                                     zplfile.append(f"        global_property_types = {type}")
#                                 zplfile.append("        list = false")
#         elif message_type == "MT_JSON":
#             default_json_str = f'{{"{simName}":{{}}}}'
#             zplfile.append(f"name = {simName}")
#             zplfile.append(f"time_delta = {fncs_step}ns")
#             zplfile.append(f"broker = tcp://{hostname}:{port}")
#             zplfile.append("values")
#             zplfile.append(f"    {simName}/fncs_input")
#             zplfile.append(f"        topic = {simName}/fncs_input")
#             zplfile.append(f"        default = {default_json_str}")
#             zplfile.append(f"        global_property_types = JSON")
#             zplfile.append(f"        list = true")
#
#         # Get a string vector of the unique function subscriptions
#         for relay in first_fncsfunction:
#             if relay.drtn == CT_READ:
#                 uniqueTopic = True
#                 for i in range(len(inFunctionTopics)):
#                     if inFunctionTopics[i] == relay.remotename:
#                         uniqueTopic = False
#                 if uniqueTopic:
#                     inFunctionTopics.append(relay.remotename)
#                     zplfile.append(f"    {relay.remotename}")
#                     zplfile.append(f"        topic = {relay.remotename}")
#                     zplfile.append("        list = true")
#
#         # Register with FNCS
#         zplfile_str = "\n".join(zplfile)
#         fncs.initialize(zplfile_str)
#         atexit(fncs_send_die)
#         last_approved_fncs_time = gl_globalclock
#         last_delta_fncs_time = gl_globalclock
#         initial_sim_time = gl_globalclock
#         gridappsd_publish_time = initial_sim_time + timedelta(seconds=real_time_gridappsd_publish_period).total_seconds()
#         return rv
#
#     def configure(self, value):
#         rv = 1
#         self.configFile = value
#
#         if self.configFile:
#             try:
#                 with open(self.configFile, 'r') as ifile:
#                     if self.message_type == "MT_GENERAL":
#                         for line in ifile:
#                             confLine = line.strip()
#                             if "publish" in confLine:
#                                 gl_verbose("fncs_msg.configure(): processing line: %s", confLine)
#                                 value = confLine[confLine.find("publish") + 9:-2]
#                                 rv = self.publish(value)
#                                 if rv == 0:
#                                     return 0
#                             elif "subscribe" in confLine:
#                                 gl_verbose("fncs_msg.configure(): processing line: %s", confLine)
#                                 value = confLine[confLine.find("subscribe") + 11:-2]
#                                 rv = self.subscribe(value)
#                                 if rv == 0:
#                                     return 0
#                             elif "route" in confLine:
#                                 gl_verbose("fncs_msg.configure(): processing line: %s", confLine)
#                                 value = confLine[confLine.find("route") + 7:-2]
#                                 rv = self.route(value)
#                                 if rv == 0:
#                                     return 0
#                             elif "option" in confLine:
#                                 gl_verbose("fncs_msg.configure(): processing line: %s", confLine)
#                                 value = confLine[confLine.find("option") + 8:-2]
#                                 rv = self.option(value)
#                                 if rv == 0:
#                                     return 0
#                     elif self.message_type == "MT_JSON":
#                         json_config_stream = ""
#                         for line in ifile:
#                             json_config_stream += line
#                         gl_verbose("fncs_msg::configure(): json string read from configure file: %s", json_config_stream)  # renke debug
#
#                         # Test code to parse JSON
#                         try:
#                             publish_json_config = json.loads(json_config_stream)
#                             gl_verbose("fncs_msg::configure(): JSON configuration parsed successfully.")
#                         except json.JSONDecodeError as e:
#                             gl_error("fncs_msg::configure(): Error parsing JSON configuration: %s", e)
#                             return 0
#
#                         rv = self.publish_fncsjson_link()
#                         if rv == 0:
#                             return 0
#
#             except FileNotFoundError:
#                 gl_error("fncs_msg::configure(): failed to open the configuration file %s", self.configFile)
#                 rv = 0
#
#         return rv
#
#     def option(self, value):
#         rv = 0
#         target, command = value.split(':', 1)
#
#         if target.startswith("connection"):
#             print("connection is always a client when operating with fncs. Ignoring option.")
#             rv = 1
#         elif target.startswith("transport"):
#             transport_options = command.split(',')
#             for option in transport_options:
#                 param, val = option.split('=', 1)
#                 param = param.strip()
#                 val = val.strip()
#
#                 if param == "port":
#                     self.port = val
#                 elif param == "header_version":
#                     self.header_version = val
#                 elif param == "hostname":
#                     self.hostname = val
#                 else:
#                     print(f"fncs_msg::option 'transport:{param}' not recognized")
#                     return 0
#
#             rv = 1
#
#         return rv
from enum import Enum

from gridlab.connection.VarMap import VarMap
from gridlab.gldcore.Globals import SIMULATIONMODE

TS_INVALID = -1
TS_NEVER = float('inf')


def fncs_send_die():
    # Placeholder for checking the exit code and deciding to send die
    exit_code = 0  # Assuming a way to retrieve the global exit code
    if exit_code != 0:
        # Assuming fncs.die() is a method to signal a termination with error
        pass  # Placeholder for fncs.die()
    else:
        # Placeholder for fncs.finalize()
        pass

class FNCSTYPE(Enum):
    FT_VOID = 0
    FT_LIST = 1
    FT_REAL = 2
    FT_INTEGER = 3
    FT_STRING = 4

class MESSAGETYPE(Enum):
    MT_GENERAL = 0
    MT_JSON = 1

class JsonProperty:
    def __init__(self, objName, objProp):
        self.object_name = objName
        self.object_property = objProp
        self.is_header = objProp == "parent"
        # Assuming placeholders for gld_property and OBJECT, as these are likely specific to gridlabd
        self.prop = None
        self.obj = None

class FNCSLIST:
    def __init__(self, type, tag, value=None, parent=None):
        self.type = type
        self.tag = tag
        self.value = value  # Simplified union representation
        self.parent = parent
        self.next = None

def fncs_hex(c):
    if c < 10:
        return chr(c + ord('0'))
    elif c < 16:
        return chr(c - 10 + ord('A'))
    else:
        return '?'

def fncs_unhex(h):
    if '0' <= h <= '9':
        return ord(h) - ord('0')
    elif 'A' <= h <= 'F':
        return ord(h) - ord('A') + 10
    elif 'a' <= h <= 'f':
        return ord(h) - ord('a') + 10
    else:
        return ord('?')

def fncs_to_hex(in_bytes):
    out = ""
    for byte in in_bytes:
        lo = byte & 0xf
        hi = (byte >> 4) & 0xf
        out += fncs_hex(hi) + fncs_hex(lo)
    return out

def fncs_from_hex(hex_str):
    if len(hex_str) % 2 != 0:
        return None  # Invalid hex string
    buf = bytearray()
    for i in range(0, len(hex_str), 2):
        hi = fncs_unhex(hex_str[i])
        lo = fncs_unhex(hex_str[i+1])
        if hi == ord('?') or lo == ord('?'):
            return None  # Bad hex data
        buf.append((hi << 4) + lo)
    return bytes(buf)


class FunctionRelay:
    def __init__(self, localclass, localcall, remoteclass, remotename, direction, ctype):
        self.localclass = localclass
        self.localcall = localcall
        self.remoteclass = remoteclass
        self.remotename = remotename
        self.direction = direction
        self.ctype = ctype
        self.route = None
        self.xlate = None

class FncsMsg:
    relays = []
    #  def __init__(self):
    def __init__(self):
        self.version = 0.0
        self.port = ""
        self.header_version = ""
        self.hostname = ""
        self.configFile = ""
        # Simplify the handling of published properties and topics
        self.inFunctionTopics = []
        self.vmap = [None] * 14  # Placeholder for varmap objects
        self.message_type = MESSAGETYPE.MT_GENERAL
        self.simulationName = ""
        # Placeholder for Json::Value types
        self.publish_json_config = {}
        self.publish_json_data = {}
        self.subscribe_json_data = {}
        # Simplifying the handling of JsonProperties
        self.vjson_publish_gld_property_name = []
        # Assuming a placeholder for FNCS timing
        self.fncs_step = 0

        # Simplified adaptation of constructor logic
        # Setting up default values for properties
        self.version = 1.0  # Assuming a default version
        self.message_type = MESSAGETYPE.MT_GENERAL
        self.real_time_gridappsd_publish_period = 0
        self.aggregate_pub = False
        self.aggregate_sub = False

        self.port = ""
        self.header_version = ""
        self.hostname = ""
        self.configFile = ""
        self.inFunctionTopics = []
        self.vmap = [None] * 14
        self.simulationName = ""
        # Assuming a placeholder for Json::Value types
        self.publish_json_config = {}
        self.publish_json_data = {}
        self.subscribe_json_data = {}
        self.vjson_publish_gld_property_name = []
        self.fncs_step = 0

        # Placeholder methods to simulate publishing load methods in Python
        # In actual usage, these should be implemented or bound to the appropriate Python functions
        self.route = self.placeholder_method
        self.option = self.placeholder_method
        self.publish = self.placeholder_method
        self.subscribe = self.placeholder_method
        self.configure = self.placeholder_method
        self.create()

    @staticmethod
    def add_fncs_function(route, fclass, flocal, rclass, rname, xlate, direction, ctype):
        # Check for the existence of a relay
        for relay in FncsMsg.relays:
            if relay.remotename == rname and relay.remoteclass == rclass:
                print(f"fncs_msg::add_fncs_function: a relay function is already defined for '{rclass}/{rname}'")
                return None

        # Create and setup a new relay
        new_relay = FunctionRelay(fclass, flocal, rclass, rname, direction, ctype)
        new_relay.route = route
        new_relay.xlate = xlate
        FncsMsg.relays.append(new_relay)

        # Return the relay handling function based on direction
        if direction == "DXD_WRITE":
            return FncsMsg.outgoing_fncs_function
        else:
            return None

    @staticmethod
    def find_fncs_function(rclass, rname):
        for relay in FncsMsg.relays:
            if relay.remotename == rname and relay.remoteclass == rclass:
                return relay
        return None

    @staticmethod
    def outgoing_fncs_function(from_class, to, funcName, funcClass, data):
        relay = FncsMsg.find_fncs_function(funcClass, funcName)
        if relay is None:
            raise Exception(f"the relay function for function name {funcName} could not be found.")

        # Additional logic to handle the data and send it through FNCS would be needed here


    def create(self):
        self.version = 1.0
        self.message_type = MESSAGETYPE.MT_GENERAL
        # Assuming placeholder functions for add_clock_update, register_object_interupdate, etc.
        self.add_clock_update(self.fncs_clocks_update)
        self.register_object_interupdate(self.fncs_dInterupdate)
        self.register_object_deltaclockupdate(self.fncs_dClockupdate)

        # Setup all the variable maps
        # Assuming varmap is a class or structure you have defined or will define
        self.vmap = [None] + [VarMap() for _ in range(1, 14)]

        self.port = ""
        self.header_version = ""
        self.hostname = ""
        self.inFunctionTopics = []
        self.real_time_gridappsd_publish_period = 3
        self.aggregate_pub = False
        self.aggregate_sub = False

        return 1  # Simulating the C++ method's return value for success

    # Placeholder methods for functionality that needs specific implementation or binding
    def fncs_clocks_update(self, *args):
        pass

    def fncs_dInterupdate(self, *args):
        pass

    def fncs_dClockupdate(self, *args):
        pass

    def placeholder_method(self, *args, **kwargs):
        print("This is a placeholder method. Implement functionality as needed.")

    def publish(self, value):
        # Assuming a placeholder for gl_warning or equivalent logging
        # print("entering fncs_msg::publish()")
        rv = self.fncs_link(value, "CT_PUBSUB")
        return rv

    def subscribe(self, value):
        # print("entering fncs_msg::subscribe()")
        rv = self.fncs_link(value, "CT_PUBSUB")
        return rv

    def route(self, value):
        rv = self.fncs_link(value, "CT_ROUTE")
        return rv

    def fncs_link(self, value, communication_type):
        # Placeholder for the actual implementation of fncs_link functionality
        # This method should handle the linking based on the value and communication type
        # For now, let's simulate a successful operation
        print(f"Linking {value} with communication type {communication_type}")
        return 1  # Simulating a successful operation return value

    def init(self, parent):
        pass




    # Add other method placeholders as needed

    # Static methods for FNCSLIST handling
    @staticmethod
    def parse(buffer):
        pass

    @staticmethod
    def find(list, tag):
        pass

    @staticmethod
    def get(list, tag):
        pass

    @staticmethod
    def destroy(list):
        pass

    def precommit(self, t1):
        result = 0
        if self.message_type == MESSAGETYPE.MT_GENERAL:
            self.incoming_fncs_function()
            if t1 < self.gl_globalstoptime:  # Assuming self.gl_globalstoptime is defined
                result = self.publishVariables(self.vmap[4])
                if result == 0:
                    return result
                result = self.subscribeVariables(self.vmap[4])
                if result == 0:
                    return result
        # Assuming implementation for MT_JSON message type and its methods
        return 1

    def presync(self, t1):
        result = 0
        if self.message_type == MESSAGETYPE.MT_GENERAL:
            result = self.publishVariables(self.vmap[5])
            if result == 0:
                return TS_INVALID
            result = self.subscribeVariables(self.vmap[5])
            if result == 0:
                return TS_INVALID
        elif self.message_type == MESSAGETYPE.MT_JSON:
            result = self.subscribeJsonVariables()
            if result == 0:
                return TS_INVALID
        return TS_NEVER

    def subscribeJsonVariables(self):
        # Placeholder for subscribing to JSON variables
        return 1

    def plc(self, t1):
        if t1 < self.gl_globalstoptime:  # Assuming self.gl_globalstoptime is defined elsewhere
            result = self.publishVariables(self.vmap[12])
            if result == 0:
                return TS_INVALID
            result = self.subscribeVariables(self.vmap[12])
            if result == 0:
                return TS_INVALID
        return TS_NEVER

    def sync(self, t1):
        if t1 < self.gl_globalstoptime:
            result = self.publishVariables(self.vmap[6])
            if result == 0:
                return TS_INVALID
            result = self.subscribeVariables(self.vmap[6])
            if result == 0:
                return TS_INVALID

        if self.message_type == MESSAGETYPE.MT_GENERAL:
            return TS_NEVER
        elif self.message_type == MESSAGETYPE.MT_JSON:
            t2 = t1 + 1  # Assuming a simple increment for the next timestamp
            return t2

        return TS_INVALID

    def postsync(self, t1):
        if t1 < self.gl_globalstoptime:
            result = self.publishVariables(self.vmap[7])
            if result == 0:
                return TS_INVALID
            result = self.subscribeVariables(self.vmap[7])
            if result == 0:
                return TS_INVALID

        return TS_NEVER

    def prenotify(self, property_name, value):
        # Assuming property_name and value replace the C++ PROPERTY* p and char* v parameters
        # and assuming these are used or needed for determining what to publish/subscribe.
        # This is a simplification and might need adjustment based on actual usage.

        result = self.publishVariables(self.vmap[9])
        if result == 0:
            return result

        result = self.subscribeVariables(self.vmap[9])
        if result == 0:
            return result

        return 1

    def postnotify(self, property_name, value):
        # Similar simplification as in prenotify

        result = self.publishVariables(self.vmap[10])
        if result == 0:
            return result

        result = self.subscribeVariables(self.vmap[10])
        if result == 0:
            return result

        return 1

    def deltaInterUpdate(self, delta_iteration_counter, t0, dt):
        # Placeholder for checking the global deltaclock, assuming a method to access it
        deltaclock = self.get_deltaclock()  # This method needs to be defined

        if deltaclock is None or deltaclock <= 0:
            # Placeholder for logging an error
            print("fncs_msg::deltaInterUpdate: Unable to find global deltaclock!")
            return SIMULATIONMODE.SM_ERROR

        # Define the logic based on the delta_iteration_counter
        vmap_index = None
        if delta_iteration_counter == 0:
            vmap_index = 8
        elif delta_iteration_counter == 1:
            vmap_index = 5
        elif delta_iteration_counter == 2:
            vmap_index = 12
        elif delta_iteration_counter == 3:
            vmap_index = 6
        elif delta_iteration_counter == 4:
            vmap_index = 7

        if vmap_index is not None:
            result = self.publishVariables(self.vmap[vmap_index])
            if result == 0:
                return SIMULATIONMODE.SM_ERROR
            result = self.subscribeVariables(self.vmap[vmap_index])
            if result == 0:
                return SIMULATIONMODE.SM_ERROR

            # Call to process external function calls for the first iteration
            if delta_iteration_counter == 0:
                self.incoming_fncs_function()

            return SIMULATIONMODE.SM_DELTA_ITER

        return SIMULATIONMODE.SM_EVENT

    # Placeholder method for get_deltaclock
    def get_deltaclock(self):
        # This method should retrieve the global deltaclock value
        return 1  # Example placeholder value

    # Placeholder methods for publishVariables, subscribeVariables, incoming_fncs_function
    def publishVariables(self, vmap):
        # Placeholder for publishing variables logic
        return 1

    def subscribeVariables(self, vmap):
        # Placeholder for subscribing to variables logic
        return 1

    def incoming_fncs_function(self):
        # Placeholder for handling incoming FNCS functions
        pass

    def deltaClockUpdate(self, t1, timestep, sysmode):
        rv = SIMULATIONMODE.SM_DELTA
        # Placeholder for FNCS logic
        # This is a simplified version and might need actual FNCS bindings or equivalent logic in Python
        if t1 > self.last_delta_fncs_time:
            # Simulate FNCS time update logic
            # This part needs to be replaced with actual interaction with FNCS in Python
            fncs_time = t1  # Simplified placeholder
            if sysmode == SIMULATIONMODE.SM_EVENT:
                self.exitDeltamode = True
                rv = SIMULATIONMODE.SM_EVENT
            if fncs_time != t1:
                # Placeholder for logging an error
                print("fncs_msg::deltaClockUpdate: Cannot return anything other than the time GridLAB-D requested in deltamode.")
                return SIMULATIONMODE.SM_ERROR
            else:
                self.last_delta_fncs_time = fncs_time
        return rv

    def clk_update(self, t1):
        # Placeholder for FNCS logic
        # This needs actual FNCS interaction or simulation logic
        if self.exitDeltamode:
            # Simulate FNCS time update logic
            self.exitDeltamode = False
        if t1 > self.last_approved_fncs_time:
            # Simulate time update logic, including FNCS interactions
            fncs_time = t1 + 1  # Simplified placeholder
            if fncs_time <= t1:  # Placeholder condition
                print("fncs_msg::clock_update: Cannot return the current time or less than the current time.")
                return TS_INVALID
            else:
                self.last_approved_fncs_time = fncs_time
                t1 = fncs_time
        return t1

    def finalize(self):
        # Assuming vjson_publish_gld_property_name is a list of objects that might hold resources
        # Since Python manages memory automatically, explicit deletion might not be necessary
        # unless dealing with external resources or large datasets
        # This loop simulates cleaning up any resources or references held by the objects
        for obj in self.vjson_publish_gld_property_name:
            # Assuming cleanup or release of resources if necessary
            pass  # Placeholder for cleanup logic
        return 1


    def get_varmapindex(self, name):
        varmapname = [
            "", "allow", "forbid", "init", "precommit", "presync", "sync", "postsync",
            "commit", "prenotify", "postnotify", "finalize", "plc", "term"
        ]
        if name in varmapname:
            return varmapname.index(name)
        return 0

    def fncs_link(self, value, comtype):
        # Assuming 'vmap' is a list of VARMAP objects initialized in the class
        command, argument = value.split(':', 1)
        if command == "init":
            print("fncs_msg::publish: It is not possible to pass information at init time with fncs. communication is ignored")
            return 1
        elif command == "function":
            return self.parse_fncs_function(argument, comtype)
        else:
            n = self.get_varmapindex(command)
            if n != 0:
                # Assuming 'add' is a method in the VARMAP class to add a variable with the given command
                return self.vmap[n].add(argument, comtype)
        print(f"fncs_msg::publish: Unable to parse input {value}.")
        return 0

    def parse_fncs_function(self, value, comtype):
        # This is a simplified placeholder for parsing FNCS function strings and integrating with FNCS
        print(f"Parsing FNCS function with value: {value} and comtype: {comtype}")
        # Actual integration logic goes here
        return 1

    def publish_fncsjson_link(self):
        # Assuming 'publish_json_config' is a JSON-like dictionary and 'vjson_publish_gld_property_name' is a list
        if not self.publish_json_config:
            print("Publish json configure is empty!!!")
            return 1

        self.vjson_publish_gld_property_name.clear()
        for gldObjectName, properties in self.publish_json_config.items():
            for gldPropertyName in properties:
                gldProperty = JsonProperty(gldObjectName, gldPropertyName)
                self.vjson_publish_gld_property_name.append(gldProperty)
        return 1