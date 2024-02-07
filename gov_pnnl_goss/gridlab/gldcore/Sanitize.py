

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
        buffer = f"{global_sanitizeprefix.get_string()}{id(safe):X}"
        safe.name = object_set_name(obj, buffer)
        safe.next = safename_list
        safename_list = safe
        return safe.name



    @staticmethod
    def sanitize(argc, argv):
        obj = None
        fp = None
        delta_latitude = 0
        delta_longitude = 0
        
        if global_sanitizeoffset == "":
            delta_latitude = random.uniform(-5,5)
            delta_longitude = random.uniform(-180,180)
        elif global_sanitizeoffset == "destroy":
            delta_latitude = delta_longitude = float('nan')
        else:
            parts = global_sanitizeoffset.get_string().split('-')
            if len(parts) != 2:
                parts = global_sanitizeoffset.get_string().split(',')
                if len(parts) != 2:
                    parts = global_sanitizeoffset.get_string().split('/')
                    if len(parts) != 2:
                        output_error("sanitize_offset lat/lon '%s' is not valid", global_sanitizeoffset.get_string())
                        return -2

            delta_latitude = float(parts[0])
            delta_longitude = float(parts[1])

        for obj in object_get_first():
            if obj.name is not None and (global_sanitizeoptions & SO_NAMES) == SO_NAMES:
                Sanitize.sanitize_name(obj)
            if math.isfinite(obj.latitude) and (global_sanitizeoptions & SO_GEOCOORDS) == SO_GEOCOORDS:
                obj.latitude += delta_latitude
                if obj.latitude < -90:
                    obj.latitude = -90
                if obj.latitude > 90:
                    obj.latitude = 90
            if math.isfinite(obj.longitude) and (global_sanitizeoptions & SO_GEOCOORDS) == SO_GEOCOORDS:
                obj.longitude = (obj.longitude + delta_longitude) % 360
        
        if global_sanitizeindex == ".xml":
            global_sanitizeindex = global_modelname
            ext = global_sanitizeindex.rfind('.')
            if ext and global_sanitizeindex[ext:] == ".glm":
                global_sanitizeindex = global_sanitizeindex[:ext] + "-index.xml"
            else:
                global_sanitizeindex += "-index.xml"
        elif global_sanitizeindex == ".txt":
            global_sanitizeindex = global_modelname
            ext = global_sanitizeindex.rfind('.')
            if ext and global_sanitizeindex[ext:] == ".glm":
                global_sanitizeindex = global_sanitizeindex[:ext] + "-index.txt"
            else:
                global_sanitizeindex += "-index.txt"
        elif global_sanitizeindex[0] == ".":
            pass
        
        if global_sanitizeindex != "":
            ext = global_sanitizeindex.rfind('.')
            use_xml = (ext and global_sanitizeindex[ext:] == ".xml")
            fp = open(global_sanitizeindex, 'w')
            if fp:
                pass
        
        return 0



