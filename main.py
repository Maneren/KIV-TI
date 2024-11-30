from enum import Enum
from typing import Iterator
from FSM import FSM, UnexpectedSymbol

from utils import (
    CharReader,
    Σ,
    O,
    scan,
    get_diagram_from_markdown,
)


class Q(Enum):
    E = "E"
    Odd = "Odd"
    Even = "Even"


def δ(q: Q, σ: Σ) -> Q:
    print(f"δ({q}, {σ})")
    match (q, σ):
        case (Q.E, "0"):
            return Q.Even
        case (Q.E, "1"):
            return Q.Odd
        case (Q.Odd, "0"):
            return Q.Odd
        case (Q.Odd, "1"):
            return Q.Even
        case (Q.Even, "0"):
            return Q.Even
        case (Q.Even, "1"):
            return Q.Odd

    raise UnexpectedSymbol


def λ(q: Q, σ: Σ) -> O:
    print(f"λ({q}, {σ})")
    match (q, σ):
        case (Q.E, "0"):
            return "e0"
        case (Q.E, "1"):
            return "e1"
        case (Q.Odd, "0"):
            return "O0"
        case (Q.Odd, "1"):
            return "O1"
        case (Q.Even, "0"):
            return "E0"
        case (Q.Even, "1"):
            return "E1"

    return "?"


def stepper(q0: Q) -> Iterator[tuple[Q, O]]:
    states = scan(q0, δ, CharReader())
    outputs = map(λ, states, CharReader())
    return zip(states, outputs)


def main():
    with open("docs.md", "r") as f:
        diagram = get_diagram_from_markdown(f.read())
        fsm = FSM.from_marmaid(diagram)

    print(fsm)

    for qᵢ, oᵢ in stepper(Q.E):
        print(qᵢ, oᵢ)


if __name__ == "__main__":
    main()
