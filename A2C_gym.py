import gym
import torch
import numpy as np
from A2C_models import ActorCriticContinuous, ActorCriticDiscrete
from A2C_memory import Memory
from torch.distributions.categorical import Categorical
from torch.optim.lr_scheduler import StepLR
import gym_examples

"""
Implementation of Advantage-Actor-Critic for gym environments
"""

device = torch.device("cpu")


def select_action(model, state, mode):
    state = torch.Tensor(state).to(device)
    if mode == "continuous":
        mean, sigma, state_value = model(state)
        s = torch.distributions.MultivariateNormal(mean, torch.diag(sigma))
    else:
        probs, state_value = model(state)
        s = Categorical(probs)

    action = s.sample()
    entropy = s.entropy()

    return action.numpy(), entropy, s.log_prob(action), state_value


def evaluate(actor_critic, env, repeats, mode):
    actor_critic.eval()
    perform = 0
    timesteps = 0
    for _ in range(repeats):
        state= env.reset()[0]
        done = False
        while not done:
            
            state = torch.Tensor(state).to(device)
            with torch.no_grad():
                if mode == "continuous":
                    mean, sigma, _ = actor_critic(state)
                    m = torch.distributions.Normal(mean, sigma)
                else:
                    probs, _ = actor_critic(state)
                    m = Categorical(probs)
            action = m.sample()
            state, reward, term, trun,_ = env.step(action.numpy())
            done = term or trun
            perform += reward
            timesteps += 1
    actor_critic.train()
    return (perform/repeats, int(timesteps/repeats))


def train(memory, optimizer, gamma, eps):
    action_prob, values, disc_rewards, entropy = memory.calculate_data(gamma)

    advantage = disc_rewards.detach() - values

    policy_loss = (-action_prob*advantage.detach()).mean()
    value_loss = 0.5 * advantage.pow(2).mean()
    loss = policy_loss + value_loss - eps*entropy.mean()

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


def main(gamma=0.99, lr=5e-3, num_episodes=100, eps=0.001, seed=42, lr_step=100, lr_gamma=0.9, measure_step=1, 
         measure_repeats=20, horizon=100000, hidden_dim=64, env_name='gym_examples/DangerousDave-v0', render=False):
    """
    :param gamma: reward discount factor
    :param lr: initial learning rate
    :param num_episodes: total number of episodes performed in the environment
    :param eps: entropy regularization parameter (increases exploration)
    :param seed: random seed
    :param lr_step: every "lr_step" many episodes the lr is updated by the factor "lr_gamma"
    :param lr_gamma: see above
    :param measure_step: every "measure_step" many episodes the the performance is measured using "measure_repeats" many
    episodes
    :param measure_repeats: see above
    :param horizon: if not set to infinity limits the length of the episodes when training
    :param hidden_dim: hidden dimension used for the DNN
    :param env_name: name of the gym environment
    :param render: if True the environment is rendered twice every "measure_step" many episodes
    """
    env = gym.make(env_name, step_limit=3000)
    torch.manual_seed(seed)
    
    # check whether the environment has a continuous or discrete action space.
    if type(env.action_space) == gym.spaces.Discrete:
        action_mode = "discrete"
    elif type(env.action_space) == gym.spaces.Box:
        action_mode = "continuous"
    else:
        raise Exception("action space is not known")

    # Get number of actions for the discrete case and action dimension for the continuous case.
    if action_mode == "continuous":
        action_dim = env.action_space.shape[0]
    else:
        action_dim = env.action_space.n
    
    state_dim = env.observation_space.shape[0]

    if action_mode == "continuous":
        actor_critic = ActorCriticContinuous(action_dim=action_dim, state_dim=state_dim, hidden_dim=hidden_dim).to(device)
    else:
        actor_critic = ActorCriticDiscrete(action_dim=action_dim, state_dim=state_dim, hidden_dim=hidden_dim).to(device)

    optimizer = torch.optim.Adam(actor_critic.parameters(), lr=lr)
    scheduler = StepLR(optimizer, step_size=lr_step, gamma=lr_gamma)
    total_timesteps = 0
    performance = []
    rewards = []
    for episode in range(num_episodes):
        # reset memory
        memory = Memory()
        # display the episode_performance
        if episode % measure_step == 0:
            evalu = evaluate(actor_critic, env, measure_repeats, action_mode)
            performance.append([episode, evalu[0]])
            print("Episode: ", episode)
            print("rewards: ", performance[-1][1])
            print("lr: ", scheduler.get_last_lr())
            total_timesteps += evalu[1]
            episode_t = evalu[1]
            rewards.append(performance[-1][1])
            with open('npg.txt', 'a') as f:
                f.write(f"Total T: {total_timesteps} Episode: {episode + 1} Episode T: {episode_t + 1} Reward: {performance[-1][1]} Average Reward: {np.mean(rewards[-100:])}\n")
        state = env.reset()[0]

        done = False
        count = 0
        while not done and count < horizon:
            count += 1
            action, entropy, log_prob, state_value = select_action(actor_critic, state, action_mode)
            state, reward, term,trun, _ = env.step(action)
            done = term or trun

            if render and episode % int((measure_step)) == 0:
                env.render()

            # save the information
            memory.update(reward, entropy, log_prob, state_value)

        # train on the observed data
        train(memory, optimizer, gamma, eps)
        # update the learning rate
        scheduler.step()

    return actor_critic, performance


if __name__ == '__main__':
    main()