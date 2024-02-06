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
    
    def compare(self, card):
        return card == self.stringify()

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
            if card.compare(played):
                self.cards.remove(card)
                return
    
    def playable(self, trump, trick):
        playable = []
        required_suit = trick[0].suit if trick else None
        for card in self.cards:
            if card.suit == required_suit or card.suit == trump:
                playable.append(card)
        if not playable:
            playable = [card for card in self.cards]
        return playable
    
class Trick:
    def __init__(self) -> None:
        self.played = []

    def stringify(self):
        string = ""
        for card in self.played:
            string += f"{card.stringify()} "
        return string
    
    def getCards(self):
        return self.played

    def add(self, card):
        self.played.append(card)

    def empty(self):
        self.played = []
               
    def score(self):
        sum = 0
        for card in self.played:
            sum += card.points
        return sum



hand = None
turn = 0
player = ""
teammate = 0
trick = Trick()
played = []
bids = [0, 0, 0, 0]
bidWinner = 0
trump = None
new_game = False

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
                playable = hand.playable(trump, trick.getCards())
                # print(f"{playable[0].stringify()}", file=sys.stderr)
                playable_hand = Hand(playable)
                # print(f"{playable_hand.cards[0].stringify()}")
                print(f"playable: {playable_hand.stringify()}", file=sys.stderr)
                print(0)
            else:
                turn = (turn + 1) % 4
                card = line[2]
                trick.add(Card(card))
                print(f"trick: {trick.stringify()}\n", file=sys.stderr)
                if new_game:
                    trump = line[2][0]
                if not turn: #turn == 0
                    print(f"Trick score: {trick.score()}", file=sys.stderr)
                    played.extend(trick.getCards())
                    trick.empty()
                if line[1] == player:
                    hand.remove(card)
                    print(f"hand: {hand.stringify()}\n", file=sys.stderr)
    
