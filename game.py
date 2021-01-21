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
        self.aces = 0
        self.sevens = 0

    def run(self):
        self.generate_cards()
        self.init_players()
        while len(self.players) > 1:
            self.round = self.players.index(self.winner) if self.winner is not None else 0
            self.winner = None
            shuffle(self.cards)
            self.deal_cards()
            self.played.append(self.deck.pop())
            while not self.game_ended():
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
        player.won_last_round = False
        if not player.has_cards():
            self.increase_round()
            return
        self.print_options(player)
        self.choose_and_play(player)
        if not player.has_cards():
            player.won_last_round = True
            print(f"{player.name} won this round! Congratulations!")
            if self.winner is None:
                self.winner = player
        self.increase_round()
        print()

    def print_options(self, player: Player):
        print(f"It's {player.name}'s turn! The last played card is {self.played[-1]}.")
        print(player.name + "'s cards:")
        someone_won = any(p.won_last_round for p in self.players)
        last_player = sum(p.has_cards() for p in self.players) == 1
        player.print_playable_cards(self.played[-1], someone_won, bool(self.aces), bool(self.sevens), last_player)
        if self.aces:
            print(f"{len(player.cards)} - Skip this round")
        elif self.sevens:
            print(f"{len(player.cards)} - Draw {3 * self.sevens} cards")
        else:
            print(f"{len(player.cards)} - Draw a card")

    def choose_and_play(self, player: Player):
        someone_won = any(p.won_last_round for p in self.players)
        last = sum(p.has_cards() for p in self.players) == 1
        playable = player.get_playable_cards(self.played[-1], someone_won, bool(self.aces), bool(self.sevens), last)
        card_index = int(input("Which card would you like to play? "))
        while (
            card_index not in range(len(player.cards)) or player.cards[card_index] not in playable
        ) and card_index != len(player.cards):
            card_index = int(input("You can't play this card! Please choose one of the '*' marked cards or draw. "))
        if card_index == len(player.cards):
            self.special_effect(player)
        else:
            card = player.play_card(card_index)
            self.play_card(card)

    def play_card(self, card: Card):
        if self.aces:
            self.aces -= 1
        if card.value == Value.ACE:
            self.aces += 1
        if card == Card(Mark.LEAVES, Value.UNTER):
            self.sevens = 0
        if card.value == Value.SEVEN:
            if card.mark == Mark.HEARTS and any(p.won_last_round for p in self.players) and not self.sevens:
                print("What would you like to do?")
                print("0 - Use this card as a regular seven")
                print("1 - Return someone to game")
                opt = int(input())
                if opt:
                    self.play_seven_of_hearts()
                else:
                    self.sevens += 1
            else:
                self.sevens += 1
        self.played.append(card)

    def game_ended(self) -> bool:
        return sum(player.has_cards() for player in self.players) <= 1 and (
            all(not player.has_seven_of_hearts() for player in self.players)
            or all(not player.won_last_round for player in self.players)
            or self.aces
        )

    def special_effect(self, player: Player):
        if self.aces:
            self.aces -= 1
        elif self.sevens:
            for i in range(3 * self.sevens):
                self.draw_card(player)
            self.sevens = 0
        else:
            self.draw_card(player)

    def play_seven_of_hearts(self):
        print("Whom would you like to return to game?")
        winners = list(filter(lambda p: p.won_last_round, self.players))
        for i, p in enumerate(winners):
            print(f"{i} - {p.name}")
        index = int(input())
        for i in range(3):
            self.draw_card(winners[index])

    def draw_card(self, player: Player):
        player.draw_card(self.deck.pop())
        if len(self.deck) == 0:
            print("The deck is empty! Adding already played cards back to the deck.")
            self.deck.extend(self.played[len(self.played) - 2 :: -1])
            self.played = [self.played[-1]]

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
