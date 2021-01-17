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
