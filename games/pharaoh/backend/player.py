from card import Card
from mark import Mark
from value import Value


class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards = []
        self.loses = 0
        self.won_last_round = False

    def __str__(self):
        text = "Player " + self.name + ":\n"
        for card in self.cards:
            text += str(card) + "\n"
        return text

    def print_playable_cards(self, last_played: Card, someone_won: bool, ace: bool, seven: bool, last: bool):
        playable = self.get_playable_cards(last_played, someone_won, ace, seven, last)
        for i, card in enumerate(self.cards):
            print(i, "-", card, end=" *\n" if card in playable else "\n")

    def sort_cards(self):
        self.cards.sort()

    def play_card(self, index: int) -> Card:
        return self.cards.pop(index)

    def draw_card(self, card: Card):
        self.cards.append(card)
        self.sort_cards()

    def has_cards(self) -> bool:
        return bool(len(self.cards))

    def get_playable_cards(self, played: Card, someone_won: bool, ace: bool, seven: bool, last: bool) -> list[Card]:
        if last:
            playable = list(filter(lambda card: card == Card(Mark.HEARTS, Value.SEVEN), self.cards))
        elif ace:
            playable = list(filter(lambda card: card.value == Value.ACE, self.cards))
        elif seven:
            playable = list(filter(lambda card: card.value == Value.SEVEN, self.cards))
            if Card(Mark.LEAVES, Value.UNTER) in self.cards:
                playable.append(Card(Mark.LEAVES, Value.UNTER))
        else:
            playable = list(filter(played.can_be_played, self.cards))
            if someone_won and Card(Mark.HEARTS, Value.SEVEN) in self.cards:
                playable.append(Card(Mark.HEARTS, Value.SEVEN))
        return playable

    def has_seven_of_hearts(self) -> bool:
        return Card(Mark.HEARTS, Value.SEVEN) in self.cards
