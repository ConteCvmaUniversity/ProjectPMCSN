# File whit Simulation core function
from SystemConf import *
from TimeDef    import Timer,Event,Area, EventType
from Utility    import *
from Errors     import SimulationStop

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
    
    def GetArrivalByClient(self,cl:ClientType):
        # A new arrival can by added only if it's time is not over the limit
        ev = GetArrival(cl,self.identifier)
        if ev.time > self.metadata.simulationTime:
            self.AddEvent(GetArrival(cl,self.identifier))
            self.UpdateTimer()
        else:
            raise SimulationStop("New Arrival time largen than simulation Time val:{}".format(ev.time))
        
    def AddEvent(self,event:Event):
        self.events = sorted(self.events.append(event) , key=lambda event:event.time)
        self.UpdateTimer() #TODO vedere se serve o rimuovere
    
    def UpdateTimer(self):
        ne = self.getNextEvent()
        if (ne.typ == EventType.ARRIVAL):
            self.timer.arrival = ne.time
        elif (ne.typ == EventType.COMPLETATION):
            self.timer.completation = ne.time
    
    def UpdateSetArea(self,globalTime):
        if self.status.number > 0:
            self.area.UpdateArea(globalTime,self.timer.current)

    def UpdateCurrentTime(self,time):
        # TODO servono controlli su time?
        self.timer.UpdateCurrent(time)

    def NextEventTime(self):
        return self.events[0].time
    
    def getNextEvent(self)->Event:
        return self.events[0]
    
    def popNextEvent(self)->Event:
        ret = self.events.pop(0)
        self.UpdateTimer()
        return ret
    
    def AddClient(self,cl:ClientType):
        self.status.AddClient(cl)
    
    def GetIdleServerId(self):
        # TODO completare la funzione
        for server in self.servers:
            pass
            

class ServerSetStatus:

    def __init__(self) -> None:
        self.clients = [0] * CLIENTTYPENUM              # Number of client for each type in set
        self.servedClients = [0] * CLIENTTYPENUM        # Served number of client for each type
        self.number = 0                                 # number of job in set
    
    def AddClient(self,cl:ClientType):
        self.clients[cl["index"]]   += 1
        self.number                 += 1

    
class Server:
    def __init__(self,ID,id,initialState:ServerStateType) -> None:
        self.setID = ID             # Set identifier
        self.identifier = id        # Server identifier
        self.state = initialState   # server state
        self.client = None          # actual served client




class Simulation:
    def __init__(self,seed) -> None:
        # Initialize simulation state
        
        self.seed = seed
        self.clock = Timer()        # Global clock TODO serve il global clock
        self.continueSim = True
        self.serverSets = []
        self.next = None            # Next Event
        #TODO remove ? self.current = None         # Current Event
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

        while(  (continueSim) or                        \
                (self.serverSets[0].hasJob() > 0) or    \
                (self.serverSets[1].hasJob() > 0) or    \
                (self.serverSets[2].hasJob() > 0) or    \
                (self.serverSets[3].hasJob() > 0) or    \
                (self.serverSets[4].hasJob() > 0)       \
             ):
            
            # First setup next arrival

            # Select the next event
            self.next = self.getNextEvent()
            nextIsArrival:bool = self.next.typ == EventType.ARRIVAL
            # Based on next event type select the right identifier
            setSelector = self.next.identifier if nextIsArrival else self.next.identifier[0] # identifier of set from 1 to 5
            client = self.next.client

            # TODO vedi commento dopo setSelector-=1 # decrement for selection 
            # TODO bisogna creare la logica per ogni set decidere se farla qui con degli if (soluzione piu semplice)
            #oppure mettere una funzione nei metadata dei set da poter invocare ... da studiare
            selectedSet :ServerSet = self.serverSets[setSelector]   # set of the event
            selectedSet.UpdateSetArea(self.next.time)               # update set area
            selectedSet.UpdateCurrentTime(self.next.time)           # update current value in set timer

            if (setSelector == 1):
                # Event for set 1

                # Is an arrival 
                if nextIsArrival:
                    # Increment clients
                    selectedSet.AddClient(client)

                    # The function rise SimulationStop if the new Arrival overflow limit time
                    try:
                        selectedSet.GetArrivalByClient(client)
                    except SimulationStop as stop:
                        # SetUp stop simulation
                        # TODO controllare se basta aggiornare solo questa variabile
                        print("Simulation Stop raised from GetArrivalByClient: {}".format(stop))
                        continueSim = False
                    
                    # Schedule the arrival and generate completation event
                    # TODO
                else:
                    # TODO sto gestendo un completamento
                    pass

            # END SET 1     
                
            elif (setSelector == 2):
                #Event for set 2
                pass
            
            elif (setSelector == 3):
                #Event for set 3
                pass
            
            elif (setSelector == 4):
                #Event for set 4
                pass
            
            elif (setSelector == 5):
                #Event for set 5
                pass

            else:
                pass

        #END WHILE
    
    # This function search next event from events list of the sets and pop it
    def getNextEvent(self) -> Event:
        
        for elem in self.serverSets:
            pass
