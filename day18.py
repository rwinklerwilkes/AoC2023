from aocd import get_data
import re

data = get_data(day=18,year=2023)

example = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

def parse_data(data):
    matcher = r'([RDLU]) ([0-9]+) \((#[0-9a-z]{6})\)'
    parsed_data = []
    for line in data.split('\n'):
        gps = re.match(matcher, line).groups()
        parsed_data.append([gps[0], int(gps[1]), gps[2]])
    return parsed_data

def determine_inside(filled, row, col):
    edges = 0
    while col >= 0:
        if (row, col) in filled:
            edges += 1
        col -= 1
    if edges % 2 == 0:
        return False
    else:
        return True

def draw_board(filled):
    m = max([i[0] for i in filled])
    n = max([i[1] for i in filled])
    board = [['.' for j in range(n+1)] for i in range(m+1)]
    for f in filled:
        board[f[0]][f[1]] = '#'
    output = '\n'.join([''.join(row) for row in board])
    return output

def fill_board(parsed_data):
    filled = {(0, 0)}
    dir = {'R':[0,1],'U':[-1,0],'L':[0,-1],'D':[1,0]}
    row,col = 0,0
    for instruction in parsed_data:
        dir_to_go, num, _ = instruction
        while num > 0:
            drow, dcol = dir[dir_to_go]
            row += drow
            col += dcol
            filled.add((row,col))
            num -= 1
    return filled

def find_interior(filled):
    m = max([i[0] for i in filled])
    n = max([i[1] for i in filled])
    for i in range(m):
        for j in range(n):
            if (i,j) in filled:
                continue
            else:
                if determine_inside(filled, i, j):
                    return (i,j)


def flood_fill(filled):
    start_row, start_col = find_interior(filled)
    interior = set()
    q = [(start_row, start_col)]
    while q:
        r,c = q.pop()
        interior.add((r,c))
        check = [(r-1,c),(r+1, c),(r, c-1),(r, c+1)]
        for c in check:
            if c not in filled and c not in interior:
                q.append(c)
    return interior

def part_one(data):
    parsed_data = parse_data(data)
    filled = fill_board(parsed_data)
    interior = flood_fill(filled)
    answer = len(interior.union(filled))
    return answer

def parse_data_part_two(parsed_data):
    hex = [pd[2] for pd in parsed_data]
    dir = ['R','D','L','U']
    true_inst = []
    for h in hex:
        dir_to_use = dir[int(h[-1])]
        dist = int(h[1:-1],16)
        true_inst.append([dir_to_use, dist])
    return true_inst

import numpy as np

def poly_area(x,y):
    x = np.array(x, dtype=np.float64)
    y = np.array(y, dtype=np.float64)
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def part_two(data):
    parsed_data = parse_data(data)
    parsed_data_p2 = parse_data_part_two(parsed_data)
    dirs = {'R': [0, 1], 'U': [-1, 0], 'L': [0, -1], 'D': [1, 0]}
    total_points = 0
    loc = (0,0)
    rows = []
    cols = []
    for dir, dist in parsed_data_p2:
        actual_dir = dirs[dir]
        total_points += dist
        loc = (loc[0] + actual_dir[0] * dist, loc[1] + actual_dir[1] * dist)
        rows.append(loc[0])
        cols.append(loc[1])
    area = poly_area(rows, cols)
    b = total_points
    i = area + 1 - b // 2
    answer = int(i+b)
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)