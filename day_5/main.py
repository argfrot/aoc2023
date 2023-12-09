def get_example_input():
    with open('day_5/example.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def get_input():
    with open('day_5/input.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def parse(line):
    return line.strip()

class RangeMapper:
    def __init__(self, destination_start, source_start, length) -> None:
        self.destination_start = destination_start
        self.source_start = source_start
        self.length = length

    def contains(self, source_id):
        return source_id >= self.source_start and source_id < self.source_start+self.length
        
    def map(self, source_id):
        if self.contains(source_id):
            return source_id + (self.destination_start-self.source_start)
        else:
            return source_id

class Mapper:
    def __init__(self, from_class, to_class) -> None:
        self.from_class = from_class
        self.to_class = to_class
        self.ranges = []
    
    def add_range(self, destination_start, source_start, length):
        self.ranges.append(RangeMapper(destination_start, source_start, length))

    def contains(self, source_id):
        return any(r.contains(source_id) for r in self.ranges)
    
    def map(self, source_id):
        for r in self.ranges:
            if r.contains(source_id):
                return r.map(source_id)
        return source_id

def test():
    m = RangeMapper(50, 98, 2)
    m2 = RangeMapper(52, 50, 48)

    r = Mapper('seed', 'soil')
    r.add_range(50,98,2)
    r.add_range(52,50,48)
    for i in range(100):
        print(f'{i=} {r.contains(i)=} {r.map(i)=}')

def build_mappers(data):
    seeds = []
    mappers = {}
    current_mapper = None
    for line in data:
        if line.startswith('seeds:'):
            seeds = list(map(int, line.split(':')[1].split()))
        elif not line.strip():
            continue
        elif 'map:' in line:
            a = line.split()[0].split('-')
            frm=a[0]
            to=a[2]
            current_mapper = Mapper(frm, to)
            mappers[frm] = current_mapper
        else:
            a = map(int, line.split())
            current_mapper.add_range(*a)
    return (seeds, mappers)

def follow_seed(seed, mappers):
    current_id = seed
    current_type = 'seed'
    while current_type in mappers:
        next_id = mappers[current_type].map(current_id)
        next_type = mappers[current_type].to_class
        current_id, current_type = next_id, next_type
    return current_id, current_type

if __name__ == '__main__':
    data = get_input()
    seeds, mappers = build_mappers(data)
    destinations = [follow_seed(seed, mappers) for seed in seeds]
    # part 1 - 57075758
    print(min(dest_id for dest_id, dest_type in destinations))
