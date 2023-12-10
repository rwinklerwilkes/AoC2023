from aocd import get_data
import networkx as nx
import numpy as np

data = get_data(day=10,year=2023)

example = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

def add_safe(g, source, target ,direction):
    all_nodes = g.nodes(data=True)
    allows = {'|':['up','down'],
              '-':['left','right'],
              'L':['up','right'],
              'J':['up','left'],
              '7':['down','left'],
              'F':['down','right']}
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
    start = None
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
                    add_safe(g, above, current, 'down')  # above
                    add_safe(g, below, current, 'up')  # below
                case '-':
                    g.add_edge(left, current)  # left
                    g.add_edge(right, current)  # right
                case 'L':
                    g.add_edge(above, current)  # above
                    g.add_edge(right, current)  # right
                case 'J':
                    g.add_edge(above, current)  # above
                    g.add_edge(left, current)  # left
                case '7':
                    g.add_edge(below, current)  # below
                    g.add_edge(left, current)  # left
                case 'F':
                    g.add_edge(below, current)  # below
                    g.add_edge(right, current)  # right
                case '.':
                    pass
                case 'S':
                    start = n * i + j


    return g, start

g, start = parse_data(example)
cyc = nx.find_cycle(g, start)
all_nodes = g.nodes(data=True)
for start, next in cyc:
    print(f'Start: {all_nodes[start]["shape"]}')

all_nodes[0]