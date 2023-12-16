from aocd import get_data
import numpy as np
data = get_data(day=16,year=2023)

example = """.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""

def parse_data(data):
    board = [[char for char in row] for row in data.split('\n')]
    board = np.array(board)
    board = np.pad(board, 1, mode='constant', constant_values='E')
    return board

def add_with_visited(rays, visited, ray):
    if ray not in visited:
        rays.append(ray)
    return rays


def shoot_ray(board, starting_ray=(1,1,'R')):
    rays = [starting_ray]
    dirs = {'R':(0,1),'U':(-1,0),'L':(0,-1),'D':(1,0)}
    new_dirs = {'R': {'|': ['U', 'D'], '/': ['U'], '\\': ['D']},
                'L': {'|': ['U', 'D'], '/': ['D'], '\\': ['U']},
                'U': {'-': ['L', 'R'], '/': ['R'], '\\': ['L']},
                'D': {'-': ['L', 'R'], '/': ['L'], '\\': ['R']},
                }
    energized = set()
    visited = set()
    while rays:
        cur_ray = rays.pop()
        row = cur_ray[0]
        col = cur_ray[1]
        dir = cur_ray[2]
        #Check if we've been here already
        if (row, col, dir) in visited:
            #Don't run through here again
            pass
        else:
            spot = board[row][col]
            drow, dcol = dirs[dir]
            if spot == 'E':
                pass
            else:
                energized.add((row, col))
                visited.add((row, col, dir))
                to_add = new_dirs[dir].get(spot)
                if to_add:
                    for new_dir in to_add:
                        drow, dcol = dirs[new_dir]
                        rays = add_with_visited(rays, visited, (row+drow, col+dcol, new_dir))
                else:
                    rays = add_with_visited(rays, visited, (row+drow, col+dcol, dir))

    return energized

def part_one(data):
    board = parse_data(data)
    energized = shoot_ray(board)
    answer = len(energized)
    return answer

def part_two(data):
    board = parse_data(data)
    max_score = 0
    for r in range(1, board.shape[0]-1):
        rscore = len(shoot_ray(board,(r,1,'R')))
        lscore = len(shoot_ray(board,(r,board.shape[0]-2,'L')))
        if rscore > max_score:
            max_score = rscore
        if lscore > max_score:
            max_score = lscore
    for c in range(1, board.shape[1]-1):
        rscore = len(shoot_ray(board,(1,c,'D')))
        lscore = len(shoot_ray(board,(board.shape[1]-2,c,'U')))
        if rscore > max_score:
            max_score = rscore
        if lscore > max_score:
            max_score = lscore
    answer = max_score
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)