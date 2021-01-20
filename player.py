from card import Card


class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards = []
        self.loses = 0

    def __str__(self):
        text = "Player " + self.name + ":\n"
        for card in self.cards:
            text += str(card) + "\n"
        return text

    def print_playable_cards(self, last_played: Card):
        playable = self.get_playable_cards(last_played)
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

    def get_playable_cards(self, last_played: Card):
        return list(filter(last_played.can_be_played, self.cards))
