from collections import defaultdict

from ....Tools.Command.Command import Command
from .CloseOptionsTracker import CloseOptionsTracker


class CloseCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsTrackerInstance: CloseOptionsTracker,
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsTrackerInstance: CloseOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Close"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = defaultdict(list)
        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        return OutputDict
