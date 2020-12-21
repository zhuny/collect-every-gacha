from dataclasses import dataclass
from typing import List

from common.problem import BaseProblem
from common.state import State, Transition


@dataclass(unsafe_hash=True, order=True)
class P2State(State):
    state: tuple


class Problem(BaseProblem):
    def __init__(self, number, many: int, goal: int):
        super().__init__(number)
        self.many = many
        self.goal = goal

    @staticmethod
    def _iter_state(state: P2State, index: int):
        for i, v in enumerate(state.state):
            if i == index:
                yield v-1
            elif i-1 == index:
                yield v+1
            else:
                yield v

    def _move_next(self, state: P2State, index: int):
        return P2State(state=tuple(self._iter_state(state, index)))

    def _adj_state(self, state: P2State):
        for i, v in enumerate(state.state):
            if v > 0:
                yield self._move_next(state, i)

    def _first_state(self):
        state = [0] * self.goal
        state[0] = self.many
        return P2State(state=tuple(state))

    def list_of_state(self) -> List[P2State]:
        state_set = {self._first_state()}
        done = set()
        while state_set:
            state = state_set.pop()
            if state not in done:
                done.add(state)
                state_set.update(self._adj_state(state))
        return list(done)

    def _probability(self, source: P2State, target: P2State):
        for s, t in zip(source.state, target.state):
            if s != t:
                return self.one * s / self.many

    def transition(self, state: P2State) -> List[Transition]:
        total = sum(state.state)
        if 0 < total < self.many:
            yield Transition(
                next_state=state,
                probability=self.one*(self.many-total)/self.many,
                cost=self.one
            )
        for adj in self._adj_state(state):
            yield Transition(
                next_state=adj,
                probability=self._probability(state, adj),
                cost=self.one
            )
