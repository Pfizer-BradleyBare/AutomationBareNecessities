from ......Driver.Tools import Command, ExecuteCallback
from ....BaseTempControlDevice import TempControlDevice


def UpdateCurrentTemperatureCallback(CommandInstance: Command, args: tuple):

    TempControlDeviceInstance: TempControlDevice = args[0]
    ResponseInstance = CommandInstance.GetResponse()

    TempControlDeviceInstance.CurrentTemperature = ResponseInstance.GetAdditional()[
        "Temperature"
    ]

    ExecuteCallback(args[1], CommandInstance, args[2])