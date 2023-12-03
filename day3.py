from collections import defaultdict

from aocd import get_data
import re

data = get_data(day=3, year=2023)
example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

def parse_grid(data):
    grid = [[symbol for symbol in row] for row in data.split('\n')]
    return grid

def find_symbols(grid):
    all_symbols = set()
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val not in '0123456789.':
                all_symbols.add((i,j))
    return all_symbols

def is_adjacent(all_symbols, i, j):
    for i_val in range(-1, 2):
        for j_val in range(-1, 2):
            if (i+i_val, j+j_val) in all_symbols:
                return True, (i+i_val, j+j_val)
    return False, None

def find_numbers(grid, all_symbols):
    adjacent_numbers = []
    adjacent_count = defaultdict(int)
    adjacent_to = defaultdict(list)
    for row_num, row in enumerate(grid):
        row_str = ''.join(row)
        all_matches = re.finditer(r'\d+', row_str)
        for match in all_matches:
            for col_num in range(*match.span()):
                is_adj, adj_spot = is_adjacent(all_symbols, row_num, col_num)
                if is_adj:
                    adjacent_count[adj_spot] += 1
                    number = int(match[0])
                    adjacent_to[adj_spot].append(number)
                    adjacent_numbers.append(number)
                    break
    return adjacent_numbers, adjacent_count, adjacent_to

def part_one_and_two(data):
    grid = parse_grid(data)
    all_symbols = find_symbols(grid)
    all_adjacent, adjacent_count, adjacent_to = find_numbers(grid, all_symbols)
    part_one = sum(all_adjacent)
    part_two = 0
    for k, v in adjacent_count.items():
        if v == 2:
            part_two += adjacent_to[k][0] * adjacent_to[k][1]
    return part_one, part_two

part_one_example_answer, part_two_example_answer = part_one_and_two(example)
part_one_answer, part_two_answer = part_one_and_two(data)