from ....Tools.AbstractClasses import ObjectABC
from ...Labware import Labware
from ...Layout import LayoutItem


class LoadedLabware(ObjectABC):
    Counter: int = 1

    def __init__(
        self, Name: str, LabwareInstance: Labware, LayoutItemInstance: LayoutItem
    ):
        self.Name: str = Name + str(LoadedLabware.Counter)
        LoadedLabware.Counter += 1

        self.LabwareInstance: Labware = LabwareInstance
        self.LayoutItemInstance: LayoutItem = LayoutItemInstance

        self.Wells = [False] * 2

    def GetName(self) -> str:
        return self.Name

    def GetLabware(self) -> Labware:
        return self.LabwareInstance
