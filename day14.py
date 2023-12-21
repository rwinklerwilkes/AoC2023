from aocd import get_data
import numpy as np

data = get_data(day=14,year=2023)
example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

def parse_data(data):
    movable = set()
    fixed = set()
    for i, row in enumerate(data.split('\n')):
        for j, tile in enumerate(row):
            if tile == 'O':
                movable.add((i,j))
            elif tile == '#':
                fixed.add((i,j))
        n_row = i+1
        n_col = len(row)

    for i in range(n_row):
        fixed.add((i, -1))
        fixed.add((i, n_col))
    for j in range(n_col):
        fixed.add((-1, j))
        fixed.add((n_row, j))

    return movable, fixed

def parse_board(data):
    board = []
    for i, row in enumerate(data.split('\n')):
        row_to_use = []
        for j, tile in enumerate(row):
            if tile == 'O':
                row_to_use.append(1)
            elif tile == '#':
                row_to_use.append(2)
            else:
                row_to_use.append(0)
        board.append(row_to_use)
    board = np.array(board)
    board = np.pad(board, 1, 'constant', constant_values=2)
    return board

def tilt_up(board):
    for col in range(board.shape[1]):
        for row in range(1,board.shape[0]):
            check_row = row
            finished = False
            while not finished:
                if board[check_row][col] == 1 and board[check_row-1][col] == 0:
                    board[check_row - 1][col] = 1
                    board[check_row][col] = 0
                    check_row -= 1
                else:
                    finished = True
    return board

def calculate_load(board):
    inner_board = board[1:-1,1:-1]
    nrows = inner_board.shape[0]
    weight = (inner_board==1)*np.tile([list(range(nrows, 0, -1))], (nrows, 1)).T
    return np.sum(weight)

def part_one(data):
    board = parse_board(data)
    tilted_board = tilt_up(board)
    answer = calculate_load(tilted_board)
    return answer

def find_cycle(board):
    cycle_detected = False
    previous_boards = [board]
    i = 1
    start_cycle = 0
    cycle_length = 0
    while not cycle_detected:
        prev = previous_boards[-1].copy()
        for rot_i, direction in enumerate(['up', 'left','down','right']):
            if rot_i > 0:
                prev = np.rot90(prev, k=-rot_i, axes=(0, 1))
            prev = tilt_up(prev)
            if rot_i > 0:
                prev = np.rot90(prev, k=rot_i, axes=(0, 1))
        next_board = prev
        for j, b in enumerate(previous_boards):
            if np.all(next_board==b):
                cycle_detected = True
                start_cycle = j
                cycle_length = i - start_cycle
        else:
            previous_boards.append(next_board)
        i += 1
    num_iter = (1000000000-start_cycle)//cycle_length
    left = 1000000000 - (num_iter*cycle_length + start_cycle)
    cycle = previous_boards[start_cycle:]
    return start_cycle, cycle_length, cycle[left]

def part_two(data):
    board = parse_board(data)
    start_cycle, cycle_length, board = find_cycle(board)
    answer = calculate_load(board)
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)