
from collections import defaultdict
import random
from pprint import pprint
# 7 States:

# Fairway -- > At, Past, Left
# Ravine -- > At, Past, Left
# Close 
# Same 
# Over
# At 
# In

ENDING_STATE_POSITION = 0
PROBABILITY_POSITION = 1



class Enviroment:

    def __init__(self):
        self.__transitionModel = defaultdict(list)   #(state,action) -> [ (state, probability), ]

    def parseEnviroment(self, input):

        for line in open(input,'r').readlines():
            elements = line.split('/')

            startState  = elements[0]
            action      = elements[1]
            endState    = elements[2] 
            probability = elements[3]

            if(probability[-1] == "\n"):
                probability = probability[:-1]

            self.__transitionModel[(startState,action)].append([endState,float(probability)])
        self._generateTransitionModel()
    
    def getNextState(self,state,action):
        # get the possible outcomes given the state and action
        assert self.__transitionModel.get(state,action) != None
        probabilityDistribution = self.__transitionModel[(state,action)]
        # generate a random number between 1 and 0 to represent probability
        randomNumber = random.uniform(0,1)
        # return first state which the random is less than
        for pair in probabilityDistribution:
            if randomNumber < pair[PROBABILITY_POSITION]:
                print(randomNumber, pair[ENDING_STATE_POSITION])
                return pair[ENDING_STATE_POSITION]


    def _generateTransitionModel(self):
            for outcomes in self.__transitionModel.values():
                outcomes.sort(key= lambda x: x[PROBABILITY_POSITION])
                for i in range(1,len(outcomes)):
                    outcomes[i][PROBABILITY_POSITION] += outcomes[i-1][PROBABILITY_POSITION]

            pprint(self.__transitionModel)

        