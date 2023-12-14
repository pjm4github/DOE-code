
def default_format():
    return "gld"

def save_glm(filename, fp):
    pass

def save_xml(filename, fp):
    pass

def save_xml_strict(filename, fp):
    count = 0
    buffer = [1024]
    globalvar = None
    globalvar = global_find("stylesheet")
    old_suppress_deprecated = global_suppress_deprecated_messages
    global_suppress_deprecated_messages = 1
    count += fp.write(f"<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
    count += fp.write(f"<gridlabd>\n")

def save_all(filename):
    fp = None
    ext = filename.rsplit('.', 1)[-1]
    map = [{"glm": save_glm}, {"xml": save_xml}]
    if ext is None:
        pass
    else:
        ext += 1

    if filename[0] == '-':
        fp = stdout
    elif (fp = fopen(filename, "wb")) == None:
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

import os
import time

def save_glm(filename, fp):
    count = 0
    now = time.time()
    buffer = bytearray(1024)

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
    count += fp.write("\ttimezone %s;\n" % timestamp_current_timezone())
    if convert_from_timestamp(global_starttime, buffer, len(buffer)) > 0:
        count += fp.write("\tstarttime '%s';\n" % buffer.decode())
    if convert_from_timestamp(global_stoptime, buffer, len(buffer)) > 0:
        count += fp.write("\tstoptime '%s';\n" % buffer.decode())
    count += fp.write("}\n")
  
    count += module_save_all(fp)
    count += class_save_all(fp)
    count += schedule_save_all(fp)
    count += transform_save_all(fp)
    count += object_save_all(fp)
    
    count += fp.write("\n")
    count += fp.write("\n")
    count += fp.write("\n")
    if fp != sys.stdout:
        fp.close()
    return count
