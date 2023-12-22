from aocd import get_data
from collections import defaultdict

data = get_data(day=22,year=2023)

example = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

def parse_data(data):
    all_bricks = []
    for row in data.split('\n'):
        brick = [int(r) for r in row.split('~')[0].split(',')] + [int(r) for r in row.split('~')[1].split(',')]
        all_bricks.append(brick)
    return all_bricks

def drop_brick(tallest_brick, brick):
    sx, fx = brick[0], brick[3]
    sy, fy = brick[1], brick[4]
    sz, fz = brick[2], brick[5]
    tallest_in_range = max(tallest_brick[(x,y)] for x in range(sx, fx+1) for y in range(sy, fy+1))
    if sz > tallest_in_range:
        diff_z = sz - tallest_in_range - 1
    else:
        diff_z = 0
    new_brick = (sx, sy, sz-diff_z, fx, fy, fz-diff_z)
    if diff_z != 0:
        fell = True
    else:
        fell = False
    return new_brick, fell

def drop(all_bricks):
    tallest_brick = defaultdict(int)
    dropped_tower = []
    number_fell = 0
    for brick in all_bricks:
        new_brick, fell = drop_brick(tallest_brick, brick)
        if fell:
            number_fell += 1
        sx, fx = brick[0], brick[3]
        sy, fy = brick[1], brick[4]
        dropped_tower.append(new_brick)
        for x in range(sx, fx+1):
            for y in range(sy, fy+1):
                new_fz = new_brick[5]
                tallest_brick[(x,y)] = new_fz
    return dropped_tower, number_fell

def part_one(data):
    parsed_bricks = parse_data(data)
    parsed_bricks = sorted(parsed_bricks, key=lambda x: x[2])
    dropped_tower, number_fell = drop(parsed_bricks)
    answer = 0
    for i in range(len(dropped_tower)):
        removed = dropped_tower.copy()
        _ = removed.pop(i)
        new_dropped_tower, number_fell = drop(removed)
        if number_fell == 0:
            answer += 1
    return answer

def part_two(data):
    parsed_bricks = parse_data(data)
    parsed_bricks = sorted(parsed_bricks, key=lambda x: x[2])
    dropped_tower, number_fell = drop(parsed_bricks)
    answer = 0
    for i in range(len(dropped_tower)):
        removed = dropped_tower.copy()
        _ = removed.pop(i)
        new_dropped_tower, number_fell = drop(removed)
        if number_fell > 0:
            answer += number_fell
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)