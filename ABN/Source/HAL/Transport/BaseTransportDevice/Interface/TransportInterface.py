from abc import abstractmethod

from .....Tools.AbstractClasses import InterfaceABC
from ....Layout import LayoutItem


class TransportInterface(InterfaceABC):
    @abstractmethod
    def MovePlate(
        self, SourceLayoutItem: LayoutItem, DestinationLayoutItem: LayoutItem
    ):
        raise NotImplementedError
