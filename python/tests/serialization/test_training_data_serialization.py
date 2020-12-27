import struct
from unittest import TestCase

import torch

import serialization as s
from serialization.training_data_serialization import get_episode_flat, episode_to_tensors, to_training_data

# training_data, bytes_read = to_list(training_data_bytes, get_episode(state_size, action_size), start_index)
print(get_episode_flat)
print(episode_to_tensors)
print(to_training_data)


def flatten(list_):
    return [item for sublist in list_ for item in sublist]


def flatten_episode(episode):
    return flatten([state + action + [reward] + next_state for state, action, reward, next_state in episode])


def episode_to_bytes(episode, state_size, action_size):
    transition_size = 2 * state_size + action_size + 1
    flat = flatten_episode(episode)
    return s.to_bytes(len(episode)) + \
           struct.pack(s.get_format(s.DataTypes.Float, s.Endianness.Native, transition_size * len(episode)), *flat)


class Tests(TestCase):
    def test_get_single_episode_from_bytes(self):
        action_size = 1
        state_size = 4

        state = [1, 2, 3, 4]
        next_state = [5, 5, 6, 7]
        action = [0]
        reward = 100

        transition = [state, action, reward, next_state]
        episode = [transition]

        b = episode_to_bytes(episode, state_size, action_size)
        value, bytes_read = get_episode_flat(state_size, action_size)(b, 0, None)

        self.assertEqual(flatten_episode(episode), value)

    def test_get_several_episodes_from_bytes(self):
        action_size = 1
        state_size = 4

        state = [1, 2, 3, 4]
        next_state = [5, 5, 6, 7]
        action = [0]
        reward = 100

        transition = [state, action, reward, next_state]
        transition2 = [[6, 7, 8, 9], [1], 500, [-1, 2, -.5, .25]]
        episode = [transition2, transition, transition2, transition2, transition]

        b = episode_to_bytes(episode, state_size, action_size)
        value, bytes_read = get_episode_flat(state_size, action_size)(b, 0, None)

        self.assertEqual(flatten_episode(episode), value)

    def test_episode_to_tensors(self):
        action_size = 1
        state_size = 4

        state = [1, 2, 3, 4]
        next_state = [5, 5, 6, 7]
        action = [0]
        reward = 100
        state2 = [6, 7, 8, 9]
        action2 = [1]
        reward2 = 500
        next_state2 = [-1, 2, -.5, .25]

        transition = [state, action, reward, next_state]
        transition2 = [state2, action2, reward2, next_state2]
        episode = [transition2, transition, transition2, transition2, transition]

        flat = flatten_episode(episode)
        states, actions, rewards, next_states = episode_to_tensors(flat, state_size, action_size, 'cpu')

        self.assertTrue(torch.all(states == torch.tensor([state2, state, state2, state2, state], dtype=torch.float32)))

        self.assertTrue(
                torch.all(
                        next_states == torch.tensor([next_state2, next_state, next_state2, next_state2, next_state], dtype=torch.float32)))

        self.assertTrue(torch.all(actions == torch.tensor([action2, action, action2, action2, action], dtype=torch.float32)))
        # self.assertTrue(torch.all(rewards == torch.tensor([reward2, reward, reward2, reward2, reward], dtype=torch.float32)).item())

    def test_episode_to_tensors(self):
        action_size = 1
        state_size = 4

        state = [1, 2, 3, 4]
        next_state = [5, 5, 6, 7]
        action = [0]
        reward = 100
        state2 = [6, 7, 8, 9]
        action2 = [1]
        reward2 = 500
        next_state2 = [-1, 2, -.5, .25]

        transition = [state, action, reward, next_state]
        transition2 = [state2, action2, reward2, next_state2]
        episode = [transition2, transition, transition2, transition2, transition]

        flat = flatten_episode(episode)
        states, actions, rewards, next_states = episode_to_tensors(flat, state_size, action_size, 'cpu')

        self.assertTrue(torch.all(states == torch.tensor([state2, state, state2, state2, state], dtype=torch.float32)))

        self.assertTrue(
                torch.all(
                        next_states == torch.tensor([next_state2, next_state, next_state2, next_state2, next_state], dtype=torch.float32)))

        self.assertTrue(torch.all(actions == torch.tensor([action2, action, action2, action2, action], dtype=torch.float32)))
