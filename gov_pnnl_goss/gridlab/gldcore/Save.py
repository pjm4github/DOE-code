import datetime
import math
import os
import sys
import time

from gridlab.gldcore import Gui
from gridlab.gldcore.Class import DynamicClass
from gridlab.gldcore.Exec import Exec, PASSINIT, PASSCMP, PASSINC
from gridlab.gldcore.Globals import global_urlbase, global_version_major, global_version_minor, global_find, \
    global_suppress_deprecated_messages, global_streaming_io_enabled, EINVAL, global_get_next, global_xmlstrict, \
    global_start_time, global_stop_time, global_clock
from gridlab.gldcore.GridLabD import global_getvar
from gridlab.gldcore.Module import Module
from gridlab.gldcore.Object import Object
from gridlab.gldcore.Output import output_error
from gridlab.gldcore.PropertyHeader import PropertyType
from gridlab.gldcore.Schedule import Schedule
from gridlab.gldcore.TimeStamp import local_datetime, TimeStamp
from gridlab.gldcore.Transform import Transform


class SaveAll:
    """
    Class containing methods to save files in different formats.
    """

    @staticmethod
    def default_format():
        return "gld"

    @staticmethod
    def save_glm(filename, fp):
        """
        Save the file in glm format.
        Args:
        - filename: Name of the file
        - fp: File pointer

        Returns:
        - int: Number of characters written to the file
        """
        pass


    def save_all(self, filename):
        fp = None
        ext = filename.rsplit('.', 1)[-1]
        map = [{"glm": self.save_glm()}, {"xml": self.save_xml()}]
        if ext is None:
            pass
        else:
            ext += 1

        if filename[0] == '-':
            fp = sys.stdout
        else:
            fp = open(filename, "wb")
        if not fp:
            output_error("saveall: unable to open stream '%s' for writing", filename)
            return 0

        if global_streaming_io_enabled:
            pass

        for i in range(len(map)):
            if ext == map[i]["format"]:
                return map[i]["save"](filename, fp)

        output_error("saveall: extension '.%s' not a known format", ext)
        errno = EINVAL
        return -1

    @staticmethod
    def save_xml_strict(filename, fp):
        global global_suppress_deprecated_messages
        """
        Save the file in strict xml format.
        Args:
        - filename: Name of the file
        - fp: File pointer

        Returns:
        - int: Number of characters written to the file
        """
        count = 0
        buffer = '\0' * 1024
        global_var = None
        module = None
        stylesheet = global_find("stylesheet")
        old_suppress_deprecated = global_suppress_deprecated_messages
        global_suppress_deprecated_messages = 1
        count += fp.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        if stylesheet is None or stylesheet.prop.global_property_types != PropertyType.PT_char1024:
            count += fp.write("<?xml-stylesheet href=\"%sgridlabd-%d_%d.xsl\" global_property_types=\"text/xsl\" ?>\n"
                              % (global_urlbase, global_version_major, global_version_minor))
        else:
            count += fp.write("<?xml-stylesheet href=\"%s.xsl\" global_property_types=\"text/xsl\" ?>\n".format(stylesheet.prop.addr))
        count += fp.write("<gridlabd>\n")
        global_var = global_get_next(global_var)
        while global_var is not None:
            if (':' in global_var.prop.name):
                continue
            if global_getvar(global_var.prop.name, buffer, len(buffer)):
                count += fp.write("\t<%s>%s</%s>\n" % (global_var.prop.name, buffer, global_var.prop.name))
            global_var = global_get_next(global_var)

        count += fp.write("\t<timezone>%s</timezone>\n" % TimeStamp.timestamp_current_timezone())
        fp.write("\t<sync-order>\n")
        ranks = Exec.getranks()
        for p in range(len(ranks)):
            passname = ["pretopdown", "bottomup", "posttopdown"]
            lastrank = -1;
            fp.write(f"\t\t<pass>\n\t\t\t<name>{passname[p]}</name>\n")
            for i in range(PASSINIT(p), PASSCMP(i, p), PASSINC(p)):
                if ranks[p].ordinal[i] is not None:
                    for item in ranks[p].ordinal[i].first:
                        pass
            if lastrank >= 0:
                fp.write("\t\t</rank>\n")
            fp.write("\t\t</pass>\n")
        fp.write("\t</sync-order>\n")
        for module in Module.module_get_first():
            owner_class = None
            count += fp.write("\t<%s>\n" % module.name)
            count += fp.write("\t\t<version.major>%d</version.major>\n" % module.major)
            count += fp.write("\t\t<version.minor>%d</version.minor>\n" % module.minor)
            global_var = global_get_next(global_var)
            while global_var is not None:
                modname, name = global_var.prop.name.split(':')
                if (len(modname) < 2 or modname != module.name):
                    continue
                count += fp.write("\t\t<%s>%s</%s>\n" % (name, global_getvar(global_var.prop.name, buffer, len(buffer))
                                if global_getvar(global_var.prop.name, buffer, len(buffer)) else "[error]", name))
                global_var = global_get_next(global_var)
            for owner_class in module.owner_class:
                obj = None
                count += fp.write("\t\t<%s_list>\n" % owner_class.name)
                if owner_class.parent:
                    count += fp.write("\t\t\t<inherits_from>%s</inherits_from>\n" % owner_class.parent.name)
                for obj in Object.object_get_first():
                    if obj.owner_class == owner_class:
                        pclass = None
                        count += fp.write("\t\t\t<%s>\n" % owner_class.name)
                        count += fp.write("\t\t\t\t<id>%d</id>\n" % obj.id)
                        count += fp.write("\t\t\t\t<rank>%d</rank>\n" % obj.rank)
                        if math.math.isfinite(obj.latitude) and Object.convert_from_latitude(obj.latitude, buffer, len(buffer)) > 0:
                            count += fp.write("\t\t\t\t<latitude>%s</latitude>\n" % buffer)
                        if math.math.isfinite(obj.longitude) and Object.onvert_from_longitude(obj.longitude, buffer, len(buffer)) > 0:
                            count += fp.write("\t\t\t\t<longitude>%s</longitude>\n" % buffer)
                        buffer = "NEVER"
                        dt = local_datetime(obj.in_svc)
                        if obj.in_svc == TimeStamp.TS_NEVER or (obj.in_svc > 0 and local_datetime(obj.in_svc, dt) and datetime.date(dt, buffer) > 0):
                            count += fp.write("\t\t\t\t<in_svc>%s</in_svc>\n" % buffer)
                        buffer = "NEVER"
                        if obj.out_svc == TimeStamp.TS_NEVER or (obj.out_svc > 0 and local_datetime(obj.out_svc, dt) and datetime.date(dt, buffer) > 0):
                            count += fp.write("\t\t\t\t<out_svc>%s</out_svc>\n" % buffer)
                        if obj.parent:
                            pass
                        buffer = "NEVER"
                        if obj.exec_clock == TimeStamp.TS_NEVER or (obj.exec_clock > 0 and local_datetime(obj.exec_clock, dt) and datetime.date(dt, buffer, len(buffer)) > 0):
                            count += fp.write("\t\t\t\t<clock>%s</clock>\n" % buffer)
                        if obj.name:
                            count += fp.write("\t\t\t\t<name>%s</name>\n" % obj.name)
                        else:
                            count += fp.write("\t\t\t\t<name>%s:%d</name>\n" % (obj.owner_class.name, obj.id))
                        for pclass in reversed(owner_class.getAllParentClasses()):
                            for prop in pclass.pmap:
                                pass
                        count += fp.write("\t\t\t</%s>\n" % owner_class.name)
                    count += fp.write("\t\t</%s_list>\n" % owner_class.name)
                count += fp.write("\t</%s>\n" % module.name)
        count += fp.write("</gridlabd>\n")
        if fp != sys.stdout:
            fp.close()
        global_suppress_deprecated_messages = old_suppress_deprecated
        return count

    @staticmethod
    def save_xml(filename, fp):
        """
        Save the file in xml format.
        Args:
        - filename: Name of the file
        - fp: File pointer

        Returns:
        - int: Number of characters written to the file
        """
        count = 0
        now = time()
        buffer = '\0' * 1024
        gvptr = global_get_next(None)
        if global_xmlstrict:
            return SaveAll.save_xml_strict(filename, fp)
        count += fp.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        count += fp.write("<load>\n")
        count += fp.write("\t<global>\n")
        count += fp.write("\t\t<class_count>%d</class_count>\n" % DynamicClass.class_get_count())
        count += fp.write("\t\t<object_count>%d</object_count>\n" % Object.object_get_count())
        while gvptr is not None:
            testp = gvptr.prop.name.find(':')
            if testp < 0:
                count += fp.write("\t\t<%s>%s</%s>\n" % (gvptr.prop.name, DynamicClass.class_property_to_string(gvptr.prop, gvptr.prop.addr, buffer, 1024) if DynamicClass.class_property_to_string(gvptr.prop, gvptr.prop.addr, buffer, 1024) > 0 else "...", gvptr.prop.name))
            gvptr = global_get_next(gvptr)
        count += fp.write("\t</global>\n")
        count += fp.write("\t<clock>\n")
        count += fp.write("\t\t<tick>1e+%d</tick>\n" % TimeStamp.TS_SCALE)
        count += fp.write("\t\t<timestamp>%s</timestamp>\n" % (TimeStamp.convert_from_timestamp(global_clock, buffer, 1024) if TimeStamp.convert_from_timestamp(global_clock, buffer, 1024) > 0 else "(invalid)"))
        if os.getenv("TZ"):
            count += fp.write("\t\t<timezone>%s</timezone>\n" % os.getenv("TZ"))
        count += fp.write("\t</clock>\n")
        Object.module_saveall_xml(fp)
        count += fp.write("\t</load>\n")
        if fp != sys.stdout:
            fp.close()
        return count



def saveglm(filename, fp):
    count = 0
    now = time.time()
    buffer = " " * 1024

    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write(os.getenv("USERNAME") if os.name == "nt" else os.getenv("USER"))
    count += fp.write("\n")
    count += fp.write(os.getenv("COMPUTERNAME") if os.name == "nt" else os.getenv("HOSTNAME"))
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")

    if Gui.gui_get_root() is not None:
        count += fp.write("\n")
        count += fp.write("\n# GUI\n")
        count += len(Gui.gui_glm_write_all(fp))
        count += fp.write("\n")

    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("clock {\n")
    count += fp.write("\ttimezone {};\n".format(TimeStamp.timestamp_current_timezone()))
    if TimeStamp.convert_from_timestamp(global_start_time,buffer,len(buffer)) > 0:
        count += fp.write("\tstarttime '{}';\n".format(buffer))
    if TimeStamp.convert_from_timestamp(global_stop_time,buffer,len(buffer)) > 0:
        count += fp.write("\tstoptime '{}';\n".format(buffer))

    count += fp.write("}\n")

    count += Object.module_saveall(fp)
    count += DynamicClass.class_saveall(fp)
    count += Schedule.schedule_saveall(fp)
    count += Transform.transform_saveall(fp)
    count += Object.object_saveall(fp)

    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    if fp != sys.stdout:
        fp.close()
    return count
