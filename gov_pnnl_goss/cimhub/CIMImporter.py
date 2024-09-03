import os
import sys
import math
import random
import time
from typing import List, Dict
import sys
import argparse
import csv

from gov_pnnl_goss.cimhub.CIMQuerySetter import CIMQuerySetter
from gov_pnnl_goss.cimhub.GldLineConfig import GldLineConfig
from gov_pnnl_goss.cimhub.GldNode import GldNode
from gov_pnnl_goss.cimhub.OperationalLimits import OperationalLimits
from gov_pnnl_goss.cimhub.components.DistBaseVoltage import DistBaseVoltage
from gov_pnnl_goss.cimhub.components.DistBreaker import DistBreaker
from gov_pnnl_goss.cimhub.components.DistCapacitor import DistCapacitor
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent
from gov_pnnl_goss.cimhub.components.DistConcentricNeutralCable import DistConcentricNeutralCable
from gov_pnnl_goss.cimhub.components.DistCoordinates import DistCoordinates
from gov_pnnl_goss.cimhub.components.DistDisconnector import DistDisconnector
from gov_pnnl_goss.cimhub.components.DistFeeder import DistFeeder
from gov_pnnl_goss.cimhub.components.DistFuse import DistFuse
from gov_pnnl_goss.cimhub.components.DistGroundDisconnector import DistGroundDisconnector
from gov_pnnl_goss.cimhub.components.DistHouse import DistHouse
from gov_pnnl_goss.cimhub.components.DistJumper import DistJumper
from gov_pnnl_goss.cimhub.components.DistLineSpacing import DistLineSpacing
from gov_pnnl_goss.cimhub.components.DistLinesCodeZ import DistLinesCodeZ
from gov_pnnl_goss.cimhub.components.DistLinesInstanceZ import DistLinesInstanceZ
from gov_pnnl_goss.cimhub.components.DistLinesSpacingZ import DistLinesSpacingZ
from gov_pnnl_goss.cimhub.components.DistLoad import DistLoad
from gov_pnnl_goss.cimhub.components.DistLoadBreakSwitch import DistLoadBreakSwitch
from gov_pnnl_goss.cimhub.components.DistMeasurement import DistMeasurement
from gov_pnnl_goss.cimhub.components.DistOverheadWire import DistOverheadWire
from gov_pnnl_goss.cimhub.components.DistPhaseMatrix import DistPhaseMatrix
from gov_pnnl_goss.cimhub.components.DistPowerXfmrCore import DistPowerXfmrCore
from gov_pnnl_goss.cimhub.components.DistPowerXfmrMesh import DistPowerXfmrMesh
from gov_pnnl_goss.cimhub.components.DistPowerXfmrWinding import DistPowerXfmrWinding
from gov_pnnl_goss.cimhub.components.DistRecloser import DistRecloser
from gov_pnnl_goss.cimhub.components.DistRegulator import DistRegulator
from gov_pnnl_goss.cimhub.components.DistSequenceMatrix import DistSequenceMatrix
from gov_pnnl_goss.cimhub.components.DistSolar import DistSolar
from gov_pnnl_goss.cimhub.components.DistStorage import DistStorage
from gov_pnnl_goss.cimhub.components.DistSubstation import DistSubstation
from gov_pnnl_goss.cimhub.components.DistSwitch import DistSwitch
from gov_pnnl_goss.cimhub.components.DistSyncMachine import DistSyncMachine
from gov_pnnl_goss.cimhub.components.DistTapeShieldCable import DistTapeShieldCable
from gov_pnnl_goss.cimhub.components.DistXfmrBank import DistXfmrBank
from gov_pnnl_goss.cimhub.components.DistXfmrCodeOCTest import DistXfmrCodeOCTest
from gov_pnnl_goss.cimhub.components.DistXfmrCodeRating import DistXfmrCodeRating
from gov_pnnl_goss.cimhub.components.DistXfmrCodeSCTest import DistXfmrCodeSCTest
from gov_pnnl_goss.cimhub.components.DistXfmrTank import DistXfmrTank
from gov_pnnl_goss.cimhub.components.DistSectionaliser import DistSectionaliser
from gov_pnnl_goss.cimhub.dto.ModelState import ModelState
from gov_pnnl_goss.cimhub.queryhandler.QueryHandler import QueryHandler
from gov_pnnl_goss.cimhub.queryhandler.impl.HTTPBlazegraphQueryHandler import HTTPBlazegraphQueryHandler
# https://github.com/GRIDAPPSD/CIMHub/blob/master/cimhub/src/main/java/gov/pnnl/gridappsd/cimhub/CIMImporter.java


class CIMImporter(QueryHandler, CIMQuerySetter, OperationalLimits):
    def __init__(self):
        super().__init__()
        self.query_handler = None
        self.query_setter = None
        self.map_banks = {}
        self.map_base_voltages = {}
        self.map_breakers = {}
        self.map_capacitors = {}
        self.map_cn_cables = {}
        self.map_code_oc_tests = {}
        self.map_code_ratings = {}
        self.map_code_sc_tests = {}
        self.map_coordinates = {}
        self.map_count_bank = {}
        self.map_count_code_rating = {}
        self.map_count_code_sc_test = {}
        self.map_count_line_phases = {}
        self.map_count_mesh = {}
        self.map_count_spacing_xy = {}
        self.map_count_tank = {}
        self.map_count_winding = {}
        self.map_disconnectors = {}
        self.map_feeders = {}
        self.map_fuses = {}
        self.map_ground_disconnectors = {}
        self.map_houses = {}
        self.map_jumpers = {}
        self.map_line_configs = {}
        self.map_lines_code_z = {}
        self.map_lines_instance_z = {}
        self.map_lines_spacing_z = {}
        self.map_load_break_switches = {}
        self.map_loads = {}
        self.map_measurements = {}
        self.map_nodes = {}
        self.map_phase_matrices = {}
        self.map_reclosers = {}
        self.map_regulators = {}
        self.map_sectionalisers = {}
        self.map_sequence_matrices = {}
        self.map_solars = {}
        self.map_spacings = {}
        self.map_storages = {}
        self.map_substations = {}
        self.map_substations = {}
        self.map_switches = {}  # Polymorphic
        self.map_sync_machines = {}
        self.map_tanks = {}
        self.map_ts_cables = {}
        self.map_wires = {}
        self.map_xfmr_cores = {}
        self.map_xfmr_meshes = {}
        self.map_xfmr_windings = {}
        self.o_limits = None
        self.all_maps_loaded = False


    def start(self, queryHandler, querySetter, fTarget, fRoot, fSched, load_scale, bWantSched, bWantZIP, randomZIP,
              useHouses, Zcoeff, Icoeff, Pcoeff, maxMeasurements, bHaveEventGen, ms, bTiming, separateLoads=[]):
        self.query_handler = queryHandler
        self.query_setter = querySetter
        fOut, fXY, fID, fDict = "", "", "", ""

        if fTarget == "glm":
            self.load_all_maps(useHouses)
            self.check_maps()
            self.update_model_state(ms)
            self.apply_current_limits()
            fDict = fRoot + "_dict.json"
            fOut = fRoot + "_base.glm"
            fXY = fRoot + "_symbols.json"
            with open(fOut, "w") as pOut:
                self.write_glm_file(pOut, load_scale, bWantSched, fSched, bWantZIP, randomZIP, useHouses,
                                    Zcoeff, Icoeff, Pcoeff, bHaveEventGen, separateLoads)
            with open(fXY, "w") as pXY:
                self.write_json_symbol_file(pXY)
            with open(fDict, "w") as pDict:
                self.write_dictionary_file(pDict, maxMeasurements)

        elif fTarget == "dss":
            self.load_all_maps()
            self.check_maps()
            self.update_model_state(ms)
            self.apply_current_limits()
            fDict = fRoot + "_dict.json"
            fOut = fRoot + "_base.dss"
            fXY = fRoot + "_busxy.dss"
            fID = fRoot + "_uuid.dss"
            with open(fOut, "w") as pOut, open(fID, "w") as pID:
                self.write_dss_file(pOut, pID, fXY, fID, load_scale, bWantSched, fSched, bWantZIP, Zcoeff, Icoeff, Pcoeff)
            with open(fXY, "w") as pXY:
                self.write_dss_coordinates(pXY)
            with open(fDict, "w") as pDict:
                self.write_dictionary_file(pDict, maxMeasurements)

        elif fTarget == "both":
            t1 = self.get_current_time()
            self.load_all_maps(useHouses)
            t2 = self.get_current_time()
            self.check_maps()
            t3 = self.get_current_time()
            self.update_model_state(ms)
            t4 = self.get_current_time()
            self.apply_current_limits()
            t5 = self.get_current_time()
            fXY = fRoot + "_busxy.dss"
            fID = fRoot + "_uuid.dss"
            with open(fRoot + "_base.dss", "w") as pDss, open(fID, "w") as pID:
                self.write_dss_file(pDss, pID, fXY, fID, load_scale, bWantSched, fSched, bWantZIP, Zcoeff, Icoeff, Pcoeff)
            t6 = self.get_current_time()
            with open(fXY, "w") as pXY:
                self.write_dss_coordinates(pXY)
            t7 = self.get_current_time()
            with open(fRoot + "_base.glm", "w") as pGld:
                self.write_glm_file(pGld, load_scale, bWantSched, fSched, bWantZIP, randomZIP, useHouses,
                                    Zcoeff, Icoeff, Pcoeff, bHaveEventGen, separateLoads)
            t8 = self.get_current_time()
            with open(fRoot + "_symbols.json", "w") as pSym:
                self.write_json_symbol_file(pSym)
            t9 = self.get_current_time()
            with open(fRoot + "_dict.json", "w") as pDict:
                self.write_dictionary_file(pDict, maxMeasurements)
            t10 = self.get_current_time()
            with open(fRoot + "_limits.json", "w") as pLimits:
                self.write_limits_file(pLimits)
            t11 = self.get_current_time()
            if bTiming:
                print(f"LoadAllMaps:         {(t2 - t1) / 1e9:.4f}")
                print(f"CheckMaps:           {(t3 - t2) / 1e9:.4f}")
                print(f"UpdateModelState:    {(t4 - t3) / 1e9:.4f}")
                print(f"ApplyCurrentLimits:  {(t5 - t4) / 1e9:.4f}")
                print(f"WriteDSSFile:        {(t6 - t5) / 1e9:.4f}")
                print(f"WriteDSSCoordinates: {(t7 - t6) / 1e9:.4f}")
                print(f"WriteGLMFile:        {(t8 - t7) / 1e9:.4f}")
                print(f"WriteJSONSymbolFile: {(t9 - t8) / 1e9:.4f}")
                print(f"WriteDictionaryFile: {(t10 - t9) / 1e9:.4f}")
                print(f"WriteLimitsFile:     {(t11 - t10) / 1e9:.4f}")

        elif fTarget == "csv":
            self.load_all_maps()
            self.check_maps()
            self.update_model_state(ms)
            self.apply_current_limits()
            self.write_csv_files(fRoot)

        elif fTarget == "idx":
            fOut = fRoot + "_feeder_index.json"
            with open(fOut, "w") as pOut:
                self.write_index_file(pOut)

        elif fTarget == "cim":
            self.load_all_maps()
            self.check_maps()
            fOut = fRoot + ".xml"
            from gov_pnnl_goss.cimhub.CIMWriter import CIMWriter
            # from gov_pnnl_goss.cimhub.CIMWriter import CIMWriter
            with open(fOut, "w") as pOut:
                CIMWriter().write_cim_file(self, queryHandler, pOut)

    def safe_name(self, s):
        # Implement the SafeName method as needed
        pass

    def GenerateModel(self, fTarget, fRoot, fSched, load_scale, bWantSched, bWantZIP, randomZIP, useHouses,
                      Zcoeff, Icoeff, Pcoeff, bHaveEventGen, ms, bTiming):
        # Implement the GenerateModel method to create the model as needed
        pass

    #################### This is the last file that was converted from the cimhub CIMImporter
    # def LoadOneCountMap(self, mapper: Dict[str, int], szTag: str):
    #     szQuery = self.query_setter.getSelectionQuery(szTag)
    #     results = self.query_handler.query(szQuery, szTag)
    #     for soln in results:
    #         key = self.SafeName(soln["?key"].to"")
    #         count = soln["?count"].getInt()
    #         mapper[key] = count
    #     results.close()


    def load_one_count_map(self, map, sz_tag):
        sz_query = self.query_setter.get_selection_query(sz_tag)
        results = self.query_handler.query(sz_query, sz_tag)
        for soln in results:
            key = DistComponent.safe_name(str(soln["?key"]))
            count = soln["?count"].toPython()
            map[key] = count
        results.close()

    def load_count_maps(self):
        self.load_one_count_map(self.map_count_bank, "CountBankTanks")
        self.load_one_count_map(self.map_count_tank, "CountTankEnds")
        self.load_one_count_map(self.map_count_mesh, "CountXfmrMeshes")
        self.load_one_count_map(self.map_count_winding, "CountXfmrWindings")
        self.load_one_count_map(self.map_count_code_rating, "CountXfmrCodeRatings")
        self.load_one_count_map(self.map_count_code_sc_test, "CountXfmrCodeSCTests")
        self.load_one_count_map(self.map_count_line_phases, "CountLinePhases")
        self.load_one_count_map(self.map_count_spacing_xy, "CountSpacingXY")
        # Call the print_all_count_maps() method if needed

    def load_base_voltages(self):
        sz_query = self.query_setter.get_selection_query("DistBaseVoltage")
        results = self.query_handler.query(sz_query, "BaseVoltage")
        for row in results:
            obj = DistBaseVoltage(row)
            self.map_base_voltages[obj.get_key()] = obj
        results.close()

    def load_substations(self):
        sz_query = self.query_setter.get_selection_query("DistSubstation")
        results = self.query_handler.query(sz_query, "Substation")
        for row in results:
            obj = DistSubstation(row)
            self.map_substations[obj.get_key()] = obj
        results.close()

    def load_solars(self):
        sz_query = self.query_setter.get_selection_query("DistSolar")
        results = self.query_handler.query(sz_query, "Solar")
        for row in results:
            obj = DistSolar(row)
            self.map_solars[obj.get_key()] = obj
        results.close()

    def load_measurements(self, use_houses):
        sz_query = self.query_setter.get_selection_query("DistMeasurement")
        results = self.query_handler.query(sz_query, "Measurement")
        for row in results:
            obj = DistMeasurement(row, use_houses)
            self.map_measurements[obj.get_key()] = obj
        results.close()

    def load_storages(self):
        sz_query = self.query_setter.get_selection_query("DistStorage")
        results = self.query_handler.query(sz_query, "Storage")
        for row in results:
            obj = DistStorage(row)
            self.map_storages[obj.get_key()] = obj
        results.close()

    def load_capacitors(self):
        sz_query = self.query_setter.get_selection_query("DistCapacitor")
        results = self.query_handler.query(sz_query, "Capacitor")
        for row in results:
            obj = DistCapacitor(row)
            self.map_capacitors[obj.get_key()] = obj
        results.close()

    def load_loads(self):
        sz_query = self.query_setter.get_selection_query("DistLoad")
        results = self.query_handler.query(sz_query, "Load")
        for row in results:
            obj = DistLoad(row)
            self.map_loads[obj.get_key()] = obj
        results.close()

    def load_phase_matrices(self):
        sz_query = self.query_setter.get_selection_query("DistPhaseMatrix")
        results = self.query_handler.query(sz_query, "PhaseMatrix")
        for row in results:
            obj = DistPhaseMatrix(row)
            self.map_phase_matrices[obj.get_key()] = obj
        results.close()

    def load_sequence_matrices(self):
        sz_query = self.query_setter.get_selection_query("DistSequenceMatrix")
        results = self.query_handler.query(sz_query, "SequenceMatrix")
        for row in results:
            obj = DistSequenceMatrix(row)
            self.map_sequence_matrices[obj.get_key()] = obj
        results.close()

    def load_xfmr_code_ratings(self):
        sz_query = self.query_setter.get_selection_query("DistXfmrCodeRating")
        results = self.query_handler.query(sz_query, "XfmrCodeRating")
        for row in results:
            obj = DistXfmrCodeRating(row, self.map_count_code_rating)
            self.map_code_ratings[obj.get_key()] = obj
        results.close()

    def load_xfmr_code_oc_tests(self):
        sz_query = self.query_setter.get_selection_query("DistXfmrCodeOCTest")
        results = self.query_handler.query(sz_query, "XfmrCodeOCTest")
        for row in results:
            obj = DistXfmrCodeOCTest(row)
            self.map_code_oc_tests[obj.get_key()] = obj
        results.close()

    def load_xfmr_code_sc_tests(self):
        sz_query = self.query_setter.get_selection_query("DistXfmrCodeSCTest")
        results = self.query_handler.query(sz_query, "XfmrCodeSCTest")
        for row in results:
            obj = DistXfmrCodeSCTest(row, self.map_count_code_sc_test)
            self.map_code_sc_tests[obj.get_key()] = obj
        results.close()

    def load_power_xfmr_core(self):
        sz_query = self.query_setter.get_selection_query("DistPowerXfmrCore")
        results = self.query_handler.query(sz_query, "PowerXfmrCore")
        for row in results:
            obj = DistPowerXfmrCore(row)
            self.map_xfmr_cores[obj.get_key()] = obj
        results.close()

    def load_power_xfmr_mesh(self):
        sz_query = self.query_setter.get_selection_query("DistPowerXfmrMesh")
        results = self.query_handler.query(sz_query, "PowerXfmrMesh")
        for row in results:
            obj = DistPowerXfmrMesh(row, self.map_count_mesh)
            self.map_xfmr_meshes[obj.get_key()] = obj
        results.close()

    def load_overhead_wires(self):
        sz_query = self.query_setter.get_selection_query("DistOverheadWire")
        results = self.query_handler.query(sz_query, "OverheadWire")
        for row in results:
            obj = DistOverheadWire(row)
            self.map_wires[obj.get_key()] = obj
        results.close()

    def load_tape_shield_cables(self):
        sz_query = self.query_setter.get_selection_query("DistTapeShieldCable")
        results = self.query_handler.query(sz_query, "TSCable")
        for row in results:
            obj = DistTapeShieldCable(row)
            self.map_ts_cables[obj.get_key()] = obj
        results.close()

    def load_concentric_neutral_cables(self):
        sz_query = self.query_setter.get_selection_query("DistConcentricNeutralCable")
        results = self.query_handler.query(sz_query, "CNCable")
        for row in results:
            obj = DistConcentricNeutralCable(row)
            self.map_cn_cables[obj.get_key()] = obj
        results.close()

    def load_line_spacings(self):
        sz_query = self.query_setter.get_selection_query("DistLineSpacing")
        results = self.query_handler.query(sz_query, "LineSpacing")
        for row in results:
            obj = DistLineSpacing(row, self.map_count_spacing_xy)
            self.map_spacings[obj.get_key()] = obj
        results.close()

    def load_load_break_switches(self):
        sz_query = self.query_setter.get_selection_query("DistLoadBreakSwitch")
        results = self.query_handler.query(sz_query, "LoadBreakSwitch")
        for row in results:
            obj = DistLoadBreakSwitch(row)
            self.map_load_break_switches[obj.get_key()] = obj
        results.close()

    def load_fuses(self):
        sz_query = self.query_setter.get_selection_query("DistFuse")
        results = self.query_handler.query(sz_query, "Fuse")
        for row in results:
            obj = DistFuse(row)
            self.map_fuses[obj.get_key()] = obj
        results.close()

    def load_disconnectors(self):
        sz_query = self.query_setter.get_selection_query("DistDisconnector")
        results = self.query_handler.query(sz_query, "Disconnector")
        for row in results:
            obj = DistDisconnector(row)
            self.map_disconnectors[obj.get_key()] = obj
        results.close()

    def load_ground_disconnectors(self):
        sz_query = self.query_setter.get_selection_query("DistGroundDisconnector")
        results = self.query_handler.query(sz_query, "GroundDisconnector")
        for row in results:
            obj = DistGroundDisconnector(row)
            self.map_ground_disconnectors[obj.get_key()] = obj
        results.close()

    def load_jumpers(self):
        sz_query = self.query_setter.get_selection_query("DistJumper")
        results = self.query_handler.query(sz_query, "Jumper")
        for row in results:
            obj = DistJumper(row)
            self.map_jumpers[obj.get_key()] = obj
        results.close()

    def load_breakers(self):
        sz_query = self.query_setter.get_selection_query("DistBreaker")
        results = self.query_handler.query(sz_query, "Breaker")
        for row in results:
            obj = DistBreaker(row)
            self.map_breakers[obj.get_key()] = obj
        results.close()

    def load_reclosers(self):
        sz_query = self.query_setter.get_selection_query("DistRecloser")
        results = self.query_handler.query(sz_query, "Recloser")
        for row in results:
            obj = DistRecloser(row)
            self.map_reclosers[obj.get_key()] = obj
        results.close()

    def load_sectionalisers(self):
        sz_query = self.query_setter.get_selection_query("DistSectionaliser")
        results = self.query_handler.query(sz_query, "Sectionaliser")
        for row in results:
            obj = DistSectionaliser(row)
            self.map_sectionalisers[obj.get_key()] = obj
        results.close()

    def load_lines_instance_z(self):
        sz_query = self.query_setter.get_selection_query("DistLinesInstanceZ")
        results = self.query_handler.query(sz_query, "LinesInstanceZ")
        for row in results:
            obj = DistLinesInstanceZ(row, self.map_count_line_phases)
            self.map_lines_instance_z[obj.get_key()] = obj
        results.close()

    def load_lines_code_z(self):
        sz_query = self.query_setter.get_selection_query("DistLinesCodeZ")
        results = self.query_handler.query(sz_query, "LinesCodeZ")
        for row in results:
            obj = DistLinesCodeZ(row, self.map_count_line_phases)
            self.map_lines_code_z[obj.get_key()] = obj
        results.close()


    def load_lines_spacing_z(self):
        sz_query = self.query_setter.get_selection_query("DistLinesSpacingZ")
        results = self.query_handler.query(sz_query, "LinesSpacingZ")
        for row in results:
            obj = DistLinesSpacingZ(row, self.map_count_line_phases)
            self.map_lines_spacing_z[obj.get_key()] = obj
        results.close()

    def load_regulators(self):
        sz_query_banked = (
                self.query_setter.get_selection_query("DistRegulatorPrefix")
                + self.query_setter.get_selection_query("DistRegulatorBanked")
                + self.query_setter.get_selection_query("DistRegulatorSuffix")
        )
        results_banked = self.query_handler.query(sz_query_banked, "DistRegulatorBanked")
        for row in results_banked:
            obj = DistRegulator(row, self.query_handler)
            self.map_regulators[obj.get_key()] = obj
        results_banked.close()

        sz_query_tanked = (
                self.query_setter.get_selection_query("DistRegulatorPrefix")
                + self.query_setter.get_selection_query("DistRegulatorTanked")
                + self.query_setter.get_selection_query("DistRegulatorSuffix")
        )
        results_tanked = self.query_handler.query(sz_query_tanked, "DistRegulatorTanked")
        for row in results_tanked:
            obj = DistRegulator(row, self.query_handler)
            self.map_regulators[obj.get_key()] = obj
        results_tanked.close()

    def load_xfmr_tanks(self):
        results = self.query_handler.query(self.query_setter.get_selection_query("DistXfmrTank"), "XfmrTank")
        for row in results:
            obj = DistXfmrTank(row, self.map_count_tank)
            self.map_tanks[obj.get_key()] = obj
        results.close()

    def load_xfmr_banks(self):
        results = self.query_handler.query(self.query_setter.get_selection_query("DistXfmrBank"), "XfmrBank")
        for row in results:
            obj = DistXfmrBank(row, self.map_count_bank)
            self.map_banks[obj.get_key()] = obj
        results.close()

    def load_power_xfmr_windings(self):
        results = self.query_handler.query(self.query_setter.get_selection_query("DistPowerXfmrWinding"),
                                           "PowerXfmrWinding")
        for row in results:
            obj = DistPowerXfmrWinding(row, self.map_count_winding)
            self.map_xfmr_windings[obj.get_key()] = obj
        results.close()

    def load_coordinates(self):
        results = self.query_handler.query(self.query_setter.get_selection_query("DistCoordinates"), "Coordinate")
        for row in results:
            obj = DistCoordinates(row)
            self.map_coordinates[obj.get_key()] = obj
        results.close()

    def load_feeders(self):
        results = self.query_handler.query(self.query_setter.get_selection_query("DistFeeder"), "Feeder")
        for row in results:
            obj = DistFeeder(row)
            self.map_feeders[obj.get_key()] = obj
        results.close()

    def load_houses(self):
        results = self.query_handler.query(self.query_setter.get_selection_query("DistHouse"), "House")
        for row in results:
            obj = DistHouse(row)
            self.map_houses[obj.get_key()] = obj
        results.close()

    def load_sync_machines(self):
        results = self.query_handler.query(self.query_setter.get_selection_query("DistSyncMachine"), "SyncMach")
        for row in results:
            obj = DistSyncMachine(row)
            self.map_sync_machines[obj.get_key()] = obj
        results.close()

    def print_one_map(self, component_map, label):
        print(label)
        keys = sorted(component_map.keys())
        for key in keys:
            print(component_map[key].display_string())

    def print_one_count_map(self, count_map, label):
        print(label)
        keys = sorted(count_map.keys())
        for key in keys:
            print(key + ":" + str(count_map[key]))

    def print_gld_node_map(self, node_map, label):
        print(label)
        keys = sorted(node_map.keys())
        for key in keys:
            print(node_map[key].display_string())

    def print_all_count_maps(self):
        self.print_one_count_map(self.map_count_bank, "Count of Bank Tanks")
        self.print_one_count_map(self.map_count_tank, "Count of Tank Ends")
        self.print_one_count_map(self.map_count_mesh, "Count of Xfmr Meshes")
        self.print_one_count_map(self.map_count_winding, "Count of Xfmr Windings")
        self.print_one_count_map(self.map_count_code_rating, "Count of XfmrCode Ratings")
        self.print_one_count_map(self.map_count_code_sc_test, "Count of XfmrCode SCTests")
        self.print_one_count_map(self.map_count_line_phases, "Count of Line Phases")
        self.print_one_count_map(self.map_count_spacing_xy, "Count of Spacing XY Positions")


    def print_all_maps(self):
        self.print_one_map(self.map_base_voltages, "** BASE VOLTAGES")
        self.print_one_map(self.map_capacitors, "** CAPACITORS")
        self.print_one_map(self.map_cn_cables, "** CN CABLES")
        self.print_one_map(self.map_coordinates, "** COMPONENT XY COORDINATES")
        self.print_one_map(self.map_lines_code_z, "** LINES REFERENCING MATRICES")
        self.print_one_map(self.map_lines_instance_z, "** LINES WITH IMPEDANCE ATTRIBUTES")
        self.print_one_map(self.map_spacings, "** LINE SPACINGS")
        self.print_one_map(self.map_lines_spacing_z, "** LINES REFERENCING SPACINGS")
        self.print_one_map(self.map_breakers, "** BREAKERS")
        self.print_one_map(self.map_reclosers, "** RECLOSERS")
        self.print_one_map(self.map_fuses, "** FUSES")
        self.print_one_map(self.map_load_break_switches, "** LOADBREAK SWITCHES")
        self.print_one_map(self.map_sectionalisers, "** SECTIONALISERS")
        self.print_one_map(self.map_jumpers, "** JUMPERS")
        self.print_one_map(self.map_disconnectors, "** DISCONNECTORS")
        self.print_one_map(self.map_ground_disconnectors, "** GROUND DISCONNECTORS")
        self.print_one_map(self.map_loads, "** LOADS")
        self.print_one_map(self.map_wires, "** OVERHEAD WIRES")
        self.print_one_map(self.map_phase_matrices, "** PHASE IMPEDANCE MATRICES")
        self.print_one_map(self.map_xfmr_cores, "** POWER XFMR CORE ADMITTANCES")
        self.print_one_map(self.map_xfmr_meshes, "** POWER XFMR MESH IMPEDANCES")
        self.print_one_map(self.map_xfmr_windings, "** POWER XFMR WINDINGS")
        self.print_one_map(self.map_regulators, "** REGULATORS")
        self.print_one_map(self.map_sequence_matrices, "** SEQUENCE IMPEDANCE MATRICES")
        self.print_one_map(self.map_solars, "** SOLAR PV SOURCES")
        self.print_one_map(self.map_storages, "** STORAGE SOURCES")
        self.print_one_map(self.map_substations, "** SUBSTATION SOURCES")
        self.print_one_map(self.map_ts_cables, "** TS CABLES")
        self.print_one_map(self.map_code_oc_tests, "** XFMR CODE OC TESTS")
        self.print_one_map(self.map_code_ratings, "** XFMR CODE WINDING RATINGS")
        self.print_one_map(self.map_code_sc_tests, "** XFMR CODE SC TESTS")
        self.print_one_map(self.map_banks, "** XFMR BANKS")
        self.print_one_map(self.map_tanks, "** XFMR TANKS")
        self.print_one_map(self.map_houses, "** HOUSES")
        self.print_one_map(self.map_sync_machines, "** SYNC MACHINES")

    # def LoadAllMaps(self, useHouses=False):
    #     # Implement the LoadAllMaps method to load all necessary maps
    #     pass

    def load_all_maps(self, use_houses=False):
        self.load_count_maps()
        self.load_base_voltages()
        self.load_breakers()
        self.load_capacitors()
        self.load_concentric_neutral_cables()
        self.load_coordinates()
        self.load_disconnectors()
        self.load_fuses()
        self.load_jumpers()
        self.load_lines_code_z()
        self.load_lines_instance_z()
        self.load_line_spacings()
        self.load_lines_spacing_z()
        self.load_load_break_switches()
        self.load_loads()
        self.load_measurements(use_houses)
        self.load_overhead_wires()
        self.load_phase_matrices()
        self.load_power_xfmr_core()
        self.load_power_xfmr_mesh()
        self.load_power_xfmr_windings()
        self.load_reclosers()
        self.load_regulators()
        self.load_sectionalisers()
        self.load_sequence_matrices()
        self.load_solars()
        self.load_storages()
        self.load_substations()
        self.load_tape_shield_cables()
        self.load_xfmr_code_oc_tests()
        self.load_xfmr_code_ratings()
        self.load_xfmr_code_sc_tests()
        self.load_xfmr_tanks()
        self.load_xfmr_banks()
        self.load_feeders()
        self.load_houses()
        self.load_sync_machines()

        self.make_switch_map()

        self.o_limits = OperationalLimits()
        self.o_limits.build_limit_maps(self, self.query_handler, self.map_coordinates)
        self.all_maps_loaded = True

    def check_maps(self):
        n_links, n_nodes = 0, 0

        # CIMPatching is not used in the provided code, so it'status commented out

        if len(self.map_substations) < 1:
            raise RuntimeError("No substation source")

        n_links = (
                len(self.map_load_break_switches)
                + len(self.map_lines_code_z)
                + len(self.map_lines_spacing_z)
                + len(self.map_lines_instance_z)
                + len(self.map_xfmr_windings)
                + len(self.map_tanks)
                + len(self.map_fuses)
                + len(self.map_disconnectors)
                + len(self.map_breakers)
                + len(self.map_reclosers)
                + len(self.map_sectionalisers)
                + len(self.map_jumpers)
        )

        if n_links < 1:
            raise RuntimeError("No lines, transformers, or switches")

        n_nodes = (
                len(self.map_loads)
                + len(self.map_capacitors)
                + len(self.map_solars)
                + len(self.map_storages)
                + len(self.map_sync_machines)
        )

        if n_nodes < 1:
            raise RuntimeError("No loads, capacitors, synchronous machines, solar PV, or batteries")

        return True

    # def ApplyCurrentLimits(self):
    #     # Implement the ApplyCurrentLimits method to apply current limits if necessary
    #     pass

    def apply_current_limits(self):
        # Apply available current limits to a polymorphic mapper of line segments
        map_segments = {}
        map_segments.update(self.map_lines_instance_z)
        map_segments.update(self.map_lines_code_z)
        map_segments.update(self.map_lines_spacing_z)

        for key, obj in map_segments.items():
            if obj.id in self.o_limits.map_current_limits:
                vals = self.o_limits.map_current_limits[obj.id]
                obj.normal_current_limit = vals[0]
                obj.emergency_current_limit = vals[1]

        # Apply to a polymorphic mapper of switches
        for key, obj in self.map_switches.items():
            if obj.id in self.o_limits.map_current_limits:
                vals = self.o_limits.map_current_limits[obj.id]
                obj.normal_current_limit = vals[0]
                obj.emergency_current_limit = vals[1]

        # Apply to transformers and tanks
        for key, obj in self.map_xfmr_windings.items():
            if obj.id in self.o_limits.map_current_limits:
                vals = self.o_limits.map_current_limits[obj.id]
                obj.normal_current_limit = vals[0]
                obj.emergency_current_limit = vals[1]

        for key, obj in self.map_tanks.items():
            if obj.id in self.o_limits.map_current_limits:
                vals = self.o_limits.map_current_limits[obj.id]
                obj.normal_current_limit = vals[0]
                obj.emergency_current_limit = vals[1]

        # Apply to regulators, for GridLAB-D
        # TODO: Implement regulator-specific logic
        for key, obj in self.map_regulators.items():
            if obj.pxfid in self.o_limits.map_current_limits:
                vals = self.o_limits.map_current_limits[obj.pxfid]
                obj.normal_current_limit = vals[0]
                obj.emergency_current_limit = vals[1]

        return True


    def write_limits_file(self, out, o_limits):
        out.write("{\"limits\":{\n")
        out.write("\"voltages\":[\n")
        o_limits.voltage_map_to_json(out)
        out.write("],\n")
        out.write("\"currents\":[\n")
        o_limits.current_map_to_json(out)
        out.write("]\n")
        out.write("}}\n")
        out.close()

    def write_map_dictionary(self, map, label, b_last, out, max_measurements=-1):
        count = 1
        last = len(map)
        out.write("\"" + label + "\":[")

        sorted_keys = sorted(map.keys())

        # If we only want a limited number of measurements, restrict them
        if max_measurements >= 0 and len(sorted_keys) > max_measurements:
            sorted_keys = sorted_keys[:max_measurements]

        for key in sorted_keys:
            out.write(map[key].get_json_entry())
            if count < last:
                out.write(",")
            else:
                out.write("")
            count += 1

        if b_last:
            out.write("]")
        else:
            out.write("],")

    # def WriteDictionaryFile(self, out, maxMeasurements):
    #     # Implement the WriteDictionaryFile method to write the dictionary file
    #     pass

    def write_dictionary_file(self, out, max_measurements):
        out.write("{\"feeders\":[\n")

        for _, fdr in self.map_feeders.items():
            if fdr.feeder_id == self.query_handler.get_feeder_selection():
                out.write("{\"name\":\"" + fdr.feeder_name + "\",\n")
                out.write("\"mRID\":\"" + fdr.feeder_id + "\",\n")
                out.write("\"substation\":\"" + fdr.substation_name + "\",\n")
                out.write("\"substationID\":\"" + fdr.substation_id + "\",\n")
                out.write("\"subregion\":\"" + fdr.subregion_name + "\",\n")
                out.write("\"subregionID\":\"" + fdr.subregion_id + "\",\n")
                out.write("\"region\":\"" + fdr.region_name + "\",\n")
                out.write("\"regionID\":\"" + fdr.region_id + "\",\n")

        self.write_map_dictionary(self.map_sync_machines, "synchronous_machines", False, out)
        self.write_map_dictionary(self.map_capacitors, "capacitors", False, out)
        self.write_map_dictionary(self.map_regulators, "regulators", False, out)
        self.write_map_dictionary(self.map_solars, "solarpanels", False, out)
        self.write_map_dictionary(self.map_storages, "batteries", False, out)
        self.write_map_dictionary(self.map_load_break_switches, "switches", False, out)
        self.write_map_dictionary(self.map_fuses, "fuses", False, out)
        self.write_map_dictionary(self.map_jumpers, "jumpers", False, out)
        self.write_map_dictionary(self.map_sectionalisers, "sectionalisers", False, out)
        self.write_map_dictionary(self.map_breakers, "breakers", False, out)
        self.write_map_dictionary(self.map_reclosers, "reclosers", False, out)
        self.write_map_dictionary(self.map_disconnectors, "disconnectors", False, out)
        self.write_map_dictionary(self.map_loads, "energyconsumers", False, out)
        self.write_map_dictionary(self.map_measurements, "measurements", True, out, max_measurements)

        out.write("}]}\n")
        out.close()

    def write_map_symbols(self, map, label, b_last, out):
        count = 1
        last = len(map)
        out.write("\"" + label + "\":[")

        sorted_keys = sorted(map.keys())

        for key in sorted_keys:
            out.write(map[key].get_json_symbols(self.map_coordinates))
            if count < last:
                out.write(",")
            else:
                out.write("")
            count += 1

        if b_last:
            out.write("]")
        else:
            out.write("],")

    def write_regulator_map_symbols(self, b_last, out):
        count = 1
        last = len(self.map_regulators)
        out.write("\"regulators\":[")

        for key, reg in self.map_regulators.items():
            out.write(reg.get_json_symbols(self.map_coordinates, self.map_tanks, self.map_xfmr_windings))
            if count < last:
                out.write(",")
            else:
                out.write("")
            count += 1

        if b_last:
            out.write("]")
        else:
            out.write("],")

    # def WriteJSONSymbolFile(self, out):
    #     # Implement the WriteJSONSymbolFile method to write the JSON symbol file
    #     pass

    def write_json_symbol_file(self, out):
        count = 1
        last = 0

        out.write("{\"feeders\":[")
        for _, fdr in self.map_feeders.items():
            if fdr.feeder_id == self.query_handler.get_feeder_selection():
                out.write("{\"name\":\"" + fdr.feeder_name + "\",")
                out.write("\"mRID\":\"" + fdr.feeder_id + "\",")
                out.write("\"substation\":\"" + fdr.substation_name + "\",")
                out.write("\"substationID\":\"" + fdr.substation_id + "\",")
                out.write("\"subregion\":\"" + fdr.subregion_name + "\",")
                out.write("\"subregionID\":\"" + fdr.subregion_id + "\",")
                out.write("\"region\":\"" + fdr.region_name + "\",")
                out.write("\"regionID\":\"" + fdr.region_id + "\",")
        out.write("]")

        self.write_map_symbols(self.map_substations, "swing_nodes", False, out)
        self.write_map_symbols(self.map_sync_machines, "synchronous_machines", False, out)
        self.write_map_symbols(self.map_capacitors, "capacitors", False, out)
        self.write_map_symbols(self.map_solars, "solarpanels", False, out)
        self.write_map_symbols(self.map_storages, "batteries", False, out)

        out.write("\"overhead_lines\":[")
        for _, pair in self.map_lines_code_z.items():
            out.write(pair[1].get_json_symbols(self.map_coordinates))
            last += 1
            if count < last:
                out.write(",")
            else:
                out.write("")
            count += 1

        for _, pair in self.map_lines_instance_z.items():
            out.write(pair[1].get_json_symbols(self.map_coordinates))
            last += 1
            if count < last:
                out.write(",")
            else:
                out.write("")
            count += 1

        for _, pair in self.map_lines_spacing_z.items():
            out.write(pair[1].get_json_symbols(self.map_coordinates))
            last += 1
            if count < last:
                out.write(",")
            else:
                out.write("")
            count += 1

        out.write("],")

        self.write_map_symbols(self.map_load_break_switches, "switches", False, out)
        self.write_map_symbols(self.map_fuses, "fuses", False, out)
        self.write_map_symbols(self.map_jumpers, "jumpers", False, out)
        self.write_map_symbols(self.map_breakers, "breakers", False, out)
        self.write_map_symbols(self.map_reclosers, "reclosers", False, out)
        self.write_map_symbols(self.map_sectionalisers, "sectionalisers", False, out)
        self.write_map_symbols(self.map_disconnectors, "disconnectors", False, out)

        out.write("\"transformers\":[")
        last = len(self.map_xfmr_windings)
        for _, pair in self.map_tanks.items():
            if pair[1].glm_used:
                last += 1

        for _, pair in self.map_xfmr_windings.items():
            out.write(pair[1].get_json_symbols(self.map_coordinates))
            last += 1
            if count < last:
                out.write(",")
            else:
                out.write("")
            count += 1

        for _, pair in self.map_tanks.items():
            obj = pair[1]
            if obj.glm_used:
                out.write(obj.get_json_symbols(self.map_coordinates))
                last += 1
                if count < last:
                    out.write(",")
                else:
                    out.write("")
                count += 1

        out.write("],")

        self.write_regulator_map_symbols(True, out)

        out.write("}]")
        out.close()

    def get_glm_line_configuration(self, ln):
        match_A = ""
        match_B = ""
        match_C = ""
        match_N = ""
        config_name = ""
        bCable = False
        buf = ["spc_" + ln.spacing + "_"]

        # What are we looking for?
        for i in range(ln.nwires):
            if ln.wire_classes[i] == "ConcentricNeutralCableInfo":
                bCable = True
                break
            if ln.wire_classes[i] == "TapeShieldCableInfo":
                bCable = True
                break

        for i in range(ln.nwires):
            if ln.wire_phases[i] == "A":
                match_A = self.get_match_wire(ln.wire_classes[i], ln.wire_names[i], bCable)
                buf.append("A")
            if ln.wire_phases[i] == "B":
                match_B = self.get_match_wire(ln.wire_classes[i], ln.wire_names[i], bCable)
                buf.append("B")
            if ln.wire_phases[i] == "C":
                match_C = self.get_match_wire(ln.wire_classes[i], ln.wire_names[i], bCable)
                buf.append("C")
            if ln.wire_phases[i] == "N":
                match_N = self.get_match_wire(ln.wire_classes[i], ln.wire_names[i], bCable)

                # We may need to write this as an unshielded underground line conductor
                if bCable and ln.wire_classes[i] == "OverheadWireInfo":
                    oh_wire = self.map_wires.get(ln.wire_names[i])
                    oh_wire.can_bury = True
                buf.append("N")

        match_SPC = "".join(buf)

        # Search for an existing one
        for config_name, cfg in self.map_line_configs.items():
            if (
                    cfg.spacing == match_SPC
                    and cfg.conductor_A == match_A
                    and cfg.conductor_B == match_B
                    and cfg.conductor_C == match_C
                    and cfg.conductor_N == match_N
            ):
                return config_name

        # Need to make a new one
        config_name = "lcon_" + ln.spacing + "_" + ln.name
        cfg = GldLineConfig(config_name)
        cfg.spacing = match_SPC
        cfg.conductor_A = match_A
        cfg.conductor_B = match_B
        cfg.conductor_C = match_C
        cfg.conductor_N = match_N
        self.map_line_configs[config_name] = cfg
        return config_name

    @staticmethod
    def get_match_wire(wire_class, wire_name, is_cable):
        # Implement the logic for getting match wire based on wire_class, wire_name, and is_cable
        # You can add the logic specific to your application here
        pass

    def make_switch_map(self):
        # Build a polymorphic mapper of switches
        self.map_switches.update(self.map_load_break_switches)
        self.map_switches.update(self.map_fuses)
        self.map_switches.update(self.map_jumpers)
        self.map_switches.update(self.map_breakers)
        self.map_switches.update(self.map_reclosers)
        self.map_switches.update(self.map_sectionalisers)
        self.map_switches.update(self.map_disconnectors)


    # def WriteGLMFile(self, out, load_scale, bWantSched, fSched,
    #                  bWantZIP, randomZIP, useHouses, Zcoeff,
    #                  Icoeff, Pcoeff, bHaveEventGen, dssCommandList):
    #     # Implement the WriteGLMFile method to write the GLM file
    #     pass

    import random

    def write_glm_file(self, out, load_scale, bWantSched, fSched,
                       bWantZIP, randomZIP, useHouses, Zcoeff,
                       Icoeff, Pcoeff, bHaveEventGen, separateLoads):
        # preparatory steps to build the list of nodes
        results = self.query_handler.query(
            "SELECT ?name WHERE {"
            " ?fdr c:IdentifiedObject.mRID ?fdrid."
            " ?status c:ConnectivityNode.ConnectivityNodeContainer ?fdr."
            " ?status r:global_property_types c:ConnectivityNode."
            " ?status c:IdentifiedObject.name ?name."
            "} ORDER by ?name", "list nodes")

        mapNodes = {}
        for soln in results:
            bus = DistComponent.safe_name(soln.get("?name").to_string())
            mapNodes[bus] = GldNode(bus)

        for pair in self.map_substations.items():
            obj = pair[1]
            nd = mapNodes.get(obj.bus)
            nd.bSwing = True
            nd.nomvln = obj.basev / math.sqrt(3.0)
            nd.phases = "ABC"

        # do the Tanks first, because they assign primary and secondary phasings
        for pair in self.map_tanks.items():
            obj = pair[1]
            code = self.map_code_ratings.get(obj.tankinfo)
            code.glmUsed = True
            bServiceTransformer = False
            primaryPhase = ""
            for i in range(obj.size):
                nd = mapNodes.get(obj.bus[i])
                nd.nomvln = obj.basev[i] / math.sqrt(3.0)
                nd.add_phases(obj.phs[i])
                if nd.bSecondary:
                    bServiceTransformer = True
                else:
                    primaryPhase = obj.phs[i]
                    if i > 1:
                        nd.bTertiaryWinding = True

            if bServiceTransformer:
                for i in range(obj.size):
                    nd = mapNodes.get(obj.bus[i])
                    if nd.bSecondary:
                        nd.add_phases(primaryPhase)
                        pt1 = self.map_coordinates.get("PowerTransformer:" + obj.pname + ":1")
                        pt2 = self.map_coordinates.get("PowerTransformer:" + obj.pname + ":2")
                        if pt1.x == 0.0 and pt1.y == 0.0:
                            if pt2.x != 0.0 or pt2.y != 0.0:
                                pt1.x = pt2.x + 3.0
                                pt1.y = pt2.y + 0.0
                        elif pt2.x == 0.0 and pt2.y == 0.0:
                            if pt1.x != 0.0 or pt1.y != 0.0:
                                pt2.x = pt1.x + 3.0
                                pt2.y = pt1.y + 0.0

        for pair in self.map_loads.items():
            obj = pair[1]
            nd = mapNodes.get(obj.bus)
            nd.nomvln = obj.basev / math.sqrt(3.0)
            nd.accumulate_loads(obj.name, obj.phases, obj.precisions, obj.q, obj.pe, obj.qe, obj.pz, obj.pi, obj.pp, obj.qz,
                                obj.qi, obj.qp, randomZIP)

        for pair in self.map_capacitors.items():
            obj = pair[1]
            nd = mapNodes.get(obj.bus)
            nd.nomvln = obj.basev / math.sqrt(3.0)
            nd.add_phases(obj.phs)

        for pair in self.map_lines_instance_z.items():
            obj = pair[1]
            nd1 = mapNodes.get(obj.bus1)
            nd1.nomvln = obj.basev / math.sqrt(3.0)
            nd1.add_phases(obj.phases)
            nd2 = mapNodes.get(obj.bus2)
            nd2.nomvln = nd1.nomvln
            nd2.add_phases(obj.phases)

        for pair in self.map_lines_code_z.items():
            obj = pair[1]
            zmat = self.map_phase_matrices.get(obj.lname)
            if zmat is not None:
                zmat.MarkGLMPermutationsUsed(obj.phases)
            else:
                zseq = self.map_sequence_matrices.get(obj.lname)
            nd1 = mapNodes.get(obj.bus1)
            nd1.nomvln = obj.basev / math.sqrt(3.0)
            nd2 = mapNodes.get(obj.bus2)
            nd2.nomvln = nd1.nomvln
            if "status" in obj.phases:
                nd1.bSecondary = True
                nd2.bSecondary = True
                if len(nd2.phases) > 0:
                    nd1.add_phases(nd2.phases)
                    obj.phases = obj.phases + ":" + nd2.phases
                elif len(nd1.phases) > 0:
                    nd2.add_phases(nd1.phases)
                    obj.phases = obj.phases + ":" + nd1.phases
                pt1 = self.map_coordinates.get("ACLineSegment:" + obj.name + ":1")
                pt2 = self.map_coordinates.get("ACLineSegment:" + obj.name + ":2")
                if pt1.x == 0.0 and pt1.y == 0.0:
                    if pt2.x != 0.0 or pt2.y != 0.0:
                        pt1.x = pt2.x + 3.0
                        pt1.y = pt2.y + 0.0
                elif pt2.x == 0.0 and pt2.y == 0.0:
                    if pt1.x != 0.0 or pt1.y != 0.0:
                        pt2.x = pt1.x + 3.0
                        pt2.y = pt1.y + 0.0
            else:
                nd1.add_phases(obj.phases)
                nd2.add_phases(obj.phases)

        for pair in self.map_lines_spacing_z.items():
            obj = pair[1]
            obj.glm_config = self.get_glm_line_configuration(obj)
            spc = self.map_spacings.get(obj.spacing)
            if spc is not None:
                spc.MarkPermutationsUsed(obj.phases)

            nd1 = mapNodes.get(obj.bus1)
            nd1.nomvln = obj.basev / math.sqrt(3.0)
            nd1.add_phases(obj.phases)
            nd2 = mapNodes.get(obj.bus2)
            nd2.nomvln = nd1.nomvln
            nd2.add_phases(obj.phases)

        for pair in self.map_switches.items():
            obj = pair[1]
            nd1 = mapNodes.get(obj.bus1)
            nd2 = mapNodes.get(obj.bus2)
            if "S" in obj.glm_phases:
                phs1 = nd1.get_phases()
                phs2 = nd2.get_phases()
                if len(phs1) > 1 and "S" in phs1:
                    obj.glm_phases = nd1.get_phases()
                    nd2.reset_phases(phs1)
                elif len(phs2) > 1 and "S" in phs2:
                    obj.glm_phases = nd2.get_phases()
                    nd1.reset_phases(phs2)
            else:
                nd1.nomvln = obj.basev / math.sqrt(3.0)
                nd1.add_phases(obj.phases)
                nd2.nomvln = nd1.nomvln
                nd2.add_phases(obj.phases)

        for pair in self.map_xfmr_windings.items():
            obj = pair[1]
            for i in range(obj.size):
                nd = mapNodes.get(obj.bus[i])
                nd.nomvln = obj.basev[i] / math.sqrt(3.0)
                nd.add_phases("ABC")
                if i > 1:
                    nd.bTertiaryWinding = True

        for pair in self.map_solars.items():
            obj = pair[1]
            nd = mapNodes.get(obj.bus)
            nd.bSolarInverters = True
            if nd.nomvln < 0.0:
                if obj.phases == "ABC" or obj.phases == "AB" or obj.phases == "AC" or obj.phases == "BC":
                    nd.nomvln = obj.ratedU / math.sqrt(3.0)
                else:
                    nd.nomvln = obj.ratedU
            nd.add_phases(obj.phases)
            if nd.bSecondary:
                obj.phases = nd.get_phases()

        for pair in self.map_storages.items():
            obj = pair[1]
            nd = mapNodes.get(obj.bus)
            nd.bStorageInverters = True
            if nd.nomvln < 0.0:
                if obj.phases == "ABC" or obj.phases == "AB" or obj.phases == "AC" or obj.phases == "BC":
                    nd.nomvln = obj.ratedU / math.sqrt(3.0)
                else:
                    nd.nomvln = obj.ratedU
            nd.add_phases(obj.phases)
            if nd.bSecondary:
                obj.phases = nd.get_phases()

        for pair in self.map_sync_machines.items():
            obj = pair[1]
            nd = mapNodes.get(obj.bus)
            nd.bSyncMachines = True
            if nd.nomvln < 0.0:
                if obj.phases == "ABC" or obj.phases == "AB" or obj.phases == "AC" or obj.phases == "BC":
                    nd.nomvln = obj.ratedU / math.sqrt(3.0)
                else:
                    nd.nomvln = obj.ratedU
            nd.add_phases(obj.phases)
            if nd.bSecondary:
                obj.phases = nd.get_phases()

        for pair in self.map_regulators.items():
            reg = pair[1]
            if reg.hasTanks:
                tank = self.map_tanks.get(reg.tname[0])
                code = self.map_code_ratings.get(tank.tankinfo)
                out.write(reg.GetTankedGLM(tank))
                code.glmUsed = False
                tank.glmUsed = False
                for i in range(1, reg.size):
                    tank = self.map_tanks.get(reg.tname[i])
                    code = self.map_code_ratings.get(tank.tankinfo)
                    code.glmUsed = False
                    tank.glmUsed = False
            else:
                xfmr = self.map_xfmr_windings.get(reg.pname)
                out.write(reg.GetGangedGLM(xfmr))
                xfmr.glmUsed = False

        # GLM configurations
        for pair in self.map_wires.items():
            out.write(pair[1].get_glm())
        for pair in self.map_cn_cables.items():
            out.write(pair[1].get_glm())
        for pair in self.map_ts_cables.items():
            out.write(pair[1].get_glm())
        for pair in self.map_spacings.items():
            out.write(pair[1].get_glm())
        for pair in self.map_line_configs.items():
            out.write(pair[1].get_glm())
        for pair in self.map_phase_matrices.items():
            out.write(pair[1].get_glm())
        for pair in self.map_sequence_matrices.items():
            out.write(pair[1].get_glm())
        for pair in self.map_code_ratings.items():
            code = pair[1]
            if code.glmUsed:
                sct = self.map_code_sc_tests.get(code.tname)
                oct = self.map_code_oc_tests.get(code.tname)
                out.write(code.get_glm(sct, oct))

        # GLM circuit components
        for pair in self.map_capacitors.items():
            out.write(pair[1].get_glm())
        for pair in self.map_solars.items():
            out.write(pair[1].get_glm())
        for pair in self.map_storages.items():
            out.write(pair[1].get_glm())
        for pair in self.map_sync_machines.items():
            out.write(pair[1].get_glm())
        for pair in self.map_lines_spacing_z.items():
            out.write(pair[1].get_glm())
        for pair in self.map_lines_code_z.items():
            out.write(pair[1].get_glm())
        for pair in self.map_lines_instance_z.items():
            out.write(pair[1].get_glm())
        for pair in self.map_switches.items():
            obj = pair[1]
            if "S" in obj.glm_phases:
                nd1 = mapNodes.get(obj.bus1)
                nd2 = mapNodes.get(obj.bus2)
                if "_tn_" in nd1.name:
                    nd2.CopyLoad(nd1)
                    mapNodes.pop(obj.bus1)
                else:
                    nd1.CopyLoad(nd2)
                    mapNodes.pop(obj.bus2)
            else:
                out.write(obj.get_glm())
        for pair in self.map_XfmrWindings.items():
            obj = pair[1]
            if obj.glmUsed:
                mesh = self.map_XfmrMeshes.get(obj.name)
                core = self.map_XfmrCores.get(obj.name)
                out.write(pair[1].get_glm(mesh, core))
        for pair in self.map_Tanks.items():
            obj = pair[1]
            if obj.glmUsed:
                out.write(obj.get_glm())

        # GLM nodes and loads
        bWroteEventGen = bHaveEventGen
        for pair in mapNodes.items():
            nd = pair[1]
            out.write(pair[1].get_glm(load_scale, bWantSched, fSched, bWantZIP, useHouses, Zcoeff, Icoeff, Pcoeff,
                                      separateLoads))
            if not bWroteEventGen and nd.bSwingPQ:
                bWroteEventGen = True
                out.write("object fault_check {\n")
                out.write("    name base_fault_check_object;\n")
                out.write("    check_mode ONCHANGE;\n")
                out.write("    strictly_radial false;\n")
                out.write("    eventgen_object testgendev;\n")
                out.write("    grid_association true;\n")
                out.write("}\n")
                out.write("object eventgen {\n")
                out.write("    name testgendev;\n")
                out.write("	fault_type \"DLG-X\";\n")
                out.write("	manual_outages \"" + nd.name + ",2100-01-01 00:00:05,2100-01-01 00:00:30\";\n")
                out.write("}\n")
        # GLM houses
        if useHouses:
            r = random.randint(0,4999)
            for pair in self.map_houses:
                out.write(pair.getValue().get_glm(r))
        # try to link all CIM measurements to the GridLAB-D objects
        # PrintGldNodeMap (mapNodes, "GldNode Map for Measurements");
        measurements_not_linked = 0
        for pair in self.map_measurements:
            obj = pair.getValue()
        #   System.out.println (self.Display"");
            nd = mapNodes.get(obj.bus)
        #   System.out.println (nd.Display"");
            if nd is not None:
                obj.FindSimObject(nd.loadname, nd.phases, nd.bStorageInverters, nd.bSolarInverters, nd.bSyncMachines)
                if not obj.LinkedToSimulatorObject():
                    measurements_not_linked += 1
            else:
                measurements_not_linked += 1

        if measurements_not_linked > 0:
            print(F"*** Could not FindSimObject for {measurements_not_linked} Measurements")
        out.close()

    # def WriteDSSCoordinates(self, out):
    #     # Implement the WriteDSSCoordinates method to write the DSS coordinates
    #     pass

    def write_dss_coordinates(self, out):
        bus_xy_map = {}

        # Loads, capacitors, transformers, and energy sources have a single bus location, assumed to be correct
        for name, coordinates in self.map_coordinates.items():
            if coordinates.x != 0 or coordinates.y != 0:
                if coordinates.cname == "EnergyConsumer":
                    bus = self.map_loads[coordinates.name].bus
                elif coordinates.cname == "LinearShuntCompensator":
                    bus = self.map_capacitors[coordinates.name].bus
                elif coordinates.cname == "EnergySource":
                    bus = self.map_substations[coordinates.name].bus
                elif coordinates.cname == "BatteryUnit":
                    bus = self.map_storages[coordinates.name].bus
                elif coordinates.cname == "PhotovoltaicUnit":
                    bus = self.map_solars[coordinates.name].bus
                elif coordinates.cname == "SynchronousMachine":
                    bus = self.map_sync_machines[coordinates.name].bus
                elif coordinates.cname == "PowerTransformer":
                    tank = self.map_tanks.get(coordinates.name)
                    if tank is not None:
                        for i in range(tank.size):
                            bus_xy_map[tank.bus[i]] = [coordinates.x, coordinates.y]
                    else:
                        winding = self.map_xfmr_windings.get(coordinates.name)
                        if winding is not None:
                            bus_xy_map[winding.bus[coordinates.seq - 1]] = [coordinates.x, coordinates.y]

                if bus:
                    bus_xy_map[bus] = [coordinates.x, coordinates.y]

        # Switches and lines have bus locations; should be in correct order using ACDCTerminal.sequenceNumber
        for name, obj in self.map_lines_code_z.items():
            pt1 = self.map_coordinates.get(f"ACLineSegment:{name}:1")
            pt2 = self.map_coordinates.get(f"ACLineSegment:{name}:2")
            if pt1 and pt2:
                bus_xy_map[obj.bus1] = [pt1.x, pt1.y]
                bus_xy_map[obj.bus2] = [pt2.x, pt2.y]

        for name, obj in self.map_lines_instance_z.items():
            pt1 = self.map_coordinates.get(f"ACLineSegment:{name}:1")
            pt2 = self.map_coordinates.get(f"ACLineSegment:{name}:2")
            if pt1 and pt2:
                bus_xy_map[obj.bus1] = [pt1.x, pt1.y]
                bus_xy_map[obj.bus2] = [pt2.x, pt2.y]

        for name, obj in self.map_lines_spacing_z.items():
            pt1 = self.map_coordinates.get(f"ACLineSegment:{name}:1")
            pt2 = self.map_coordinates.get(f"ACLineSegment:{name}:2")
            if pt1 and pt2:
                bus_xy_map[obj.bus1] = [pt1.x, pt1.y]
                bus_xy_map[obj.bus2] = [pt2.x, pt2.y]

        for name, obj in self.map_load_break_switches.items():
            pt1 = self.map_coordinates.get(f"LoadBreakSwitch:{name}:1")
            pt2 = self.map_coordinates.get(f"LoadBreakSwitch:{name}:2")
            if pt1 and pt2:
                bus_xy_map[obj.bus1] = [pt1.x, pt1.y]
                bus_xy_map[obj.bus2] = [pt2.x, pt2.y]

        for name, obj in self.map_fuses.items():
            pt1 = self.map_coordinates.get(f"Fuse:{name}:1")
            pt2 = self.map_coordinates.get(f"Fuse:{name}:2")
            if pt1 and pt2:
                bus_xy_map[obj.bus1] = [pt1.x, pt1.y]
                bus_xy_map[obj.bus2] = [pt2.x, pt2.y]

        for name, obj in self.map_jumpers.items():
            pt1 = self.map_coordinates.get(f"Jumper:{name}:1")
            pt2 = self.map_coordinates.get(f"Jumper:{name}:2")
            if pt1 and pt2:
                bus_xy_map[obj.bus1] = [pt1.x, pt1.y]
                bus_xy_map[obj.bus2] = [pt2.x, pt2.y]

        for name, obj in self.map_reclosers.items():
            pt1 = self.map_coordinates.get(f"Recloser:{name}:1")
            pt2 = self.map_coordinates.get(f"Recloser:{name}:2")
            if pt1 and pt2:
                bus_xy_map[obj.bus1] = [pt1.x, pt1.y]
                bus_xy_map[obj.bus2] = [pt2.x, pt2.y]

        for name, obj in self.map_breakers.items():
            pt1 = self.map_coordinates.get(f"Breaker:{name}:1")
            pt2 = self.map_coordinates.get(f"Breaker:{name}:2")
            if pt1 and pt2:
                bus_xy_map[obj.bus1] = [pt1.x, pt1.y]
                bus_xy_map[obj.bus2] = [pt2.x, pt2.y]

        for name, obj in self.map_sectionalisers.items():
            pt1 = self.map_coordinates.get(f"Sectionaliser:{name}:1")
            pt2 = self.map_coordinates.get(f"Sectionaliser:{name}:2")
            if pt1 and pt2:
                bus_xy_map[obj.bus1] = [pt1.x, pt1.y]
                bus_xy_map[obj.bus2] = [pt2.x, pt2.y]

        for name, obj in self.map_disconnectors.items():
            pt1 = self.map_coordinates.get(f"Disconnector:{name}:1")
            pt2 = self.map_coordinates.get(f"Disconnector:{name}:2")
            if pt1 and pt2:
                bus_xy_map[obj.bus1] = [pt1.x, pt1.y]
                bus_xy_map[obj.bus2] = [pt2.x, pt2.y]

        # The bus locations in bus_xy_map should now be unique, and topologically consistent, so write them.
        for bus, xy in bus_xy_map.items():
            out.write(f"{bus},{xy[0]},{xy[1]}\n")

        out.close()

    @staticmethod
    def uuid_from_cim_mrid(id_str):
        idx = id_str.find("_")
        if idx >= 0:
            return id_str[idx + 1:]
        return id_str

    # def WriteDSSFile(self, out, outID, fXY, fID, load_scale, bWantSched, fSched, bWantZIP, Zcoeff, Icoeff, Pcoeff):
    #     # Implement the WriteDSSFile method to write the DSS file
    #     pass

    def write_dss_file(self, out, out_id, f_xy, f_id, load_scale,
                       b_want_sched, f_sched, b_want_zip, z_coeff,
                       i_coeff, p_coeff):
        out.write("clear\n")

        for key, value in self.map_substations.items():
            out.write(value.get_dss())
            out_id.write("Circuit." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_wires.items():
            out.write(value.get_dss())
            out_id.write("Wiredata." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_cn_cables.items():
            out.write(value.get_dss())
            out_id.write("CNData." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_ts_cables.items():
            out.write(value.get_dss())
            out_id.write("TSData." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_lines_spacing_z.items():
            obj = value
            spc = self.map_spacings.get(obj.spacing)
            if spc:
                spc.mark_permutations_used(obj.phases)

        for key, value in self.map_spacings.items():
            out.write(value.get_dss())
            out_id.write("LineSpacing." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_phase_matrices.items():
            out.write(value.get_dss())
            out_id.write("Linecode." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_sequence_matrices.items():
            out.write(value.get_dss())
            out_id.write("Linecode." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_code_ratings.items():
            obj = value
            sct = self.map_code_sc_tests.get(obj.tname)
            oct = self.map_code_oc_tests.get(obj.tname)
            out.write(obj.get_dss(sct, oct))
            out_id.write("Xfmrcode." + obj.tname + "\t" + self.uuid_from_cim_mrid(obj.id) + "\n")

        out.write("\n")
        for key, value in self.map_solars.items():
            out.write(value.get_dss())
            out_id.write("PVSystem." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_storages.items():
            out.write(value.get_dss())
            out_id.write("Storage." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_sync_machines.items():
            out.write(value.get_dss())
            out_id.write("Generator." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_loads.items():
            out.write(value.get_dss())
            out_id.write("Load." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_load_break_switches.items():
            out.write(value.get_dss())
            out_id.write("Line." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_fuses.items():
            out.write(value.get_dss())
            out_id.write("Line." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_reclosers.items():
            out.write(value.get_dss())
            out_id.write("Line." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_sectionalisers.items():
            out.write(value.get_dss())
            out_id.write("Line." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_breakers.items():
            out.write(value.get_dss())
            out_id.write("Line." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_disconnectors.items():  # TODO: use map_switches?
            out.write(value.get_dss())
            out_id.write("Line." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_jumpers.items():
            out.write(value.get_dss())
            out_id.write("Line." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_lines_code_z.items():
            out.write(value.get_dss())
            out_id.write("Line." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_lines_spacing_z.items():
            out.write(value.get_dss())
            out_id.write("Line." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_lines_instance_z.items():
            out.write(value.get_dss())
            out_id.write("Line." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_xfmr_windings.items():
            obj = value
            mesh = self.map_xfmr_meshes.get(obj.name)
            core = self.map_xfmr_cores.get(obj.name)
            out.write(obj.get_dss(mesh, core))
            out_id.write("Transformer." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_tanks.items():
            out.write(value.get_dss())
            out_id.write("Transformer." + value.tname + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        for key, value in self.map_regulators.items():
            obj = value
            out.write(obj.get_dss())
            for i in range(obj.size):
                out_id.write("RegControl." + obj.rname[i] + "\t" + self.uuid_from_cim_mrid(obj.id[i]) + "\n")

        out.write("\n")
        for key, value in self.map_capacitors.items():
            out.write(value.get_dss())
            out_id.write("Capacitor." + value.name + "\t" + self.uuid_from_cim_mrid(value.id) + "\n")

        out.write("\n")
        out.write("set voltagebases=[")
        for key, value in self.map_base_voltages.items():
            out.write(value.get_dss())
        out.write("]\n\n")
        out.write("calcv\n\n")

        if b_want_sched:
            out.write(
                f"new loadshape.player npts=1440 sinterval=60 mult=(file={f_sched}.player,col=2,header=yes) action=normalize\n")
            out.write("batchedit load..* duty=player daily=player\n")

        f_xy_file = os.path.basename(f_xy)
        f_id_file = os.path.basename(f_id)

        out.write(f"buscoords {f_xy_file}\n")
        out.write(f"uuids {f_id_file}\n\n")

        out.close()
        out_id.close()

        # ... Other methods and class members ...

    # def WriteIndexFile(self, out):
    #     # Implement the WriteIndexFile method to write the feeder index file
    #     pass
    def write_index_file(self, out):
        self.load_feeders()
        self.print_one_map(self.map_feeders, "*** FEEDERS ***")

        out.write("{\"feeders\":[")

        count = 1
        last = len(self.map_feeders)

        for key, value in self.map_feeders.items():
            out.write(value.get_json_entry())
            if count < last:
                out.write(",")
            else:
                out.write("")

            count += 1

        out.write("]}")
        out.close()

    def write_csv_files(self, fRoot):
        with open(fRoot + "_Buscoords.csv", 'w', newline='') as out:
            csv_writer = csv.writer(out)
            csv_writer.writerow(DistCoordinates.sz_csv_header)
            self.write_dss_coordinates(out)

        self.write_csv_file_with_map_entries(fRoot + "_Capacitors.csv", DistCapacitor.sz_csv_cap_header, self.map_capacitors, lambda x: x.get_cap_csv())
        self.write_csv_file_with_map_entries(fRoot + "_CapControls.csv", DistCapacitor.sz_csv_cap_control_header, self.map_capacitors, lambda x: x.get_cap_control_csv(), lambda x: x.ctrl == "true")
        self.write_csv_file_with_map_entries(fRoot + "_LinesCodeZ.csv", DistLinesCodeZ.sz_csv_header, self.map_lines_code_z, lambda x: x.GetCSV(), lambda x: "status" not in x.phases)
        self.write_csv_file_with_map_entries(fRoot + "_LinesInstanceZ.csv", DistLinesInstanceZ.sz_csv_header, self.map_lines_instance_z, lambda x: x.GetCSV(), lambda x: "status" not in x.phases)

        with open(fRoot + "_LinesSpacingZ.csv", 'w', newline='') as out:
            csv_writer = csv.writer(out)
            csv_writer.writerow(DistLinesSpacingZ.sz_csv_header)
            for pair in self.map_lines_spacing_z.items():
                obj = pair[1]
                spc = self.map_spacings.get(obj.spacing)
                if spc:
                    spc.MarkPermutationsUsed(obj.phases)
                if "status" not in obj.phases:
                    csv_writer.writerow(obj.GetCSV())

        self.write_csv_file_with_map_entries(fRoot + "_Spacings.csv", DistLineSpacing.sz_csv_header, self.map_spacings, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_Loads.csv", DistLoad.sz_csv_header, self.map_loads, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_Regulators.csv", DistRegulator.sz_csv_header, self.map_regulators, lambda x: x.GetCSV())

        with open(fRoot + "_XfmrCodes.csv", 'w', newline='') as out:
            csv_writer = csv.writer(out)
            csv_writer.writerow(DistXfmrCodeRating.sz_csv_header)
            for pair in self.map_code_ratings.items():
                obj = pair[1]
                sct = self.map_code_sc_tests.get(obj.tname)
                oct = self.map_code_oc_tests.get(obj.tname)
                csv_writer.writerow(obj.GetCSV(sct, oct))

        self.write_csv_file_with_map_entries(fRoot + "_XfmrTanks.csv", DistXfmrTank.sz_csv_header, self.map_tanks, lambda x: x.GetCSV(), lambda x: x.glmUsed)

        with open(fRoot + "_Transformers.csv", 'w', newline='') as out:
            csv_writer = csv.writer(out)
            csv_writer.writerow(DistPowerXfmrWinding.sz_csv_header)
            for pair in self.map_xfmr_windings.items():
                obj = pair[1]
                if obj.glmUsed:
                    mesh = self.map_xfmr_meshes.get(obj.name)
                    core = self.map_xfmr_cores.get(obj.name)
                    csv_writer.writerow(obj.GetCSV(mesh, core))

        self.write_csv_file_with_map_entries(fRoot + "_TriplexLines.csv", DistLinesCodeZ.sz_csv_header, self.map_lines_code_z, lambda x: x.GetCSV(), lambda x: "status" in x.phases)
        self.write_csv_file_with_map_entries(fRoot + "_PhaseLineCodes.csv", DistPhaseMatrix.sz_csv_header, self.map_phase_matrices, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_SequenceLineCodes.csv", DistSequenceMatrix.sz_csv_header, self.map_sequence_matrices, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_Wires.csv", DistOverheadWire.sz_csv_header, self.map_wires, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_CNCables.csv", DistConcentricNeutralCable.sz_csv_header, self.map_cn_cables, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_TSCables.csv", DistTapeShieldCable.sz_csv_header, self.map_ts_cables, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_Switches.csv", DistSwitch.sz_csv_header, self.map_switches, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_Solar.csv", DistSolar.sz_csv_header, self.map_solars, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_Storage.csv", DistStorage.sz_csv_header, self.map_storages, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_SyncGen.csv", DistSyncMachine.sz_csv_header, self.map_sync_machines, lambda x: x.GetCSV())
        self.write_csv_file_with_map_entries(fRoot + "_Source.csv", DistSubstation.sz_csv_header, self.map_substations, lambda x: x.GetCSV())


    # def UpdateModelState(self, ms):
    #     machinesToUpdate = ms.getSynchronousmachines()
    #     switchesToUpdate = ms.getSwitches()
    #
    #     for machine in machinesToUpdate:
    #         toUpdate = self.mapSyncMachines.get(machine.name)
    #         if toUpdate is not None:
    #             toUpdate.precisions = machine.precisions
    #             toUpdate.q = machine.q
    #
    #     mapSwitches = self.mapLoadBreakSwitches.copy()
    #     mapSwitches.update(self.mapFuses)
    #     mapSwitches.update(self.mapJumpers)
    #     mapSwitches.update(self.mapBreakers)
    #     mapSwitches.update(self.mapReclosers)
    #     mapSwitches.update(self.mapSectionalisers)
    #     mapSwitches.update(self.mapDisconnectors)
    #     mapSwitches.update(self.mapJumpers)
    #     mapSwitches.update(self.mapGroundDisconnectors)
    #
    #     for sw in switchesToUpdate:
    #         toUpdate = mapSwitches.get(sw.name)
    #         if toUpdate is not None:
    #             toUpdate.is_open = sw.is_open

    def update_model_state(self, ms):
        machines_to_update = ms.synchronous_machines
        switches_to_update = ms.switches

        for machine in machines_to_update:
            to_update = self.map_sync_machines.get(machine.name)
            if to_update is not None:
                to_update.precisions = machine.precisions
                to_update.q = machine.q

        map_switches = {}
        map_switches.update(self.map_load_break_switches)
        map_switches.update(self.map_fuses)
        map_switches.update(self.map_jumpers)
        map_switches.update(self.map_breakers)
        map_switches.update(self.map_reclosers)
        map_switches.update(self.map_sectionalisers)
        map_switches.update(self.map_disconnectors)
        map_switches.update(self.map_jumpers)
        map_switches.update(self.map_ground_disconnectors)

        for sw in switches_to_update:
            to_update = map_switches.get(sw.name)
            if to_update is not None:
                to_update.open = sw.open
        # 	for(DistSwitch status: switchesToUpdate){
        # 		DistSwitch toUpdate = mapLoadBreakSwitches.get(status.name);
        # 		if(toUpdate!=null){
        # 			toUpdate.is_open = status.is_open;
        # 		}
        # 		//mapLoadBreakSwitches.put(status.name, (DistLoadBreakSwitch) toUpdate);
        # 	}
        # 	for(DistSwitch status: switchesToUpdate){
        # 		DistSwitch toUpdate = mapFuses.get(status.name);
        # 		if(toUpdate!=null){
        # 			toUpdate.is_open = status.is_open;
        # 		}
        # 		//mapFuses.put(status.name, (DistFuse)toUpdate);
        # 	}
        # 	for(DistSwitch status: switchesToUpdate){
        # 		DistSwitch toUpdate = mapBreakers.get(status.name);
        # 		if(toUpdate!=null){
        # 			toUpdate.is_open = status.is_open;
        # 		}
        # 		//mapBreakers.put(status.name, (DistBreaker) toUpdate);
        # 	}
        # 	for(DistSwitch status: switchesToUpdate){
        # 		DistSwitch toUpdate = mapReclosers.get(status.name);
        # 		if(toUpdate!=null){
        # 			toUpdate.is_open = status.is_open;
        # 		}
        # 		//mapReclosers.put(status.name, (DistRecloser) toUpdate);
        # 	}
        # 	for(DistSwitch status: switchesToUpdate){
        # 		DistSwitch toUpdate = mapSectionalisers.get(status.name);
        # 		if(toUpdate!=null){
        # 			toUpdate.is_open = status.is_open;
        # 		}
        # 		//mapSectionalisers.put(status.name, (DistSectionaliser) toUpdate);
        # 	}
        # 	for(DistSwitch status: switchesToUpdate){
        # 		DistSwitch toUpdate = mapDisconnectors.get(status.name);
        # 		if(toUpdate!=null){
        # 			toUpdate.is_open = status.is_open;
        # 		}
        # 		//mapDisconnectors.put(status.name,  (DistDisconnector) toUpdate);
        # 	}
        #
        # 	System.out.println("Switches");
        # 	for(String key: mapSwitches.keySet()){
        # 		DistSwitch gen = mapSwitches.get(key);
        # 		System.out.println(key+"  "+gen.is_open);
        # 	}


    # def generateJSONSymbolFile(self, query_handler, out):
    #     self.query_handler = query_handler
    #     if self.query_setter is None:
    #         self.query_setter = CIMQuerySetter()
    #     if not self.all_maps_loaded:
    #         self.LoadAllMaps()
    #     self.CheckMaps()
    #     self.WriteJSONSymbolFile(out)


    def generate_json_symbol_file(self, query_handler, out):
        self.query_handler = query_handler

        if self.query_setter is None:
            self.query_setter = CIMQuerySetter()

        if not self.all_maps_loaded:
            self.load_all_maps()

        self.check_maps()
        self.write_json_symbol_file(out)

    # def generateGLMFile(self, query_handler, query_setter, out, fSched,
    #                     load_scale, bWantSched, bWantZIP,
    #                     randomZIP, useHouses, Zcoeff,
    #                     Icoeff, Pcoeff, bHaveEventGen):
    #     self.query_handler = query_handler
    #     if self.query_setter is None:
    #         self.query_setter = query_setter
    #     if not self.all_maps_loaded:
    #         self.LoadAllMaps()
    #     self.CheckMaps()
    #     self.ApplyCurrentLimits()
    #     self.WriteGLMFile(out, load_scale, bWantSched, fSched,
    #                       bWantZIP, randomZIP, useHouses, Zcoeff,
    #                       Icoeff, Pcoeff, bHaveEventGen, [])

    def generate_glm_file(self, query_handler, query_setter, out, f_sched,
                          load_scale, b_want_sched, b_want_zip, random_zip, use_houses,
                          z_coeff, i_coeff, p_coeff, b_have_event_gen):
        self.query_handler = query_handler

        if self.query_setter is None:
            self.query_setter = query_setter

        if not self.all_maps_loaded:
            self.load_all_maps()

        self.check_maps()
        self.apply_current_limits()
        self.write_glm_file(out, load_scale, b_want_sched, f_sched, b_want_zip, random_zip,
                            use_houses, z_coeff, i_coeff, p_coeff, b_have_event_gen, [])

    # def generateDictionaryFile(self, query_handler, out, useHouses, modelState):
    #     self.generateDictionaryFile(query_handler, out, -1, useHouses, modelState)
    #
    # def generateDictionaryFile(self, query_handler, out, maxMeasurements, useHouses, ms):
    #     self.query_handler = query_handler
    #     if self.query_setter is None:
    #         self.query_setter = CIMQuerySetter()
    #     if not self.all_maps_loaded:
    #         self.LoadAllMaps(useHouses)
    #     self.CheckMaps()
    #     self.UpdateModelState(ms)
    #     self.WriteDictionaryFile(out, maxMeasurements)

    def generate_dictionary_file(self, query_handler, out, a, b, c=None):
        if not c:
            max_measurements = -1
            use_houses = a
            model_state = b
        else:
            max_measurements = a
            use_houses = b
            model_state = c

        self.query_handler = query_handler

        if self.query_setter is None:
            self.query_setter = CIMQuerySetter()

        if not self.all_maps_loaded:
            self.load_all_maps(use_houses)

        self.check_maps()
        self.update_model_state(model_state)

        self.write_dictionary_file(out, max_measurements)


    #     def generateDSSFile(self, query_handler, out, outID, fXY, fID,
    #                         load_scale, bWantSched, fSched, bWantZIP,
    #                         Zcoeff, Icoeff, Pcoeff):
    #         self.query_handler = query_handler
    #         if self.query_setter is None:
    #             self.query_setter = CIMQuerySetter()
    #         if not self.all_maps_loaded:
    #             self.LoadAllMaps()
    #         self.CheckMaps()
    #         self.ApplyCurrentLimits()
    #         self.WriteDSSFile(out, outID, fXY, fID, load_scale, bWantSched, fSched, bWantZIP, Zcoeff, Icoeff, Pcoeff)

    def generate_dss_file(self, query_handler, out, out_id, f_xy, f_id,
                          load_scale, b_want_sched, f_sched, b_want_zip,
                          z_coeff, i_coeff, p_coeff):
        self.query_handler = query_handler

        if self.query_setter is None:
            self.query_setter = CIMQuerySetter()

        if not self.all_maps_loaded:
            self.load_all_maps()

        self.check_maps()
        self.apply_current_limits()

        self.write_dss_file(out, out_id, f_xy, f_id, load_scale, b_want_sched, f_sched, b_want_zip, z_coeff, i_coeff, p_coeff)


    #     def generateDSSCoordinates(self, query_handler, out):
    #         self.query_handler = query_handler
    #         if self.query_setter is None:
    #             self.query_setter = CIMQuerySetter()
    #         if not self.all_maps_loaded:
    #             self.LoadAllMaps()
    #         self.CheckMaps()
    #         self.WriteDSSCoordinates(out)

    def generate_dss_coordinates(self, query_handler, out):
        self.query_handler = query_handler

        if self.query_setter is None:
            self.query_setter = CIMQuerySetter()

        if not self.all_maps_loaded:
            self.load_all_maps()

        self.check_maps()

        self.write_dss_coordinates(out)

    def write_csv_file_with_map_entries(self, filename, header, map_entries, get_csv_function, filter_function=None):
        with open(filename, 'w', newline='') as out:
            csv_writer = csv.writer(out)
            csv_writer.writerow(header)
            for pair in map_entries.items():
                obj = pair[1]
                if not filter_function or filter_function(obj):
                    csv_writer.writerow(get_csv_function(obj))

    def generate_feeder_index_file(self, queryHandler, out):
        self.query_handler = queryHandler
        if self.query_setter is None:
            self.query_setter = CIMQuerySetter()
        self.write_index_file(out)

    def get_current_time(self):
        # Return the system time in nanoseconds
        return time.time_ns()


def main():
    """
    # Usage example:

    # Instantiate the CIMImporter class
    cim_importer = CIMImporter()

    # Replace the following code with the appropriate queries, parameters, and file paths.
    # For example, you would need to provide the query_handler, query_setter, and other necessary inputs.
    cim_importer.generateGLMFile(query_handler, query_setter, "output.glm", "output.sch",
                                 1.0, True, True, False, False,
                                 False, 0.0, 0.0, 0.0, False)

    :return:
    """
    fRoot = ""
    freq = 60.0
    load_scale = 1.0
    bWantSched = False
    bWantZIP = False
    bSelectFeeder = False
    randomZIP = False
    useHouses = False
    bHaveEventGen = False
    bTiming = False
    bReadSPARQL = False
    fSched = ""
    fTarget = "dss"
    feeder_mRID = ""
    Zcoeff = 0.0
    Icoeff = 0.0
    Pcoeff = 0.0
    blazegraphURI = "http://localhost:8889/bigdata/namespace/kb/sparql"
    fSPARQL = ""
    maxMeasurements = -1

    example_string = "Example 1: java CIMImporter -l=1 -i=1 -dimensions=zipload_schedule ieee8500"\
                     "   assuming Jena and Commons-Math are in Java'status classpath, this will produce two output files"\
                     "   1) ieee8500_base.glm with GridLAB-D components for a constant-current model at peak load,"\
                     "      where each load'status base_power attributes reference zipload_schedule.player"\
                     "      This file includes an adjustable source voltage, and manual capacitor/tap changer states."\
                     "      It should be invoked from a separate GridLAB-D file that sets up the clock, solver, recorders, etc."\
                     "      For example, these two GridLAB-D input lines set up 1.05 per-unit source voltage on a 115-kV system:"\
                     "          #define VSOURCE=69715.065 // 66395.3 * 1.05"\
                     "          #include \"ieee8500_base.glm\""\
                     "      If there were capacitor/tap changer controls in the CIM input file, that data was written to"\
                     "          ieee8500_base.glm as comments, which can be recovered through manual edits."\
                     "   2) ieee8500_symbols.json with component labels and geographic coordinates, used in GridAPPS-D but not GridLAB-D"\
                     "Example 2: java CIMImporter -o=dss ieee8500"\
                     "   assuming Jena and Commons-Math are in Java'status classpath, this will produce three output files"\
                     "   1) ieee8500_base.dss with OpenDSS components for the CIM LoadResponseCharacteristic at peak load"\
                     "      It should be invoked from a separate OpenDSS file that sets up the solution and options."\
                     "   2) ieee8500_busxy.dss with node xy coordinates"\
                     "   3) ieee8500_uuid.dss with CIM mRID values for the components"

    parser = argparse.ArgumentParser("CIM Importer", add_help=False)

    parser.add_argument("output_root", type=str, help="Output root directory")
    parser.add_argument("--help", help=example_string)
    parser.add_argument("-q", dest="queries_file", help="Optional file with CIM namespace and component queries (defaults to CIM100)")
    parser.add_argument("-status", dest="feeder_mRID", help="Select one feeder by CIM mRID; selects all feeders if not specified")
    parser.add_argument("-o", dest="output_format", choices=["glm", "dss", "both", "idx", "cim", "csv"], default="glm", help="Output format; defaults to glm")
    parser.add_argument("-l", dest="load_scale", type=float, default=1.0, help="Load scaling factor; defaults to 1")
    parser.add_argument("-functions", dest="freq", type=float, default=60.0, help="System frequency; defaults to 60")
    parser.add_argument("-dimensions", dest="schedule_name", help="Root input_code_filename for scheduled ZIP loads (defaults to none)")
    parser.add_argument("-z", dest="constant_Z", type=float, default=0.0, help="Constant Z portion (defaults to 0 for CIM-defined LoadResponseCharacteristic)")
    parser.add_argument("-i", dest="constant_I", type=float, default=0.0, help="Constant I portion (defaults to 0 for CIM-defined LoadResponseCharacteristic)")
    parser.add_argument("-precisions", dest="constant_P", type=float, default=0.0, help="Constant P portion (defaults to 0 for CIM-defined LoadResponseCharacteristic)")
    parser.add_argument("-r", dest="random_ZIP", type=int, choices=[0, 1], default=0, help="Determine ZIP load fraction based on given XML file or randomized fractions")
    parser.add_argument("-h", dest="use_houses", type=int, choices=[0, 1], default=0, help="Determine if house load objects should be added to the model or not")
    parser.add_argument("-x", dest="have_event_gen", type=int, choices=[0, 1], default=0, help="Indicate whether for glm, the model will be called with a fault_check already created")
    parser.add_argument("-t", dest="timing", type=int, choices=[0, 1], default=0, help="Request timing of top-level methods and SPARQL queries, requires -o=both for methods")
    parser.add_argument("-u", dest="blazegraph_uri", default="http://localhost:8889/bigdata/namespace/kb/sparql", help="Blazegraph URI (if connecting over HTTP); defaults to http://localhost:8889/bigdata/namespace/kb/sparql")
    parser.add_argument("-Q", dest="sparql_queries_file", help="Queries file for SPARQL")

    args = parser.parse_args()

    try:

        blazegraphURI = args.blazegraph_uri
        qh = HTTPBlazegraphQueryHandler(blazegraphURI)
        qs = CIMQuerySetter()

        if args.sparql_queries_file:
            fSPARQL = args.sparql_queries_file
            bReadSPARQL = True
            qs.set_queries_from_xml_file(fSPARQL)
        if args.feeder_mRID:
            feeder_mRID = args.feeder_mRID
            bSelectFeeder = True
        if bSelectFeeder:
            pass
            qh.addFeederSelection (feeder_mRID)
        if args.timing:
            bTiming = True

        qh.setTiming(bTiming)

        # List < SyncMachine > machinesToUpdate = new ArrayList <> ();
        machinesToUpdate = []
        # List < Switch > switchesToUpdate = new ArrayList <> ();
        switchesToUpdate = []
        ms = ModelState(machinesToUpdate, switchesToUpdate)

        fTarget = args.output_format
        fRoot = args.output_format
        cim_importer = CIMImporter()
        cim_importer.start(qh, qs, fTarget, fRoot, fSched, load_scale,
                            bWantSched, bWantZIP, randomZIP, useHouses,
                            Zcoeff, Icoeff, Pcoeff, maxMeasurements, bHaveEventGen, ms, bTiming)

                    # queryHandler, querySetter, fTarget, fRoot, fSched, load_scale,
                    # bWantSched, bWantZIP, randomZIP, useHouses,
                    # Zcoeff, Icoeff, Pcoeff, maxMeasurements, bHaveEventGen, ms, bTiming, separateLoads=[]):


    except RuntimeError as e:
        print(f"Can not produce a model: {e}")
        # print(e)


    #
    #     CIMImporter.generateFeederIndexFile(
    #         args.output_root,
    #         args.queries_file,
    #         args.feeder_mRID,
    #         args.output_format,
    #         args.load_scale,
    #         args.freq,
    #         args.schedule_name,
    #         args.constant_Z,
    #         args.constant_I,
    #         args.constant_P,
    #         args.random_ZIP,
    #         args.use_houses,
    #         args.have_event_gen,
    #         args.timing,
    #         args.blazegraph_uri,
    #         args.sparql_queries_file
    #     )
    # except Exception as e:
    #     print("Error:", e)
    #     sys.exit(1)

if __name__ == "__main__":
    # Heres a list of runtime parameters to try
    # DB_URL="http://localhost:8889/bigdata/namespace/kb/sparql"
    # -status=_DFBF372D-4291-49EF-ACCA-53DAFDE0338F -u=$DB_URL -o=both -l=1.0 -i=1 -h=0 -x=0 -t=1 ieee13assets
    # See the ./example/example.sh
    main()
