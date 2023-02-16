# # -------------------------------------------------------------------------  
#  * This program is based on a one-pass algorithm for the calculation of an  
#  * array of autocorrelations r[1], r[2], ... r[K].  The key feature of this 
#  * algorithm is the circular array 'hold' which stores the (K + 1) most 
#  * recent data points and the associated index 'p' which points to the 
#  * (rotating) head of the array. 
#  * 
#  * Data is read from a text file in the format 1-data-point-per-line (with 
#  * no blank lines).  Similar to programs UVS and BVS, this program is
#  * designed to be used with OS redirection. 
#  * 
#  * NOTE: the constant K (maximum lag) MUST be smaller than the # of data 
#  * points in the text file, n.  Moreover, if the autocorrelations are to be 
#  * statistically meaningful, K should be MUCH smaller than n. 
#  *
#  * Name              : acs.c  (AutoCorrelation Statistics) 
#  * Author            : Steve Park & Dave Geyer 
#  * Language          : ANSI C
#  * Latest Revision   : 2-10-97 
#  * Compile with      : gcc -lm acs.c
#  * Execute with      : acs.out < acs.dat
#  # Translated by     : Philip Steele 
#  # Language          : Python 3.3
#  # Latest Revision   : 3/26/14
#  * Execute with      : python acs.py < acs.dat
#  * ------------------------------------------------------------------------- 
#  */

#include <stdio.h>
#include <math.h>

from SystemConfiguration import ROOT_DIR
import os
import pandas as pd
import numpy as np
from lib.rvms import idfStudent
from math import sqrt

# for select the path of simulation file
TEST_DIR = "outputStat"
stringName = "FindBatch/2048"
file = "w_stat_compact.csv"
columName = "Total"

path = os.path.join(ROOT_DIR,TEST_DIR,stringName)

def acs_f(data):

    K = 10                             # K is the maximum lag */
    SIZE = (K + 1)


    i = 0                          # data point index              */
    sum = 0.0                      # sums x[i]                     */
    j = 0                          # lag index                     */
    hold = []                      # K + 1 most recent data points */
    p = 0                          # points to the head of 'hold'  */
    cosum = [0 for i in range(0,SIZE)]    # cosum[j] sums x[i] * x[i+j]   */


    while (i < SIZE):              # initialize the hold array with */
        try:
            x =  data.pop(0) #lines read in as string
        except:
            print(data)
            raise     # the first K + 1 data values    */

        sum += x
        hold.append(x)
        i += 1
    #EndWhile



    while (len(data)<0):
        for j in range(0,SIZE):
            cosum[j] += hold[p] * hold[(p + j) % SIZE]
        try:
            tmp =  data.pop(0) #lines read in as string
        except:
            print(data)
            raise
        
        
        sum    += tmp
        hold[p] = tmp
        p       = (p + 1) % SIZE
        i += 1 
        
    #EndWhile
    n = i #the total number of data points

    while (i < n + SIZE):         # empty the circular array */
        for j in range(0,SIZE):
            cosum[j] += hold[p] * hold[(p + j) % SIZE]
        hold[p] = 0.0
        p       = (p + 1) % SIZE
        i += 1 
    #EndWhile

    mean = sum / n
    for j in range(0,K+1):  
        cosum[j] = (cosum[j] / (n - j)) - (mean * mean)

    #print("for {0} data points".format(n))
    #print("the mean is ... {0:8.2f}".format(mean))
    #print("the stdev is .. {0:8.2f}\n".format(sqrt(cosum[0])))
    #print("  j (lag)   r[j] (autocorrelation)\n")
    
    for j in range(1,SIZE):
        print("{0:3d}  {1:11.3f}".format(j, cosum[j] / cosum[0]))


# main
print("READING COLUMN: {}\n".format(columName))
print("DIRECTORY : {}".format(path))
print("FILE: {}\n".format(file))


filePath = os.path.join(path, file)
df=pd.read_csv(filePath)

specific_column=df[columName] #extract column

a = []
for elem in specific_column:
    a.append(elem)


acs_f(a)
print("")