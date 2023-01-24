# File whit Simulation core function
from SystemConf import *
from TimeDef    import Timer

class ServerSet:

    def __init__(self,id:int,numServ:int) -> None:
        self.identifier = id
        self.metadata = FactorySetMetadata().getMetadata(id)
        
        
        self.channel = numServ # represent number of server
        self.number = 0
        
        self.events = [self.metadata.serverStateType.IDLE] * self.channel
        self.timer = Timer(self.metadata.numberOfQueue)

class Simulation:
    def __init__(self,simulationTime) -> None:
        # Initialize simulation state
        self.simulationTime = simulationTime
        self.reset_initial_state()

    def reset_initial_state(self):
        self.clients = [0] * CLIENTTYPENUM
        self.serverSet1 = ServerSet(1, ServerNumber.SET1)  
        self.serverSet2 = ServerSet(2, ServerNumber.SET2)  
        self.serverSet3 = ServerSet(3, ServerNumber.SET3)  
        self.serverSet4 = ServerSet(4, ServerNumber.SET4)  
        self.serverSet5 = ServerSet(5, ServerNumber.SET5) 
    
    def startSimulation(self):
        while((self.serverSet1.timer.arrival < self.simulationTime)):
            pass

