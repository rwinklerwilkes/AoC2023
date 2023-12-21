from aocd import get_data
import re

data = get_data(day=4,year=2023)
example = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def parse_input(data):
    cards = {}
    for card in data.split('\n'):
        try:
            card, numbers = card.split(': ')
            card_number = int(re.split(r'\s', card)[-1])
            winning, player = numbers.split(' | ')
            winning = set(int(i) for i in winning.split(' ') if len(i) > 0)
            player = set(int(i) for i in player.split(' ') if len(i) > 0)
            cards[card_number] = (winning, player)
        except Exception as e:
            print(card)
            raise e
    return cards

def score_cards(parsed_data):
    total_score = 0
    for card, (winning, player) in parsed_data.items():
        winning_numbers = winning.intersection(player)
        if winning_numbers:
            score = 2**(len(winning_numbers)-1)
            total_score += score
    return total_score

def process_cards(parsed_data):
    copies = {card:1 for card in parsed_data.keys()}
    max_card = max(copies.keys())
    for card in copies.keys():
        currently_have = copies[card]
        winning, player = parsed_data[card]
        cards_won = len(winning.intersection(player))
        cards_to_add = [card + i + 1 for i in range(cards_won) if card + i + 1 <= max_card]
        for card in cards_to_add:
            copies[card] += currently_have
    total_pile = sum(copies.values())
    return total_pile


def part_one(data):
    parsed_data = parse_input(data)
    total_score = score_cards(parsed_data)
    return total_score

def part_two(data):
    parsed_data = parse_input(data)
    total_pile = process_cards(parsed_data)
    return total_pile

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)