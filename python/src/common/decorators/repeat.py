import functools


def repeat(times: int, message=None):
    assert times > 0

    def decorator(func):
        if message is None:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for _ in range(times):
                    result = func(*args, **kwargs)

                return result

            return wrapper

        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for i in range(times):
                    print(f"{message} {i}")
                    result = func(*args, **kwargs)

                return result

            return wrapper

    return decorator
