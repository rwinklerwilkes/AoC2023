from aocd import get_data
import re

data = get_data(day=5,year=2023)

example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

def parse_data(data):
    seeds, map = data.split('\n\n',maxsplit=1)
    seeds = seeds.split(': ')[-1]
    seeds = [int(i) for i in seeds.split(' ')]
    maps = map.split('\n\n')
    parsed_maps = [parse_map(map) for map in maps]
    return seeds, parsed_maps

def parse_map(map):
    title, rest = map.split('\n', maxsplit=1)
    title_re = r'([a-z]+)\-to\-([a-z]+)'
    first_title, second_title = list(re.match(title_re, title).groups())
    row_re = r'([0-9]+) ([0-9]+) ([0-9]+)'
    parsed_lines = []
    for line in rest.split('\n'):
        destination_start, source_start, length = list(re.match(row_re, line).groups())
        parsed_lines.append([int(i) for i in [destination_start, source_start, length]])
    return first_title, second_title, parsed_lines

def get_corresponding_value(map, i):
    ranges = map[2]
    value = None
    for full_range in ranges:
        destination_start, source_start, length = full_range
        if i >= source_start and i < source_start + length:
            value = (destination_start + i-source_start)
    if value is None:
        value = i
    return value

def convert_to_range(source, destination, length):
    return [(source, source+length), (destination, destination+length)]

# seeds, maps = parse_data(example)

def part_one(data):
    seeds, maps = parse_data(data)
    new_stage = [seeds]
    for m in maps:
        stage_to_use = new_stage[-1]
        new_stage.append([get_corresponding_value(m, s) for s in stage_to_use])
    answer = min(new_stage[-1])
    return answer

def map_range(map, range):
    ranges = [range]
    results = []
    while ranges:
        start_range, end_range = ranges.pop()
        for target, start_map, r in map:
            end_map = start_map + r
            offset = target - start_map
            if end_map <= start_range or end_range <= start_map:  # no overlap
                continue
            if start_range < start_map:
                ranges.append([start_range, start_map])
                start_range = start_map
            if end_map < end_range:
                ranges.append([end_map, end_range])
                end_range = end_map
            results.append([start_range + offset, end_range + offset])
            break
        else:
            results.append([start_range, end_range])
    return results

def map_all(maps, seeds):
    final_map = []
    for i in range(0, len(seeds), 2):
        ranges = [(seeds[i], seeds[i]+seeds[i+1])]
        results = []
        for map in maps:
            while ranges:
                range_to_use = ranges.pop()
                results += map_range(map[2], range_to_use)
            ranges = results
            results = []
        final_map += ranges
    return final_map

def part_two(data):
    seeds, maps = parse_data(data)
    final_map = map_all(maps, seeds)
    answer = min([x[0] for x in final_map])
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)