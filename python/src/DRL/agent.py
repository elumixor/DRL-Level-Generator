from typing import List, Tuple

import torch
import torch.nn as nn
from torch.distributions import Uniform, Categorical
from torch.optim import Adam

from layout import action_size, state_size
from utilities import bootstrap, normalize, rewards_to_go

hidden_size = 20

base = nn.Sequential(
    nn.Linear(state_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, hidden_size),
    nn.ReLU()
)

actor_head = nn.Sequential(
    base,
    nn.Linear(hidden_size, action_size),
    nn.Softmax(dim=-1)
)

critic_head = nn.Sequential(
    base,
    nn.Linear(hidden_size, 1)
)

# print(actor_head.state_dict().keys())
print(nn.Linear(5, 5).state_dict().keys())
# print(critic_head.state_dict().keys())
print(nn.Sequential().forward(torch.tensor([5])))
for p in actor_head.parameters():
    print(p.shape)

# print(critic_head.state_dict().keys())

# Actor maps state to probabilities of taking action
actor = nn.Sequential(
    nn.Linear(state_size, hidden_size),
    nn.ReLU(),
    # nn.Linear(hidden_size, hidden_size),
    # nn.ReLU(),
    nn.Linear(hidden_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, action_size),
    nn.Softmax(dim=-1)).cuda()

# Critic maps state to value of the state
critic = nn.Sequential(
    nn.Linear(state_size, hidden_size),
    nn.ReLU(),
    # nn.Linear(hidden_size, hidden_size),
    # nn.ReLU(),
    nn.Linear(hidden_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, 1)).cuda()

optim_actor = Adam(actor.parameters(), lr=0.01)
optim_critic = Adam(critic.parameters(), lr=0.005)

discounting = 0.99

Episode = Tuple[torch.tensor, torch.tensor, torch.tensor, torch.tensor]

total_means = []
epoch = 0


def fit_networks(loss_actor, loss_critic):
    optim_actor.zero_grad()
    loss_actor.backward()
    optim_actor.step()

    # optim_critic.zero_grad()
    # loss_critic.backward()
    # optim_critic.step()


class Agent:

    @staticmethod
    def infer(state: torch.tensor) -> torch.tensor:
        with torch.no_grad():
            p_tap = actor(state.cuda())
            return Categorical(probs=p_tap).sample() * 2 - 1

    @staticmethod
    def train(training_data: List[Episode]):
        global epoch, t
        epoch += 1
        loss_actor = 0
        loss_critic = 0
        total_len = 0

        total_rewards = []
        for states, actions, rewards, next_states in training_data:
            # A2C
            # values = critic(states)

            # last_state = next_states[-1].unsqueeze(0)
            # last_value = critic(last_state).item()
            # next_values = bootstrap(rewards, last_value, discounting)

            # advantage = (next_values - values).flatten()

            # loss_critic = loss_critic + .5 * (advantage ** 2).sum()

            # probabilities = actor(states)
            # probabilities = probabilities[range(
            #     states.shape[0]), actions.flatten()]
            # loss_actor = loss_actor - \
            #     (torch.log(probabilities) * advantage.detach()).sum()

            # VPG
            # Improvement: use discounted rewards to go
            weights = rewards_to_go(rewards, discounting).flatten()
            weights = normalize(weights)

            # Get probabilities, shape (episode_length * numz_actions)
            # Then select only the probabilities corresponding to sampled actions
            probabilities = actor(states)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss_actor -= (probabilities.log() * weights).sum()

            total_len += states.shape[0]

            total_rewards.append(rewards.sum())

        print(
            f'epoch {epoch}\t average total reward: {torch.tensor(total_rewards).mean()}')

        loss_actor = loss_actor / total_len
        loss_critic = loss_critic / total_len

        fit_networks(loss_actor, loss_critic)
