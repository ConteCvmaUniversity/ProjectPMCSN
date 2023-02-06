
from SystemConfiguration import ROOT_DIR
import os
import pandas as pd
import numpy as np
from lib.rvms import idfStudent
from math import sqrt

# for select the path of simulation file
TEST_DIR = "outputStat"
stringName = "Stationary"
columName = "completations"

path = os.path.join(ROOT_DIR,TEST_DIR,stringName)

def estimate(data):

    LOC = 0.95                             # level of confidence,        */ 
                                       # use 0.95 for 95% confidence */

    n    = 0                     # counts data points */
    sum  = 0.0
    mean = 0.0

    for elem in (data):                         # use Welford's one-pass method */                                    
        n += 1                              # to calculate the sample mean  */   
        diff  = float(elem) - mean          # and standard deviation        */
        sum  += diff * diff * (n - 1.0) / n
        mean += diff / n
        #print("n: {}, data : {}".format(n,elem))
    #EndWhile
    stdev  = sqrt(sum / n)
    #print("n:{} sum:{} mean:{} stdev:{} ".format(n,sum,mean,stdev))
    if (n > 1): 
        u = 1.0 - 0.5 * (1.0 - LOC)              # interval parameter  */
        t = idfStudent(n - 1, u)                 # critical value of t */
        w = t * stdev / sqrt(n - 1)              # interval half width */
        print("\nbased upon {0:1d} data points and with {1:d} confidence".format(n,int(100.0 * LOC + 0.5)))
        print("the expected value is in the interval {0:10.2f} +/-{1:6.2f}".format(mean, w))

    else:
        print("ERROR - insufficient data\n")



# main

for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:

    filePath = os.path.join(path, file)
    df=pd.read_csv(filePath)

    specific_column=df[columName] #extract column

    print("file : {}".format(file))
    
    estimate(specific_column)
    print("")