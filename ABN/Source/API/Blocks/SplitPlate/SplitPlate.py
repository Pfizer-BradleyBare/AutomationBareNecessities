from typing import cast
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)
from ....Tools import Excel
from ...Workbook import Workbook
from ....HAL import Hal
from ...Tools.Context import (
    Context,
    WellFactorTracker,
    WellSequenceTracker,
    WellFactor,
)
from ...Tools.Container import Container
from ...Blocks import Plate


@ClassDecorator_AvailableBlock
class SplitPlate(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Split Plate" + str((self.Row, self.Col))

    def GetPathwayChoice(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetPathway1Name(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def GetPathway2Name(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 4, self.Col + 2, self.Row + 4, self.Col + 2
        )

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):
        Pathway1Name = self.GetPathway1Name()
        Pathway2Name = self.GetPathway2Name()
        PathwayChoices = self.GetPathwayChoice()

        if WorkbookInstance.GetWorklist().IsWorklistColumn(PathwayChoices) is True:
            PathwayChoices = WorkbookInstance.GetWorklist().ReadWorklistColumn(
                PathwayChoices
            )
        else:
            PathwayChoices = WorkbookInstance.GetWorklist().ConvertToWorklistColumn(
                PathwayChoices
            )

        # Do parameter validation here

        ContextTrackerInstance = WorkbookInstance.GetContextTracker()
        InactiveContextTrackerInstance = WorkbookInstance.GetInactiveContextTracker()

        OldContextInstance = WorkbookInstance.GetExecutingContext()
        NewPathway1ContextInstance = Context(
            OldContextInstance.GetName() + ":" + Pathway1Name,
            WellSequenceTracker(),
            WellSequenceTracker(),
            WellFactorTracker(),
        )
        NewPathway2ContextInstance = Context(
            OldContextInstance.GetName() + ":" + Pathway2Name,
            WellSequenceTracker(),
            WellSequenceTracker(),
            WellFactorTracker(),
        )
        # New Contexts. Now we need to load them

        for WellNumber in range(0, WorkbookInstance.GetWorklist().GetNumSamples()):

            PathwayChoice = PathwayChoices[WellNumber]

            Factor = (
                OldContextInstance.GetWellFactorTracker()
                .GetObjectByName(WellNumber)
                .GetFactor()
            )
            SequenceInstance = (
                OldContextInstance.GetDispenseWellSequenceTracker().GetObjectByName(
                    WellNumber
                )
            )

            if PathwayChoice == Pathway1Name:
                Pathway1Factor = Factor * 1.0
                Pathway2Factor = Factor * 0.0

            elif PathwayChoice == Pathway2Name:
                Pathway1Factor = Factor * 0.0
                Pathway2Factor = Factor * 1.0

            elif PathwayChoice == "Split":
                Pathway1Factor = Factor * 0.5
                Pathway2Factor = Factor * 0.5

            else:  # PathwayChoice == "Concurrent":
                Pathway1Factor = Factor * 1.0
                Pathway2Factor = Factor * 1.0

            # Pathway 1 context
            NewPathway1ContextInstance.GetAspirateWellSequenceTracker().ManualLoad(
                SequenceInstance
            )
            NewPathway1ContextInstance.GetDispenseWellSequenceTracker().ManualLoad(
                SequenceInstance
            )
            NewPathway1ContextInstance.GetWellFactorTracker().ManualLoad(
                WellFactor(WellNumber, Pathway1Factor)
            )

            # Pathway 2 context
            NewPathway2ContextInstance.GetAspirateWellSequenceTracker().ManualLoad(
                SequenceInstance
            )
            NewPathway2ContextInstance.GetDispenseWellSequenceTracker().ManualLoad(
                SequenceInstance
            )
            NewPathway2ContextInstance.GetWellFactorTracker().ManualLoad(
                WellFactor(WellNumber, Pathway2Factor)
            )

        # Create the contexts here

        InactiveContextTrackerInstance.ManualLoad(OldContextInstance)
        ContextTrackerInstance.ManualLoad(NewPathway1ContextInstance)
        ContextTrackerInstance.ManualLoad(NewPathway2ContextInstance)
        WorkbookInstance.SetExecutingContext(NewPathway1ContextInstance)
        # Deactivate the previous context and active this new context
        # We always execute pathway 1 first. Just easier to remember cause it is like reading a book. Left to right

        ContainerTracker = WorkbookInstance.GetContainerTracker()

        Children: list[Plate] = cast(list[Plate], self.GetChildren())
        for Child in Children:
            ContainerTracker.ManualLoad(
                Container(Child.GetPlateName(), Child.GetPlateType())
            )
            WorkbookInstance.GetExecutedBlocksTracker().ManualLoad(Child)
            # We are executing these blocks in the split plate step so we need to track them as executed.
        # Create the containers for the plate blocks followin the split plate
        # Split plate pathways must be unique. Thus we are guarenteed that the container does not already exist
