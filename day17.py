from aocd import get_data
import heapq

data = get_data(day=17,year=2023)
example = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

def parse_data(data):
    return [[int(c) for c in row] for row in data.split('\n')]

def solve(parsed_data, part_two = False):
    q = [(0,0,0,-1,-1)]
    distances = {}
    directions = [[-1,0],[0,1],[1,0],[0,-1]] #up right down left
    m = len(parsed_data)
    n = len(parsed_data[0])
    while q:
        dist, row, col, current_dir, num_traveled = heapq.heappop(q)
        if (row, col, current_dir, num_traveled) in distances:
            continue
        distances[(row, col, current_dir, num_traveled)] = dist
        for i, (drow, dcol) in enumerate(directions):
            new_row = row + drow
            new_col = col + dcol
            new_dir = i
            need_new_direction = (1 if new_dir != current_dir else num_traveled + 1)
            going_backwards = ((new_dir + 2)%4 != current_dir)
            if not part_two:
                valid_distance = need_new_direction <= 3
            else:
                valid_distance = need_new_direction <= 10 and (num_traveled >= 4 or new_dir == current_dir or current_dir == -1)
            if 0<=new_row and new_row < m and 0<= new_col and new_col < n and valid_distance and going_backwards:
                cost = parsed_data[new_row][new_col]
                heapq.heappush(q, (dist+cost, new_row, new_col, new_dir, need_new_direction))
    return distances


def part_one(data):
    parsed_data = parse_data(data)
    distances = solve(parsed_data)
    m = len(parsed_data)
    n = len(parsed_data[0])
    answer = 1e20
    for k,v in distances.items():
        if k[0] == m-1 and k[1] == n-1:
            answer = min(answer, v)
    return answer

def part_two(data):
    parsed_data = parse_data(data)
    distances = solve(parsed_data, part_two=True)
    m = len(parsed_data)
    n = len(parsed_data[0])
    answer = 1e20
    for k, v in distances.items():
        if k[0] == m - 1 and k[1] == n - 1:
            answer = min(answer, v)
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)