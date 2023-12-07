from aocd import get_data
from collections import Counter
import re

data = get_data(day=7,year=2023)
example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

def score_hand(hand):
    hv = hand.values()
    if max(hv) == 5:
        #Five of a kind
        rank = 7
    elif max(hv) == 4:
        #Four of a kind
        rank = 6
    elif sorted(hv,reverse=True) == [3,2]:
        #Full house
        rank = 5
    elif max(hv) == 3:
        #Three of a kind
        rank = 4
    elif sorted(hv,reverse=True) == [2,2,1]:
        #Two pair
        rank = 3
    elif max(hand.values()) == 2:
        #Pair
        rank = 2
    else:
        rank = 1
    return rank

class Hand:
    def __init__(self, hand, score):
        self.text_hand = [c for c in hand]
        self.hc = Counter([c for c in hand])
        self.rank = score_hand(self.hc)
        self.bid = int(score)

    def __repr__(self):
        return ''.join(self.text_hand)

    def __lt__(self, other):
        rank_one = self.rank
        rank_two = other.rank
        if rank_one > rank_two:
            return False
        elif rank_one < rank_two:
            return True
        else:
            card_orders = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
            card_orders = list(reversed(card_orders))
            for i in range(len(self.text_hand)):
                idx_one = card_orders.index(self.text_hand[i])
                idx_two = card_orders.index(other.text_hand[i])
                if idx_one > idx_two:
                    return False
                elif idx_one < idx_two:
                    return True


def score_hand_part_two(hand):
    hv = hand.values()
    if max(hv) == 5:
        #Five of a kind
        rank = 7
    elif max(hv) == 4:
        #Four of a kind
        rank = 6
    elif sorted(hv,reverse=True) == [3,2]:
        #Full house
        rank = 5
    elif max(hv) == 3:
        #Three of a kind
        rank = 4
    elif sorted(hv,reverse=True) == [2,2,1]:
        #Two pair
        rank = 3
    elif max(hand.values()) == 2:
        #Pair
        rank = 2
    else:
        rank = 1
    return rank

class HandPartTwo:
    def __init__(self, hand, score):
        self.card_orders = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
        self.text_hand = [c for c in hand]
        max_rank = 0
        for co in self.card_orders[:-1]:
            h = hand.replace('J', co)
            hc = Counter([c for c in h])
            rank = score_hand(hc)
            if rank > max_rank:
                max_rank = rank
                max_rank_hand = h
        self.rank = max_rank
        self.bid = int(score)

    def __repr__(self):
        return ''.join(self.text_hand)

    def __lt__(self, other):
        rank_one = self.rank
        rank_two = other.rank
        if rank_one > rank_two:
            return False
        elif rank_one < rank_two:
            return True
        else:
            card_orders = list(reversed(self.card_orders))
            for i in range(len(self.text_hand)):
                idx_one = card_orders.index(self.text_hand[i])
                idx_two = card_orders.index(other.text_hand[i])
                if idx_one > idx_two:
                    return False
                elif idx_one < idx_two:
                    return True


def parse_data(data):
    hands = []
    hands_part_two = []
    for row in data.split('\n'):
        hand, score = row.split(' ')
        hands.append(Hand(hand, score))
        hands_part_two.append(HandPartTwo(hand, score))
    return hands, hands_part_two

def part_one(data):
    hands, _ = parse_data(data)
    hands = sorted(hands)
    answer = 0
    for i, h in enumerate(hands):
        answer += h.bid * (i+1)
    return answer

def part_two(data):
    _, hands = parse_data(data)
    hands = sorted(hands)
    answer = 0
    for i, h in enumerate(hands):
        answer += h.bid * (i + 1)
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)