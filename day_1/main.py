def get_example_input():
    with open('day_1/example.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def get_input():
    with open('day_1/input.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def parse(line):
    return line.strip()

def find_digits(s):
    return list(map(int, filter(str.isdigit, s)))

def first_and_last(l):
    return (l[0]*10 + l[-1]) if len(l) else 0

NUMBERS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5, 
    'six': 6, 
    'seven': 7, 
    'eight': 8, 
    'nine': 9,
}

def yield_from_spelled_digits(s):
    for i in range(len(s)):
        if str.isdigit(s[i]):
            yield int(s[i])
        else:

            for n in NUMBERS:
                if s[i:].startswith(n):
                    yield NUMBERS[n]

if __name__ == '__main__':
    data = get_input()
    # part 1 -- 55123
    print(sum(first_and_last(find_digits(l)) for l in data))
    # part 2 -- 55260
    print(sum(first_and_last(list(yield_from_spelled_digits(l))) for l in data))
