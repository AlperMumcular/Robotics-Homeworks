import gym_examples
import gym as gymnasium
env = gymnasium.make("gym_examples/DangerousDave-v0", step_limit=1000, render_mode="human")
env.reset()

for i in range(20000):

    #env.render()
    #print("a")


    #env.step(env.action_space.sample())
    obs, rew , term, trun, _ = env.step(env.action_space.sample())

    print(obs)
    if i % 1000 == 0:
        print("reset")

    if term or trun:
        env.reset()    
        
print("Terminated: ", term)
print("Truncated:  ", trun)
env.close()