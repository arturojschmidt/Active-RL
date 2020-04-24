
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
    # agent = ModelFreeActiveLearning(,10,agentEnviroment,30,1000)
    # agent.QLearning()
    agent = ModelBasedActiveLearning(agentEnviroment,100,10000,0.9)
    agent._generateModel(10000)
    agent.valueIterationBellman()



    #print(agentEnviroment.takeAction(s,a))





if __name__ == "__main__":
    main()