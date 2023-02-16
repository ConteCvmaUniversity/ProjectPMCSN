
import os
from matplotlib.transforms import Transform
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

TEST_DIR = "outputStat"
ROOT_DIR = os.path.dirname(__file__)



def getDFfromCSV(filePath)->pd.DataFrame:
    ret = pd.read_csv(filePath)
    ret['id'] = range(1, len(ret) + 1)
    return ret

def responseTimePlotLambda(df:pd.DataFrame,df2=None,title="",batchSize=1):
    
    plt.figure(figsize=(16,9))
    plt.xticks(np.arange(0, 66 , step=8),rotation=-45)
    plt.title(f"{title}")

    plt.ylabel(f"Response time (min)")
    plt.xlabel("Batch number")

    x = df['id'] 
    y = df["Total"]
    plt.plot(x,y,label="Global response time")

    mean = np.nanmean(y)
    plt.axhline(y=mean,linestyle='--',label="mean")
    plt.text(
            0,
            mean,
            "{:0.3f}".format(mean),
            fontsize=10,
            va="center",
            ha="center",
            color="red",
            backgroundcolor="white"
        )

    if (type(df2) != type(None)):
        x = df2['id'] 
        y = df2["Total"]

        plt.plot(x,y,label="Global response time for lambda = 1.0714")
        plt.axhline(y=19.201,color="orange",linestyle='--',label="mean value for lambda = 1.0714")
        plt.text(
            0,
            19.201,
            str(19.201),
            fontsize=10,
            va="center",
            ha="center",
            color="red",
            backgroundcolor="white"
        )
    
    ax = plt.gca()
    #ax.set_ylim([5, 30])
    

    plt.legend(loc="upper left")
    plt.show()




if __name__ == "__main__":

    file = "LambdaVar/480/w_stat_compact.csv"

    path = os.path.join(ROOT_DIR,TEST_DIR,file)

    df = getDFfromCSV(path)

    file = "FindBatch/256/w_stat_compact.csv"
    path = os.path.join(ROOT_DIR,TEST_DIR,file)
    df2 = getDFfromCSV(path)
    
    responseTimePlotLambda(df,df2=df2,title="Responce Time on Infinite Horizon for lambda = 1.1429",batchSize=512)
    

    