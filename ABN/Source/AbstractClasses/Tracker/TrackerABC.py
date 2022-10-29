from ..Object.ObjectABC import ObjectABC
from typing import Generic, TypeVar

T = TypeVar("T", bound="ObjectABC")


class TrackerABC(Generic[T]):
    def __init__(self):
        self.Collection: dict[str, T] = dict()

    def ManualLoad(self, ObjectABCInstance: T) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                type(ObjectABCInstance).__name__ + " is already tracked. Name: " + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: T) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                type(ObjectABCInstance).__name__ + " is not yet tracked. Name: " + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: T) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[T]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[str, T]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> T:
        return self.Collection[Name]
