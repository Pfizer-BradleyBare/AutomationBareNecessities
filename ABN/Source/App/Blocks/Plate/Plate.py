from ...Tools import InputChecker
from ...Tools.Container import Plate as PlateContainer
from ...Tools.Context import Context
from ...Tools.Excel import Excel
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class Plate(Block):
    PlateNames: list[str] = list()
    # we can use this to determine if a plate name is already a solution or not.

    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

    def GetPlateName(self, WorkbookInstance: Workbook) -> str:
        return InputChecker.CheckAndConvertItem(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1),
            [str],
            [],
        )

    def GetPlateType(self, WorkbookInstance: Workbook) -> str:
        return InputChecker.CheckAndConvertItem(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 2, self.Col + 1),
            [str],
            [],
        )

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        PlateName = self.GetPlateName(WorkbookInstance)
        PlateFilter = self.GetPlateType(WorkbookInstance)

        # Do parameter validation here

        ContextTrackerInstance = WorkbookInstance.GetContextTracker()

        OldContextInstance = WorkbookInstance.GetExecutingContext()
        NewContextInstance = Context(
            OldContextInstance.GetName() + ":" + PlateName,
            OldContextInstance.GetDispenseWellSequenceTracker(),
            OldContextInstance.GetDispenseWellSequenceTracker(),
            OldContextInstance.GetWellFactorTracker(),
        )
        # We only bring forward the dispense well sequences

        ContextTrackerInstance.ManualUnload(OldContextInstance)
        ContextTrackerInstance.ManualLoad(NewContextInstance)
        WorkbookInstance.SetExecutingContext(NewContextInstance)
        # Deactivate the previous context and active this new context by removing and new adding

        ContainerTracker = WorkbookInstance.GetContainerTracker()
        if ContainerTracker.PlateTrackerInstance.IsTracked(PlateName) is False:
            ContainerTracker.PlateTrackerInstance.ManualLoad(
                PlateContainer(PlateName, WorkbookInstance.GetName(), PlateFilter)
            )
        # Create the container if it does not already exists

        return True
