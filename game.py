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
        self.winner = None

    def run(self):
        self.generate_cards()
        self.init_players()
        while len(self.players) > 1:
            self.round = self.players.index(self.winner) if self.winner is not None else 0
            self.winner = None
            shuffle(self.cards)
            self.deal_cards()
            self.played.append(self.deck.pop())
            while sum(player.has_cards() for player in self.players) > 1:
                self.turn()
            loser = list(filter(lambda player: player.has_cards(), self.players))[0]
            loser.loses += 1
            print(f"{loser.name} lost this round! Better luck next time!\n")
            if loser.loses >= 5:
                print(f"{loser.name} lost completely! You fool!")
                self.players.remove(loser)
        print(f"And the winner is... {self.players[0].name}! Congrats!")

    def turn(self):
        player = self.players[self.round]
        if not player.has_cards():
            self.increase_round()
            return
        print(f"It's {player.name}'s turn! The last played card is {self.played[-1]}.")
        print(player.name + "'s cards:")
        player.print_cards()
        print(f"{len(player.cards)} - Draw a card")
        self.choose_and_play(player)
        if not player.has_cards():
            print(f"{player.name} won this round! Congratulations!")
            if self.winner is None:
                self.winner = player
        self.increase_round()
        print()

    def choose_and_play(self, player: Player):
        card_index = int(input("Which card would you like to play? "))
        while card_index not in range(len(player.cards) + 1):
            card_index = int(input(f"Invalid option! Please choose option in range<0, {len(player.cards)}> "))
        if card_index == len(player.cards):
            player.draw_card(self.deck.pop())
        else:
            self.played.append(player.play_card(card_index))

    def increase_round(self):
        self.round += 1
        if self.round >= len(self.players):
            self.round = 0

    def generate_cards(self):
        self.cards = []
        for mark in Mark:
            for value in Value:
                self.cards.append(Card(mark, value))

    def init_players(self):
        num_players = int(input("Number of players (2-5): "))
        for i in range(num_players):
            name = input("Player " + str(i + 1) + " name: ")
            self.players.append(Player(name))
        print()

    def deal_cards(self):
        dealt = 0
        for player in self.players:
            to_deal = 5 - player.loses
            player.cards = self.cards[dealt : dealt + to_deal]
            player.sort_cards()
            dealt += to_deal
        self.deck = self.cards[dealt:]
