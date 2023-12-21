from aocd import get_data
import numpy as np

data = get_data(day=13,year=2023)

example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

def parse_data(data):
    graphs = data.split('\n\n')
    all_graphs = []
    for graph in graphs:
        lines = graph.split('\n')
        new_graph = []
        for line in lines:
            new_line = []
            for cell in line:
                if cell == '#':
                    new_line.append(1)
                else:
                    new_line.append(0)
            new_graph.append(new_line)
        all_graphs.append(np.array(new_graph))
    return all_graphs

def check_mirror(graph, index, row_col,exact = True):
    actual = index - 1
    if row_col == 'row':
        m = graph.shape[0]
        l = index
        r = m - index
        nrow = min(l, r)
        mat_one = graph[(index - nrow):index, :]
        mat_two = graph[index:index + nrow, :]
        if min(mat_one.shape) == 0 or min(mat_two.shape) == 0:
            return False
        if exact:
            return np.all(mat_one == np.flipud(mat_two))
        else:
            return ((mat_one != np.flipud(mat_two)) * 1).sum() == 1
    elif row_col == 'col':
        n = graph.shape[1]
        l = index
        r = n - index
        ncol = min(l, r)
        mat_one = graph[:, (index - ncol):(index)]
        mat_two = graph[:, index:(index + ncol)]
        if min(mat_one.shape) == 0 or min(mat_two.shape) == 0:
            return False
        if exact:
            return np.all(mat_one == np.fliplr(mat_two))
        else:
            return ((mat_one != np.fliplr(mat_two))*1).sum() == 1


def find_mirror(graph, exact=True):
    for i, rc in enumerate(['row','col']):
        szidx = graph.shape[i]
        for index in range(1, szidx):
            if check_mirror(graph, index, rc, exact):
                return index, rc
    return 0, 'none'

def part_one(data):
    parsed_data = parse_data(data)
    answer = 0
    for graph in parsed_data:
        index, rc = find_mirror(graph)
        if rc == 'col':
            answer += index
        elif rc == 'row':
            answer += index*100
    return answer

def part_two(data):
    parsed_data = parse_data(data)
    answer = 0
    for graph in parsed_data:
        index, rc = find_mirror(graph,exact=False)
        if rc == 'col':
            answer += index
        elif rc == 'row':
            answer += index*100
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)