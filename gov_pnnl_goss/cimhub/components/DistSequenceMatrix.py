import json
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent



class DistSequenceMatrix(DistComponent):
    sz_cim_class = "SequenceMatrix"
    sz_csv_header = "Name,NumPhases,Units,r1,x1,c1[nF],r0,x0,c0[nF]"

    def __init__(self, results):
        super().__init__()
        self.name = ""
        self.id = ""
        self.r1 = 0.0
        self.x1 = 0.0
        self.b1 = 0.0
        self.r0 = 0.0
        self.x0 = 0.0
        self.b0 = 0.0

        self.seqZs = ""
        self.seqZm = ""
        self.seqCs = ""
        self.seqCm = ""

        if results:
            for soln in results:
                self.name = self.safe_name(soln["name"].toString())
                self.id = soln["voltage_id"].toString()
                self.r1 = float(soln["r1"].toString())
                self.x1 = float(soln["x1"].toString())
                self.b1 = float(soln["b1"].toString())
                self.r0 = float(soln["r0"].toString())
                self.x0 = float(soln["x0"].toString())
                self.b0 = float(soln["b0"].toString())

                self.seqZs = self.c_format(complex(self.g_m_per_mile * (self.r0 + 2.0 * self.r1) / 3.0,
                                                   self.g_m_per_mile * (self.x0 + 2.0 * self.x1) / 3.0))
                self.seqZm = self.c_format(complex(self.g_m_per_mile * (self.r0 - self.r1) / 3.0,
                                                   self.g_m_per_mile * (self.x0 - self.x1) / 3.0))
                self.seqCs = f"{1.0e9 * self.g_m_per_mile * (self.b0 + 2.0 * self.b1) / 3.0 / self.g_omega:.4f}"
                self.seqCm = f"{1.0e9 * self.g_m_per_mile * (self.b0 - self.b1) / 3.0 / self.g_omega:.4f}"

    def get_json_entry(self):
        return json.dumps({"name": self.name, "mRID": self.id})

    def display_string(self):
        return f"{self.name} r1={self.r1:.4f} x1={self.x1:.4f} " \
               f"b1={self.b1:.4f} r0={self.r0:.4f} x0={self.x0:.4f} b0={self.b0:.4f}"

    def append_permutation(self, buf, perm, perm_idx):
        cnt = len(perm_idx)

        buf.append("object line_configuration {")
        buf.append(f"  name \"lcon_{self.name}_{perm}\";")
        for i in range(cnt):
            for j in range(cnt):
                indices = str(perm_idx[i]) + str(perm_idx[j]) + " "
                if i == j:
                    buf.append(f"  z{indices}{self.seqZs};")
                    buf.append(f"  c{indices}{self.seqCs};")
                else:
                    buf.append(f"  z{indices}{self.seqZm};")
                    buf.append(f"  c{indices}{self.seqCm};")
        buf.append("}")

    # TODO: implement glmUsed pattern from DistPhaseMatrix here; for now always writing the ABC permutation
    def get_glm(self):
        buf = []
        self.append_permutation(buf, "ABC", [1, 2, 3])
        return "\n".join(buf)

    def get_dss(self):
        buf = [f"new Linecode.{self.name} nphases=3 units=mi",
               f" r1={self.g_m_per_mile * self.r1:.6f}",
               f" x1={self.g_m_per_mile * self.x1:.6f}",
               f" c1={1.0e9 * self.g_m_per_mile * self.b1 / self.g_omega:.6f}",
               f" r0={self.g_m_per_mile * self.r0:.6f}",
               f' x0={self.g_m_per_mile * self.x0:.6f}',
               f" c0={1.0e9 * self.g_m_per_mile * self.b0 / self.g_omega:.6f}\n"]
        return "".join(buf)

    @staticmethod
    def get_csv_header():
        return "Name,NumPhases,Units,r1,x1,c1[nF],r0,x0,c0[nF]"

    def csv_header(self):
        return self.sz_csv_header

    def get_csv(self):
        c = f"{self.name},3,mi,{self.g_m_per_mile * self.r1:.6f}," \
            f"{self.g_m_per_mile * self.x1:.6f}," \
            f"{1.0e9 * self.g_m_per_mile * self.b1 / self.g_omega:.6f}," \
            f"{self.g_m_per_mile * self.r0:.6f}," \
            f"{self.g_m_per_mile * self.x0:.6f}," \
            f"{1.0e9 * self.g_m_per_mile * self.b0 / self.g_omega:.6f}\n"
        return c

    def get_key(self):
        return self.name
