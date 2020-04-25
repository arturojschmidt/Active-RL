
from ActiveLearning import ActiveLearning
import matplotlib.pyplot as plt

import numpy as np
import random
from decimal import Decimal

from pprint import pprint
#Q(s,a) = Q(s,a) + alpha(R(s) + y maxQ(s',a') - Q(s,a))
# q of previous state and action is equal to itself + its reward + the difference 

#optimal policy is pi(s) = max Q(s,a) for all a in s



import math
from collections import defaultdict

class ModelFreeActiveLearning(ActiveLearning):

    def __init__(self, learnRate, discountValue, maxShots, enviroment, epochs):
        ActiveLearning.__init__(self, learnRate,maxShots)

        self.enviroment            = enviroment
        self._qtable               = defaultdict(int) # state, action -> utility
        self._stateActionFrequency = defaultdict(int)

        self.maxShots      = maxShots
        self.learnRate     = learnRate
        self.discountValue = discountValue
        self._epochs       = epochs

        self.iterations = 0

    def _getNextAction(self, state):  
        # balances exploration vs exploitation 
        # get the highest qvalued action at passed state
        # if randoms turn, return a random action
        maxQAction = self.getMaxQAction(state)
        randomAction = self.getRandomAction(state)
        randomnessProbability = self.getRandomActionProbability()
        x = random.uniform(0,1)
        if maxQAction == None or x < randomnessProbability:
            return randomAction
        return maxQAction
    def getMaxQAction(self,state):
        # k = (state, action)  // v = qValue
        # we iterate from the q table until we find starts at the same state as was passed.
        # we check if the qValue assiociated with its action is the highest we've seen so far
        # if it is, we return it
        currentMax = float('-inf')
        maxAction = None
        for k, v in self._qtable.items():
            if k[0] == state and v > currentMax:
                maxAction = k[1]
        return maxAction
    def getRandomAction(self,state):
        #returns a list of possible actions from a state
        possibleActions = list(self.enviroment.getPossibleActions(state))
        if len(possibleActions) == 0:
            return None
        return random.choice(possibleActions)
    def getRandomActionProbability(self):
        # return a probability according to a exponential function that decreases as the number of iterations increases
        exponent = -10/self._epochs*self.iterations
        probability = round(math.exp(exponent),3)
        return probability
    def play(self): 
        #first get the inital starting state for the enviroment
        #then select highest q-valued action
        #take the action in the enviroment
        #update q[s,a] table 
        #set s to resulting s, 
        totalsActions = 0
        while(self.iterations < self._epochs):
            notInTerminalState = True
            currentShots = 0
            prevState = self.enviroment.getStartingState()
        
            while notInTerminalState:
                #gets max q action for given state
                action = self._getNextAction(prevState)   # this is the function that handles exploration vs exploitation
                # returns new state and reward of that state when taking the action in previous state
                currentState, reward = self.enviroment.takeActionInState(action,prevState)
                totalsActions += 1
                self._stateActionFrequency[(prevState, action)] += 1

                nextMaxQAction  = self.getMaxQAction(currentState)
                nextMaxQValue   = self._qtable[currentState, nextMaxQAction]
                currentQValue   = self._qtable[prevState,action]
                long = self.learnRate*(reward + (self.discountValue*nextMaxQValue - currentQValue))
                # self._qtable[prevState,action] += round(long, 3)
                self._qtable[prevState,action] += long
                self._qtable[prevState,action] = round(self._qtable[prevState,action],5)

                prevState = currentState

                if currentState == self.enviroment.getTerminalState():
                    notInTerminalState = False

                currentShots += 1
            
            self.iterations += 1
        pprint(self._qtable)
        return totalsActions
    def resetGame(self):
        # resets the game to how it was constructred for performance measurements
        self._qtable               = None# state, action -> utility
        self._stateActionFrequency = None
        self._qtable = defaultdict(int)
        self._stateActionFrequency = defaultdict(int)
        self.iterations = 0
    def calculatePerforance(self, startValue, step):
        values = list()
        steps = list()
        current = startValue
        while(current < 1):
            self.resetGame()
            self.learnrate = current
            totalShots = self.play()
            values.append(round(totalShots/self._epochs,8))
            steps.append(current)
            current = round(current + step, 5)
        plt.plot(steps,values)
        plt.ylabel('totalShots')
        plt.xlabel('learnrate value')
        plt.title('MF LEARNRATE AVG shots/v(d)')
        plt.show()
        
        values = list()
        steps = list()
        current = startValue
        while(current < 1):
            self.discountValue = current
            self.resetGame()
            totalShots = self.play()
            values.append(round(totalShots/self._epochs,4))
            steps.append(current)
            current = round(current + step, 5)
        plt.plot(steps,values)
        plt.ylabel('totalShots')
        plt.xlabel('discount value')
        plt.title('MF DISCOUNT AVG shots/v(d)')
        plt.show()
        

