from typing import Dict

from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistSwitch(DistComponent):
    sz_cim_class = 'Switch'
    sz_csv_header = 'Name,Bus1,Phases,Bus2,Phases,Type,Status'

    def __init__(self, results):
        super().__init__()
        self.id = ''
        self.name = ''
        self.bus1 = ''
        self.bus2 = ''
        self.phases = ''
        self.open = ''
        self.basev = ''
        self.rated = 0.0
        self.breaking = 0.0
        self.normal_current_limit = 0.0
        self.emergency_current_limit = 0.0
        self.glm_phases = ''

    def cim_class(self):
        return ''

    def get_json_entry(self):
        buf = []
        buf.append('{"name":"' + self.name + '"')
        buf.append(',"mRID":"' + self.id + '"')
        buf.append(',"CN1":"' + self.bus1 + '"')
        buf.append(',"CN2":"' + self.bus2 + '"')
        buf.append(',"phases":"' + self.phases.replace('\n', '') + '"')
        buf.append(',"ratedCurrent":' + f'{self.rated: .1f}')
        buf.append(',"breakingCapacity":' + f'{self.breaking: .1f}')
        if self.open:
            buf.append(',"normalOpen":true')
        else:
            buf.append(',"normalOpen":false')
        buf.append('}')
        return '\n'.join(buf)

    def initialize_from_results(self, soln):
        self.name = self.safe_name(soln.get('?name').toPython())
        self.id = soln.get('?voltage_id').toPython()
        self.basev = float(soln.get('?basev').toPython())
        self.rated = self.optional_double(soln, '?rated', 0.0)
        self.breaking = self.optional_double(soln, '?breaking', 0.0)
        self.bus1 = self.safe_name(soln.get('?bus1').toPython())
        self.bus2 = self.safe_name(soln.get('?bus2').toPython())
        self.phases = self.optional_string(soln, '?phases', 'ABC')
        self.open = bool(soln.get('?is_open').toPython())
        glm_phs = []
        if 'A' in self.phases:
            glm_phs.append('A')
        if 'B' in self.phases:
            glm_phs.append('B')
        if 'C' in self.phases:
            glm_phs.append('C')
        if 'status' in self.phases:
            glm_phs.append('S')
        if len(glm_phs) < 1:
            glm_phs.append('ABC')
        if ''.join(glm_phs) == 'AB' and self.basev <= 208.1:
            self.glm_phases = 'S'
        else:
            self.glm_phases = ''.join(glm_phs)

    def display_string(self):
        buf = []
        buf.append(self.name + ' from ' + self.bus1 + ' to ' + self.bus2 + ' basev=' +
                   f'{self.basev: .2f}' + ' rated=' + f'{self.rated: .1f}' +
                   ' breaking=' + f'{self.breaking: .1f}' + ' phases=' +
                   self.glm_phases + ' is_open=' + str(self.open))
        return '\n'.join(buf)

    def get_glm(self):
        buf = []
        buf.append('object switch { // CIM ' + self.cim_class())
        buf.append('  name "swt_' + self.name + '";')
        buf.append('  from "' + self.bus1 + '";')
        buf.append('  to "' + self.bus2 + '";')
        buf.append('  phases ' + self.glm_phases + ';')
        if self.open:
            buf.append('  status OPEN;')
        else:
            buf.append('  status CLOSED;')
        self.append_glm_ratings(buf, self.glm_phases, self.normal_current_limit, self.emergency_current_limit)
        buf.append('}')
        return '\n'.join(buf)

    def get_key(self):
        return self.name

    def get_json_symbols(self, map: Dict[str, 'DistCoordinates']):
        pt1 = map.get(self.cim_class() + ':' + self.name + ':1')
        pt2 = map.get(self.cim_class() + ':' + self.name + ':2')
        buf = []
        buf.append('{"name":"' + self.name + '"')
        buf.append(',"from":"' + self.bus1 + '"')
        buf.append(',"to":"' + self.bus2 + '"')
        buf.append(',"phases":"' + self.glm_phases + '"')
        buf.append(',"is_open":"' + str(self.open) + '"')
        buf.append(',"x1":' + str(pt1.x))
        buf.append(',"y1":' + str(pt1.y))
        buf.append(',"x2":' + str(pt2.x))
        buf.append(',"y2":' + str(pt2.y))
        buf.append('}')
        return '\n'.join(buf)

    def get_dss(self):
        buf = []
        buf.append('new Line.' + self.name)
        buf.append(' phases=' + str(self.dss_phase_count(self.phases, False)) + ' bus1=' +
                   self.dss_bus_phases(self.bus1, self.phases) + ' bus2=' +
                   self.dss_bus_phases(self.bus2, self.phases) + ' switch=y // CIM ' + self.cim_class())
        self.append_dss_ratings(buf, self.normal_current_limit, self.emergency_current_limit)
        if self.open:
            buf.append('  is_open Line.' + self.name + ' 1')
        else:
            buf.append('  close Line.' + self.name + ' 1')
        return '\n'.join(buf)

    def get_open_closed_status(self):
        if self.open:
            return 'Open'
        return 'Closed'

    def get_csv(self):
        return self.name + ',' + self.bus1 + ',' + self.csv_phase_string(self.phases) + ',' + \
            self.bus2 + ',' + self.csv_phase_string(self.phases) + ',' + self.cim_class() + ',' + \
            self.get_open_closed_status()
