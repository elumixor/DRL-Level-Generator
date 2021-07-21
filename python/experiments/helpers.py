from environments import PendulumEnvJIT
from environments.pendulum import State
from environments.pendulum.state import enemy_x as s_enemy_x, size as state_size, create_variable
from evaluators.utils import weight_skills
from numba import njit, prange

from evaluators import TrajectoryRewardsEvaluator, DirectEvaluator
from evaluators.direct_actor import DirectActor
from shared_parameters import *


def create_actors(num_actors, actor_class=DirectActor):
    skills = np.linspace(0, 1, num_actors, dtype=np.float32)
    actors = np.array([actor_class(skill) for skill in skills])
    weights = weight_skills(skills, skill_weighting.mean, skill_weighting.std, skill_weighting.skew)

    return actors, weights


@njit
def create_state(enemy_x):
    return State(bob_radius, max_angle, connector_length, vertical_speed, current_angle, position, angular_speed,
                 enemy_radius, enemy_x, enemy_y)


@njit
def create_state_variable(enemies):
    return create_variable(bob_radius, max_angle, connector_length, vertical_speed, current_angle, position,
                           angular_speed, enemy_radius, enemies)


@njit(parallel=True)
def _x2states(x):
    x = x.flatten()
    y = np.zeros((x.shape[0], state_size), dtype=np.float32)
    for i in prange(len(x)):
        y[i] = create_state(x[i])

    return y


def x2states(x):
    s = x.shape[:-1] if x.ndim > 1 else x.shape
    return _x2states(x).reshape(*s, state_size)


@njit(parallel=True)
def states2x(x):
    original_shape = x.shape
    x = x.reshape(-1, state_size)
    y = np.zeros((x.shape[0]), dtype=np.float32)
    for i in prange(x.shape[0]):
        y[i] = x[i][s_enemy_x]

    return y.reshape(original_shape[:-1])


class SimpleTRE(TrajectoryRewardsEvaluator):
    def __init__(self, num_actors=num_actors, skill_weighting=skill_weighting, num_evaluations=num_evaluations,
                 max_trajectory_length=max_trajectory_length):
        env = PendulumEnvJIT()

        skills = np.linspace(0, 1, num_actors)
        actors = [DirectActor(skill) for skill in skills]

        # Also compute the weighting of each skill, w.r.t. the skewed normal distribution
        actors_weights = weight_skills(skills, skill_weighting.mean, skill_weighting.std, skill_weighting.skew)

        super(SimpleTRE, self).__init__(env, actors, actors_weights, num_evaluations, max_trajectory_length)

    def evaluate_x(self, x):
        return self.evaluate(x2states(x))

    def evaluate(self, states: np.ndarray) -> np.ndarray:
        if states.ndim == 1:
            s = states.reshape([1, 1, state_size])
        elif states.ndim == 2:
            s = states.reshape([states.shape[0], 1, state_size])

        d_out = super(SimpleTRE, self).evaluate(s)

        if states.ndim == 1:
            return d_out.flatten()

        return d_out.reshape(states.shape[:-1])


class SimpleDE(DirectEvaluator):
    def __init__(self):
        super().__init__(connector_length, max_angle, enemy_radius, bob_radius)

    def evaluate(self, state):
        # DirectEvaluator evaluates x, but the SimpleEvaluator accepts the full state
        return super().evaluate(states2x(state))

    def evaluate_x(self, x):
        return super().evaluate(x)
