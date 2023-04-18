import numpy as np
import gym
import random

total_episodes = 3000        # Total episodes
Qlearning = 1

def learn(learning_rate = 0.8, gamma = 0.95, method=Qlearning):
    # List of rewards
    rewards = []
    env = gym.make("FrozenLake-v0")

    action_size = env.action_space.n
    state_size = env.observation_space.n

    qtable = np.zeros((state_size, action_size))

    max_steps = 99                # Max steps per episode
    
    # Exploration parameters
    epsilon = 1.0                 # Exploration rate
    max_epsilon = 1.0             # Exploration probability at start
    min_epsilon = 0.01            # Minimum exploration probability 
    decay_rate = 0.005             # Exponential decay rate for exploration prob
    learning_data = np.zeros((total_episodes, 3))
    for episode in range(total_episodes):
        # Reset the environment
        state = env.reset()
        step = 0
        done = False
        total_rewards = 0
        
        for step in range(max_steps):
            # 3. Choose an action a in the current world state (s)
            ## First we randomize a number
            exp_exp_tradeoff = random.uniform(0, 1)
            
            ## If this number > greater than epsilon --> exploitation (taking the biggest Q value for this state)
            if exp_exp_tradeoff > epsilon:
                action = np.argmax(qtable[state,:])

            # Else doing a random choice --> exploration
            else:
                action = env.action_space.sample()

            # Take the action (a) and observe the outcome state(s') and reward (r)
            new_state, reward, done, info = env.step(action)

            # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
            # qtable[new_state,:] : all the actions we can take from new state
            if method == Qlearning:
                qtable[state, action] = qtable[state, action] + learning_rate * (reward + gamma * np.max(qtable[new_state, :]) - qtable[state, action])
            else:
                if exp_exp_tradeoff > epsilon:
                    new_action = np.argmax(qtable[new_state,:])
                else:
                    new_action = env.action_space.sample()
                qtable[state, action] = qtable[state, action] + learning_rate * (reward + gamma * np.max(qtable[new_state, new_action]) - qtable[state, action])

            total_rewards = reward
            
            # Our new state is state
            state = new_state
            
            # If done (if we're dead) : finish episode
            if done == True: 
                learning_data[episode, 0] = step
                learning_data[episode, 1] = reward
                break
            
        # Reduce epsilon (because we need less and less exploration)
        epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode) 
        rewards.append(total_rewards)
        print ("Score over time: " +  str(sum(rewards)/total_episodes))
        learning_data[episode, 2] = sum(rewards)/total_episodes 
    env.close()
    return learning_data
