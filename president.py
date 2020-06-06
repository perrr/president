from deck import *
from player import *
import random


def trumps_on_hand(cards):
    trumps = []
    sixes = []
    for card in cards:
        if card.rank == 6 and len(sixes) < 3:
            sixes.append(card)
        elif card.is_three_of_clubs():
            trumps.append([card])
    if len(sixes) == 3:
        trumps.append(sixes)
    return trumps


def get_legal_combinations(cards, number_of_cards_on_table, rank_on_table):
    combinations_on_hand = {}
    for card in cards:
        if not card.is_three_of_clubs():
            if card.rank not in combinations_on_hand:
                combinations_on_hand[card.rank] = [card]
            elif len(combinations_on_hand[card.rank]) < number_of_cards_on_table:
                combinations_on_hand[card.rank].append(card)
    legal_combinations = []
    for rank in combinations_on_hand:
        if combinations_on_hand[rank][0].is_higher_or_equal_rank(rank_on_table) \
                and len(combinations_on_hand[rank]) == number_of_cards_on_table \
                and not (rank == 6 and len(combinations_on_hand[rank]) >= 3):
            legal_combinations.append(combinations_on_hand[rank])
    return legal_combinations


def print_hand(cards):
    for i in range(len(cards)):
        print(str(i) + ': ' + str(cards[i]))


def is_trump(hand):
    return (len(hand) == 1 and hand[0].is_three_of_clubs()) \
           or (len(hand) == 3 and hand[0].rank == 6 and hand[1].rank == 6 and hand[2].rank == 6)


def is_legal_hand(hand, hand_on_table):
    if not hand_on_table:
        return True
    if is_trump(hand):
        return True
    return len(hand) == len(hand_on_table) and hand[0].is_higher_or_equal_rank(hand_on_table[0].rank)


def sort_cards(cards):
    sorted_cards = []
    for rank in [3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A', 2]:
        pop_cards = []
        for card in cards:
            if card.rank == rank and not card.is_three_of_clubs():
                sorted_cards.append(card)
                pop_cards.append(card)
        for pop_card in pop_cards:
            cards.pop(cards.index(pop_card))
    if len(cards) == 1:  # Three of clubs left
        sorted_cards.append(cards[0])
    return sorted_cards


def get_legal_hands(cards, hand_on_table):
    legal_hands = trumps_on_hand(cards)
    if not hand_on_table:  # First hand
        for i in range(1, 5):
            legal_hands.extend(get_legal_combinations(cards, i, 3))
        return legal_hands
    number_of_cards_on_table = len(hand_on_table)
    rank_on_table = hand_on_table[0].rank
    legal_hands.extend(get_legal_combinations(cards, number_of_cards_on_table, rank_on_table))
    return legal_hands


def play_computer_hand(player, hand_on_table):
    legal_hands = get_legal_hands(player.cards, hand_on_table)
    if len(legal_hands) == 0:
        return None
    return random.choice(legal_hands)


class Round:

    def __init__(self):
        self.number_of_players = 4
        self.deck = Deck()
        self.players = []
        self.finished_players = []
        player_one = random.randint(0, 3)
        for n in range(self.number_of_players):
            cards = self.deck.give(13)
            self.players.append(Player(cards, n == player_one))
        giver = 0
        while True:
            last_giver = self.play_round(giver)
            print('Player ' + str(last_giver) + ' wins round')
            if len(self.finished_players) == self.number_of_players:  # Game finished
                print('Game over')
                break
            giver = last_giver

    def play_round(self, first_giver):
        player_number = first_giver
        last_player = None
        passes = []
        hand_on_table = None
        while True:
            if player_number == last_player:
                return player_number
            if len(passes) + len(self.finished_players) == self.number_of_players:
                return last_player
            if player_number in passes or player_number in self.finished_players:
                player_number = (player_number + 1) % self.number_of_players
                continue
            hand = self.play_hand(self.players[player_number], hand_on_table)
            if not hand:
                print('Player ' + str(player_number) + ' passes')
                passes.append(player_number)
                player_number = (player_number + 1) % self.number_of_players
                continue
            last_player = player_number
            self.print_hand_on_table(player_number, hand)
            self.players[player_number].play(hand)
            if is_trump(hand):
                return last_player
            hand_on_table = hand
            if len(self.players[player_number].cards) == 0:
                self.finished_players.append(player_number)
                self.print_player_finished(player_number)
            player_number = (player_number + 1) % self.number_of_players

    def play_hand(self, player, hand_on_table):
        if player.is_player_one:
            return self.play_input_hand(player, hand_on_table)
        return play_computer_hand(player, hand_on_table)

    def play_input_hand(self, player, hand_on_table):
        player.cards = sort_cards(player.cards)
        print_hand(player.cards)
        play_command = input('Play cards (p for pass): ')
        play_cards = play_command.split(' ')
        hand = []
        for play_card in play_cards:
            if play_card == 'p':
                return None
            try:
                if int(play_card) > len(player.cards) - 1 or int(play_card) < 0:
                    print('Invalid play')
                    return self.play_input_hand(player, hand_on_table)
                hand.append(player.cards[int(play_card)])
            except ValueError:
                print('Invalid play')
                return self.play_input_hand(player, hand_on_table)
        if not is_legal_hand(hand, hand_on_table):
            print('Invalid play')
            return self.play_input_hand(player, hand_on_table)
        return hand

    def print_hand_on_table(self, player_number, cards):
        s = 'Player ' + str(player_number) + ' plays '
        s += ', '.join(str(card) for card in cards)
        s += ' (' + str(len(self.players[player_number].cards) - len(cards)) + ' cards left)'
        print(s)

    def print_player_finished(self, player_number):
        finishes = ['president', 'vice president', 'vice bum', 'bum']
        print('Player ' + str(player_number) + ' finishes as ' + finishes[len(self.finished_players) - 1])


if __name__ == '__main__':
    Round()
