import numpy as np
from collections import defaultdict
import random
import json
class Agent:

    def __init__(self, nA=5, Bootsrap_policy=False):
        """ Initialize agent.

        Params
        ======
        - nA: number of actions available to the agent
        """
        self.nA = nA
        if Bootsrap_policy:
            with open('Q_table.txt') as json_file:
                self.Q = json.load(json_file)
        else:
            self.Q = defaultdict(lambda: [0,0,0,0,0])    #Since we are storing in a json file, using a list instead of numpy arrays
        self.epsilon=1.0
        self.epsilon_decay=0.0001
        self.epsilon_min=0.0003
        self.alpha=0.7
        self.gamma=0.995

    def update_epsilon(self):
        self.epsilon=max(self.epsilon*self.epsilon_decay,self.epsilon_min)

    def get_action_probs(self,state):
        prob_action_policy=np.ones(self.nA)*(self.epsilon/self.nA)
        best_a=np.argmax(self.Q[str(state)]) if str(state) in self.Q.keys() else 0
        prob_action_policy[best_a]=1.0-self.epsilon+(self.epsilon/self.nA)
        return prob_action_policy

    def select_action(self, state):
        """ Given the state, select an action.

        Params
        ======
        - state: the current state of the environment

        Returns
        =======
        - action: an integer, compatible with the task's action space
        """
        action_set=('l','r','lh','hl','hh')
        n=np.random.random()
        if n>self.epsilon:
            action=np.argmax(self.Q[str(state)] if str(state) in self.Q.keys() else 0)
        else:
            action= np.random.choice(self.nA)

        return action

    def step(self, state, action, reward, next_state, done):
        """ Update the agent's knowledge, using the most recently sampled tuple.

        Params
        ======
        - state: the previous state of the environment
        - action: the agent's previous choice of action
        - reward: last reward received
        - next_state: the current state of the environment
        - done: whether the episode is complete (True or False)
        """
        #print("action",action)
        action_prob=self.get_action_probs(next_state)
        if str(state) not in self.Q.keys():
            self.Q[str(state)]=[0,0,0,0,0]
        if str(next_state) not in self.Q.keys():
            self.Q[str(next_state)]=[0,0,0,0,0]
        error= reward+self.gamma*(self.Q[str(next_state)][np.argmax(self.Q[str(next_state)])])-self.Q[str(state)][action]
        self.Q[str(state)][action] = self.Q[str(state)][action]+ self.alpha*(reward+self.gamma*(self.Q[str(next_state)][np.argmax(self.Q[str(next_state)])])-self.Q[str(state)][action])
        self.update_epsilon()
        return self.Q,error