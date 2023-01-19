from typing import Callable

from ...Driver.ClosedContainer.FlipTube import (
    CloseCommand,
    CloseOptions,
    CloseOptionsTracker,
    InitializeCommand,
    InitializeOptions,
    OpenCommand,
    OpenOptions,
    OpenOptionsTracker,
)
from ...Driver.NOP import NOPCommand
from ...Driver.Tools import Command, CommandTracker
from ..Labware import LabwareTracker
from ..Layout import LayoutItem
from .BaseClosedContainer.ClosedContainer import ClosedContainer, ClosedContainerTypes


class FlipTube(ClosedContainer):
    def __init__(
        self, ToolSequence: str, SupportedLabwareTrackerInstance: LabwareTracker
    ):
        ClosedContainer.__init__(
            self,
            ClosedContainerTypes.FlipTube,
            ToolSequence,
            SupportedLabwareTrackerInstance,
        )

    def Initialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            InitializeCommand(
                "",
                InitializeOptions(""),
                None,
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def Deinitialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            NOPCommand(
                "FlipTube Deinitialize NOP",
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def Open(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        OpenOptionsTrackerInstance = OpenOptionsTracker()
        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            OpenOptionsTrackerInstance.ManualLoad(
                OpenOptions(
                    "", self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        ReturnCommandTracker.ManualLoad(
            OpenCommand(
                "",
                OpenOptionsTrackerInstance,
                None,
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def Close(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        CloseOptionsTrackerInstance = CloseOptionsTracker()

        for LayoutItemInstance, Position in zip(LayoutItemInstances, Positions):
            CloseOptionsTrackerInstance.ManualLoad(
                CloseOptions(
                    "", self.ToolSequence, LayoutItemInstance.Sequence, Position
                )
            )

        ReturnCommandTracker.ManualLoad(
            CloseCommand(
                "",
                CloseOptionsTrackerInstance,
                None,
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker
