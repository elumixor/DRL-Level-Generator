import abc

from torch import Tensor


class AbstractEvaluator(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, embeddings: Tensor, *args, **kwargs) -> Tensor:
        """
        Evaluates embeddings' difficulty
        :param embeddings: Levels in embedding space, shape (num_levels, embedding_size)
        :return: Evaluated difficulty, shape (num_embeddings, 1)
        """
        pass

    def __call__(self, embeddings: Tensor, *args, **kwargs) -> Tensor:
        return self.evaluate(embeddings, *args, **kwargs)
