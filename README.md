#### Markov Decision Processes (MDP's) & Active Reinforcement Learning

## Defining MDP's

**Markov** defines a state in which previous states do not matter for our next decision. P(s'|all history) = P(s'| current state)



In a **MDP**, our agent exists in a stochastic enviroment, which means that the outcome of each action is not certain, but defined by a certain probability

Components:

* States S
* Actions A(s) -- available actions at state s
* Transition model P(s'|s,a) -- probability of being in s' from state s and taking an action 
    * Implies that for A(s), the transition model is going to have A(s)^s entries
* Reward Function R(s,a,s') -- reward for moving from state s with action a to state s'

With these we try to find:

* Policy -- maps a state to the optimal action at that state
    where argmax is the set of points/values where a function is maximized
    For a single state:
        policy(s) = argmax \sum_{i=1}^n P(s_i|s,a)U(s_i) for all actions in A(s)
    For complete policy (Bellman equation 1952):
        U(s) = R(s) + max \sum_{i=1}^n P(s_i|s,a)U(s_i) for all actions in A(s)
    In the case of infinite state sequences, we add a discount value to not care as much about future actions. 
    This discount value is between 0 and 1, where 0 means whe only care about the present state and 1 meaning that every action ever has the same importance. 
        U(s) = R(s) + (discountValue * max\sum_{i=1}^n P(s_i|s,a)U(s_i) for all actions in A(s))

    Things to consider:
        - What is we don't know whether our state sequences are infinite? If if large but not infininte state sequences, should we still apply a discount value?

    Ways to compute this policy:

    1) Value iteration:
    2) Policy iteration:
    


**Examples:**
    * Say you are trying to spell your name of a keyboard. When in a state of not typing, the is a set of possible action (pressing of every key). There is a transition model, which determines the p(target charcter|current position). This means that if you are trying to go to the state 'a', there is a probability that you land on 'a', but there is also the smaller probability, that you land on a neighboring key by accident. Say p(neighbor of target character|current position) = 0.1. Our reward function, if we are trying to spell 'arturo' would yield larger rewards for transistioning to state 'a' vs all other states. 

    Our policy would result in trying to press 'a', if we fail, try to press backspace, if we don't try to press 'r', if we fail, try to press backspace and so on. How big is this policy?

**Reinforcement Learning** uses rewards and punishments and instead of trying to find patterns in data (as would be the case in supervised/unsupervised learning), tries to find an action model (policy) which will give the maximum cumulative reward.

# Passive Reinforcement Learning

We have no prior knowledge of the enviroment and no prior knowldge of the reward function.

The agent does not know how the enviroment works or what its actions do
 
# Important Definitions

**Value** is he future reward that an agent would receive by taking an action at a particular state
**Policy** maps state to action
**Reward function** reward of taking an action a in state s
**Utility function** is the short term reward r(s) + the summation of the long term results of the agents lifetime (assuming best actions are taken)


policy(state) = action --> this action should be the one with the highest future reward
value(action|state) = future reward

