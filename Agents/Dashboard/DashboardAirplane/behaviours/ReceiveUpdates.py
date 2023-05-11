from spade.behaviour import CyclicBehaviour
import jsonpickle
from MessagesProtocol.DashboardAirplaneMessage import DashboardAirplaneMessage
from GlobalTypes.Types import DashboardAirplaneMessageType, StatusType
import customtkinter

class ReceiveUpdatesBehaviour(CyclicBehaviour):
    async def on_start(self):
        print("[DashboardAirplane] Starting ReceiveUpdatesBehaviour")

    async def run(self):
        msg = await self.receive(timeout=100) 
        if msg:
            dashboardAirplane:DashboardAirplaneMessage = jsonpickle.decode(msg.body)

            # add airplane in airplanes list
            if dashboardAirplane.type == DashboardAirplaneMessageType.CREATE:

                labelId = customtkinter.CTkLabel(master=self.agent.view.airplanesTable)
                labelId.grid(row=self.agent.rowIndex, column=0, padx=20, pady=(0,10))
                labelId.configure(text=dashboardAirplane.airplaneInfo.id)

                """
                # add button to activate airplane actions (land, request to fly, etc)
                if dashboardAirplane.airplaneInfo.status == StatusType.IN_STATION: 
                    labelAction = customtkinter.CTkButton(master=self.agent.view.airplanesTable, command=lambda airplaneID=dashboardAirplane.airplaneInfo.id: self.agent.view.requestToTakeOff(airplaneID))
                    labelAction.grid(row=self.agent.rowIndex, column=1, padx=20, pady=(0,10))
                    labelAction.configure(text="Take Off")
                elif dashboardAirplane.airplaneInfo.status == StatusType.FLYING:
                    labelAction = customtkinter.CTkButton(master=self.agent.view.airplanesTable, command=lambda airplaneID=dashboardAirplane.airplaneInfo.id: self.agent.view.requestToLand(airplaneID))
                    labelAction.grid(row=self.agent.rowIndex, column=1, padx=20, pady=(0,10))
                    labelAction.configure(text="Land")
                else:
                    labelAction = customtkinter.CTkLabel(master=self.agent.view.airplanesTable, text="--None--")
                    labelAction.grid(row=self.agent.rowIndex, column=1, padx=20, pady=(0,10))
                """

                # add label entry for airplane STATUS
                labelStatus = customtkinter.CTkLabel(master=self.agent.view.airplanesTable, text=self.agent.view.airplaneStatus(dashboardAirplane.airplaneInfo.status))
                labelStatus.grid(row=self.agent.rowIndex, column=1, padx=10, pady=(0,10), sticky="ew")
                
                # update rowIndex for next label
                self.agent.rowIndex += 1

                # keep STATUS to eventually updates some value in this label
                self.agent.view.labels[dashboardAirplane.airplaneInfo.id] = {}
                self.agent.view.labels[dashboardAirplane.airplaneInfo.id]["status"] = labelStatus

            elif dashboardAirplane.type == DashboardAirplaneMessageType.UPDATE:
                # self.agent.view.labels[dashboardAirplane.airplaneInfo.id] 
                self.agent.view.labels[dashboardAirplane.airplaneInfo.id]["status"].configure(text=self.agent.view.airplaneStatus(dashboardAirplane.airplaneInfo.status))