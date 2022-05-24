from ..Steps import Steps as STEPS
from ..Steps import Wait as WAIT
from ..Steps import Plate as PLATE
from ..Steps import Liquid_Transfer as LIQUID_TRANSFER
from ...User import Samples as SAMPLES
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...Hamilton.Commands import Transport as TRANSPORT
from ...Hamilton.Commands import Labware as LABWARE
from ...Hamilton.Commands import Vacuum as VACUUM
from ...Hamilton.Commands import Pipette as PIPETTE
from ...User import Configuration as CONFIGURATION
from ...General import Log as LOG
from ...General import HamiltonIO as HAMILTONIO

TITLE = "Vacuum"
SOURCE = "Source"
VOLUME = "Volume (uL)"
VACUUM_PLATE = "Vacuum Plate"
WAIT_TIME = "Pre Vacuum Wait (min)"
PRESSURE = "Pressure Difference (mTorr)"
TIME = "Vacuum Time (min)"

IsUsedFlag = False
VacPlates = set()

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def GetVacPlates():
	global VacPlates
	return VacPlates

def Init(MutableStepsList):
	global IsUsedFlag
	global VacPlates

	for Step in MutableStepsList:
		if Step.GetTitle() == TITLE:
			IsUsedFlag = True
			VacPlates.add(Step.GetParameters()[VACUUM_PLATE])
			CONFIGURATION.AddOmitLoading(Step.GetParameters()[VACUUM_PLATE])

def Step(step):

	Destination = step.GetParentPlateName()
	SourceList = SAMPLES.Column(step.GetParameters()[SOURCE])
	VolumeList = SAMPLES.Column(step.GetParameters()[VOLUME])
	WaitTime = step.GetParameters()[WAIT_TIME]
	VacPlate = step.GetParameters()[VACUUM_PLATE]

	PLATES.LABWARE.GetLabware(Destination).SetIsVacuum(VacPlate)
	#The plate that we vacuum into needs to be a vacuum compatible plate. Set that here on a per step basis

	DestinationNamesList = SAMPLES.Column(Destination)
	DestinationContextStringsList = PLATES.LABWARE.GetContextualStringsList(step,DestinationNamesList)
	SourceNamesList = SourceList
	SourceContextStringsList = PLATES.LABWARE.GetContextualStringsList(step,SourceNamesList)
	SourceVolumesList = VolumeList
	MixingList = SAMPLES.Column("No")

	Sequence = PLATES.CreatePipetteSequence(DestinationContextStringsList,DestinationNamesList,SourceContextStringsList,SourceNamesList,SourceVolumesList,MixingList)
	#we are going to create the sequence here so we can get all associated info at once.

	LiquidTransferFlag = False
	if Sequence.GetNumSequencePositions() != 0:
		TransferVolumes = Sequence.GetTransferVolumes()
		LiquidClassStrings = Sequence.GetLiquidClassStrings()

		HAMILTONIO.AddCommand(PIPETTE.GetLiquidClassStrings({"TransferVolumes":TransferVolumes,"LiquidCategories":LiquidClassStrings}),False)
		HAMILTONIO.AddCommand(PIPETTE.GetTipSequenceStrings({"TransferVolumes":TransferVolumes}),False)
		LiquidTransferFlag = True

	HAMILTONIO.AddCommand(VACUUM.GetVacuumPlateSequenceString({"VacuumPlateName":VacPlate}),False)

	HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[Destination]}),False)
	HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[Destination]}),False)
	HAMILTONIO.AddCommand(VACUUM.GetVacuumCollectionPlateSequenceString({"VacuumPlateName":VacPlate}),False)
	HAMILTONIO.AddCommand(VACUUM.GetVacuumCollectionPlateTransportType({"VacuumPlateName":VacPlate}),False)
	#Get info to move collection plate

	HAMILTONIO.AddCommand(VACUUM.GetVacuumParkSequenceString({"VacuumPlateName":VacPlate}),False)
	HAMILTONIO.AddCommand(VACUUM.GetVacuumParkTransportType({"VacuumPlateName":VacPlate}),False)
	HAMILTONIO.AddCommand(VACUUM.GetVacuumManifoldSequenceString({"VacuumPlateName":VacPlate}),False)
	HAMILTONIO.AddCommand(VACUUM.GetVacuumManifoldTransportType({"VacuumPlateName":VacPlate}),False)
	#Get info to move vacuum manifold

	Response = HAMILTONIO.SendCommands()

	if Response == False:
		LiquidClassStrings = ""
		TipSequenceStrings = ""
		VacuumPlateSequence = ""
		DeckPlateSequence = ""
		DeckPlateType = ""
		CollectionPlateSequence = ""
		CollectionPlateType = ""
		VacuumParkSequence = ""
		VacuumParkType = ""
		VacuumManifoldSequence = ""
		VacuumManifoldType = ""
	else:
		if LiquidTransferFlag == True:
			LiquidClassStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
			TipSequenceStrings = Response.pop(0)["Response"].split(HAMILTONIO.GetDelimiter())
		VacuumPlateSequence = Response.pop(0)["Response"]
		DeckPlateSequence = Response.pop(0)["Response"]
		DeckPlateType = Response.pop(0)["Response"]
		CollectionPlateSequence = Response.pop(0)["Response"]
		CollectionPlateType = Response.pop(0)["Response"]
		VacuumParkSequence = Response.pop(0)["Response"]
		VacuumParkType = Response.pop(0)["Response"]
		VacuumManifoldSequence = Response.pop(0)["Response"]
		VacuumManifoldType = Response.pop(0)["Response"]
	#Lets get the info we need to move everything

	if not (TITLE in STEPS.GetPreviousStepInPathway(step).GetTitle()):
		HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":DeckPlateType,"SourceSequenceString":DeckPlateSequence,"DestinationLabwareType":CollectionPlateType,"DestinationSequenceString":CollectionPlateSequence,"Park":"False","CheckExists":"After"}))
		HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":VacuumParkType,"SourceSequenceString":VacuumParkSequence,"DestinationLabwareType":VacuumManifoldType,"DestinationSequenceString":VacuumManifoldSequence,"Park":"True","CheckExists":"False"}))
		#Move collection plate then manifold

		Response = HAMILTONIO.SendCommands()
	
	if LiquidTransferFlag == True:

		for Counter in range(0,Sequence.GetNumSequencePositions()):
			Sequence.GetDestinations()[Counter] = VacPlate
			Sequence.GetCurrentDestinationVolumes()[Counter] = 0
		#We need to modify the destination to be the vacuum plate sequence above. The liquid needs to move through the vacuum plate.
		#We additionally need to modify the CurrentDestinationVolume to be zero since the vacuum plate should always be zero.

		HAMILTONIO.AddCommand(PIPETTE.Transfer({"SequenceClass":Sequence,"LiquidClasses":LiquidClassStrings,"TipSequences":TipSequenceStrings,"KeepTips":"False","DestinationPipettingOffset":8}))
		Response = HAMILTONIO.SendCommands()
	#This will perform the move of the collection plate, manifold (If required) and finally pipette liquid into the vacuum plate.

	WAIT.StartTimer(step,WaitTime,PreVacuumWaitCallback)
	#Vacuum wait time

def PreVacuumWaitCallback(step):
	Destination = step.GetParentPlateName()
	Volume = step.GetParameters()[VOLUME]
	VacPlate = step.GetParameters()[VACUUM_PLATE]
	WaitTime = step.GetParameters()[WAIT_TIME]
	Pressure = step.GetParameters()[PRESSURE]
	Time = step.GetParameters()[TIME]

	HAMILTONIO.AddCommand(VACUUM.Start({"VacuumPlateName":VacPlate,"VacuumPressure":Pressure}))
	Response = HAMILTONIO.SendCommands()

	WAIT.StartTimer(step,Time,VacuumWaitCallback)
	#Wait for vacuum time now

def VacuumWaitCallback(step):

	Destination = step.GetParentPlateName()
	Volume = step.GetParameters()[VOLUME]
	VacPlate = step.GetParameters()[VACUUM_PLATE]
	WaitTime = step.GetParameters()[WAIT_TIME]
	Pressure = step.GetParameters()[PRESSURE]
	Time = step.GetParameters()[TIME]

	HAMILTONIO.AddCommand(VACUUM.Stop({"VacuumPlateName":VacPlate}))
	Response = HAMILTONIO.SendCommands()
	

	HAMILTONIO.AddCommand(LABWARE.GetSequenceStrings({"PlateNames":[Destination]}),False)
	HAMILTONIO.AddCommand(LABWARE.GetLabwareTypes({"PlateNames":[Destination]}),False)
	HAMILTONIO.AddCommand(VACUUM.GetVacuumCollectionPlateSequenceString({"VacuumPlateName":VacPlate}),False)
	HAMILTONIO.AddCommand(VACUUM.GetVacuumCollectionPlateTransportType({"VacuumPlateName":VacPlate}),False)
	#Get info to move collection plate

	HAMILTONIO.AddCommand(VACUUM.GetVacuumParkSequenceString({"VacuumPlateName":VacPlate}),False)
	HAMILTONIO.AddCommand(VACUUM.GetVacuumParkTransportType({"VacuumPlateName":VacPlate}),False)
	HAMILTONIO.AddCommand(VACUUM.GetVacuumManifoldSequenceString({"VacuumPlateName":VacPlate}),False)
	HAMILTONIO.AddCommand(VACUUM.GetVacuumManifoldTransportType({"VacuumPlateName":VacPlate}),False)
	#Get info to move vacuum manifold
		
	Response = HAMILTONIO.SendCommands()

	if Response == False:
		DeckPlateSequence = ""
		DeckPlateType = ""
		CollectionPlateSequence = ""
		CollectionPlateType = ""
		VacuumParkSequence = ""
		VacuumParkType = ""
		VacuumManifoldSequence = ""
		VacuumManifoldType = ""
	else:
		DeckPlateSequence = Response.pop(0)["Response"]
		DeckPlateType = Response.pop(0)["Response"]
		CollectionPlateSequence = Response.pop(0)["Response"]
		CollectionPlateType = Response.pop(0)["Response"]
		VacuumParkSequence = Response.pop(0)["Response"]
		VacuumParkType = Response.pop(0)["Response"]
		VacuumManifoldSequence = Response.pop(0)["Response"]
		VacuumManifoldType = Response.pop(0)["Response"]
	#Lets get the info we need to move everything

	if not (TITLE in STEPS.GetNextStepInPathway(step).GetTitle()):
		HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":VacuumManifoldType,"SourceSequenceString":VacuumManifoldSequence,"DestinationLabwareType":VacuumParkType,"DestinationSequenceString":VacuumParkSequence,"Park":"False","CheckExists":"False"}))
		HAMILTONIO.AddCommand(TRANSPORT.MoveLabware({"SourceLabwareType":CollectionPlateType,"SourceSequenceString":CollectionPlateSequence,"DestinationLabwareType":DeckPlateType,"DestinationSequenceString":DeckPlateSequence,"Park":"True","CheckExists":"After"}))
		Response = HAMILTONIO.SendCommands()
		#Move collection plate then manifold
