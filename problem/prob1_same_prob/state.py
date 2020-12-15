import collections
from dataclasses import dataclass
from fractions import Fraction
from numbers import Number
from typing import List

NumberType = (
    float,
    Fraction,
    Number
)


class State:
    pass


@dataclass
class Transition:
    next_state: State
    probability: NumberType
    cost: NumberType


@dataclass(unsafe_hash=True)
class P1State(State):
    have: int


class Row:
    def __init__(self, num_type):
        self.body = collections.defaultdict(num_type)
        self.num_type = num_type

    def __getitem__(self, item):
        if item in self.body:
            return self.body[item]
        else:
            return self.num_type()

    def __setitem__(self, key, value):
        self.body[key] = value

    def divide(self, value):
        for k, v in self.body.items():
            self.body[k] = v / value

    def add(self, row, value):
        for k, v in row.body.items():
            self.body[k] += v * value


class Matrix:
    def __init__(self, row_set, col_set, num_type):
        self.row_set = set(row_set)
        self.col_set = set(col_set)
        self.num_type = num_type
        self.body = {
            row: Row(num_type)
            for row in self.row_set
        }

    def _check_item(self, item):
        row, col = item
        if row not in self.row_set:
            raise ValueError(f"{row} is not invalid row value")
        if col not in self.col_set:
            raise ValueError(f"{col} is not invalid col value")
        return row, col

    def __setitem__(self, key, value):
        row, col = self._check_item(key)
        self.body[row][col] = value

    def __getitem__(self, item):
        row, col = self._check_item(item)
        return self.body[row][col]

    def __mul__(self, other: 'Matrix'):
        if self.col_set != other.row_set:
            raise ValueError("Row is unmatched.")

        first, second, third = self.row_set, self.col_set, other.col_set
        result = Matrix(first, third, self.num_type)
        for x in first:
            for z in third:
                result[x, z] = sum(self[x, y]*other[y, z] for y in second)
        return result

    def _divide_row(self, row, value):
        self.body[row].divide(value)

    def _add_row(self, source, target, value):
        self.body[target].add(self.body[source], value)

    @classmethod
    def identity(cls, row_set, num_type):
        matrix = cls(row_set, row_set, num_type)
        for row in row_set:
            matrix[row, row] = num_type(1)
        return matrix

    def copy(self):
        matrix = Matrix(self.row_set, self.col_set, self.num_type)
        for row in self.row_set:
            matrix.body[row].add(self.body[row], self.num_type(1))
        return matrix

    def _max_col(self, col):
        def get_index(row):
            return self[row, col]
        return max(self.row_set, key=get_index)

    def _swap(self, row1, row2):
        self.body[row1], self.body[row2] = self.body[row2], self.body[row1]

    def inverse(self):
        if self.row_set != self.col_set:
            raise ValueError("This is not a square matrix")

        reference: Matrix = self.copy()
        result = Matrix.identity(self.row_set, self.num_type)

        for i in self.row_set:
            if reference[i, i] == 0:
                n = reference._max_col(i)
                reference._swap(i, n)
                result._swap(i, n)

            v = reference[i, i]
            if v == 0:
                raise ValueError("This matrix is not invertible")

            result._divide_row(i, v)
            reference._divide_row(i, v)

            for j in self.row_set:
                if i == j:
                    continue
                result._add_row(i, j, -reference[j, i])
                reference._add_row(i, j, -reference[j, i])

        return result

    def show(self):
        for row in self.row_set:
            print(row, self.body[row].body)


class Problem:
    def __init__(self, number, many: int):
        self.number = number
        self.zero: NumberType = number(0)
        self.one: NumberType = number(1)
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
                Transition(state, self.one*state.have/self.many, self.one),
                Transition(
                    P1State(state.have+1),
                    self.one * (self.many - state.have) / self.many,
                    self.one
                )
            ]

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
        for state in states:
            print(state, solution[state, 0])
