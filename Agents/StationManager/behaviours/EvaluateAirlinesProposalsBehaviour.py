from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from MessagesProtocol.DashboardAirlines import DashboardAirlines
from GlobalTypes.Types import DashboardAirlineUpdate, NegotiationStatus
import jsonpickle
from Conf import Conf

class EvaluateAirlinesProposalsBehaviour(PeriodicBehaviour):
    async def on_start(self):
        print("Starting Evaluate Airlines Proposals Behaviour . . .")

    async def run(self):

        # Sort proposals by price per spot
        proposalsByPrice = sorted(self.agent.airlinesProposals, key=lambda proposal: proposal["proposal"].price_per_spot)
        for proposal in proposalsByPrice:

            # Verify if Airline can buy all the spots required
            airlineCanBuy = self.agent.checkIfAirlineCanBuy(
                proposal["proposal"].n_spots,
                proposal["proposal"].spotType
            )

            if airlineCanBuy:

                # Change Stations Spots State
                self.agent.buySpots(
                    proposal["proposal"].n_spots,
                    proposal["proposal"].spotType,
                    proposal["proposal"].airlineID,
                )

                ###### Send positive feedback for Airline ######
                msg = Message(to=str(proposal["agentID"]))
                msg.set_metadata("performative", "agree")
                msg.body = "Proposal of spots accepted. " + str(proposal["proposal"].n_spots) + " spots bought."
                await self.send(msg)

                ############### Update Dashboard ###############
                msg = Message(to="dashboardAirline@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")
                bodyMessage:DashboardAirlines = DashboardAirlines(
                    type=DashboardAirlineUpdate.NEGOTIATION,
                    negotiationStatus=NegotiationStatus.SUCCESS,
                    negotiationText="Accepted proposal by " + proposal["proposal"].airlineID
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)
            else:
                ###### Send negative feedback for Airline ######
                msg = Message(to=str(proposal["agentID"]))
                msg.set_metadata("performative", "reject-proposal")
                msg.body = "Proposal of spots was not accepted. " + str(proposal["proposal"].n_spots) + " spots not available to buy."
                await self.send(msg)

                ############### Update Dashboard ###############
                msg = Message(to="dashboardAirline@" + Conf().get_openfire_server())
                msg.set_metadata("performative", "inform")
                bodyMessage:DashboardAirlines = DashboardAirlines(
                    type=DashboardAirlineUpdate.NEGOTIATION,
                    negotiationStatus=NegotiationStatus.FAIL,
                    negotiationText="Refuse proposal by " + proposal["proposal"].airlineID
                )
                msg.body = jsonpickle.encode(bodyMessage)
                await self.send(msg)
        
        # Remove all previous proposals
        self.agent.airlinesProposals = []