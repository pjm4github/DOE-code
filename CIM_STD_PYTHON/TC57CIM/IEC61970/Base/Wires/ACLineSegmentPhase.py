class ACLineSegmentPhase:
    def __init__(self):
        self.phase = None  # The phase connection of the wire at both ends
        self.sequence_number = None  # Number designation for this line segment phase
        self.ac_line_segment = None  # The line segment to which the phase belongs

    def get_ac_line_segment(self):
        return self.ac_line_segment

    def get_phase(self):
        return self.phase

    def get_sequence_number(self):
        return self.sequence_number

    def set_ac_line_segment(self, new_val):
        self.ac_line_segment = new_val

    def set_phase(self, new_val):
        self.phase = new_val

    def set_sequence_number(self, new_val):
        self.sequence_number = new_val
