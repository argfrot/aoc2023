from collections import Counter
from functools import reduce
import operator

def get_example_input():
    with open('day_7/example.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def get_input():
    with open('day_7/input.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def parse(line):
    return line.strip().split()


def is_5_of_kind(hand_counter):
    val, count = hand_counter.most_common(1)[0]
    return count == 5

def is_4_of_kind(hand_counter):
    val, count = hand_counter.most_common(1)[0]
    return count == 4

def is_full_house(hand_counter):
    c = hand_counter.most_common()
    return len(c) == 2 and c[0][1] == 3

def is_three_of_a_kind(hand_counter):
    val, count = hand_counter.most_common(1)[0]
    return count == 3

def is_two_pair(hand_counter):
    c = hand_counter.most_common()
    return len(c) == 3 and c[0][1] == 2 and c[1][1] == 2

def is_one_pair(hand_counter):
    c = hand_counter.most_common()
    return len(c) == 4 and c[0][1] == 2

def is_high_card(hand_counter):
    c = hand_counter.most_common()
    return len(c) == 5

HAND_TYPES = [
    is_5_of_kind,
    is_4_of_kind,
    is_full_house,
    is_three_of_a_kind,
    is_two_pair,
    is_one_pair,
    is_high_card,
]

CARDS = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
}
def card(c):
    return 15 - (CARDS.get(c) if c in CARDS else int(c))

def classify_hand(hand):
    hand_counter = Counter(hand)
    for i, hand_type in enumerate(HAND_TYPES):
        if hand_type(hand_counter):
            return i, tuple(map(card, hand)), hand, hand_type.__name__
    return None

def rank_hands(data):
    sorted_hands = sorted([classify_hand(hand) for (hand, bid) in data], reverse=True)
    return {hand: rank+1 for (rank, (_, _, hand, _)) in enumerate(sorted_hands)}

def winnings(data):
    ranks = rank_hands(data)
    return sum([ranks[hand]*int(bid) for (hand, bid) in data])

if __name__ == '__main__':
    data = get_input()
    # part 1 - 248569531
    # hand_classes = list([classify_hand(hand) for (hand, bid) in data])
    # for i, cards, hand, name in hand_classes:
    #     print(f'{i=} {hand=} {name=}')
    # print(rank_hands(data))
    print(winnings(data))
