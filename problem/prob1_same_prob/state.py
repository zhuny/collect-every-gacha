from dataclasses import dataclass
from typing import List

from common.problem import BaseProblem
from common.state import State, Transition


@dataclass(unsafe_hash=True)
class P1State(State):
    have: int


class Problem(BaseProblem):
    def __init__(self, number, many: int):
        super().__init__(number)
        self.many = many

    def list_of_state(self) -> List[P1State]:
        return [
            P1State(i)
            for i in range(self.many+1)
        ]

    def transition(self, state: P1State) -> List[Transition]:
        if state.have == self.many:
            return []
        else:
            return [
                Transition(state, self.one * state.have / self.many, self.one),
                Transition(
                    P1State(state.have+1),
                    self.one * (self.many - state.have) / self.many,
                    self.one
                )
            ]
