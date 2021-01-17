from functools import total_ordering

from mark import Mark
from value import Value


@total_ordering
class Card:
    def __init__(self, mark: Mark, value: Value):
        self.mark = mark
        self.value = value

    def __str__(self):
        return self.value.name + " of " + self.mark.name

    def __eq__(self, other):
        return self.mark == other.mark and self.value == other.value

    def __gt__(self, other):
        return self.value > other.value or (self.value == other.value and self.mark > other.mark)
