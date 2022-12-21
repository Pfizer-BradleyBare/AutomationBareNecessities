from typing import Callable

from ...Tools.Command.Command import Command
from .UnloadCarrierOptions import UnloadCarrierOptions


class UnloadCarrierCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: UnloadCarrierOptions,
        CallbackFunction: Callable[[tuple], None] | None = None,
        CallbackArgs: tuple | None = None,
    ):
        Command.__init__(
            self,
            self.__class__.__name__ + ": " + Name,
            CustomErrorHandling,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsInstance: UnloadCarrierOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Autoload"

    def GetCommandName(self) -> str:
        return "Unload Carrier"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
