import random
import math
#
# class Complex:
#     def __init__(self, real, imaginary=0.0):
#         self.real = real
#         self.imaginary = imaginary
#
#     def multiply(self, other):
#         real_part = (self.real * other.real) - (self.imaginary * other.imaginary)
#         imaginary_part = (self.real * other.imaginary) + (self.imaginary * other.real)
#         return Complex(real_part, imaginary_part)
#
#     def divide(self, other):
#         denominator = (other.real ** 2) + (other.imaginary ** 2)
#         real_part = ((self.real * other.real) + (self.imaginary * other.imaginary)) / denominator
#         imaginary_part = ((self.imaginary * other.real) - (self.real * other.imaginary)) / denominator
#         return Complex(real_part, imaginary_part)
#
#     def conjugate(self):
#         return Complex(self.real, -self.imaginary)
#
#     def abs(self):
#         return math.sqrt(self.real**2 + self.imaginary**2)


class GldNode:
    neg120 = complex(-0.5, -0.5 * math.sqrt(3.0))
    pos120 = complex(-0.5, 0.5 * math.sqrt(3.0))

    def __init__(self, name):
        self.name = name
        self.loadname = ""
        self.phases = ""
        self.nomvln = -1.0
        self.pa_z = 0.0
        self.pb_z = 0.0
        self.pc_z = 0.0
        self.qa_z = 0.0
        self.qb_z = 0.0
        self.qc_z = 0.0
        self.pa_i = 0.0
        self.pb_i = 0.0
        self.pc_i = 0.0
        self.qa_i = 0.0
        self.qb_i = 0.0
        self.qc_i = 0.0
        self.pa_p = 0.0
        self.pb_p = 0.0
        self.pc_p = 0.0
        self.qa_p = 0.0
        self.qb_p = 0.0
        self.qc_p = 0.0
        self.bDelta = False
        self.bSwing = False
        self.bSolarInverters = False
        self.bStorageInverters = False
        self.bSyncMachines = False
        self.bSwingPQ = False
        self.bTertiaryWinding = False
        self.bSecondary = False

    @staticmethod
    def c_format(c: complex):
        if c.imag < 0:
            sgn = "-"
        else:
            sgn = "+"
        return f"{c.real:.6g}{sgn}{abs(c.imag):.6g}j"

    def display_string(self):
        return f"{self.name}:{self.phases}:{self.loadname}:{self.bSecondary}"

    def add_phases(self, phs):
        buf = ""
        if 'A' in self.phases or 'A' in phs:
            buf += "A"
        if 'B' in self.phases or 'B' in phs:
            buf += "B"
        if 'C' in self.phases or 'C' in phs:
            buf += "C"
        if 'status' in phs.lower():
            self.bSecondary = True
        elif 'ABC' in phs:
            self.bSecondary = False
        self.phases = buf

    def reset_phases(self, phs):
        self.phases = ""
        self.bSecondary = False
        self.add_phases(phs)

    def get_phases(self):
        if self.bDelta and not self.bSecondary:
            return self.phases + "D"
        if self.bSecondary:
            return self.phases + "S"
        return self.phases + "N"

    def accumulate_loads(self, ldname, phs, pL, qL, Pv, Qv, Pz, Pi, Pp, Qz, Qi, Qp, randomZIP):
        fa, fb, fc, denom = 0.0, 0.0, 0.0, 0.0
        self.loadname = "ld_" + ldname

        if "A" in phs or "status" in phs:
            fa = 1.0
            denom += 1.0
        if "B" in phs or "status" in phs:
            fb = 1.0
            denom += 1.0
        if "C" in phs:
            fc = 1.0
            denom += 1.0

        if fa > 0.0:
            fa /= denom
        if fb > 0.0:
            fb /= denom
        if fc > 0.0:
            fc /= denom

        fpz, fqz, fpi, fqi, fpp, fqp = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

        if not randomZIP:
            denom = Pz + Pi + Pp
            if denom > 0.0:
                fpz = Pz / denom
                fpi = Pi / denom
                fpp = Pp / denom
            else:
                if 0.9 < Pv < 1.1:
                    fpi = 1.0
                elif 1.9 < Pv < 2.1:
                    fpz = 1.0
                else:
                    fpp = 1.0

            denom = Qz + Qi + Qp
            if denom > 0.0:
                fqz = Qz / denom
                fqi = Qi / denom
                fqp = Qp / denom
            else:
                if 0.9 < Qv < 1.1:
                    fqi = 1.0
                elif 1.9 < Qv < 2.1:
                    fqz = 1.0
                else:
                    fqp = 1.0
        else:
            Zpmax, Zpmin, Ppmax, Ppmin = 1, 0, 3, 0
            rand = random.Random()
            fpz = round(Zpmin + rand.uniform(0, 1) * (Zpmax - Zpmin), 2)
            fpp = round(Ppmin + rand.uniform(0, 1) * (Ppmax - Ppmin), 2)
            fpi = 1.0 - fpz - fpp

            Zqmax, Zqmin, Pqmax, Pqmin = 1, 0, 1, 0
            fqz = round(Zqmin + rand.uniform(0, 1) * (Zqmax - Zqmin), 2)
            fqp = round(Pqmin + rand.uniform(0, 1) * (Pqmax - Pqmin), 2)
            fqi = 1.0 - fqz - fqp

        pL *= 1000.0
        qL *= 1000.0
        self.add_phases(phs)
        self.pa_z += fa * pL * fpz
        self.pb_z += fb * pL * fpz
        self.pc_z += fc * pL * fpz
        self.qa_z += fa * qL * fqz
        self.qb_z += fb * qL * fqz
        self.qc_z += fc * qL * fqz
        self.pa_i += fa * pL * fpi
        self.pb_i += fb * pL * fpi
        self.pc_i += fc * pL * fpi
        self.qa_i += fa * qL * fqi
        self.qb_i += fb * qL * fqi
        self.qc_i += fc * qL * fqi
        self.pa_p += fa * pL * fpp
        self.pb_p += fb * pL * fpp
        self.pc_p += fc * pL * fpp
        self.qa_p += fa * qL * fqp
        self.qb_p += fb * qL * fqp
        self.qc_p += fc * qL * fqp

    def apply_zip(self, Z, I, P):
        total = Z + I + P
        Z /= total
        I /= total
        P /= total

        total = self.pa_z + self.pa_i + self.pa_p
        self.pa_z = total * Z
        self.pa_i = total * I
        self.pa_p = total * P
        total = self.qa_z + self.qa_i + self.qa_p
        self.qa_z = total * Z
        self.qa_i = total * I
        self.qa_p = total * P

        total = self.pb_z + self.pb_i + self.pb_p
        self.pb_z = total * Z
        self.pb_i = total * I
        self.pb_p = total * P
        total = self.qb_z + self.qb_i + self.qb_p
        self.qb_z = total * Z
        self.qb_i = total * I
        self.qb_p = total * P

        total = self.pc_z + self.pc_i + self.pc_p
        self.pc_z = total * Z
        self.pc_i = total * I
        self.pc_p = total * P
        total = self.qc_z + self.qc_i + self.qc_p
        self.qc_z = total * Z
        self.qc_i = total * I
        self.qc_p = total * P


    def rescale_load(self, scale):
        self.pa_z *= scale
        self.pb_z *= scale
        self.pc_z *= scale
        self.qa_z *= scale
        self.qb_z *= scale
        self.qc_z *= scale
        self.pa_i *= scale
        self.pb_i *= scale
        self.pc_i *= scale
        self.qa_i *= scale
        self.qb_i *= scale
        self.qc_i *= scale
        self.pa_p *= scale
        self.pb_p *= scale
        self.pc_p *= scale
        self.qa_p *= scale
        self.qb_p *= scale
        self.qc_p *= scale

    def has_load(self):
        return (
            self.pa_z != 0.0
            or self.pb_z != 0.0
            or self.pc_z != 0.0
            or self.qa_z != 0.0
            or self.qb_z != 0.0
            or self.qc_z != 0.0
            or self.pa_i != 0.0
            or self.pb_i != 0.0
            or self.pc_i != 0.0
            or self.qa_i != 0.0
            or self.qb_i != 0.0
            or self.qc_i != 0.0
            or self.pa_p != 0.0
            or self.pb_p != 0.0
            or self.pc_p != 0.0
            or self.qa_p != 0.0
            or self.qb_p != 0.0
            or self.qc_p != 0.0
        )

    def copy_load(self, src):
        self.loadname = src.loadname
        self.pa_z = src.pa_z
        self.pa_i = src.pa_i
        self.pa_p = src.pa_p
        self.qa_z = src.qa_z
        self.qa_i = src.qa_i
        self.qa_p = src.qa_p
        self.pb_z = src.pb_z
        self.pb_i = src.pb_i
        self.pb_p = src.pb_p
        self.qb_z = src.qb_z
        self.qb_i = src.qb_i
        self.qb_p = src.qb_p
        self.pc_z = src.pc_z
        self.pc_i = src.pc_i
        self.pc_p = src.pc_p
        self.qc_z = src.qc_z
        self.qc_i = src.qc_i
        self.qc_p = src.qc_p
        return True

    def append_sub_meter(self, buf, meter_class, suffix):
        buf.append(f"object {meter_class} {{\n")
        buf.append(f"  name \"{self.name}{suffix}\";\n")
        buf.append(f"  parent \"{self.name}\";\n")
        buf.append(f"  phases {self.get_phases()};\n")
        buf.append(f"  nominal_voltage {self.nomvln:.2f};\n")
        buf.append("}\n")
        return buf

    def get_glm(self, load_scale, bWantSched, fSched, bWantZIP, useHouses, 
                Zcoeff, Icoeff, Pcoeff, separateLoads):
        buf = []
    
        if self.bTertiaryWinding:
            return ""
    
        if self.bSwing:
            buf.append(f"object substation {{\n")
            buf.append(f"  name \"{self.name}\";\n")
            buf.append(f"  bustype SWING;\n")
            buf.append(f"  phases {self.get_phases()};\n")
            buf.append(f"  nominal_voltage {self.nomvln:.2f};\n")
            buf.append("  base_power 12MVA;\n")
            buf.append("  power_convergence_value 100VA;\n")
            buf.append("  positive_sequence_voltage ${VSOURCE};\n")
            buf.append("}\n")
        elif self.bSecondary:
            buf.append(f"object triplex_node {{\n")
            buf.append(f"  name \"{self.name}\";\n")
            buf.append(f"  phases {self.get_phases()};\n")
            buf.append(f"  nominal_voltage {self.nomvln:.2f};\n")
            buf.append("}\n")
            if self.bSolarInverters:
                self.append_sub_meter(buf, "triplex_meter", "_pvmtr")
            if self.bStorageInverters:
                self.append_sub_meter(buf, "triplex_meter", "_stmtr")
            if self.bSyncMachines:
                self.append_sub_meter(buf, "triplex_meter", "_dgmtr")
        else:  # primary connected
            buf.append(f"object node {{\n")
            buf.append(f"  name \"{self.name}\";\n")
            buf.append(f"  phases {self.get_phases()};\n")
            buf.append(f"  nominal_voltage {self.nomvln:.2f};\n")
            if self.bSyncMachines or self.bStorageInverters:
                buf.append("  bustype SWING_PQ;\n")
                self.bSwingPQ = True
            buf.append("}\n")
            if self.bSolarInverters:
                self.append_sub_meter(buf, "meter", "_pvmtr")
            if self.bStorageInverters:
                self.append_sub_meter(buf, "meter", "_stmtr")
            if self.bSyncMachines:
                self.append_sub_meter(buf, "meter", "_dgmtr")

        if not self.bSwing and self.has_load():
            self.rescale_load(load_scale)
            if bWantZIP:
                self.apply_zip(Zcoeff, Icoeff, Pcoeff)

            va = complex(self.nomvln)
            vmagsq = complex(self.nomvln * self.nomvln)
            lead_or_lag = 1.0

            if self.bSecondary:
                if useHouses:
                    buf.append(f"object triplex_meter {{\n")
                    buf.append(f"  name \"{self.loadname}_ldmtr\";\n")
                    buf.append(f"  parent \"{self.name}\";\n")
                    buf.append(f"  phases {self.get_phases()};\n")
                    buf.append(f"  nominal_voltage {self.nomvln:.2f};\n")
                    buf.append("}\n")
                else:
                    buf.append(f"object triplex_load {{\n")
                    buf.append(f"  name \"{self.loadname}\";\n")
                    buf.append(f"  parent \"{self.name}\";\n")
                    buf.append(f"  phases {self.get_phases()};\n")
                    buf.append(f"  nominal_voltage {self.nomvln:.2f};\n")
                    base1 = complex(self.pa_z + self.pa_i + self.pa_p, self.qa_z + self.qa_i + self.qa_p)
                    base2 = complex(self.pb_z + self.pb_i + self.pb_p, self.qb_z + self.qb_i + self.qb_p)
                    b12 = False
                    # TODO: Need to fix the complex math
                    if abs(base1) > 0.0 and abs(base2) == 0.0:
                        b12 = True

                    if self.loadname in separateLoads:
                        if b12:
                            buf.append("  constant_power_12 0.0+0.0j;\n")
                        else:
                            buf.append("  constant_power_1 0.0+0.0j;\n")
                            buf.append("  constant_power_2 0.0+0.0j;\n")
                    else:
                        if bWantSched:
                            if b12:
                                buf.append(f"  base_power_12 {fSched}.value*{abs(base1):.2f};\n")
                            else:
                                buf.append(f"  base_power_1 {fSched}.value*{abs(base1):.2f};\n")
                                buf.append(f"  base_power_2 {fSched}.value*{abs(base2):.2f};\n")
                        else:
                            if b12:
                                buf.append(f"  base_power_12 {abs(base1):.2f};\n")
                            else:
                                buf.append(f"  base_power_1 {abs(base1):.2f};\n")
                                buf.append(f"  base_power_2 {abs(base2):.2f};\n")

                        if self.pa_p != 0.0:
                            base = complex(self.pa_p, self.qa_p)
                            if self.qa_p >= 0.0:
                                lead_or_lag = 1.0
                            else:
                                lead_or_lag = -1.0
                            if b12:
                                buf.append(f"  power_pf_12 {lead_or_lag * self.pa_p / abs(base):.2f};\n")
                                buf.append(f"  power_fraction_12 {self.pa_p / base1.real:.2f};\n")
                            else:
                                buf.append(f"  power_pf_1 {lead_or_lag * self.pa_p / abs(base):.2f};\n")
                                buf.append(f"  power_fraction_1 {self.pa_p / base1.real:.2f};\n")

                        if self.pb_p != 0.0:
                            base = complex(self.pb_p, self.qb_p)
                            if self.qb_p >= 0.0:
                                lead_or_lag = 1.0
                            else:
                                lead_or_lag = -1.0
                            buf.append(f"  power_pf_2 {lead_or_lag * self.pb_p / abs(base):.2f};\n")
                            buf.append(f"  power_fraction_2 {self.pb_p / base2.real:.2f};\n")

                        if self.pa_i != 0.0:
                            base = complex(self.pa_i, self.qa_i)
                            if self.qa_i >= 0.0:
                                lead_or_lag = 1.0
                            else:
                                lead_or_lag = -1.0
                            if b12:
                                buf.append(f"  current_pf_12 {lead_or_lag * self.pa_i / abs(base):.2f};\n")
                                buf.append(f"  current_fraction_12 {self.pa_i / base1.real:.2f};\n")
                            else:
                                buf.append(f"  current_pf_1 {lead_or_lag * self.pa_i / abs(base):.2f};\n")
                                buf.append(f"  current_fraction_1 {self.pa_i / base1.real:.2f};\n")

                        if self.pb_i != 0.0:
                            base = complex(self.pb_i, self.qb_i)
                            if self.qb_i >= 0.0:
                                lead_or_lag = 1.0
                            else:
                                lead_or_lag = -1.0
                            buf.append(f"  current_pf_2 {lead_or_lag * self.pb_i / abs(base):.2f};\n")
                            buf.append(f"  current_fraction_2 {self.pb_i / base2.real:.2f};\n")

                        if self.pa_z != 0.0:
                            base = complex(self.pa_z, self.qa_z)
                            if self.qa_z >= 0.0:
                                lead_or_lag = 1.0
                            else:
                                lead_or_lag = -1.0
                            if b12:
                                buf.append(f"  impedance_pf_12 {lead_or_lag * self.pa_z / abs(base):.2f};\n")
                                buf.append(f"  impedance_fraction_12 {self.pa_z / base1.real:.2f};\n")
                            else:
                                buf.append(f"  impedance_pf_1 {lead_or_lag * self.pa_z / abs(base):.2f};\n")
                                buf.append(f"  impedance_fraction_1 {self.pa_z / base1.real:.2f};\n")

                        if self.pb_z != 0.0:
                            base = complex(self.pb_z, self.qb_z)
                            if self.qb_z >= 0.0:
                                lead_or_lag = 1.0
                            else:
                                lead_or_lag = -1.0
                            buf.append(f"  impedance_pf_2 {lead_or_lag * self.pb_z / abs(base):.2f};\n")
                            buf.append(f"  impedance_fraction_2 {self.pb_z / base2.real:.2f};\n")
                    buf.append("\n")
            else:
                buf.append(f"object load {{\n")
                buf.append(f"  name \"{self.loadname}\";\n")
                buf.append(f"  parent \"{self.name}\";\n")
                buf.append(f"  phases {self.get_phases()};\n")
                buf.append(f"  nominal_voltage {self.nomvln:.2f};\n")
                if self.loadname in separateLoads or not bWantSched:
                    if self.pa_p != 0.0 or self.qa_p != 0.0:
                        buf.append(f"  constant_power_A {self.c_format(complex(self.pa_p, self.qa_p))};\n")
                    if self.pb_p != 0.0 or self.qb_p != 0.0:
                        buf.append(f"  constant_power_B {self.c_format(complex(self.pb_p, self.qb_p))};\n")
                    if self.pc_p != 0.0 or self.qc_p != 0.0:
                        buf.append(f"  constant_power_C {self.c_format(complex(self.pc_p, self.qc_p))};\n")
                    if self.pa_z != 0.0 or self.qa_z != 0.0:
                        s = complex(self.pa_z, self.qa_z)
                        z = vmagsq / s.conjugate()
                        buf.append(f"  constant_impedance_A {self.c_format(z)};\n")
                    if self.pb_z != 0.0 or self.qb_z != 0.0:
                        s = complex(self.pb_z, self.qb_z)
                        z = vmagsq / s.conjugate()
                        buf.append(f"  constant_impedance_B {self.c_format(z)};\n")
                    if self.pc_z != 0.0 or self.qc_z != 0.0:
                        s = complex(self.pc_z, self.qc_z)
                        z = vmagsq / s.conjugate()
                        buf.append(f"  constant_impedance_C {self.c_format(z)};\n")
                    if self.pa_i != 0.0 or self.qa_i != 0.0:
                        s = complex(self.pa_i, self.qa_i)
                        amps = s / va
                        buf.append(f"  constant_current_A {self.c_format(amps.conjugate())};\n")
                    if self.pb_i != 0.0 or self.qb_i != 0.0:
                        s = complex(self.pb_i, self.qb_i)
                        amps = s / (va * self.neg120)
                        buf.append(f"  constant_current_B {self.c_format(amps.conjugate())};\n")
                    if self.pc_i != 0.0 or self.qc_i != 0.0:
                        s = complex(self.pc_i, self.qc_i)
                        amps = s / (va * self.pos120)
                        buf.append(f"  constant_current_C {self.c_format(amps.conjugate())};\n")
                else:
                    baseA = complex(self.pa_p + self.pa_i + self.pa_z, self.qa_p + self.qa_i + self.qa_z)
                    baseB = complex(self.pb_p + self.pb_i + self.pb_z, self.qb_p + self.qb_i + self.qb_z)
                    baseC = complex(self.pc_p + self.pc_i + self.pc_z, self.qc_p + self.qc_i + self.qc_z)
                    if abs(baseA) != 0.0:
                        buf.append(f"  base_power_A {fSched}.value*{abs(baseA):.2f};\n")
                    if abs(baseB) != 0.0:
                        buf.append(f"  base_power_B {fSched}.value*{abs(baseB):.2f};\n")
                    if abs(baseC) != 0.0:
                        buf.append(f"  base_power_C {fSched}.value*{abs(baseC):.2f};\n")
                    if self.pa_p != 0.0 or self.qa_p != 0.0:
                        constPowerA = complex(self.pa_p, self.qa_p)
                        if self.qa_p >= 0.0:
                            lead_or_lag = 1.0
                        else:
                            lead_or_lag = -1.0
                        buf.append(f"  power_pf_A {lead_or_lag * self.pa_p / abs(constPowerA):.2f};\n")
                        buf.append(f"  power_fraction_A {self.pa_p / abs(baseA):.2f};\n")
                    if self.pb_p != 0.0 or self.qb_p != 0.0:
                        constPowerB = complex(self.pb_p, self.qb_p)
                        if self.qb_p >= 0.0:
                            lead_or_lag = 1.0
                        else:
                            lead_or_lag = -1.0
                        buf.append(f"  power_pf_B {lead_or_lag * self.pb_p / abs(constPowerB):.2f};\n")
                        buf.append(f"  power_fraction_B {self.pb_p / abs(baseB):.2f};\n")
                    if self.pc_p != 0.0 or self.qc_p != 0.0:
                        constPowerC = complex(self.pc_p, self.qc_p)
                        if self.qc_p >= 0.0:
                            lead_or_lag = 1.0
                        else:
                            lead_or_lag = -1.0
                        buf.append(f"  power_pf_C {lead_or_lag * self.pc_p / abs(constPowerC):.2f};\n")
                        buf.append(f"  power_fraction_C {self.pc_p / abs(baseC):.2f};\n")
                    if self.pa_z != 0.0 or self.qa_z != 0.0:
                        constImpedanceA = complex(self.pa_z, self.qa_z)
                        if self.qa_z >= 0.0:
                            lead_or_lag = 1.0
                        else:
                            lead_or_lag = -1.0
                        buf.append(f"  impedance_pf_A {lead_or_lag * self.pa_z / abs(constImpedanceA):.2f};\n")
                        buf.append(f"  impedance_fraction_A {self.pa_z / abs(baseA):.2f};\n")
                    if self.pb_z != 0.0 or self.qb_z != 0.0:
                        constImpedanceB = complex(self.pb_z, self.qb_z)
                        if self.qb_z >= 0.0:
                            lead_or_lag = 1.0
                        else:
                            lead_or_lag = -1.0
                        buf.append(f"  impedance_pf_B {lead_or_lag * self.pb_z / abs(constImpedanceB):.2f};\n")
                        buf.append(f"  impedance_fraction_B {self.pb_z / abs(baseB):.2f};\n")
                    if self.pc_z != 0.0 or self.qc_z != 0.0:
                        constImpedanceC = complex(self.pc_z, self.qc_z)
                        if self.qc_z >= 0.0:
                            lead_or_lag = 1.0
                        else:
                            lead_or_lag = -1.0
                        buf.append(f"  impedance_pf_C {lead_or_lag * self.pc_z / abs(constImpedanceC):.2f};\n")
                        buf.append(f"  impedance_fraction_C {self.pc_z / abs(baseC):.2f};\n")
                    if self.pa_i != 0.0 or self.qa_i != 0.0:
                        constCurrentA = complex(self.pa_i, self.qa_i)
                        if self.qa_i >= 0.0:
                            lead_or_lag = 1.0
                        else:
                            lead_or_lag = -1.0
                        buf.append(f"  current_pf_A {lead_or_lag * self.pa_i / abs(constCurrentA):.2f};\n")
                        buf.append(f"  current_fraction_A {self.pa_i / abs(baseA):.2f};\n")
                    if self.pb_i != 0.0 or self.qb_i != 0.0:
                        constCurrentB = complex(self.pb_i, self.qb_i)
                        if self.qb_i >= 0.0:
                            lead_or_lag = 1.0
                        else:
                            lead_or_lag = -1.0
                        buf.append(f"  current_pf_B {lead_or_lag * self.pb_i / abs(constCurrentB):.2f};\n")
                        buf.append(f"  current_fraction_B {self.pb_i / abs(baseB):.2f};\n")
                    if self.pc_i != 0.0 or self.qc_i != 0.0:
                        constCurrentC = complex(self.pc_i, self.qc_i)
                        if self.qc_i >= 0.0:
                            lead_or_lag = 1.0
                        else:
                            lead_or_lag = -1.0
                        buf.append(f"  current_pf_C {lead_or_lag * self.pc_i / abs(constCurrentC):.2f};\n")
                        buf.append(f"  current_fraction_C {self.pc_i / abs(baseC):.2f};\n")
                buf.append("}\n")
        return '\n'.join(buf)
