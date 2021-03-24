from torch.distributions import Normal
from torch.optim import Adam

from utilities import get_total_gradient


class GeneratorWrapper:
    def __init__(self, nn, lr, sample_size, enemy_x_min, enemy_x_max):
        self.nn = nn
        self.sample_size = sample_size
        self.enemy_x_max = enemy_x_max
        self.enemy_x_min = enemy_x_min

        self.optim = Adam(nn.parameters(), lr=lr)

    def generate(self, d_in):
        mean, std = self.nn(d_in)
        distribution = Normal(mean, std)

        # Sample from the distribution and the log probabilities
        x = distribution.sample([self.sample_size])
        log_prob = distribution.log_prob(x)

        # Transpose to [batch_size, sample_size, 1]
        x = x.transpose(0, 1)
        log_prob = log_prob.transpose(0, 1)

        # Constrain the samples to a valid range
        x_constrained = x.clamp(self.enemy_x_min, self.enemy_x_max)

        # Compute the constrain loss
        constrain_loss = (x_constrained - x).abs()

        return x_constrained, log_prob, constrain_loss

    def fit(self, loss):
        self.optim.zero_grad()
        loss.backward()
        gradient = get_total_gradient(self.nn)
        self.optim.step()

        return gradient
