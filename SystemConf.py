from enum import Enum

# GLOBAL VALUE






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

class ServerStateType(Enum):
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

#
# Metadata for server set
#

class SetMetadata:
    numberOfQueue = None
    serverStateType : ServerStateType = None


class SetMetadata1(SetMetadata):
    numberOfQueue = 1
    serverStateType = ServerStateType1

class SetMetadata2(SetMetadata):
    numberOfQueue = 1
    serverStateType = ServerStateType2

class SetMetadata3(SetMetadata):
    numberOfQueue = 2
    serverStateType = ServerStateType3

class SetMetadata4(SetMetadata):
    numberOfQueue = 1
    serverStateType = ServerStateType4
    extraNumberOfQueue = 3

class SetMetadata5(SetMetadata):
    numberOfQueue = 2
    serverStateType = ServerStateType5

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
