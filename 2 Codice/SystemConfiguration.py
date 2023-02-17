from enum import Enum
from TimeDef import STOP
import os

ROOT_DIR = os.path.dirname(__file__)
STATIONARY_DIR = "outputStat/Stationary"

# GLOBAL VALUE
simulationTimeG         = STOP
probabilityDiscardSet1  = 0.01
arrivalRate             = (450/STOP)   # MODIFICABLE 
#arrivalRate             = (525/STOP)
timeSlotSize            = 1
timeSlotNum             = int(STOP/timeSlotSize)


#-------------------------------------------------------------------------
# CLIENT CONFIGURATION
#-------------------------------------------------------------------------

class ClientTProb(Enum):
    SOCIO       = 0.05
    RINNOVO     = 0.1
    NEWMODULO   = 0.2
    NEWMAGG     = 0.25
    NEWFAMILY   = 0.4

class ClientPProb(Enum):
    SINGOLO     = 0.35
    GRUPPO      = 0.65


# Enum for client type value

class ClientTV(Enum):
    SOCIO       = 1
    RINNOVO     = 2
    NEWMODULO   = 3
    NEWMAGG     = 4
    NEWFAMILY   = 5

# Enum for client pay value
class ClientPV(Enum):
    SINGOLO     = 1
    GRUPPO      = 2


# Client type according to documentation
class ClientType(Enum):
    SS      = {"index" : 0 , "type": ClientTV.SOCIO    ,  "pay": ClientPV.SINGOLO , "prob": ClientTProb.SOCIO     .value * ClientPProb.SINGOLO.value } 
    SG      = {"index" : 1 , "type": ClientTV.SOCIO    ,  "pay": ClientPV.GRUPPO  , "prob": ClientTProb.SOCIO     .value * ClientPProb.GRUPPO .value }
    RS      = {"index" : 2 , "type": ClientTV.RINNOVO  ,  "pay": ClientPV.SINGOLO , "prob": ClientTProb.RINNOVO   .value * ClientPProb.SINGOLO.value }
    RG      = {"index" : 3 , "type": ClientTV.RINNOVO  ,  "pay": ClientPV.GRUPPO  , "prob": ClientTProb.RINNOVO   .value * ClientPProb.GRUPPO .value } 
    NMOS    = {"index" : 4 , "type": ClientTV.NEWMODULO,  "pay": ClientPV.SINGOLO , "prob": ClientTProb.NEWMODULO .value * ClientPProb.SINGOLO.value } 
    NMOG    = {"index" : 5 , "type": ClientTV.NEWMODULO,  "pay": ClientPV.GRUPPO  , "prob": ClientTProb.NEWMODULO .value * ClientPProb.GRUPPO .value }
    NMAS    = {"index" : 6 , "type": ClientTV.NEWMAGG  ,  "pay": ClientPV.SINGOLO , "prob": ClientTProb.NEWMAGG   .value * ClientPProb.SINGOLO.value } 
    NMAG    = {"index" : 7 , "type": ClientTV.NEWMAGG  ,  "pay": ClientPV.GRUPPO  , "prob": ClientTProb.NEWMAGG   .value * ClientPProb.GRUPPO .value }
    NFS     = {"index" : 8 , "type": ClientTV.NEWFAMILY,  "pay": ClientPV.SINGOLO , "prob": ClientTProb.NEWFAMILY .value * ClientPProb.SINGOLO.value }
    NFG     = {"index" : 9 , "type": ClientTV.NEWFAMILY,  "pay": ClientPV.GRUPPO  , "prob": ClientTProb.NEWFAMILY .value * ClientPProb.GRUPPO .value } 


CLIENTTYPENUM = len(ClientType)


#-------------------------------------------------------------------------
# SERVER STATE CONFIGURATION
#-------------------------------------------------------------------------

EXPONENTIAL = False  # if true all service are exponential # MODIFICABLE

class ServerStateType():
    IDLE    = -1

class ServerStateType1(ServerStateType):
    BUSY    = 1
    FAMILY  = 2

# Same state of type 1 but repeted for logical reason
class ServerStateType2(ServerStateType):
    BUSY    = 1
    FAMILY  = 2

class ServerStateType3(ServerStateType):
    MAGG    = 1
    FAMILY  = 2

class ServerStateType4(ServerStateType):
    COMPLETE    = 1
    MAGG        = 2
    FAMILY      = 3

class ServerStateType5(ServerStateType):
    SINGOLO     = 1
    GRUPPO      = 2

# Classes that define service time (clone of state)
class ServerServiceTime1(Enum): # Erlang (n,b)
    BUSY    = (2,0.25)
    FAMILY  = (2,0.5)

class ServerServiceTime2(Enum): # Uniform (a,b)
    BUSY    = (1/3,2/3)
    FAMILY  = (2/3,4/3)

class ServerServiceTime3(Enum): # Truncated Normal (m,sd,a,b)
    MAGG    = (4,2,2,10)
    FAMILY  = (6,2,2,10)

class ServerServiceTime4(Enum): # Truncated Normal (m,sd,a,b)
    COMPLETE    = (3,1,1,5)
    MAGG        = (3,1,1,5)
    FAMILY      = (3,1,1,5)

class ServerServiceTime5(Enum):
    SINGOLO     = (1.5,0.2,1,2) # Truncated Normal (m,sd,a,b)
    GRUPPO      = (1/3,2/3)     # Uniform (a,b)

# Exponential service configuration
class ServerServiceTime1Exp(Enum):
    BUSY    = 0.75
    FAMILY  = 0.75

class ServerServiceTime2Exp(Enum):
    BUSY    = 0.75
    FAMILY  = 0.75

class ServerServiceTime3Exp(Enum):
    MAGG    = 5
    FAMILY  = 5

class ServerServiceTime4Exp(Enum):
    COMPLETE    = 3
    MAGG        = 3
    FAMILY      = 3

class ServerServiceTime5Exp(Enum):
    SINGOLO     = 1
    GRUPPO      = 1

#-------------------------------------------------------------------------
# SERVER NUMBER CONFIGURATION
#-------------------------------------------------------------------------

class ServerNumber(Enum): # MODIFICABLE
    SET1    = 2 
    SET2    = 2
    SET3    = 4
    SET4    = 4
    SET5    = 2

#SERVERNUMBER = 16


#-------------------------------------------------------------------------
# Metadata for server set
#-------------------------------------------------------------------------

class SetMetadata:
    numberOfQueue = None                        #Define number of queue in set, consequently number of arrivals type
    serverStateType : ServerStateType = None
    lossPropability = None
    clientToSStateMap = None
    serverEventNumber = None
    simulationTime = simulationTimeG

    def __new__(cls):
        if not hasattr(cls , 'instance'):
            cls.instance = super(SetMetadata, cls).__new__(cls)
        return cls.instance


class SetMetadata1(SetMetadata):
    numberOfQueue = 1
    serverStateType = ServerStateType1
    serverEventNumber = 2
    lossPropability = 0.01
    clientToSStateMap = {   ClientType.SS   : ServerStateType1.BUSY     ,                    \
                            ClientType.SG   : ServerStateType1.BUSY     ,                    \
                            ClientType.RS   : ServerStateType1.BUSY     ,                    \
                            ClientType.RG   : ServerStateType1.BUSY     ,                    \
                            ClientType.NMOS : ServerStateType1.BUSY     ,                    \
                            ClientType.NMOG : ServerStateType1.BUSY     ,                    \
                            ClientType.NMAS : ServerStateType1.BUSY     ,                    \
                            ClientType.NMAG : ServerStateType1.BUSY     ,                    \
                            ClientType.NFS  : ServerStateType1.FAMILY   ,                    \
                            ClientType.NFG  : ServerStateType1.FAMILY   }

class SetMetadata2(SetMetadata):
    numberOfQueue = 1
    serverStateType = ServerStateType2
    serverEventNumber = 2
    clientToSStateMap = {   ClientType.SS   : ServerStateType2.BUSY     ,                    \
                            ClientType.SG   : ServerStateType2.BUSY     ,                    \
                            ClientType.RS   : ServerStateType2.BUSY     ,                    \
                            ClientType.RG   : ServerStateType2.BUSY     ,                    \
                            ClientType.NMOS : ServerStateType2.BUSY     ,                    \
                            ClientType.NMOG : ServerStateType2.BUSY     ,                    \
                            ClientType.NMAS : ServerStateType2.BUSY     ,                    \
                            ClientType.NMAG : ServerStateType2.BUSY     ,                    \
                            ClientType.NFS  : ServerStateType2.FAMILY   ,                    \
                            ClientType.NFG  : ServerStateType2.FAMILY   }

class SetMetadata3(SetMetadata):
    numberOfQueue = 2
    serverStateType = ServerStateType3
    serverEventNumber = 2
    clientToSStateMap = {   ClientType.SS   : -1                        ,                    \
                            ClientType.SG   : -1                        ,                    \
                            ClientType.RS   : -1                        ,                    \
                            ClientType.RG   : -1                        ,                    \
                            ClientType.NMOS : -1                        ,                    \
                            ClientType.NMOG : -1                        ,                    \
                            ClientType.NMAS : ServerStateType3.MAGG     ,                    \
                            ClientType.NMAG : ServerStateType3.MAGG     ,                    \
                            ClientType.NFS  : ServerStateType3.FAMILY   ,                    \
                            ClientType.NFG  : ServerStateType3.FAMILY   }

class SetMetadata4(SetMetadata):
    numberOfQueue = 1
    serverStateType = ServerStateType4
    serverEventNumber = 3
    extraNumberOfQueue = 3
    #clientToSStateMap = {   ClientType.SS   : -1                        ,                    \
    #                        ClientType.SG   : -1                        ,                    \
    #                        ClientType.RS   : ServerStateType4.COMPLETE ,                    \
    #                        ClientType.RG   : ServerStateType4.COMPLETE ,                    \
    #                        ClientType.NMOS : ServerStateType4.COMPLETE ,                    \
    #                        ClientType.NMOG : ServerStateType4.COMPLETE ,                    \
    #                        ClientType.NMAS : ServerStateType4.MAGG     ,                    \
    #                        ClientType.NMAG : ServerStateType4.MAGG     ,                    \
    #                        ClientType.NFS  : ServerStateType4.FAMILY   ,                    \
    #                        ClientType.NFG  : ServerStateType4.FAMILY   }
    
    clientToSStateMap = {   ClientType.SS   : -1                        ,                    \
                            ClientType.SG   : -1                        ,                    \
                            ClientType.RS   : ServerStateType4.COMPLETE ,                    \
                            ClientType.RG   : ServerStateType4.COMPLETE ,                    \
                            ClientType.NMOS : ServerStateType4.COMPLETE ,                    \
                            ClientType.NMOG : ServerStateType4.COMPLETE ,                    \
                            ClientType.NMAS : ServerStateType4.COMPLETE ,                    \
                            ClientType.NMAG : ServerStateType4.COMPLETE ,                    \
                            ClientType.NFS  : ServerStateType4.COMPLETE ,                    \
                            ClientType.NFG  : ServerStateType4.COMPLETE }

class SetMetadata5(SetMetadata):
    numberOfQueue = 2
    serverStateType = ServerStateType5
    serverEventNumber = 2
    clientToSStateMap = {   ClientType.SS   : ServerStateType5.SINGOLO  ,                    \
                            ClientType.SG   : ServerStateType5.GRUPPO   ,                    \
                            ClientType.RS   : ServerStateType5.SINGOLO  ,                    \
                            ClientType.RG   : ServerStateType5.GRUPPO   ,                    \
                            ClientType.NMOS : ServerStateType5.SINGOLO  ,                    \
                            ClientType.NMOG : ServerStateType5.GRUPPO   ,                    \
                            ClientType.NMAS : ServerStateType5.SINGOLO  ,                    \
                            ClientType.NMAG : ServerStateType5.GRUPPO   ,                    \
                            ClientType.NFS  : ServerStateType5.SINGOLO  ,                    \
                            ClientType.NFG  : ServerStateType5.GRUPPO   }

class FactorySetMetadata:
    def getMetadata(self,typ:int) -> SetMetadata:
        if typ == 1 : 
            return SetMetadata1
        elif typ == 2 : 
            return SetMetadata2
        elif typ == 3 : 
            return SetMetadata3
        elif typ == 4 : 
            return SetMetadata4
        elif typ == 5 : 
            return SetMetadata5
        
    def __new__(cls):
        if not hasattr(cls , 'instance'):
            cls.instance = super(FactorySetMetadata, cls).__new__(cls)
        return cls.instance
