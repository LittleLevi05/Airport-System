from typing import Dict, List
import sys, platform
if platform.system() == "Darwin":  # macOS
    sys.path.append("../")
    sys.path.append("../../")
elif platform.system() == "Windows":
    sys.path.append("..") 
    sys.path.append("..\\..") 
else:
    print("Unsupported operating system")
from spade.agent import Agent
from spade.template import Template
from GlobalTypes.Coord import Coord
from .behaviours.ReceiveSpotQueryBehaviour import ReceiveSpotQueryBehaviour
from .behaviours.InformDashboardInitRunway import InformDashboardInitRunway
from .behaviours.UpdateRunwayAvailabilityBehaviour import UpdateRunwayAvailabilityBehaviour

class Runway():
    def __init__(self, id: str, coord: Coord, available: bool) -> None:
        '''
            id: identificador único da pista
            coord: localização da pista
            spots_available: número de pistas disponíveis
        '''
        self.id: str = id
        self.coord: Coord = coord
        self.available: bool = available

class RunwayManagerAgent(Agent):
    async def setup(self):
        receiveSpotsQueryBehaviour = ReceiveSpotQueryBehaviour()
        informDashBoardInitRunway = InformDashboardInitRunway()
        updateRunwayAvailability = UpdateRunwayAvailabilityBehaviour()

        template = Template()
        template.set_metadata("performative","query-if")
        template2 = Template()
        template2.set_metadata("performative", "inform-ref")

        self.add_behaviour(receiveSpotsQueryBehaviour,template)
        self.add_behaviour(informDashBoardInitRunway)
        self.add_behaviour(updateRunwayAvailability,template2)

    def __init__(self, agent_name, password, nRunways = None):
        super().__init__(agent_name,password)
        self.runways: Dict[str,Runway] = {}
        if nRunways is not None:
            for i in range(0,nRunways):
                self.addRunway(Runway(
                    id = 'Runway_' + str(i),
                    coord = Coord(),
                    available = True
                ))

    def addRunway(self, runway: Runway):
        if runway.id in self.runways:
            raise ValueError("This identifier was already taken by another runway")
        self.runways[runway.id] = runway

    def getRunwaysAvailable(self) -> List[Runway]:
        runwaysAvailable: List[Runway] = []
        for runway in self.runways:
            if self.runways[runway].available:
                runwaysAvailable.append(self.runways[runway])
        return runwaysAvailable
  
    def updateRunwayAvailability(self,isAvailable,runwayID):
        self.runways[runwayID].available = isAvailable