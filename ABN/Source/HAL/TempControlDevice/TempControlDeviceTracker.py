from ...Tools.AbstractClasses import TrackerABC
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from .TempControlDevice import TempControlDevice


class TempControlDeviceTracker(TrackerABC[TempControlDevice]):
    def __init__(
        self,
        LabwareTrackerInstance: LabwareTracker,
        DeckLocationTrackerInstance: DeckLocationTracker,
    ):
        TrackerABC.__init__(self)
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
        self.DeckLocationTrackerInstance: DeckLocationTracker = (
            DeckLocationTrackerInstance
        )
