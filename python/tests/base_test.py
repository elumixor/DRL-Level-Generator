from typing import Optional
from unittest import TestCase

from utilities import approx


class BaseTest(TestCase):
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
