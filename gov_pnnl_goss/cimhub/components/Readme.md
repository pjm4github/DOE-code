This package consists of the refactored java classes from:

`%USERPROFILE%\Documents\Git\GitHub\CIMHub\cimhub\src\main\java\gov\pnnl\gridappsd\cimhub\components`

see:

`https://zepben.github.io/evolve/docs/cim/cim100/TC57CIM/IEC61968/IEC61968CIMVersion`


A model can be found by searching in teh data model page of https://zepben.github.io/evolve/docs/cim/cim100/

Here is further info:
https://cimug.ucaiug.org/CIM%20Profiles/Forms/AllItems.aspx

## Distrubution items
- ACLineSegment
- ACLineSegmentPhase
- AsynchronousMachine
- AsynchronousMachineKind
- Breaker
- BusbarSection
- Clamp
- CompositeSwitch
- Conductor
- Connector
- CoolantType
- Cut
- Disconnector
- EarthFaultCompensator
- EnergyConnection
- EnergyConsumer
- EnergyConsumerPhase
- EnergySource
- EnergySourcePhase
- ExternalNetworkInjection
- FrequencyConverter
- Fuse
- Ground
- GroundDisconnector
- GroundingImpedance
- Jumper
- Junction
- Line
- LinearShuntCompensator
- LinearShuntCompensatorPhase
- LoadBreakSwitch
- MutualCoupling
- NonlinearShuntCompensator
- NonlinearShuntCompensatorPhase
- NonlinearShuntCompensatorPhasePo
- NonlinearShuntCompensatorPoint
- PerLengthImpedance
- PerLengthLineParameter
- PerLengthPhaseImpedance
- PerLengthSequenceImpedance
- PetersenCoil
- PetersenCoilModeKind
- PhaseImpedanceData
- PhaseShuntConnectionKind
- PhaseTapChanger
- PhaseTapChangerAsymmetrical
- PhaseTapChangerLinear
- PhaseTapChangerNonLinear
- PhaseTapChangerSymmetrical
- PhaseTapChangerTable
- PhaseTapChangerTablePoint
- PhaseTapChangerTabular
- Plant
- PowerElectronicsConnection
- PowerTransformer
- PowerTransformerEnd
- ProtectedSwitch
- RatioTapChanger
- RatioTapChangerTable
- RatioTapChangerTablePoint
- ReactiveCapabilityCurve
- Recloser
- RegulatingCondEq
- RegulatingControl
- RegulatingControlModeKind
- RegulationSchedule
- RotatingMachine
- SVCControlMode
- Sectionaliser
- SeriesCompensator
- ShortCircuitRotorKind
- ShuntCompensator
- ShuntCompensatorPhase
- SinglePhaseKind
- StaticVarCompensator
- Switch
- SwitchPhase
- SwitchSchedule
- SynchronousMachine
- SynchronousMachineKind
- SynchronousMachineOperatingMode
- TapChanger
- TapChangerControl
- TapChangerTablePoint
- TapSchedule
- TransformerControlMode
- TransformerCoreAdmittance
- TransformerEnd
- TransformerMeshImpedance
- TransformerStarImpedance
- TransformerTank
- TransformerTankEnd
- VoltageControlZone
- WindingConnection


## Distribution

In the context of the Common Information Model (CIM) for the electrical energy domain, various devices and equipment are
related to the distribution network. These devices play a crucial role in the distribution of electrical power to
end-users. Here are some of the key devices and equipment related to the distribution
network in CIM:

### 1) Distribution Substation:

Represents a facility where high-voltage power from the transmission network is transformed into lower voltage levels
for distribution to end-users.

### 2) Distribution Transformer:

Power transformers used within the distribution network to further reduce voltage levels for local distribution.
Feeder:

Represents a set of electrical conductors, including cables or overhead lines, used to deliver power from a substation
to various load points.

### 3) Switchgear:

Includes circuit breakers, disconnectors, and other switching devices used to control the flow of electricity in the
distribution network.

### 4) Recloser:

An intelligent circuit breaker that can automatically re-close after a fault or disturbance, improving the reliability
of the distribution network.

### 5) Voltage Regulator:

Device used to control and regulate voltage levels within the distribution network, ensuring consistent supply to
customers.

### 6) Capacitor Bank:

Used for power factor correction and improving the efficiency of the distribution system.

### 7) Meter:

Represents various types of meters used for measuring electrical consumption at customer premises, such as smart meters.

### 8) Load Break Switch:

A switch used to isolate or de-energize specific sections of the distribution network for maintenance or fault recovery.

### 9) Recloser Control:

Represents the control and monitoring equipment associated with reclosers.

### 10) Voltage Control Zone:

Defines regions within the distribution network where voltage control is applied to maintain desired voltage levels.

### 11) Consumer Meter:

Represents individual meters at customer premises.

### 12) Energy Consumer:

Represents consumers or loads connected to the distribution network.

### 13) Distribution Line:

Represents the physical infrastructure, including overhead lines or underground cables, used to carry power from
substations to customers.

### 14) Substation Equipment:

Various equipment within a distribution substation, such as circuit breakers, transformers, and protective relays.

### 15) Fuse:

Represents fuses used for overcurrent protection in the distribution network.
These are some of the core devices and equipment related to the distribution network in the CIM. The CIM provides a
standardized way to model and represent these elements, allowing for efficient communication and data exchange in the
domain of electrical energy distribution. The actual CIM model may include more specific classes and properties to
capture the intricacies of distribution network components.