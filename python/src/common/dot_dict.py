class DotDict(dict):
    __getattr__, __setattr__ = dict.get, dict.__setitem__


def to_dot_dict(data):
    result = DotDict()
    for key, value in data.items():
        if isinstance(value, dict):
            value = to_dot_dict(value)

        result.__setitem__(key, value)

    return result
