#!/usr/bin/python3

import sys

class Card:
    def __init__(self, name) -> None:
        self.suit = name[0]
        self.value = name[1]
        match self.value:
            case "5":
                self.points = 5
            case "T" | "A":
                self.points = 10
            case _:
                self.points = 0

    def stringify(self):
        return f"{self.suit}{self.value}"
    
    def equals(self, card):
        return card == self.stringify()
    
    def compare(self, card):
        order = "56789TJQKA"
        self_rank = order.index(self.value)
        card_rank = order.index(card.value)
        print(f"self {self.value} {self_rank} card {card.value} {card_rank}", file=sys.stderr)
        return self_rank > card_rank


class Hand:
    def __init__(self, cards) -> None:
        self.cards = cards

    def stringify(self):
        string = ""
        for card in self.cards:
            string += f"{card.stringify()} "
        return string

    def remove(self, played):
        for card in self.cards:
            if card.equals(played):
                self.cards.remove(card)
                return
    
    def playable(self, trump, trick):
        playable = []
        for card in self.cards:
            if card.suit == trick.required or card.suit == trump:
                playable.append(card)
        if not playable:
            playable = [card for card in self.cards]
        return playable
    
class Trick:
    def __init__(self) -> None:
        self.played = {}
        self.required = None

    def stringify(self):
        string = ""
        for player in self.played:
            string += f"{self.played[player].stringify()} "
        return string
    
    def getCards(self):
        return [self.played[player] for player in self.played]

    def add(self, player, card):
        if not self.played:
            self.required = card.suit
        self.played[player] = card

    def empty(self):
        self.played.clear()
        self.required = None
               
    def score(self):
        sum = 0
        for player in self.played:
            sum += self.played[player].points
        return sum

    def winner(self, trump):
        players = list(self.played)
        print(trump, file=sys.stderr)
        print(self.played, file=sys.stderr)
        print(players, file=sys.stderr)
        id = players[0]
        top = self.played[id]
        for player in players[1:]:
            card = self.played[player]
            if card.suit == trump:
                if top.suit == trump:
                    if not top.compare(card):
                        top = card
                        id = player
                else:
                    top = card
                    id = player
            elif card.suit == self.required:
                if not top.compare(card):
                    top = card
                    id = player
        return id
        
        

hand = None
turn = 0
player = ""
teammate = 0
team = 0
trick = Trick()
played = []
bids = [0, 0, 0, 0]
bidWinner = 0
trump = None
new_game = False
game_points = [0, 0]
points = [0, 0]

while (line := input().split())[0] != "end":
    # print(line, file=sys.stderr)

    match line[0]:
        case "player":
            player = line[1]
            teammate = int(player) + 2 % 4
            print(f"player number {player}, teammate {teammate}\n", file=sys.stderr)

        case "hand":
            new_game = True
            hand = Hand([Card(card) for card in line[1:]])
            print(f"hand: {hand.stringify()}\n", file=sys.stderr)

        case "bid":
            if line[1] == "?":
                print(0)
            else:
                bid = int(line[2])
                bids[int(line[1])] = bid
                if bid:
                    bidWinner = line[1]

        case "card":
            if line[1] == "?":
                playable = hand.playable(trump, trick)
                # print(f"{playable[0].stringify()}", file=sys.stderr)
                playable_hand = Hand(playable)
                # print(f"{playable_hand.cards[0].stringify()}")
                print(f"playable: {playable_hand.stringify()}", file=sys.stderr)
                print(0)
            else:
                turn = (turn + 1) % 4
                card = line[2]
                trick.add(int(line[1]), Card(card))
                print(f"trick: {trick.stringify()} winner: {trick.winner(trump)}\n", file=sys.stderr)
                if new_game:
                    trump = line[2][0]
                    new_game = False
                if not turn: #turn == 0
                    game_points[trick.winner(trump)%2] += trick.score()
                    print(f"Trick score: {trick.score()} Trick winner: {trick.winner(trump)} Winning team: {trick.winner(trump)%2} Game score: {game_points}", file=sys.stderr)
                    played.extend(trick.getCards())
                    trick.empty()
                if line[1] == player:
                    hand.remove(card)
                    print(f"hand: {hand.stringify()}\n", file=sys.stderr)
    
