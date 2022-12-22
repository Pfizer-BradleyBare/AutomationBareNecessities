from typing import Callable

from ....Tools.Command.Command import Command
from .PlacePlateOptions import PlacePlateOptions


class PlacePlateCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: PlacePlateOptions,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ):
        Command.__init__(
            self,
            self.__class__.__name__ + ": " + Name,
            CustomErrorHandling,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsInstance: PlacePlateOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Transport IPG"

    def GetCommandName(self) -> str:
        return "Place Plate"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict
