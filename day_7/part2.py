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


def is_5_of_kind(hand_counter, nojs_counter, num_js):
    val, count = hand_counter.most_common(1)[0]
    if count == 5:
        return True
    else:
        val_noj, count_noj = nojs_counter.most_common(1)[0]
        return count_noj + num_js >= 5

def is_4_of_kind(hand_counter, nojs_counter, num_js):
    val, count = hand_counter.most_common(1)[0]
    val_noj, count_noj = nojs_counter.most_common(1)[0]
    return count == 4 or (count_noj + num_js >= 4)

def is_full_house(hand_counter, nojs_counter, num_js):
    c = hand_counter.most_common()
    c_noj = nojs_counter.most_common()
    return (len(c) == 2 and c[0][1] == 3) or (c_noj[0][1] == 2 and c_noj[1][1] == 2 and num_js >= 1) or  (c_noj[0][1] == 2 and num_js >= 2) or (num_js >= 3)

def is_three_of_a_kind(hand_counter, nojs_counter, num_js):
    val, count = hand_counter.most_common(1)[0]
    val_noj, count_noj = nojs_counter.most_common(1)[0]
    return count == 3 or (count_noj + num_js >= 3)

def is_two_pair(hand_counter, nojs_counter, num_js):
    c = hand_counter.most_common()
    c_noj = nojs_counter.most_common()
    return (len(c) == 3 and c[0][1] == 2 and c[1][1] == 2) or (
        c_noj[0][1] == 2 and num_js >= 1
    ) or (
        num_js >= 2
    )

def is_one_pair(hand_counter, nojs_counter, num_js):
    c = hand_counter.most_common()
    return (len(c) == 4 and c[0][1] == 2) or num_js > 0

def is_high_card(hand_counter, nojs_counter, num_js):
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
    'J': 1,
    'T': 10,
}
def card(c):
    return 15 - (CARDS.get(c) if c in CARDS else int(c))

def classify_hand(hand):
    hand_counter = Counter(hand)
    nojs_counter = Counter(hand.replace('J', ''))
    num_js = hand_counter.get('J', 0)
    for i, hand_type in enumerate(HAND_TYPES):
        if hand_type(hand_counter, nojs_counter, num_js):
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
    # part 1 - 250382098
    # for hand, rank in rank_hands(data).items():
    #     print(f'{hand}: {rank} {classify_hand(hand)[3]}')
    # print(classify_hand('A6JA6'))
    print(winnings(data))
