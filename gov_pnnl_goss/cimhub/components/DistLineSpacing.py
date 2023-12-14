import math
import json

from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent


class DistLineSpacing(DistComponent):
    sz_cim_class = "LineSpacing"
    sz_csv_header = "Name,Ncond,Nphase,Units,Xvals,Yvals"

    def __init__(self, results, mapper):
        super().__init__()
        self.name = ""
        self.id = ""
        self.xarray = []
        self.yarray = []
        self.usage = "distribution"
        self.nwires = 0
        self.cable = False
        self.b_sep = 0.0
        self.b_cnt = 0
        self.perms = set()
        self.bTriplex = False

        for soln in results:
            self.name = self.safe_name(soln.get("?name", ""))
            self.id = soln.get("?voltage_id", "")
            self.cable = self.optional_boolean(soln, "?cable", False)
            self.usage = self.optional_string(soln, "?usage", "distribution")
            self.b_sep = self.optional_double(soln, "?bundle_sep", 0.0)
            self.b_cnt = self.optional_int(soln, "?bundle_count", 0)
            self.nwires = mapper.get(self.name, 0)
            self.xarray = [self.optional_double(soln, "?x", 0.0)]
            self.yarray = [self.optional_double(soln, "?y", 0.0)]

            for i in range(1, self.nwires):
                soln = results.next()
                self.xarray.append(self.optional_double(soln, "?x", 0.0))
                self.yarray.append(self.optional_double(soln, "?y", 0.0))

    def display_string(self):
        result = (
            f"{self.name} nwires={self.nwires} cable={self.cable} "
            f"usage={self.usage} b_cnt={self.b_cnt} b_sep={self.b_sep:.4f}"
        )
        for i in range(self.nwires):
            result += f"\n  x={self.xarray[i]:.4f} y={self.yarray[i]:.4f}"

        return result

    def mark_permutations_used(self, s):
        if "ABC" in s and self.nwires >= 3:
            self.perms.add("ABC")
        elif "ACB" in s and self.nwires >= 3:
            self.perms.add("ACB")
        elif "BAC" in s and self.nwires >= 3:
            self.perms.add("BAC")
        elif "BCA" in s and self.nwires >= 3:
            self.perms.add("BCA")
        elif "CAB" in s and self.nwires >= 3:
            self.perms.add("CAB")
        elif "CBA" in s and self.nwires >= 3:
            self.perms.add("CBA")
        elif "AB" in s and self.nwires >= 2:
            self.perms.add("AB")
        elif "BA" in s and self.nwires >= 2:
            self.perms.add("BA")
        elif "BC" in s and self.nwires >= 2:
            self.perms.add("BC")
        elif "CB" in s and self.nwires >= 2:
            self.perms.add("CB")
        elif "AC" in s and self.nwires >= 2:
            self.perms.add("AC")
        elif "CA" in s and self.nwires >= 2:
            self.perms.add("CA")
        elif "A" in s and self.nwires >= 1:
            self.perms.add("A")
        elif "B" in s and self.nwires >= 1:
            self.perms.add("B")
        elif "C" in s and self.nwires >= 1:
            self.perms.add("C")

    def wire_separation(self, i, j):
        dx = self.xarray[i] - self.xarray[j]
        dy = self.yarray[i] - self.yarray[j]
        return math.sqrt(dx * dx + dy * dy)

    def append_dss_permutation(self, buf, perm):
        nphases = len(perm)
        has_neutral = False
        if self.nwires > nphases:
            has_neutral = True

        buf.append(f"new LineSpacing.{self.name}_{perm} nconds={self.nwires} nphases={nphases} units=m\n")
        buf.append(f"~ x=[{', '.join([f'{self.xarray[i]:.4f}' for i in range(self.nwires)])}]\n")
        buf.append(f"~ h=[{', '.join([f'{self.yarray[i]:.4f}' for i in range(self.nwires)])}]\n")
        return '\n'.join(buf)

    def append_glm_permutation(self, buf, perm):
        nphases = len(perm)
        has_neutral = False
        if self.nwires > nphases:
            has_neutral = True
        if has_neutral:
            buf.append(f"object line_spacing {{\n  name \"spc_{self.name}_{perm}N\";\n")
        else:
            buf.append(f"object line_spacing {{\n  name \"spc_{self.name}_{perm}\";\n")
        idxA = 0
        idxB = 1
        idxC = 2
        if nphases == 1:
            idxB = 0
            idxC = 0
        elif nphases == 2:
            if "AC" in perm:
                idxC = 1
            elif "BC" in perm:
                idxB = 0
                idxC = 1
        if "A" in perm:
            if "B" in perm:
                buf.append(f"  distance_AB {self.wire_separation(idxA, idxB):.4f};\n")
            if "C" in perm:
                buf.append(f"  distance_AC {self.wire_separation(idxA, idxC):.4f};\n")
            if has_neutral:
                buf.append(f"  distance_AN {self.wire_separation(idxA, self.nwires - 1):.4f};\n")
            buf.append(f"  distance_AE {self.yarray[idxA]:.4f};\n")
        if "B" in perm:
            if "C" in perm:
                buf.append(f"  distance_BC {self.wire_separation(idxB, idxC):.4f};\n")
            if has_neutral:
                buf.append(f"  distance_BN {self.wire_separation(idxB, self.nwires - 1):.4f};\n")
            buf.append(f"  distance_BE {self.yarray[idxB]:.4f};\n")
        if "C" in perm:
            if has_neutral:
                buf.append(f"  distance_CN {self.wire_separation(idxC, self.nwires - 1):.4f};\n")
            buf.append(f"  distance_CE {self.yarray[idxC]:.4f};\n")
        if has_neutral:
            buf.append(f"  distance_NE {self.yarray[self.nwires - 1]:.4f};\n")
        buf.append("}\n")
        return '\n'.join(buf)

    def get_glm(self):
        buf = []
        for phs in self.perms:
            buf.append(self.append_glm_permutation(buf, phs))

        return "\n".join(buf)

    # def append_csv_permutation(self, buf, perm):
    #     nphases = len(perm)
    #     has_neutral = False
    #     if self.nwires > nphases:
    #         has_neutral = True
    #     x_values = ', '.join([functions'{self.xarray[i]:.4f}' for i in range(self.nwires)])
    #     y_values = ', '.join([functions'{self.yarray[i]:.4f}' for i in range(self.nwires)])
    #     buf.append(functions"{self.name}_{perm},{self.nwires},{nphases},multiplicities,[{x_values}],[{y_values}]")
    #     return buf

    def get_csv(self):
        csv_data = []
        for perm in self.perms:
            # csv_data = self.append_csv_permutation(csv_data, perm)
            nphases = len(perm)
            has_neutral = False
            if self.nwires > nphases:
                has_neutral = True
            x_values = ', '.join([f'{self.xarray[i]:.4f}' for i in range(self.nwires)])
            y_values = ', '.join([f'{self.yarray[i]:.4f}' for i in range(self.nwires)])
            csv_data.append(f"{self.name}_{perm},{self.nwires},{nphases},m,[{x_values}],[{y_values}]")
        return '\n'.join(csv_data)

    def get_dss(self):
        buf = []
        for perm in self.perms:
            self.append_dss_permutation(buf, perm)
        return '\n'.join(buf)

    def get_key(self):
        return self.name

    def get_json_entry(self):
        return json.dumps({"name": self.name, "mRID": self.id})
