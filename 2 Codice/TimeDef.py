from enum import Enum
import SystemConfiguration

# Default value
START =        0.0              # initial time                   */
STOP  =        420              # terminal (close the door) time */
INFINITY =  (1000 * STOP)       # must be much larger than STOP  */

class Timer:
    def __init__(self) -> None:
        self.current        = START                           # Current time   
        self.arrival        = [INFINITY] * SystemConfiguration.CLIENTTYPENUM      # Last Arrival time
        self.completation   = [INFINITY] * SystemConfiguration.CLIENTTYPENUM      # Last Completation time
        
    
    def UpdateCurrent(self,val):
        self.current = val
    
    def LastArrival(self):
        cp = self.arrival.copy()
        while INFINITY in cp : cp.remove(INFINITY)
        return max(cp)

    def LastCompletation(self):
        cp = self.arrival.copy()
        while INFINITY in cp : cp.remove(INFINITY)
        return max(cp)


class EventType(Enum):
    ARRIVAL         = 0
    COMPLETATION    = 1


class Event:
    def __init__(self,typ:EventType,id,client,time) -> None:
        self.time = time        # Occurence of event
        self.typ = typ          # Event type
        self.client = client    # Client 
        self.identifier = id    # Identifier of set and server if completation


    # TODO creare una funzione di init in base al tipo di evento?
    




# statistics for population
class Area:
    def __init__(self,nQueue) -> None:
        self.queue          = nQueue
        self.clients        = 0.0 
        self.queue          = 0.0
        self.service        = 0.0

        #self.node       = [0.0] * nQueue 
        #self.queue      = [0.0] * nQueue
        #self.service    = [0.0] * nQueue
    
    def UpdateArea(self,globalTime,current,number,service):
        self.clients    += (globalTime - current) * number 
        self.queue      += (globalTime - current) * (number - service) 
        self.service    += (globalTime - current) * service

        #for i in range(0,self.queue):
            #self.node    [i] += (globalTime - current) * number 
            #self.queue   [i] += (globalTime - current) * (number - 1) sbagliato
            #self.service [i] += (globalTime - current) sbagliato
    
    def resetArea(self):
        self.clients        = 0.0 
        self.queue          = 0.0
        self.service        = 0.0