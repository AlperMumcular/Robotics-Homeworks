import tensorflow as tf
import numpy as np
import gym
import gym_examples

class PolicyNetwork(tf.keras.Model):
    def __init__(self, num_actions):
        super(PolicyNetwork, self).__init__()
        self.dense1 = tf.keras.layers.Dense(64, activation='relu')
        self.dense2 = tf.keras.layers.Dense(num_actions, activation='softmax')

    def call(self, state):
        x = self.dense1(state)
        return self.dense2(x)

class NaturalPolicyGradientAgent:
    def __init__(self, num_actions, epsilon_initial=1.0, epsilon_final=0.1, epsilon_anneal_episodes=20):
        self.policy_network = PolicyNetwork(num_actions)
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
        self.epsilon_initial = epsilon_initial
        self.epsilon_final = epsilon_final
        self.epsilon_anneal_episodes = epsilon_anneal_episodes
        self.epsilon = epsilon_initial

    def get_action(self, state):
        state = tf.convert_to_tensor([state], dtype=tf.float32)
        probabilities = self.policy_network(state)
        
        # Epsilon-greedy exploration
        if np.random.rand() < self.epsilon:
            action = np.random.choice(len(probabilities[0]))
        else:
            action = np.argmax(probabilities[0].numpy())

        return action

    def train_step(self, states, actions, advantages):
        with tf.GradientTape() as tape:
            probabilities = self.policy_network(states, training=True)
            action_masks = tf.one_hot(actions, len(probabilities[0]))
            selected_probabilities = tf.reduce_sum(action_masks * probabilities, axis=1)
            loss = -tf.reduce_sum(tf.math.log(selected_probabilities) * advantages)

        gradients = tape.gradient(loss, self.policy_network.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.policy_network.trainable_variables))

    def save_model(self, reward, filepath='./npgModels/policy_network_model'):
        self.policy_network.save(filepath + "_" + str(reward))

    def load_model(self, reward, filepath='./npgModels/policy_network_model'):
        self.policy_network = tf.keras.models.load_model(filepath+ "_" + str(reward))

def compute_advantages(rewards, gamma=0.95):
    discounted_rewards = []
    running_add = 0
    for r in rewards[::-1]:
        running_add = running_add * gamma + r
        discounted_rewards.append(running_add)
    discounted_rewards.reverse()
    return discounted_rewards - np.mean(discounted_rewards)

def main():
    env = gym.make("gym_examples/DangerousDave-v0", step_limit=3000)
    num_actions = env.action_space.n
    state_size = env.observation_space.shape[0]

    agent = NaturalPolicyGradientAgent(num_actions)
    total_timesteps = 0
    highestScore = -9999
    num_episodes = 1000
    avg_score = []
    for episode in range(num_episodes):
        state, _ = env.reset()
        done = False
        episode_states, episode_actions, episode_rewards = [], [], []
        episode_t = 0
        while not done:
            action = agent.get_action(state)
            next_state, reward, term, trun, _ = env.step(action)
            total_timesteps += 1
            episode_t += 1
            done = term or trun
            episode_states.append(state)
            episode_actions.append(action)
            episode_rewards.append(reward)

            state = next_state

        episode_states = tf.convert_to_tensor(episode_states, dtype=tf.float32)
        episode_actions = tf.convert_to_tensor(episode_actions, dtype=tf.int32)
        episode_rewards = np.array(episode_rewards, dtype=np.float32)

        advantages = compute_advantages(episode_rewards)
        agent.train_step(episode_states, episode_actions, advantages)

        total_reward = sum(episode_rewards)
        avg_score.append(total_reward)
        print(f"Total T: {total_timesteps} Episode: {episode + 1} Episode T: {episode_t + 1} Reward: {total_reward} Average Reward: {np.mean(avg_score[-100:])}\n")
        
        # Anneal epsilon for exploration
        if episode < agent.epsilon_anneal_episodes:
            agent.epsilon = agent.epsilon_initial - \
                            (agent.epsilon_initial - agent.epsilon_final) * (episode / agent.epsilon_anneal_episodes)
        
        if total_reward > highestScore:
            highestScore = total_reward
            agent.save_model(reward=highestScore)
        
        with open('./results/npg.txt', 'a') as f:
                f.write(f"Total T: {total_timesteps} Episode: {episode + 1} Episode T: {episode_t + 1} Reward: {total_reward} Average Reward: {np.mean(avg_score[-100:])}\n")

    env.close()

if __name__ == "__main__":
    main()
