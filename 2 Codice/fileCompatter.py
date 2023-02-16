
from SystemConfiguration import ROOT_DIR
import os
import pandas as pd
import numpy as np
from lib.rvms import idfStudent
from math import sqrt

# for select the path of simulation file
TEST_DIR = "outputStat"
stringName = "LambdaVar/400"
columName = "x"


path = os.path.join(ROOT_DIR,TEST_DIR,stringName)

# main
print("READING COLUMN: {}\n".format(columName))

all_col = []
time = None

for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:

    filePath = os.path.join(path, file)
    df1=pd.read_csv(filePath)
    try:
        specific_column=df1[columName] #extract column
        time = df1["time"]
        all_col.append(specific_column.rename("{}".format(file)))
        print("file : {}".format(file))
    except:
        print("{} not valid csv".format(file))
    
time.rename("Time")

df = pd.concat([time,all_col[2],all_col[1],all_col[0],all_col[3],all_col[4]],axis=1)

df["Total"] = df.iloc[:,[1,2,3,4,5]].sum(axis=1)
df["Socio"] = df.iloc[:,[1,2,5]].sum(axis=1)
df["Tesse"] = df.iloc[:,[1,2,4,5]].sum(axis=1)
print(df)


save_path = os.path.join(path,"{}_stat_compact.csv".format(columName))

df.to_csv(save_path,index=False)
print("file saved on : {}".format(save_path))

