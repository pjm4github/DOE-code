class DistBaseVoltage:
    sz_cim_class = "BaseVoltage"

    def __init__(self, results):
        if results.has_next():
            soln = results.next()
            self.name = soln.get("?vnom").to_string()
            self.vnom = float(soln.get("?vnom").to_string())

    def get_json_entry(self):
        return f'{{"name":"{self.name}"}}'

    def display_string(self):
        return f'vnom={self.vnom:.4f}'

    def get_key(self):
        return self.name

    def get_dss(self):
        return f'{0.001 * self.vnom:.3f} '
