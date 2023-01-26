from collections import defaultdict
from typing import Callable

from ....Tools.Command.Command import Command
from .DispenseOptionsTracker import DispenseOptionsTracker


class DispenseCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsTrackerInstance: DispenseOptionsTracker,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
        )
        self.OptionsTrackerInstance: DispenseOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "Pipette 96 Channel"

    def GetCommandName(self) -> str:
        return "Dispense"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, list]:

        OutputDict = defaultdict(list)

        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        ChannelNumberList = [0] * 96

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = 1

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)  # type:ignore

        return OutputDict

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
