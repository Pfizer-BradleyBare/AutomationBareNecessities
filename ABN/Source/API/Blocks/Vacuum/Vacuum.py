from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook


@ClassDecorator_AvailableBlock
class Vacuum(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Vacuum" + str((self.Row, self.Col))

    def GetSource(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetVolume(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def GetVacuumPlate(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 4, self.Col + 2, self.Row + 4, self.Col + 2
        )

    def GetPreVacuumWaitTime(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 5, self.Col + 2, self.Row + 5, self.Col + 2
        )

    def GetPressureDifference(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 6, self.Col + 2, self.Row + 6, self.Col + 2
        )

    def GetVacuumTime(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 7, self.Col + 2, self.Row + 7, self.Col + 2
        )

    def Process(self, WorkbookInstance: Workbook):
        raise NotImplementedError
