def pairs(l):
    i = 0
    while i < len(l):
        a = l[i]
        b = l[i+1]
        yield a, b
        i += 2

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
        
    def dest_contains(self, dest_id):
        return dest_id >= self.destination_start and dest_id < self.destination_start+self.length

    def map(self, source_id):
        if self.contains(source_id):
            return source_id + (self.destination_start-self.source_start)
        else:
            return source_id

    def adjustment(self):
        return self.destination_start-self.source_start

    @property
    def source_end(self):
        return self.source_start+self.length-1

    @property
    def destination_end(self):
        return self.destination_start+self.length-1

    def overlaps(self, other_range):
        return (
            self.contains(other_range.source_start)
            or self.contains(other_range.source_end)
            or (
                other_range.source_start < self.source_start
                and other_range.source_end > self.source_end
            )
        )

    def split_overlaps(self, other_range):
        adjustment = self.adjustment()
        other_adjustment = other_range.adjustment()

        before, overlap, after = None, None, None

        if (
            other_range.contains(self.destination_start)
            or other_range.contains(self.destination_end)
            or (
                self.destination_start < other_range.source_start
                and self.destination_end > other_range.source_end
            )
        ):
            # the before section
            pre_length = max(other_range.source_start-self.destination_start, 0)
            if pre_length>0:
                before = RangeMapper(self.destination_start, self.source_start, pre_length)
            # the overlap
            overlap_start_dest = max(other_range.source_start, self.destination_start)
            overlap_end_dest = min(self.destination_end, other_range.source_end)
            overlap_start_source = self.source_start+pre_length
            overlap_length = overlap_end_dest-overlap_start_dest+1
            overlap = RangeMapper(
                overlap_start_dest+other_adjustment,
                overlap_start_source,
                overlap_length,
            )
            # the after section
            post_length = max(self.destination_end-other_range.source_end, 0)
            if post_length>0:
                offset = pre_length+overlap_length
                after = RangeMapper(self.destination_start+offset, self.source_start+offset, self.length-offset)

        return before, overlap, after
    
    def __str__(self) -> str:
        return f'({self.destination_start},{self.source_start},{self.length})'


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

    def copy(self):
        new_mapper = Mapper(self.from_class, self.to_class)
        new_mapper.ranges = self.ranges.copy()
        return new_mapper

    def combine_with(self, other_mapper):
        assert self.to_class == other_mapper.from_class
        new_mapper = self.copy()
        new_mapper.to_class = other_mapper.to_class
        new_ranges = []
        ranges = new_mapper.ranges
        while ranges:
            range = ranges.pop(0)
            for other_range in other_mapper.ranges:
                before, overlap, after = range.split_overlaps(other_range)
                if overlap:
                    new_ranges.append(overlap)
                    if before:
                        ranges.append(before)
                    if after:
                        ranges.append(after)
                    break
            else:
                new_ranges.append(range)

        new_mapper.ranges = new_ranges
        return new_mapper


def build_mappers(data):
    seeds = []
    mappers = {}
    rev_mappers = {}
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
            rev_mappers[to] = current_mapper
        else:
            a = map(int, line.split())
            current_mapper.add_range(*a)
    return (seeds, mappers, rev_mappers)

def follow_seed(seed, mappers, until=None):
    current_id = seed
    current_type = 'seed'
    while current_type in mappers and current_type != until:
        next_id = mappers[current_type].map(current_id)
        next_type = mappers[current_type].to_class
        current_id, current_type = next_id, next_type
    return current_id, current_type

def combined_mapper(mappers, start_type='seed', end_type=None):
    mapper = mappers[start_type]
    next_type = mappers[start_type].to_class
    while next_type in mappers and next_type != end_type:
        mapper = mapper.combine_with(mappers[next_type])
        next_type = mappers[next_type].to_class
    return mapper

def start_seed_map(seeds):
    m = Mapper('start', 'seed')
    for (a,b) in pairs(seeds):
        m.add_range(a, a, b)
    return m

if __name__ == '__main__':
    data = get_input()
    seeds, mappers, rev_mappers = build_mappers(data)
    # part 1 - 57075758
    destinations = [follow_seed(seed, mappers) for seed in seeds]
    print(min(dest_id for dest_id, dest_type in destinations))

    # part 2 - 31161857 -- combine map functions together
    m0 = start_seed_map(seeds)
    mappers['start'] = m0
    cm = combined_mapper(mappers, start_type='start')
    print(min([m.destination_start for m in cm.ranges]))
