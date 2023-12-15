from aocd import get_data
from collections import defaultdict
data = get_data(day=15,year=2023)
example = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

class Lens:
    def __init__(self, string):
        self.label, self.length, self.box = self.label_and_length(string)

    def __repr__(self):
        return f'{self.label} {self.length}'

    def label_and_length(self, string):
        label, length = string.split('=')
        box = run_hash(label)
        return label, int(length), box

def run_hash(string):
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value

def perform_operation(all_boxes, instr):
    if instr[-1]=='-':
        lens = instr[:-1]
        box = run_hash(lens)
        dest_box = all_boxes[box]
        dest_box_labels = [l.label for l in dest_box]
        try:
            idx = dest_box_labels.index(lens)
            dest_box.pop(idx)
        except ValueError:
            pass
    else:
        l = Lens(instr)
        dest_box = all_boxes[l.box]
        dest_box_labels = [l.label for l in dest_box]
        try:
            idx = dest_box_labels.index(l.label)
            dest_box.pop(idx)
            dest_box.insert(idx, l)
        except ValueError:
            dest_box.append(l)
    return all_boxes

def part_one(data):
    answer = 0
    for instr in data.split(','):
        answer += run_hash(instr)
    return answer

def part_two(data):
    all_boxes = defaultdict(list)
    for instr in data.split(','):
        all_boxes = perform_operation(all_boxes, instr)

    answer = 0
    for box_num, lenses in all_boxes.items():
        box_total = 0
        for i, lens in enumerate(lenses):
            box_total += (box_num+1) * (i+1) * lens.length
        answer += box_total
    return answer


part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)