from typing import Callable, Iterable, Iterator, LiteralString, Self, cast
import re

try:
    import msvcrt

    platform = "win"
except ImportError:
    import termios
    import sys
    import tty

    platform = "unix"


class CharReader:
    buffer = ""
    instance = 0

    def __init__(self):
        self.i = 0
        self.idx = self.instance
        self.instance += 1

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> str:
        print(self.idx, f"'{self.buffer}'", self.i)
        if self.i < len(self.buffer):
            ch = self.buffer[self.i]
            self.i += 1
            return ch
        else:
            self.buffer += read_char()
            return next(self)


def read_char() -> str:
    if platform == "win":
        return msvcrt.getch().decode("utf-8")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def scan[T, U](initial: U, f: Callable[[U, T], U], iterable: Iterable[T]) -> Iterator[U]:
    state = initial
    yield from (state := f(state, x) for x in iterable)


mermaid_diagram_regex = re.compile(
    r"```mermaid\n\s*%% active\s*\n(.*)```", flags=re.RegexFlag.S
)


def get_diagram_from_markdown(markdown: str) -> str:
    return mermaid_diagram_regex.search(markdown).group(1)


type O = str
type Σ = str
