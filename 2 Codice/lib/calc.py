from enum import Enum
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

#print("\n\n ...... com ....")
#for elem in list(ClientType):
    #print("{} prob: {}".format(elem.name,elem.value["prob"]))

#print("\n ...... com ....\n\n")
RHO = 0.344732375
M = 2
#LAM = 0.68946475
ES = 1


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def special_sum():
    sum = 0.0
    for i in range(0,M):
        print(i)
        sum += ((M*RHO)**i)/factorial(i)
    
    return sum


p_0 = 1/(special_sum() + ((M*RHO)**M)/(factorial(M) * (1-RHO) ) )

Pq = ((M*RHO)**M)/(factorial(M) * (1-RHO) ) * p_0

Tq = Pq * ((ES)/((1-RHO)))

print("Tq = {}".format(Tq))