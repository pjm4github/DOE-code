class GldLineConfig:
    def __init__(self, name):
        self.name = name
        self.spacing = ""
        self.conductor_A = ""
        self.conductor_B = ""
        self.conductor_C = ""
        self.conductor_N = ""

    @staticmethod
    def get_match_wire(w_class, name, buried):
        if w_class == "OverheadWireInfo":
            if buried:
                return "ugwire_" + name
            else:
                return "wire_" + name
        elif w_class == "ConcentricNeutralCableInfo":
            return "cncab_" + name
        elif w_class == "TapeShieldCableInfo":
            return "tscab_" + name
        return "unknown_" + name

    def get_glm(self):
        buf = []
        buf.append("object line_configuration {")
        buf.append(f'  name "{self.name}";')
        buf.append(f'  spacing "{self.spacing}";')
        if self.conductor_A:
            buf.append(f'  conductor_A "{self.conductor_A}";')
        if self.conductor_B:
            buf.append(f'  conductor_B "{self.conductor_B}";')
        if self.conductor_C:
            buf.append(f'  conductor_C "{self.conductor_C}";')
        if self.conductor_N:
            buf.append(f'  conductor_N "{self.conductor_N}";')
        buf.append("}")
        return "\n".join(buf)
