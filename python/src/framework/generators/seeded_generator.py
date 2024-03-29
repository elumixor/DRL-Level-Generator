from typing import Optional, List, Callable

import torch
from torch import Tensor
from torch.nn import Module, functional as F, LeakyReLU
from torch.optim import Adam

from utils import MLP
from .abstract_generator import AbstractGenerator


class SeededGenerator(AbstractGenerator):
    """
    This generator takes in a difficulty, and a n-dimensional seed, thus being able to generate multiple levels
    w.r.t. to the single difficulty
    """

    def __init__(self, bounds: Tensor, hidden: Optional[List[int]] = None, activation: Optional[Module] = None,
                 optimizer_class=None, lr=0.01, loss_function: Optional[Callable[[Tensor, Tensor], Tensor]] = None,
                 offsets_weight: float = 1.0):
        super().__init__(bounds)

        if optimizer_class is None:
            optimizer_class = Adam

        if loss_function is None:
            loss_function = F.mse_loss

        if activation is None:
            activation = LeakyReLU()

        # The actual network, which is a simple multi-layered perceptron
        self.nn = MLP(in_size=1 + self.embedding_size, out_size=self.embedding_size, hidden=hidden,
                      activation=activation)

        # todo: seed the network so it generates small offsets (or is that really necessary?)

        self.optim = optimizer_class(self.nn.parameters(), lr=lr)
        self.loss_function = loss_function

        self.d_in: Optional[Tensor] = None
        self.offsets: Optional[Tensor] = None

        self.offsets_weight = offsets_weight

    def parameters(self):
        return self.nn.parameters()

    def cuda(self):
        return self.device("cuda")

    def cpu(self):
        return self.device("cpu")

    def device(self, device):
        self.nn.to(device=device)

        self.bounds = self.bounds.to(device)
        self.bounds_min = self.bounds_min.to(device)
        self.bounds_diff = self.bounds_diff.to(device)

        return self

    def generate(self, inputs: Tensor) -> Tensor:
        """
        Generates levels
        :param inputs: Batch of input difficulties and input seeds. Shape (batch_size, 1 + embedding_size)
        :return: Generated levels in the embedding space. Shape (batch_size, embedding_size)
        """
        if inputs.ndim != 2 or inputs.shape[1] != (1 + self.embedding_size):
            raise Exception(f"'d_in' should have shape (batch_size, {1 + self.embedding_size}), but was {inputs.shape}")

        d_in, seeds = inputs[:, :1], inputs[:, 1:]

        if d_in.min() < 0 or d_in.max() > 1:
            raise Exception(f"'d_in' should be in [0, 1] range, but was in [{d_in.min()}, {d_in.max()}]")

        # todo: Check that seeds are within the bounds as well

        # Transform the seeds from the embedding space to the [0, 1] space
        seeds = self.from_embedding(seeds)

        # Generate offsets from the inputs
        offsets = self.nn(inputs)

        # Save data for the backwards step
        self.d_in = d_in
        self.offsets = offsets

        # todo: There's no guarantee that the generated offsets are in the correct range
        #       thus we may need to clamp them to the valid range

        # The generated offsets are in [0, 1] range. Thus, we need to remap them to the embedding space
        offsets = self.to_embedding(offsets)

        # The generated levels are then the seeds + the offsets
        return seeds + offsets

    def update(self, d_out: Tensor):
        """
        Updates the generator by minimizing the difference between the input difficulties, that were used to generate
        the levels, and the output real difficulty of the generated levels.

        Also minimizes the generated offsets, which is crucial for correct training.

        :param d_out: Output difficulty, obtained from difficulty evaluation of the generated levels
        :return: Tuple (difficulty_loss, offsets_loss)
        """
        if self.d_in is None or self.offsets is None:
            raise Exception(f"Run the forward pass first.")

        if self.d_in.shape != d_out.shape:
            raise Exception(f"'d_in' shape should be equal to 'd_out' shape, but were {self.d_in.shape} and "
                            f"{d_out.shape}")

        # Minimize the difference between the input and the output difficulties
        difficulty_loss = self.loss_function(self.d_in, d_out)

        # Also minimize generated offsets. This is crucial!
        offsets_loss = torch.norm(self.offsets, dim=-1).mean()

        loss = difficulty_loss + self.offsets_weight * offsets_loss

        # Perform gradient step
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        # Clear the recorded d_in
        self.d_in = None
        self.offsets = None

        return difficulty_loss, offsets_loss
