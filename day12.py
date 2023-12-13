from aocd import get_data
data = get_data(day=12,year=2023)

example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

def parse_data(data):
    all_data = [line.split(' ') for line in data.split('\n')]
    return all_data

def score(springs):
    groups = []
    i = 0
    in_spring = False
    while i < len(springs):
        if not in_spring and springs[i] == '#':
            in_spring = True
            ct = 1
        elif in_spring and springs[i] == '#':
            ct += 1
        elif in_spring and springs[i] == '.':
            in_spring = False
            groups.append(ct)
        i += 1
    if in_spring:
        groups.append(ct)
    return ','.join([str(i) for i in groups])

#Modeled after https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/12.py
def dynamic_approach(springs:str, scores:list[int], spring_position:int, score_position:int, current_spring_length:int):
    cache_key = (spring_position, score_position, current_spring_length)
    if cache_key in cache:
        return cache[cache_key]
    if spring_position == len(springs):
        if score_position == len(scores) and current_spring_length == 0:
            return 1
        elif score_position == len(scores)-1 and scores[score_position] == current_spring_length:
            return 1
        else:
            return 0
    answer = 0
    for char in ['.', '#']:
        if springs[spring_position] == char or springs[spring_position] == '?':
            if char == '.' and current_spring_length == 0:
                answer += dynamic_approach(springs, scores, spring_position+1, score_position, 0)
            elif char == '.' and current_spring_length > 0 and score_position<len(scores) and scores[score_position]==current_spring_length:
                answer += dynamic_approach(springs, scores, spring_position+1, score_position+1, 0)
            elif char == '#':
                answer += dynamic_approach(springs, scores, spring_position + 1, score_position, current_spring_length + 1)
    cache[cache_key] = answer
    return answer

cache = {}

def part_one(data):
    parsed_data = parse_data(data)
    final_answer = 0
    for line in parsed_data:
        springs, scores = line
        scores = [int(i) for i in scores.split(',')]
        answer = dynamic_approach(springs, scores, 0, 0, 0,)
        final_answer += answer
        cache.clear()

    return final_answer

def part_two(data):
    parsed_data = parse_data(data)
    final_answer = 0
    for line in parsed_data:
        springs, scores = line
        springs = '?'.join([springs, springs, springs, springs, springs])
        scores = ','.join([scores, scores, scores, scores, scores])
        scores = [int(i) for i in scores.split(',')]
        answer = dynamic_approach(springs, scores, 0, 0, 0, )
        final_answer += answer
        cache.clear()

    return final_answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)