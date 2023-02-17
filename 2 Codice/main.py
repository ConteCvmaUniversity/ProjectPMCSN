import time
import SystemConfiguration
from SimCore import Simulation
import lib.rngs
import os



# Main function 
def main():

    print("|------------------------------------------|\n")
    print("\tPMCSN Simulation Program\n")
    print("\tAuthor :    Marco Calavaro \n")
    
    print("|------------------------------------------|\n\n")
    
    inp = -1

    while (inp !=0):

        print("\n--------------------MENU--------------------\n")
        print("\t[0] Quit program \n")
        print("\t[1] Output single simulation run \n")
        print("\t[2] Verify Run\n")
        print("\t[3] Infinite Horizon study\n")
        print("\t[4] TEST Configuration 1\n")
        print("\t[5] TEST Configuration 2\n")
        print("\t[6] TEST Configuration 3\n")
        print("\t[7] Find batch based on correlation\n")
        print("\t[8] Lambda variation\n")
        print("\t[9] Slotted Test\n")

        try:
            inp = int(input("Select a number from menu: "))
        except:
            print("No input on menu' quitting........")
            quit()

        if (inp == 1) :
            try:
                seed = int(input("Enter a seed for the run: "))
                singleRun(seed) # execute a single run whit seed
            except:
                print("No input starting a default........")
                singleRun(9)
            
        elif (inp == 2):
            validation(100,"outputStat/Verify")
            

        elif (inp == 3) :
            
            #batch = (1024,128) #(b,k) TODO come selezionare
            batch = (256,64)
            InfiniteHorizonStudy(batch)

        elif (inp == 4):
            print("ATTENTION CONFIGURE SYSTEM MANUALLY, CONTROL IT")
            time.sleep(1)

            file = "outputStat/Test/conf1"
            test(500,file)
        elif (inp == 5):
            print("ATTENTION CONFIGURE SYSTEM MANUALLY, CONTROL IT")
            time.sleep(1)

            file = "outputStat/Test/conf2"
            test(500,file)

        elif (inp == 6):
            print("ATTENTION CONFIGURE SYSTEM MANUALLY, CONTROL IT")
            time.sleep(1)
            
            file = "outputStat/Test/conf3"
            test(500,file)
        
        elif (inp==7):
            FindBatch(64)
        
        elif (inp == 8):
            file = "outputStat/LambdaVar/520" # MODIFICABLE
            batch = (512,64)
            lambda_variation(batch,file)

        elif (inp == 9):
            print("ATTENTION CONFIGURE SYSTEM MANUALLY, CONTROL IT")
            time.sleep(1)

            repli   = 100
            seed    = 56486921
            file    = "outputStat/Slotted/conf1" # MODIFICABLE
            slotted_test(repli,file,seed)

        elif (inp == 0):
            print("\n-------------------QUIT--------------------\n")
        else:
            print("Wrong input")
        
        #time.sleep(2)

    # End program
    quit()    

def singleRun(seed = 9):
    sim = Simulation(seed)
    sim.startSimulation()

def validation(replica,file):
    seed = 123456789
    sim = Simulation(seed)
    for i in range(0,replica):
        sim.startSimulation(saveFile=file)
        seed = lib.rngs.getSeed()
        print("Run number {} completed, new seed: {}".format(i,seed))
        sim.reset_initial_state(seed)

def InfiniteHorizonStudy(batch,seed = 12345):
    simulationTime = ( batch[0] * batch[1] ) #/ SystemConfiguration.arrivalRate
    sim = Simulation(seed,simulationTime=simulationTime)
    sim.startSimulation(batch=batch)

def FindBatch(k):
    seed = 25637
    sim = Simulation(seed)
    b = 64 
    while(b<2049):
        path = "outputStat/FindBatch/{}".format(b)
        try:
            os.mkdir(os.path.join(os.path.dirname(__file__),path))
        except FileExistsError:
            print("existing dir")

        sim.reset_initial_state(seed,simulationTime=b*k)

        batch = (b,k)
        sim.startSimulation(batch=batch,saveFile=path)

        seed = lib.rngs.getSeed()
        print("Run batch {} completed, new seed: {}".format(b,seed))
        b = b*2

def lambda_variation(batch,file,seed = 72392):
    simulationTime = ( batch[0] * batch[1] ) #/ SystemConfiguration.arrivalRate
    sim = Simulation(seed,simulationTime=simulationTime)

    try:
        os.mkdir(os.path.join(os.path.dirname(__file__),file))
    except FileExistsError:
        print("existing dir")
    sim.startSimulation(batch=batch,saveFile=file)
    
def slotted_test(replica,file,seed):
    lib.rngs.plantSeeds(seed)
    sim = Simulation(None)
    for i in range(0,replica):
        sim.startSimulation(saveFile=file,slotted=True)
        print("Run number {} completed".format(i))
        sim.reset_initial_state(None)
        time.sleep(0.4)

def test(replica,file):
    lib.rngs.plantSeeds(9)
    sim = Simulation(None)
    for i in range(0,replica):
        sim.startSimulation(saveFile=file)
        print("Run number {} completed".format(i))
        sim.reset_initial_state(None)







#Start simulation
if __name__ == "__main__":
    main()