from dataclasses import dataclass
from fractions import Fraction
from numbers import Number


class State:
    pass


NumberType = (
    float,
    Fraction,
    Number
)


@dataclass
class Transition:
    next_state: State
    probability: NumberType
    cost: NumberType