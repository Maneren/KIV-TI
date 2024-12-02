from itertools import tee
from typing import Iterator
from FSM import FSM, UnexpectedSymbol, Q

from utils import (
    CharReader,
    O,
    scan,
    get_diagram_from_markdown,
)


def stepper(A: FSM, q0: Q) -> Iterator[tuple[Q, O]]:
    states = scan(q0, A.δ, CharReader())
    [states, λ_states] = tee(states, 2)
    outputs = map(A.λ, λ_states, CharReader())
    yield from zip(states, outputs)


def main():
    with open("docs.md", mode="r", encoding="utf-8") as f:
        diagram = get_diagram_from_markdown(f.read())
        fsm = FSM.from_marmaid(diagram)

    for id, q in fsm.states.items():
        print(id, ":", q.name)

    print(f" {fsm.initial.name}: ", end="", flush=True)

    reader = CharReader()

    try:
        for qᵢ, oᵢ in stepper(fsm, fsm.initial):
            print(f"\r{oᵢ}: {''.join(reader.buffer)}", end="", flush=True)
    except UnexpectedSymbol:
        print("Unexpected symbol encountered")


if __name__ == "__main__":
    main()
