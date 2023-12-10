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

    return g, start

def part_one(data):
    g, start = parse_data(data)
    cyc = nx.find_cycle(g, start)
    return len(cyc)//2

harder_example = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

part_one_example_answer = part_one(example)
part_one_harder_example_answer = part_one(harder_example)
part_one_answer = part_one(data)

g, start = parse_data(data)
g.edges(start)