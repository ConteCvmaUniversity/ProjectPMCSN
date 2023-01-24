# File whit Simulation core function
from SystemConf import *
from TimeDef    import Timer

class ServerSet:

    def __init__(self,id:int,numServ:int) -> None:
        self.identifier = id
        self.metadata = FactorySetMetadata().getMetadata(id)
        
        self.clients = [0] * CLIENTTYPENUM 
        
        self.channel = numServ  # represent number of server
        self.number = 0         # number of job in service 
        self.area = 0.0
        self.servers = [Server(self.identifier,self.metadata.serverStateType.IDLE)] * self.channel 
        self.timer = Timer(self.metadata.numberOfQueue)
        #TODO definire gli eventi
    
class Server:
    def __init__(self,ID,initialState) -> None:
        self.setID = ID
        self.state = initialState  # in example x(t)
        self.client = None

class Simulation:
    def __init__(self,simulationTime,seed) -> None:
        # Initialize simulation state
        self.simulationTime = simulationTime
        self.seed = seed
        self.serverSet1 = ServerSet(1, ServerNumber.SET1)
        self.reset_initial_state()

    def reset_initial_state(self):
        self.serverSet1 = ServerSet(1, ServerNumber.SET1)  
        self.serverSet2 = ServerSet(2, ServerNumber.SET2)  
        self.serverSet3 = ServerSet(3, ServerNumber.SET3)  
        self.serverSet4 = ServerSet(4, ServerNumber.SET4)  
        self.serverSet5 = ServerSet(5, ServerNumber.SET5) 
        
    
    def startSimulation(self):
        while(  (self.serverSet1.timer.arrival < self.simulationTime) or    \
                (self.serverSet1.number > 0) or                             \
                (self.serverSet2.number > 0) or                             \
                (self.serverSet3.number > 0) or                             \
                (self.serverSet4.number > 0) or                             \
                (self.serverSet5.number > 0)                                \
             ):
            
            pass

