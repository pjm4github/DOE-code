from gov_pnnl_goss.gridlab.connection.Connection import ET_GROUPOPEN, ET_GROUPCLOSE, ETO_QUOTES, MESSAGEFLAG
from gov_pnnl_goss.gridlab.connection.Native import Native
from gov_pnnl_goss.gridlab.gldcore.GridLabD import PC_PRETOPDOWN, PC_BOTTOMUP, PC_POSTTOPDOWN, gl_debug, gl_error, \
    gl_publish_variable, gl_warning
from gov_pnnl_goss.gridlab.gldcore.Property import PROPERTYTYPE


class JSONTYPE:
    JT_VOID = 0
    JT_LIST = 1
    JT_REAL = 2
    JT_INTEGER = 3
    JT_STRING = 4


class JSONLIST:
    def __init__(self):
        self.type = JSONTYPE.JT_VOID
        self.tag = ""
        self.real = 0.0
        self.integer = 0
        self.list = None
        self.string = ""
        self.parent = None
        self.next = None


def json_translate(local, local_len, remote, remote_len, flag):
    raise Exception("obsolete code used")
    # def convert(remote, var):
    #     if var.dir == "DXD_READ":
    #         name = bytearray(1024)
    #         value = bytearray(1024)
    #         len = ctypes.c_size_t()
    #         if ctypes.CFUNCTYPE(remote, "<property><name>%1024[^<]</name><value>%1024[^<]</value></property>", name,
    #                             value) != 2:
    #             gl_error(
    #                 f"json_translate(char *remote='{remote}',VARMAP *var->local_name='{var.local_name}'): remote data format is not correct")
    #             return 0
    #         elif len.value > local_len:
    #             gl_error(
    #                 f"json_translate(char *remote='{remote}',VARMAP *var->local_name='{var.local_name}'): remote data too big for local value")
    #             return 0
    #         elif name != var.local_name:
    #             gl_error(
    #                 f"json_translate(char *remote='{remote}',VARMAP *var->local_name='{var.local_name}'): local name does not match remote data")
    #             return 0
    #         else:
    #             local = value.decode('utf-8')
    #             return len.value

    # // translates data to cache
    # int json_translate(char *local, size_t local_len, char *remote, size_t remote_len, TRANSLATIONFLAG flag, ...)
    # {
    # 	throw "obsolete code used";
    # 	va_list ptr;
    # 	va_start(ptr,flag);
    # 	if ( flag==TF_DATA ) // default is data
    # 	{
    # 		VARMAP *var = va_arg(ptr,VARMAP*);
    # 		if ( var->dir==DXD_READ ) // from remote to local
    # 		{
    # 			char name[1024];
    # 			char value[1024];
    # 			size_t len;
    # 			if ( sscanf(remote,"<property><name>%1024[^<]</name><value>%1024[^<]</value></property>",name,value)!=2 )
    # 			{
    # 				gl_error("json_translate(char *remote='%s',VARMAP *var->local_name='%s'): remote data format is not correct",remote,var->local_name);
    # 				return 0;
    # 			}
    # 			else if ( (len=strlen(value))>local_len )
    # 			{
    # 				gl_error("json_translate(char *remote='%s',VARMAP *var->local_name='%s'): remote data too big for local value",remote,var->local_name);
    # 				return 0;
    # 			}
    # 			else if ( strcmp(name,var->local_name)!=0 )
    # 			{
    # 				gl_error("json_translate(char *remote='%s',VARMAP *var->local_name='%s'): local name does not match remote data",remote,var->local_name);
    # 				return 0;
    # 			}
    # 			else
    # 			{
    # 				strcpy(local,value);
    # 				// TODO recursively process remaining payload in remote if varmap contains a next item
    # 				return (int)len;
    # 			}
    # 		}
    # 		else if ( var->dir==DXD_WRITE ) // from local to remote
    # 		{
    # 			return sprintf(remote,"<property><name>%s</name><value>%s</value></property>",var->remote_name,local);
    # 		}
    # 		else
    # 			throw "json_translate(...): invalid DATAEXCHANGEDIR";
    # 	}
    # 	else if ( flag==TF_SCHEMA )
    # 	{
    # 		return -1; // TODO implement schema translations
    # 	}
    # 	else if ( flag==TF_TUPLE )
    # 	{
    # 		return -1; // TODO implement tuple translation
    # 	}
    # 	else
    # 		throw "json_translate(...): invalid flags";
    # 	va_end(ptr);
    # }


def json_export(transport, tag, v, vlen, options):
    if v == None:
        if transport.get_size() < 2:
            transport.error("json_export(): export buffer overrun")
            return -1
        if vlen == ET_GROUPOPEN:
            if tag == None:
                return transport.message_append("%s", "{")
            else:
                return transport.message_append("\"%s\": {", tag)
        elif vlen == ET_GROUPCLOSE:
            return transport.message_append("%s", "}")
        else:
            transport.error("json_export(): invalid group control code %d", vlen)
            return -1
    else:
        if vlen > transport.get_size():
            transport.error("json_export(): export buffer overrun")
            return -1
        elif options & ETO_QUOTES:
            return transport.message_append(R'("%s": "%s")', tag, v)
        else:
            return transport.message_append("\"%s\": %s", tag, v)


def json_translator(buffer, translation=None):
    if translation is not None:
        Json.destroy(translation)
    return Json.parse(buffer)


def json_import(transport, tag, v, vlen, options):
    """
    :param transport:
    :param tag:		// NULL for group close, name for group open (or NULL if none)
    :param v:       // NULL for group open/close
    :param vlen:    // 0 for match only on read (ignored on export)
    			    // -1 for group begin
 				    // -2 for group end
    :param options: // ETO_QUOTES enclose value in quotes
    :return:
    """

    # 	// test sequence
    # 	//JSONLIST *data = json::parse("{\"method\" : \"init\", \"params\" : {\"application\" : \"gridlabd\", \"version\" : 3.0, \"modelname\" : \"modelname.glm\"}, \"id\" : 1}");
    # 	//char *method = json::get(data,"method");
    # 	//char *id = json::get(data,"id");
    # 	//char *version = json::get(data,"version");
    # 	//char *application = json::get(data,"application");
    # 	//char *modelname = json::get(data,"modelname");
    # 	//gl_debug("method=%s; id=%s; version=%s; application=%s; modelname=%s", method,id,version,application,modelname);
    # 	//JSONLIST *params = json::find(data,"params");
    # 	//version = json::get(params,"version");
    # 	//application = json::get(params,"application");
    # 	//modelname = json::get(params,"modelname");
    # 	//gl_debug("method=%s; id=%s; version=%s; application=%s; modelname=%s", method,id,version,application,modelname);
    # 	//	JSONLIST *data = json::parse(transport->get_input());
    # 	// TODO extract data

    translation = transport.get_translation()
    if translation is None:
        transport.set_translator(json_translator)
        translation = json_translator(transport.get_input())
        transport.set_translation(translation)

    if tag is None:
        return 1

    value = Json.get(translation, tag)
    if value is None:
        gl_error("json_import(tag='%s',...) tag not found in incoming data", tag)
        return 0

    if v is None:
        return 1

    if vlen == 0:
        if v == value:
            return 1
        gl_error("json_import(tag='%s',...) incoming value '%s' did not match expected/required value '%s'", tag, value,
                 v)
        return 0
    elif len(value) < vlen:
        v = value
        return 1
    else:
        gl_error("json_import(tag='%s',...) incoming longer than %d bytes allowed", tag, vlen)
        return 0


def json_new_list(tail=None):
    list = JSONLIST()
    list.__init__(0, 0, 0, None)  # Assuming the JSONLIST class constructor takes 4 arguments
    if tail is not None:
        tail.next = list
        list.parent = tail.parent
    return list


def json_new_sublist(parent):
    list = json_new_list()
    list.parent = parent
    parent.list = list
    return list


def json_read_number(item):
    if item.type == JSONTYPE.JT_REAL:
        item.real = float(item.string)
    elif item.type == JSONTYPE.JT_INTEGER:
        item.integer = int(item.string)
    else:
        gl_warning("json_read_number(JSONLIST item={string:'%s',...}): ignoring attempt to read non-number type" % item.string)


def json_dump(item, indent=0):
    indentchars = ' ' * indent
    if indent == 0:
        print('{')
    while item is not None:
        if item.type == JSONTYPE.JT_LIST:
            print(f'{indentchars}"{item.tag}": {{')
            json_dump(item.list, indent + 1)
            print(f'{indentchars}}}')
        elif item.type == JSONTYPE.JT_STRING:
            print(f'{indentchars}"{item.tag}": "{item.string}"{"," if item.next is not None else ""}')
        elif item.type == JSONTYPE.JT_VOID:
            print(f'{indentchars}"{item.tag}": (void){"," if item.next is not None else ""}')
        else:
            print(f'{indentchars}"{item.tag}": {item.string}{"," if item.next is not None else ""}')
        item = item.next
    if indent == 0:
        print('}')



class Json(Native):
    version = GL_ATOMIC(float, 0.0)
    oclass = CLASS(classname="json")

    def __init__(self, module):
        super().__init__(module)
        # TODO: Add published properties here
        self.oclass = None
        self.defaults = Json.oclass
        self.oclass = gl_create(module, "json", 0, PC_AUTOLOCK | PC_PRETOPDOWN | PC_BOTTOMUP | PC_POSTTOPDOWN | PC_OBSERVER)
        if self.oclass == None:
            raise Exception("connection/json::__init__: unable to register class connection:json")
        else:
            self.oclass.trl = TRL_UNKNOWN
        self.defaults = self
        if gl_publish_variable(self.oclass,
                              PROPERTYTYPE.PT_INHERIT,
                              "native",
                              PROPERTYTYPE.PT_double,
                              "version",
                              get_version_offset(),
                              PROPERTYTYPE.PT_DESCRIPTION,
                              "json version",
                              None) < 1:
            raise Exception("connection/json::__init__: unable to publish properties of connection:json")
        if not gl_publish_load_method(self.oclass, "link", loadmethod_json_link):
            raise Exception("connection/json::__init__: unable to publish link method of connection:json")
        if not gl_publish_load_method(self.oclass, "option", loadmethod_json_option):
            raise Exception("connection/json::__init__: unable to publish option method of connection:json")

    def create(self):
        version = 1.0
        return super().create()

    def init(self, parent):
        super().init(parent, json_translate)

        if self.get_connection() == None:
            gl_error("connection options not specified")
            return 0

        self.get_connection().set_translators(json_export, json_import, json_translate)
        self.get_connection().get_transport().set_delimiter(", ")
        self.get_connection().get_transport().set_message_format("JSON")
        self.get_connection().get_transport().set_message_version(1.0)

        if self.get_connection().init() == 0:
            return 0

        appname = PACKAGE
        appversion = MAJOR + 0.1 * MINOR
        modelname = gld_global("modelname")
        name = modelname.to_string(sizeof(name) - 1)
        id = 0

        if self.get_connection().client_initiated(
                MESSAGEFLAG.MSG_CRITICAL,
                MESSAGEFLAG.MSG_INITIATE,
                MESSAGEFLAG.MSG_TAG, "method", "init",
                MESSAGEFLAG.MSG_OPEN, "params",
                MESSAGEFLAG.MSG_STRING, "application", sizeof(appname) - 1, appname,
                MESSAGEFLAG.MSG_REAL, "version", appversion,
                MESSAGEFLAG.MSG_STRING, "modelname", sizeof(name), name,
                MESSAGEFLAG.MSG_CLOSE,
                MESSAGEFLAG.MSG_COMPLETE, id,
                None) < 0:
            gl_error("handshake initiation failed")
            return 0

        if self.get_connection().server_response(
                MESSAGEFLAG.MSG_CRITICAL,
                MESSAGEFLAG.MSG_INITIATE,
                MESSAGEFLAG.MSG_TAG, "result", "init",
                MESSAGEFLAG.MSG_COMPLETE, id,
                None) < 0:
            gl_error("handshake response failed")
            return 0

        if self.get_connection().client_initiated(
                MESSAGEFLAG.MSG_CRITICAL,
                MESSAGEFLAG.MSG_INITIATE,
                MESSAGEFLAG.MSG_TAG, "method", "input",
                MESSAGEFLAG.MSG_OPEN, "schema",
                MESSAGEFLAG.MSG_SCHEMA, DXD_READ,
                MESSAGEFLAG.MSG_CLOSE,
                MESSAGEFLAG.MSG_COMPLETE, id,
                None) < 0:
            gl_error("schema exchange failed")
            return 0

        if self.get_connection().server_response(
                MESSAGEFLAG.MSG_CRITICAL,
                MESSAGEFLAG.MSG_INITIATE,
                MESSAGEFLAG.MSG_TAG, "result", "input",
                MESSAGEFLAG.MSG_COMPLETE, id,
                None) < 0:
            gl_error("handshake response failed")
            return 0

        if get_connection().client_initiated(
                MESSAGEFLAG.MSG_CRITICAL,
                MESSAGEFLAG.MSG_INITIATE,
                MESSAGEFLAG.MSG_TAG, "method", "output",
                MESSAGEFLAG.MSG_OPEN, "schema",
                MESSAGEFLAG.MSG_SCHEMA, DXD_WRITE,
                MESSAGEFLAG.MSG_CLOSE,
                MESSAGEFLAG.MSG_COMPLETE, id,
                None) < 0:
            gl_error("schema exchange failed")
            return 0

        if get_connection().server_response(
                MESSAGEFLAG.MSG_CRITICAL,
                MESSAGEFLAG.MSG_INITIATE,
                MESSAGEFLAG.MSG_TAG, "result", "output",
                MESSAGEFLAG.MSG_COMPLETE, id,
                None) < 0:
            gl_error("handshake response failed")
            return 0

        return self.get_connection().update(self.get_initmap(), "start", &json_translate) >= 0

    # def link(self, value):
    #     return native.link(value)
    def link(self, value):
        return 0


    def option(self, value):
        target = ""
        command = ""

        if sscanf(value, "%[^:]:%[^\n]", target, command) == 2:
            gl_verbose("connection/json::option(char *value='%s') parsed ok", value)
            return native.option(target, command)
        else:
            gl_error("connection/json::option(char *value='%s'): unable to parse option argument", value)
            return 0

    # def precommit(self, timestamp):
    #     return timestamp
    def precommit(self, t):
        return native.precommit(t)

    # def presync(self, t):
    #     return native.presync(t)
    def presync(self, timestamp):
        return timestamp

    def sync(self, timestamp):
        return timestamp

    def postsync(self, timestamp):
        return timestamp

    # def commit(self, t0, t1):
    #     return native.commit(t0, t1)
    #     #
    def commit(self, t1, t2):
        return t2

    # def prenotify(self, property, value):
    #     return native.prenotify(property, value)
    # #
    def prenotify(self, prop, value):
        return 0


    # def post_notify(self, p, v):
    #     return native.post_notify(p, v)
    def postnotify(self, prop, value):
        return 0

    # def finalize(self):
    #     return native.finalize()
    def finalize(self):
        return 0

    def plc(self, timestamp):
        return timestamp

    # def term(self, t):
    #     return native.term(t)
    def term(self, timestamp):
        pass
        # TODO: Add other event handlers here

    #
    # def parse(buffer):
    #     head = json_new_list()
    #     tail = head
    #     tail.next = None
    #     nest = 0
    #     state = "START"
    #     for p in buffer:
    #         if state == "START":
    #             if p.isspace():
    #                 pass
    #             elif p == "{":
    #                 nest += 1
    #                 state = "TAG0"
    #             else:
    #                 Syntax()
    #         elif state == "TAG0":
    #             if p.isspace():
    #                 pass
    #             elif p == '"':
    #                 state = "TAG"
    #                 t = tail.tag
    #             else:
    #                 Syntax()
    #         elif state == "TAG":
    #             if p == '"':
    #                 t = None
    #                 state = "COLON"
    #             else:
    #                 t += p
    #         elif state == "COLON":
    #             if p.isspace():
    #                 pass
    #             elif p == ':':
    #                 state = "PARAM"
    #                 t = tail.string
    #             else:
    #                 Syntax()
    #         elif state == "PARAM":
    #             if p.isspace():
    #                 pass
    #             elif p == '"':
    #                 state = "STRING"
    #                 tail.type = "JT_STRING"
    #             elif p.isdigit() or p == '-' or p == '+' or p == '.':
    #                 t += p
    #                 state = "NUMBER"
    #                 tail.type = "JT_INTEGER"
    #             elif p == '{':
    #                 nest += 1
    #                 state = "TAG0"
    #                 tail.type = "JT_LIST"
    #                 tail = json_new_sublist(tail)
    #             else:
    #                 Syntax()
    #
    #         elif state == "STRING":
    #             if p == '"':
    #                 state = "COMMA"
    #                 t = None
    #             else:
    #                 t += p
    #         elif state == "NUMBER":
    #             if p.isspace() or p == ',' or p == '}':
    #                 t = None
    #                 p -= 1
    #                 state = "COMMA"
    #                 json_read_number(tail)
    #             elif tail.type == "JT_INTEGER" and p == '.':
    #                 t += p
    #                 tail.type = "JT_REAL"
    #             elif p.isdigit():
    #                 t += p
    #             else:
    #                 Syntax()
    #         elif state == "COMMA":
    #             if p.isspace():
    #                 pass
    #             elif p == '}':
    #                 state = "END" if (nest == 0) else "COMMA"
    #                 tail = tail.parent
    #             elif p == ',':
    #                 state = "TAG0"
    #                 tail = json_new_list(tail)
    #             else:
    #                 Syntax()
    #         elif state == "END":
    #             if p.isspace():
    #                 pass
    #             else:
    #                 Syntax()
    #         else:
    #             gl_error(f"json::parse(char *buffer='{buffer}'): parser state error at position {buffer.index(p)}")
    #             Error()
    #
    #     gl_debug("json parse dump...")
    #     json_dump(head)
    #     return head

    def parse(self, buffer):
        head = JSONLIST()
        tail = head
        tail.next = None
        nest = 0
        state = "START"
        p = 0
        t = ""

        def json_new_list(parent):
            new_list = JSONLIST()
            new_list.parent = parent
            return new_list

        def json_new_sublist(parent):
            new_sublist = JSONLIST()
            new_sublist.parent = parent
            parent.list = new_sublist
            return new_sublist

        def json_read_number(item):
            if item.type == JSONTYPE.JT_INTEGER:
                item.integer = int(item.string)
            elif item.type == JSONTYPE.JT_REAL:
                item.real = float(item.string)

        while p < len(buffer):
            if state == "START":
                if buffer[p].isspace():
                    pass
                elif buffer[p] == '{':
                    nest += 1
                    state = "TAG0"
                else:
                    break
            elif state == "TAG0":
                if buffer[p].isspace():
                    pass
                elif buffer[p] == '"':
                    state = "TAG"
                    t = tail.tag
                else:
                    break
            elif state == "TAG":
                if buffer[p] == '"':
                    t = ""
                    state = "COLON"
                else:
                    t += buffer[p]
            elif state == "COLON":
                if buffer[p].isspace():
                    pass
                elif buffer[p] == ':':
                    state = "PARAM"
                    t = tail.string
                else:
                    break
            elif state == "PARAM":
                if buffer[p].isspace():
                    pass
                elif buffer[p] == '"':
                    state = "STRING"
                    tail.type = JSONTYPE.JT_STRING
                elif buffer[p].isdigit() or buffer[p] == '-' or buffer[p] == '+' or buffer[p] == '.':
                    t += buffer[p]
                    state = "NUMBER"
                    tail.type = JSONTYPE.JT_INTEGER
                elif buffer[p] == '{':
                    nest += 1
                    state = "TAG0"
                    tail.type = JSONTYPE.JT_LIST
                    tail = json_new_sublist(tail)
                else:
                    break
            elif state == "STRING":
                if buffer[p] == '"':
                    t = ""
                    state = "COMMA"
                else:
                    t += buffer[p]
            elif state == "NUMBER":
                if buffer[p].isspace() or buffer[p] == ',' or buffer[p] == '}':
                    t = ""
                    p -= 1
                    state = "COMMA"
                    json_read_number(tail)
                elif tail.type == JSONTYPE.JT_INTEGER and buffer[p] == '.':
                    t += buffer[p]
                    tail.type = JSONTYPE.JT_REAL
                elif buffer[p].isdigit():
                    t += buffer[p]
                else:
                    break
            elif state == "COMMA":
                if buffer[p].isspace():
                    pass
                elif buffer[p] == '}':
                    nest -= 1
                    state = "END" if nest == 0 else "COMMA"
                    tail = tail.parent
                elif buffer[p] == ',':
                    state = "TAG0"
                    tail = json_new_list(tail)
                else:
                    break
            elif state == "END":
                if buffer[p].isspace():
                    pass
                else:
                    break
            else:
                gl_error(f"json_parse: parser state error at position {p}")
                return None
            p += 1

        gl_debug("json parse dump...")
        json_dump(head)
        return head

    # @staticmethod
    # def find(list, tag):
    #     return None
    def find(self, json_list, tag):
        if json_list is None:
            return None
        if json_list.tag == tag:
            return json_list
        sub = self.find(json_list.list, tag) if json_list.type == JSONTYPE.JT_LIST else None
        if sub is not None:
            return sub
        return self.find(json_list.next, tag)

    def get(self, list, tag):
        found = self.find(list, tag)
        return found.string if found else None

    def destroy(self, json_list):
        if json_list is not None:
            if json_list.type == JSONTYPE.JT_LIST:
                self.destroy(json_list.list)
            self.destroy(json_list.next)
            del json_list
