# Required libs
import numpy as np
import torch
import random
import TD3 as TD3
import ReplayBuffer as ReplayBuffer
import gym_examples
import gym as gymnasium

if __name__ == "__main__":
    # Env create
    env = gymnasium.make("gym_examples/DangerousDave-v0", step_limit=1000)
    
    # Fix seeds in order to avoid randomness in the code/agent
    random.seed(10)

    #!!!!!!!!!!!!!!!!!!!!!!!!!
    seedNumber = 1 # You can set seed number as you desired, we tested between 1 and 6 (both included)
    #!!!!!!!!!!!!!!!!!!!!!!!!!
    env.reset()

    # Seeded Environment
    #env.reset(seed=seedNumber)

    # Fix seeds again
    env.action_space.seed(seedNumber)
    torch.manual_seed(seedNumber)
    np.random.seed(seedNumber)
    
    #print(env.observation_space.shape)
    # Get the dimension of state and action spaces
    total_observation_shape = sum(space.shape[0] for space in env.observation_space.values())
    state_dim = total_observation_shape
    #print(state_dim)
    #state_dim = env.observation_space.shape[0]
    action_dim = 1
    #print(action_dim)

    max_action = env.action_space.n - 1 # [1,1]

    # Create our agent
    policy=TD3.TD3(state_dim=state_dim, action_dim=action_dim, max_action=max_action, policy_noise= 0, noise_clip= 0)

    # Create replay buffer
    replay_buffer = ReplayBuffer.ReplayBuffer(state_dim, action_dim)
    
    # Lists for results (for graph purposes)
    evaluations=[]
    testevaluations=[]

    # Reset environment
    state, _ = env.reset()
    done, truncated = False, False
    #state = state[0] # state was tuple when we call reset, so state[0] was necessary to get the observation
    
    # Initial variables and their values for for-loop
    episode_reward = 0
    episode_timesteps = 0
    episode_num = 0
    
    # At most 1 M timesteps and first 25K move will be random
    max_timesteps = 1e6
    start_timesteps = 25e3
    
    # Timestep - for loop
    for t in range(int(max_timesteps)):
        # Exit condition - After reaching 1000 ep break the code
        if episode_num == 2500:
            exit()
        
        # For each time increase timestep
        episode_timesteps += 1

        # Select action randomly for first 25K timesteps - Algorithm Structure wants like this
        if t < start_timesteps:
            action = env.action_space.sample()
        # After 25K timesteps, choose action according to the policy
        else:
            state_policy = np.array([state[key] for key in ["agent_x", "agent_y", "trophy_x", "trophy_y", "door_x", "door_y"]], dtype=np.float32)
            action = (policy.select_action(np.array(state_policy)) + np.random.normal(0, max_action, size=action_dim)).clip(0, max_action)
            print(policy.select_action(np.array(state_policy)))
		
        # Perform action
        next_state, reward, done, truncated, _ = env.step(action) 
        # Update done condition terminated or truncated
        done_bool = float(done or truncated) if episode_timesteps < env.step_limit else 0

		# Store data in replay buffer
        state_buffer = np.array([state[key] for key in ["agent_x", "agent_y", "trophy_x", "trophy_y", "door_x", "door_y"]], dtype=np.float32)
        next_state_buffer = np.array([next_state[key] for key in ["agent_x", "agent_y", "trophy_x", "trophy_y", "door_x", "door_y"]], dtype=np.float32)
        replay_buffer.add(state_buffer, action, next_state_buffer, reward, done_bool)

        # Update state and ep reward
        state = next_state
        episode_reward += reward

		# Train agent after collecting sufficient data
        if t >= start_timesteps:
            policy.train(replay_buffer, 256)

        # End of an episode
        if done or truncated: 
            print("Episode: " + str(episode_num) + " Total reward: " + str(episode_reward))
            # Add the ep reward to the list
            evaluations.append(episode_reward)

            # Get average of the last 100 rewards
            avg_score = np.mean(evaluations[-100:])
			
            # Test in test environment seed
            #test_score = eval_policy(policy, seedNumber+10)

            # Add the test result to the list
            #testevaluations.append(test_score)

            # Get average of the last 100 test rewards
            #test_avg_score = np.mean(testevaluations[-100:])

            # --- You can disable it if you want ---
            #print(f"Total T: {t+1} Episode Num: {episode_num+1} Episode T: {episode_timesteps} Reward: {episode_reward:.3f} Seed: {seedNumber} Average Reward: {avg_score:.3f} Test Score: {test_score:.3f} Test Average Score: {test_avg_score:.3f}")

            # Write all results to the txt file, for graphing purposes
            #with open('./results/output_seed' + str(seedNumber) + '.txt', 'a') as f:
            #    f.write(f"Total T: {t+1} Episode Num: {episode_num+1} Episode T: {episode_timesteps} Reward: {episode_reward:.3f} Seed: {seedNumber} Average Reward: {avg_score:.3f} Test Score: {test_score:.3f} Test Average Score: {test_avg_score:.3f}\n")

            # Save model in episode 1000
            if episode_num == 1000:
                policy.save(f"./models/td3_seed{seedNumber}_1000")

			# Reset environment
            state, _ = env.reset()
            done, truncated = False, False
            #state = state[0] # State is tuple initially when we get from reset, so state[0] is required for obs space
            
            # Prepare variables for the next episode
            episode_reward = 0 
            episode_timesteps = 0
            episode_num += 1 
            
            