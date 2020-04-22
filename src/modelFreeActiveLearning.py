
from ActiveLearning import ActiveLearning

import numpy as np
import random

from pprint import pprint
#Q(s,a) = Q(s,a) + alpha(R(s) + y maxQ(s',a') - Q(s,a))
# q of previous state and action is equal to itself + its reward + the difference 

#optimal policy is pi(s) = max Q(s,a) for all a in s




from collections import defaultdict

class ModelFreeActiveLearning(ActiveLearning):

    def __init__(self, learnRate, maxShots, enviroment, minTries, epochs):
        ActiveLearning.__init__(self, learnRate,maxShots)
        self.enviroment = enviroment
        self._qtable = defaultdict(int)
        self._stateActionFrequency = defaultdict(int)

        self._minTries = minTries
        self.maxShots = maxShots
        self._epochs = epochs

    def _getNextAction(self, state):  # balances exploration vs exploitation 
        
        # get the highest qvalued action at passed state
        #print("state to choose action from:" , state)
        maxQAction = self.getMaxQAction(state)
        randomAction = self.getRandomAction(state)
        if maxQAction == None:
            #print('random state 1: ', randomAction)
            return randomAction
 
        if self._stateActionFrequency[(state,maxQAction)] > self._minTries: # greedy approach since we've seen > minTries examples
            print("MAX PRINTED")
            return maxQAction
        #print('random state 23: ', randomAction)
        return randomAction # exploration
        

    
    def getMaxQAction(self,state):
        currentMax = float('-inf')
        maxAction = None
        #print('state')
        #print(self._qtable)
        for k, v in self._qtable.items():
            #print('k', k)
            #print('v',v)
            if k[0] == state and v > currentMax:
                maxAction = k[1]
        return maxAction
        #for every action that is available from this state
        #return the action which corresponds to the highest qvalue

    def getRandomAction(self,state):
        possibleActions = list(self.enviroment.getPossibleActions(state))
        #print(possibleActions)
        if len(possibleActions) == 0:
            return None
        return random.choice(possibleActions)

        

        # choose one at random and return 


    def QLearning(self):  ## takes in a state and a reward 

        #first get the inital starting state for the enviroment
        #then select a random action
        # take the action in the enviroment
        # update q[s,a] table 
        #set s to resulting s, 

        counter = 0
        while(counter < self._epochs):
            notInTerminalState = True
            currentShots = 0
            prevState = self.enviroment.getStartingState()
            while currentShots < self.maxShots and notInTerminalState:

                #gets max q action for given state
                action = self._getNextAction(prevState)   # this is the function that handles exploration vs exploitation
                # returns new state and reward of that state when taking the action in previous state
                print(prevState, action)
                currentState, reward = self.enviroment.takeActionInState(action,prevState)
                print(prevState, "," , action, "-->" , currentState)
                    
                self._stateActionFrequency[(prevState, action)] += 1

                nextMaxQAction  = self._getNextAction(currentState)
                nextMaxQValue   = self._qtable[currentState, nextMaxQAction]
                currentQValue   = self._qtable[prevState,action]

                newQvalue = round(currentQValue + self.learnRate*(reward + nextMaxQValue - currentQValue),2)
                self._qtable[prevState,action] = newQvalue
                
                
                print("q(", prevState, ",", action,") = ", self._qtable[prevState,action])

                prevState = currentState
                print("-----------------------------")

                if currentState == self.enviroment.getTerminalState():
                    notInTerminalState = False

                currentShots += 1
            counter += 1
        pprint(self._qtable)
        




    
        

