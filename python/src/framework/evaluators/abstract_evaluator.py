import abc

from torch import Tensor


class AbstractEvaluator(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, embeddings: Tensor, *args, **kwargs) -> Tensor:
        """
        Evaluates levels as embeddings
        :param embeddings: Levels in embedding space, shape (num_levels, embedding_size)
        :return: Difficulty for the levels, shape (num_levels, 1)
        """
        pass

    def __call__(self, levels: Tensor, *args, **kwargs) -> Tensor:
        return self.evaluate(levels, *args, **kwargs)
