
from SystemConfiguration import ROOT_DIR
import os
import pandas as pd
import numpy as np
from lib.rvms import idfStudent
from math import sqrt

# for select the path of simulation file
TEST_DIR = "outputStat/Slotted/Test"
stringName = "w_stat_compact.csv"
stat = "w"
#columName = ["Total"]
#columName = ["Set1.csv","Set2.csv","Set3.csv","Set4.csv","Set5.csv"]
columName = ["Set1.csv","Set2.csv","Set3.csv","Set4.csv","Set5.csv","Total","Tesse","Socio"]

path = os.path.join(ROOT_DIR,TEST_DIR,stringName)

def estimate(data,prints=True):

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
        if prints:
            print("\nbased upon {0:1d} data points and with {1:d} confidence".format(n,int(100.0 * LOC + 0.5)))
            print("the expected value is in the interval {0:10.3f} +/-{1:6.3f}\n".format(mean, w))

        return (mean,w)

    else:
        print("ERROR - insufficient data\n")



# main
def all_file_reading():
    print("READING COLUMNS: {}\n".format(columName))

    for col in columName:
        print("READING COLUMN: {}\n".format(col))
        for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:

            filePath = os.path.join(path, file)
            df=pd.read_csv(filePath)

            
            
            specific_column=df[col] #extract column

            
            print("file : {}".format(file))
            
            estimate(specific_column)
            
        print("--------------------------")


def single_file_reading():
    print("READING COLUMNS: {}\n".format(columName))

    for col in columName:
        print("READING COLUMN: {}\n".format(col))

        
        df=pd.read_csv(path)

        
        
        specific_column=df[col] #extract column

        
        estimate(specific_column)
            
        print("--------------------------")

def complex_reading(slot,step):

    df=pd.read_csv(path)
    
    tempDict = {"Time":[x for x in np.arange(0,420.1,step)]}

    for col in columName:

        tempinternalDict = {"mean":[],"var":[]}

        for i in range(1,slot+1):
            # mean value and confidence
            rslt_df = df[df["Slot"] == i]
            specific_column=rslt_df[col]
            try:
                ret = estimate(specific_column,prints=False)
            except:
                print("ERROR")
                print(f"i value {i}")
                raise

            tempinternalDict["mean"].append(ret[0])
            tempinternalDict["var"].append(ret[1])

        tempDict[f"{col}_mean"] = tempinternalDict["mean"]
        tempDict[f"{col}_var"]  = tempinternalDict["var"]

        #print(f"{col}_dict: {tempDict}")

    df_final = pd.DataFrame(tempDict)
    print(df_final)

    save_path = os.path.join(ROOT_DIR,TEST_DIR,f"{stat}_advaceReading.csv")
    df_final.to_csv(save_path,index=False)
    print("file saved on : {}".format(save_path))



    # END EXTERNAL FOR



    

if __name__ == "__main__":

    #all_file_reading()
    #single_file_reading()
    #complex_reading(421,1)
    complex_reading(1681,0.25)
