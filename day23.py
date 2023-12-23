from collections import defaultdict
from aocd import get_data

data = get_data(day=23, year=2023)

example = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

def parse_data(data):
    parsed_data = [[c for c in row] for row in data.split('\n')]
    start = parsed_data[0].index('.')
    finish = parsed_data[-1].index('.')
    return parsed_data, (0,start), (len(parsed_data)-1,finish)


def get_edges(graph):
    m = len(graph)
    n = len(graph[0])
    edges = defaultdict(set)
    neighbors = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for r, row in enumerate(graph):
        for c, val in enumerate(row):
            for dr, dc in neighbors:
                nr = r + dr
                nc = c + dc
                if val == '.':
                    if nr >= 0 and nr < m and nc >= 0 and nc < n:
                        if graph[nr][nc] == '.':
                            edges[(r,c)].add((nr,nc))
                            edges[(nr, nc)].add((r, c))
            if val == '>':
                edges[(r, c)].add((r, c+1))
                edges[(r, c-1)].add((r, c))
            if val == 'v':
                edges[(r, c)].add((r+1, c))
                edges[(r-1, c)].add((r, c))

    return edges

def get_edges_part_two(graph):
    m = len(graph)
    n = len(graph[0])
    edges = defaultdict(set)
    neighbors = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for r, row in enumerate(graph):
        for c, val in enumerate(row):
            for dr, dc in neighbors:
                nr = r + dr
                nc = c + dc
                if nr >= 0 and nr < m and nc >= 0 and nc < n:
                    if val in '.>v':
                        if graph[nr][nc] in '.>v':
                            edges[(r,c)].add((nr,nc,1))
                            edges[(nr, nc)].add((r, c,1))

    return edges

#Thanks to /u/qwewqa/ for this trick
def merge_edges(edges_part_two):
    finished = False
    new_edges = edges_part_two.copy()
    while not finished:
        for (cr, cc), e in new_edges.items():
            if len(e) == 2:
                left, right = e
                lr, lc, ldist = left
                rr, rc, rdist = right
                new_edges[(lr,lc)].remove((cr, cc, ldist))
                new_edges[(rr,rc)].remove((cr, cc, rdist))
                new_edges[(lr,lc)].add((rr, rc, ldist + rdist))
                new_edges[(rr, rc)].add((lr, lc, ldist + rdist))
                del new_edges[(cr, cc)]
                break
        else:
            finished = True
    return new_edges

def dfs(graph, start, finish):
    edges = get_edges(graph)
    discovered = set()
    r,c = start
    q = [(r,c,0)]
    best = 0
    while q:
        cr, cc, cdist = q.pop()
        if cdist == -1:
            discovered.remove((cr, cc))
            continue
        if (cr, cc) == finish:
            best = max(best, cdist)
            continue
        if (cr, cc) not in discovered:
            discovered.add((cr, cc))
            q.append((cr, cc, -1))
            next_edges = edges[(cr, cc)]
            for (nr, nc) in next_edges:
                q.append((nr, nc, cdist+1))
    return best

def dfs_part_two(graph, start, finish):
    edges = get_edges_part_two(graph)
    merged_edges = merge_edges(edges)
    discovered = set()
    r,c = start
    q = [(r,c,0)]
    best = 0
    while q:
        cr, cc, cdist = q.pop()
        if cdist == -1:
            discovered.remove((cr, cc))
            continue
        if (cr, cc) == finish:
            best = max(best, cdist)
            continue
        if (cr, cc) not in discovered:
            discovered.add((cr, cc))
            q.append((cr, cc, -1))
            next_edges = merged_edges[(cr, cc)]
            for (nr, nc, ndist) in next_edges:
                q.append((nr, nc, cdist+ndist))
    return best

def part_one(data):
    graph, start, finish = parse_data(data)
    answer = dfs(graph, start, finish)
    return answer

def part_two(data):
    graph, start, finish = parse_data(data)
    answer = dfs_part_two(graph, start, finish)
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)