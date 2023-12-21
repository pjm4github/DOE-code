from math import sqrt
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent



class DistLoad(DistComponent):
    sz_cim_class = "Load"
    sz_csv_header = "Name,NumPhases,Bus,Phases,kV,Model,Connection,kW,pf"

    def __init__(self, results):
        super().__init__()
        self.nwires = 0
        self.wire_phases = []
        self.wire_names = []
        self.wire_classes = []
        self.wire_type = ""

        if results.hasNext():
            soln = results.next()
            self.name = self.safe_name(soln.get("?name").to"")
            self.id = soln.get("?voltage_id").to""
            self.bus = self.safe_name(soln.get("?bus").to"")
            self.basev = float(soln.get("?basev").to"")
            self.phases = self.optional_string(soln, "?phases", "ABC").replace('\n', ':')
            self.conn = soln.get("?conn").to""
            self.p = 0.001 * float(soln.get("?precisions").to"")
            self.q = 0.001 * float(soln.get("?q").to"")
            self.pz = float(soln.get("?pz").to"")
            self.qz = float(soln.get("?qz").to"")
            self.pi = float(soln.get("?pi").to"")
            self.qi = float(soln.get("?qi").to"")
            self.pp = float(soln.get("?pp").to"")
            self.qp = float(soln.get("?qp").to"")
            self.pe = float(soln.get("?pe").to"")
            self.qe = float(soln.get("?qe").to"")
            self.cnt = self.optional_int(soln, "?cnt", 1)

        self.dss_load_model = 8
        self.bDelta = False

    def display_string(self):
        buf = [f"{self.name} @ {self.bus} basev={self.basev:.4f} phases={self.phases} conn={self.conn}",
               f" kw={self.p:.4f} kvar={self.q:.4f}", f" Real ZIP={self.pz:.4f}:{self.pi:.4f}:{self.pp:.4f}",
               f" Reactive ZIP={self.qz:.4f}:{self.qi:.4f}:{self.qp:.4f}", f" Exponents={self.pe:.4f}:{self.qe:.4f}"]
        return " ".join(buf)

    def set_dss_load_model(self):
        if self.pe == 1 and self.qe == 2:
            self.dss_load_model = 4
            return
        total_pz = self.pz + self.pi + self.pp
        self.pz = self.pz / total_pz
        self.pi = self.pi / total_pz
        self.pp = self.pp / total_pz
        total_qz = self.qz + self.qi + self.qp
        self.qz = self.qz / total_qz
        self.qi = self.qi / total_qz
        self.qp = self.qp / total_qz

        if self.pz >= 0.999999 and self.qz >= 0.999999:
            self.dss_load_model = 2
        elif self.pi >= 0.999999 and self.qi >= 0.999999:
            self.dss_load_model = 5
        elif self.pp >= 0.999999 and self.qp >= 0.999999:
            self.dss_load_model = 1
        else:
            self.dss_load_model = 8

        if self.conn == "D":
            self.bDelta = True
        else:
            self.bDelta = False

    def get_zipv(self):
        return f"[{self.pz:.4f}, {self.pi:.4f}, {self.pp:.4f}, " \
               f"{self.qz:.4f}, {self.qi:.4f}, {self.pp:.4f}, 0.8]"

    def get_dss(self):
        buf = [f"new Load.{self.name}"]
        self.set_dss_load_model()
        nphases = self.dss_phase_count(self.phases, self.bDelta)
        kv = 0.001 * self.basev

        if nphases < 2 and not self.bDelta:
            kv /= sqrt(3.0)

        buf.append(f" phases={nphases} bus1={self.dss_shunt_phases(self.bus, self.phases, self.bDelta)}")
        buf.append(f" conn={self.dss_conn(self.bDelta)} kw={self.p:.3f} kvar={self.q:.3f}")
        buf.append(f" numcust=1 kv={kv:.3f} model={self.dss_load_model}")

        if self.dss_load_model == 8:
            buf.append(f" zipv={self.get_zipv()}")

        return " ".join(buf)

    def get_key(self):
        return self.name

    def get_csv(self):
        self.set_dss_load_model()
        nphases = self.dss_phase_count(self.phases, self.bDelta)
        kv = 0.001 * self.basev
        if nphases < 2 and not self.bDelta:  # 2-phase wye load should be line-line for secondary?
            kv /= sqrt(3.0)
        s = sqrt(self.p * self.p + self.q * self.q)
        pf = 1.0

        if s > 0.0:
            pf = self.p / s

        if self.q < 0.0:
            pf *= -1.0

        self.wire_type = "TS" if self.bDelta else "CN" if self.bDelta else "OHD"

        wire_names = "\""
        for i in range(self.nwires):
            wire_names += f"{self.wire_names[i]}"
            if i < self.nwires - 1:
                wire_names += ","
        wire_names += "\""

        buf = f"{self.name},{nphases},{self.bus},{self.csv_phase_string(self.phases)}," \
              f"{kv:.3f},{self.dss_load_model},{self.dss_conn(self.bDelta)}," \
              f"{self.p:.3f},{pf:.4f}\n"

        return buf

    @staticmethod
    def csv_header():
        return "Name,NumPhases,Bus,Phases,kV,Model,Connection,kW,pf"

    def get_json_entry(self):
        return f'{{"name":"{self.name}", "mRID":"{self.id}", "phases":"{self.phases}"}}'
