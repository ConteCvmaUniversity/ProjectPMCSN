# File whit Simulation core function
from SystemConf import *
from TimeDef    import Timer,Event,Area, EventType
from Utility    import *

class ServerSet:

    def __init__(self,id:int,numServer:int) -> None:
        self.identifier = id    # identifier of the server set
        self.metadata = FactorySetMetadata().getMetadata(id)    # metadata of the set
        self.status = ServerSetStatus() # status rapresentation of the set
        self.channels = numServer       # number of server
        self.area = Area(self.metadata.numberOfQueue) # time integrated number in the node 
        self.events = [] # List of event in set can be arrival or a server completation 
        self.servers = [Server(self.identifier,i,self.metadata.serverStateType.IDLE)for i in range(0,self.channels)] 
        self.timer = Timer()
        
        #TODO definire gli eventi e il tempo

    def hasJob(self) -> bool:
        if self.status.number > 0:
            return True
        else:
            return False
        
    def GetArrivalForAllEvent(self):        
        for elem in list(ClientType):
            self.AddEvent(GetArrival(elem,self.identifier))
        self.UpdateTimer() # update information about next arrival
    
    def AddEvent(self,event:Event):
        self.events = sorted(self.events.append(event) , key=lambda event:event.time)
        self.UpdateTimer() #TODO vedere se serve o rimuovere
    
    def UpdateTimer(self):
        ne = self.getNextEvent()
        if (ne.typ == EventType.ARRIVAL):
            self.timer.arrival = ne.time
        elif (ne.typ == EventType.COMPLETATION):
            self.timer.completation = ne.time

    def NextEventTime(self):
        return self.events[0].time
    
    def getNextEvent(self)->Event:
        return self.events[0]
    
    def popNextEvent(self)->Event:
        ret = self.events.pop(0)
        self.UpdateTimer()
        return ret
            

class ServerSetStatus:

    def __init__(self) -> None:
        self.clients = [0] * CLIENTTYPENUM              # Number of client for each type in set
        self.servedClients = [0] * CLIENTTYPENUM        # Served number of client for each type
        self.number = 0                                 # number of job in set

    
class Server:
    def __init__(self,ID,id,initialState:ServerStateType) -> None:
        self.setID = ID             # Set identifier
        self.identifier = id        # Server identifier
        self.state = initialState   # server state
        self.client = None          # actual served client




class Simulation:
    def __init__(self,simulationTime,seed) -> None:
        # Initialize simulation state
        self.simulationTime = simulationTime
        self.seed = seed
        self.clock = Timer()        # Global clock
        self.serverSets = []
        self.next = None            # Next Event
        self.reset_initial_state()

    def reset_initial_state(self):
        self.serverSets.append( ServerSet(1, ServerNumber.SET1) ) 
        self.serverSets.append( ServerSet(2, ServerNumber.SET2) ) 
        self.serverSets.append( ServerSet(3, ServerNumber.SET3) ) 
        self.serverSets.append( ServerSet(4, ServerNumber.SET4) ) 
        self.serverSets.append( ServerSet(5, ServerNumber.SET5) )
        
    
    def startSimulation(self):
        #TODO controllo setup e start del sistema GetArrival()
        self.serverSets[0].GetArrivalForAllEvent()

        #TODO controllare prima condizione
        while(  (self.serverSets[0].timer.arrival < self.simulationTime) or     \
                (self.serverSets[0].hasJob() > 0) or                             \
                (self.serverSets[1].hasJob() > 0) or                             \
                (self.serverSets[2].hasJob() > 0) or                             \
                (self.serverSets[3].hasJob() > 0) or                             \
                (self.serverSets[4].hasJob() > 0)                                \
             ):
            
            # Select the next event
            self.next = self.getNextEvent()

            # Based on next event type select the right identifier
            setSelector = self.next.identifier if self.next.typ == EventType.ARRIVAL else self.next.identifier[0] # identifier of set from 1 to 5
            # TODO vedi commento dopo setSelector-=1 # decrement for selection 
            # TODO bisogna creare la logica per ogni set decidere se farla qui con degli if (soluzione piu semplice)
            #oppure mettere una funzione nei metadata dei set da poter invocare ... da studiare

        #END WHILE
    
    def getNextEvent(self) -> Event:
        
        for elem in self.serverSets:
            pass
