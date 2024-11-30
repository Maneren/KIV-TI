from __future__ import annotations


class UnexpectedSymbol(Exception):
    pass


class FSM:
    """
    Class for representing finite-state machines
    """

    # Dictionary where ids are keys and values are state objects
    states: dict[str, State] = {}

    # Set of characters that represents alphabet of the finite-state machine
    alphabet: set[str]

    # Ids of initial state
    initial: str

    # Ids of terminal states
    terminals: set[str]

    # Index used for generating unique state names
    name_index: int = 0

    def __init__(self, alphabet: set):
        self.alphabet = alphabet

    def generate_state_name(self) -> str:
        index: int = self.name_index

        prefix_val: int = index // 26
        suffix_val: int = index % 26

        prefix: str = chr(ord("A") + prefix_val - 1) if prefix_val >= 1 else ""

        # Generating suffix
        suffix: str = chr(ord("A") + suffix_val)

        # Incrementing name_index for next use
        self.name_index += 1

        return prefix + suffix

    def add_state(self, id: str, name: str = "") -> None:
        if not name:
            name = self.generate_state_name()

        new_state = State(name)
        self.states[id] = new_state

    def add_transition(
        self,
        start_id: str,
        end_id: str,
        character: str,
        start_name: str = "",
        end_name: str = "",
    ) -> None:
        if character not in self.alphabet:
            raise UnexpectedSymbol

        if start_id not in self.states:
            self.add_state(start_id, start_name)

        if end_id not in self.states:
            self.add_state(end_id, end_name)

        self.states[start_id].add_transition(self.states[end_id], character)

    def set_initial(self, initial_id: str, initial_name: str = "") -> None:
        if initial_id not in self.states:
            self.add_state(initial_id, initial_name)

        self.initial = initial_id

    def add_terminal(self, terminal_id: str, terminal_name: str = "") -> None:
        if terminal_id not in self.states:
            self.add_state(terminal_id, terminal_name)

        self.terminals.add(terminal_id)


class State:
    """
    Class for representing a state in finite-state machine
    """

    # Name of the state
    name: str

    # Dictionary where key is the character of the transition and value is the next state for given transition
    nbs: dict[str, State] = {}

    def __init__(self, name: str):
        self.name = name

    def add_transition(self, nb: State, symbol: str) -> None:
        self.nbs[symbol] = nb


if __name__ == "__main__":
    alphabet: set = {"a", "b"}
    fsm: FSM = FSM(alphabet)

    fsm.add_transition("1", "2", "b")
    pass
