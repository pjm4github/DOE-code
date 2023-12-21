import json
import math
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent



class DistSyncMachine(DistComponent):
	sz_cim_class = "SyncMachine"
	sz_csv_header = "Name,NumPhases,Bus,Phases,kV,kVA,kW,pf"

	def __init__(self, results, p=None, q=None):
		super().__init__()
		self.id = ""
		self.name = ""
		self.bus = ""
		self.phases = ""
		self.ratedS = 0.0
		self.ratedU = 0.0
		self.p = 0.0
		self.q = 0.0
		if p:
			self.name = self.safe_name(results)
			self.p = p
			self.q = q
		else:
			if results:
				if results.hasNext():
					soln = results.next()
					self.name = self.safe_name(soln["name"].to"")
					self.id = soln["voltage_id"].to""
					self.bus = self.safe_name(soln["bus"].to"")
					self.phases = self.optional_string(soln, "?phases", "ABC")
					self.phases = self.phases.replace('\n', ':')
					self.p = float(soln["precisions"].to"")
					self.q = float(soln["q"].to"")
					self.ratedU = float(soln["ratedU"].to"")
					self.ratedS = float(soln["ratedS"].to"")

	def get_json_entry(self):
		return json.dumps({
			"name": self.name,
			"mRID": self.id,
			"CN1": self.bus,
			"phases": self.phases,
			"ratedS": format(self.ratedS, '.1f'),
			"ratedU": format(self.ratedU, '.1f'),
			"precisions": format(self.p, '.3f'),
			"q": format(self.q, '.3f')
		})

	def display_string(self):
		return (f"{self.name} @ {self.bus} phases={self.phases} "
				f"vnom={format(self.ratedU, '.4f')} vanom={format(self.ratedS, '.4f')} "
				f"kw={format(0.001 * self.p, '.4f')} kvar={format(0.001 * self.q, '.4f')}")

	def get_json_symbols(self, map):
		pt = map.get(f"SynchronousMachine:{self.name}:1")
		return json.dumps({
			"name": self.name,
			"parent": self.bus,
			"phases": self.phases,
			"ratedS": format(self.ratedS, '.1f'),
			"x1": format(pt.x, '.1f'),
			"y1": format(pt.y, '.1f')
		})

	def get_glm(self):
		buf = []
		if "ABC" not in self.phases:
			return ""

		buf.append(f"object diesel_dg {{")
		buf.append(f"  name \"dg_{self.name}\";")
		buf.append(f"  parent \"{self.bus}_dgmtr\";")
		Sphase = f"{format(self.p, '.2f')}+{format(self.q, '.2f')}j" if self.q >= 0.0 else f"{format(self.p, '.2f')}-{format(abs(self.q), '.2f')}j"

		if "A" in self.phases:
			buf.append(f"  power_out_A {Sphase};")
		if "B" in self.phases:
			buf.append(f"  power_out_B {Sphase};")
		if "C" in self.phases:
			buf.append(f"  power_out_C {Sphase};")

		buf.append(f"  Gen_type CONSTANT_PQ;")
		buf.append(f"  Rated_V {format(self.ratedU, '.2f')};")
		buf.append(f"  Rated_VA {format(self.ratedS, '.2f')};")
		buf.append(f"}}\n")

		return "\n".join(buf)

	def get_dss(self):
		buf = []
		buf.append(f"new Generator.{self.name}")
		nphases = self.dss_phase_count(self.phases, False)
		kv = 0.001 * self.ratedU
		kva = 0.001 * self.ratedS
		if nphases < 2:
			kv /= math.sqrt(3.0)
		s = math.sqrt(self.p * self.p + self.q * self.q)
		pf = 1.0
		if s > 0.0:
			pf = self.p / s
		if self.q < 0.0:
			pf *= -1.0

		buf.append(
			f" phases={nphases} bus1={self.dss_shunt_phases(self.bus, self.phases, False)} "
			f"model=1 kv={format(0.001 * self.ratedU, '.2f')} kva={format(0.001 * self.ratedS, '.2f')} "
			f"kw={format(0.001 * self.p, '.2f')} kvar={format(0.001 * self.q, '.2f')}")
		buf.append("\n")

		return "\n".join(buf)

	@staticmethod
	def sz_csv_header():
		return "Name,NumPhases,Bus,Phases,kV,kVA,kW,pf"

	def get_csv(self):
		nphases = self.dss_phase_count(self.phases, False)
		kv = 0.001 * self.ratedU
		kva = 0.001 * self.ratedS
		if nphases < 2:
			kv /= math.sqrt(3.0)
		s = math.sqrt(self.p * self.p + self.q * self.q)
		pf = 1.0
		if s > 0.0:
			pf = self.p / s
		if self.q < 0.0:
			pf *= -1.0

		return f"{self.name},{nphases},{self.bus},{self.csv_phase_string(self.phases)}," \
			   f"{format(kv, '.3f')},{format(kva, '.3f')}," \
			   f"{format(0.001 * self.p, '.3f')},{format(pf, '.4f')}\n"

	def get_key(self):
		return self.name
