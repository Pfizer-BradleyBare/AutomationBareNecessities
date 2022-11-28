from .....Tools.AbstractClasses import ObjectABC


class InitializeOptions(ObjectABC):
    def __init__(self, Name: str, TipSequence: str):

        self.Name: str = Name

        self.TipSequence: str = TipSequence

    def GetName(self) -> str:
        return self.Name
