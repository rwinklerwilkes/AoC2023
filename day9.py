from aocd import get_data

data = get_data(day=9,year=2023)

example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

def parse_data(data):
    parsed_data = [[int(i) for i in sequence.split()] for sequence in data.split('\n')]
    return parsed_data

def extrapolate_sequence(sequence):
    finished = False
    all_sequences = [sequence.copy()]
    while not finished:
        current_sequence = all_sequences[-1]
        next_sequence = []
        for i in range(1, len(current_sequence)):
            next_sequence.append(current_sequence[i]-current_sequence[i-1])
        all_sequences.append(next_sequence)
        if min(next_sequence) == 0 and max(next_sequence) == 0:
            finished = True
    for i in range(len(all_sequences) - 2, -1, -1):
        last = all_sequences[i+1]
        last_val = last[-1]
        cur = all_sequences[i]
        cur_val = cur[-1]
        cur.append(cur_val + last_val)
    return all_sequences[0]

def part_one(data):
    parsed_data = parse_data(data)
    answer = 0
    for sequence in parsed_data:
        ext_sq = extrapolate_sequence(sequence)
        answer += ext_sq[-1]
    return answer

def part_two(data):
    parsed_data = parse_data(data)
    parsed_data = [list(reversed(seq)) for seq in parsed_data]
    answer = 0
    for sequence in parsed_data:
        ext_sq = extrapolate_sequence(sequence)
        answer += ext_sq[-1]
    return answer


part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)