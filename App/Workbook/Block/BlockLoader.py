from typing import cast

from ...Blocks import Finish, Plate, SplitPlate
from ...Tools.Excel import Excel
from .Block import Block, BlockObjectCreationWrapper
from .BlockTracker import BlockTracker


def Load(BlockTrackerInstance: BlockTracker, ExcelInstance: Excel):

    MethodSheet = ExcelInstance.ReadRangeValues("Method", 1, 1, 1500, 100)

    Rows = len(MethodSheet)
    Cols = len(MethodSheet[0])

    BlockInstancesList: list[list[Block]] = list()

    for ColIndex in range(0, Cols):
        Temp = list()
        for RowIndex in range(0, Rows):
            Name = MethodSheet[RowIndex][ColIndex]

            if Name is None:
                continue

            if type(Name) is not str:
                continue

            if " - (Click Here to Update)" not in Name:
                continue

            Name = Name.replace(" - (Click Here to Update)", "")

            Temp.append(
                BlockObjectCreationWrapper(
                    ExcelInstance, Name, RowIndex + 1, ColIndex + 1
                )
                # Excel is 1 indexed but python is 0 indexed... Dumb!
            )

        if len(Temp) != 0:
            BlockInstancesList.append(Temp)
    # Put blocks in a list of lists that is loaded according to the column of the block

    TempBlockInstancesList = list()
    for BlockInstances in BlockInstancesList:
        Temp = list()
        for BlockInstance in BlockInstances:
            if not isinstance(BlockInstance, SplitPlate):
                Temp.append(BlockInstance)
            else:
                Temp.append(BlockInstance)
                TempBlockInstancesList.append(Temp)
                Temp = list()
        if len(Temp) != 0:
            TempBlockInstancesList.append(Temp)
    BlockInstancesList = TempBlockInstancesList
    # Traverse each list and split the list if a split plate is present.

    Pathways = list()
    for BlockInstances in BlockInstancesList:
        BlockInstance = BlockInstances[0]
        if not isinstance(BlockInstance, Plate):
            raise Exception("Method is not valid!")
        else:
            PlateName = BlockInstance.PlateName.ReadRaw(ExcelInstance)
            if PlateName in Pathways:
                raise Exception("Method is not valid!")
            Pathways.append(PlateName)
    # Check that the starting Block is a Plate and the name is unique in each list

    for BlockInstances in BlockInstancesList:
        BlockInstance = BlockInstances[-1]
        if isinstance(BlockInstance, SplitPlate):

            if (
                BlockInstance.Pathway1Name.ReadRaw(ExcelInstance)
                not in Pathways  # Pathway 1
            ):
                raise Exception("Pathways are not referenced correctly!")
            if (
                BlockInstance.Pathway2Name.ReadRaw(ExcelInstance)
                not in Pathways  # Pathway 2
            ):
                raise Exception("Pathways are not referenced correctly!")
    # Now we need to confirm that a split plate references the correct pathways

    MethodPathways = list()

    # This will effectively connect our blocks into a wonderful tree in order of correct execution :)
    # It will also make complete pathways from start to end. Neato!
    def TraversePathways(
        OutputList, CollectionList, TraversalList, PathwaysList, PreviousBlock, Context
    ):
        for BlockInstance in TraversalList:
            CollectionList.append(BlockInstance)
            BlockInstance.SetParentNode(PreviousBlock)
            BlockInstance.Context = Context
            PreviousBlock = BlockInstance
            if isinstance(BlockInstance, Plate):
                Context += ":" + BlockInstance.PlateName.ReadRaw(ExcelInstance)

            if isinstance(BlockInstance, SplitPlate):
                Pathways = [
                    BlockInstance.Pathway1Name.ReadRaw(ExcelInstance),
                    BlockInstance.Pathway2Name.ReadRaw(ExcelInstance),
                ]
                for Pathway in PathwaysList[:]:
                    if (
                        cast(Plate, Pathway[0]).PlateName.ReadRaw(ExcelInstance)
                        in Pathways
                    ):
                        PathwaysList.remove(Pathway)
                        TraversePathways(
                            OutputList,
                            CollectionList[:],
                            Pathway,
                            PathwaysList,
                            PreviousBlock,
                            Context,
                        )
                return
            # We need to traverse both pathways
        OutputList.append(CollectionList)

    StartingPathway = BlockInstancesList[0]  # Load with something random
    for BlockInstances in BlockInstancesList:
        if BlockInstances[0].GetRow() < StartingPathway[0].GetRow():
            StartingPathway = BlockInstances
    BlockInstancesList.remove(StartingPathway)
    # Find first traversal pathway.

    TraversePathways(
        MethodPathways,
        list(),
        StartingPathway,
        BlockInstancesList,
        None,
        ":__StartingContext__",
    )
    # Now we need to create a seperate list for each pathway... This will need to happen recursively. Kill me now

    for Pathway in MethodPathways:
        if not isinstance(Pathway[-1], Finish):
            raise Exception("All pathways must end with a finish step")
    # Check that each pathway ends with a finish step.

    # LOL IDK
    # Unique
    OrganizedBlocks = list()
    for Pathway in MethodPathways:
        for BlockInstance in Pathway:
            if BlockInstance not in OrganizedBlocks:
                BlockTrackerInstance.ManualLoad(BlockInstance)
                OrganizedBlocks.append(BlockInstance)
    # Now get each block uniquely from the list of blocks. This is relatively in order which is what we want
