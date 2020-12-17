import numpy as np


def normalize(tensor):
    # std = tensor.std()
    # if torch.isnan(std) or std == 0:
    #     print("nan)))")
    #     return tensor

    return tensor - tensor.mean()


def running_average(arr, smoothing=0.8):
    size = len(arr)
    res = np.zeros(size)

    if size == 0:
        return res

    res[0] = arr[0]
    for i in range(1, size):
        res[i] = res[i - 1] * smoothing + arr[i] * (1 - smoothing)

    return res
