import math
from enum import Enum

from gridlab.gldcore import Globals, Random
from gridlab.gldcore.Object import Object


class SANITIZEOPTIONS(Enum):
    SO_ERASE = 0x0001,	# option to erase/reset to default instead of obfuscate
    SO_NAMES = 0x0010,	# option to sanitize names
    SO_LATITUDE = 0x0020,	# option to sanitize latitude
    SO_LONGITUDE = 0x0040,	# option to sanitize longitude
    SO_GEOCOORDS = 0x0060,	# option to sanitize	lat/lon
    SO_CITY = 0x0080,	# option to sanitize city
    SO_TIME = 0x0100,	# option to sanitize times (start/stop/in/out)
    SO_DATE = 0x0200,	# option to sanitize date (start/stop/in/out)
    SO_TIMEZONE = 0x0800,	# option to sanitize timezone
    SO_SPATIAL = 0x00f0,	# option to sanitize all spatial info
    SO_TEMPORAL = 0x0f00,	# option to sanitize all temporal info
    SO_ALL = 0x0ff0,	# option to sanitize all info



class SafeName:
    def __init__(self, name, old):
        self.name = name
        self.old = old
        self.next = None

safename_list:[SafeName] = []

class Sanitize:
    """
    Sanitizes a gridlabd model by clearing names and position from object headers
    @returns 0 on success, -2 on error
    """
    safename_list = None
    
    @staticmethod
    def sanitize_name(obj):
        # Code for sanitizing the object names
        safe = SafeName()
        if not safe:
            return None
        safe.old = obj.name
        buffer = f"{Globals.global_sanitizeprefix().get_string()}{id(safe):X}"
        safe.name = Object.object_set_name(obj, buffer)
        safe.next = Object.safename_list
        safename_list = safe
        return safe.name



    @staticmethod
    def sanitize(argc, argv):
        obj = None
        fp = None
        delta_latitude = 0
        delta_longitude = 0
        
        if Globals.global_sanitize_offset == "":
            delta_latitude = Random.uniform(-5,5)
            delta_longitude = Random.uniform(-180,180)
        elif Globals.global_sanitize_offset == "destroy":
            delta_latitude = delta_longitude = float('nan')
        else:
            parts = Globals.global_sanitize_offset.get_string().split('-')
            if len(parts) != 2:
                parts = Globals.global_sanitize_offset.get_string().split(',')
                if len(parts) != 2:
                    parts = Globals.global_sanitize_offset.get_string().split('/')
                    if len(parts) != 2:
                        print("sanitize_offset lat/lon '%s' is not valid", Globals.global_sanitize_offset.get_string())
                        return -2

            delta_latitude = float(parts[0])
            delta_longitude = float(parts[1])

        for obj in Globals.object_get_first():
            if obj.name is not None and (Globals.global_sanitize_options & SANITIZEOPTIONS.SO_NAMES) == SANITIZEOPTIONS.SO_NAMES:
                Sanitize.sanitize_name(obj)
            if math.isfinite(obj.latitude) and (Globals.global_sanitize_options & SANITIZEOPTIONS.SO_GEOCOORDS) == SANITIZEOPTIONS.SO_GEOCOORDS:
                obj.latitude += delta_latitude
                if obj.latitude < -90:
                    obj.latitude = -90
                if obj.latitude > 90:
                    obj.latitude = 90
            if math.isfinite(obj.longitude) and (Globals.global_sanitize_options & SANITIZEOPTIONS.SO_GEOCOORDS) == SANITIZEOPTIONS.SO_GEOCOORDS:
                obj.longitude = (obj.longitude + delta_longitude) % 360
        
        if Globals.global_sanitize_index == ".xml":
            Globals.global_sanitize_index = Globals.global_modelname
            ext = Globals.global_sanitize_index.rfind('.')
            if ext and  Globals.global_sanitize_index[ext:] == ".glm":
                global_sanitize_index = Globals.global_sanitize_inde[:ext] + "-index.xml"
            else:
                Globals.global_sanitize_index += "-index.xml"
        elif Globals.global_sanitize_index == ".txt":
            global_sanitize_index = Globals.global_modelname
            ext = Globals.global_sanitize_index.rfind('.')
            if ext and Globals.global_sanitize_index[ext:] == ".glm":
                Globals.global_sanitize_index = Globals.global_sanitize_index[:ext] + "-index.txt"
            else:
                Globals.global_sanitize_index += "-index.txt"
        elif Globals.global_sanitize_index[0] == ".":
            pass
        
        if Globals.global_sanitize_index != "":
            ext = Globals.global_sanitize_index.rfind('.')
            use_xml = (ext and Globals.global_sanitize_index[ext:] == ".xml")
            fp = open(Globals.global_sanitize_index, 'w')
            if fp:
                pass
        
        return 0



