from aocd import get_data

data = get_data(day=1,year=2023)
example = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

part_two_example = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

def extract_digits(instr):
    digits = [i for i in instr if i.isdigit()]
    first_last = digits[0] + digits[-1]
    return int(''.join(first_last))

def replace_word_digits(instr):
    start_char = 0
    new_str = instr
    while start_char < len(instr):
        end_char = start_char + 1
        while end_char <= len(instr):
            check_str = instr[start_char:end_char]
            if digit := string_to_num(check_str):
                #Sometimes the last letter overlaps - keep the last letter in for the "eighthree" case
                end_char -= 1
                check_str = instr[start_char:end_char]
                new_str = new_str.replace(check_str, str(digit), 1)
                #Skip remainder of while loop
                start_char = end_char - 1
                end_char = len(instr)
            end_char += 1
        start_char += 1
    return new_str


def string_to_num(word):
    string_to_num_dict = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }
    return string_to_num_dict.get(word,None)

def part_one(strings):
    return sum([extract_digits(instr) for instr in strings.split('\n')])

def part_two(strings):
    words_digits = [replace_word_digits(instr) for instr in strings.split('\n')]
    check_data = [extract_digits(i) for i in words_digits]
    return sum(check_data)

test_answer = part_one(example)
assert test_answer == 142
part_one_answer = part_one(data)
print(part_one_answer)

test_answer = part_two(part_two_example)
assert test_answer == 281
part_two_answer = part_two(data)
print(part_two_answer)

part_two('eightwo')
