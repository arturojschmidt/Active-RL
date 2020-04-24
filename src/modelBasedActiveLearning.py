

import random
from collections import defaultdict
from pprint import pprint

OPTIMISTIC_UTILITY = 10


class ModelBasedActiveLearning:
    def __init__(self, enviroment, minExplorations, maxIterations, discountValue):
        self.enviroment  = enviroment

        self.transitions = defaultdict(list)  # (state,action) -> state, probability
        self.utilities   = defaultdict(int)
        self.policy      = defaultdict() # state -> action

        self.minExplorations = minExplorations
        self.discountValue   = discountValue
        self.minExplorations = minExplorations
        self.maxIterations   = maxIterations

    def _generateModel(self, epochs):
        for _ in range(0,epochs):
            state = self.enviroment.getStartingState()
            while(self.enviroment.getTerminalState()!=state):
                possibleActions =list(self.enviroment.getPossibleActions(state))
                action = random.choice(possibleActions)
                newState, reward = self.enviroment.takeActionInState(action,state)
                seen = False
                for results in self.transitions[state,action]:
                    if newState == results[0]:
                        results[1] += 1
                        seen = True
                if not seen:
                    self.transitions[state,action].append([newState,1])
                state = newState
        self._calculateTransistionProbabilities()
        pprint(self.transitions)
    def _calculateTransistionProbabilities(self):

            for k, v in self.transitions.items():
                count = 0
                for entry in v:
                    count += entry[1]
                for entry in v:
                    entry[1]  = round(entry[1]/count,3)
    def findHighestUtilityAction(self,state):
        #takes in a state, executes every action in that state and returns the one with the hightest utility
        possibleActions =list(self.enviroment.getPossibleActions(state))
        returnAction = None
        currentMax = float('-inf')

        for action in possibleActions:
            utility = self.calculateTotalUtility(state,action)
            if utility > currentMax:
                currentMax = utility
                returnAction = action

        return returnAction
    def valueIterationBellman(self):
        occurrences = defaultdict(int) # state, action -> occurrences
        for _ in range(0,self.maxIterations):
            state = self.enviroment.getStartingState()
            while(self.enviroment.getTerminalState()!=state):
                action = self.findHighestUtilityAction(state)
                newState, reward = self.enviroment.takeActionInState(action,state)
                occurrences[state,action] +=  1
                exploredUtility = self.explorationFunction(state,action,occurrences[state,action])
                self.utilities[state] = reward + self.discountValue * exploredUtility
                state = newState
        self.createPolicy()
        pprint(self.utilities)
        pprint(self.policy)
    def explorationFunction(self,state,action, occurrences):
        utility = 0
        if occurrences < self.minExplorations:
            utility = OPTIMISTIC_UTILITY
        else:
            utility = self.calculateTotalUtility(state,action)
        return utility
    def createPolicy(self):

        for state in self.utilities.keys():
            self.policy[state] = self.findHighestUtilityAction(state)

        # for every state, there are possible actions. The utility of that action, is the summation of 
        # the probability of all its possible next states*their utility. After we have the utility of all 
        # actions, we choose the one with the highest value.
    def calculateTotalUtility(self,state,action):
        totalUtility = 0
        for outcomes in self.transitions[state,action]:
            totalUtility += round(self.utilities[outcomes[0]]*outcomes[1],3)
        return totalUtility


        
                


