

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
import os
from time import time
from enum import Enum

from gov_pnnl_goss.gridlab.gldcore.Class import ClassRegistry
from gov_pnnl_goss.gridlab.gldcore.Convert import output_error, convert_from_timestamp, object_find_name
from gov_pnnl_goss.gridlab.gldcore.Globals import FAILED, global_find, SUCCESS
from gov_pnnl_goss.gridlab.gldcore.Output import output_verbose, output_warning, output_error_raw
from gov_pnnl_goss.gridlab.gldcore.GridLabD import global_getvar, global_setvar
from gridlab.gldcore.Find import Find


MAX_TABLES = 16
table=-1
row = ["" * MAX_TABLES]
col= ["" * MAX_TABLES]
span= ["" * MAX_TABLES]
TABLEOPTIONS = " border=0 CELLPADDING=0 CELLSPACING=0"


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

class GuiEntity:
    """
    This class represents a GUI entity and provides methods to manipulate GUI entities and generate HTML output.
    """
    gui_root = None
    gui_last = None
    def __init__(self):
        # Internal variables
        self._fp = None
        self._gui_last = None
        self._gui_root = None
        self._wait_status = "GUIACT_NONE"
        # Public values
        self.action = ""
        self.action_status = GUIACTIONSTATUS.GUIACT_NONE  # Instance of GUIACTIONSTATUS
        self.data = None  # Can be any global_property_types, depending on the usage context
        self.env = ""  # Environmental variables, represented as a string or None
        self.fp = None
        self.globalname = ""
        self.gnuplot = ""
        self.height = 0
        self.hold = 0
        self.next = None  # Could be another instance of GUIENTITY or None
        self.obj = None  # Instance of OBJECT or None
        self.objectname = ""
        self.options = ""
        self.parent = None  # Could be another instance of GUIENTITY or None
        self.prop = None  # Instance of PROPERTY or None
        self.propertyname = ""
        self.size = 0
        self.source = ""
        self.span = 0
        self.srcref = ""
        self.type = GUIENTITYTYPE.GUI_UNKNOWN  # Instance of GUIENTITYTYPE
        self.unit = None  # Instance of UNIT or None
        self.value = ""
        self.var = None  # Instance of GLOBALVAR or None
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
        self.gui_html_output = stream
        self.fp = ref

    def gui_html_output(self, fp, content):
        print(content, file=fp)  # Assuming a simple print to a file or stdout for demonstration

    def gui_get_root(self):
        return self.gui_root

    def gui_get_last(self):
        return self.gui_last

    def gui_create_entity(self):
        entity = self.gui_last
        if entity is None or entity.global_property_types != GUIENTITYTYPE.GUI_UNKNOWN:
            entity = GuiEntity()
        if entity is None:
            return None
        # entity = GUIENTITY()
        if self.gui_root is None:
            self.gui_root = entity
        if self.gui_last is not None:
            self.gui_last.next = entity
        self.gui_last = entity
        return entity

    def gui_get_type(self, entity):
        return self.entity.global_property_types

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
        return type_mapping.get(entity.global_property_types, "<INVALID>")

    def gui_is_header(self, entity):
        return entity.global_property_types in [
            GUIENTITYTYPE.GUI_TITLE,
            GUIENTITYTYPE.GUI_STATUS,
        ]

    def gui_is_grouping(self, entity):
        return entity.global_property_types in [
            GUIENTITYTYPE.GUI_ROW,
            GUIENTITYTYPE.GUI_TAB,
            GUIENTITYTYPE.GUI_PAGE,
            GUIENTITYTYPE.GUI_GROUP,
            GUIENTITYTYPE.GUI_SPAN,
        ]

    def gui_is_labeling(self, entity):
        return entity.global_property_types in [
            GUIENTITYTYPE.GUI_TITLE,
            GUIENTITYTYPE.GUI_STATUS,
            GUIENTITYTYPE.GUI_TEXT,
        ]

    def gui_is_input(self, entity):
        return entity.global_property_types in [
            GUIENTITYTYPE.GUI_INPUT,
            GUIENTITYTYPE.GUI_CHECK,
            GUIENTITYTYPE.GUI_RADIO,
            GUIENTITYTYPE.GUI_SELECT,
        ]

    def gui_is_output(self, entity):
        return entity.global_property_types in [
            GUIENTITYTYPE.GUI_BROWSE,
            GUIENTITYTYPE.GUI_TABLE,
            GUIENTITYTYPE.GUI_GRAPH,
        ]

    def gui_is_action(self, entity):
        return entity.global_property_types in [GUIENTITYTYPE.GUI_ACTION]

    def gui_set_srcref(self, entity, filename, linenum):
        entity.srcref = f"{filename}:{linenum}"

    def gui_set_type(self, entity, type):
        entity.global_property_types = type

    def gui_set_value(self, entity, value):
        entity.value = value[:min(len(value), len(entity.value))]

    def gui_set_variablename(self, entity, global_name):
        entity.global_name = global_name[:len(entity.global_name)] if len(global_name) < len(
            entity.global_name) else global_name

    def gui_set_objectname(self, entity, objectname):
        entity.data = None
        entity.objectname = objectname


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

    def gui_get_dump(self, entity):
        buffer = "{global_property_types=%s,srcref='%s',value='%s',globalname='%s',object='%s',property='%s',action='%s',span=%d}" % (
            self.gui_get_typename(entity), entity.srcref, entity.value, entity.globalname, entity.objectname,
            entity.propertyname, entity.action, entity.span)
        return buffer

    def gui_get_parent(self, entity):
        return entity.parent

    def gui_get_next(self, entity):
        return entity.next

    def gui_get_value(self, entity):
        from gridlab.gldcore.Object import Object
        obj = self.gui_get_object(entity)
        buffer = ""
        if obj:
            if entity.propertyname == "name":

                entity.value = Object.object_name(obj)
            elif entity.propertyname == "class":
                entity.value = obj.owner_class.name
            elif entity.propertyname == "parent":
                entity.value = Object.object_name(obj.parent) if obj.parent else ""
            elif entity.propertyname == "rank":
                entity.value = str(obj.rank)
            elif entity.propertyname == "clock":
                entity.value = convert_from_timestamp(obj.exec_clock)
            elif entity.propertyname == "valid_to":
                entity.value = convert_from_timestamp(obj.valid_to)
            elif entity.propertyname == "in_svc":
                entity.value = convert_from_timestamp(obj.in_svc)
            elif entity.propertyname == "out_svc":
                entity.value = convert_from_timestamp(obj.out_svc)
            elif entity.propertyname == "latitude":
                entity.value = Object.convert_from_latitude(obj.latitude)
            elif entity.propertyname == "longitude":
                entity.value = Object.convert_from_latitude(obj.longitude)
            elif not obj.object_get_value_by_name(entity.propertyname, entity.value):
                output_error_raw("{}: ERROR: {} refers to a non-existent property '{}'".format(entity.srcref, self.gui_get_typename(entity), entity.propertyname))
        elif self.gui_get_variable(entity):
            entity.var = global_find(entity.globalname)
            entity.value = global_getvar(entity.globalname)
        elif self.gui_get_environment(entity):
            entity.value = entity.env
        return entity.value


    def gui_get_object(self, entity):
        if not entity.obj:
            entity.obj = object_find_name(entity.object_name)
        return entity.obj

    def gui_get_property(self, entity):
        if entity.prop == None:
            if self.gui_get_object(entity):
                entity.prop = ClassRegistry.find_property(entity.obj.owner_class, entity.propertyname)
            elif self.gui_get_variable(entity):
                entity.prop = entity.var.prop
        return entity.prop

    def gui_get_name(self, entity):
        if self.gui_get_object(entity):
            buffer = "{}.{}".format(entity.objectname, entity.propertyname)
            return buffer
        elif self.gui_get_variable(entity):
            return entity.var.prop.name
        else:
            return ""

    def gui_get_data(self, entity):
        from gridlab.gldcore.Object import Object
        if entity.data is None:
            if self.gui_get_object(entity):

                entity.data = Object.object_get_addr(entity.obj, entity.propertyname)
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
        self.gui_type = entity.global_property_types
        if self.gui_type == GUIENTITYTYPE.GUI_TITLE:
            print("%s " % self.gui_get_value(entity))
        elif self.gui_type == GUIENTITYTYPE.GUI_STATUS:
            pass
        elif self.gui_type == GUIENTITYTYPE.GUI_ROW:
            if item > 0:
                print("\n%2d. " % item)
            return 1
        elif self.gui_type == GUIENTITYTYPE.GUI_TAB:
            pass
        elif self.gui_type == GUIENTITYTYPE.GUI_PAGE:
            pass
        elif self.gui_type == GUIENTITYTYPE.GUI_GROUP:
            pass
        elif self.gui_type == GUIENTITYTYPE.GUI_SPAN:
            pass
        elif self.gui_type == GUIENTITYTYPE.GUI_TEXT:
            print("%s " % self.gui_get_value(entity))
        elif self.gui_type == GUIENTITYTYPE.GUI_INPUT:
            print("[%s] " % self.gui_get_value(entity))
        elif self.gui_type == GUIENTITYTYPE.GUI_CHECK:
            print("[%s] " % self.gui_get_value(entity))
        elif self.gui_type == GUIENTITYTYPE.GUI_RADIO:
            print("[%s] " % self.gui_get_value(entity))
        elif self.gui_type == GUIENTITYTYPE.GUI_SELECT:
            print("[%s] " % self.gui_get_value(entity))
        elif self.gui_type == GUIENTITYTYPE.GUI_ACTION:
            pass
        else:
            pass
        return 0

    def gui_cmd_prompt(self, parent):
        from gridlab.gldcore.Object import Object
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
            result = Object.object_set_value_by_name(entity.obj, entity.propertyname, result)
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
            self.entity.newtable()
        if row[table] == 0:
            self.gui_html_output(self.fp,
                            "\t<table" + TABLEOPTIONS + "> <!-- table %d %s -->\n" % (table, self.gui_get_typename(entity)))
        if col[table] > 0:
            self.gui_html_output(self.fp, "\t</td> <!-- table %d col %d -->\n" % (table, col[table]))
        col[table] = 0
        if row[table] > 0:
            self.gui_html_output(self.fp, "\t</tr> <!--  table %d row %d -->\n" % (table, row[table]))
        row[table] += 1
        self.gui_html_output(self.fp, "\t<tr> <!-- row %d -->\n" % row[table])

    def newcol(self, entity):
        if self.span[table] > 0:
            return
        if table < 0 or row[table] == 0:
            entity.newrow()
        if col[table] > 0:
            self.gui_html_output(self.fp, f"\t</td> <!-- table {table} col {col[table]} -->\n")
        col[table] += 1
        if entity.global_property_types == GUIENTITYTYPE.GUI_SPAN:
            self.gui_html_output(self.fp, f"\t<td colspan=\"{entity.size}\"> <!-- table {table} col {col[table]} -->\n")
            if entity.size == 0:
                output_warning(
                    f"{entity.srcref}: not all browsers accept span size 0 (meaning to end), span size may not work as expected")
        else:
            self.gui_html_output(self.fp, f"\t<td> <!-- table {table} col {col[table]} -->\n")

    def end_table(self, fp, table, col, row):
        if table < 0:
            return
        if col[table] > 0:
            self.gui_html_output(self.fp, "\t</td> <!-- table %d col %d -->\n" % (table, col[table]))
        if row[table] > 0:
            self.gui_html_output(self.fp, "\t</tr> <!-- table %d row %d -->\n" % (table, row[table]))
        self.gui_html_output(self.fp, "\t</table> <!-- table %d -->\n" % (table,))
        table -= 1


    def gui_output_html_textarea(self, entity):
        src = open(entity.source, "r")

        rows = ""
        cols = ""
        if entity.height > 0:
            rows = " rows=\"{}\"".format(entity.height)
        if entity.width > 0:
            cols = " cols=\"{}\"".format(entity.width)

        self.gui_html_output(self.fp, "<textarea class=\"browse\"%s%s >\n" % (rows, cols))

        if src == None:
            self.gui_html_output(self.fp, "***'%s' is not found: %s***" % (entity.source, "Source Not Found" ))
            return
        buffer = src.read(65536)

        if len(buffer) == 0:
            self.gui_html_output(self.fp, "***'{}' read failed: {}***".format(entity.source, "File Size"))
        elif len(buffer) < 65536:
            self.gui_html_output(self.fp, "{}".format(buffer))
        if len(buffer) >= 65536:
            self.gui_html_output(self.fp, "{}\n***file truncated***".format(buffer[0:65536]))
        self.gui_html_output(self.fp, "</textarea>\n")

    def gui_output_html_table(self, entity):
        src = open(entity.source, "r")
        line = ' ' * 65536
        row = 0
        col = 0
        header = ' ' * 1024
        self.gui_html_output(self.fp, "<table class=\"%s\">\n" % entity.options)
        if src == None:
            self.gui_html_output(self.fp, "***'%s' is not found: %s***", entity.source, "File Not Opened")
            self.gui_html_output(self.fp, "</table>\n")
            return
        while line := src.readline() is not None:
            try:
                if eol := line.find('\n'):
                    line[eol] = '\0'
                if line[0] == '#':
                    pass
                else:
                    p = None

                    if row == 0:
                        pass
                    row += 1
                    if entity.height == 0 or row <= entity.height:
                        pass
            except ValueError as e:
                self.gui_html_output(self.fp, "<tr><td>ERROR: %s</td></tr>\n" % e)
        self.gui_html_output(self.fp, "</table>\n")

    def gui_output_html_graph(self, entity):
        script = f"{entity.source}.plt"
        command = f"gnuplot {script}"
        image = f"{entity.source}.png"
        height = f" height=\"{entity.height}\"" if entity.height > 0 else ""
        width = f" width=\"{entity.width}\"" if entity.width > 0 else ""
        if entity.width > 0:
            width = f" width=\"{entity.width}\""
        if entity.height > 0:
            height = f" height=\"{entity.height}\""
        with open(script, "w") as plot:
            if not plot:
                self.gui_html_output(self.fp, "<span class=\"error\">Unable to run gnuplot</span>\n")
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
                plot.write("set timefmt \"%%Y-%%m-%%d %%H:%%M:%%S\"\n")
                plot.write("set format x \"%%H:%%M\"\n")
                plot.write("set xlabel \"Time\"\n")
                if entity.unit:
                    plot.write(f"set ylabel '{entity.unit.name}'\n")
                plot.write(f"plot '{entity.source}' using 1:2\n")
            else:
                plot.write(entity.gnuplot)

        if os.system(command) == 0:
            self.gui_html_output(self.fp, f"<img src=\"/output/{image}\" alt=\"{entity.source}\"{height}{width}/>\n")
        else:
            self.gui_html_output(self.fp, "<span class=\"error\">Unable to run gnuplot</span>\n")


    def gui_html_source_page(self, source):
        buffer = ""
        src = open(source, 'rt')
        if src is None:
            return 0
        while True:
            data = src.readinto(buffer)
            if data == 0:
                break
            buffer = ""
            self.gui_html_output(self.fp, "%s", buffer)
        src.close()
        return 1

    def gui_entity_html_content(self, entity):
        ptype = self.gui_get_property(entity).class_get_property_typename() if self.gui_get_property(entity) else ""

        if entity.global_property_types ==  GUIENTITYTYPE.GUI_PAGE:
            if entity.source and not self.gui_html_source_page(entity.source):
                self.gui_html_output(self.fp, f"ERROR: page '{entity.source}' not found")

        elif entity.global_property_types == GUIENTITYTYPE.GUI_TITLE:
            if entity.parent is None:
                self.gui_html_output(self.fp, f"<title>{entity.value}</title>\n")
            elif entity.parent.global_property_types == GUIENTITYTYPE.GUI_GROUP:
                self.gui_html_output(self.fp, f"<legend>{entity.value}</legend>\n")
            else:
                # Assuming 'table' is defined elsewhere, and handling it accordingly
                self.gui_html_output(self.fp, f"<h{table + 1}>{entity.value}</h{table + 1}>\n")

        elif entity.global_property_types == GUIENTITYTYPE.GUI_STATUS:
            self.gui_html_output(self.fp, f'<script lang="jscript"> window.status="{entity.value}";</script>\n')

        elif entity.global_property_types == GUIENTITYTYPE.GUI_TEXT:
            if not entity.parent or self.gui_get_type(entity.parent) != "GUI_SPAN":
                entity.newcol()
            self.gui_html_output(self.fp, f'<span class="text">{entity.value}</span>\n')

        elif entity.global_property_types == GUIENTITYTYPE.GUI_INPUT:
            if not entity.parent or self.gui_get_type(entity.parent) != "GUI_SPAN":
                entity.newcol()
            self.gui_html_output(self.fp,
                            f'<input class="{ptype}" global_property_types="text" name="{self.gui_get_name(entity)}" value="{self.gui_get_value(entity)}" onchange="update_{ptype}(this)" />\n')

        elif entity.global_property_types == GUIENTITYTYPE.GUI_CHECK:
            prop = self.gui_get_property(entity)
            if not entity.parent or self.gui_get_type(entity.parent) != "GUI_SPAN":
                entity.newcol()
            for key in prop.keywords:
                value = self.gui_get_data(entity)
                checked = "checked" if value == key.value else ""
                label = key.name.replace('_', ' ').capitalize()
                self.gui_html_output(self.fp,
                                f'<nobr><input class="{ptype}" global_property_types="checkbox" name="{self.gui_get_name(entity)}" value="{key.value}" {checked} onchange="update_{ptype}(this)" />{label}</nobr>\n')

        elif entity.global_property_types == GUIENTITYTYPE.GUI_RADIO:
            prop = self.gui_get_property(entity)
            if not entity.parent or self.gui_get_type(entity.parent) != "GUI_SPAN":
                entity.newcol()
            for key in prop.keywords:
                value = self.gui_get_data(entity)
                checked = "checked" if value == key.value else ""
                label = key.name.replace('_', ' ').capitalize()
                self.gui_html_output(self.fp,
                                f'<nobr><input class="{ptype}" global_property_types="radio" name="{self.gui_get_name(entity)}" value="{key.value}" {checked} onchange="update_{ptype}(this)" />{label}</nobr>\n')

        elif entity.global_property_types == GUIENTITYTYPE.GUI_SELECT:
            prop = self.gui_get_property(entity)
            multiple = "multiple" if prop.global_property_types == "PT_set" else ""
            size = f'size="{entity.size}"' if entity.size > 0 else ""
            if not entity.parent or self.gui_get_type(entity.parent) != "GUI_SPAN":
                entity.newcol()
            self.gui_html_output(self.fp,
                            f'<select class="{ptype}" name="{self.gui_get_name(entity)}" {multiple} {size} onchange="update_{ptype}(this)">\n')
            for key in prop.keywords:
                value = self.gui_get_data(entity)
                selected = "selected" if value == key.value else ""
                label = key.name.replace('_', ' ').capitalize()
                self.gui_html_output(self.fp, f'<option value="{key.value}" {selected}>{label}</option>\n')
            self.gui_html_output(self.fp, '</select>\n')

        elif entity.global_property_types == GUIENTITYTYPE.GUI_BROWSE:
            if not entity.parent or self.gui_get_type(entity.parent) != "GUI_SPAN":
                entity.newcol()
            self.gui_output_html_textarea(entity)

        elif entity.global_property_types == GUIENTITYTYPE.GUI_TABLE:
            if not entity.parent or self.gui_get_type(entity.parent) != "GUI_SPAN":
                entity.newcol()
            self.gui_output_html_table(entity)

        elif entity.global_property_types == GUIENTITYTYPE.GUI_GRAPH:
            if not entity.parent or self.gui_get_type(entity.parent) != "GUI_SPAN":
                entity.newcol()
            self.gui_output_html_graph(entity)

        elif entity.global_property_types == GUIENTITYTYPE.GUI_ACTION:
            if not entity.parent or self.gui_get_type(entity.parent) != "GUI_SPAN":
                entity.newcol()
            self.gui_html_output(self.fp,
                            f'<input class="action" global_property_types="submit" name="action" value="{entity.action}" onclick="click(this)" />\n')

    def gui_entity_html_open(self, entity):
        if entity.global_property_types == GUIENTITYTYPE.GUI_TAB:
            pass
        elif entity.global_property_types == GUIENTITYTYPE.GUI_GROUP:
            entity.newcol()
            self.gui_html_output(self.fp, "<fieldset>\n")
            entity.newtable()
        elif entity.global_property_types == GUIENTITYTYPE.GUI_SPAN:
            entity.newcol()
            entity.start_span()
        else:
            pass
        self.gui_entity_html_content(entity)

    def gui_entity_html_close(self, entity):
        entity_type = entity.global_property_types
        if entity_type == GUIENTITYTYPE.GUI_ROW:
            entity.newrow()
        elif entity_type == GUIENTITYTYPE.GUI_TAB:
            pass
        elif entity_type == GUIENTITYTYPE.GUI_GROUP:
            self.end_table()
            self.gui_html_output(self.fp, "</fieldset>\n")
        elif entity_type == GUIENTITYTYPE.GUI_SPAN:
            entity.end_span()
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


    def gui_include_element(self, file):
        path = ""
        if not Find.find_file(file, None, path):
            output_error("unable to find '%s'", file)
        else:
            fin = open(path, "r")
            if not fin:
                output_error("unable to open '%s'", path[0])
            else:
                buffer = fin.read(65536)
                len_= len(buffer)
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
        len_output += self.gui_html_output(self.fp, "<html>\n<head>\n")
        for entity in self.gui_get_root():
            if entity is not None and self.gui_is_header(entity):
                self.gui_entity_html_content(entity)
        len_output += self.gui_html_output(self.fp, "</head>\n")
        self.gui_include_element("script", "lang=\"jscript\"", "gridlabd.js")
        self.gui_include_element("style", None, "gridlabd.css")
        len_output += self.gui_html_output(self.fp, "<body>\n")
        self.gui_html_output_children(None)
        self.endtable()
        len_output += self.gui_html_output(self.fp, "</body>\n</html>\n")
        return len_output

    def gui_html_output_all(self):
        entity = self.gui_get_root()

        self.gui_html_output(self.fp,"<html>\n<head>\n")
        while entity is not None:
            if self.gui_is_header(entity):
                self.gui_entity_html_content(entity)
            entity = entity.next

        self.gui_html_output(self.fp,"</head>\n")

        self.gui_include_element("script","lang=\"jscript\"","gridlabd.js")
        self.gui_include_element("style",None,"gridlabd.css")

        self.gui_html_output(self.fp,"<body>\n")
        self.gui_html_output_children(None)
        self.endtable()
        self.gui_html_output(self.fp,"</body>\n</html>\n")
        return SUCCESS


    # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
    def gui_glm_typename(type):
        type_name = [
            None, "row", "tab", "page", "group", "span", None,
            "title", "status", "text", None,
            "input", "check", "radio", "select", "action", None,
            "browse", "table", "graph", None,
            None,
        ]
        if type >= 0 or type < len(type_name):
            return type_name[type]
        else:
            return None


    # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
    import os

    started = 0

    def gui_startup(self):
        global started
        if started:
            return "SUCCESS"

        if os.name == "nt":
            cmd = f"start {os.environ['BROWSER']} http://"
        else:
            cmd = f"{os.environ['BROWSER']} http:"

        if os.system(cmd) != 0:
            output_error("unable to start interface")
            return "FAILED"
        else:
            output_verbose("starting interface")
            started = 1
            return "SUCCESS"

    def gui_wait(self):
        if self.server_startup(0, None) == FAILED:
            output_error("gui is unable to start server")
            return 0
        if self.gui_startup(0, None) == FAILED:
            output_error("gui is unable to start client")
            return 0
        if self.gui_root.wait_for == "":
            return 1
        wait_status = GUIACTIONSTATUS.GUIACT_WAITING
        while wait_status == GUIACTIONSTATUS.GUIACT_WAITING:
            time.sleep(250000)
        if wait_status == GUIACTIONSTATUS.GUIACT_HALT:
            return 0
        wait_status = GUIACTIONSTATUS.GUIACT_NONE
        return 1

    def gui_wait_status(self, status):
        wait_status = status

class GUIEntity(QWidget):
    def __init__(self, parent=None):
        super(GUIEntity, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Initialize all the properties
        self.sourceRef = ""
        self.entityType = None
        self.value = None
        self.variableName = None
        self.propertyName = None
        self.span = 1  # Default span value
        self.unit = None
        self.nextEntity = None
        self.parentEntity = parent  # Use the provided parent as the parent entity
        self.source = None
        self.options = None
        self.wait_for = None

    def add_label(self, text):
        label = QLabel(text)
        self.layout.addWidget(label)


    # Other previously defined methods remain the same

    def set_propertyname(self, propertyName):
        self.propertyName = propertyName
        # Handle the property name as needed for your application

    def set_span(self, span):
        self.span = span
        # Adjust GUI layout or widget size based on span, if applicable

    def set_unit(self, unit):
        self.unit = unit
        # Use the unit for formatting or displaying values

    def set_next(self, nextEntity):
        self.nextEntity = nextEntity
        # You might use this to manage a sequence or chain of GUI entities

    def set_parent(self, parentEntity):
        self.parentEntity = parentEntity
        # This can be used to establish a hierarchical relationship between entities

    def set_source(self, source):
        self.source = source
        # Use source information as needed, perhaps for loading external data

    def set_options(self, options):
        self.options = options
        # Options could be used to configure the appearance or behavior of the entity

    def set_wait(self, wait):
        self.wait_for = wait
        # Implement logic to handle waiting conditions as required by your application


    def add_action(self, action_name, callback):
        button = QPushButton(action_name)
        button.clicked.connect(callback)
        self.layout.addWidget(button)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('GridLAB-D GUI')
        self.central_widget = GUIEntity(self)
        self.setCentralWidget(self.central_widget)
        self.setup_gui()

    def setup_gui(self):
        # Example adding GUI entities
        self.central_widget.add_label('Welcome to GridLAB-D GUI')
        self.central_widget.add_action('Action 1', self.action1_callback)
        self.central_widget.add_action('Quit', self.quit_application)

    def action1_callback(self):
        print("Action 1 triggered")

    def quit_application(self):
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()