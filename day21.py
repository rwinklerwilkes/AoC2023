from aocd import get_data
import heapq

data = get_data(day=21,year=2023)

example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

def parse_data(data):
    plots = set()
    for rn, row in enumerate(data.split('\n')):
        for cn, cell in enumerate(row):
            if cell == '#':
                plots.add((rn,cn))
            if cell == 'S':
                start = (rn,cn)
    m = len(data.split('\n'))
    n = len(data.split('\n')[0])
    return plots, start, m, n

def take_steps(plots, start, m, n, steps_needed):
    steps_at_target = set()
    visited = set()
    q = [(0, start[0], start[1])]

    while q:
        steps, row, col = q.pop(0)
        if (steps, row, col) in visited:
            continue
        visited.add((steps, row, col))
        if steps == steps_needed:
            steps_at_target.add((row, col))
        else:
            if row-1 >= 0 and (row-1,col) not in plots:
                q.append((steps+1,row-1,col))
            if row+1 < m and (row+1,col) not in plots:
                q.append((steps + 1, row + 1, col))
            if col-1 >= 0 and (row,col-1) not in plots:
                q.append((steps+1,row,col-1))
            if col+1 < n and (row,col+1) not in plots:
                q.append((steps + 1, row, col+1))
    return steps_at_target

def part_one(data):
    plots, start, m, n = parse_data(data)
    steps_at_target = take_steps(plots, start, m, n, 64)
    answer = len(steps_at_target)
    return answer


part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

plots, start, m, n = parse_data(data)
steps_at_target = take_steps(plots, start, m, n, 196)
answer = len(steps_at_target)
#3738
#33270
#92194

#With much help from https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keao4q8/
f = lambda n,a,b,c: a+n*(b-a+(n-1)*(c-b-b+a)//2)
print(f(26501365 // 131, *[3738,33270,92194]))