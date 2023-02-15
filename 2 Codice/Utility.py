from SystemConfiguration import ClientType,ServerStateType, \
                                ServerStateType1,ServerStateType2,ServerStateType3,ServerStateType4,ServerStateType5,   \
                                ServerServiceTime1,ServerServiceTime2,ServerServiceTime3,ServerServiceTime4,ServerServiceTime5, \
                                ServerServiceTime1Exp,ServerServiceTime2Exp,ServerServiceTime3Exp,ServerServiceTime4Exp,ServerServiceTime5Exp, \
                                arrivalRate

from TimeDef    import Event ,EventType
from lib.rngs   import plantSeeds,random,selectStream
from lib.rvgs   import Exponential,Uniform,Erlang,TruncatedNormal


# Si poteva creare una enum o una classe per questi dati ?!
DISC_PROB_STREAM      = 0

__SS_ARR_STREAM       = DISC_PROB_STREAM +  1
__SG_ARR_STREAM       = DISC_PROB_STREAM +  2
__RS_ARR_STREAM       = DISC_PROB_STREAM +  3
__RG_ARR_STREAM       = DISC_PROB_STREAM +  4
__NMOS_ARR_STREAM     = DISC_PROB_STREAM +  5
__NMOG_ARR_STREAM     = DISC_PROB_STREAM +  6
__NMAS_ARR_STREAM     = DISC_PROB_STREAM +  7
__NMAG_ARR_STREAM     = DISC_PROB_STREAM +  8
__NFS_ARR_STREAM      = DISC_PROB_STREAM +  9
__NFG_ARR_STREAM      = DISC_PROB_STREAM +  10

__BUSY1_STREAM        = DISC_PROB_STREAM +  11
__FAM1_STREAM         = DISC_PROB_STREAM +  12

__BUSY2_STREAM        = DISC_PROB_STREAM +  13
__FAM2_STREAM         = DISC_PROB_STREAM +  14

__MAG3_STREAM         = DISC_PROB_STREAM +  14
__FAM3_STREAM         = DISC_PROB_STREAM +  15

__COM4_STREAM         = DISC_PROB_STREAM +  16
__MAG4_STREAM         = DISC_PROB_STREAM +  17
__FAM4_STREAM         = DISC_PROB_STREAM +  18

__SIN5_STREAM         = DISC_PROB_STREAM +  19
__GRU5_STREAM         = DISC_PROB_STREAM +  20

# TODO sul file sostituire boh il valore lo imposto nei metadata ? in caso affermativo devo passarli in qualche modo
# altrimenti imposto tutte variabili

def GetRandom(stream:int) -> float:
    selectStream(stream)
    return random()

def __EventCreationExp(typ:EventType,stream,expM,currentTime,cl,id) ->Event:
    selectStream(stream)
    time = currentTime + Exponential(expM)
    return Event(typ,id,cl,time)

def __EventCreationUni(typ:EventType,stream,a,b,currentTime,cl,id) ->Event:
    selectStream(stream)
    time = currentTime + Uniform(a,b)
    return Event(typ,id,cl,time)

def __EventCreationErl(typ:EventType,stream,n,b,currentTime,cl,id) -> Event:
    selectStream(stream)
    time = currentTime + Erlang(n,b)
    return Event(typ,id,cl,time)

def __EventCreationTruNormal(typ:EventType,stream,m,sd,a,b,currentTime,cl,id):
    selectStream(stream)
    time = currentTime + TruncatedNormal(m,sd,a,b)
    return Event(typ,id,cl,time)

def GetArrival(clientType : ClientType , setId , currentTime) -> Event:
    event = None
    typ = EventType.ARRIVAL

    mVal = (1 / (clientType.value["prob"] * arrivalRate) ) # compute value based on client type
    
    if (clientType == ClientType.SS):
        event = __EventCreationExp(typ,__SS_ARR_STREAM,mVal,currentTime,clientType,setId)
    
    elif (clientType == ClientType.SG):
        event = __EventCreationExp(typ,__SG_ARR_STREAM,mVal,currentTime,clientType,setId)
    
    elif (clientType == ClientType.RS):
        event = __EventCreationExp(typ,__RS_ARR_STREAM,mVal,currentTime,clientType,setId)

    elif (clientType == ClientType.RG):
        event = __EventCreationExp(typ,__RG_ARR_STREAM,mVal,currentTime,clientType,setId)

    elif (clientType == ClientType.NMOS):
        event = __EventCreationExp(typ,__NMOS_ARR_STREAM,mVal,currentTime,clientType,setId)

    elif (clientType == ClientType.NMOG):
        event = __EventCreationExp(typ,__NMOG_ARR_STREAM,mVal,currentTime,clientType,setId)

    elif (clientType == ClientType.NMAS):
        event = __EventCreationExp(typ,__NMAS_ARR_STREAM,mVal,currentTime,clientType,setId)

    elif (clientType == ClientType.NMAG):
        event = __EventCreationExp(typ,__NMAG_ARR_STREAM,mVal,currentTime,clientType,setId)

    elif (clientType == ClientType.NFS):
        event = __EventCreationExp(typ,__NFS_ARR_STREAM,mVal,currentTime,clientType,setId)

    elif (clientType == ClientType.NFG):
        event = __EventCreationExp(typ,__NFG_ARR_STREAM,mVal,currentTime,clientType,setId)

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
    typ = EventType.COMPLETATION
    if (serverState == ServerStateType1.BUSY):
        mVal = (ServerServiceTime1.BUSY.value)
        event = __EventCreationErl(typ,__BUSY1_STREAM,mVal[0],mVal[1],time,clientType,Identifier)
        
    elif (serverState == ServerStateType1.FAMILY):
        mVal = (ServerServiceTime1.FAMILY.value)
        event = __EventCreationErl(typ,__FAM1_STREAM,mVal[0],mVal[1],time,clientType,Identifier)


    return event

def __GetServiceSet2(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None
    typ = EventType.COMPLETATION
    if (serverState == ServerStateType2.BUSY):
        mVal = (ServerServiceTime2.BUSY.value)
        event = __EventCreationUni(typ,__BUSY2_STREAM,mVal[0],mVal[1],time,clientType,Identifier)
        

    elif (serverState == ServerStateType2.FAMILY):
        mVal = (ServerServiceTime2.FAMILY.value)
        event = __EventCreationUni(typ,__FAM2_STREAM,mVal[0],mVal[1],time,clientType,Identifier)

    return event

def __GetServiceSet3(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None
    typ = EventType.COMPLETATION
    if (serverState == ServerStateType3.MAGG):
        mVal = (ServerServiceTime3.MAGG.value)
        event = __EventCreationTruNormal(typ,__MAG3_STREAM,mVal[0],mVal[1],mVal[2],mVal[3],time,clientType,Identifier)

    elif (serverState == ServerStateType3.FAMILY):
        mVal = (ServerServiceTime3.FAMILY.value)
        event = __EventCreationTruNormal(typ,__FAM3_STREAM,mVal[0],mVal[1],mVal[2],mVal[3],time,clientType,Identifier)

    return event

def __GetServiceSet4(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None
    typ = EventType.COMPLETATION

    if (serverState == ServerStateType4.COMPLETE):
        mVal = (ServerServiceTime4.COMPLETE.value)
        event = __EventCreationTruNormal(typ,__COM4_STREAM,mVal[0],mVal[1],mVal[2],mVal[3],time,clientType,Identifier)

    elif (serverState == ServerStateType4.MAGG):
        mVal = (ServerServiceTime4.MAGG.value)
        event = __EventCreationTruNormal(typ,__MAG4_STREAM,mVal[0],mVal[1],mVal[2],mVal[3],time,clientType,Identifier)

    elif (serverState == ServerStateType4.FAMILY):
        mVal = (ServerServiceTime4.FAMILY.value)
        event = __EventCreationTruNormal(typ,__FAM4_STREAM,mVal[0],mVal[1],mVal[2],mVal[3],time,clientType,Identifier)

    return event

def __GetServiceSet5(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None
    typ = EventType.COMPLETATION
    if (serverState == ServerStateType5.SINGOLO):
        mVal = (ServerServiceTime5.SINGOLO.value)
        event = __EventCreationTruNormal(typ,__SIN5_STREAM,mVal[0],mVal[1],mVal[2],mVal[3],time,clientType,Identifier)

    elif (serverState == ServerStateType5.GRUPPO):
        mVal = (ServerServiceTime5.GRUPPO.value)
        event = __EventCreationUni(typ,__GRU5_STREAM,mVal[0],mVal[1],time,clientType,Identifier)


    return event


#---------------------------------------------------
# Exponential service
#---------------------------------------------------


# Identifier it's a tuple (setId,serverId)
def GetServiceExp(time,clientType : ClientType ,Identifier,serverState) -> Event :

    if (Identifier[0] == 1):
        return __GetServiceSet1Exp(time,clientType,Identifier,serverState)
    
    if (Identifier[0] == 2):
        return __GetServiceSet2Exp(time,clientType,Identifier,serverState)
    
    if (Identifier[0] == 3):
        return __GetServiceSet3Exp(time,clientType,Identifier,serverState)
    
    if (Identifier[0] == 4):
        return __GetServiceSet4Exp(time,clientType,Identifier,serverState)
    
    if (Identifier[0] == 5):
        return __GetServiceSet5Exp(time,clientType,Identifier,serverState)
    

def __GetServiceSet1Exp(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None
    typ = EventType.COMPLETATION
    if (serverState == ServerStateType1.BUSY):
        mVal = (ServerServiceTime1Exp.BUSY.value)
        event = __EventCreationExp(typ,__BUSY1_STREAM,mVal,time,clientType,Identifier)

    elif (serverState == ServerStateType1.FAMILY):
        mVal = (ServerServiceTime1Exp.FAMILY.value)
        event = __EventCreationExp(typ,__FAM1_STREAM,mVal,time,clientType,Identifier)


    return event

def __GetServiceSet2Exp(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None
    typ = EventType.COMPLETATION
    if (serverState == ServerStateType2.BUSY):
        mVal = (ServerServiceTime2Exp.BUSY.value)
        event = __EventCreationExp(typ,__BUSY2_STREAM,mVal,time,clientType,Identifier)

    elif (serverState == ServerStateType2.FAMILY):
        mVal = (ServerServiceTime2Exp.FAMILY.value)
        event = __EventCreationExp(typ,__FAM2_STREAM,mVal,time,clientType,Identifier)

    return event

def __GetServiceSet3Exp(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None
    typ = EventType.COMPLETATION
    if (serverState == ServerStateType3.MAGG):
        mVal = (ServerServiceTime3Exp.MAGG.value)
        event = __EventCreationExp(typ,__MAG3_STREAM,mVal,time,clientType,Identifier)

    elif (serverState == ServerStateType3.FAMILY):
        mVal = (ServerServiceTime3Exp.FAMILY.value)
        event = __EventCreationExp(typ,__FAM3_STREAM,mVal,time,clientType,Identifier)

    return event

def __GetServiceSet4Exp(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None
    typ = EventType.COMPLETATION

    if (serverState == ServerStateType4.COMPLETE):
        mVal = (ServerServiceTime4Exp.COMPLETE.value)
        event = __EventCreationExp(typ,__COM4_STREAM,mVal,time,clientType,Identifier)

    elif (serverState == ServerStateType4.MAGG):
        mVal = (ServerServiceTime4Exp.MAGG.value)
        event = __EventCreationExp(typ,__MAG4_STREAM,mVal,time,clientType,Identifier)

    elif (serverState == ServerStateType4.FAMILY):
        mVal = (ServerServiceTime4Exp.FAMILY.value)
        event = __EventCreationExp(typ,__FAM4_STREAM,mVal,time,clientType,Identifier)

    return event

def __GetServiceSet5Exp(time,clientType : ClientType ,Identifier,serverState) -> Event:
    event = None
    typ = EventType.COMPLETATION
    if (serverState == ServerStateType5.SINGOLO):
        mVal = (ServerServiceTime5Exp.SINGOLO.value)
        event = __EventCreationExp(typ,__SIN5_STREAM,mVal,time,clientType,Identifier)

    elif (serverState == ServerStateType5.GRUPPO):
        mVal = (ServerServiceTime5Exp.GRUPPO.value)
        event = __EventCreationExp(typ,__GRU5_STREAM,mVal,time,clientType,Identifier)


    return event