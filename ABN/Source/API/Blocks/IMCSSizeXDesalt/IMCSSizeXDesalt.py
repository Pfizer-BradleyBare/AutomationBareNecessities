from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook
from ....HAL import Hal


@ClassDecorator_AvailableBlock
class IMCSSizeXDesalt(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "IMCS SizeX Desalt" + str((self.Row, self.Col))

    def GetSource(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetWaste(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def GetEQBuffer(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 4, self.Col + 2, self.Row + 4, self.Col + 2
        )

    def GetLoadVolume(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 5, self.Col + 2, self.Row + 5, self.Col + 2
        )

    def GetElutionMethod(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 6, self.Col + 2, self.Row + 6, self.Col + 2
        )

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass
