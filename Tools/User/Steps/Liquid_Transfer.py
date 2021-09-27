from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...User import Samples as SAMPLES
from ...Hamilton.Commands import Pipette as PIPETTE
from ...User import Configuration as CONFIGURATION
from ...General import HamiltonIO as HAMILTONIO
from ...General import Log as LOG
import copy

TITLE = "Liquid Transfer"
NAME = "Source"
TYPE = "Liquid Type"
STORAGE = "Storage Condition"
VOLUME = "Volume (uL)"
MIXING = "Mix?"

IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init():
	pass

def CreateStep(DestinationPlate, Source, Type, Storage, Volume, Mixing):
	NewStep = STEPS.Class(TITLE)
	NewStep.SetCoordinates(STEPS.NOT_EXCEL_COORDINATES[0],STEPS.NOT_EXCEL_COORDINATES[1])
	NewStep.SetParentPlate(DestinationPlate)

	NewStep.AddParameters(NAME, Source)
	NewStep.AddParameters(TYPE, Type)
	NewStep.AddParameters(STORAGE, Storage)
	NewStep.AddParameters(VOLUME, Volume)
	NewStep.AddParameters(MIXING, Mixing)

	return NewStep

def Step(step):
	LOG.BeginCommentsLog()

	DestinationPlate = step.GetParentPlate()
	
	SourceList = SAMPLES.Column(step.GetParameters()[NAME])
	SourceVolumeList = SAMPLES.Column(step.GetParameters()[VOLUME])
	MixList = SAMPLES.Column(step.GetParameters()[MIXING])
	
	for Source in SourceList:
		SOLUTIONS.AddSolution(Source, step.GetParameters()[TYPE], step.GetParameters()[STORAGE])

	Sequences = PLATES.GetPlate(DestinationPlate).CreatePipetteSequence(SourceList, SourceVolumeList,MixList)
	
	_Temp = copy.deepcopy(Sequences)
	for Sequence in _Temp:
			SOLUTIONS.GetSolution(Sequence["Source"]).AddVolume(Sequence["Volume"])
			SOLUTIONS.AddPipetteVolume(Sequence["Volume"])
	
	if HAMILTONIO.IsSimulated() == False:
		for sequence in Sequences:
			try:
				sequence["Source"] = CONFIGURATION.GetDeckLoading(sequence["Source"])["Sequence"]
			except:
				pass
			try:
				sequence["Destination"] = CONFIGURATION.GetDeckLoading(sequence["Destination"])["Sequence"]
			except:
				pass
	#Translate User defined names into sequence loading names

	if len(Sequences) == 0:
		LOG.Comment("Number of sequences is zero so no liquid transfer will actually occur.")

	LOG.EndCommentsLog()

	LOG.BeginCommandLog()
	if len(Sequences) != 0:
		PIPETTE.Do(DestinationPlate, Sequences)
	LOG.EndCommandLog()

