import math

from gov_pnnl_goss.gridlab.gldcore.Class import PASSCONFIG
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_verbose, gl_error
from gov_pnnl_goss.gridlab.gldcore.PropertyHeader import PropertyType


def clocks_update(ptr, t1):
    my = ptr
    return my.clk_update(t1)


def d_interupdate(ptr, d_interval_counter, t0, dt):
    my = ptr
    return my.delta_inter_update(d_interval_counter, t0, dt)



def d_clock_update(ptr, t1, timestep, sysmode):
    my = ptr
    return my.delta_clock_update(t1, timestep, sysmode)


def check_return_value(rv):
    if rv == 0:
        return 0


def convert_to_python_function(t1, last_delta_helics_time, sysmode, initial_sim_time, timestep, gld_helics_federate, HELICS_PROPERTY_TIME_PERIOD, DT_SECOND, SM_EVENT, SM_ERROR):
    if t1 > last_delta_helics_time:
        helics_t = 0
        t = 0
        dt = 0
        t_ns = 0
        helics_t_ns = 0
        dt = (t1 - float(initial_sim_time))*1000000000.0
        if sysmode == SM_EVENT:
            t = (((dt + (1000000000.0 / 2.0)) - (dt + (1000000000.0 / 2.0)) % 1000000000.0)/1000000000.0)
        else:
            t = (((dt + float(timestep) / 2.0) - (dt + float(timestep) / 2.0) % float(timestep))/1000000000.0)
        gld_helics_federate.setProperty(HELICS_PROPERTY_TIME_PERIOD, float(timestep)/DT_SECOND)
        helics_t = gld_helics_federate.requestTime(t)
        
        if sysmode == SM_EVENT:
            exit_deltamode = True
        t_ns = int(round(t * 1000000000.0))
        helics_t_ns = int(round(helics_t * 1000000000.0))
        if helics_t_ns != t_ns:
            gl_error("helics_msg::delta_clock_update: Cannot return anything other than the time GridLAB-D requested in deltamode. Time requested %f. Time returned %f.", float(t), float(helics_t))
            return SM_ERROR
        else:
            last_delta_helics_time = float(helics_t) + float(initial_sim_time)
    return


class HelicsMsg:
    
    def __init__(self, module):
        self.oclass = gld_class.create(module, "helics_msg", 0,
                                       PASSCONFIG.PC_AUTOLOCK|PASSCONFIG.PC_PRETOPDOWN|PASSCONFIG.PC_BOTTOMUP|PASSCONFIG.PC_POSTTOPDOWN|PASSCONFIG.PC_OBSERVER
                                       )
        
        if self.oclass is None:
            raise Exception("connection/helics_msg::helics_msg(MODULE*): unable to register class connection:helics_msg")
        else:
            self.oclass.trl = TRL_UNKNOWN
        
        self.defaults = self
        
        if gl_publish_variable(
            self.oclass,
            PropertyType.PT_double,
            "version", 
            get_version_offset(), 
            PropertyType.PT_DESCRIPTION,
            "helics_msg version",
            PropertyType.PT_enumeration,
            "message_type", 
            PADDR(message_type), 
            PropertyType.PT_DESCRIPTION,
            "set the global_property_types of message format you wish to construct",
            PropertyType.PT_KEYWORD,
            "GENERAL", 
            enumeration(HMT_GENERAL), 
            PropertyType.PT_DESCRIPTION,
            "use this for sending a general HELICS topic/value pair.",
            PropertyType.PT_KEYWORD,
            "JSON", 
            enumeration(HMT_JSON), 
            PropertyType.PT_DESCRIPTION,
            "use this for want to send a bundled json formatted messag in a single topic.",
            PropertyType.PT_int32,
            "publish_period", 
            PADDR(publish_period), 
            PropertyType.PT_DESCRIPTION,
            "use this with json bundling to set the period [s] at which data is published.",
            None
        ) < 1:
            raise Exception("connection/helics_msg::helics_msg(MODULE*): unable to publish properties of connection:helics_msg")
        
        if not gl_publish_loadmethod(
            self.oclass,
            "configure",
            lambda val, string: loadmethod_helics_msg_configure(OBJECT(val), string)
        ):
            raise Exception("connection/helics_msg::helics_msg(MODULE*): unable to publish configure method of connection:helics_msg")

    def create(self):
        self.add_clock_update(self, self.clocks_update)
        self.register_object_interupdate(self, self.d_interupdate)
        self.register_object_deltaclockupdate(self, self.d_clockupdate)
        self.message_type = HMT_GENERAL
        self.publish_period = 0
        return 1

    def configure(self, value):
        rv = 1
        configFile = value[:1024]
        if configFile != "":
            self.federate_configuration_file = configFile
        else:
            gl_error("helics_msg::configure(): No configuration file was give. Please provide a configuration file!")
            rv = 0
        return rv

    def init_helics_msg(self, parent: OBJECT) -> int:
    
        gl_verbose("entering helics_msg::init()")
    
        rv = 1
        # ...
        
        if rv == 0:
            return 0

    def precommit(self, t1):
        result = 0
        if self.message_type == HMT_GENERAL:
            result = self.subscribe_variables()
            if result == 0:
                return result
        return 1

    def presync(self, t1):
        if self.message_type == HMT_JSON:
            result = 0
            result = self.subscribe_json_variables()
            if result == 0:
                return TS_INVALID
        return TS_NEVER

    def sync(self, t1):
        return TS_NEVER

    def post_sync(self, t1):
        return "TS_NEVER"

    def commit(self, t_0, t_1):
        return TS_NEVER

    def delta_inter_update(self, delta_iteration_counter, t0, dt):
        result = 0
        dclock = gld_global("deltaclock")
        if not dclock.is_valid():
            gl_error("helics_msg::deltaInterUpdate: Unable to find global deltaclock!")
            return SM_ERROR
        if dclock.get_int64() > 0:
            if delta_iteration_counter == 0:
                result = self.subscribe_variables()
                if result == 0:
                    return SM_ERROR
                return SM_DELTA_ITER
            if delta_iteration_counter in [1, 2, 3]:
                return SM_DELTA_ITER
            if delta_iteration_counter == 4:
                result = self.publish_variables()
                if result == 0:
                    return SM_ERROR
        return SM_EVENT

    def delta_clock_update(self, t1, timestep, sysmode):
        if t1 > self.last_delta_helics_time:
    
            helics_t = 0
            t = 0
            dt = 0
            t_ns = 0
            helics_t_ns = 0
            
            dt = (t1 - float(self.initial_sim_time)) * 1000000000.0
            if sysmode == SimulationMode.EVENT:
                t = ((dt + (1000000000.0 / 2.0)) - (dt + (1000000000.0 / 2.0)) % 1000000000.0) / 1000000000.0
            else:
                t = ((dt + (float(timestep) / 2.0)) - (dt + (float(timestep) / 2.0)) % float(timestep)) / 1000000000.0
            self.gld_helics_federate.set_property(HelicsProperty.TIME_PERIOD, float(timestep) / DT_SECOND)
            helics_t = self.gld_helics_federate.request_time(t)
    
            if sysmode == SimulationMode.EVENT:
                self.exit_delta_mode = True
            t_ns = int(round(t * 1000000000.0))
            helics_t_ns = int(round(helics_t * 1000000000.0))
            if helics_t_ns != t_ns:
                gl_error(f"helics_msg::delta_clock_update: Cannot return anything other than the time GridLAB-D requested in deltamode. Time requested {float(t)}. Time returned {float(helics_t)}.")
                return SimulationMode.ERROR
            else:
                self.last_delta_helics_time = float(helics_t) + float(self.initial_sim_time)
            
        if sysmode == SimulationMode.DELTA:
            return SimulationMode.DELTA
        elif sysmode == SimulationMode.EVENT:
            return SimulationMode.EVENT
        else:
            return SimulationMode.ERROR

    def clk_update(self, t1):
        helics_t = 0
        if self.exit_delta_mode:
            gl_verbose("helics_msg: Calling setTimeDelta")
            gld_helics_federate.setProperty(HELICS_PROPERTY_TIME_PERIOD, 1.0)
            self.exit_delta_mode = False
        if t1 > self.last_approved_helics_time:
            result = 0
            if gl_globalclock == gl_globalstoptime:
                gl_verbose("helics_msg: Calling finalize")
                pHelicsFederate.finalize()
                return t1
            elif t1 > gl_globalstoptime and gl_globalclock < gl_globalstoptime:
                t1 = gl_globalstoptime
            if self.message_type == HMT_GENERAL:
                if self.publish_period == 0 or t1 == self.publish_time:
                    if self.publish_period > 0:
                        self.publish_time = t1 + TIMESTAMP(self.publish_period)
                    result = self.publish_variables()
                    if result == 0:
                        return TS_INVALID
            elif self.message_type == HMT_JSON:
                if self.publish_period == 0 or t1 == self.publish_time:
                    if self.publish_period > 0:
                        self.publish_time = t1 + TIMESTAMP(self.publish_period)
                    if t1 < gl_globalstoptime:
                        result = self.publish_json_variables()
                        if result == 0:
                            return TS_INVALID
            t = HelicsTime(float(t1 - self.initial_sim_time))
            gl_verbose("helics_msg: Calling requestime")
            gl_verbose("helics_msg: Requesting %f", float(t))
            rt = gld_helics_federate.requestTime(t)
            gl_verbose("helics_msg: Granted %f", float(rt))
            helics_t = TIMESTAMP(rt) + self.initial_sim_time
            if helics_t <= gl_globalclock:
                gl_error("helics_msg::clock_update: Cannot return the current time or less than the current time.")
                return TS_INVALID
            else:
                self.last_approved_helics_time = helics_t
                t1 = helics_t
        return t1

    def publish_variables(self):
        buffer = bytearray(1024)
        buffer_size = 0
        temp_value = ""
        message_buffer_stream = io.StringIO()
        complex_temp = 0.0 + 0.0j
        json_publish_data = {}
        complex_val = io.StringIO()
        writer_builder = JsonStreamWriterBuilder()
        json_message_str = ""
        for pub in self.helics_value_publications:
            buffer_size = 0
            if pub.p_object_property.is_complex():
                real_part = pub.p_object_property.get_part("real")
                imag_part = pub.p_object_property.get_part("imag")
                val_unit = pub.p_object_property.get_unit()
                complex_temp = complex(real_part, imag_part)
                gl_verbose("helics_msg: calling publish({}+{}j) on publication {}".format(real_part, imag_part, pub.name))
                pub.HelicsPublication.publish(complex_temp)
            elif pub.p_object_property.is_integer():
                integer_temp = pub.p_object_property.get_integer()
                gl_verbose("helics_msg: calling publishInt({}) on publication {}".format(integer_temp, pub.name))
                pub.HelicsPublication.publish(integer_temp)
            elif pub.p_object_property.is_double():
                double_temp = pub.p_object_property.get_double()
                gl_verbose("helics_msg: calling publish({}) on publication {}".format(double_temp, pub.name))
                pub.HelicsPublication.publish(double_temp)
            else:
                buffer_size = pub.p_object_property.to_string(buffer, 1023)
                if buffer_size <= 0:
                    temp_value = ""
                else:
                    temp_value = buffer.decode('utf-8')[:buffer_size]
                    gl_verbose("helics_msg: Calling publish('{}') on publication {}".format(temp_value, pub.name))
                    pub.HelicsPublication.publish(temp_value)
    
        for pub in self.helics_endpoint_publications:
            buffer_size = 0
            message_buffer_stream.seek(0)
            if pub.p_object_property.is_complex():
                real_part = pub.p_object_property.get_part("real")
                imag_part = pub.p_object_property.get_part("imag")
                complex_temp = complex(real_part, imag_part)
                buffer_size = sprintf(buffer, "%.3f%+.3fj", real_part, imag_part)
            else:
                buffer_size = pub.p_object_property.to_string(buffer, 1023)
            message_buffer_stream.write(buffer.decode('utf-8'))
            message_buffer = message_buffer_stream.getvalue()
            message_buffer_stream.truncate(0)
            
            if gld_helics_federate.get_current_mode() == HELICS_STATE_EXECUTION:
                try:
                    msg = helics.Message(pub.HelicsPublicationEndpoint)
                    msg.data(message_buffer)
                    gl_verbose("calling helics sendMessage on endpoint {}. Message: {}".format(pub.name, message_buffer))
                    pub.HelicsPublicationEndpoint.send_message(msg)
                    del msg
                except Exception as e:
                    gl_error("calling HELICS sendMessage resulted in an unknown error.")
                    print(e)
    
        for pub in self.json_helics_value_publications:
            json_publish_data.clear()
            for o in pub.json_publications:
                prop = o.prop
                if prop.is_valid():
                    object_name = o.object_name
                    if object_name not in json_publish_data:
                        json_publish_data[object_name]
                    if prop.is_double():
                        json_publish_data[object_name][o.property_name] = prop.get_double()
                    elif prop.is_complex():
                        real_part = prop.get_part("real")
                        imag_part = prop.get_part("imag")
                        val_unit = prop.get_unit()
                        complex_val.seek(0)
                        complex_val.write("{:.8f}".format(real_part))
                        if imag_part >= 0:
                            complex_val.write("+{:.8f}j".format(abs(imag_part)))
                        else:
                            complex_val.write("{:.8f}j".format(imag_part))
                        if val_unit and val_unit.is_valid():
                            unit_name = str(val_unit.get_name())
                            complex_val.write(" {}".format(unit_name))
                        json_publish_data[object_name][o.property_name] = complex_val.getvalue()
                    elif prop.is_integer():
                        json_publish_data[object_name][o.property_name] = prop.get_integer()
                    elif prop.is_timestamp():
                        json_publish_data[object_name][o.property_name] = int(prop.get_timestamp())
                    else:
                        ch_temp = bytearray(1024)
                        prop.to_string(ch_temp, 1023)
                        json_publish_data[object_name][o.property_name] = ch_temp.decode('utf-8')
            json_message_str = Json.write_string(writer_builder, json_publish_data)
            gl_verbose("publishing json message on publication {}: {}".format(pub.name, json_message_str))
            pub.HelicsPublication.publish(json_message_str)
      
        for pub in self.json_helics_endpoint_publications:
            json_publish_data.clear()
            for o in pub.json_publications:
                prop = o.prop
                if prop.is_valid():
                    object_name = o.object_name
                    if object_name not in json_publish_data:
                        json_publish_data[object_name]
                    if prop.is_double():
                        json_publish_data[object_name][o.property_name] = prop.get_double()
                    elif prop.is_complex():
                        real_part = prop.get_part("real")
                        imag_part = prop.get_part("imag")
                        val_unit = prop.get_unit()
                        complex_val.seek(0)
                        complex_val.write("{:.8f}".format(real_part))
                        if imag_part >= 0:
                            complex_val.write("+{:.8f}j".format(abs(imag_part))
                        else:
                            complex_val.write("{:.8f}j".format(imag_part))
                        if val_unit and val_unit.is_valid():
                            unit_name = str(val_unit.get_name())
                            complex_val.write(" {}".format(unit_name))
                        json_publish_data[object_name][o.property_name] = complex_val.getvalue()
                    elif prop.is_integer():
                        json_publish_data[object_name][o.property_name] = prop.get_integer()
                    elif prop.is_timestamp():
                        json_publish_data[object_name][o.property_name] = int(prop.get_timestamp())
                    else:
                        ch_temp = bytearray(1024)
                        prop.to_string(ch_temp, 1023)
                        json_publish_data[object_name][o.property_name] = ch_temp.decode('utf-8')
                    msg = helics.Message(pub.HelicsPublicationEndpoint)
                    json_message_str = Json.write_string(writer_builder, json_publish_data)
                    msg.data(json_message_str)
                    gl_verbose("sending JSON message on endpoint {}: {}".format(pub.name, json_message_str))
                    pub.HelicsPublicationEndpoint.send_message(msg)
        return 1

    def subscribe_variables(self):
        value_buffer = ""
        gld_complex_temp = gld.Complex(0.0, 0.0)
        integer_temp = 0
        double_temp = 0.0
        complex_temp = complex(0.0, 0.0)
        obj = OBJECTHDR(self)
        buf = ctypes.create_string_buffer(1024)
        sim_name = gl_name(obj, buf, 1023).decode()
        json_message = Json::Value()
        parse_err = Json::""
        json_builder = Json::CharReaderBuilder()
        value = ""
        object_name = ""
        property_name = ""
        gld_property = None
        
        for sub in self.helics_value_subscriptions:
            if sub.HelicsSubscription.isUpdated():
                try:
                    if sub.p_object_property.is_complex():
                        gl_verbose(f"helics_msg: Calling getComplex on subscription {sub.target}")
                        complex_temp = sub.HelicsSubscription.getComplex()
                        if not math.isnan(complex_temp.real) and not math.isnan(complex_temp.imag):
                            gld_complex_temp.set_real(complex_temp.real)
                            gld_complex_temp.set_imag(complex_temp.imag)
                            sub.p_object_property.setp(gld_complex_temp)
                    elif sub.p_object_property.is_integer():
                        gl_verbose(f"helics_msg: Calling getInteger on subscription {sub.target}")
                        property_type = sub.p_object_property.get_type()
                        integer_temp = sub.HelicsSubscription.getInteger()
                        if property_type == PropertyType.PT_int64:
                            sub.p_object_property.setp(integer_temp)
                        elif property_type == PropertyType.PT_int32:
                            int32_temp = ctypes.c_int32(integer_temp).value
                            sub.p_object_property.setp(int32_temp)
                        elif property_type == PropertyType.PT_int16:
                            int16_temp = ctypes.c_int16(integer_temp).value
                            sub.p_object_property.setp(int16_temp)
                    elif sub.p_object_property.is_double():
                        gl_verbose(f"helics_msg: Calling getDouble on subscription {sub.target}")
                        double_temp = sub.HelicsSubscription.getDouble()
                        if not math.isnan(double_temp):
                            sub.p_object_property.setp(double_temp)
                    else:
                        gl_verbose(f"helics_msg: Calling getString on subscription {sub.target}")
                        value_buffer = sub.HelicsSubscription.get""
                        if value_buffer:
                            value_buf = value_buffer.encode('utf-8')
                            sub.p_object_property.from_string(value_buf)
                except Exception:
                    value_buffer = ""
                    gl_verbose(f"helics_msg: Calling getString on subscription {sub.target}")
                    value_buffer = sub.HelicsSubscription.get""
                    if value_buffer:
                        value_buf = value_buffer.encode('utf-8')
                        sub.p_object_property.from_string(value_buf)
                    value_buffer = ""
        
        for sub in self.helics_endpoint_subscriptions:
            gl_verbose(f"Has message status for endpoint {sub.name}: {'True' if sub.HelicsSubscriptionEndpoint.hasMessage() else 'False'}")
            if sub.HelicsSubscriptionEndpoint.hasMessage():
                mesg = helicscpp.Message()
                pending_messages = sub.HelicsSubscriptionEndpoint.pendingMessageCount()
                for i in range(pending_messages):
                    gl_verbose(f"calling getMessage() for endpoint {sub.name}")
                    mesg = sub.HelicsSubscriptionEndpoint.getMessage()
                message_buffer = ctypes.c_char_p(mesg.c_str())
                message_size = mesg.size()
                if message_size:
                    value_buf = ctypes.create_string_buffer(message_buffer.value, message_size)
                    sub.p_object_property.from_string(value_buf.value)
        
        for sub in self.json_helics_value_subscriptions:
            if sub.HelicsSubscription.isUpdated():
                gl_verbose(f"JSON subscription {sub.target} updated.")
                value = sub.HelicsSubscription.get""
                value_length = len(value)
                jReader = json_builder.newCharReader()
                if jReader.parse(value, value + value_length, json_message, parse_err):
                    for o in json_message:
                        object_name = o.name()
                        for p in json_message[object_name]:
                            property_name = p.name()
                            buf_obj = object_name.encode('utf-8')
                            buf_prop = property_name.encode('utf-8')
                            gld_property = gld.PropertyMap(buf_obj, buf_prop)
                            if gld_property.is_valid():
                                if gld_property.is_integer():
                                    itmp = json_message[object_name][property_name].asInt64()
                                    property_type = gld_property.get_type()
                                    if property_type == PropertyType.PT_int64:
                                        gld_property.setp(itmp)
                                    elif property_type == PropertyType.PT_int32:
                                        int32_temp = ctypes.c_int32(itmp).value
                                        gld_property.setp(int32_temp)
                                    elif property_type == PropertyType.PT_int16:
                                        int16_temp = ctypes.c_int16(itmp).value
                                        gld_property.setp(int16_temp)
                                elif gld_property.is_double():
                                    dtmp = json_message[object_name][property_name].asDouble()
                                    gld_property.setp(dtmp)
                                else:
                                    stmp = json_message[object_name][property_name].as""
                                    sbuf = stmp.encode('utf-8')
                                    gld_property.from_string(sbuf)
                            else:
                                gl_error(f"helics_msg::subscribeVariables(): There is no object {object_name} with property {property_name}")
                                return 0
                else:
                    raise Exception(f"Couldn't parse the json message for HelicsSubscription {sub.target}. {parse_err}")
        
        for sub in self.json_helics_endpoint_subscriptions:
            if sub.HelicsSubscriptionEndpoint.hasMessage():
                mesg = helicscpp.Message()
                pending_messages = sub.HelicsSubscriptionEndpoint.pendingMessageCount()
                for i in range(pending_messages):
                    gl_verbose(f"calling getMessage() for endpoint {sub.name}")
                    mesg = sub.HelicsSubscriptionEndpoint.getMessage()
                message_buffer = mesg.c_str()
                message_length = len(message_buffer)
                jReader = json_builder.newCharReader()
                if jReader.parse(message_buffer, message_buffer + message_length, json_message, parse_err):
                    for o in json_message:
                        object_name = o.name()
                        for p in json_message[object_name]:
                            property_name = p.name()
                            buf_obj = object_name.encode('utf-8')
                            buf_prop = property_name.encode('utf-8')
                            gld_property = gld.PropertyMap(buf_obj, buf_prop)
                            if gld_property.is_valid():
                                if gld_property.is_integer():
                                    itmp = json_message[object_name][property_name].asInt64()
                                    property_type = gld_property.get_type()
                                    if property_type == PropertyType.PT_int64:
                                        gld_property.setp(itmp)
                                    elif property_type == PropertyType.PT_int32:
                                        int32_temp = ctypes.c_int32(itmp).value
                                        gld_property.setp(int32_temp)
                                    elif property_type == PropertyType.PT_int16:
                                        int16_temp = ctypes.c_int16(itmp).value
                                        gld_property.setp(int16_temp)
                                elif gld_property.is_double():
                                    dtmp = json_message[object_name][property_name].asDouble()
                                    gld_property.setp(dtmp)
                                else:
                                    stmp = json_message[object_name][property_name].as""
                                    sbuf = stmp.encode('utf-8')
                                    gld_property.from_string(sbuf)
                            else:
                                gl_error(f"helics_msg::subscribeVariables(): There is no object {object_name} with property {property_name}")
                                return 0
        return 1

    def publish_json_variables(self):
        obj = objecthdr(self)
        buf = ctypes.create_string_buffer(1024)
        sim_name = gl_name(obj, buf, 1023).decode("utf-8")
        json_publish_data = {}
        json_writer_builder = Json.JsonWriterBuilder()
        complex_val = StringIO()
        json_message_str = ""
        if HAVE_HELICS:
            for pub in self.json_helics_value_publications:
                json_publish_data[sim_name] = {}
                for o in pub.json_publications:
                    prop = o.prop
                    if prop.is_valid():
                        if o.object_name not in json_publish_data[sim_name]:
                            json_publish_data[sim_name][o.object_name] = {}
                        if prop.is_double():
                            json_publish_data[sim_name][o.object_name][o.property_name] = prop.get_double()
                        elif prop.is_complex():
                            real_part = prop.get_part("real")
                            imag_part = prop.get_part("imag")
                            val_unit = prop.get_unit()
                            complex_val.seek(0)
                            complex_val.truncate()
                            complex_val.write(f"{real_part:.6f}")
                            if imag_part >= 0:
                                complex_val.write(f"+{abs(imag_part):.6f}j")
                            else:
                                complex_val.write(f"{imag_part:.6f}j")
                            if val_unit and val_unit.is_valid():
                                unit_name = val_unit.get_name().decode("utf-8")
                                complex_val.write(f" {unit_name}")
                            json_publish_data[sim_name][o.object_name][o.property_name] = complex_val.get_value()
                        elif prop.is_integer():
                            json_publish_data[sim_name][o.object_name][o.property_name] = prop.get_integer()
                        elif prop.is_timestamp():
                            json_publish_data[sim_name][o.object_name][o.property_name] = prop.get_timestamp()
                        else:
                            ch_temp = ctypes.create_string_buffer(1024)
                            prop.to_string(ch_temp, 1023)
                            json_publish_data[sim_name][o.object_name][o.property_name] = ch_temp.value.decode("utf-8")
                json_message_str = Json.writeString(json_writer_builder, json_publish_data)
                pub.HelicsPublication.publish(json_message_str)
            for pub in self.json_helics_endpoint_publications:
                json_publish_data[sim_name] = {}
                for o in pub.json_publications:
                    prop = o.prop
                    if prop.is_valid():
                        if o.object_name not in json_publish_data[sim_name]:
                            json_publish_data[sim_name][o.object_name] = {}
                        if prop.is_double():
                            json_publish_data[sim_name][o.object_name][o.property_name] = prop.get_double()
                        elif prop.is_complex():
                            real_part = prop.get_part("real")
                            imag_part = prop.get_part("imag")
                            val_unit = prop.get_unit()
                            complex_val.seek(0)
                            complex_val.truncate()
                            complex_val.write(f"{real_part:.6f}")
                            if imag_part >= 0:
                                complex_val.write(f"+{abs(imag_part):.6f}j")
                            else:
                                complex_val.write(f"{imag_part:.6f}j")
                            if val_unit and val_unit.is_valid():
                                unit_name = val_unit.get_name().decode("utf-8")
                                complex_val.write(f" {unit_name}")
                            json_publish_data[sim_name][o.object_name][o.property_name] = complex_val.get_value()
                        elif prop.is_integer():
                            json_publish_data[sim_name][o.object_name][o.property_name] = prop.get_integer()
                        elif prop.is_timestamp():
                            json_publish_data[sim_name][o.object_name][o.property_name] = prop.get_timestamp()
                        else:
                            ch_temp = ctypes.create_string_buffer(1024)
                            prop.to_string(ch_temp, 1023)
                            json_publish_data[sim_name][o.object_name][o.property_name] = ch_temp.value.decode("utf-8")
                msg = helicscpp.Message(pub.HelicsPublicationEndpoint)
                json_message_str = Json.writeString(json_writer_builder, json_publish_data)
                msg.data(json_message_str)
                pub.HelicsPublicationEndpoint.sendMessage(msg)
        return 1

    def subscribe_json_variables(self):
        obj = OBJECTHDR(self)
        buf = ""
        sim_name = str(gld_helics_federate.getName())
        json_message = Json.Value()
        json_data = Json.Value()
        json_reader_builder = Json.CharReaderBuilder()
        parse_err = ""
        value = ""
        object_name = ""
        property_name = ""
        gld_property = None
    
        if HAVE_HELICS:
            for sub in self.json_helics_value_subscriptions:
                if sub.HelicsSubscription.isUpdated():
                    value = sub.HelicsSubscription.get""
                    value_length = len(value)
                    j_reader = json_reader_builder.newCharReader()
    
                    if j_reader.parse(value, value_length, json_message, parse_err):
                        if not json_message.isMember(sim_name):
                            json_data = json_message
    
                            for o in json_data:
                                object_name = o.name()
    
                                for p in json_data[object_name]:
                                    property_name = p.name()
                                    expr1 = object_name
                                    expr2 = property_name
                                    buf_obj = expr1.encode('utf-8')
                                    buf_prop = expr2.encode('utf-8')
                                    gld_property = gld_property(buf_obj, buf_prop)
    
                                    if gld_property.is_valid():
                                        if gld_property.is_integer():
                                            itmp = json_data[object_name][property_name].asInt64()
                                            property_type = gld_property.get_type()
    
                                            if property_type == PropertyType.PT_int64:
                                                gld_property.setp(itmp)
                                            elif property_type == PropertyType.PT_int32:
                                                int32_temp = int(itmp)
                                                gld_property.setp(int32_temp)
                                            elif property_type == PropertyType.PT_int16:
                                                int16_temp = int(itmp)
                                                gld_property.setp(int16_temp)
                                        elif gld_property.is_double():
                                            dtmp = json_data[object_name][property_name].asDouble()
                                            gld_property.setp(dtmp)
                                        else:
                                            stmp = json_data[object_name][property_name].as""
                                            sbuf = stmp[:1023]
                                            gld_property.from_string(sbuf)
    
                                    del gld_property
                        else:
                            json_data = json_message[sim_name]
    
                            for o in json_data:
                                object_name = o.name()
    
                                for p in json_data[object_name]:
                                    property_name = p.name()
                                    expr1 = object_name
                                    expr2 = property_name
                                    buf_obj = expr1.encode('utf-8')
                                    buf_prop = expr2.encode('utf-8')
                                    gld_property = gld_property(buf_obj, buf_prop)
    
                                    if gld_property.is_valid():
                                        if gld_property.is_integer():
                                            itmp = json_data[object_name][property_name].asInt64()
                                            property_type = gld_property.get_type()
    
                                            if property_type == PropertyType.PT_int64:
                                                gld_property.setp(itmp)
                                            elif property_type == PropertyType.PT_int32:
                                                int32_temp = int(itmp)
                                                gld_property.setp(int32_temp)
                                            elif property_type == PropertyType.PT_int16:
                                                int16_temp = int(itmp)
                                                gld_property.setp(int16_temp)
                                        elif gld_property.is_double():
                                            dtmp = json_data[object_name][property_name].asDouble()
                                            gld_property.setp(dtmp)
                                        else:
                                            stmp = json_data[object_name][property_name].as""
                                            sbuf = stmp[:1023]
                                            gld_property.from_string(sbuf)
    
                                    del gld_property
                    else:
                        raise Exception(f"Couldn't parse the json message for HelicsSubscription {sub.target}. {parse_err}")
    
            for sub in self.json_helics_endpoint_subscriptions:
                if sub.HelicsSubscriptionEndpoint.hasMessage():
                    mesg = helicscpp.Message()
                    pending_messages = sub.HelicsSubscriptionEndpoint.pendingMessageCount()
    
                    for i in range(pending_messages):
                        gl_verbose(f"calling getMessage() for endpoint {sub.name}")
                        mesg = sub.HelicsSubscriptionEndpoint.getMessage()
    
                    message_buffer = str(mesg.c_str())
                    message_length = len(message_buffer)
                    j_reader = json_reader_builder.newCharReader()
    
                    if j_reader.parse(message_buffer, message_length, json_message, parse_err):
                        if not json_message.isMember(sim_name):
                            json_data = json_message
    
                            for o in json_data:
                                object_name = o.name()
    
                                for p in json_data[object_name]:
                                    property_name = p.name()
                                    expr1 = object_name
                                    expr2 = property_name
                                    buf_obj = expr1.encode('utf-8')
                                    buf_prop = expr2.encode('utf-8')
                                    gld_property = gld_property(buf_obj, buf_prop)
    
                                    if gld_property.is_valid():
                                        if gld_property.is_integer():
                                            itmp = json_data[object_name][property_name].asInt64()
                                            property_type = gld_property.get_type()
    
                                            if property_type == PropertyType.PT_int64:
                                                gld_property.setp(itmp)
                                            elif property_type == PropertyType.PT_int32:
                                                int32_temp = int(itmp)
                                                gld_property.setp(int32_temp)
                                            elif property_type == PropertyType.PT_int16:
                                                int16_temp = int(itmp)
                                                gld_property.setp(int16_temp)
                                        elif gld_property.is_double():
                                            dtmp = json_data[object_name][property_name].asDouble()
                                            gld_property.setp(dtmp)
                                        else:
                                            stmp = json_data[object_name][property_name].as""
                                            sbuf = stmp[:1023]
                                            gld_property.from_string(sbuf)
    
                                    del gld_property
                        else:
                            json_data = json_message[sim_name]
    
                            for o in json_data:
                                object_name = o.name()
    
                                for p in json_data[object_name]:
                                    property_name = p.name()
                                    expr1 = object_name
                                    expr2 = property_name
                                    buf_obj = expr1.encode('utf-8')
                                    buf_prop = expr2.encode('utf-8')
                                    gld_property = gld_property(buf_obj, buf_prop)
    
                                    if gld_property.is_valid():
                                        if gld_property.is_integer():
                                            itmp = json_data[object_name][property_name].asInt64()
                                            property_type = gld_property.get_type()
    
                                            if property_type == PropertyType.PT_int64:
                                                gld_property.setp(itmp)
                                            elif property_type == PropertyType.PT_int32:
                                                int32_temp = int(itmp)
                                                gld_property.setp(int32_temp)
                                            elif property_type == PropertyType.PT_int16:
                                                int16_temp = int(itmp)
                                                gld_property.setp(int16_temp)
                                        elif gld_property.is_double():
                                            dtmp = json_data[object_name][property_name].asDouble()
                                            gld_property.setp(dtmp)
                                        else:
                                            stmp = json_data[object_name][property_name].as""
                                            sbuf = stmp[:1023]
                                            gld_property.from_string(sbuf)
    
                                    del gld_property
                    else:
                        raise Exception(f"Couldn't parse the json message for HelicsEndpoint {sub.name}. {parse_err}")
    
        return 1
