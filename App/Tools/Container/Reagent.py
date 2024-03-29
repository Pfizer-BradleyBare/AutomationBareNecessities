from PytomatedLiquidHandling.API.Tools.Container import Reagent as APIReagent
from PytomatedLiquidHandling.API.Tools.Container.BaseContainer import (
    LiquidClassCategory,
)
from PytomatedLiquidHandling.API.Tools.Container.Reagent.ReagentProperty import (
    HomogeneityReagentProperty,
    LLDReagentProperty,
    ViscosityReagentProperty,
    VolatilityReagentProperty,
)

from ..Excel import Excel


class Reagent(APIReagent):
    def __init__(
        self,
        Name: str,
        MethodName: str,
        PreferredLabware: str,
        ExcelInstance: Excel,
        Row: int,
        Col: int,
    ):
        APIReagent.__init__(
            self,
            Name,
            MethodName,
            VolatilityReagentProperty.Low,
            ViscosityReagentProperty.Low,
            HomogeneityReagentProperty.Homogenous,
            LLDReagentProperty.Normal,
        )  # This is a default value.

        self.Filter.append(PreferredLabware)

        self.PreferredLabware: str = PreferredLabware
        self.ExcelInstance: Excel = ExcelInstance
        self.Row: int = Row
        self.Col: int = Col

    def IsCorrectSolution(self) -> bool:
        return (
            self.ExcelInstance.ReadCellValue("Solutions", self.Row, self.Col)
            == self.Name
        )

    def GetLiquidClassCategory(self, WellNumber: int) -> LiquidClassCategory:

        return LiquidClassCategory(
            VolatilityReagentProperty[
                str(
                    self.ExcelInstance.ReadCellValue(
                        "Solutions", self.Row + 3, self.Col + 1
                    )
                )
            ],
            ViscosityReagentProperty[
                str(
                    self.ExcelInstance.ReadCellValue(
                        "Solutions", self.Row + 4, self.Col + 1
                    )
                )
            ],
            HomogeneityReagentProperty[
                str(
                    self.ExcelInstance.ReadCellValue(
                        "Solutions", self.Row + 5, self.Col + 1
                    )
                )
            ],
            LLDReagentProperty[
                str(
                    self.ExcelInstance.ReadCellValue(
                        "Solutions", self.Row + 6, self.Col + 1
                    )
                )
            ],
        )
