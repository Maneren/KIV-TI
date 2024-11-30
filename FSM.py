from __future__ import annotations
from typing import Self, cast
import re


class UnexpectedSymbol(Exception):
    pass


class InvalidMermaid(Exception):
    pass


marmaid_line_regex = re.compile(
    r"(?P<start>[^\s]+) --> (?P<end>[^\s]+) (?:: (?P<char>[^\s]+)|% (?P<name>[^\s]+))"
)


class FSM:
    """
    Class for representing finite-state machines
    """

    # Dictionary where ids are keys and values are state objects
    states: dict[str, State]

    # Set of characters that represents alphabet of the finite-state machine
    alphabet: set[str]

    # Ids of initial state
    initial: str

    # Ids of terminal states
    terminals: set[str]

    # Index used for generating unique state names
    name_index: int

    def __init__(self, alphabet: set[str]):
        self.states = {}
        self.alphabet = alphabet
        self.initial = ""
        self.terminals = set()
        self.name_index = 0

    def generate_state_name(self) -> str:
        index: int = self.name_index

        prefix_val, suffix_val = divmod(index, 26)
        # Generating prefix
        prefix = chr(ord("A") + prefix_val - 1) if prefix_val >= 1 else ""
        # Generating suffix
        suffix: str = chr(ord("A") + suffix_val)

        # Incrementing name_index for next use
        self.name_index += 1

        return prefix + suffix

    def add_state(self, id: str, name: str | None = None) -> None:
        if name is None:
            name = self.generate_state_name()

        new_state = State(name)
        self.states[id] = new_state

    def add_transition(
        self,
        start_id: str,
        end_id: str,
        characters: list[str],
    ) -> None:
        if any(character not in self.alphabet for character in characters):
            raise UnexpectedSymbol

        if start_id not in self.states:
            self.add_state(start_id)

        if end_id not in self.states:
            self.add_state(end_id)

        start_state = self.states[start_id]
        end_state = self.states[end_id]

        for character in characters:
            start_state.add_transition(end_state, character)

    def set_initial(self, initial_id: str, initial_name: str | None = None) -> None:
        if initial_id not in self.states:
            self.add_state(initial_id, initial_name)

        self.initial = initial_id

    def add_terminal(self, terminal_id: str, terminal_name: str | None = None) -> None:
        if terminal_id not in self.states:
            self.add_state(terminal_id, terminal_name)

        self.terminals.add(terminal_id)

    @staticmethod
    def from_marmaid(mermaid_diagram: str) -> Self:
        lines = list(map(str.strip, mermaid_diagram.split("\n")))
        assert lines[0] == "stateDiagram-v2"

        comments = [line for line in lines if line.startswith("%%")]
        edges = [line for line in lines if line.find("-->") != -1]

        Σ = cast(
            set[str] | None,
            next(
                (
                    set(comment[5:].split(","))
                    for comment in comments
                    if comment.startswith("%% Σ ")
                ),
                None,
            ),
        )

        if Σ is None:
            raise InvalidMermaid

        graph = FSM(Σ)

        for edge in edges:
            match = marmaid_line_regex.match(edge)

            start = match.group("start")
            end = match.group("end")
            chars = match.group("char")
            name = match.group("name")

            if start == "[*]":
                graph.set_initial(end, name)
                continue
            elif end == "[*]":
                graph.add_terminal(start, name)
                continue

            chars = list(chars.split(","))

            assert all(c in Σ for c in chars)

            graph.add_transition(start, end, chars)

        return graph

    def δ(self, Q: State, character: str) -> State:
        return Q.get_next_one(character)
    
    def λ(self, Q: State, character: str) -> str:
        return f"{Q.name}"


class State:
    """
    Class for representing a state in finite-state machine
    """

    # Name of the state
    name: str

    # Dictionary where key is the character of the transition and value is the next state for given transition
    nbs: dict[str, State] = {}

    def __init__(self, name: str, id: str):
        self.name = name
        self.name = id

    def add_transition(self, nb: State, character: str) -> None:
        self.nbs[character] = nb

    def get_next_one(self, character: str) -> State:
        return self.nbs[character]
