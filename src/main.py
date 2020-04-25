
from enviroment import Enviroment

from modelFreeActiveLearning import ModelFreeActiveLearning
from modelBasedActiveLearning import ModelBasedActiveLearning
import sys

def main():

    print('g')
    args = sys.argv
    print(args)
    agentEnviroment = Enviroment()
    agentEnviroment.parseEnviroment("exampleInput.txt")


    print('MODEL FREE STATE-ACTION UTILITY')
    agent = ModelFreeActiveLearning(0.998,0.988,25,agentEnviroment,10000)
    agent.play()
    print('------------------------------------------------------------------------------')

    agent = ModelBasedActiveLearning(agentEnviroment,50,10000,0.98,0.98)
    agent._generateModel(10000)
    agent.play()
   



if __name__ == "__main__":
    main()