from ....HAL.DeckLocation import DeckLocation
from ....HAL.Labware import Labware
from ....HAL.Layout import LayoutItem
from ....Server.Globals.HandlerRegistry import HandlerRegistry
from ...Tools.HALLayer.HALLayer import HALLayer


def GetLayoutItem(
    DeckLocationInstance: DeckLocation, LabwareInstance: Labware
) -> LayoutItem | None:

    HALLayerInstance: HALLayer = HandlerRegistry.GetObjectByName(
        "API"
    ).HALLayerInstance  # type:ignore

    LayoutItemTrackerInstance = HALLayerInstance.LayoutItemTrackerInstance

    DeckLocationFiltering = [
        Item
        for Item in LayoutItemTrackerInstance.GetObjectsAsList()
        if Item.DeckLocationInstance == DeckLocationInstance
    ]

    if len(DeckLocationFiltering) == 0:
        return None

    LabwareFiltering = [
        Item
        for Item in DeckLocationFiltering
        if Item.LabwareInstance == LabwareInstance
    ]

    if len(LabwareFiltering) == 0:
        return None

    if len(LabwareFiltering) > 1:
        raise Exception(
            "Length of LabwareFiltering is greater than 1. This should not happen. Please fix."
        )

    return LabwareFiltering[0]