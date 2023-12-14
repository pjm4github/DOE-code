from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistWire(DistComponent):
    sz_cim_class = "Wire"
    sz_csv_header = "Name,GMR,Radius,Rac,Rdc,NormAmps,Units"

    def __init__(self):
        super().__init__()
        self.name = None
        self.id = None
        self.rad = None
        self.gmr = None
        self.rdc = None
        self.r25 = None
        self.r50 = None
        self.r75 = None
        self.corerad = None
        self.amps = None
        self.insthick = None
        self.ins = None
        self.insmat = None

    def append_wire_display(self, buf):
        buf.append(f"{self.name} rad={self.rad:.6f} gmr={self.gmr:.6f} rdc={self.rdc:.6f}")
        buf.append(f" r25={self.r25:.6f} r50={self.r50:.6f} r75={self.r75:.6f}")
        buf.append(f" corerad={self.corerad:.6f} amps={self.amps:.1f}")
        buf.append(f" ins={str(self.ins)} insmat={self.insmat} insthick={self.insthick:.6f}")
        return "\n".join(buf)

    def append_dss_wire_attributes(self, buf):
        if self.gmr < 1.0e-6 or self.rad < 1.0e-6 or self.r25 < 1.0e-6 or self.rdc < 1.0e-6:
            buf.append(f"{self.name} gmr={self.gmr:.12f} radius={self.rad:.12f} rac={self.r25:.12f}")
            buf.append(f" rdc={self.rdc:.12f} normamps={self.amps:.1f} Runits=m Radunits=m gmrunits=m")
        else:
            buf.append(f"{self.name} gmr={self.gmr:.6f} radius={self.rad:.6f} rac={self.r25:.6f}")
            buf.append(f" rdc={self.rdc:.6f} normamps={self.amps:.1f} Runits=m Radunits=m gmrunits=m")
        return "\n".join(buf)

    def csv_header(self):
        return self.sz_csv_header

    def append_csv_wire_attributes(self, buf):
        if self.gmr < 1.0e-6 or self.rad < 1.0e-6 or self.r25 < 1.0e-6 or self.rdc < 1.0e-6:
            buf.append(f"{self.name},{self.gmr:.12f},{self.rad:.12f},{self.r25:.12f}")
            buf.append(f",{self.rdc:.12f},{self.amps:.1f},m")
        else:
            buf.append(f"{self.name},{self.gmr:.6f},{self.rad:.6f},{self.r25:.6f}")
            buf.append(f",{self.rdc:.6f},{self.amps:.1f},m")
        return "\n".join(buf)

    def append_glm_wire_attributes(self, buf):
        if self.amps > 0.0:
            buf.append(f"  rating.summer.continuous {self.amps:.2f};")
            buf.append(f"  rating.summer.emergency {self.amps:.2f};")
            buf.append(f"  rating.winter.continuous {self.amps:.2f};")
            buf.append(f"  rating.winter.emergency {self.amps:.2f};")
        return "\n".join(buf)

    def get_json_entry(self):
        buf = []
        buf.append(f"{{\"name\":\"{self.name}\"")
        buf.append(f",\"mRID\":\"{self.id}\"")
        buf.append(f",\"rad\":{self.rad:.6f}")
        buf.append(f",\"gmr\":{self.gmr:.6f}")
        buf.append(f",\"rdc\":{self.rdc:.6f}")
        buf.append(f",\"r25\":{self.r25:.6f}")
        buf.append(f",\"r50\":{self.r50:.6f}")
        buf.append(f",\"r75\":{self.r75:.6f}")
        buf.append(f",\"corerad\":{self.corerad:.6f}")
        buf.append(f",\"amps\":{self.amps:.1f}")
        buf.append(f",\"insthick\":{self.insthick:.6f}")
        buf.append(f",\"ins\":{str(self.ins)}")
        buf.append(f",\"insmat\":\"{self.insmat}\"")
        buf.append("}")
        return "\n".join(buf)

    def get_dss(self):
        buf = []
        buf.append(f"new Wire.{self.name}")
        buf.append(f" rad={self.rad:.6f} gmrac={self.gmr / self.rdc:.6f} resist={self.r25:.6f}")
        buf.append(f" runits=m radunits=m rdc={self.rdc:.6f}")
        buf.append(f" normamps={self.amps:.1f}")
        if self.ins:
            buf.append(f" insgmrac=1000000.0")
        buf.append(" units=ft")
        return "\n".join(buf)

    def get_key(self):
        return self.name

    def get_csv(self):
        buf = [f"{self.name},{self.gmr:.6f},"
               f"{self.rad:.6f},{self.r25:.6f}",
               f",{self.rdc:.6f},{self.amps:.1f},m"]
        return "\n".join(buf)
