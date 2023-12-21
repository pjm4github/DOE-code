from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistXfmrCodeRating(DistComponent):
    sz_cim_class = "XfmrCodeRating"
    sz_csv_header = "Name,NumWindings,NumPhases,Wdg1kV,Wdg1kVA,Wdg1Conn," \
                  "Wdg1R,Wdg2kV,Wdg2kVA,Wdg2Conn,Wdg2R,Wdg3kV,Wdg3kVA,Wdg3Conn," \
                  "Wdg3R,%x12,%x13,%x23,%imag,%NoLoadLoss"

    def __init__(self, results, mapper):
        super().__init__()
        self.pname = ""
        self.tname = ""
        self.id = ""
        self.eid = []
        self.ename = []
        self.wdg = []
        self.conn = []
        self.ang = []
        self.ratedS = []
        self.ratedU = []
        self.r = []
        self.size = 0
        self.glmUsed = False

        if results.hasNext():
            soln = results.next()
            p = soln.get("?pname").to""
            t = soln.get("?tname").to""
            self.pname = self.safe_name(p)
            self.tname = self.safe_name(t)
            self.id = soln.get("?voltage_id").to""
            self.set_size(mapper.get(self.tname))
            for i in range(self.size):
                self.eid.append(soln.get("?eid").to"")
                self.ename.append(self.safe_name(soln.get("?ename").to""))
                self.wdg.append(int(soln.get("?enum").to""))
                self.conn.append(soln.get("?conn").to"")
                self.ang.append(int(soln.get("?ang").to""))
                self.ratedS.append(float(soln.get("?ratedS").to""))
                self.ratedU.append(float(soln.get("?ratedU").to""))
                self.r.append(float(soln.get("?res").to""))
                if i + 1 < self.size:
                    soln = results.next()

    def display_string(self):
        buf = [f"{self.pname}:{self.tname}"]
        for i in range(self.size):
            buf.append(
                f"\n  wdg={self.wdg[i]} conn={self.conn[i]} ang={self.ang[i]} U={self.ratedU[i]: .4f} "
                f"S={self.ratedS[i]: .4f} r={self.r[i]: .4f}"
            )
        return "".join(buf)

    def get_glm(self, sct, oct_):
        buf = []
        rpu = 0.0
        zpu = 0.0
        zbase1 = self.ratedU[0] * self.ratedU[0] / self.ratedS[0]
        zbase2 = self.ratedU[1] * self.ratedU[1] / self.ratedS[1]
        if sct.ll[0] > 0.0 and self.size < 3:
            rpu = 1000.0 * sct.ll[0] / self.ratedS[0]
        else:
            rpu = (self.r[0] / zbase1) + 0.5 * (self.r[1] / zbase2)
        if rpu <= 0.000001:
            rpu = 0.000001

        if sct.fwdg[0] == 1:
            zpu = sct.z[0] / zbase1
        elif sct.fwdg[0] == 2:
            zpu = sct.z[0] / zbase2
        xpu = zpu
        if zpu >= rpu:
            xpu = (zpu * zpu - rpu * rpu) ** 0.5

        sConnect = self.get_gld_transformer_connection(self.conn, self.size)
        sKVA = f"{self.ratedS[0] * 0.001: .3f}"
        buf.append(f"object transformer_configuration {{\n")
        buf.append(f"  name \"xcon_{self.tname}\";\n")
        buf.append(f"  power_rating {sKVA};\n")

        if sConnect == "SINGLE_PHASE_CENTER_TAPPED":
            if "_as_" in self.tname:
                buf.append(f"  powerA_rating {sKVA};\n")
                buf.append(f"  powerB_rating 0.0;\n")
                buf.append(f"  powerC_rating 0.0;\n")
            elif "_bs_" in self.tname:
                buf.append(f"  powerA_rating 0.0;\n")
                buf.append(f"  powerB_rating {sKVA};\n")
                buf.append(f"  powerC_rating 0.0;\n")
            elif "_cs_" in self.tname:
                buf.append(f"  powerA_rating 0.0;\n")
                buf.append(f"  powerB_rating 0.0;\n")
                buf.append(f"  powerC_rating {sKVA};\n")
            buf.append(f"  primary_voltage {self.ratedU[0]: .3f};\n")
            buf.append(f"  secondary_voltage {self.ratedU[1]: .3f};\n")
        elif sConnect == "SINGLE_PHASE":
            if "_an_" in self.tname:
                buf.append(f"  powerA_rating {sKVA};\n")
                buf.append(f"  powerB_rating 0.0;\n")
                buf.append(f"  powerC_rating 0.0;\n")
            elif "_bn_" in self.tname:
                buf.append(f"  powerA_rating 0.0;\n")
                buf.append(f"  powerB_rating {sKVA};\n")
                buf.append(f"  powerC_rating 0.0;\n")
            elif "_cn_" in self.tname:
                buf.append(f"  powerA_rating 0.0;\n")
                buf.append(f"  powerB_rating 0.0;\n")
                buf.append(f"  powerC_rating {sKVA};\n")
            buf.append(f"  primary_voltage {self.ratedU[0] * (3.0 ** 0.5): .3f};\n")
            buf.append(f"  secondary_voltage {self.ratedU[1] * (3.0 ** 0.5): .3f};\n")
            sConnect = "WYE_WYE"
        else:
            buf.append(f"  primary_voltage {self.ratedU[0]: .3f};\n")
            buf.append(f"  secondary_voltage {self.ratedU[1]: .3f};\n")
        if sConnect == "Y_D":
            buf.append(f"  connect_type WYE_WYE; // should be Y_D\n")
        else:
            buf.append(f"  connect_type {sConnect};\n")
        if sConnect == "SINGLE_PHASE_CENTER_TAPPED":
            impedance = self.c_format(complex(0.5 * rpu, 0.8 * xpu))
            impedance1 = self.c_format(complex(rpu, 0.4 * xpu))
            impedance2 = self.c_format(complex(rpu, 0.4 * xpu))
            buf.append(f"  impedance {impedance};\n")
            buf.append(f"  impedance1 {impedance1};\n")
            buf.append(f"  impedance2 {impedance2};\n")
        else:
            buf.append(f"  resistance {rpu: .6f};\n")
            buf.append(f"  reactance {xpu: .6f};\n")
        if oct_.iexc > 0.0:
            buf.append(f"  shunt_reactance {100.0 / oct_.iexc: .6f};\n")
        if oct_.nll > 0.0:
            buf.append(f"  shunt_resistance {self.ratedS[0] / (oct_.nll * 1000.0): .6f};\n")
        buf.append("}\n")
        return "".join(buf)

    def get_dss(self, sct, oct_):
        phases = 3
        for i in range(self.size):
            if "I" in self.conn[i]:
                phases = 1
                break
        buf = []
        buf.append(f"new Xfmrcode.{self.tname} windings={self.size} phases={phases}")

        for i in range(sct.size):
            fwdg = sct.fwdg[i]
            twdg = sct.twdg[i]
            zbase = self.ratedU[fwdg - 1] * self.ratedU[fwdg - 1] / self.ratedS[fwdg - 1]
            xpct = 100.0 * sct.z[i] / zbase
            if (fwdg == 1 and twdg == 2) or (fwdg == 2 and twdg == 1):
                buf.append(f" xhl={xpct: .6f}")
            elif (fwdg == 1 and twdg == 3) or (fwdg == 3 and twdg == 1):
                buf.append(f" xht={xpct: .6f}")
            elif (fwdg == 2 and twdg == 3) or (fwdg == 3 and twdg == 2):
                buf.append(f" xlt={xpct: .6f}")

        buf.append(
            f" %imag={oct_.iexc: .3f} %noloadloss={100.0 * 1000.0 * oct_.nll / self.ratedS[0]: .3f}\n")

        for i in range(self.size):
            bDelta = "D" in self.conn[i]
            zbase = self.ratedU[i] * self.ratedU[i] / self.ratedS[i]
            buf.append(f"~ wdg={i + 1} conn={self.dss_conn(bDelta)} "
                       f"kv={0.001 * self.ratedU[i]: .3f} kva={0.001 * self.ratedS[i]: .1f} "
                       f"%r={100.0 * self.r[i] / zbase: .6f}\n")

        return "".join(buf)

    @staticmethod
    def get_csv_header():
        return "Name,NumWindings,NumPhases," + ",".join(
            [f"Wdg{i + 1}kV,Wdg{i + 1}kVA,Wdg{i + 1}Conn,Wdg{i + 1}R" for i in range(3)]
        ) + ",%x12,%x13,%x23,%imag,%NoLoadLoss"

    def get_csv(self, sct, oct_):
        phases = 3
        for i in range(self.size):
            if "I" in self.conn[i]:
                phases = 1
                break

        buf = [f"{self.tname},{self.size},{phases}"]
        for i in range(self.size):
            bDelta = "D" in self.conn[i]
            zbase = self.ratedU[i] * self.ratedU[i] / self.ratedS[i]
            buf.append(f",{0.001 * self.ratedU[i]: .3f},{0.001 * self.ratedS[i]: .1f},"
                       f"{self.dss_conn(bDelta)},{100.0 * self.r[i] / zbase: .6f}")
        if self.size < 3:
            buf.extend([",,,", ",,,"])

        x12 = 0.0
        x13 = 0.0
        x23 = 0.0
        for i in range(sct.size):
            fwdg = sct.fwdg[i]
            twdg = sct.twdg[i]
            zbase = self.ratedU[fwdg - 1] * self.ratedU[fwdg - 1] / self.ratedS[fwdg - 1]
            xpct = 100.0 * sct.z[i] / zbase
            if (fwdg == 1 and twdg == 2) or (fwdg == 2 and twdg == 1):
                x12 = xpct
            elif (fwdg == 1 and twdg == 3) or (fwdg == 3 and twdg == 1):
                x13 = xpct
            elif (fwdg == 2 and twdg == 3) or (fwdg == 3 and twdg == 2):
                x23 = xpct

        buf.extend([f",{x12: .6f},{x13: .6f},{x23: .6f}",
                    f",{oct_.iexc: .3f},{0.001 * oct_.nll / self.ratedS[0]: .3f}\n"])
        return "".join(buf)

    def get_key(self):
        return self.tname

    def get_json_entry(self) -> str:
        buf = []
        buf.append(f'{{"name":"{self.pname}"')
        buf.append(f',"mRID":"{self.id}"')
        buf.append("}")
        return '\n'.join(buf)

    def set_size(self, val):
        size = val
        self.eid = [""] * size
        self.ename = [""] * size
        self.wdg = [0] * size
        self.conn = [""] * size
        self.ang = [0] * size
        self.ratedS = [0.0] * size
        self.ratedU = [0.0] * size
        self.r = [0.0] * size
