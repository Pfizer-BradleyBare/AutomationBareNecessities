from typing import Self, cast

from ...Blocks import SplitPlate
from ...Tools import BlockParameter
from ...Tools.Context import Context
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class MergePlates(Block):
    MergedPathwayInstances: list[SplitPlate] = list()
    WaitingMergeInstances: list[Self] = list()

    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

        # Params
        self.PlateName = BlockParameter.Item[str](self, 1)
        self.MergeType = BlockParameter.Item[str](self, 2, ["Yes", "No"])

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        ProcessingMergeInstanceMergeType = self.MergeType.Read(WorkbookInstance)

        SplitPlateBlockInstance: SplitPlate = cast(SplitPlate, self)
        while True:
            SearchBlockInstance = SplitPlateBlockInstance.GetParentNode()

            if SearchBlockInstance is None:
                break

            if (
                type(SplitPlateBlockInstance).__name__ == SplitPlate.__name__
                and SplitPlateBlockInstance not in MergePlates.MergedPathwayInstances
            ):
                break
        # Does this step come after a SplitPlate step? Lets Check

        # Do input validation here

        ContextTrackerInstance = WorkbookInstance.ContextTrackerInstance
        InactiveContextTrackerInstance = WorkbookInstance.InactiveContextTrackerInstance
        # Get Context Trackers

        InactiveContextTrackerInstance.ManualLoad(
            WorkbookInstance.ExecutingContextInstance
        )
        # First thing we need to do is disable this context. If both pathways are merged then we will re-enable the context

        MergePlates.WaitingMergeInstances.append(self)
        # Now we will add ourself to the waiting instances.

        WaitingMergeInstance: MergePlates | None = None
        for MergeInstance in MergePlates.WaitingMergeInstances:
            if MergeInstance.GetParentPlateName() == self.PlateName.Read(
                WorkbookInstance
            ):
                WaitingMergeInstance = MergeInstance

        if WaitingMergeInstance is None:
            return True
        # The other merge plates step hasn't been run yet. We need to wait for it to run. Return

        MergePlates.WaitingMergeInstances.remove(self)
        MergePlates.WaitingMergeInstances.remove(WaitingMergeInstance)
        # We are going to do the merge so these steps are no longer waiting

        WaitingMergeInstanceContext = ContextTrackerInstance.GetObjectByName(
            WaitingMergeInstance.GetContext()
        )
        ProcessingMergeInstanceContext = ContextTrackerInstance.GetObjectByName(
            self.GetContext()
        )
        # Get Merge Instance Contexts

        WaitingMergeInstanceMergeType = WaitingMergeInstance.MergeType.Read(
            WorkbookInstance
        )

        if (
            WaitingMergeInstanceMergeType == "Yes"
            and ProcessingMergeInstanceMergeType == "Yes"
        ):

            InactiveContextTrackerInstance.ManualUnload(ProcessingMergeInstanceContext)
            InactiveContextTrackerInstance.ManualUnload(WaitingMergeInstanceContext)
        # If both merge plate steps continue here then all we need to do is re-enable the pathways
        # This is not an official merge because pathways are not combined

        else:
            MergePlates.MergedPathwayInstances.append(SplitPlateBlockInstance)

            UpdateContextFactorsFlag = True
            if (
                SplitPlateBlockInstance.PathwayChoice.Read(WorkbookInstance) == "Split"
                or SplitPlateBlockInstance.PathwayChoice.Read(WorkbookInstance)
                == "Concurrent"
            ):
                UpdateContextFactorsFlag = False

            def CombineFactors(
                DestinationContextInstance: Context,
                SourceContextInstance: Context,
            ):
                for WellNumber in range(
                    0, WorkbookInstance.WorklistInstance.GetNumSamples()
                ):
                    WellFactorInstance = DestinationContextInstance.GetWellFactorTracker().GetObjectByName(
                        WellNumber
                    )
                    if WellFactorInstance.GetFactor() == 0:
                        DestinationContextInstance.GetWellFactorTracker().ManualUnload(
                            WellFactorInstance
                        )
                        DestinationContextInstance.GetWellFactorTracker().ManualLoad(
                            SourceContextInstance.GetWellFactorTracker().GetObjectByName(
                                WellNumber
                            )
                        )

            # It is guarenteed that the wells in one pathway to do not overlap with the other merging pathway

            if WaitingMergeInstanceMergeType == "Yes":
                InactiveContextTrackerInstance.ManualUnload(WaitingMergeInstanceContext)
                WorkbookInstance.ExecutedBlocksTrackerInstance.ManualLoad(
                    self.GetChildren()[0]
                )
                # We load the other pathways finish step as executed because theoretically it should execute

                if UpdateContextFactorsFlag is True:
                    CombineFactors(
                        WaitingMergeInstanceContext,
                        ProcessingMergeInstanceContext,
                    )

            elif ProcessingMergeInstanceMergeType == "Yes":
                InactiveContextTrackerInstance.ManualUnload(
                    ProcessingMergeInstanceContext
                )
                WorkbookInstance.ExecutedBlocksTrackerInstance.ManualLoad(
                    WaitingMergeInstance.GetChildren()[0]
                )
                # We load the other pathways finish step as executed because theoretically it should execute

                if UpdateContextFactorsFlag is True:
                    CombineFactors(
                        ProcessingMergeInstanceContext,
                        WaitingMergeInstanceContext,
                    )

        return True
