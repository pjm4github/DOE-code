
import os
import sys
import time

from gridlab.gldcore.Exec import object_get_first
from gridlab.gldcore.Globals import global_find, global_getnext, global_getvar, global_xmlstrict
from gridlab.gldcore.Object import object_get_count
from gridlab.gldcore.Output import output_error
from gridlab.gldcore.Timestamp import local_datetime


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
        if stylesheet is None or stylesheet.prop.ptype != PT_char1024:
            count += fp.write("<?xml-stylesheet href=\"%sgridlabd-%d_%d.xsl\" type=\"text/xsl\" ?>\n"
                              % (global_urlbase, global_version_major, global_version_minor))
        else:
            count += fp.write("<?xml-stylesheet href=\"%s.xsl\" type=\"text/xsl\" ?>\n" % static_cast(str, stylesheet.prop.addr))
        count += fp.write("<gridlabd>\n")
        global_var = global_getnext(global_var)
        while global_var is not None:
            if (':' in global_var.prop.name):
                continue
            if global_getvar(global_var.prop.name, buffer, len(buffer)):
                count += fp.write("\t<%s>%s</%s>\n" % (global_var.prop.name, buffer, global_var.prop.name))
            global_var = global_getnext(global_var)

        count += fp.write("\t<timezone>%s</timezone>\n" % timestamp_current_timezone())
        fp.write("\t<sync-order>\n")
        ranks = exec_getranks()
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
        for module in module_get_first():
            oclass = None
            count += fp.write("\t<%s>\n" % module.name)
            count += fp.write("\t\t<version.major>%d</version.major>\n" % module.major)
            count += fp.write("\t\t<version.minor>%d</version.minor>\n" % module.minor)
            global_var = global_getnext(global_var)
            while global_var is not None:
                modname, name = global_var.prop.name.split(':')
                if (len(modname) < 2 or modname != module.name):
                    continue
                count += fp.write("\t\t<%s>%s</%s>\n" % (name, global_getvar(global_var.prop.name, buffer, len(buffer))
                                if global_getvar(global_var.prop.name, buffer, len(buffer)) else "[error]", name))
                global_var = global_getnext(global_var)
            for oclass in module.oclass:
                obj = None
                count += fp.write("\t\t<%s_list>\n" % oclass.name)
                if oclass.parent:
                    count += fp.write("\t\t\t<inherits_from>%s</inherits_from>\n" % oclass.parent.name)
                for obj in object_get_first():
                    if obj.oclass == oclass:
                        pclass = None
                        count += fp.write("\t\t\t<%s>\n" % oclass.name)
                        count += fp.write("\t\t\t\t<id>%d</id>\n" % obj.id)
                        count += fp.write("\t\t\t\t<rank>%d</rank>\n" % obj.rank)
                        if isfinite(obj.latitude) and convert_from_latitude(obj.latitude, buffer, len(buffer)) > 0:
                            count += fp.write("\t\t\t\t<latitude>%s</latitude>\n" % buffer)
                        if isfinite(obj.longitude) and convert_from_longitude(obj.longitude, buffer, len(buffer)) > 0:
                            count += fp.write("\t\t\t\t<longitude>%s</longitude>\n" % buffer)
                        buffer = "NEVER"
                        if obj.in_svc == TS_NEVER or (obj.in_svc > 0 and local_datetime(obj.in_svc, dt) and strdatetime(dt, buffer, len(buffer)) > 0):
                            count += fp.write("\t\t\t\t<in_svc>%s</in_svc>\n" % buffer)
                        buffer = "NEVER"
                        if obj.out_svc == TS_NEVER or (obj.out_svc > 0 and local_datetime(obj.out_svc, dt) and strdatetime(dt, buffer, len(buffer)) > 0):
                            count += fp.write("\t\t\t\t<out_svc>%s</out_svc>\n" % buffer)
                        if obj.parent:
                            pass
                        buffer = "NEVER"
                        if obj.clock == TS_NEVER or (obj.clock > 0 and local_datetime(obj.clock, dt) and strdatetime(dt, buffer, len(buffer)) > 0):
                            count += fp.write("\t\t\t\t<clock>%s</clock>\n" % buffer)
                        if obj.name:
                            count += fp.write("\t\t\t\t<name>%s</name>\n" % obj.name)
                        else:
                            count += fp.write("\t\t\t\t<name>%s:%d</name>\n" % (obj.oclass.name, obj.id))
                        for pclass in reversed(oclass.getAllParentClasses()):
                            for prop in pclass.pmap:
                                pass
                        count += fp.write("\t\t\t</%s>\n" % oclass.name)
                    count += fp.write("\t\t</%s_list>\n" % oclass.name)
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
        gvptr = global_getnext(None)
        if global_xmlstrict:
            return SaveAll.save_xml_strict(filename, fp)
        count += fp.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        count += fp.write("<load>\n")
        count += fp.write("\t<global>\n")
        count += fp.write("\t\t<class_count>%d</class_count>\n" % class_get_count())
        count += fp.write("\t\t<object_count>%d</object_count>\n" % object_get_count())
        while gvptr is not None:
            testp = gvptr.prop.name.find(':')
            if testp < 0:
                count += fp.write("\t\t<%s>%s</%s>\n" % (gvptr.prop.name, class_property_to_string(gvptr.prop, gvptr.prop.addr, buffer, 1024) if class_property_to_string(gvptr.prop, gvptr.prop.addr, buffer, 1024) > 0 else "...", gvptr.prop.name))
            gvptr = global_getnext(gvptr)
        count += fp.write("\t</global>\n")
        count += fp.write("\t<clock>\n")
        count += fp.write("\t\t<tick>1e+%d</tick>\n" % TS_SCALE)
        count += fp.write("\t\t<timestamp>%s</timestamp>\n" % (convert_from_timestamp(global_clock, buffer, 1024) if convert_from_timestamp(global_clock, buffer, 1024) > 0 else "(invalid)"))
        if getenv("TZ"):
            count += fp.write("\t\t<timezone>%s</timezone>\n" % os.getenv("TZ"))
        count += fp.write("\t</clock>\n")
        module_saveall_xml(fp)
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

    if gui_get_root() is not None:
        count += fp.write("\n")
        count += fp.write("\n# GUI\n")
        count += len(gui_glm_write_all(fp))
        count += fp.write("\n")

    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("clock {\n")
    count += fp.write("\ttimezone {};\n".format(timestamp_current_timezone()))
    if convert_from_timestamp(global_starttime,buffer,len(buffer)) > 0:
        count += fp.write("\tstarttime '{}';\n".format(buffer))
    if convert_from_timestamp(global_stoptime,buffer,len(buffer)) > 0:
        count += fp.write("\tstoptime '{}';\n".format(buffer))

    count += fp.write("}\n")

    count += module_saveall(fp)
    count += class_saveall(fp)
    count += schedule_saveall(fp)
    count += transform_saveall(fp)
    count += object_saveall(fp)

    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    if fp != stdout:
        fp.close()
    return count
