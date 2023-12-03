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

def get_or_none(data, row, col):
    try:
        return_val = int(data[row][col])
    except ValueError:
        return_val = data[row][col]
    except IndexError:
        return_val = ''
    return return_val

def is_adjacent(data, row, col):
    #Decides if a particular row and column is adjacent to a symbol
    is_adj = False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i or j:
                val = get_or_none(data, row+i, col+j)
                if val and type(val) != int:
                    is_adj = True
    return is_adj

def construct_number(data, row, col):
    number = data[row][col]
    going_left = True
    going_right = True
    i = 1
    while going_left or going_right:
        left_val = get_or_none(data, row, col-i)
        right_val = get_or_none(data, row, col+i)
        if left_val and type(left_val) == int and going_left:
            number = str(left_val) + number
        else:
            going_left = False
        if right_val and type(right_val) == int and going_right:
            number = number + str(right_val)
        else:
            going_right = False
        i += 1
    return int(number)


def part_one(data):
    pass

def part_two(data):
    pass

# part_one_example_answer = part_one(example)
# part_one_answer = part_one(data)
#
# part_two_example_answer = part_two(example)
# part_two_answer = part_two(data)

data = parse_grid(example)
# is_adjacent(data, 0, 2)
construct_number(data, 0, 2)