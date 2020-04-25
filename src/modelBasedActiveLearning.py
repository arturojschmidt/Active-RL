
import matplotlib.pyplot as plt

import random
from collections import defaultdict
from pprint import pprint

OPTIMISTIC_UTILITY = 10


class ModelBasedActiveLearning:
    def __init__(self, enviroment, minExplorations, maxIterations, discountValue, learnrate):
        self.enviroment  = enviroment

        self.transitions = defaultdict(list)  # (state,action) -> state, probability
        self.utilities   = defaultdict(int)
        self.policy      = defaultdict() # state -> action

        self.minExplorations = minExplorations
        self.discountValue   = discountValue
        self.minExplorations = minExplorations
        self.maxIterations   = maxIterations
        self.learnrate       = learnrate

        self._minExplorations = minExplorations
        self._discountValue   = discountValue
        self._minExplorations = minExplorations
        self._maxIterations   = maxIterations

    def _generateModel(self, epochs):
        # plays the game epoch times, taking random actions and noting the time [state,action] -> newstate has ocurred
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
        pprint("MODEL BASED TRANSITION PROBABILITIES")
        pprint(self.transitions)
    def _calculateTransistionProbabilities(self):
        # turns the number of transitions of state, action -> state into probabilities
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
    def play(self):
        occurrences = defaultdict(int) # state, action -> occurrences
        totalActions = 0
        # runs this for as many times as passed in
        for _ in range(0,self.maxIterations):
            state = self.enviroment.getStartingState()
            while(self.enviroment.getTerminalState()!=state):
                # returns the action that leads to the highest SUM (P(s'|s,a)*U(s')) 
                action = self.findHighestUtilityAction(state)
                #takes the action in the enviroment
                newState, reward = self.enviroment.takeActionInState(action,state)
                totalActions += 1
                occurrences[state,action] +=  1
                # returns either an optimistic utility or the true utility. Done for exploration
                exploredUtility = self.explorationFunction(state,action,occurrences[state,action])
                # updates the utilities
                self.utilities[state] = self.learnrate*(reward + self.discountValue * exploredUtility)
                state = newState
        # from this utility table we can simply choose from every state the action maximize V = P(s'|s,a)*U(s') to create our policy
        self.createPolicy()
        print("MODEL BASED POLICY")
        pprint(self.policy)
        return totalActions
    def explorationFunction(self,state,action, occurrences):
        # see how many times an action occured and return either maximum utility of the true utility
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
    def resetGame(self):
        # resets the game to state at creation
        self.transitions = defaultdict(list)  # (state,action) -> state, probability
        self.utilities   = defaultdict(int)
        self.policy      = defaultdict() # state -> action

        self.minExplorations = self._minExplorations
        self.discountValue   = self._discountValue
        self.minExplorations = self._minExplorations
        self.maxIterations   = self._maxIterations
    def calculatePerforance(self, startValue, step, maxExplorations, explorationStep):
        values = list()
        steps = list()
        current = startValue
        while(current < 1):
            self.resetGame()
            self.learnrate = current
            totalShots = self.play()
            values.append(round(totalShots/self.maxIterations,8))
            steps.append(current)
            current = round(current + step, 5)
        plt.plot(steps,values)
        plt.ylabel('totalShots')
        plt.xlabel('learnrate value')
        plt.title('MB LEARNRATE AVG shots/v(d)')
        plt.show()
        
        values = list()
        steps = list()
        current = startValue
        while(current < 1):
            self.resetGame()
            self.discountValue = current
            totalShots = self.play()
            values.append(round(totalShots/self.maxIterations,4))
            steps.append(current)
            current = round(current + step, 5)
        plt.plot(steps,values)
        plt.ylabel('totalShots')
        plt.xlabel('discount value')
        plt.title('MB DISCOUNT AVG shots/v(d)')
        plt.show()

                
        values = list()
        steps = list()
        current = 0
        while(current < maxExplorations):
            self.resetGame()
            self.minExplorations = current
            totalShots = self.play()
            values.append(round(totalShots/self.maxIterations,4))
            steps.append(current)
            current += explorationStep
        plt.plot(steps,values)
        plt.ylabel('totalShots avg')
        plt.xlabel('Nº min exlorations')
        plt.title('Exploration vs Exploitation')
        plt.show()