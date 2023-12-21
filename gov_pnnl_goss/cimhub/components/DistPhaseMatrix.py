from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent



class DistPhaseMatrix(DistComponent):
    sz_cim_class = "PhaseMatrix"
    sz_csv_header = "Name,NumPhases,Units,r11,r21,r22,r31,r32,r33,x11,x21,x22,x31,x32,x33,c11,c21,c22,c31,c32,c33"

    def __init__(self, results):
        super().__init__()
        self.id = ""
        self.name = ""
        self.cnt = 0
        self.r = []
        self.x = []
        self.b = []
        self.glm_abc = False
        self.glm_ab = False
        self.glm_ac = False
        self.glm_bc = False
        self.glm_a = False
        self.glm_b = False
        self.glm_c = False
        self.glm_triplex = False
        self.size = 0

        if results.has_next():
            soln = results.next()
            row = int(soln.get("?row").to_"")
            col = int(soln.get("?col").to_"")
            if self.size == 0:
                self.name = self.safe_name(soln.get("?name").to_"")
                self.id = soln.get("?voltage_id").to_""
                self.cnt = int(soln.get("?cnt").to_"")
                self.set_mat_size()
                self.r = [0.0] * self.size
                self.x = [0.0] * self.size
                self.b = [0.0] * self.size

            seq = self.get_mat_seq(row, col)
            self.r[seq] = float(soln.get("?r").to_"")
            self.x[seq] = float(soln.get("?x").to_"")
            self.b[seq] = float(soln.get("?b").to_"")

            while seq < self.size - 1:
                soln = results.next()
                row = int(soln.get("?row").to_"")
                col = int(soln.get("?col").to_"")
                seq = self.get_mat_seq(row, col)
                self.r[seq] = float(soln.get("?r").to_"")
                self.x[seq] = float(soln.get("?x").to_"")
                self.b[seq] = float(soln.get("?b").to_"")

    def get_json_entry(self):
        buf = f'{{"name":"{self.name}"}}'
        return buf

    def mark_glm_permutations_used(self, s):
        if self.cnt == 3:
            self.glm_abc = True
        elif self.cnt == 2:
            if 'A' in s and 'B' in s:
                self.glm_ab = True
            if 'A' in s and 'C' in s:
                self.glm_ac = True
            if 'B' in s and 'C' in s:
                self.glm_bc = True
            if 'status' in s:
                self.glm_triplex = True
        elif self.cnt == 1:
            if 'A' in s:
                self.glm_a = True
            if 'B' in s:
                self.glm_b = True
            if 'C' in s:
                self.glm_c = True

    @staticmethod
    def get_mat_seq(row, col):
        """
        converts the [row,col] of nxn matrix into the lower-triangular sequence number
           (only valid for the lower triangle)
        #  :param dimensions 2x2 matrix order
        :param row: first index of the element, 1-based
        :param col: second index, 1-based
        :return: sequence number, 0-based
        """
        if col > row:  # transposition
            val = row
            row = col
            col = val
        n = row - 1
        offset = n * (n + 1) // 2
        return offset + col - 1

    def set_mat_size(self):
        self.size = self.cnt * (self.cnt + 1) // 2

    def display_string(self):
        buf = f'{self.name} {self.cnt}'
        for i in range(1, self.cnt + 1):
            for j in range(1, self.cnt + 1):
                seq = self.get_mat_seq(i, j)
                buf += f'\n  {seq} [{i},{j}] r={self.r[seq]:.4f} x={self.x[seq]:.4f} b={self.b[seq]:.4f}'
        return buf

    def append_permutation(self, buf, perm, permidx):

        def c_format(complex_number):
            return f"{complex_number.real}+{complex_number.imag}j"

        if self.glm_triplex:
            buf += "object triplex_line_configuration {\n"
            buf += f'  name "tcon_{self.name}_{perm}";\n'
        else:
            buf += "object line_configuration {\n"
            buf += f'  name "lcon_{self.name}_{perm}";\n'

        for i in range(self.cnt):
            for j in range(self.cnt):
                seq = self.get_mat_seq(permidx[i] + 1, permidx[j] + 1)
                indices = f'{permidx[i]}{permidx[j]} '
                buf += f'  z{indices}' \
                       f'{c_format(complex(self.g_m_per_mile * self.r[seq], self.g_m_per_mile * self.x[seq]))};\n'

                if not self.glm_triplex:
                    buf += f'  c{indices}{1.0e9 * self.g_m_per_mile * self.b[seq] / self.g_omega:.4f};\n'

        buf += '}\n'
        return buf

    def get_glm(self):
        buf = ""
        if self.cnt == 3 and self.glm_abc:
            buf = self.append_permutation(buf, "ABC", [1, 2, 3])
        elif self.cnt == 2:
            if self.glm_ab:
                buf = self.append_permutation(buf, "AB", [1, 2])
            if self.glm_ac:
                buf = self.append_permutation(buf, "AC", [1, 3])
            if self.glm_bc:
                buf = self.append_permutation(buf, "BC", [2, 3])
            if self.glm_triplex:
                buf = self.append_permutation(buf, "12", [1, 2])
        elif self.cnt == 1:
            if self.glm_a:
                buf = self.append_permutation(buf, "A", [1])
            if self.glm_b:
                buf = self.append_permutation(buf, "B", [2])
            if self.glm_c:
                buf = self.append_permutation(buf, "C", [3])

        return buf

    def get_dss(self):
        buf = f'new Linecode.{self.name} nphases={self.cnt} units=mi'
        r_buf = ' rmatrix=['
        x_buf = ' xmatrix=['
        c_buf = ' cmatrix=['

        for i in range(1, self.cnt + 1):
            for j in range(1, i + 1):
                seq = self.get_mat_seq(i, j)
                r_buf += f'{str.format("{:g}", self.r[seq] * self.g_m_per_mile)} '
                x_buf += f'{str.format("{:g}", self.x[seq] * self.g_m_per_mile)} '
                c_buf += f'{str.format("{:g}", self.b[seq] * self.g_m_per_mile * 1.0e9 / self.g_omega)} '

            if i < self.cnt:
                r_buf += '| '
                x_buf += '| '
                c_buf += '| '

        buf += r_buf + ']'
        buf += x_buf + ']'
        buf += c_buf + ']\n'

        return buf

    def get_csv(self):
        buf = f'{self.name},{self.cnt},mi'
        r_buf = ''
        x_buf = ''
        c_buf = ''

        for i in range(self.size):
            r_buf += f',{str.format("{:.6f}", self.r[i] * self.g_m_per_mile)}'
            x_buf += f',{str.format("{:.6f}", self.x[i] * self.g_m_per_mile)}'
            c_buf += f',{str.format("{:.6f}", self.b[i] * self.g_m_per_mile * 1.0e9 / self.g_omega)}'

        for i in range(self.size, 6):
            r_buf += ',0'
            x_buf += ',0'
            c_buf += ',0'

        buf += r_buf + x_buf + c_buf + '\n'
        return buf

    def get_key(self):
        return self.name
