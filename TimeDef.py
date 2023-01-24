
START =        0.0              # initial time                   */
STOP  =    20000.0              # terminal (close the door) time */
INFINITY =  (100.0 * STOP)      # must be much larger than STOP  */

class Timer:
    def __init__(self,nQueue) -> None:
        self.current        = START
        self.next           = -1
        self.last           = [-1] * nQueue
    