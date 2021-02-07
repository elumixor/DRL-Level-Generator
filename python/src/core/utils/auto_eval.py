import functools


def auto_eval(*names):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            instance = func(*args, **kwargs)

            def eval():
                for attr in names:
                    getattr(instance, attr).eval()

            def train():
                for attr in names:
                    getattr(instance, attr).train()

            instance.eval = eval
            instance.train = train

            return instance

        return wrapper

    return decorator
