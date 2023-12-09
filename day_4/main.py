def get_example_input():
    with open('day_4/example.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def get_input():
    with open('day_4/input.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def parse(line):
    s = line.split(":")
    card = int(s[0].split()[1])
    numbers = s[1].split("|")
    winners = set(map(int, numbers[0].split()))
    my_numbers = set(map(int, numbers[1].split()))
    return (card, winners, my_numbers)

def winner_points(data):
    for (card, winners, my_numbers) in data:
        win = winners.intersection(my_numbers)
        if win:
            yield 2**(len(win)-1)

def how_many_winners(data):
    for (card, winners, my_numbers) in data:
        win = winners.intersection(my_numbers)
        yield (card, len(win))

def scratch_card_wins(data):
    cards = list(how_many_winners(data))
    copies = [1]*len(cards)
    for i, (card, winners) in enumerate(cards):
        for c in range(i+1, i+1+winners):
            copies[c]+=copies[i]
    return copies

if __name__ == '__main__':
    data = get_input()
    # part 1 - 21213
    print(sum(winner_points(data)))
    # part 2 - 8549735
    print(sum(scratch_card_wins(data)))
