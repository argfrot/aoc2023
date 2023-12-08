def get_example_input():
    with open('day_2/example.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def get_input():
    with open('day_2/input.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def parse(line):
    a = line.split(':')
    game = int(a[0].split()[1])
    draws = a[1].split(';')
    reveals = []
    for draw in draws:
        red, green, blue = 0, 0, 0
        balls = draw.split(',')
        for ball in balls:
            n, colour = map(str.strip, ball.split())
            if colour == 'red':
                red = int(n)
            elif colour == 'green':
                green = int(n)
            elif colour == 'blue':
                blue = int(n)
            else:
                raise 'Unknown colour: %s' % colour
        reveals.append((red,green,blue))
    return (game, reveals)

def games_below_max(data, max_red, max_green, max_blue):
    for game, reveals in data:
        r,g,b = list(map(max, zip(*reveals)))
        if r<=max_red and g<=max_green and b<=max_blue:
            yield game

def game_power(data):
    for game, reveals in data:
        r,g,b = list(map(max, zip(*reveals)))
        yield r*g*b


if __name__ == '__main__':
    data = get_input()
    # part 1 - 2416
    print(sum(games_below_max(data, 12, 13, 14)))
    # part 2 - 63307
    print(sum(game_power(data)))

