
from enviroment import Enviroment

from modelFreeActiveLearning import ModelFreeActiveLearning
import sys

def main():

    print('g')
    args = sys.argv
    print(args)
    agentEnviroment = Enviroment()
    agentEnviroment.parseEnviroment("exampleInput.txt")
    agent = ModelFreeActiveLearning(0.8,10,agentEnviroment,30,1000)
    agent.QLearning()


    #print(agentEnviroment.takeAction(s,a))





if __name__ == "__main__":
    main()