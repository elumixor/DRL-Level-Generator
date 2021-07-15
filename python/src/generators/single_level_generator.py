from typing import Optional, List

from torch import Tensor
from torch.nn import Module, functional as F
from torch.optim import Adam

from utils import MLP
from .abstract_generator import AbstractGenerator


class SingleLevelGenerator(AbstractGenerator):
    """
    This generator takes in a difficulty and outputs a single level embedding w.r.t. to the difficulty
    """

    def __init__(self, bounds: Tensor, hidden: Optional[List[int]] = None, activation: Optional[Module] = None,
                 optimizer_class=None, lr=0.01):
        super().__init__(bounds)

        if optimizer_class is None:
            optimizer_class = Adam

        # The actual network, which is a simple multi-layered perceptron
        self.nn = MLP(in_size=1, out_size=self.embedding_size, hidden=hidden, activation=activation)
        self.optim = optimizer_class(self.nn.parameters(), lr=lr)

        self.d_in: Optional[Tensor] = None

    def generate(self, d_in: Tensor):
        """
        Generates levels
        :param d_in: Batch of input difficulties. Shape (batch_size, 1)
        :return: Generated levels. Shape (batch_size, embedding_size)
        """
        if d_in.ndim != 2 or d_in.shape[1] != 1:
            raise Exception(f"'d_in' should have shape (batch_size, 1), but was {d_in.shape}")

        if d_in.min() < 0 or d_in.max() > 1:
            raise Exception(f"'d_in' should be in [0, 1] range, but was in [{d_in.min()}, {d_in.max()}]")

        # Save inputs for the backwards step
        self.d_in = d_in

        # Generate embeddings
        embeddings = self.nn(d_in)

        # todo: There's no guarantee that the generated embeddings are in the correct range
        #       thus we may need to clamp them to the valid range

        # The generated embeddings are generated in [0, 1] range. Thus, we need to remap to the embedding space
        embeddings = self.remap(embeddings)

        return embeddings

    def update(self, d_out: Tensor):
        """
        Updates the generator by minimizing the difference between the input difficulties, that were used to generate
        the levels, and the output real difficulty of the generated levels.

        :param d_out: Output difficulty, obtained from difficulty evaluation of the generated levels
        :return: Loss
        """
        if self.d_in is None:
            raise Exception(f"'d_in' is None. Run the forward pass first.")

        if self.d_in.shape != d_out.shape:
            raise Exception(
                f"'d_in' shape should be equal to 'd_out' shape, but were {self.d_in.shape} and {d_out.shape}")

        # Minimize the difference between the input and the output difficulties
        loss = F.mse_loss(self.d_in, d_out)

        # Perform gradient step
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        # Clear the recorded d_in
        self.d_in = None

        return loss
