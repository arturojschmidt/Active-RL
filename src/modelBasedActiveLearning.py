


class ModelBasedActiveLearning:


    def __init__(self, enviroment):
        self.enviroment = enviroment

    def valueIterationADP(self):
        counter = 0
        while counter < self.maxIterations:
            prevState = None
            prevAction = None
            notInTerminalState = True

            while notInTerminalState:
                currentState = self.enviroment.getStartingState()

                if self.utilities[currentState] == None:
                    self.utilities[currentState] = reward

                if prevState != None:
                    # increment transition probability table for prevState, prevAction = currentState, n
                    # incremenet utility function of prev state
                    pass
                if currentState == self.enviroment.getTerminalState():
                    notInTerminalState = False


                counter += 1



