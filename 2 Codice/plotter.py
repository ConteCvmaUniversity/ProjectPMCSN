
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

def plot_horizzontal_line(val,col,lab,m):

    plt.axhline(y=val,color=col,linestyle='--',label=lab)
    plt.text(
        m,
        val,
        str(val),
        fontsize=10,
        va="center",
        ha="center",
        color="red",
        backgroundcolor="white"
    )


def var_plot(x,y,w,col,lab):

    #plt.plot(x, y, "k.")
    plt.plot(x, y, color=col,label=lab)
    #plt.plot([x, x], [y - w, y + w], color='k', linestyle='-', linewidth=2)
    plt.fill_between(x,y-w,y+w,color=col,alpha=.15)


def normal_plot(x,y,col,lab):
    plt.plot(x, y, color=col,label=lab)


def slottedResponceTimePlot(df:pd.DataFrame,title="",subs=""):

    plt.figure(figsize=(16,9))

    #plt.xticks(np.arange(0, 421 , step=15),rotation=0)
    v = 420
    ste = 15

    plt.xticks(np.arange(0, v+1 , step=ste),rotation=0)
    
    plt.title(f"{title}")

    plt.ylabel(f"Response time (min)")
    plt.xlabel("Time (min)")

    x = df['Time'].values[:v]
    
    y = df["Total_mean"].values[:v]
    w = df["Total_var"].values[:v]
    #plt.plot(x,y,label="Global response time")
    var_plot(x,y,w,"blue",f"Global {subs}")

    plot_horizzontal_line(15,"blue","QoS 1",v)

    y = df["Tesse_mean"].values[:v]
    w = df["Tesse_var"].values[:v]
    #plt.plot(x,y,label="Set 1-2-4-5 response time")
    var_plot(x,y,w,"orange",f"Set 1-2-4-5 {subs}")

    plot_horizzontal_line(7,"orange","QoS 2",v)

    y = df["Socio_mean"].values[:v]
    w = df["Socio_var"].values[:v]

    #plt.plot(x,y,label="Set 1-2-5 response time")
    var_plot(x,y,w,"green",f"Set 1-2-5 {subs}")

    plot_horizzontal_line(3,"green","QoS 3",v)

    

    plt.legend(loc="upper left")
    plt.show()

def slottedUtilization(df:pd.DataFrame,title="",subs=""):
    plt.figure(figsize=(16,9))

    #plt.xticks(np.arange(0, 421 , step=15),rotation=0)
    v = 420
    ste = 15

    plt.xticks(np.arange(0, v+1 , step=ste),rotation=0)
    
    plt.title(f"{title}")

    plt.ylabel(f"Response time (min)")
    plt.xlabel("Time (min)")

    x = df['Time'].values[:v]

    y = df["Set1.csv_mean"].values[:v]
    normal_plot(x,y,"blue","Set 1 utilizzation")
    #mean = round(np.nanmean(y),3)
    #plot_horizzontal_line(mean,"blue","mean",v)


    y = df["Set2.csv_mean"].values[:v]
    normal_plot(x,y,"orange","Set 2 utilizzation")

    y = df["Set3.csv_mean"].values[:v]
    normal_plot(x,y,"green","Set 3 utilizzation")
    #mean = round(np.nanmean(y),3)
    #plot_horizzontal_line(mean,"green","mean",v)

    y = df["Set4.csv_mean"].values[:v]
    normal_plot(x,y,"purple","Set 4 utilizzation")
    #mean = round(np.nanmean(y),3)
    #plot_horizzontal_line(mean,"purple","mean",v)

    y = df["Set5.csv_mean"].values[:v]
    normal_plot(x,y,"brown","Set 5 utilizzation")

    plt.legend(loc="upper left")
    plt.show()



def main1():
    file = "LambdaVar/480/w_stat_compact.csv"

    path = os.path.join(ROOT_DIR,TEST_DIR,file)

    df = getDFfromCSV(path)

    file = "FindBatch/256/w_stat_compact.csv"
    path = os.path.join(ROOT_DIR,TEST_DIR,file)
    df2 = getDFfromCSV(path)
    
    responseTimePlotLambda(df,df2=df2,title="Responce Time on Infinite Horizon for lambda = 1.1429",batchSize=512)

def main2():
    file = "outputStat/Slotted/conf1/w_advaceReading.csv"
    path = os.path.join(ROOT_DIR,file)
    df = getDFfromCSV(path)
    slottedResponceTimePlot(df,title="Responce Time for configuration 1",subs="response time")

def main3():
    file = "outputStat/Slotted/conf1/x_advaceReading.csv"
    path = os.path.join(ROOT_DIR,file)
    df = getDFfromCSV(path)
    slottedUtilization(df,title="Set Utilizzation for configuration 1")





if __name__ == "__main__":
    #main1()
    main2()
    #main3()    
    

    