import yaml

from ..Layout import LayoutItem
from .Lid import Lid
from .LidTracker import LidTracker


def LoadYaml(LidTrackerInstance: LidTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for LidID in ConfigFile["Lid IDs"]:
        LidItem = ConfigFile["Lid IDs"][LidID]

        if LidItem["Enabled"] is not True or LidItem["Supported Labware"] is None:
            continue

        LidLabware = LidTrackerInstance.LabwareTrackerInstance.GetObjectByName(
            LidItem["Labware"]
        )
        LidLocation = LidTrackerInstance.DeckLocationTrackerInstance.GetObjectByName(
            LidItem["Deck Location ID"]
        )
        LidSequence = LidItem["Sequence"]

        Labwares = list()

        for LabwareID in LidItem["Supported Labware"]:
            Labwares.append(
                LidTrackerInstance.LabwareTrackerInstance.GetObjectByName(LabwareID)
            )

        LidTrackerInstance.ManualLoad(
            Lid(LidID, LayoutItem(LidSequence, LidLocation, LidLabware), Labwares)
        )
        # Create Labware Class and append