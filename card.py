from mark import Mark
from value import Value


class Card:
    def __init__(self, mark: Mark, value: Value):
        self.mark = mark
        self.value = value

    def __str__(self):
        return self.value.name + " of " + self.mark.name

    def __eq__(self, other):
        return self.mark == other.mark and self.value == other.value
