from ...Tools.Command.Command import Command
from .LoadCarrierOptions import LoadCarrierOptions


class LoadCarrierCommand(Command):
    def __init__(self, Name: str, OptionsInstance: LoadCarrierOptions):
        Command.__init__(self, Name)
        self.OptionsInstance: LoadCarrierOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Autoload"

    def GetCommandName(self) -> str:
        return "Load Carrier"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
