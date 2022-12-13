from ....Tools.Command.Command import Command
from .TipsRemainingOptions import TipsRemainingOptions


class TipsRemainingCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: TipsRemainingOptions,
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: TipsRemainingOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Tip NTR"

    def GetCommandName(self) -> str:
        return "Tips Remaining"

    def GetResponseKeys(self) -> list[str]:
        return ["NumRemaining"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict