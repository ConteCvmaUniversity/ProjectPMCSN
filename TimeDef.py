
START =        0.0              # initial time                   */
STOP  =    20000.0              # terminal (close the door) time */
INFINITY =  (100.0 * STOP)      # must be much larger than STOP  */

class Timer:
    def __init__(self) -> None:
        self.current        = START
        self.arrival        = INFINITY
        self.next           = -1
    