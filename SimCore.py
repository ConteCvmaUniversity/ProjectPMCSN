# File whit Simulation core function
from SystemConf import *
from TimeDef    import Timer,Event,Area, EventType
from Utility    import *
from Errors     import SimulationStop,NoServerIdle, AllQueueEmpty , SimulationError

class ServerSet:

    def __init__(self,id:int,numServer:int) -> None:
        self.identifier = id    # identifier of the server set
        self.metadata = FactorySetMetadata().getMetadata(id)    # metadata of the set
        self.status = ServerSetStatus() # status rapresentation of the set
        self.channels = numServer       # number of server
        self.area = Area(self.metadata.numberOfQueue) # time integrated number in the node 
        self.events = [] # List of event in set can be arrival or a server completation 
        self.servers = [Server(self.identifier,i)for i in range(0,self.channels)] 
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
            self.AddEvent(ev)
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
    
    # Function that add client to set status (increment client.type number, number)
    def AddClient(self,cl:ClientType):
        self.status.AddClient(cl)
    
    def RemoveClient(self,cl:ClientType):
        self.status.RemoveClient(cl)
    
    def CompletationEvent(self,cl:ClientType):
        self.status.IncrementCompleted(cl)
        self.status.RemoveClient(cl)
        

    def GetService(self,client,id,serverState):
        
        ev = GetService(self.timer.current,client,id,serverState)
        self.AddEvent(ev)
        self.status.AddServedClient(client)
    
    def GetIdleServerId(self):
        if (self.status.number <= self.channels):
            i = 0
            while (self.servers[i].state != ServerStateType.IDLE):
                i+=1
            return i
        else:
            return -1
    
    
    # This function does not check the server status but schedule a queued job
    def ScheduleJob(self,serverId,priority = False):
        # TODO tracciamo in qualche modo il tempo di lavoro che viene schedulato??
        server:Server = self.servers[serverId]
        try:
            if (priority):
                client = self.status.GetFirstClientQueueNotEmptyPriority()
            else:
                client = self.status.GetFirstClientQueueNotEmpty()
            serverNewState = self.metadata.clientToSStateMap[client]
            if serverNewState == -1:
                raise SimulationError("Server {} receive a client not admitted {}".format((self.identifier,serverId),client))
            
            self.GetService(client,server.GetServerIdentifier(),serverNewState)
            #Update server state
            server.UpdateState(serverNewState,client)

        except AllQueueEmpty:
            # No job to schedule reset Server Status
            server.ResetServer()
    
    

            

class ServerSetStatus:

    def __init__(self) -> None:
        self.clients = [0] * CLIENTTYPENUM              # Number of client for each type in set
        self.servedClients = [0] * CLIENTTYPENUM        # Served number of client for each type
        self.number = 0                                 # Number of job in set
        self.completed = [0] * CLIENTTYPENUM            # Number of completed job
    
    def AddClient(self,cl:ClientType):
        self.clients[cl.value["index"]]   += 1
        self.number                 += 1
    
    def AddServedClient(self,cl:ClientType):
        self.servedClients[cl.value["index"]] += 1
    
    def RemoveClient(self,cl:ClientType):
        self.clients[cl.value["index"]]   -= 1
        self.number                 -= 1
    
    def IncrementCompleted(self,cl:ClientType):
        self.completed[cl.value["index"]] += 1

    # No priority defined for select the empty queue
    def GetFirstClientQueueNotEmpty(self) -> ClientType:
        for typ in list(ClientType):
            if (self.__clientInQueue(typ) > 0 ) :
                return typ
        # All queue are empty    
        raise AllQueueEmpty()
    
    # Ad hoc function for payment type selection
    def GetFirstClientQueueNotEmptyPriority(self) -> ClientType:
        priority_list   = filter(lambda item: item.value["pay"]== ClientPV.GRUPPO ,list(ClientType))
        second_list     = filter(lambda item: item.value["pay"]== ClientPV.SINGOLO ,list(ClientType))

        for typ in priority_list:
            if (self.__clientInQueue(typ) > 0 ) :
                return typ
        
        for typ in second_list:
            if (self.__clientInQueue(typ) > 0 ) :
                return typ

        # All queue are empty    
        raise AllQueueEmpty()   
        


    def __clientInQueue(self,cl:ClientType):
        idx = cl.value["index"]
        ret = self.clients[idx] - self.servedClients[idx]
        return ret

    
class Server:
    def __init__(self,IDset,id,) -> None:
        self.setID = IDset                  # Set identifier
        self.identifier = id                # Server identifier
        self.state = ServerStateType.IDLE   # server state
        self.client = None                  # actual served client
    
    def UpdateState(self,state,client):
        self.state = state
        self.client = client
    
    def GetServerIdentifier(self):
        return (self.setID,self.identifier)
    
    def ResetServer(self):
        self.state = ServerStateType.IDLE
        self.client = None




class Simulation:
    def __init__(self,seed) -> None:
        # Initialize simulation state
        
        self.seed = seed
        self.clock = Timer()        # Global clock TODO serve il global clock
        self.continueSim = True
        self.serverSets = []
        self.next = None            # Next Event
        self.discarded = 0
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

        #TODO plant seeds??

        while(  (continueSim) or                        \
                (self.serverSets[0].hasJob() > 0) or    \
                (self.serverSets[1].hasJob() > 0) or    \
                (self.serverSets[2].hasJob() > 0) or    \
                (self.serverSets[3].hasJob() > 0) or    \
                (self.serverSets[4].hasJob() > 0)       \
             ):
            
            # First setup next arrival

            # Select the next event
            self.next = self.__getNextEvent()

            nextIsArrival:bool = self.next.typ == EventType.ARRIVAL
            # Based on next event type select the right identifier
            setSelector = self.next.identifier if nextIsArrival else self.next.identifier[0] # identifier of set from 1 to 5
            client = self.next.client

            selectedSet :ServerSet = self.serverSets[setSelector - 1]   # set of the event ATTETION setSelector start from 1
            selectedSet.UpdateSetArea(self.next.time)                   # update set area
            selectedSet.UpdateCurrentTime(self.next.time)               # update current value in set timer

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
                    # If a server is free
                    idleId = selectedSet.GetIdleServerId()
                    if (idleId != -1):
                        # A free server it's available and at least one queue as job (we have an arrival)
                        selectedSet.ScheduleJob(idleId)
                        
                
                else:
                    # Completation Event
                    selectedSet.CompletationEvent(client)
                    serverId = self.next.identifier[1]
                    # Try to schedule new work on this server
                    selectedSet.ScheduleJob(serverId)

                    # A completation in this set generate an event for set 2
                    # First generate a discard probability
                    discardProb = GetRandom(0)

                    if (discardProb > probabilityDiscardSet1):
                        # schedule an arrival for set 2
                        self.serverSets[1].GetArrivalByClient(client)
                    else:
                        # discard job
                        self.discarded += 1

            # END SET 1     
                
            elif (setSelector == 2):
                #Event for set 2

                # Is an arrival 
                if nextIsArrival:
                    # Increment clients
                    selectedSet.AddClient(client)

                    # Schedule the arrival and generate completation event
                    # If a server is free
                    idleId = selectedSet.GetIdleServerId()
                    if (idleId != -1):
                        # A free server it's available and at least one queue as job (we have an arrival)
                        selectedSet.ScheduleJob(idleId)
                else:
                    # Completation event
                    selectedSet.CompletationEvent(client)
                    serverId = self.next.identifier[1]
                    selectedSet.ScheduleJob(serverId)

                    clientType = client.value["type"]
                    # A completation in this set can trigger a new arrival in the next sets based on client type
                    if (clientType == ClientTV.SOCIO):
                        # Generate an arrival for set 5 
                        self.serverSets[4].GetArrivalByClient(client)
                    elif (clientType == ClientTV.NEWMODULO):
                        # Generate an arrival for set 4
                        self.serverSets[3].GetArrivalByClient(client)
                    elif (( clientType == ClientTV.NEWMODULO ) or ( clientType == ClientTV.NEWMODULO )):
                        # Generate an arrival for set 3
                        self.serverSets[2].GetArrivalByClient(client)

            # END SET 2

            elif (setSelector == 3):
                #Event for set 3

                # Is an arrival 
                if nextIsArrival:
                    # Increment clients
                    selectedSet.AddClient(client)

                    # Schedule the arrival and generate completation event
                    # If a server is free
                    idleId = selectedSet.GetIdleServerId()
                    if (idleId != -1):
                        # A free server it's available and at least one queue as job (we have an arrival)
                        selectedSet.ScheduleJob(idleId)
                else:
                    # Completation event
                    selectedSet.CompletationEvent(client)
                    serverId = self.next.identifier[1]
                    selectedSet.ScheduleJob(serverId)

                    # All completation for this set only generate an arrival for set 4
                    self.serverSets[3].GetArrivalByClient(client)

            
            # END SET 3

            elif (setSelector == 4):
                #Event for set 4
                # Is an arrival 
                if nextIsArrival:
                    # Increment clients
                    selectedSet.AddClient(client)

                    # Schedule the arrival and generate completation event
                    # If a server is free
                    idleId = selectedSet.GetIdleServerId()
                    if (idleId != -1):
                        # A free server it's available and at least one queue as job (we have an arrival)
                        selectedSet.ScheduleJob(idleId)
                else:
                    # Completation event
                    selectedSet.CompletationEvent(client)
                    serverId = self.next.identifier[1]
                    selectedSet.ScheduleJob(serverId)

                    # All completation for this set only generate an arrival for set 4
                    self.serverSets[3].GetArrivalByClient(client)
            
            # END SET 4

            elif (setSelector == 5):
                #Event for set 5
                # Is an arrival 
                if nextIsArrival:
                    # Increment clients
                    selectedSet.AddClient(client)

                    # Schedule the arrival and generate completation event
                    # If a server is free
                    idleId = selectedSet.GetIdleServerId()
                    if (idleId != -1):
                        # A free server it's available and at least one queue as job (we have an arrival)
                        selectedSet.ScheduleJob(idleId,priority=True)
                else:
                    # Completation event
                    selectedSet.CompletationEvent(client)
                    serverId = self.next.identifier[1]
                    selectedSet.ScheduleJob(serverId,priority=True)

            # END SET 5

            else:
                raise SimulationError("Set Selector not in range val:{}".format(setSelector))

            # if debug is on print update of simulation

            if __debug__ :
                self.printDebugUpdate()           

        #END WHILE
    
    # This function search next event from events list of the sets and pop it
    def __getNextEvent(self,priority=False) -> Event:
        #TODO da fare la funzione
        for elem in self.serverSets:
            pass

    

    def printDebugUpdate():
        #TODO
        pass
