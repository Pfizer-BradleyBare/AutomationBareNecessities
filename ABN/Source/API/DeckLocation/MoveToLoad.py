from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.Labware.BaseLabware import Labware as APILabware
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker
from ..Transport.Tools.GetLayoutItem import GetLayoutItem
from ..Transport.Transport import Transport


def MoveToLoad(APILabwareInstance: APILabware) -> bool:

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        HandlerRegistry.GetObjectByName(
            "API"
        ).LoadedLabwareTrackerInstance  # type:ignore
    )

    ResourceLockTrackerInstance: ResourceLockTracker = HandlerRegistry.GetObjectByName(
        "API"
    ).ResourceLockTrackerInstance  # type:ignore

    HALLayerInstance: HALLayer = HandlerRegistry.GetObjectByName(
        "API"
    ).HALLayerInstance  # type:ignore
    # Get our API objects

    DeckLocationTrackerInstance = HALLayerInstance.DeckLocationTrackerInstance

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(APILabwareInstance)
    )

    for (
        LoadedLabwareAssignmentInstance
    ) in LoadedLabwareAssignmentInstances.GetObjectsAsList():

        if (
            LoadedLabwareAssignmentInstance.LayoutItemInstance.DeckLocationInstance.IsLoadableLocation()
        ):
            continue
        # Is it already in the appropriate location?

        PossibleDeckLocationInstances = [
            Location
            for Location in DeckLocationTrackerInstance.GetObjectsAsList()
            if not ResourceLockTrackerInstance.IsTracked(Location.GetName())
            and Location.IsLoadableLocation()
        ]
        # Use filtering to get the possible deck locations

        if len(PossibleDeckLocationInstances) == 0:
            return False

        for PossibleDeckLocationInstance in PossibleDeckLocationInstances:
            DestinationLayoutItemInstance = GetLayoutItem(
                PossibleDeckLocationInstance,
                LoadedLabwareAssignmentInstance.LayoutItemInstance.LabwareInstance,
            )
            # Try to get the layout item for this deck location

            if DestinationLayoutItemInstance is None:
                continue
            # If there isn't a valid item then we will try the next location

            ResourceLockTrackerInstance.ManualUnload(
                LoadedLabwareAssignmentInstance.LayoutItemInstance.DeckLocationInstance
            )
            ResourceLockTrackerInstance.ManualLoad(PossibleDeckLocationInstance)
            # Unload the old location and load the new location. Old location and now available and new location and reserved

            Transport(
                LoadedLabwareAssignmentInstance.LayoutItemInstance,
                DestinationLayoutItemInstance,
            )

            break
            # We moved it! Done with this loop!

    return True