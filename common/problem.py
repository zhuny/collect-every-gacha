from typing import List

from common.matrix import Matrix
from common.state import NumberType, State, Transition


class BaseProblem:
    def __init__(self, number):
        self.number = number
        self.zero: NumberType = number(0)
        self.one: NumberType = number(1)

    def list_of_state(self) -> List[State]:
        raise NotImplementedError()

    def transition(self, state: State) -> List[Transition]:
        raise NotImplementedError()

    def solve(self):
        states = self.list_of_state()
        trans_matrix = Matrix(states, states, self.number)
        cost_row = Matrix(states, [0], self.number)
        for state in states:
            trans_matrix[state, state] = self.one
            for transition in self.transition(state):
                trans_matrix[state,
                             transition.next_state] -= transition.probability
                cost_row[state, 0] += transition.probability*transition.cost

        solution = trans_matrix.inverse() * cost_row

        # show result
        for state in sorted(states):
            print(state, solution[state, 0])
