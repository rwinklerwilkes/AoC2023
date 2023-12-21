from aocd import get_data
from math import gcd

data = get_data(day=8,year=2023)

example = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

class Node:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

    def __repr__(self):
        return self.name

    def update_left_right(self, all_nodes):
        self.left = all_nodes[self.left]
        self.right = all_nodes[self.right]

def parse_data(data):
    instructions, nodes = data.split('\n\n')
    all_nodes = {}
    for row in nodes.split('\n'):
        node_name, inst = row.split(' = ')
        left = inst.split(', ')[0][1:]
        right = inst.split(', ')[1][:-1]
        all_nodes[node_name] = Node(node_name, left, right)
    for node in all_nodes.keys():
        all_nodes[node].update_left_right(all_nodes)
    return instructions, all_nodes

def part_one(data):
    instructions, all_nodes = parse_data(data)
    current_node = all_nodes['AAA']
    answer = 0
    inst_it = 0
    while current_node.name != 'ZZZ':
        instruction = instructions[inst_it]
        if instruction == 'L':
            current_node = current_node.left
        elif instruction == 'R':
            current_node = current_node.right
        inst_it += 1
        inst_it %= len(instructions)
        answer += 1
    return answer

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def part_two(data):
    instructions, all_nodes = parse_data(data)
    nodes_to_explore = [all_nodes[k] for k in all_nodes if k[-1] == 'A']
    cycles = {}
    inst_it = 0
    for node in nodes_to_explore:
        cycle_length = 0
        last_char = node.name[-1]=='Z'
        new_node = node
        while not last_char:
            instruction = instructions[inst_it]
            if instruction == 'L':
                new_node = new_node.left
            elif instruction == 'R':
                new_node = new_node.right
            inst_it += 1
            inst_it %= len(instructions)
            cycle_length += 1
            last_char = new_node.name[-1]=='Z'
        cycles[node.name] = cycle_length

    answer = 1
    for v in cycles.values():
        answer = answer * v//gcd(answer,v)
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

part_two_example_answer = part_two(part_two_example)
part_two_answer = part_two(data)