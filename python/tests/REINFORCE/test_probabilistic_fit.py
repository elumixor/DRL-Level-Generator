import torch
from torch.distributions import Normal
from torch.nn import Module, Linear, Softplus
from torch.optim import Adam

from generator import Generator
from test_utils import BaseTest, ConvergenceChecker

convergence_length = 100
convergence_threshold = 1e-2
epochs = 5000
lr = 0.01
# weight_decay = 1e-5
weight_decay = 0.0


def convergence_checker():
    return ConvergenceChecker(convergence_length, convergence_threshold)


class NN(Module):
    def __init__(self):
        super().__init__()

        self.l1 = Linear(1, 4)
        self.mean = Linear(4, 1)
        self.std = Linear(4, 1)
        self.softplus = Softplus()

    def forward(self, x):
        x = self.l1(x).relu()

        mean = self.mean(x)
        std = self.softplus(self.std(x)) + 0.01

        return mean, std


class TestStaticTarget(BaseTest):
    @torch.no_grad()
    def test_shapes(self):
        generator = Generator()

        batch_size = 100
        level_size = 1

        d_in = torch.rand([batch_size, level_size])
        mean, std = generator.forward(d_in)

        self.assertEqual(d_in.shape, mean.shape)
        self.assertEqual(d_in.shape, std.shape)
        self.assertEqual(mean.shape, torch.Size([batch_size, level_size]))

        sample_size = 1000
        dist = Normal(mean, std)
        sample = dist.sample([sample_size])

        self.assertEqual(sample.shape, torch.Size([sample_size, batch_size, level_size]))

        log_prob = dist.log_prob(sample)

        self.assertEqual(log_prob.shape, torch.Size([sample_size, batch_size, level_size]))

        log_prob = log_prob.transpose(0, 1)
        sample = sample.transpose(0, 1)

        self.assertEqual(log_prob.shape, torch.Size([batch_size, sample_size, level_size]))
        self.assertEqual(sample.shape, torch.Size([batch_size, sample_size, level_size]))

        # let's just assume this d_out
        d_out = sample

        differences_direct = torch.linalg.norm(d_out - d_in.unsqueeze(1), dim=-1)

        # cyclic implementation
        differences_cyclic = torch.zeros([batch_size, sample_size])
        for d, difficulty in enumerate(d_out):
            d_in_current = d_in[d]

            for l, d_out_current in enumerate(difficulty):
                difference = torch.linalg.norm(d_in_current - d_out_current, dim=-1)

                differences_cyclic[d][l] = difference

        self.assertTrue(torch.all(differences_direct == differences_cyclic))

        self.assertEqual(differences_direct.shape, torch.Size([batch_size, sample_size]))

        weighted = log_prob * differences_direct.unsqueeze(-1)
        self.assertEqual(weighted.shape, torch.Size([batch_size, sample_size, level_size]))
        self.assertEqual(weighted.shape, torch.Size([batch_size, sample_size, level_size]))

    @BaseTest.confidence(10, 10)
    def test_minimization(self):
        target = torch.tensor([10.0])

        mean = torch.tensor(0.0, requires_grad=True)
        std = torch.tensor(1.0, requires_grad=True)

        softplus = Softplus()

        validation_convergence = convergence_checker()

        for epoch in range(epochs):
            dist = Normal(mean, softplus(std) + 0.01)

            sample = dist.sample([100])
            differences = (sample - target).abs()

            log_prob = dist.log_prob(sample)

            loss = (differences * log_prob).mean()

            loss.backward()

            with torch.no_grad():
                mean -= lr * mean.grad
                std -= lr * std.grad

                mean.grad.zero_()
                std.grad.zero_()

                validation_difference = (mean - target).abs().mean()

            if validation_convergence.step(validation_difference):
                return

        self.fail(f"Did not converge after {epochs} epochs")

    @BaseTest.confidence(10, 10)
    def test_minimization_adam(self):
        target = torch.tensor(10.0)

        mean = torch.tensor(0.0, requires_grad=True)
        std = torch.tensor(1.0, requires_grad=True)

        softplus = Softplus()

        optim = Adam([mean, std], lr=lr)

        validation_convergence = convergence_checker()

        for epoch in range(epochs):
            dist = Normal(mean, softplus(std) + 0.01)

            sample = dist.sample([100])

            differences = (sample - target).abs()

            log_prob = dist.log_prob(sample)

            loss = (differences * log_prob).mean()

            with torch.no_grad():
                validation_diff = (mean - target).abs().mean().item()

            if validation_convergence.step(validation_diff):
                return

            optim.zero_grad()
            loss.backward()
            optim.step()

        self.fail(f"Did not converge after {epochs} epochs")

    @BaseTest.confidence(48, 50)
    def test_minimization_nn(self):
        target = torch.tensor(10.0)

        nn = NN()
        optim = Adam(nn.parameters(), lr=lr, weight_decay=weight_decay)
        validation_convergence = convergence_checker()

        epochs = 50000
        for epoch in range(epochs):
            mean, std = nn(target.unsqueeze(0))
            dist = Normal(mean, std)

            sample = dist.sample([100])
            log_prob = dist.log_prob(sample)

            differences = (sample - target).abs()

            loss = (differences * log_prob).mean()

            with torch.no_grad():
                validation_diff = (mean - target).abs().item()

            if validation_convergence.step(validation_diff):
                return

            optim.zero_grad()
            loss.backward()
            optim.step()

        self.fail(f"Did not converge after {epochs} epochs")


class TestMoving(BaseTest):
    @BaseTest.confidence(48, 50)
    def test_nn_random(self):
        nn = NN()
        optim = Adam(nn.parameters(), lr=lr, weight_decay=weight_decay)
        validation_convergence = convergence_checker()

        epochs = 50000
        batch_size = 100
        sample_size = 100

        for epoch in range(epochs):
            target = 10.0 * torch.rand([batch_size, 1])
            mean, std = nn(target)
            dist = Normal(mean, std)

            sample = dist.sample([sample_size])
            log_prob = dist.log_prob(sample)

            self.assertEqual(sample.shape, torch.Size([sample_size, batch_size, 1]))

            sample = sample.transpose(0, 1)
            log_prob = log_prob.transpose(0, 1)

            differences = (sample - target.unsqueeze(1)).abs()

            loss = (differences * log_prob).mean()

            with torch.no_grad():
                validation_diff = (mean - target).abs().mean().item()

            if validation_convergence.step(validation_diff):
                return

            optim.zero_grad()
            loss.backward()
            optim.step()

        # self.plot(validation_convergence.values)
        self.fail(f"Did not converge after {epochs} epochs")

    @BaseTest.confidence(48, 50)
    def test_nn_systematic(self):
        nn = NN()
        optim = Adam(nn.parameters(), lr=lr, weight_decay=weight_decay)
        validation_convergence = convergence_checker()

        epochs = 50000
        batch_size = 100
        sample_size = 100

        target = torch.linspace(0.0, 10.0, batch_size).unsqueeze(-1)
        for epoch in range(epochs):
            mean, std = nn(target)
            dist = Normal(mean, std)

            sample = dist.sample([sample_size])
            log_prob = dist.log_prob(sample)

            self.assertEqual(sample.shape, torch.Size([sample_size, batch_size, 1]))

            sample = sample.transpose(0, 1)
            log_prob = log_prob.transpose(0, 1)

            differences = (sample - target.unsqueeze(1)).abs()

            loss = (differences * log_prob).mean()

            with torch.no_grad():
                validation_diff = (mean - target).abs().mean().item()

            if validation_convergence.step(validation_diff):
                return

            optim.zero_grad()
            loss.backward()
            optim.step()

        self.fail(f"Did not converge after {epochs} epochs")


class TestConstrained(BaseTest):
    @BaseTest.confidence(48, 50)
    def test_nn_single(self):
        nn = NN()
        optim = Adam(nn.parameters(), lr=lr, weight_decay=weight_decay)
        validation_convergence = convergence_checker()

        epochs = 50000
        sample_size = 100
        clamp_weight = 0.5

        penalties = []

        target = torch.tensor(10.0)
        x_min = target - 1
        x_max = target + 1

        for epoch in range(epochs):
            mean, std = nn(target.unsqueeze(0))
            dist = Normal(mean, std)

            x = dist.sample([sample_size])
            log_prob = dist.log_prob(x)

            clamped = x.clip(x_min, x_max)

            differences = (clamped - target).abs()
            penalty = (x - clamped).abs()
            penalties.append(penalty.mean().item())

            loss = ((differences + clamp_weight * penalty) * log_prob).mean()

            with torch.no_grad():
                clamped = mean.clip(x_min, x_max)
                validation_diff = (clamped - target).abs().mean().item()

            if validation_convergence.step(validation_diff):
                return

            optim.zero_grad()
            loss.backward()
            optim.step()

        self.plot(validation_convergence.values)
        self.plot(penalties)

        self.fail(f"Did not converge after {epochs} epochs")

    @BaseTest.confidence(48, 50)
    def test_nn_systematic(self):
        nn = NN()
        optim = Adam(nn.parameters(), lr=lr, weight_decay=weight_decay)
        validation_convergence = convergence_checker()

        epochs = 50000
        batch_size = 100
        sample_size = 99
        clamp_weight = 0.5

        target = torch.linspace(0.0, 10.0, batch_size).unsqueeze(-1)
        x_min = (target - 1).unsqueeze(1)
        x_max = (target + 1).unsqueeze(1)

        for epoch in range(epochs):
            mean, std = nn(target)
            dist = Normal(mean, std)

            x = dist.sample([sample_size])
            log_prob = dist.log_prob(x)

            x = x.transpose(0, 1)
            log_prob = log_prob.transpose(0, 1)

            clamped = torch.max(torch.min(x, x_max), x_min)

            differences = (clamped - target.unsqueeze(1)).abs()
            penalty = (x - clamped).abs()

            loss = ((differences + clamp_weight * penalty) * log_prob).mean()

            with torch.no_grad():
                clamped = torch.max(torch.min(mean, x_max.squeeze(1)), x_min.squeeze(1))
                validation_diff = (clamped - target).abs().mean().item()

            if validation_convergence.step(validation_diff):
                return

            optim.zero_grad()
            loss.backward()
            optim.step()

        self.fail(f"Did not converge after {epochs} epochs")

    @BaseTest.confidence(48, 50)
    def test_nn_random(self):
        nn = NN()
        optim = Adam(nn.parameters(), lr=lr, weight_decay=weight_decay)
        validation_convergence = convergence_checker()

        epochs = 50000
        batch_size = 100
        sample_size = 99
        clamp_weight = 0.5

        for epoch in range(epochs):
            target = 10.0 * torch.rand([batch_size, 1])
            x_min = (target - 1).unsqueeze(1)
            x_max = (target + 1).unsqueeze(1)

            mean, std = nn(target)
            dist = Normal(mean, std)

            x = dist.sample([sample_size])
            log_prob = dist.log_prob(x)

            x = x.transpose(0, 1)
            log_prob = log_prob.transpose(0, 1)

            clamped = torch.max(torch.min(x, x_max), x_min)

            differences = (clamped - target.unsqueeze(1)).abs()
            penalty = (x - clamped).abs()

            loss = ((differences + clamp_weight * penalty) * log_prob).mean()

            with torch.no_grad():
                clamped = torch.max(torch.min(mean, x_max.squeeze(1)), x_min.squeeze(1))
                validation_diff = (clamped - target).abs().mean().item()

            if validation_convergence.step(validation_diff):
                return

            optim.zero_grad()
            loss.backward()
            optim.step()

        self.fail(f"Did not converge after {epochs} epochs")
