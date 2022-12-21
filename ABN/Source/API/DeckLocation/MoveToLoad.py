from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.Labware.BaseLabware import Labware as APILabware


def MoveToLoad(APILabwareInstance: APILabware):

    HALLayerInstance: HALLayer = HandlerRegistry.GetObjectByName(
        "API"
    ).HALLayerInstance  # type:ignore
