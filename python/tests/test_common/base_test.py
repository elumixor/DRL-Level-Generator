import functools
from typing import Optional
from unittest import TestCase

from utilities import approx


class BaseTest(TestCase):
    @staticmethod
    def confidence(min_ok: int, total: int):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                succeeded = 0
                failed = 0
                max_failed = total - min_ok

                for i in range(1, total + 1):
                    try:
                        func(self, *args, **kwargs)
                        succeeded += 1

                        print(f"{i} ok: {succeeded}+{failed}/{total}")

                        if succeeded >= min_ok:
                            return

                    except AssertionError as e:
                        failed += 1

                        print(f"{i} failed: {succeeded}+{failed}/{total}")
                        print(e)

                        if failed > max_failed:
                            self.fail(f"Failed {failed}. Maximum allowed: {max_failed}/{total}")

            return wrapper

        return decorator

    def assertHasAttr(self, obj: object, attribute: str, msg: Optional[str] = None):
        if hasattr(obj, attribute):
            return

        if msg is None:
            msg = f"Attribute \"{attribute}\" was not present in {obj}"

        self.fail(msg)

    def assertNotHasAttr(self, obj: object, attribute: str, msg: Optional[str] = None):
        if not hasattr(obj, attribute):
            return

        if msg is None:
            msg = f"Attribute \"{attribute}\" was present in {obj}"

        self.fail(msg)

    def assertAlmostEqual(self, first: float, second: float, places: int = 7, msg=None,
                          delta=None) -> None:
        result = approx(first, second, 1 ** -places)
        if result:
            return

        if msg is None:
            msg = f"{first} did not equal {second}. Diff = {abs(first - second)}"

        self.fail(msg)

    def reset_experiment(self):
        self.current_values = dict()
        self.steps = dict()

    def assert_decreases(self, key, value, smoothing=0.9, window_size=10, strict=False, threshold=float("inf")):
        if key not in self.current_values:
            self.current_values[key] = [value]
            self.steps[key] = 1
            return

        self.steps[key] += 1
        window = self.current_values[key]
        current_value = window[-1]
        smoothed = current_value * smoothing + (1 - smoothing) * value

        window.append(smoothed)

        if len(window) < window_size:
            return

        previous = window[0]
        window.pop(0)

        if value < threshold:
            return

        if strict:
            if smoothed > previous:
                self.fail(f"\"{key}\" does not decrease after step {self.steps[key]}. "
                          f"Was: {current_value}. "
                          f"Became {smoothed}")

        else:
            if smoothed >= previous:
                self.fail(f"\"{key}\" does not decrease after step {self.steps[key]}. "
                          f"Was: {current_value}. "
                          f"Became {smoothed}")
