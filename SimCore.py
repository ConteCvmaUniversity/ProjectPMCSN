# File whit Simulation core function
from SystemConf import *
from TimeDef    import Timer,Event,Area
from Utility    import *

class ServerSet:

    def __init__(self,id:int,numServer:int) -> None:
        self.identifier = id    # identifier of the server set
        self.metadata = FactorySetMetadata().getMetadata(id)    # metadata of the set
        self.status = ServerSetStatus() # status rapresentation of the set
        self.channels = numServer         # number of server
        self.area = Area(self.metadata.numberOfQueue) # time integrated number in the node 
        self.events = [Event()] * (CLIENTTYPENUM + self.channels) # Events[0... CLIENTTYPENUM] rapresent arrivals , next events a completation for each server
        self.servers = [Server(self.identifier,self.metadata.serverStateType.IDLE)] * self.channels
        self.timer = Timer()
        
        #TODO definire gli eventi e il tempo

    def asJob(self):
        if self.status.number > 0:
            return True
        else:
            return False
        
    def GetArrivalForAllEvent(self):        
        for elem in list(ClientType):
            i = elem.value["index"]
            self.events[i].time = GetArrival(elem)

class ServerSetStatus:

    def __init__(self) -> None:
        self.clients = [0] * CLIENTTYPENUM              # Number of client for each type in set
        self.servedClients = [0] * CLIENTTYPENUM        # Served number of client for each type
        self.number = 0                                 # number of job in set

    
class Server:
    def __init__(self,ID,initialState) -> None:
        self.setID = ID             # Set identifier
        self.state = initialState   # server state
        self.client = None          # actual served client




class Simulation:
    def __init__(self,simulationTime,seed) -> None:
        # Initialize simulation state
        self.simulationTime = simulationTime
        self.seed = seed
        self.clock = Timer()        # Global clock
        self.reset_initial_state()

    def reset_initial_state(self):
        self.serverSet1 = ServerSet(1, ServerNumber.SET1)  
        self.serverSet2 = ServerSet(2, ServerNumber.SET2)  
        self.serverSet3 = ServerSet(3, ServerNumber.SET3)  
        self.serverSet4 = ServerSet(4, ServerNumber.SET4)  
        self.serverSet5 = ServerSet(5, ServerNumber.SET5) 
        
    
    def startSimulation(self):
        #TODO controllo setup e start del sistema GetArrival()
        self.serverSet1.GetArrivalForAllEvent()

        while(  (self.serverSet1.timer.arrival < self.simulationTime) or    \
                (self.serverSet1.asJob() > 0) or                             \
                (self.serverSet2.asJob() > 0) or                             \
                (self.serverSet3.asJob() > 0) or                             \
                (self.serverSet4.asJob() > 0) or                             \
                (self.serverSet5.asJob() > 0)                                \
             ):
            
            # Select the next event

            self.clock = self.getNextEvent()
        #END WHILE
    
    def getNextEvent(self):
        pass
