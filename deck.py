import random


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return str(self.rank) + self.suit

    def is_three_of_clubs(self):
        return self.rank == 3 and self.suit == '♣'

    # Does not take three of clubs into account
    def is_higher_or_equal_rank(self, rank):
        ranks = [3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A', 2]
        this_rank = ranks.index(self.rank)
        that_rank = ranks.index(rank)
        return this_rank >= that_rank


class Deck:

    def __init__(self):
        suits = ['♣', '♦', '♥', '♠']
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)

    def give(self, number):
        popped = []
        for _ in range(number):
            popped.append(self.cards.pop(0))
        return popped
