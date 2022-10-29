from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook
from ....HAL import Hal


@ClassDecorator_AvailableBlock
class LiquidTransfer(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Liquid Transfer" + str((self.Row, self.Col))

    def GetSource(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetVolume(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def GetMix(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 4, self.Col + 2, self.Row + 4, self.Col + 2
        )

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):
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

        # We need to figure out the pipetting first
