# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:65535/Command/Respond

import web

from ....Server.Globals.HandlerRegistry import GetDriverHandler
from ....Server.Tools.Parser import Parser
from ...Tools.Command.CommandTracker import CommandTracker
from ...Tools.Command.Response.Response import Response as CommandResponse

urls = ("/Driver/Respond", "ABN.Source.Driver.Handler.Endpoints.Respond.Respond")


class Respond:
    def POST(self):
        ParserObject = Parser("Driver Respond", web.data())

        CommandTrackerInstance: CommandTracker = (
            GetDriverHandler().CommandTrackerInstance  # type:ignore
        )

        if CommandTrackerInstance.GetNumObjects() == 0:
            ParserObject.SetAPIReturn(
                "Message", "Command not currently waiting on response."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        if not ParserObject.IsValid(["State", "Message", "Request Identifier"]):
            Response = ParserObject.GetHTTPResponse()
            return Response
        # preliminary check. We will check again below

        RequestID = ParserObject.GetAPIData()["Request Identifier"]

        if not CommandTrackerInstance.IsTracked(RequestID):
            ParserObject.SetAPIReturn(
                "Message", "There is not a command with that ID waiting."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        CommandInstance = CommandTrackerInstance.GetObjectByName(RequestID)

        if CommandInstance.GetResponse() is not None:
            ParserObject.SetAPIReturn(
                "Message", "Command already has a reponse. This should never happen."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        ExpectedResponseKeys = CommandInstance.GetResponseKeys()

        if not ParserObject.IsValid(
            ["State", "Message", "Request Identifier"] + ExpectedResponseKeys
        ):
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Checking is valid is more complex than normal. Each command has expected keys. We need to add that to the normal keys to confirm the response is valid

        Additional = dict()
        for Key in ExpectedResponseKeys:
            Additional[Key] = ParserObject.GetAPIData()[Key]
        # Create dict that houses the expected keys so we can create the response object

        CommandInstance.ResponseInstance = CommandResponse(
            ParserObject.GetAPIData()["State"],
            ParserObject.GetAPIData()["Message"],
            Additional,
        )
        # boom
        CommandInstance.ResponseEvent.set()
        # Add response then release threads waiting for a response

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Response appended to command.")

        Response = ParserObject.GetHTTPResponse()
        return Response
