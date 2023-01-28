from ...Tools.Excel import Excel
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class Vacuum(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

    def GetSource(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1)

    def GetVolume(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 2, self.Col + 1)

    def GetVacuumPlate(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 3, self.Col + 1)

    def GetPreVacuumWaitTime(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 4, self.Col + 1)

    def GetPressureDifference(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 5, self.Col + 1)

    def GetVacuumTime(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 6, self.Col + 1)

    def Preprocess(self, WorkbookInstance: Workbook):
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):
        ...
