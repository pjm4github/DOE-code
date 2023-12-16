
class ACLineSegment(Conductor):
    def __init__(self):
        super().__init__()
        self.b0ch = None  # Zero sequence shunt susceptance
        self.bch = None   # Positive sequence shunt susceptance
        self.g0ch = None  # Zero sequence shunt conductance
        self.gch = None   # Positive sequence shunt conductance
        self.r = None     # Positive sequence series resistance
        self.r0 = None    # Zero sequence series resistance
        self.short_circuit_end_temperature = None  # Maximum permitted temperature
        self.x = None     # Positive sequence series reactance
        self.x0 = None    # Zero sequence series reactance
        self.clamp = None  # Clamps connected to the line segment

    def get_b0ch(self):
        return self.b0ch

    def get_bch(self):
        return self.bch

    def get_clamp(self):
        return self.clamp

    def get_g0ch(self):
        return self.g0ch

    def get_gch(self):
        return self.gch

    def get_r(self):
        return self.r

    def get_r0(self):
        return self.r0

    def get_short_circuit_end_temperature(self):
        return self.short_circuit_end_temperature

    def get_x(self):
        return self.x

    def get_x0(self):
        return self.x0

    def set_b0ch(self, new_val):
        self.b0ch = new_val

    def set_bch(self, new_val):
        self.bch = new_val

    def set_clamp(self, new_val):
        self.clamp = new_val

    def set_g0ch(self, new_val):
        self.g0ch = new_val

    def set_gch(self, new_val):
        self.gch = new_val

    def set_r(self, new_val):
        self.r = new_val

    def set_r0(self, new_val):
        self.r0 = new_val

    def set_short_circuit_end_temperature(self, new_val):
        self.short_circuit_end_temperature = new_val

    def set_x(self, new_val):
        self.x = new_val

    def set_x0(self, new_val):
        self.x0 = new_val
