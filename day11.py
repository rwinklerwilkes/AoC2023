from aocd import get_data
import numpy as np
from sklearn.metrics.pairwise import manhattan_distances

data = get_data(day=11,year=2023)
example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

def parse_data(data):
    galaxies = set()
    for row_num, row in enumerate(data.split('\n')):
        for col_num, char in enumerate(row):
            if char == '#':
                galaxies.add((row_num, col_num))
    return galaxies

def expand_galaxy(galaxies, num_to_shift=1):
    new_galaxies = []
    rows = {i[0] for i in galaxies}
    missing_rows = sorted(list(set(range(max(rows))) - rows))
    cols = {i[1] for i in galaxies}
    missing_cols = sorted(list(set(range(max(cols))) - cols))
    for galaxy in galaxies:
        shift_rows = len([i for i in missing_rows if i < galaxy[0]])
        shift_cols = len([i for i in missing_cols if i < galaxy[1]])
        new_galaxies.append([galaxy[0]+shift_rows*(num_to_shift-1), galaxy[1]+shift_cols*(num_to_shift-1)])
    new_galaxies = np.array(new_galaxies)
    return new_galaxies

def part_one(data):
    galaxies = parse_data(data)
    new_galaxies = expand_galaxy(galaxies)
    distances = manhattan_distances(new_galaxies)
    answer = np.sum(np.triu(distances))
    return int(answer)

def part_two(data, number_to_shift):
    galaxies = parse_data(data)
    new_galaxies = expand_galaxy(galaxies, number_to_shift)
    distances = manhattan_distances(new_galaxies)
    answer = np.sum(np.triu(distances))
    return int(answer)

part_one_example_answer = part_one(example)
assert part_one_example_answer == 374
part_one_answer = part_one(data)
print(part_one_answer)

part_two_example_answer_easy = part_two(example, 10)
assert part_two_example_answer_easy == 1030
part_two_example_answer_medium = part_two(example, 100)
assert part_two_example_answer_easy == 8410
part_two_answer = part_two(data, 1000000)
print(part_two_answer)