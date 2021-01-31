from typing import Tuple, List, Optional

import torch

from rendering import RenderingContext, Color
from .enemy import Enemy
from .pendulum import Pendulum
from .transition import transition as T, interpret_state, observation_size, \
    action_size, state_size, interpret_generated_parameters, parameters_size, interpret_static_configuration
from ..renderable_environment import RenderableEnvironment


class PendulumEnvironment(RenderableEnvironment):
    def __init__(self, rendering_context: RenderingContext):
        super().__init__(rendering_context)

        # Our environments serve two purposes: to sample the trajectory, and two render them
        #
        # As we don't always want to render every state or trajectory, we will skip the overhead
        # of creating a new environment every time. We will instead perform a lazy rendering on-demand
        #
        # We use the following flag to indicate whether the rendering-required actions should be performed
        self._rendering_ready = False

        # We store the last state to be used for rendering
        self._last_state: Optional[torch.tensor] = None

        # As we re-use environment, we only declare the needed fields here
        # setup() is used when we want to update the environment parameters
        # reset() is used to reset the environment to a new trajectory

        # Configurations are used on reset()
        self.static_configuration: Optional[torch.tensor] = None
        self.starting_state: Optional[torch.tensor] = None

        # Pendulum game object
        self.pendulum: Optional[Pendulum] = None

        # Enemies game objects
        self.enemies: Optional[List[Enemy]] = None

    # We will use the with-pattern
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cleanup()
        self.game_object.parent = None

    @property
    def observation_size(self):
        return observation_size

    @property
    def action_size(self):
        return action_size

    @property
    def state_size(self):
        return state_size

    @property
    def parameters_size(self):
        return parameters_size

    def reset(self) -> torch.tensor:
        """
        Called at the start of each trajectory
        :returns: The starting state
        """
        self._last_state = self.starting_state

    def transition(self, action: torch.tensor) -> Tuple[torch.tensor, float, bool]:
        # propagate to the transition function
        next_state, reward, done = T(self._last_state, action, self.static_configuration)

        # Save the state for rendering
        self._last_state = next_state

        return next_state, reward, done

    def render(self):
        # Perform necessary initializations for rendering, if not rendering-ready
        if not self._rendering_ready:
            self._initialize_for_render()

        # Put everything in place, regarding to the state
        self._setup_game_objects_from_state(self._last_state)

        # Render the frame
        super(PendulumEnvironment, self).render()

    def setup(self, generated_parameters: torch.tensor):
        """
        Setups the environment using parameters. This should be done once for every generated environment.
        On the contrary, reset() should be called on every trajectory start
        """
        self.static_configuration, self.starting_state = interpret_generated_parameters(generated_parameters)

    def _initialize_for_render(self):
        # Remove already created objects
        self._cleanup()

        pendulum_configuration, enemies_configurations = interpret_static_configuration(self.static_configuration)

        # Create and position the pendulum
        self.pendulum = Pendulum(pendulum_configuration)

        # Create and position game objects
        self.enemies = [Enemy(configuration) for configuration in enemies_configurations]

        # Add everything to the base game object as children
        self.game_object.add_child(self.pendulum, *self.enemies)

        # Set a pleasant background color
        self.rendering_context.clear_color = Color.greyscale(0.9)

        self._rendering_ready = True

    def _setup_game_objects_from_state(self, state: torch.tensor):
        # Interpret tensor to configurations
        pendulum_configuration, enemies_configurations = interpret_state(state)

        # Update the objects using their configurations
        self.pendulum.update(pendulum_configuration)

        for i, enemy in enumerate(self.enemies):
            enemy.update(enemies_configurations[i])

    def _cleanup(self):
        self.game_object.remove_children()
        self.pendulum = None
        self.enemies = None
