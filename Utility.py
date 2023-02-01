from SystemConf import ClientType
from TimeDef    import Event
from lib.rngs   import *

def GetRandom(stream:int) -> float:
    selectStream(stream)
    return random()

def GetArrival(clientType : ClientType , setId ) -> Event:
    event = None

    if (clientType == ClientType.SS):
        pass

    elif (clientType == ClientType.SG):
        pass

    elif (clientType == ClientType.RS):
        pass

    elif (clientType == ClientType.RG):
        pass

    elif (clientType == ClientType.NMOS):
        pass

    elif (clientType == ClientType.NMOG):
        pass

    elif (clientType == ClientType.NMAS):
        pass

    elif (clientType == ClientType.NMAG):
        pass

    elif (clientType == ClientType.NFS):
        pass

    elif (clientType == ClientType.NFG):
        pass

    return event

# Identifier it's a tuple (setId,serverId)
def GetService(time,clientType : ClientType ,Identifier,serverState) -> Event :

    if (Identifier[0] == 1):
        return __GetServiceSet1(time,clientType,Identifier,serverState)
    
    if (Identifier[0] == 2):
        return __GetServiceSet2(time,clientType,Identifier,serverState)
    
    if (Identifier[0] == 3):
        return __GetServiceSet3(time,clientType,Identifier,serverState)
    
    if (Identifier[0] == 4):
        return __GetServiceSet4(time,clientType,Identifier,serverState)
    
    if (Identifier[0] == 5):
        return __GetServiceSet5(time,clientType,Identifier,serverState)
    


def __GetServiceSet1(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None


    return event

def __GetServiceSet2(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None


    return event

def __GetServiceSet3(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None


    return event

def __GetServiceSet4(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None


    return event

def __GetServiceSet5(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None


    return event