
from ActiveLearning import ActiveLearning

import numpy as np
import random

#Q(s,a) = Q(s,a) + alpha(R(s) + y maxQ(s',a') - Q(s,a))
# q of previous state and action is equal to itself + its reward + the difference 

#optimal policy is pi(s) = max Q(s,a) for all a in s




from collections import defaultdict

class ModelFreeActiveLearning(ActiveLearning):

    def __init__(self, learnRate, discountValue, enviroment, minTries):
        ActiveLearning.__init__(self, learnRate,discountValue)
        self.enviroment = enviroment
        self._qtable = defaultdict(list)
        self._stateActionFrequency = defaultdict(int)
        self._prevState = None
        self._prevReward = 0
        self._prevAction = None
        self._minTries = minTries

    def _getNextAction(self, state):  # balances exploration vs exploitation 
        
        # get the highest qvalued action at passed state
        maxQAction = self.getMaxQAction(state)

      
        if self._stateActionFrequency[(state,maxQAction)] > self._minTries: # greedy approach since we've seen > minTries examples
            return maxQAction
        #else return a random action
        return self.getRandomAction(state) # exploration
        

    
    def getMaxQAction(self,state):
        currentMax = 0
        for k, v in self._qtable:
            if k[0] == state and v > currentMax:
                maxAction = state[1]
        return maxAction
        #for every action that is available from this state
        #return the action which corresponds to the highest qvalue

    def getRandomAction(self,state):
        possibleActions = list()
        #for every action that is available from this state
        for k, v in self._qtable:
            if k[0] == state:
                possibleActions.append(k[1])
        return random.choice(possibleActions)

        

        # choose one at random and return 


    def QLearning(self):  ## takes in a state and a reward 

        #first get the inital starting state for the enviroment
        #then select a random action
        # take the action in the enviroment
        # update q[s,a] table 
        #set s to resulting s, 
        prevState = self.enviroment.getStartingState()

        counter = 0
        while(counter < self._minTries):
            notInTerminalState = True
            while(notInTerminalState):
                action = self._getNextAction(prevState)   # this is the function that handles exploration vs exploitation
                currentState, reward = self.enviroment.takeAction(action)
                prevAction = action

                self._stateActionFrequency[(prevState, prevAction)] += 1

                frequency       = self._stateActionFrequency[(prevState, prevAction)]
                currentQValue   = self._qtable[prevState,prevAction]
                nextMaxQAction  = self.getMaxQAction(currentState)
                nextMaxQValue   = self._qtable[currentState, nextMaxQAction]

                currentQValue += self.learnRate*(frequency)*(reward + self.discountValue * nextMaxQValue - currentQValue)
                prevState = currentState

                if currentState.isTerminal():
                    notInTerminalState = False

            counter += 1


        #get available actions from current state
        actionsAvailable = self.enviroment.getActions(self._prevState)

        # determine which action to take
        # 
        #check if there are any actions available
        #if there are none 
            #set the result to the appropriate reward of that state
        if len(actionsAvailable) == 0:
            self._qValuePairs[(self._prevState, None)] = self._prevReward

        self._stateActionFrequency[(self._prevState, self.)]
        




    
        

