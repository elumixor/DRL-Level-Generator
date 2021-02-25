import random
from typing import Tuple, Optional

import torch

from core.environments import RenderableEnvironment
from rendering import RenderingContext, Color
from .enemy import Enemy
from .generators import PendulumGenerator
from .pendulum import Pendulum
from .state import PendulumState
from .transition import transition


class PendulumEnvironment(RenderableEnvironment):
    def __init__(self, rendering_context: RenderingContext, generator: PendulumGenerator,
                 difficulty: Optional[float] = None):
        super().__init__(rendering_context)

        self.generator = generator

        # Our environments serve two purposes: to sample the trajectory, and two render them
        #
        # As we don't always want to render every observation or trajectory, we will skip the overhead
        # of creating a new environment every time. We will instead perform a lazy rendering on-demand
        #
        # We use the following flag to indicate whether the rendering-required actions should be performed
        self._rendering_ready = False

        # We store the last observation to be used for rendering
        self.state: Optional[PendulumState] = None

        # As we re-use environment, we only declare the needed fields here
        # setup() is used when we want to update the environment parameters
        # reset() is used to reset the environment to a new trajectory

        # Pendulum game object
        self.pendulum: Optional[Pendulum] = None

        # Enemies game objects
        self.enemy: Optional[Enemy] = None

        # Difficulty with which the generator gets called
        self.difficulty = difficulty

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        self.game_object.parent = None

    @property
    def state_size(self):
        return len(PendulumState)

    @property
    def observation_size(self):
        return self.state_size

    @property
    def action_size(self):
        return 2

    def reset(self, difficulty: Optional[float] = None, seed: Optional[float] = None) -> PendulumState:
        # Generate random seed randomly, if not specified
        if seed is None:
            seed = random.random()

        # Use the last difficulty, if none specified
        # Otherwise store the new difficulty
        if difficulty is None:
            difficulty = self.difficulty
        else:
            self.difficulty = difficulty

        if difficulty is None:
            raise ValueError("Difficulty should be specified at least once")

        # Generate new starting observation, internally split into the static configuration and observation
        self.state = self.generator.generate(difficulty, seed)
        self.cleanup()
        return self.state

    def transition(self, action: torch.Tensor) -> Tuple[torch.Tensor, float, bool]:
        # propagate to the transition function
        next_state, reward, done = transition(self.state, action)

        # Save the observation for rendering
        self.state = next_state

        return self.get_observation(next_state), reward, done

    def get_observation(self, state: PendulumState):
        return state

    def render(self):
        # Perform necessary initializations for rendering, if not rendering-ready
        if not self._rendering_ready:
            self.initialize_for_render()

        # Put everything in place, regarding to the observation
        self.setup_game_objects_from_state(self.state)

        # Render the frame
        super(PendulumEnvironment, self).render()

    def initialize_for_render(self):
        # Remove already created objects
        self.cleanup()

        # Create and position the pendulum
        self.pendulum = Pendulum(self.state)

        # Create and position game objects
        self.enemy = Enemy(self.state)

        # Add everything to the base game object as children
        self.game_object.add_child(self.pendulum, self.enemy)

        # Set a pleasant background color
        self.rendering_context.clear_color = Color.greyscale(0.9)

        self._rendering_ready = True

    def setup_game_objects_from_state(self, state: PendulumState):
        # Update the objects using their configurations
        self.pendulum.update(state)

    def cleanup(self):
        self.game_object.remove_children()
        self.pendulum = None
        self.enemy = None
        self._rendering_ready = False
