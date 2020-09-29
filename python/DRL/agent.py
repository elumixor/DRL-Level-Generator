import torch
import torch.nn as nn
from torch.distributions import Uniform, Categorical
from torch.optim import Adam

from layout import action_size, state_size
from utilities import bootstrap, normalize

hidden_size = 20

# Actor maps state to probabilities of taking action
actor = nn.Sequential(
    nn.Linear(state_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, action_size),
    nn.Softmax(dim=-1)).cuda()

# Critic maps state to value of the state
critic = nn.Sequential(
    nn.Linear(state_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, 1)).cuda()

optim_actor = Adam(actor.parameters(), lr=0.01)
optim_critic = Adam(critic.parameters(), lr=0.005)

discounting = 0.99


class Agent:
    @staticmethod
    def infer(state: torch.tensor) -> torch.tensor:
        p_tap = actor(state.cuda())
        print(p_tap)
        return Categorical(probs=p_tap).sample() * 2 - 1

    @staticmethod
    def train(training_data):
        states, selected_actions, rewards, next_states = training_data

        # 2nd step: use advantage function, estimated by critic
        # bootstrap estimated next state values with rewards TD-1
        values = critic(states)

        last_state = next_states[-1].unsqueeze(0)

        last_value = critic(last_state).item()
        next_values = bootstrap(rewards, last_value, discounting)

        advantages = normalize(next_values - values).flatten()

        loss_critic = .5 * (advantages ** 2).sum()

        # Get probabilities, shape (episode_length * num_actions)
        # Then select only the probabilities corresponding to sampled actions
        probabilities = actor(states)
        probabilities = probabilities[range(states.shape[0]), selected_actions.long().flatten()]
        loss_actor = (-torch.log(probabilities) * advantages.detach()).sum()

        length = states.shape[0]

        loss_actor = loss_actor / length
        loss_critic = loss_critic / length

        optim_actor.zero_grad()
        loss_actor.backward()
        optim_actor.step()

        optim_critic.zero_grad()
        loss_critic.backward()
        optim_critic.step()
