import json
from collections import defaultdict
from gov_pnnl_goss.cimhub.components.DistCoordinates import DistCoordinates


class VoltageLimit:
    def __init__(self, voltage_id, bus, x, y, Blo, Alo, Ahi, Bhi):
        self.id = voltage_id
        self.bus = bus
        self.x = x
        self.y = y
        self.Alo = Alo
        self.Ahi = Ahi
        self.Blo = Blo
        self.Bhi = Bhi

class OperationalLimits:
    # Define constants from the original code
    szBUSEQ = """
    SELECT ?cnid ?eqtype ?eqname ?tseq WHERE {
     ?fdr c:IdentifiedObject.mRID ?fdrid.
     ?eq c:Equipment.EquipmentContainer ?fdr.
     ?trm c:Terminal.ConductingEquipment ?eq.
     ?trm c:Terminal.ConnectivityNode ?cn.
     ?cn c:IdentifiedObject.mRID ?cnid.
     ?eq a ?classraw.
      bind(strafter(str(?classraw),"CIM100#") as ?eqtype)
     ?eq c:IdentifiedObject.name ?eqname.
     ?trm c:ACDCTerminal.sequenceNumber ?tseq.
    } ORDER by ?cnid ?eqtype ?eqname ?tseq
    """

    szVOLT = """
    SELECT ?voltage_id ?val ?dur ?dir ?bus WHERE {
     ?fdr c:IdentifiedObject.mRID ?fdrid.
     ?status c:ConnectivityNode.ConnectivityNodeContainer ?fdr.
     ?status r:global_property_types c:ConnectivityNode.
     ?status c:IdentifiedObject.name ?bus.
     ?status c:IdentifiedObject.mRID ?voltage_id.
     ?status c:ConnectivityNode.OperationalLimitSet ?ols.
     ?vlim c:OperationalLimit.OperationalLimitSet ?ols.
     ?vlim r:global_property_types c:VoltageLimit.
     ?vlim c:OperationalLimit.OperationalLimitType ?olt.
     ?olt c:OperationalLimitType.acceptableDuration ?dur.
     ?olt c:OperationalLimitType.direction ?rawdir.
      bind(strafter(str(?rawdir),"OperationalLimitDirectionKind.") as ?dir)
     ?vlim c:VoltageLimit.value ?val.
    } ORDER by ?voltage_id ?val
    """

    szCURR = """
    SELECT ?voltage_id ?val ?dur ?dir WHERE {
     ?fdr c:IdentifiedObject.mRID ?fdrid.
     ?eq c:Equipment.EquipmentContainer ?fdr.
     ?eq c:IdentifiedObject.mRID ?voltage_id.
     ?t c:Terminal.ConductingEquipment ?eq.
     ?t c:ACDCTerminal.OperationalLimitSet ?ols.
     ?clim c:OperationalLimit.OperationalLimitSet ?ols.
     ?clim r:global_property_types c:CurrentLimit.
     ?clim c:OperationalLimit.OperationalLimitType ?olt.
     ?olt c:OperationalLimitType.acceptableDuration ?dur.
     ?olt c:OperationalLimitType.direction ?rawdir.
     bind(strafter(str(?rawdir),"OperationalLimitDirectionKind.") as ?dir)
     ?clim c:CurrentLimit.value ?val.
    } ORDER by ?voltage_id ?val
    """

    def __init__(self):
        self.query_handler = None
        # map_voltage_limits: an ascending list of voltage thresholds, indexed by ConnectivityNode ID
        #                     normally the indexing will be 0:ANSI B Range Low, 1:A Low, 2:A High, 3: B High
        self.map_voltage_limits = {}  # Dictionary of VoltageLimit objects
        # map_current_limits: an ascending list of current magnitude thresholds, indexed by equipment ID
        #                     normally the indexing will be 0:normal, 1:emergency
        self.map_current_limits = defaultdict(lambda: [1.0e9, 0.0])  # Default values for current limits
        # map_bus_equipment: a list of equipment terminals associated with connectivity node voltage_id
        self.map_bus_equipment = defaultdict(list)

    def load_voltage_map(self, map_coordinates):
        res_temp = self.query_handler.query("bus-equipment mapper", self.szBUSEQ)
        for soln in res_temp:
            cnid = soln.get("?cnid").to""
            key = f"{soln.get('?eqtype')}:{soln.get('?eqname')}:{soln.get('?tseq')}"
            self.map_bus_equipment[cnid].append(key)

        results = self.query_handler.query("voltage mapper", self.szVOLT)
        last_id = ""
        bus = ""
        Alo = Ahi = 0.0
        Blo = Bhi = 1.0e9
        x = y = 0.0

        for soln in results:
            soln_id = soln.get("?voltage_id").to""
            if soln_id != last_id and soln_id in self.map_bus_equipment:
                keys = self.map_bus_equipment[soln_id]
                for key in keys:
                    if key in map_coordinates:
                        pt1 = map_coordinates[key]
                        x, y = pt1.x, pt1.y
                        break

            if soln_id != last_id:
                if last_id:
                    self.map_voltage_limits[last_id] = VoltageLimit(last_id, bus, x, y, Blo, Alo, Ahi, Bhi)
                Alo = 0.0
                Blo = 1.0e9
                Ahi = 1.0e9
                Bhi = 0.0
                last_id = soln_id

            soln_dir = str(soln.get("?dir"))
            bus = str(soln.get("?bus"))
            dur = float(soln.get("?dur"))
            val = float(soln.get("?val"))

            if soln_dir == "low":
                if val > Alo:
                    Alo = val
                if val < Blo:
                    Blo = val
            elif soln_dir == "high":
                if val < Ahi:
                    Ahi = val
                if val > Bhi:
                    Bhi = val

        if last_id and last_id not in self.map_voltage_limits:
            self.map_voltage_limits[last_id] = VoltageLimit(last_id, bus, x, y, Blo, Alo, Ahi, Bhi)

    def voltage_map_to_json(self, out):
        # df2 = decimal.Decimal("#0.00")
        # df4 = decimal.Decimal("#0.0000")
        idx_last = len(self.map_voltage_limits) - 1
        idx = 0
        s_term = "},"
        for v_id, vLim in self.map_voltage_limits.items():
            if idx == idx_last:
                s_term = "}"
            out.write(
                json.dumps(
                    {
                        "voltage_id": v_id,
                        "Blo": f"{vLim.Blo: .2f}",
                        "Alo": f"{vLim.Alo: .2f}",
                        "Ahi": f"{vLim.Ahi: .2f}",
                        "Bhi": f"{vLim.Bhi: .2f}",
                        "ConnectivityNode": vLim.bus,
                        "x": f"{vLim.x: .4f}",
                        "y": f"{vLim.y: .4f}",
                    }
                )
                + s_term
            )
            idx += 1

    def current_map_to_json(self, out):
        # df2 = decimal.Decimal("#0.00")
        idx_last = len(self.map_current_limits) - 1
        idx = 0
        s_term = "},"
        for v_id, vals in self.map_current_limits.items():
            if idx == idx_last:
                s_term = "}"
            out.write(
                json.dumps(
                    {"voltage_id": v_id, "Normal": f"{vals[0]: .2f}", "Emergency": f"{vals[1]:.2f}"}
                )
                + s_term
            )
            idx += 1

    def load_current_map(self):
        results = self.query_handler.query("current mapper", self.szCURR)
        last_id = ""
        Norm = 1.0e9
        Emer = 0.0
        for soln in results:
            v_id = soln.get("?voltage_id").to""
            if v_id != last_id:
                if last_id:
                    self.map_current_limits[last_id] = [Norm, Emer]
                Norm = 1.0e9
                Emer = 0.0
                last_id = v_id

            soln_dir = str(soln.get("?dir"))
            dur = float(soln.get("?dur"))
            val = float(soln.get("?val"))

            if val < Norm:
                Norm = val
                if Norm > Emer:
                    Emer = Norm
            if val > Emer:
                Emer = val

        if last_id and last_id not in self.map_current_limits:
            self.map_current_limits[last_id] = [Norm, Emer]

    def build_limit_maps(self, mdl, qH, map_coordinates=None):
        self.query_handler = qH
        self.load_voltage_map(map_coordinates or DistCoordinates(mdl))
        self.load_current_map()


if __name__ == "__main__":
    # Usage example:
    operational_limits = OperationalLimits()
    # operational_limits.build_limit_maps(mdl, qH)
    # operational_limits.voltage_map_to_json(out)
    # operational_limits.current_map_to_json(out)
