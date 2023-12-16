from typing import Optional
from TC57CIM.IEC61970.Base.Domain import PerCent, Frequency, RotationSpeed, ActivePower, Resistance, Seconds, Reactance

class AsynchronousMachine(RotatingMachine):
    def __init__(self) -> None:
        super().__init__()
        self.asynchronousMachineType: Optional[AsynchronousMachineKind] = None  # Type of Asynchronous Machine (motor or generator)
        self.converterFedDrive: Optional[bool] = None  # Indicates if the machine is a converter fed drive
        self.efficiency: Optional[PerCent] = None  # Efficiency of the asynchronous machine at nominal operation in percent
        self.iaIrRatio: Optional[float] = None  # Ratio of locked-rotor current to the rated current of the motor (Ia/Ir)
        self.nominalFrequency: Optional[Frequency] = None  # Nameplate data indicates if the machine is 50 or 60 Hz
        self.nominalSpeed: Optional[RotationSpeed] = None  # Nameplate data (depends on the slip and number of pole pairs)
        self.polePairNumber: Optional[int] = None  # Number of pole pairs of stator
        self.ratedMechanicalPower: Optional[ActivePower] = None  # Rated mechanical power (Pr in the IEC 60909-0)
        self.reversible: Optional[bool] = None  # Indicates if the power can be reversible (for converter drive motors)
        self.rr1: Optional[Resistance] = None  # Damper 1 winding resistance
        self.rr2: Optional[Resistance] = None  # Damper 2 winding resistance
        self.rxLockedRotorRatio: Optional[float] = None  # Locked rotor ratio (R/X)
        self.tpo: Optional[Seconds] = None  # Transient rotor time constant (greater than tppo)
        self.tppo: Optional[Seconds] = None  # Sub-transient rotor time constant (greater than 0)
        self.xlr1: Optional[Reactance] = None  # Damper 1 winding leakage reactance
        self.xlr2: Optional[Reactance] = None  # Damper 2 winding leakage reactance
        self.xm: Optional[Reactance] = None  # Magnetizing reactance
        self.xp: Optional[Reactance] = None  # Transient reactance (unsaturated) (greater than or equal to xpp)
        self.xpp: Optional[Reactance] = None  # Sub-transient reactance (unsaturated) (greater than Xl)
        self.xs: Optional[Reactance] = None  # Synchronous reactance (greater than xp)

    def get_asynchronousMachineType(self) -> Optional[AsynchronousMachineKind]:
        return self.asynchronousMachineType

    def get_converterFedDrive(self) -> Optional[bool]:
        return self.converterFedDrive

    def get_efficiency(self) -> Optional[PerCent]:
        return self.efficiency

    def get_iaIrRatio(self) -> Optional[float]:
        return self.iaIrRatio

    def get_nominalFrequency(self) -> Optional[Frequency]:
        return self.nominalFrequency

    def get_nominalSpeed(self) -> Optional[RotationSpeed]:
        return self.nominalSpeed

    def get_polePairNumber(self) -> Optional[int]:
        return self.polePairNumber

    def get_ratedMechanicalPower(self) -> Optional[ActivePower]:
        return self.ratedMechanicalPower

    def get_reversible(self) -> Optional[bool]:
        return self.reversible

    def get_rr1(self) -> Optional[Resistance]:
        return self.rr1

    def get_rr2(self) -> Optional[Resistance]:
        return self.rr2

    def get_rxLockedRotorRatio(self) -> Optional[float]:
        return self.rxLockedRotorRatio

    def get_tpo(self) -> Optional[Seconds]:
        return self.tpo

    def get_tppo(self) -> Optional[Seconds]:
        return self.tppo

    def get_xlr1(self) -> Optional[Reactance]:
        return self.xlr1

    def get_xlr2(self) -> Optional[Reactance]:
        return self.xlr2

    def get_xm(self) -> Optional[Reactance]:
        return self.xm

    def get_xp(self) -> Optional[Reactance]:
        return self.xp

    def get_xpp(self) -> Optional[Reactance]:
        return self.xpp

    def get_xs(self) -> Optional[Reactance]:
        return self.xs

    def set_asynchronousMachineType(self, new_val: Optional[AsynchronousMachineKind]) -> None:
        self.asynchronousMachineType = new_val

    def set_converterFedDrive(self, new_val: Optional[bool]) -> None:
        self.converterFedDrive = new_val

    def set_efficiency(self, new_val: Optional[PerCent]) -> None:
        self.efficiency = new_val

    def set_iaIrRatio(self, new_val: Optional[float]) -> None:
        self.iaIrRatio = new_val

    def set_nominalFrequency(self, new_val: Optional[Frequency]) -> None:
        self.nominalFrequency = new_val

    def set_nominalSpeed(self, new_val: Optional[RotationSpeed]) -> None:
        self.nominalSpeed = new_val

    def set_polePairNumber(self, new_val: Optional[int]) -> None:
        self.polePairNumber = new_val

    def set_ratedMechanicalPower(self, new_val: Optional[ActivePower]) -> None:
        self.ratedMechanicalPower = new_val

    def set_reversible(self, new_val: Optional[bool]) -> None:
        self.reversible = new_val

    def set_rr1(self, new_val: Optional[Resistance]) -> None:
        self.rr1 = new_val

    def set_rr2(self, new_val: Optional[Resistance]) -> None:
        self.rr2 = new_val

    def set_rxLockedRotorRatio(self, new_val: Optional[float]) -> None:
        self.rxLockedRotorRatio = new_val

    def set_tpo(self, new_val: Optional[Seconds]) -> None:
        self.tpo = new_val

    def set_tppo(self, new_val: Optional[Seconds]) -> None:
        self.tppo = new_val

    def set_xlr1(self, new_val: Optional[Reactance]) -> None:
        self.xlr1 = new_val

    def set_xlr2(self, new_val: Optional[Reactance]) -> None:
        self.xlr2 = new_val

    def set_xm(self, new_val: Optional[Reactance]) -> None:
        self.xm = new_val

    def set_xp(self, new_val: Optional[Reactance]) -> None:
        self.xp = new_val

    def set_xpp(self, new_val: Optional[Reactance]) -> None:
        self.xpp = new_val

    def set_xs(self, new_val: Optional[Reactance]) -> None:
        self.xs = new_val