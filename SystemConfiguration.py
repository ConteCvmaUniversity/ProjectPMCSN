from enum import Enum
from TimeDef import STOP

# GLOBAL VALUE
simulationTimeG = STOP
probabilityDiscardSet1 = 0.01




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
    SS      = {"index" : 0 , "type": ClientTV.SOCIO    ,  "pay": ClientPV.SINGOLO } 
    SG      = {"index" : 1 , "type": ClientTV.SOCIO    ,  "pay": ClientPV.GRUPPO  }
    RS      = {"index" : 2 , "type": ClientTV.RINNOVO  ,  "pay": ClientPV.SINGOLO }
    RG      = {"index" : 3 , "type": ClientTV.RINNOVO  ,  "pay": ClientPV.GRUPPO  }
    NMOS    = {"index" : 4 , "type": ClientTV.NEWMODULO,  "pay": ClientPV.SINGOLO }
    NMOG    = {"index" : 5 , "type": ClientTV.NEWMODULO,  "pay": ClientPV.GRUPPO  }
    NMAS    = {"index" : 6 , "type": ClientTV.NEWMAGG  ,  "pay": ClientPV.SINGOLO }
    NMAG    = {"index" : 7 , "type": ClientTV.NEWMAGG  ,  "pay": ClientPV.GRUPPO  }
    NFS     = {"index" : 8 , "type": ClientTV.NEWFAMILY,  "pay": ClientPV.SINGOLO }
    NFG     = {"index" : 9 , "type": ClientTV.NEWFAMILY,  "pay": ClientPV.GRUPPO  }


CLIENTTYPENUM = len(ClientType)

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

class ServerNumber(Enum):
    SET1    = 2 
    SET2    = 3
    SET3    = 3
    SET4    = 3
    SET5    = 3

SERVERNUMBER = 14
#
# Metadata for server set
#

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
    clientToSStateMap = {   ClientType.SS   : -1                        ,                    \
                            ClientType.SG   : -1                        ,                    \
                            ClientType.RS   : ServerStateType4.COMPLETE ,                    \
                            ClientType.RG   : ServerStateType4.COMPLETE ,                    \
                            ClientType.NMOS : ServerStateType4.COMPLETE ,                    \
                            ClientType.NMOG : ServerStateType4.COMPLETE ,                    \
                            ClientType.NMAS : ServerStateType4.MAGG     ,                    \
                            ClientType.NMAG : ServerStateType4.MAGG     ,                    \
                            ClientType.NFS  : ServerStateType4.FAMILY   ,                    \
                            ClientType.NFG  : ServerStateType4.FAMILY   }

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
