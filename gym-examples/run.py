import gym_examples
import gym as gymnasium
env = gymnasium.make('gym_examples/DangerousDave-v0')
env.reset()

for i in range(10000):
    env.render()
    print("a")
    
    #env.step(env.action_space.sample())