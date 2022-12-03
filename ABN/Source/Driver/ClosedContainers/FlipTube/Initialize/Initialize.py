from ....Tools.Command.Command import Command
from .InitializeOptions import InitializeOptions


class InitializeCommand(Command):
    def __init__(self, Name: str, OptionsInstance: InitializeOptions):
        Command.__init__(self, Name)
        self.OptionsInstance: InitializeOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Initialize"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
