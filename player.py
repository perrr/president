class Player:

    def __init__(self, cards, is_player_one):
        self.cards = cards
        self.is_player_one = is_player_one

    def play(self, cards):
        for card in cards:
            self.cards.pop(self.cards.index(card))
