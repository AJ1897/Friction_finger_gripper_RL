from agent import Agent
from monitor import interact
from env import Friction_finger_env
import numpy as np

env = Friction_finger_env()
agent = Agent()
avg_rewards, best_avg_reward,policy = interact(env, agent)

#Test_cases
start_state=(7.1,8.0)
env1=Friction_finger_env(start_state)
action=policy[start_state]
i=0
print("\n")
while(i<100):
    next_state,reward,done=env1.step(action)
    print(next_state,action)
    action=policy[next_state]
    i=i+1
    if(done):
        break