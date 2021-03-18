import torch


def calculate_diversity(batch_levels, batch_difficulties=None):
    differences = batch_levels.unsqueeze(-3) - batch_levels.unsqueeze(-2)
    differences = torch.linalg.norm(differences, dim=-1)

    if batch_difficulties is not None:
        weights = batch_difficulties.unsqueeze(-3) - batch_difficulties.unsqueeze(-2)
        weights = weights.squeeze(-1).abs()
    else:
        weights = 1

    return (weights * differences / 2).mean()
