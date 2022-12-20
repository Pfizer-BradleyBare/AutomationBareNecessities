from abc import abstractmethod

from .....Tools.AbstractClasses import ObjectABC
from ..Plate.Well.WellSolution.WellSolutionTracker import WellSolutionTracker
from .LiquidClassCategory.LiquidClassCategory import LiquidClassCategory


class Labware(ObjectABC):
    def __init__(self, Name: str, Filter: str):
        self.Name: str = Name
        self.Filter: str = Filter

    def GetName(self) -> str:
        return self.Name

    @abstractmethod
    def GetVolume(self) -> float:
        ...

    @abstractmethod
    def GetLiquidClassCategory(self) -> LiquidClassCategory:
        ...

    @abstractmethod
    def Aspirate(self, WellNumber: int, Volume: float) -> WellSolutionTracker:
        ...

    @abstractmethod
    def Dispense(
        self, WellNumber: int, WellSolutionTrackerInstance: WellSolutionTracker
    ):
        ...
