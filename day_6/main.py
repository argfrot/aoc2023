from functools import reduce
import math
import operator

def get_example_input():
    with open('day_6/example.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def get_input():
    with open('day_6/input.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def parse(line):
    return line.strip()

def build_games(data):
    for line in data:
        if line.startswith('Time:'):
            times = list(map(int, line.split(':')[1].split()))
        elif line.startswith('Distance:'):
            distances = list(map(int, line.split(':')[1].split()))
    return list(zip(times, distances))

# y = t*(7-t) = 7t - t.t
#
# dy/dt = 7 - 2t = 0
# 2t = 7
# t = 7/2
# t = 3.5
# therefore max is at either 3 or 4
#
# we want to find intersection with the plane at y=9
# 7t - t.t = 9
# -t.t + 7t - 9 = 0
# a=-1, b=7 c=-9
# roots = (-b +/- sqrt(b.b - 4ac))/2a
#       = (-7 +/- sqrt(7*7 - 4*-1*-9))/2*-1
#       = (-7 +/- sqrt(49 - 36))/-2
#       = (-7 +/- sqrt(13))/-2
#       = (-7 +/- 3.61)/-2
#       = 1.695 or 5.305
# so winning between 2 and 5.
#
# taking the floor of low+1 and ceil of high-1 to
# handle the case where we land on the exact number
# (we want to beat the number so need to be bigger).

def find_game_limits(time, distance):
    a, b, c = -1, time, -distance
    i1 = b*b - 4*a*c
    i2 = math.sqrt(i1)
    low = (-b + i2)/(2*a)
    high = (-b - i2)/(2*a)
    return (math.floor(low+1),math.ceil(high-1))

if __name__ == '__main__':
    data = get_input()
    games = build_games(data)
    # part 1 - 1159152
    limits = [find_game_limits(t,d) for (t,d) in games]
    differences = [h-l+1 for (l,h) in limits]
    product = reduce(operator.mul, differences, 1)
    print(product)

    # part 2 - 41513103
    d = list(zip(*games))
    time = int(''.join([str(n) for n in d[0]]))
    distance = int(''.join([str(n) for n in d[1]]))
    low, high = find_game_limits(time, distance)
    print(high-low+1)