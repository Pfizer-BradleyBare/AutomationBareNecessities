from ...Tools.Command.Command import Command
from .LoadCarrierOptions import LoadCarrierOptions


class LoadCarrierCommand(Command):
    def __init__(
        self, Name: str, CustomErrorHandling: bool, OptionsInstance: LoadCarrierOptions
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: LoadCarrierOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Autoload"

    def GetCommandName(self) -> str:
        return "Load Carrier"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict