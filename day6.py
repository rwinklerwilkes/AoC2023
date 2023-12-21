from aocd import get_data
import re

data = get_data(day=6,year=2023)
example = """Time:      7  15   30
Distance:  9  40  200"""

def parse_data(data):
    time, distance = data.split('\n')
    time = [int(i.group()) for i in re.finditer('\d+',time)]
    distance = [int(i.group()) for i in re.finditer('\d+', distance)]
    return time, distance



def calculate_distances(time, distance):
    possible_distances = [time*i - i**2 for i in range(time+1)]
    winning_distances = [(dist > distance)*1 for dist in possible_distances]
    return possible_distances, winning_distances

def calculate_span(time, distance):
    t = 1
    while time - t <= (distance / t):
        t += 1
    first = t
    t = time
    while time - t <= (distance / t):
        t -= 1
    last = t
    return last-first+1


def part_one(data):
    times, distances = parse_data(data)
    answer = 1
    for t,d in zip(times, distances):
        # possible, winning = calculate_distances(t,d)
        # answer *= sum(winning)
        winning = calculate_span(t, d)
        answer *= winning
    return answer

def part_two(data):
    times, distances = parse_data(data)
    time = int(''.join([str(s) for s in times]))
    distance = int(''.join([str(s) for s in distances]))
    answer = calculate_span(time, distance)
    return answer


part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)
