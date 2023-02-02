from enum import Enum
import SystemConfiguration

START =        0.0              # initial time                   */
STOP  =        840              # terminal (close the door) time */
INFINITY =  (100.0 * STOP)      # must be much larger than STOP  */

class Timer:
    def __init__(self) -> None:
        self.current        = START                           # Current time   
        self.arrival        = [INFINITY] * SystemConfiguration.CLIENTTYPENUM      # Next Arrival time
        self.completation   = [INFINITY] * SystemConfiguration.CLIENTTYPENUM      # Next Completation time
        
    
    def UpdateCurrent(self,val):
        self.current = val


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
        self.node       = [0.0] * nQueue 
        self.queue      = [0.0] * nQueue
        self.service    = [0.0] * nQueue
    
    def UpdateArea(self,globalTime,current,number):
        self.node    += (globalTime - current) * number
        self.queue   += (globalTime - current) * (number - 1)
        self.service += (globalTime - current)