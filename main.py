import time
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
        print("\t[1] Output for best probability study\n")
        print("\t[2] TEST Output for best probability study\n")
        print("\t[3] TEST Output for best probability study\n")
        print("\t[4] TEST Output for best probability study\n")

        inp = int(input("Select a number from menu: "))

        if (inp == 1) :
            print("1")
            sim = Simulation(9)
            sim.startSimulation()

        elif (inp == 2) :
            print("2")
        elif (inp == 0):
            print("\n-------------------QUIT--------------------\n")
        else:
            print("Wrong input")
        
        #time.sleep(2)

    # End program
    quit()    








#Start simulation
if __name__ == "__main__":
    main()