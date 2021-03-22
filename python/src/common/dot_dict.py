class DotDict(dict):
    __getattr__, __setattr__ = dict.get, dict.__setitem__

    def __delattr__(self, item):
        self.__delitem__(item)


def to_dot_dict(data):
    if isinstance(data, dict):
        result = DotDict()
        for key, value in data.items():
            result[key] = to_dot_dict(value)
        return result

    elif isinstance(data, list):
        return [to_dot_dict(item) for item in data]

    return data
