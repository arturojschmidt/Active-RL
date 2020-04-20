
from enviroment import Enviroment
from state import State
from action import Action
import sys

def main():

    print('g')
    args = sys.argv
    print(args)
    agentEnviroment = Enviroment()
    agentEnviroment.parseEnviroment(args[1])

    

    #print(agentEnviroment.takeAction(s,a))





if __name__ == "__main__":
    main()