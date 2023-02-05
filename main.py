import time
import SystemConfiguration
from SimCore import Simulation



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
        print("\t[2] Infinite Horizon study\n")
        print("\t[3] TEST Output for best probability study\n")
        print("\t[4] TEST Output for best probability study\n")

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
            
            
            

        elif (inp == 2) :
            print("2")
            batch = (256,64) #(b,k) TODO come selezionare
            InfiniteHorizonStudy(batch)

        elif (inp == 0):
            print("\n-------------------QUIT--------------------\n")
        else:
            print("Wrong input")
        
        #time.sleep(2)

    # End program
    quit()    

def singleRun(seed):
    sim = Simulation(seed)
    sim.startSimulation()

def InfiniteHorizonStudy(batch):
    simulationTime = ( batch[0] * batch[1] ) #/ SystemConfiguration.arrivalRate
    seed = 12345
    sim = Simulation(seed,simulationTime=simulationTime)
    sim.startSimulation(stationary=True,batch=batch)


def FiniteHorizonStudy():
    replication = None






#Start simulation
if __name__ == "__main__":
    main()