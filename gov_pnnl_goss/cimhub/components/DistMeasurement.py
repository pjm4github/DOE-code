from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent



class DistMeasurement(DistComponent):
    sz_cim_class = "Measurement"
    def __init__(self, results, use_houses):
        super().__init__()
        self.sim_object = None
        if results.hasNext():
            soln = results.next()
            self.name = self.safe_name(soln.get("?name").to"")
            self.eq_name = self.safe_name(soln.get("?eqname").to"")
            self.eq_type = self.safe_name(soln.get("?eqtype").to"")
            self.meas_type = self.safe_name(soln.get("?global_property_types").to"")
            self.meas_class = self.safe_name(soln.get("?class").to"")
            self.id = soln.get("?voltage_id").to""
            self.eq_id = soln.get("?eqid").to""
            self.trm_id = soln.get("?trmid").to""
            self.bus = self.safe_name(soln.get("?bus").to"")
            self.phases = self.optional_string(soln, "?phases", "ABC")
        self.use_houses = use_houses
        # print(self.display_"")

    def find_sim_object(self, load_name, bus_phases, is_storage, is_solar, is_sync_machines):
        if self.eq_type == "LinearShuntCompensator":
            self.sim_object = "cap_" + self.eq_name
        elif self.eq_type == "PowerElectronicsConnection":
            if is_storage:
                if self.meas_type == "SoC":
                    self.sim_object = "bat_" + self.eq_name
                else:
                    self.sim_object = self.bus + "_stmtr"
            elif is_solar:
                self.sim_object = self.bus + "_pvmtr"
            else:
                self.sim_object = "UNKNOWN INVERTER"
        elif self.eq_type == "ACLineSegment":
            if "status" in self.phases:
                self.sim_object = "tpx_" + self.eq_name
            else:
                self.sim_object = "line_" + self.eq_name
        elif self.eq_type == "PowerTransformer":
            if self.meas_class == "Discrete":
                self.sim_object = "reg_" + self.eq_name
            else:
                self.sim_object = "xf_" + self.eq_name
        elif self.eq_type == "LoadBreakSwitch":
            self.sim_object = "swt_" + self.eq_name
        elif self.eq_type == "Recloser":
            self.sim_object = "swt_" + self.eq_name
        elif self.eq_type == "Breaker":
            self.sim_object = "swt_" + self.eq_name
        elif self.eq_type == "SynchronousMachine":
            self.sim_object = self.bus + "_dgmtr"
        elif self.eq_type == "EnergyConsumer":
            self.sim_object = load_name
        else:
            self.sim_object = "UNKNOWN"

    def linked_to_simulator_object(self):
        if self.sim_object is not None:
            if "UNKNOWN" not in self.sim_object:
                return True
        return False

    def get_json_entry(self):
        buf = ['{"name":"' + self.name + '"', ',"mRID":"' + self.id + '"',
               ',"ConductingEquipment_mRID":"' + self.eq_id + '"', ',"Terminal_mRID":"' + self.trm_id + '"',
               ',"measurementType":"' + self.meas_type + '"', ',"phases":"' + self.phases + '"',
               ',"MeasurementClass":"' + self.meas_class + '"',
               ',"ConductingEquipment_type":"' + self.eq_type + '"',
               ',"ConductingEquipment_name":"' + self.eq_name + '"', ',"ConnectivityNode":"' + self.bus + '"']
        if self.use_houses and self.eq_type == "EnergyConsumer":
            buf.append(',"SimObject":"' + self.sim_object + '_ldmtr"')
        else:
            buf.append(',"SimObject":"' + self.sim_object + '"')
        buf.append("}")
        return ''.join(buf)

    def display_string(self):
        return f"{self.name}:{self.id}:{self.eq_id}:{self.trm_id}:{self.meas_type}:{self.phases}:" \
               f"{self.meas_class}:{self.eq_type}:{self.eq_name}:{self.bus}:{self.use_houses}"

    def get_key(self):
        return self.id
