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

    def can_be_played(self, last_played) -> bool:
        leaves_unter = Card(Mark.LEAVES, Value.UNTER)
        if last_played == leaves_unter or self == leaves_unter:
            return True
        if last_played.mark == self.mark or last_played.value == self.value:
            return True
        return False
