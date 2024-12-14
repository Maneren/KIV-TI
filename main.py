from itertools import takewhile, tee
from typing import Iterator
from FSM import FSM, UnexpectedSymbol, Q

from utils import (
    CharReader,
    O,
    scan,
    get_diagram_from_markdown,
)


def stepper(A: FSM, q0: Q) -> Iterator[tuple[Q, O]]:
    states = scan(q0, A.δ, takewhile(lambda ch: ch != " ", CharReader()))
    [states, λ_states] = tee(states, 2)
    outputs = map(A.λ, λ_states, CharReader())
    return zip(states, outputs)


def main():
    with open("docs.md", mode="r", encoding="utf-8") as f:
        diagram = get_diagram_from_markdown(f.read())
        fsm = FSM.from_marmaid(diagram)

    if fsm.initial is None:
        print("FSM has no initial state")
        exit(1)

    print(fsm.terminals)

    for id, q in fsm.states.items():
        print(id, ":", q.name)

    print(f" {fsm.initial.name}: ", end="", flush=True)

    reader = CharReader()

    qᵢ = fsm.initial
    oᵢ = fsm.initial.name
    try:
        for qᵢ, oᵢ in stepper(fsm, fsm.initial):
            print(f"\r{oᵢ}: {''.join(reader.buffer)}", end="", flush=True)

        if qᵢ.name not in fsm.terminals:
            print(f"\nHaven't reached a terminal state, instead reached: {qᵢ.name}")
            exit(128)
    except UnexpectedSymbol as e:
        print(f"\r{oᵢ}: {''.join(reader.buffer)}", flush=True)

        if e.char in fsm.alphabet:
            print(f"\nReached a non-terminal absorbing state")
        else:       
            print(f"\nUnexpected symbol encountered: '{e.char}' ({ord(e.char):x})")


if __name__ == "__main__":
    main()
