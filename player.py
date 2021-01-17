from card import Card


class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def __str__(self):
        text = "Player " + self.name + ":\n"
        for card in self.cards:
            text += str(card) + "\n"
        return text

    def print_cards(self):
        for i, card in enumerate(self.cards):
            print(i, "-", card)

    def sort_cards(self):
        self.cards.sort()

    def play_card(self, index: int) -> Card:
        return self.cards.pop(index)

    def draw_card(self, card: Card):
        self.cards.append(card)
        self.sort_cards()
