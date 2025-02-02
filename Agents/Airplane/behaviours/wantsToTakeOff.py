from spade.behaviour import TimeoutBehaviour
from spade.message import Message

import sys, platform, datetime, jsonpickle

if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
elif platform.system() == "Windows":
    sys.path.append("..\\..")
else:
    print("Unsupported operating system")

from MessagesProtocol.RequestFromAirplane import RequestFromAirplane
from MessagesProtocol.DashboardAirplaneMessage import DashboardAirplaneMessage, DashboardAirplaneMessageType, AirplaneInfo
from GlobalTypes.Types import RequestType
from Conf import Conf

class WantsToTakeOffBehaviour(TimeoutBehaviour):

    async def on_start(self):
        print("[Airplane] starting WantsToTakeOffBehaviour")

    async def run(self):
        msg = Message(to="controlTower@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "request")

        requestToTakeOff = RequestFromAirplane(
            typeRequest=RequestType.TAKEOFF,
            id=self.agent.airplaneID,
            spotType=self.agent.typeTransport,
            status=self.agent.status,
            airlineID=self.agent.airline,
            requestTime=datetime.datetime.now(), 
            priority=self.agent.priority,
            station=self.agent.stationPark
        )
        msg.body = jsonpickle.encode(requestToTakeOff)
        await self.send(msg)

        ############ Update Dashboard ############
        msg = Message(to="dashboardAirplane@" + Conf().get_openfire_server())
        msg.set_metadata("performative", "inform")
        bodyMessage:DashboardAirplaneMessage = DashboardAirplaneMessage(
            type=DashboardAirplaneMessageType.UPDATE,
            airplaneInfo=AirplaneInfo(
                id=self.agent.airplaneID,
                status=self.agent.status,
                airlineID=self.agent.airline
            )
        )
        msg.body = jsonpickle.encode(bodyMessage)
        await self.send(msg)