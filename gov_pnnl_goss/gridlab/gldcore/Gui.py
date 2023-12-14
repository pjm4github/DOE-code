import os
from enum import Enum
import sys
import ctypes
from gov_pnnl_goss.gridlab.gldcore.Class import Class
from gov_pnnl_goss.gridlab.gldcore.Cmex import object_set_value_by_name
from gov_pnnl_goss.gridlab.gldcore.Convert import output_error
from gov_pnnl_goss.gridlab.gldcore.Globals import global_setvar, FAILED, global_find
from gov_pnnl_goss.gridlab.gldcore.Output import output_verbose, output_warning, output_error_raw


class GUIENTITYTYPE(Enum):
    GUI_UNKNOWN = 0,
    GUI_ROW = 1,
    GUI_TAB = 2,
    GUI_PAGE = 3,
    GUI_GROUP = 4,
    GUI_SPAN = 5,
    _GUI_GROUPING_END = 6,
    GUI_TITLE = 7,
    GUI_STATUS = 8,
    GUI_TEXT = 9,
    _GUI_LABELING_END = 10,
    GUI_INPUT = 11,
    GUI_CHECK = 12,
    GUI_RADIO = 13,
    GUI_SELECT = 14,
    _GUI_INPUT_END = 15,
    GUI_BROWSE = 16,
    GUI_TABLE = 17,
    GUI_GRAPH = 18,
    _GUI_OUTPUT_END = 19,
    GUI_ACTION = 20,
    _GUI_ACTION_END = 21


class GUIACTIONSTATUS(Enum):
    GUIACT_NONE = 0
    GUIACT_WAITING = 1
    GUIACT_PENDING = 2
    GUIACT_HALT = 3


class GUIStreamFn:
    def __call__(self, ref, message, *args):
        pass




class GUIEntity:
    gui_root = None
    gui_last = None
    def __init__(self):
        self.action = ""
        self.action_status = GUIACTIONSTATUS.GUIACT_NONE
        self.data = None
        self.env = ""
        self.fp = None
        self.globalname = ""
        self.gnuplot = ""
        self.height = 0
        self.hold = 0
        self.next = None
        self.obj = None
        self.objectname = ""
        self.options = ""
        self.parent = None
        self.prop = None
        self.propertyname = ""
        self.size = 0
        self.source = ""
        self.span = 0
        self.srcref = ""
        self.type = GUIENTITYTYPE.GUI_UNKNOWN
        self.unit = None
        self.value = ""
        self.var = None
        self.wait_for = ""
        self.wait_status = GUIACTIONSTATUS.GUIACT_NONE
        self.width = 0

    def gui_default_stream(self, ref, format, *args):
        if ref is None:
            ref = sys.stdout
        libc = ctypes.CDLL(None)
        vfprintf = libc.vfprintf
        vfprintf.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]
        vfprintf.restype = ctypes.c_int
        len = vfprintf(ctypes.c_void_p(id(ref)), format.encode(), args)
        return len

    def gui_set_html_stream(self, ref, stream):
        gui_html_output = stream
        fp = ref

    def gui_get_root(self):
        return self.gui_root

    def gui_get_last(self):
        return self.gui_last

    def gui_create_entity(self):
        entity = gui_last
        if entity is None or entity.type != GUIENTITYTYPE.GUI_UNKNOWN:
            entity = GUIENTITY()
        if entity is None:
            return None
        entity = GUIENTITY()
        memset(entity, 0, sizeof(GUIENTITY))
        if gui_root is None:
            gui_root = entity
        if gui_last is not None:
            gui_last.next = entity
        gui_last = entity
        return entity

    def gui_get_type(self, entity):
        return self.entity.type

    def gui_glm_typename(self, type):
        type_name = [
            None,
            "row", "tab", "page", "group", "span", None,
            "title", "status", "text", None,
            "input", "check", "radio", "select", "action", None,
            "browse", "table", "graph", None,
            None
        ]
        if type >= 0 and type < len(type_name):
            return type_name[type]
        else:
            return None

    def gui_glm_write_all(self, fp):
        pass

    def gui_get_typename(self, entity):
        type_mapping = {
            0: GUIENTITYTYPE.GUI_UNKNOWN,
            1: GUIENTITYTYPE.GUI_ROW,
            2: GUIENTITYTYPE.GUI_TAB,
            3: GUIENTITYTYPE.GUI_PAGE,
            4: GUIENTITYTYPE.GUI_GROUP,
            5: GUIENTITYTYPE.GUI_SPAN,
            6: GUIENTITYTYPE._GUI_GROUPING_END,
            7: GUIENTITYTYPE.GUI_TITLE,
            8: GUIENTITYTYPE.GUI_STATUS,
            9: GUIENTITYTYPE.GUI_TEXT,
            10: GUIENTITYTYPE.GUI_INPUT,
            11: GUIENTITYTYPE.GUI_CHECK,
            12: GUIENTITYTYPE.GUI_RADIO,
            13: GUIENTITYTYPE.GUI_SELECT,
            14: GUIENTITYTYPE.GUI_ACTION
        }
        return type_mapping.get(entity.type, "<INVALID>")

    def gui_is_header(self, entity):
        return entity.type in [
            GUIENTITYTYPE.GUI_TITLE,
            GUIENTITYTYPE.GUI_STATUS,
        ]

    def gui_is_grouping(self, entity):
        return entity.type in [
            GUIENTITYTYPE.GUI_ROW,
            GUIENTITYTYPE.GUI_TAB,
            GUIENTITYTYPE.GUI_PAGE,
            GUIENTITYTYPE.GUI_GROUP,
            GUIENTITYTYPE.GUI_SPAN,
        ]

    def gui_is_labeling(self, entity):
        return entity.type in [
            GUIENTITYTYPE.GUI_TITLE,
            GUIENTITYTYPE.GUI_STATUS,
            GUIENTITYTYPE.GUI_TEXT,
        ]

    def gui_is_input(self, entity):
        return entity.type in [
            GUIENTITYTYPE.GUI_INPUT,
            GUIENTITYTYPE.GUI_CHECK,
            GUIENTITYTYPE.GUI_RADIO,
            GUIENTITYTYPE.GUI_SELECT,
        ]

    def gui_is_output(self, entity):
        return entity.type in [
            GUIENTITYTYPE.GUI_BROWSE,
            GUIENTITYTYPE.GUI_TABLE,
            GUIENTITYTYPE.GUI_GRAPH,
        ]

    def gui_is_action(self, entity):
        return entity.type in [GUIENTITYTYPE.GUI_ACTION]

    def gui_set_srcref(self, entity, filename, linenum):
        entity.srcref = f"{filename}:{linenum}"

    def gui_set_type(self, entity, type):
        entity.type = type

    def gui_set_value(self, entity, value):
        entity.value = value[:min(len(value), len(entity.value))]

    def gui_set_variablename(self, entity, global_name):
        entity.global_name = global_name[:len(entity.global_name)] if len(global_name) < len(
            entity.global_name) else global_name

    def gui_set_objectname(self, entity, objectname):
        entity.objectname = objectname

    # def gui_set_objectname(self, entity, objectname):
    #     entity.data = None
    #     entity.objectname = objectname[:len(entity.objectname)]

    def gui_set_propertyname(self, entity, property_name):
        entity.data = None
        entity.property_name = property_name[:len(entity.property_name)] if len(property_name) > len(
            entity.property_name) else property_name

    def gui_set_span(self, entity, span):
        entity.span = span

    def gui_set_unit(self, entity, unit):
        entity.unit = unit
    # def gui_set_unit(entity, unit):
    #     entity.unit = unit_find(unit)
    #

    def gui_set_next(self, entity, next):
        entity.next = next

    def gui_set_parent(self, entity, parent):
        entity.parent = parent

    def gui_set_source(self, entity, source):
        entity.source = source[:len(entity.source)] if len(source) >= len(entity.source) else source

    def gui_set_options(self, entity, options):
        entity.options = options

    # def gui_set_options(entity, options):
    #     entity.options = options[:sizeof(entity.options)]

    def gui_set_wait(self, entity, wait):
        entity.wait_for = wait

    # def gui_set_wait(entity, wait):
    #     entity.wait_for = wait[:len(entity.wait_for)]
    #

    def gui_get_dump(self, entity):
        buffer = "{type=%s,srcref='%s',value='%s',globalname='%s',object='%s',property='%s',action='%s',span=%d}" % (
            self.gui_get_typename(entity), entity.srcref, entity.value, entity.globalname, entity.objectname,
            entity.propertyname, entity.action, entity.span)
        return buffer

    def gui_get_parent(self, entity):
        return entity.parent

    def gui_get_next(self, entity):
        return entity.next

    def gui_get_value(self, entity):
        obj = gui_get_object(entity)
        buffer = [64]
        if obj:
            if entity.property_name == "name":
                entity.value = object_name(obj, buffer, 63)
            elif entity.property_name == "class":
                entity.value = obj.oclass.name
            elif entity.property_name == "parent":
                entity.value = object_name(obj.parent, buffer, 63) if obj.parent else ""
            elif entity.property_name == "rank":
                entity.value = str(obj.rank)
            elif entity.property_name == "clock":
                convert_from_timestamp(obj.clock, entity.value, len(entity.value))
            elif entity.property_name == "valid_to":
                convert_from_timestamp(obj.valid_to, entity.value, len(entity.value))
            elif entity.property_name == "in_svc":
                convert_from_timestamp(obj.in_svc, entity.value, len(entity.value))
            elif entity.property_name == "out_svc":
                convert_from_timestamp(obj.out_svc, entity.value, len(entity.value))
            elif entity.property_name == "latitude":
                convert_from_latitude(obj.latitude, entity.value, len(entity.value))
            elif entity.property_name == "longitude":
                convert_from_longitude(obj.longitude, entity.value, len(entity.value))
            elif not object_get_value_by_name(obj, entity.property_name, entity.value, len(entity.value)):
                output_error_raw("%s: ERROR: %s refers to a non-existent property '%s'", entity.srcref,
                                 gui_get_typename(entity), entity.property_name)
        elif gui_get_variable(entity):
            entity.var = global_find(entity.global_name)
            global_getvar(entity.global_name, entity.value, len(entity.value))
        elif gui_get_environment(entity):
            entity.value = entity.env
        return entity.value

    def gui_get_object(self, entity):
        if not entity.obj:
            entity.obj = object_find_name(entity.object_name)
        return entity.obj

    def gui_get_property(self, entity):
        if entity.prop == None:
            if self.gui_get_object(entity):
                entity.prop = Class.class_find_property(entity.obj.oclass, entity.propertyname)
            elif gui_get_variable(entity):
                entity.prop = entity.var.prop
        return entity.prop

    def gui_get_name(self, entity):
        if self.gui_get_object(entity):
            buffer = "{}.{}".format(entity.objectname, entity.propertyname)
            return buffer
        elif gui_get_variable(entity):
            return entity.var.prop.name
        else:
            return ""

    def gui_get_data(self, entity):
        if entity.data is None:
            if self.gui_get_object(entity):
                entity.data = object_get_addr(entity.obj, entity.propertyname)
            elif self.gui_get_variable(entity):
                entity.data = entity.var.prop.addr
            else:
                entity.data = None
        return entity.data

    def gui_get_variable(self, entity):
        if entity.var is None:
            entity.var = global_find(entity.global_name)
        return entity.var

    def gui_get_environment(self, entity):
        if entity.env is None:
            entity.env = os.getenv(entity.globalname)
        return entity.env

    def gui_get_span(self, entity):
        return entity.span

    def gui_get_unit(self, entity):
        return entity.unit

    def gui_post_action(self, action):
        if action == "quit":
            return -1
        if action == "continue":
            self.wait_status = GUIACTIONSTATUS.GUIACT_PENDING
            return 1
        for entity in self.gui_root:
            pass
        return 0

    def gui_cmd_entity(self, item, entity):
        gui_type = entity.type
        if gui_type == GUIENTITYTYPE.GUI_TITLE:
            print(self.gui_get_value(entity), end=' ')
        elif gui_type == GUIENTITYTYPE.GUI_STATUS:
            pass
        elif gui_type == GUIENTITYTYPE.GUI_ROW:
            if item > 0:
                print("\n%2d. " % item, end='')
            return 1
        elif gui_type == GUIENTITYTYPE.GUI_TAB:
            pass
        elif gui_type == GUIENTITYTYPE.GUI_PAGE:
            pass
        elif gui_type == GUIENTITYTYPE.GUI_GROUP:
            pass
        elif gui_type == GUIENTITYTYPE.GUI_SPAN:
            pass
        elif gui_type == GUIENTITYTYPE.GUI_TEXT:
            print(self.gui_get_value(entity), end=' ')
        elif gui_type == GUIENTITYTYPE.GUI_INPUT:
            print("[%s] " % self.gui_get_value(entity), end='')
        elif gui_type == GUIENTITYTYPE.GUI_CHECK:
            print("[%s] " % self.gui_get_value(entity), end='')
        elif gui_type == GUIENTITYTYPE.GUI_RADIO:
            print("[%s] " % self.gui_get_value(entity), end='')
        elif gui_type == GUIENTITYTYPE.GUI_SELECT:
            print("[%s] " % self.gui_get_value(entity), end='')
        elif gui_type == GUIENTITYTYPE.GUI_ACTION:
            pass
        else:
            pass
        return 0

        pass

    def gui_cmd_prompt(self, parent):
        buffer = [1024]
        item = 0
        ans = -1
        label = None
        entity = None
        for entity in self.gui_root:
            if entity.parent == parent:
                if self.gui_is_labeling(entity):
                    label = self.gui_get_value(entity)
                else:
                    break
        no_answer = True
        while no_answer:
            print('\n%s> [%s] ' % (label, self.gui_get_value(entity)))
            result = input()
            if result == "":
                return
            result = object_set_value_by_name(entity.obj, entity.propertyname, result)
            if entity.obj and not result:
                print("Invalid input, try again.")
                pass
            result = global_setvar(entity.globalname, result) 
            if entity.var and result == FAILED:
                print("Invalid input, try again.")
                pass
            if entity.env:
                pass

    def gui_cmd_input_count(self, entity):
        count = 0
        item = self.gui_root
        while item is not None:
            if item.parent != entity:
                continue
            if self.gui_is_input(item):
                count += 1
            else:
                count += self.gui_cmd_input_count(item)
            item = item.next
        return count

    def gui_cmd_menu(self, parent):
        buffer = [1024]
        entity = None
        list_ = [100]
        count = None
        while True:
            pass

    def gui_cmd_start(self):
        self.gui_cmd_menu(None)

    def gui_X11_start(self):
        pass

    def gui_html_start(self):
        pass

    def startspan(self):
        if self.table >= 0:
            self.span[self.table] += 1

    def endspan(self):
        if self.table >= 0:
            self.span[self.table] -= 1

    def new_table(self, entity):
        if table < MAX_TABLES:
            table += 1
            row[table] = 0
            col[table] = 0
        else:
            output_error_raw("%s: ERROR: table nesting exceeded limit of %d" % (entity.srcref, MAX_TABLES))

    def newrow(self, entity):
        global table, row, col
        if table < 0:
            self.new_table(entity)
        if row[table] == 0:
            self.gui_html_output(fp,
                            "\t<table" + TABLEOPTIONS + "> <!-- table %d %s -->\n" % (table, self.gui_get_typename(entity)))
        if col[table] > 0:
            self.gui_html_output(fp, "\t</td> <!-- table %d col %d -->\n" % (table, col[table]))
        col[table] = 0
        if row[table] > 0:
            self.gui_html_output(fp, "\t</tr> <!--  table %d row %d -->\n" % (table, row[table]))
        row[table] += 1
        self.gui_html_output(fp, "\t<tr> <!-- row %d -->\n" % row[table])

    def newcol(self, entity):
        if self.span[table] > 0:
            return
        if table < 0 or row[table] == 0:
            self.new_row(entity)
        if col[table] > 0:
            self.gui_html_output(fp, f"\t</td> <!-- table {table} col {col[table]} -->\n")
        col[table] += 1
        if entity.type == GUIENTITYTYPE.GUI_SPAN:
            self.gui_html_output(fp, f"\t<td colspan=\"{entity.size}\"> <!-- table {table} col {col[table]} -->\n")
            if entity.size == 0:
                output_warning(
                    f"{entity.srcref}: not all browsers accept span size 0 (meaning to end), span size may not work as expected")
        else:
            self.gui_html_output(fp, f"\t<td> <!-- table {table} col {col[table]} -->\n")

    def end_table(self, fp, table, col, row):
        if table < 0:
            return
        if col[table] > 0:
            self.gui_html_output(fp, "\t</td> <!-- table %d col %d -->\n" % (table, col[table]))
        if row[table] > 0:
            self.gui_html_output(fp, "\t</tr> <!-- table %d row %d -->\n" % (table, row[table]))
        self.gui_html_output(fp, "\t</table> <!-- table %d -->\n" % (table,))
        table -= 1

    def gui_output_html_textarea(self, entity):
        src = open(entity.source, "r")
        buffer = bytearray(65536)
        len = 0
        rows = ""
        cols = ""
        if entity.height > 0:
            rows = " rows=\"{}\"".format(entity.height)
        if entity.width > 0:
            cols = " cols=\"{}\"".format(entity.width)
        self.gui_html_output(fp, "<textarea class=\"browse\"{}{} >\n".format(rows, cols))
        if src is None:
            self.gui_html_output(fp, "***'{}' is not found: {}***".format(entity.source, strerror(errno)))
            return
        buffer = src.read(65536)
        if len < 0:
            self.gui_html_output(fp, "***'{}' read failed: {}***".format(entity.source, strerror(errno)))
        elif len < 65536:
            buffer[len] = '\0'
            self.gui_html_output(fp, "{}".format(buffer))
        if len >= 65536:
            self.gui_html_output(fp, "\n***file truncated***")
        self.gui_html_output(fp, "</textarea>\n")

    def gui_output_html_table(self, entity):
        src = open(entity.source, "r")
        line = [65536]
        row = 0
        col = 0
        header = [1024]
        self.gui_html_output(fp, "<table class=\"%s\">\n" % entity.options)
        if src == None:
            self.gui_html_output(fp, "***'%s' is not found: %s***", entity.source, strerror(errno))
            self.gui_html_output(fp, "</table>\n")
            return
        while line := src.readline() is not None:
            if eol := line.find('\n'):
                line[eol] = '\0'
            if line[0] == '#':
                pass
            else:
                p = None

                if row == 0:
                    pass
                row += 1
                if entity.height == 0 || row <= entity.height:
                    pass
            if ferror(src):
                self.gui_html_output(fp, "<tr><td>ERROR: %s</td></tr>\n" % strerror(errno))
        self.gui_html_output(fp, "</table>\n")

    def gui_output_html_graph(self, entity):
        script = f"{entity.source}.plt"
        command = f"gnuplot {script}"
        image = f"{entity.source}.png"
        height = ""
        width = ""
        if entity.width > 0:
            width = f" width=\"{entity.width}\""
        if entity.height > 0:
            height = f" height=\"{entity.height}\""
        with open(script, "w") as plot:
            if not plot:
                self.gui_html_output(fp, "<span class=\"error\">Unable to run gnuplot</span>\n")
                return
            if entity.gnuplot == "":
                if entity.width > 0 and entity.height > 0:
                    plot.write(f"set terminal png size {entity.width},{entity.height} {entity.options}\n")
                else:
                    plot.write(f"set terminal png {entity.options}\n")
                plot.write(f"set output '{image}'\n")
                plot.write("set key off\n")
                plot.write("set datafile separator \",\"\n")
                plot.write("set xdata time\n")
                plot.write("set timefmt '%%Y-%%m-%%d %%H:%%M:%%S'\n")
                plot.write("set format x '%%H:%%M'\n")
                plot.write("set xlabel 'Time'\n")
                if entity.unit:
                    plot.write(f"set ylabel '{entity.unit.name}'\n")
                plot.write(f"plot '{entity.source}' using 1:2\n")
            else:
                plot.write(entity.gnuplot)
        if os.system(command) == 0:
            self.gui_html_output(fp, f"<img src=\"/output/{image}\" alt=\"{entity.source}\"{height}{width}/>\n")
        else:
            self.gui_html_output(fp, "<span class=\"error\">Unable to run gnuplot</span>\n")

    def gui_html_source_page(self, source):
        buffer = bytearray(65536)
        src = open(source, 'rt')
        if src is None:
            return 0
        while True:
            data = src.readinto(buffer)
            if data == 0:
                break
            buffer[data] = 0
            self.gui_html_output(fp, "%s", buffer)
        src.close()
        return 1

    def gui_entity_html_content(self, entity):
        ptype = Class.class_get_property_typename(entity.prop.ptype) if entity.prop else ""
        if entity.type == GUIENTITYTYPE.GUI_PAGE:
            if entity.source and not self.gui_html_source_page(entity.source):
                self.gui_html_output(fp, "ERROR: page '%s' not found: %s", entity.source,
                                strerror(errno))
        elif entity.type == GUIENTITYTYPE.GUI_TITLE:
            if entity.parent == None:
                self.gui_html_output(fp, "<title>%s</title>\n" % self.gui_get_value(entity))
            elif entity.parent.type == GUIENTITYTYPE.GUI_GROUP:
                self.gui_html_output(fp, "<legend>%s</legend>\n" % self.gui_get_value(entity))
            else:
                self.gui_html_output(fp, "<h%d>%s</h%d>\n" % (table + 1, self.gui_get_value(entity), table + 1))
        elif entity.type == GUIENTITYTYPE.GUI_STATUS:
            self.gui_html_output(fp, "<script lang=\"jscript\"> window.status=\"%s\";</script>\n" % self.gui_get_value(entity))
        elif entity.type == GUIENTITYTYPE.GUI_TEXT:
            if entity.parent == None or self.gui_get_type(entity.parent) != GUIENTITYTYPE.GUI_SPAN:
                self.newcol(entity)
            self.gui_html_output(fp, "<span class=\"text\">%s</span>\n" % self.gui_get_value(entity))
        elif entity.type == GUIENTITYTYPE.GUI_INPUT:
            if entity.parent == None or self.gui_get_type(entity.parent) != GUIENTITYTYPE.GUI_SPAN:
                self.newcol(entity);
            self.gui_html_output(fp,
                            "<input class=\"%s\" type=\"text\" name=\"%s\" value=\"%s\" onchange=\"update_%s(this)\"/>\n" % (
                            ptype, self.gui_get_name(entity), self.gui_get_value(entity), ptype))
        elif entity.type == GUIENTITYTYPE.GUI_CHECK:
            prop = self.gui_get_property(entity)
            key = None
            if entity.parent == None or self.gui_get_type(entity.parent) != GUIENTITYTYPE.GUI_SPAN:
                self.newcol(entity);
            key = prop.keywords
            if entity.var and global_setvar(entity.globalname, buffer) == FAILED:
                self.gui_html_output(fp, "Invalid input, try again.\n")
                # goto(Retry)
            else:
                entity.env
        else:
            pass

    def gui_entity_html_open(self, entity):
        if entity.type == GUIENTITYTYPE.GUI_TAB:
            pass
        elif entity.type == GUIENTITYTYPE.GUI_GROUP:
            new_col(entity)
            self.gui_html_output(fp, "<fieldset>\n")
            new_table(entity)
        elif entity.type == GUIENTITYTYPE.GUI_SPAN:
            new_col(entity)
            start_span()
        else:
            pass
        self.gui_entity_html_content(entity)

    def gui_entity_html_close(self, entity):
        entity_type = entity.type
        if entity_type == GUIENTITYTYPE.GUI_ROW:
            new_row(entity)
        elif entity_type == GUIENTITYTYPE.GUI_TAB:
            pass
        elif entity_type == GUIENTITYTYPE.GUI_GROUP:
            self.end_table()
            self.gui_html_output(fp, "</fieldset>\n")
        elif entity_type == GUIENTITYTYPE.GUI_SPAN:
            self.end_span()
        else:
            pass

    def gui_html_output_children(self, entity):
        child = self.gui_get_root()
        if entity is not None:
            self.gui_entity_html_open(entity)
        while child is not None:
            if not self.gui_is_header(child) and child.parent == entity:
                self.gui_html_output_children(child)
            child = child.next
        if entity is not None:
            self.gui_entity_html_close(entity)

    def gui_include_element(self, tag, options, file):
        path = [1024]
        if not find_file(file, None, R_OK, path, sizeof(path)):
            output_error("unable to find '%s'", file)
        else:
            fin = open(path, "r")
            if not fin:
                output_error("unable to open '%s'", path[0])
            else:
                buffer = [65536]
                len_ = fin.read(buffer, sizeof(buffer))
                if len_ >= 0:
                    pass
                else:
                    output_error("unable to read '%s'", path[0])

    def gui_html_output_page(self, page):
        entity = None
        len_output = 0
        if page is not None:
            for entity in self.gui_get_root():
                if entity is not None and page == entity.value:
                    return self.gui_html_source_page(entity.source)
        len_output += self.gui_html_output(fp, "<html>\n<head>\n")
        for entity in self.gui_get_root():
            if entity is not None and self.gui_is_header(entity):
                self.gui_entity_html_content(entity)
        len_output += self.gui_html_output(fp, "</head>\n")
        self.gui_include_element("script", "lang=\"jscript\"", "gridlabd.js")
        self.gui_include_element("style", None, "gridlabd.css")
        len_output += self.gui_html_output(fp, "<body>\n")
        self.gui_html_output_children(None)
        self.endtable()
        len_output += self.gui_html_output(fp, "</body>\n</html>\n")
        return len_output

    def gui_html_output_all(self):
        count = 0
        entity = None
        if self.gui_root == None:
            return 0
        self.gui_html_output(fp, "gui {\n")
        for entity in self.gui_get_root():
            if entity.parent == None:
                count += self.gui_glm_write(fp, entity, 1)
        count += self.gui_html_output(fp, "}\n")
        return count

    def gui_startup(self, argc, argv):
        started = 0
        cmd = ""
        if started:
            return "SUCCESS"
        else:
            cmd = "%s http:" % ("start" if sys.platform.system() == "Windows" else "")
            if os.system(cmd) != 0:
                output_error("unable to start interface")
                return "FAILED"
            else:
                output_verbose("starting interface")
                started = 1
                return "SUCCESS"

    def gui_wait(self):
        if server_startup(0, None) == FAILED:
            output_error("gui is unable to start server")
            return 0
        if self.gui_startup(0, None) == FAILED:
            output_error("gui is unable to start client")
            return 0
        if self.gui_root.wait_for == "":
            return 1
        wait_status = GUIACTIONSTATUS.GUIACT_WAITING
        while wait_status == GUIACTIONSTATUS.GUIACT_WAITING:
            exec_sleep(250000)
        if wait_status == GUIACTIONSTATUS.GUIACT_HALT:
            return 0
        wait_status = GUIACTIONSTATUS.GUIACT_NONE
        return 1

    def gui_wait_status(self, status):
        wait_status = status