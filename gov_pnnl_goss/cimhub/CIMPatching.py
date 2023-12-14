import math


class CIMPatching:
    def __init__(self):
        self.sqrt3 = math.sqrt(3.0)

    def fix_loads(self, map_loads):
        for obj in map_loads.values():
            if obj.precisions < 0.001 and obj.q < 0.001:
                obj.precisions = 0.2  # kW

    def fix_short_circuit_tests(self, map_code_sc_tests, map_code_ratings):
        for obj in map_code_sc_tests.values():
            if obj.z[0] <= 0.0:
                rat = map_code_ratings.get(obj.tname)
                for i in range(obj.size):
                    fwdg = obj.fwdg[i]
                    twdg = obj.twdg[i]
                    vbase = rat.ratedU[fwdg - 1]
                    sbase = rat.ratedS[fwdg - 1]
                    zbase = vbase * vbase / sbase
                    if rat.r[0] <= 0.0:
                        rat.r[0] = 0.005 * zbase
                        if obj.size == 3:
                            rat.r[0] *= 2.0
                    if obj.size == 1:
                        obj.z[0] = 0.035 * zbase
                        obj.ll[0] = 0.005 * sbase
                    elif obj.size == 3:
                        if fwdg == 1:
                            obj.z[i] = 0.02 * 1.2 * zbase
                            obj.ll[i] = 0.01 * 1.5 * sbase
                        else:
                            obj.z[i] = 0.02 * 0.8 * zbase
                            obj.ll[i] = 0.01 * 2.0 * sbase
                    else:
                        print(f'*** Trying to patch the short-circuit tests on a transformer '
                              f'with more than 3 windings: {obj.tname}')

    def fix_transformer_kva(self, map_code_ratings):
        for obj in map_code_ratings.values():
            if "kVA" in obj.pname and obj.ratedS[0] < 1501.0:
                for i in range(obj.size):
                    obj.ratedS[i] *= 1000.0

    def fix_capacitors(self, map_capacitors):
        for obj in map_capacitors.values():
            obj.conn = "Y"
            obj.nomu *= self.sqrt3
            obj.set_derived_parameters()

    def fix_overhead_wires(self, map_wires):
        for obj in map_wires.values():
            if obj.name == "6A":
                obj.gmr = 0.0014097
            if obj.rad <= 0.0:
                if "2/0" in obj.name:
                    obj.amps = 255
                    obj.rad = 0.004775
                    obj.gmr = 0.00353568
                    obj.rdc = obj.r25 = obj.r50 = obj.r75 = 0.000433727
                elif "4/0" in obj.name:
                    obj.amps = 380
                    obj.rad = 0.0066294
                    obj.gmr = 0.00481584
                    obj.rdc = obj.r25 = obj.r50 = obj.r75 = 0.00027395
                elif "350" in obj.name:
                    obj.amps = 399
                    obj.rad = 0.008623
                    obj.gmr = 0.006523
                    obj.rdc = obj.r25 = obj.r50 = obj.r75 = 0.000185
                elif "2" in obj.name:
                    obj.amps = 240
                    obj.rad = 0.0037084
                    obj.gmr = 0.002691384
                    obj.rdc = obj.r25 = obj.r50 = obj.r75 = 0.000548049
                elif "4" in obj.name:
                    obj.amps = 170
                    obj.rad = 0.0025908
                    obj.gmr = 0.002020824
                    obj.rdc = obj.r25 = obj.r50 = obj.r75 = 0.000866813
                elif "6" in obj.name:
                    obj.amps = 105
                    obj.rad = 0.00233684
                    obj.gmr = 0.0014097  # CIM XML has 3 leading zeros for 6A
                    obj.rdc = obj.r25 = obj.r50 = obj.r75 = 0.002208005

    def fix_line_spacings(self, map_spacings):
        for obj in map_spacings.values():
            if obj.name == "SVC_OH_Wire_Spacing":
                obj.xarray[0] = 0.05
                obj.xarray[1] = 0.00
                obj.yarray[0] = obj.yarray[1] = 9.144
            elif obj.name == "UG_Wire_Spacing":
                obj.xarray[0] = -0.1651
                obj.xarray[1] = 0.00
                obj.xarray[2] = 0.1651
                obj.yarray[0] = obj.yarray[1] = obj.yarray[2] = 0.762

    def fix_lines_spacing_z(self, map_lines):
        for obj in map_lines.values():
            if obj.spacing == "OH_Wire_Spacing" and obj.phases == "ABC" and obj.nwires < 4:
                obj.nwires = 4
                wire_phase = obj.wire_phases[0]
                wire_name = obj.wire_names[0]
                wire_class = obj.wire_classes[0]
                print(f"Adding neutral to {obj.name}")
                obj.wire_phases = [wire_phase] * obj.nwires
                obj.wire_names = [wire_name] * obj.nwires
                obj.wire_classes = [wire_class] * obj.nwires
