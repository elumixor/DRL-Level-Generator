import time

import torch

duration = 0
for _ in range(100):
    a = torch.rand([100, 100, 10])

    result = ((a.unsqueeze(2) - a.unsqueeze(1)) ** 2).sum(dim=-1).sqrt()

    start = time.perf_counter_ns()
    result.triu().sum()
    end = time.perf_counter_ns()

    duration += end - start

print(duration)

duration = 0
for _ in range(100):
    a = torch.rand([100, 100, 10])

    result = ((a.unsqueeze(2) - a.unsqueeze(1)) ** 2).sum(dim=-1).sqrt()

    start = time.perf_counter_ns()
    result.sum() / 2
    end = time.perf_counter_ns()

    duration += end - start

print(duration)
