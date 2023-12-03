from aocd import get_data

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
    grid = [[symbol.replace('.','') for symbol in row] for row in data.split('\n')]
    return grid

def fix_grid(grid):
    new_grid = grid.copy()
    already_done = set()
    numbers = {}
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if (i,j) not in already_done:
                return_val, return_type = get_or_none(grid, i, j)
                if return_type == 'int':
                    number, used = construct_number(grid, i, j)
                    #Wasteful here to do this, but I don't care at this point
                    for (new_i, new_j) in used:
                        new_grid[new_i][new_j] = number
                    for s in used:
                        numbers[s] = used
                    already_done = already_done.union(used)
    return new_grid, numbers


def get_or_none(data, row, col):
    try:
        return_val = int(data[row][col])
        return_type = 'int'
    except ValueError:
        return_val = data[row][col]
        return_type = 'symbol'
    except IndexError:
        return_val = ''
        return_type = 'none'
    return return_val, return_type

def is_adjacent(data, row, col):
    #Decides if a particular row and column is adjacent to a symbol
    is_adj = False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i or j:
                val, val_type = get_or_none(data, row+i, col+j)
                if val and val_type == 'symbol':
                    is_adj = True
    return is_adj

def construct_number(data, row, col):
    number = data[row][col]
    used = set()
    used.add((row,col))
    going_left = True
    going_right = True
    i = 1
    while going_left or going_right:
        left_val, left_type = get_or_none(data, row, col-i)
        right_val, right_type = get_or_none(data, row, col+i)
        if left_val and left_type == 'int' and going_left:
            number = str(left_val) + number
            used.add((row, col-i))
        else:
            going_left = False
        if right_val and right_type == 'int' and going_right:
            number = number + str(right_val)
            used.add((row, col+i))
        else:
            going_right = False
        i += 1
    return int(number), used


def part_one(data):
    grid = parse_grid(data)
    new_grid, numbers = fix_grid(grid)
    used = set()
    adjacent_numbers = []
    for i, row in enumerate(new_grid):
        for j, col in enumerate(row):
            val, val_type = get_or_none(new_grid, i, j)
            if (i, j) not in used and val_type == 'int' and is_adjacent(grid, i, j):
                used = used.union(numbers[(i,j)])
                adjacent_numbers.append(val)
    return sum(adjacent_numbers), used

def part_two(data):
    pass

part_one_example_answer, _ = part_one(example)
part_one_answer, d_used = part_one(data)
#
# part_two_example_answer = part_two(example)
# part_two_answer = part_two(data)

# grid = parse_grid(example)
# new_grid, numbers = fix_grid(grid)
# # is_adjacent(data, 0, 2)
# construct_number(grid, 0, 2)

#
# from collections import defaultdict
# D = data
# lines = D.split('\n')
# G = [[c for c in line] for line in lines]
# R = len(G)
# C = len(G[0])
#
# p1 = 0
# nums = defaultdict(list)
# for r in range(len(G)):
#   gears = set() # positions of '*' characters next to the current number
#   n = 0
#   has_part = False
#   for c in range(len(G[r])+1):
#     if c<C and G[r][c].isdigit():
#       n = n*10+int(G[r][c])
#       for rr in [-1,0,1]:
#         for cc in [-1,0,1]:
#           if 0<=r+rr<R and 0<=c+cc<C:
#             ch = G[r+rr][c+cc]
#             if not ch.isdigit() and ch != '.':
#               has_part = True
#             if ch=='*':
#               gears.add((r+rr, c+cc))
#     elif n>0:
#       for gear in gears:
#         nums[gear].append(n)
#       if has_part:
#         p1 += n
#       n = 0
#       has_part = False
#       gears = set()
#
# print(p1)
# p2 = 0
# for k,v in nums.items():
#   if len(v)==2:
#     p2 += v[0]*v[1]
# print(p2)