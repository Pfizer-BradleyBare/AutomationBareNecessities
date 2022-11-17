from ....Driver.Pipette import Sequence, SequenceTracker  # , Pipette
from ....Tools import Excel, ExcelHandle
from ...Tools.Container import Container, ContainerOperator
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class LiquidTransfer(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Liquid Transfer" + str((self.Row, self.Col))

    def GetSource(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 2, self.Col + 2)

    def GetVolume(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 3, self.Col + 2)

    def GetMix(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 4, self.Col + 2)

    def Preprocess(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

            Destinations = self.GetParentPlateName()
            Sources = self.GetSource()
            Volumes = self.GetVolume()
            MixingStrings = self.GetMix()

            WorklistInstance = WorkbookInstance.GetWorklist()

            Destinations = WorklistInstance.ConvertToWorklistColumn(Destinations)
            MixingStrings = WorklistInstance.ConvertToWorklistColumn(MixingStrings)

            if WorklistInstance.IsWorklistColumn(Sources):
                Sources = WorklistInstance.ReadWorklistColumn(Sources)
            else:
                Sources = WorklistInstance.ConvertToWorklistColumn(Sources)

            if WorklistInstance.IsWorklistColumn(Volumes):
                Volumes = WorklistInstance.ReadWorklistColumn(Volumes)
            else:
                Volumes = WorklistInstance.ConvertToWorklistColumn(Volumes)

            # Input validation here

            AspirateMixingParams: list[int] = list()
            DispenseMixingParams: list[int] = list()

            for MixingString in MixingStrings:
                MixParams = {"Aspirate": 0, "Dispense": 0}

                if MixingString != "No":
                    MixingString = MixingString.replace(" ", "").split("+")

                    for MixParam in MixingString:
                        MixParam = MixParam.split(":")
                        MixParams[MixParam[0]] = int(MixParam[1])

                AspirateMixingParams.append(MixParams["Aspirate"])
                DispenseMixingParams.append(MixParams["Dispense"])
            # Convert mixing strings to mixing params

            ContainerTrackerInstance = WorkbookInstance.GetContainerTracker()

            for Source in Sources:
                SourceContainerInstance = Container(
                    Source,
                    WorkbookInstance.GetSolutionTracker()
                    .GetObjectByName(Source)
                    .GetCategory(),
                )
                if (
                    ContainerTrackerInstance.IsTracked(SourceContainerInstance)
                    is not True
                ):
                    ContainerTrackerInstance.ManualLoad(SourceContainerInstance)
            # If source is not a container then we need to add it

            SequenceTrackerInstance = SequenceTracker()
            for (
                WellNumber,
                Destination,
                Source,
                Volume,
                AspirateMixingParam,
                DispenseMixingParam,
            ) in zip(
                range(1, WorklistInstance.GetNumSamples() + 1),
                Destinations,
                Sources,
                Volumes,
                AspirateMixingParams,
                DispenseMixingParams,
            ):
                SequenceTrackerInstance.ManualLoad(
                    Sequence(
                        WellNumber,
                        ContainerOperator(
                            ContainerTrackerInstance.GetObjectByName(Destination), self
                        ),
                        ContainerOperator(
                            ContainerTrackerInstance.GetObjectByName(Source), self
                        ),
                        AspirateMixingParam,
                        DispenseMixingParam,
                        Volume,
                    )
                )
            # Create our pipetting tracker

            # Pipette(
            #    WorkbookInstance,
            #    SequenceTrackerInstance,
            #    HalInstance.GetPipetteTracker(),  # This is the general pipetting tracker
            #    HalInstance.GetPipetteTracker(),  # This is the general pipetting tracker
            # )
            # We need to figure out the pipetting first
