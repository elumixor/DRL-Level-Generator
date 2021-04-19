import torch

from .convergence_checker import ConvergenceChecker


@torch.no_grad()
def get_total_gradient(nn):
    total_grad = 0.0
    count = 0

    for p in nn.parameters():
        total_grad += p.grad.data.abs().mean()
        count += 1

    return total_grad / count
