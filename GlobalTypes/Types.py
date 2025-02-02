class SpotType:
    MERCHANDISE = 1
    COMMERCIAL = 2

class RequestType:
    LAND = 1
    TAKEOFF = 2

class StatusType:
    IN_STATION = 1
    FLYING = 2
    LANDING = 3
    WAITING_TAKEOFF = 4
    WAITING_LAND = 5
    TO_ANOTHER_AIRPORT = 6
    TAKING_OFF = 7

class Priority:
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class DashboardAirlineMessageType:
    NEGOTIATION = 1
    INFO = 2
    UPDATE = 3

class DashboardAirplaneMessageType:
    CREATE = 1
    UPDATE = 2

class DashboardRunwayMessageType:
    INFO = 1
    UPDATE = 2

class DashboardControlTowerMessageType:
    AIRPLANE_REQUEST = 1
    AIRPLANE_IN_QUEUE = 2
    PERMISSION_DENIED = 3
    PERMISSION_ACCEPTED = 4
    NEW_SPOTS = 5
    AVG_TIME_IN_QUEUE = 6
    TO_ANOTHER_AIRPORT = 7

class DashboardStationMessageType:
    INFO = 1
    UPDATE = 2

class NegotiationStatus:
    PROPOSE = 1
    SUCCESS = 2
    FAIL = 3