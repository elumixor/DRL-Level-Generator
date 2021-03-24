import torch

from evaluators.utils import calculate_diversity
from test_utils import BaseTest


class Test(BaseTest):
    def test_valid_shape(self):
        sample_size = 2
        batch_size = 5
        feature_size = 1

        x = torch.rand([batch_size, sample_size, feature_size])

        div = calculate_diversity(x)

        sequential = torch.zeros(batch_size)

        print(x)

        for j, batch in enumerate(x):
            total = 0
            count = 1

            for i, a in enumerate(batch):
                for b in batch[i + 1:]:
                    print(a, "and", b)

                    diff = torch.linalg.norm(a - b)
                    # print(diff, (a - b).abs())
                    total += diff
                    count += 1

            total /= count
            sequential[j] = total

        sequential = sequential.mean()
        print(div, sequential)
