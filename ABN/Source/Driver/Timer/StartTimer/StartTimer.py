from ...Tools.Command.Command import Command
from .StartTimerOptions import StartTimerOptions


class StartTimerCommand(Command):
    def __init__(self, Name: str, OptionsInstance: StartTimerOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: StartTimerOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Timer"

    def GetCommandName(self) -> str:
        return "Start Timer"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)