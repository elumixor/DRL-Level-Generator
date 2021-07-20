import numpy as np
from scipy.stats import skewnorm


def running_average(arr, smoothing=0.8):
    size = len(arr)
    res = np.zeros(size)

    if size == 0:
        return res

    res[0] = arr[0]
    for i in range(1, size):
        res[i] = res[i - 1] * smoothing + arr[i] * (1 - smoothing)

    return res


def constrained_skewnorm(skills, mean, std, skew) -> np.ndarray:
    cdf_0 = skewnorm.cdf(0, skew, loc=mean, scale=std)
    cdf_1 = skewnorm.cdf(1, skew, loc=mean, scale=std)
    diff = cdf_1 - cdf_0

    weights = skewnorm.pdf(skills, skew, loc=mean, scale=std) / diff
    return weights / weights.sum()
