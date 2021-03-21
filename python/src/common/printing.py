from sty import fg, ef

from common import singleton

_styles = dict()


def set_style(type: str, r=255, g=255, b=255, bold=False, italic=False):
    _styles[type] = (r, g, b, bold, italic)


def get_styles():
    return _styles


def style(*values, r=255, g=255, b=255, bold=False, italic=False, type=None):
    if type is not None:
        r, g, b, bold, italic = _styles[type]

    s = ""
    if bold:
        s += ef.bold

    if italic:
        s += ef.italic

    s += fg(r, g, b)

    s += " ".join([str(v) for v in values])

    s += fg.rs

    if bold or italic:
        s += ef.rs

    return s


set_style("bold", bold=True)
set_style("reward", bold=True, r=100, g=255, b=100)
set_style("path", bold=True, r=150, g=150, b=255)
set_style("good", r=150, g=220, b=100)
set_style("bad", r=220, g=100, b=100)


@singleton
class Printer:
    def __call__(self, *args, r=255, g=255, b=255, bold=False, italic=False, type=None, **kwargs):
        print(style(*args, r=r, g=g, b=b, bold=bold, italic=italic, type=type), **kwargs)

    def reward(self, value, title="reward", capitalize=True, separator=": "):
        if capitalize:
            title = title.capitalize()

        print(style(f"{title}{separator}", type="bold") + style(value, type="reward"))

    def save(self, path: str, title="saving to", capitalize=True, separator=": "):
        if capitalize:
            title = title.capitalize()

        print(f"{title}{separator}" + style(path, type="path"))

    def good(self, value: str):
        self(value, type="good")

    def bad(self, value: str):
        self(value, type="bad")


log = Printer()
