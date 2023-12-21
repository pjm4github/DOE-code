import math
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistRegulator(DistComponent):
    sz_cim_class = "Regulator"
    sz_csv_header = "Name,Bus1,Phase,Bus2,Phase,Vreg,PTRatio,CTRating,Band,R,X,revR,revX"

    def __init__(self, results, query_handler):
        super().__init__()
        self.pname = ""
        self.bank_phases = ""
        self.has_tanks = False
        #  GridLAB-D only supports different bank parameters for tap (step), R and X
        self.step = []
        self.fwd_r = []
        self.fwd_x = []
        #  GridLAB-D codes phs variations into certain attribute labels
        self.phs = []
        # TODO: if any of these vary within the bank, should write separate single-phase instances for GridLAB-D
        self.tname = []
        self.rname = []
        self.id = []
        self.mon_phs = []
        self.mode = []
        self.ctl_mode = []
        self.wnum = []
        self.high_step = []
        self.low_step = []
        self.neutral_step = []
        self.normal_step = []
        self.enabled = []
        self.ldc = []
        self.ltc = []
        self.discrete = []
        self.ctl_enabled = []
        self.incr = []
        self.neutral_u = []
        self.init_delay = []
        self.sub_delay = []
        self.vlim = []
        self.vset = []
        self.vbw = []
        self.rev_r = []
        self.rev_x = []
        self.ct_rating = []
        self.ct_ratio = []
        self.pt_ratio = []
        self.size = 0
        self.normal_current_limit = 0.0
        self.emergency_current_limit = 0.0
        self.pxfid = ""
        if results:
            soln = next(results)
            self.pname = self.safe_name(soln['?pname'].to"")
            self.pxfid = soln['?pxfid'].to""
            self.set_size(query_handler)
            self.hasTanks = False
            if self.size > 0:
                self.hasTanks = True
            self.phs = [soln['?phs'].to""] * self.size
            self.rname = [self.safe_name(soln['?rname'].to"")] * self.size
            self.tname = [self.safe_name(soln['?tname'].to"") if self.hasTanks else ""] * self.size
            self.id = [soln['?voltage_id'].to""] * self.size
            self.monphs = [soln['?monphs'].to""] * self.size
            self.mode = [soln['?mode'].to""] * self.size
            self.ctlmode = [soln['?ctlmode'].to""] * self.size
            self.wnum = [int(soln['?wnum'].to"")] * self.size
            self.highStep = [int(soln['?highStep'].to"")] * self.size
            self.lowStep = [int(soln['?lowStep'].to"")] * self.size
            self.neutralStep = [int(soln['?neutralStep'].to"")] * self.size
            self.normalStep = [int(soln['?normalStep'].to"")] * self.size
            self.enabled = [bool(soln['?enabled'].to"")] * self.size
            self.ldc = [bool(soln['?ldc'].to"")] * self.size
            self.ltc = [bool(soln['?ltc'].to"")] * self.size
            self.discrete = [bool(soln['?discrete'].to"")] * self.size
            self.ctl_enabled = [bool(soln['?ctl_enabled'].to"")] * self.size
            self.incr = [float(soln['?incr'].to"")] * self.size
            self.neutralU = [float(soln['?neutralU'].to"")] * self.size
            self.step = [int(soln['?step'].to"")] * self.size
            self.initDelay = [float(soln['?initDelay'].to"")] * self.size
            self.subDelay = [float(soln['?subDelay'].to"")] * self.size
            self.vlim = [float(soln['?vlim'].to"")] * self.size
            self.vset = [float(soln['?vset'].to"")] * self.size
            self.vbw = [float(soln['?vbw'].to"")] * self.size
            self.fwdR = [float(soln['?fwdR'].to"")] * self.size
            self.fwdX = [float(soln['?fwdX'].to"")] * self.size
            self.revR = [float(soln['?revR'].to"")] * self.size
            self.revX = [float(soln['?revX'].to"")] * self.size
            self.ctRating = [float(soln['?ctRating'].to"")] * self.size
            self.ctRatio = [float(soln['?ctRatio'].to"")] * self.size
            self.ptRatio = [float(soln['?ptRatio'].to"")] * self.size
            self.bankphases = "".join(self.phs)

        # print(self.display_"")

    def add_json_double_array(self, buf, tag, vals):
        buf.append(f",\"{tag}\":[")
        for i in range(self.size):
            buf.append(f"{vals[i]:.4f}")
            if i + 1 < self.size:
                buf.append(",")
            else:
                buf.append("]")

    def add_json_integer_array(self, buf, tag, vals):
        buf.append(f",\"{tag}\":[")
        for i in range(self.size):
            buf.append(str(vals[i]))
            if i + 1 < self.size:
                buf.append(",")
            else:
                buf.append("]")

    def add_json_boolean_array(self, buf, tag, vals):
        buf.append(f",\"{tag}\":[")
        for i in range(self.size):
            buf.append("true" if vals[i] else "false")
            if i + 1 < self.size:
                buf.append(",")
            else:
                buf.append("]")

    def add_json_string_array(self, buf, tag, vals):
        buf.append(f",\"{tag}\":[")
        for i in range(self.size):
            if vals[i] is None:
                buf.append("null")
            else:
                buf.append(f"\"{vals[i]}\"")
            if i + 1 < self.size:
                buf.append(",")
            else:
                buf.append("]")

    def get_json_entry(self):
        buf = []
        buf.append('{"bank_name":"' + self.pname + '"')
        buf.append(',"size":"' + str(self.size) + '"')
        buf.append(',"bank_phases":"' + self.bankphases + '"')
        self.add_json_string_array(buf, "tank_name", self.tname)
        self.add_json_integer_array(buf, "end_number", self.wnum)
        self.add_json_string_array(buf, "end_phase", self.phs)
        self.add_json_string_array(buf, "rtc_name", self.rname)
        self.add_json_string_array(buf, "mrid", self.id)
        self.add_json_string_array(buf, "monitored_phase", self.monphs)
        self.add_json_string_array(buf, "tap_changer.tcul_control_mode", self.mode)
        self.add_json_integer_array(buf, "high_step", self.high_step)
        self.add_json_integer_array(buf, "low_step", self.low_step)
        self.add_json_integer_array(buf, "neutral_step", self.neutral_step)
        self.add_json_integer_array(buf, "normal_step", self.normal_step)
        self.add_json_boolean_array(buf, "tap_changer.control_enabled", self.enabled)
        self.add_json_boolean_array(buf, "line_drop_compensation", self.ldc)
        self.add_json_boolean_array(buf, "ltc_flag", self.ltc)
        self.add_json_boolean_array(buf, "regulating_control.enabled", self.ctl_enabled)
        self.add_json_boolean_array(buf, "regulating_control.discrete", self.discrete)
        self.add_json_string_array(buf, "regulating_control.mode", self.ctlmode)
        self.add_json_integer_array(buf, "step", self.step)
        self.add_json_double_array(buf, "target_value", self.vset)
        self.add_json_double_array(buf, "target_deadband", self.vbw)
        self.add_json_double_array(buf, "limit_voltage", self.vlim)
        self.add_json_double_array(buf, "step_voltage_increment", self.incr)
        self.add_json_double_array(buf, "neutral_u", self.neutral_u)
        self.add_json_double_array(buf, "initial_delay", self.init_delay)
        self.add_json_double_array(buf, "subsequent_delay", self.sub_delay)
        self.add_json_double_array(buf, "line_drop_r", self.fwd_r)
        self.add_json_double_array(buf, "line_drop_x", self.fwd_x)
        self.add_json_double_array(buf, "reverse_line_drop_r", self.rev_r)
        self.add_json_double_array(buf, "reverse_line_drop_x", self.rev_x)
        self.add_json_double_array(buf, "ct_rating", self.ct_rating)
        self.add_json_double_array(buf, "ct_ratio", self.ct_ratio)
        self.add_json_double_array(buf, "pt_ratio", self.pt_ratio)
        buf.append('}')
        return ''.join(buf)

    def display_string(self):
        buf = []
        buf.append(f"{self.pname} bankphases={self.bank_phases}")
        for i in range(self.size):
            buf.append(f"\n  {i}")
            buf.append(f" {self.wnum[i]}:{self.rname[i]}:{self.phs[i]}")
            buf.append(f" tank={self.tname[i]}")
            buf.append(f" mode={self.mode[i]}")
            buf.append(f" ctlmode={self.ctl_mode[i]}")
            buf.append(f" monphs={self.mon_phs[i]}")
            buf.append(f" enabled={self.enabled[i]}")
            buf.append(f" ctl_enabled={self.ctl_enabled[i]}")
            buf.append(f" discrete={self.discrete[i]}")
            buf.append(f" ltc={self.ltc[i]}")
            buf.append(f" ldc={self.ldc[i]}")
            buf.append(f" highStep={self.high_step[i]}")
            buf.append(f" lowStep={self.low_step[i]}")
            buf.append(f" neutralStep={self.neutral_step[i]}")
            buf.append(f" normalStep={self.normal_step[i]}")
            buf.append(f" neutralU={self.neutral_u[i]:.4f}")
            buf.append(f" step={self.step[i]}")
            buf.append(f" incr={self.incr[i]:.4f}")
            buf.append(f" initDelay={self.initDelay[i]:.4f}")
            buf.append(f" subDelay={self.subDelay[i]:.4f}")
            buf.append(f" vlim={self.vlim[i]:.4f}")
            buf.append(f" vset={self.vset[i]:.4f}")
            buf.append(f" vbw={self.vbw[i]:.4f}")
            buf.append(f" fwdR={self.fwdR[i]:.4f}")
            buf.append(f" fwdX={self.fwdX[i]:.4f}")
            buf.append(f" revR={self.revR[i]:.4f}")
            buf.append(f" revX={self.revX[i]:.4f}")
            buf.append(f" ctRating={self.ctRating[i]:.4f}")
            buf.append(f" ctRatio={self.ctRatio[i]:.4f}")
            buf.append(f" ptRatio={self.ptRatio[i]:.4f}")
        return "\n".join(buf)

    # def get_json_symbols(self, query_handler):
    #     symbol_data = []
    #     query_handler.set_query_param('pxfid', self.pxfid)
    #     results = query_handler.query(
    #         "SELECT ?symbol ?case ?ctlMode ?ctlFlag ?controlType ?localControl ?controlRange WHERE {"
    #         "?feeder c:Feeder.Equipment ?eq. ?eq c:ConductingEquipment.BaseVoltage ?bv. "
    #         "?eq c:IdentifiedObject.name ?symbol. ?xr c:TapChanger.TransformerWinding ?xw. "
    #         "?xr c:RegulatingControl.RegulatingWinding ?rw. ?rw c:TapChanger.RegulatingControl ?ctl. "
    #         "?ctl c:RegulatingControl.mode ?ctlMode. ?ctl c:RegulatingControl.monitoredPhase ?ctlFlag. "
    #         "?ctl c:RegulatingControl.controlEnabled ?controlType. "
    #         "?ctl c:RegulatingControl.discrete ?localControl. ?ctl c:RegulatingControl.targetRange ?controlRange. "
    #         "?rw c:TransformerWinding.PowerTransformer ?pxf. ?pxf c:IdentifiedObject.mRID ?pxfid. "
    #         "?eq c:IdentifiedObject.name ?case. }", "Regulator symbols")
    #     for soln in results:
    #         if soln is not None:
    #             symbol = soln['?symbol'].to""
    #             safe_symbol = self.safe_symbol_name(symbol)
    #             symbol_data.append(self.get_json_entry(safe_symbol, soln))
    #
    #     return json.dumps(symbol_data)
    #
    def get_json_symbols(self, map, map_tank, map_xfmr):
        pt1 = map.get("PowerTransformer:" + self.pname + ":1")
        pt2 = map.get("PowerTransformer:" + self.pname + ":2")

        if self.has_tanks:
            tank = map_tank.get(self.tname[0])
            bus1, bus2 = tank.bus[0], tank.bus[1]
        else:
            xfmr = map_xfmr.get(self.pname)
            bus1, bus2 = xfmr.bus[0], xfmr.bus[1]

        buf = {
            "name": self.pname,
            "from": bus1,
            "to": bus2,
            "phases": self.bankphases,
            "x1": pt1.x,
            "y1": pt1.y,
            "x2": pt2.x,
            "y2": pt2.y
        }
        return buf

    @staticmethod
    def safe_symbol_name(name):
        return name.replace('"', '').replace("'", "")

    def set_size(self, query_handler):
        self.size = 1
        self.has_tanks = False
        sz_count = f"SELECT (count (?tank) as ?count) WHERE {{" \
                   f" ?tank c:TransformerTank.PowerTransformer ?pxf." \
                   f" ?pxf c:IdentifiedObject.mRID \"{self.pxfid}\"." \
                   f"}}"
        results = query_handler.query(sz_count, "XF count for regulator sizing")
        if results.hasNext():
            soln = results.next()
            n_tanks = soln.getLiteral("?count").getInt()
            if n_tanks > 0:
                self.has_tanks = True
                self.size = n_tanks
        self.phs = [""] * self.size
        self.rname = [""] * self.size
        self.tname = [""] * self.size
        self.id = [""] * self.size
        self.mon_phs = [""] * self.size
        self.mode = [""] * self.size
        self.ctl_mode = [""] * self.size
        self.wnum = [0] * self.size
        self.high_step = [0] * self.size
        self.low_step = [0] * self.size
        self.neutral_step = [0] * self.size
        self.normal_step = [0] * self.size
        self.enabled = [False] * self.size
        self.ldc = [False] * self.size
        self.ltc = [False] * self.size
        self.discrete = [False] * self.size
        self.ctl_enabled = [False] * self.size
        self.incr = [0.0] * self.size
        self.neutral_u = [0.0] * self.size
        self.init_delay = [0.0] * self.size
        self.sub_delay = [0.0] * self.size
        self.vlim = [0.0] * self.size
        self.vset = [0.0] * self.size
        self.vbw = [0.0] * self.size
        self.step = [0] * self.size
        self.fwd_r = [0.0] * self.size
        self.fwd_x = [0.0] * self.size
        self.rev_r = [0.0] * self.size
        self.rev_x = [0.0] * self.size
        self.ct_rating = [0.0] * self.size
        self.ct_ratio = [0.0] * self.size
        self.pt_ratio = [0.0] * self.size

    def get_csv(self, bus1, phs1, bus2, phs2):
        buf = []
        for i in range(self.size):
            buf.append(
                f"{self.rname[i]},{bus1},{phs1},{bus2},{phs2},"
                f"{self.vset[i]:.2f},{self.pt_ratio[i]:.2f},{self.ct_rating[i]:.2f},"
                f"{self.vbw[i]:.2f},{self.fwd_r[i]:.2f},{self.fwd_x[i]:.2f},"
                f"{self.rev_r[i]:.2f},{self.rev_x[i]:.2f}"
            )
        return '\n'.join(buf)

    def get_ganged_glm(self, xfmr):
        return self.get_common_glm("Yy", xfmr.bus[0], xfmr.bus[1])

    def get_common_glm(self, vgrp, bus1, bus2):
        buf = []
        d_reg = 0.01 * 0.5 * self.incr[0] * (self.high_step[0] - self.low_step[0])
        b_delta_regulator = False

        buf.append(f"object regulator_configuration {{")
        buf.append(f"  name \"rcon_{self.pname}\";")
        if "D" in vgrp or "d" in vgrp:
            b_delta_regulator = True
            if self.bankphases == "ABBC":
                buf.append("  connect_type WYE_WYE; // OPEN_DELTA_ABBC not supported for NR")
            elif self.bankphases == "CABA":
                buf.append("  connect_type WYE_WYE; // OPEN_DELTA_CABA not supported for NR")
            elif self.bankphases == "BCAC":
                buf.append("  connect_type WYE_WYE; // OPEN_DELTA_BCAC not supported for NR")
            else:
                buf.append("  connect_type WYE_WYE; // CLOSED_DELTA not supported for NR")
            self.bankphases = "ABC"
        else:
            buf.append("  connect_type WYE_WYE;")

        if self.vset[0] > 0.0 and self.vbw[0] > 0.0 and self.ltc[0]:
            if self.ldc[0]:
                buf.append("  Control MANUAL; // LINE_DROP_COMP;")
            else:
                buf.append("  Control MANUAL; // OUTPUT_VOLTAGE;")
        else:
            buf.append("  Control MANUAL;")

        buf.append("  // use these for OUTPUT_VOLTAGE mode")
        buf.append(f"  // band_center {format(self.vset[0] * self.pt_ratio[0], '.6f')};")
        buf.append(f"  // band_width {format(self.vbw[0] * self.pt_ratio[0], '.6f')};")
        buf.append("  // use these for LINE_DROP_COMP mode")
        buf.append(f"  // band_center {format(self.vset[0], '.6f')};")
        buf.append(f"  // band_width {format(self.vbw[0], '.6f')};")
        buf.append("  // transducer ratios only apply to LINE_DROP_COMP mode")
        buf.append(f"  current_transducer_ratio {format(self.ct_ratio[0], '.6f')};")
        if b_delta_regulator:
            buf.append(f"  power_transducer_ratio {format(self.pt_ratio[0] / math.sqrt(3.0), '.6f')};")
        else:
            buf.append(f"  power_transducer_ratio {format(self.pt_ratio[0], '.6f')};")
        buf.append(f"  dwell_time {format(self.init_delay[0], '.6f')};")
        buf.append(f"  raise_taps {abs(self.high_step[0] - self.neutral_step[0])};")
        buf.append(f"  lower_taps {abs(self.neutral_step[0] - self.low_step[0])};")
        buf.append(f"  regulation {format(d_reg, '.6f')};")
        buf.append("  Type B;")
        if self.has_tanks:
            for i in range(self.size):
                buf.append(f"  compensator_r_setting_{self.phs[i][0]} {format(self.fwd_r[i], '.6f')};")
                buf.append(f"  compensator_x_setting_{self.phs[i][0]} {format(self.fwd_x[i], '.6f')};")
                buf.append(f"  // comment out the manual tap setting if using automatic control")
                buf.append(f"  tap_pos_{self.phs[i][0]} {self.step[i]};")
        else:
            buf.append(f"  compensator_r_setting_A {format(self.fwd_r[0], '.6f')};")
            buf.append(f"  compensator_r_setting_B {format(self.fwd_r[0], '.6f')};")
            buf.append(f"  compensator_r_setting_C {format(self.fwd_r[0], '.6f')};")
            buf.append(f"  compensator_x_setting_A {format(self.fwd_x[0], '.6f')};")
            buf.append(f"  compensator_x_setting_B {format(self.fwd_x[0], '.6f')};")
            buf.append(f"  compensator_x_setting_C {format(self.fwd_x[0], '.6f')};")
            buf.append("  // comment out the manual tap settings if using automatic control")
            buf.append(f"  tap_pos_A {self.step[0]};")
            buf.append(f"  tap_pos_B {self.step[0]};")
            buf.append(f"  tap_pos_C {self.step[0]};")

        buf.append("}")
        buf.append(f"object regulator {{")
        buf.append(f"  name \"reg_{self.pname}\";")
        buf.append(f"  from \"{bus1}\";")
        buf.append(f"  to \"{bus2}\";")
        buf.append(f"  phases {self.bankphases};")
        buf.append(f"  configuration \"rcon_{self.pname}\";")
        self.append_glm_ratings(buf, self.bankphases, self.normal_current_limit, self.emergency_current_limit)
        buf.append("}")
        return '\n'.join(buf)

    def get_tanked_glm(self, tank):
        return self.get_common_glm(tank.vgrp, tank.bus[0], tank.bus[1])

    def get_dss(self):
        buf = ""
        xf_name = ""
    
        for i in range(self.size):
            if self.size > 1:
                xf_name = self.tname[i]
            elif self.has_tanks:
                xf_name = self.tname[i]
            else:
                xf_name = self.pname
    
            buf += "new RegControl." + self.rname[i] + " transformer=" + xf_name + " winding=" + str(self.wnum[i])
            buf += " vreg=" + str(round(self.vset[i], 2)) + " band=" + str(round(self.vbw[i], 2)) + " ptratio=" + str(round(self.pt_ratio[i], 2))
            buf += " ctprim=" + str(round(self.ct_rating[i], 2)) + " r=" + str(round(self.fwd_r[i], 2))
            buf += " x=" + str(round(self.fwd_x[i], 2)) + " revr=" + str(round(self.rev_r[i], 2)) + " revx=" + str(round(self.rev_x[i], 2))
            buf += " delay=" + str(round(self.init_delay[i], 2)) + " tapdelay=" + str(round(self.sub_delay[i], 2)) + " vlimit=" + str(round(self.vlim[i], 2))
            buf += " TapNum=" + str(self.step[i]) + "\n"
            # ptphase, enabled
            turns_ratio = 1.0 + 0.01 * self.step[i] * self.incr[i]
            buf += "\nedit transformer." + xf_name + " wdg=" + str(self.wnum[i]) + " tap=" + str(round(turns_ratio, 6)) + "\n"
    
        return buf

    def get_key(self):
        return self.pname
    