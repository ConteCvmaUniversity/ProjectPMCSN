
START =        0.0              # initial time                   */
STOP  =    20000.0              # terminal (close the door) time */
INFINITY =  (100.0 * STOP)      # must be much larger than STOP  */

class Timer:
    def __init__(self) -> None:
        self.current        = START         # Current time   
        self.arrival        = INFINITY      # Next Arrival time
        self.completation   = INFINITY      # Next Completation time
        self.next           = None          # Next event TODO serve o è da modificare?


class Event:
    def __init__(self) -> None:
        self.time = INFINITY    # Next occurence of an event
        self.client = None      # Client TODO seve o no?

# statistics for population
class Area:
    def __init__(self,nQueue) -> None:
        self.node       = [0.0] * nQueue 
        self.queue      = [0.0] * nQueue
        self.service    = [0.0] * nQueue