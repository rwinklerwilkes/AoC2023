from aocd import get_data
import networkx as nx
import numpy as np

data = get_data(day=10,year=2023)

example = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

def add_safe(g, target, source ,direction):
    all_nodes = g.nodes(data=True)
    allows = {'|':['up','down'],
              '-':['left','right'],
              'L':['up','right'],
              'J':['up','left'],
              '7':['down','left'],
              'F':['down','right'],
              'S':['up','down','left','right'],
              '.':[],
              }
    target_shape = all_nodes[target]['shape']
    if direction in allows[target_shape]:
        g.add_edge(source, target)

def parse_data(data):
    g = nx.Graph()
    data_array = [[char for char in row] for row in data.split('\n')]
    data_array = np.pad(data_array, [(1, 1), (1, 1)], mode='constant', constant_values='.')
    m = data_array.shape[0]
    n = data_array.shape[1]
    for i, row in enumerate(data_array):
        for j, val in enumerate(row):
            g.add_node(n*i+j, shape=val, orig_coords = (i-1,j-1))
            if val == 'S':
                start = n*i+j

    for i, row in enumerate(data_array):
        for j, val in enumerate(row):
            current = n * i + j
            if current == 38:
                pass
            above = (i-1) * n + j
            below = (i+1) * n + j
            left = (n*i) + (j-1)
            right  = (n*i) + (j+1)
            match val:
                case '|':
                    add_safe(g, above, current, 'down')
                    add_safe(g, below, current, 'up')
                case '-':
                    add_safe(g, left, current, 'right')
                    add_safe(g, right, current, 'left')
                case 'L':
                    add_safe(g, above, current, 'down')
                    add_safe(g, right, current, 'left')
                case 'J':
                    add_safe(g, above, current, 'down')
                    add_safe(g, left, current, 'right')
                case '7':
                    add_safe(g, below, current, 'up')
                    add_safe(g, left, current, 'right')
                case 'F':
                    add_safe(g, below, current, 'up')
                    add_safe(g, right, current, 'left')
                case '.':
                    pass

    return g, start, (m,n)

def find_inside_outside(g, boundary, row, j):
    hits = 0
    all_nodes = g.nodes(data=True)
    while j >= 0:
        cell = row + j
        if cell in boundary and all_nodes[cell]['shape'] in ['|','L','J','S']:
            hits += 1
        j-=1
    if hits % 2 == 0:
        io = 'outside'
    else:
        io = 'inside'
    return io

def part_one(data):
    g, start, shape = parse_data(data)
    cyc = nx.find_cycle(g, start)
    answer = len(cyc)//2
    return answer

def part_two(data):
    g, start, shape = parse_data(data)
    m,n = shape
    cyc = nx.find_cycle(g, start)
    uniq_cyc = {i[0] for i in cyc}
    answer = 0
    for i in range(m):
        for j in range(n):
            if i*n + j in uniq_cyc:
                continue
            if find_inside_outside(g,uniq_cyc, i*n, j) == 'inside':
                answer += 1
    return answer

harder_example = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

part_one_example_answer = part_one(example)
part_one_harder_example_answer = part_one(harder_example)
part_one_answer = part_one(data)

part_two_easy_example = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

part_two_hard_example = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""



part_two_example_answer = part_two(part_two_easy_example)
part_two_harder_example_answer = part_two(part_two_hard_example)
part_two_answer = part_two(data)