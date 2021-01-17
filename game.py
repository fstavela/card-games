from random import shuffle

from card import Card
from mark import Mark
from player import Player
from value import Value


class Game:
    def __init__(self):
        self.players = []
        self.cards = []
        self.deck = []
        self.played = []
        self.round = 0

    def run(self):
        self.generate_cards()
        self.init_players()
        self.deal_cards()
        self.played.append(self.deck.pop())
        while True:
            self.turn()

    def turn(self):
        player = self.players[self.round]
        print(f"It's {player.name}'s turn! The last played card is {self.played[-1]}.")
        print(player.name + "'s cards:")
        player.print_cards()
        print(f"{len(player.cards)} - Draw a card")
        card = int(input("Which card would you like to play? "))
        while card not in range(len(player.cards) + 1):
            card = int(input(f"Invalid option! Please choose a card in range<0, {len(player.cards)}> or draw a card"))
        if card == len(player.cards):
            player.cards.append(self.deck.pop())
        else:
            self.played.append(player.cards.pop(card))
        self.increase_round()
        print()

    def increase_round(self):
        self.round += 1
        if self.round >= len(self.players):
            self.round = 0

    def generate_cards(self):
        cards = []
        for mark in Mark:
            for value in Value:
                cards.append(Card(mark, value))
        self.cards = cards
        shuffle(self.cards)

    def init_players(self):
        num_players = int(input("Number of players (2-5): "))
        for i in range(num_players):
            name = input("Player " + str(i + 1) + " name: ")
            self.players.append(Player(name))

    def deal_cards(self):
        for i, player in enumerate(self.players):
            player.cards = self.cards[(i * 5):(i * 5 + 5)]
        self.deck = self.cards[len(self.players) * 5:]
