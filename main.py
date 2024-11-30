from enum import Enum
from typing import Iterator
from FSM import FSM, UnexpectedSymbol, Q

from utils import (
    CharReader,
    O,
    scan,
    get_diagram_from_markdown,
)


def stepper(A: FSM, q0: Q) -> Iterator[tuple[Q, O]]:
    # states = scan(q0, A.δ, CharReader())
    # outputs = map(A.λ, states, CharReader())
    # return zip(states, outputs)
    reader = CharReader()
    while True:
        char = next(reader)
        q0 = A.δ(q0, char)
        yield q0, A.λ(q0, char)


def main():
    with open("docs.md", "r") as f:
        diagram = get_diagram_from_markdown(f.read())
        fsm = FSM.from_marmaid(diagram)

    for id, q in fsm.states.items():
        print(id, ":", q.name)

    for qᵢ, oᵢ in stepper(fsm, fsm.initial):
        print(qᵢ, oᵢ)


if __name__ == "__main__":
    main()
