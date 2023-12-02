from collections import defaultdict
from itertools import chain

from aocd import get_data
import re

data = get_data(day=2, year=2023)
example = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

def parse_ball(ball):
    ball_regex = r'([0-9]{1,}) (blue|red|green)'
    mobj = re.match(ball_regex, ball)
    ball, number = mobj.group(2), int(mobj.group(1))
    return ball, number

def score_game(game):
    game, all_balls = game.split(': ')
    game_number = int(game.split(' ')[-1])
    all_picks = all_balls.split('; ')
    all_balls = list(chain.from_iterable(ball.split(', ') for ball in all_picks))
    total_balls_picked = defaultdict(int)
    max_balls_picked = defaultdict(int)
    for ball in all_balls:
        ball, number_picked = parse_ball(ball)
        total_balls_picked[ball] += number_picked
        if number_picked > max_balls_picked[ball]:
            max_balls_picked[ball] = number_picked
    return game_number, total_balls_picked, max_balls_picked

def part_one(all_games_str, ball_config):
    possible = []
    impossible = []
    for game in all_games_str.split('\n'):
        game_number, total_balls_picked, max_balls_picked = score_game(game)
        config_possible = True
        for ball, number_available in ball_config.items():
            if max_balls_picked[ball] > number_available:
                config_possible=False
                break
        if config_possible:
            possible.append(game_number)
        else:
            impossible.append(game_number)
    answer = sum(possible)
    return answer

def part_two(all_games_str):
    powers = []
    for game in all_games_str.split('\n'):
        game_number, total_balls_picked, max_balls_picked = score_game(game)
        power = max_balls_picked['blue']*max_balls_picked['red']*max_balls_picked['green']
        powers.append(power)
    answer = sum(powers)
    return answer

ball_config = {'red':12, 'green':13, 'blue':14}
part_one_example_answer = part_one(example, ball_config)
part_one_answer = part_one(data, ball_config)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)