from abc import abstractmethod

# This is an abstract loader class for loading configuration files


class ObjectABC:
    @abstractmethod
    def GetName(self) -> str:
        raise NotImplementedError  # this doesn't actually raise an error. This is an abstract method so python will complain
