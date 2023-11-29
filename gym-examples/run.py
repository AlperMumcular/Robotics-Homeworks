import gym_examples
import gym as gymnasium
env = gymnasium.make("gym_examples/DangerousDave-v0", step_limit=1453, render_mode="human")
env.reset()

for i in range(3000):
    
    #env.render()
    #print("a")
    
    #env.step(env.action_space.sample())
    if i < 1000:
        _, rew , term, trun, _ = env.step(3)
        print("Reward: ", rew)
    elif i == 1001:
        _, rew , term, trun, _ = env.step(1)
    elif i < 2000:
        _, rew , term, trun, _ = env.step(3)
        # print(trun)
    else:
        _, _ , term, _, _ = env.step(2)

    if term or trun:
            print(i)
            break    
        
print("Terminated: ", term)
print("Truncated:  ", trun)
env.close()