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
        # print(f'split-self {self.source_start}-{self.source_end} -> {self.destination_start}-{self.destination_end} -- adj = {self.adjustment()}')
        # print(f'split-othr {other_range.source_start}-{other_range.source_end} -> {other_range.destination_start}-{other_range.destination_end} -- adj = {other_range.adjustment()}')
        adjustment = self.adjustment()
        other_adjustment = other_range.adjustment()

        before, overlap, after = None, None, None
        # 79-93 -> 42-56   -- adjustment = 42-79 = -37
        # 00-69 -> 01-70   -- adjustment = 01-00 = +1
        # overlaps? 42-56 & 00-69? whole range
        # new map: 79-93 -> 43-56

        # 79-93 -> 42-56   -- adjustment = 42-79 = -37
        # 45-50 -> 46-51   -- adjustment = 46-45 = +1
        # overlaps? 42-56 & 45-50? subset
        # new map: 79-81 -> 42-44 (-37), 82-87 -> 46-51 (-37+1), 88-93 -> 51-56 (-37)

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
                mapper = RangeMapper(self.destination_start, self.source_start, pre_length)
                # print(f'split-pre  {mapper.source_start}-{mapper.source_end} -> {mapper.destination_start}-{mapper.destination_end} -- adj = {mapper.adjustment()}')
                before = mapper
            # the overlap
            overlap_start_dest = max(other_range.source_start, self.destination_start)
            overlap_end_dest = min(self.destination_end, other_range.source_end)
            overlap_start_source = self.source_start+pre_length
            overlap_length = overlap_end_dest-overlap_start_dest+1
            mapper = RangeMapper(
                overlap_start_dest+other_adjustment,
                overlap_start_source,
                overlap_length,
            )
            # print(f'split-over {mapper.source_start}-{mapper.source_end} -> {mapper.destination_start}-{mapper.destination_end} -- adj = {mapper.adjustment()}')
            overlap = mapper
            # the after section
            post_length = max(self.destination_end-other_range.source_end, 0)
            if post_length>0:
                offset = pre_length+overlap_length
                mapper = RangeMapper(self.destination_start+offset, self.source_start+offset, self.length-offset)
                # print(f'split-post {mapper.source_start}-{mapper.source_end} -> {mapper.destination_start}-{mapper.destination_end} -- adj = {mapper.adjustment()}')
                after = mapper

        return before, overlap, after

    def split_overlaps_old(self, other_range):
        adjustment = self.adjustment()
        other_adjustment = other_range.adjustment()

        ranges =[]

        if self.contains(other_range.source_start) and self.contains(other_range.source_end):
            # the before section
            if self.source_start < other_range.source_start:
                ranges.append(RangeMapper(self.destination_start, self.source_start, other_range.source_start-self.source_start))
            # the overlap
            ranges.append(RangeMapper(other_range.destination_start+adjustment, other_range.source_start, other_range.length))
            # the after section
            if self.source_end > other_range.source_end:
                offset = other_range.source_end-self.source_start
                ranges.append(RangeMapper(self.destination_start+offset, self.source_start+offset, self.length-offset))

        elif self.contains(other_range.source_start):
            # the before section
            if self.source_start < other_range.source_start:
                ranges.append(RangeMapper(self.destination_start, self.source_start, other_range.source_start-self.source_start))
            # the overlap
            ranges.append(RangeMapper(other_range.destination_start+adjustment, other_range.source_start, self.length-(other_range.source_start-self.source_start)))

        elif self.contains(other_range.source_end):
            offset = other_range.source_end-self.source_start
            # the overlap
            ranges.append(RangeMapper(self.destination_start+other_adjustment, self.source_start, offset))
            # the after section
            if self.source_end > other_range.source_end:
                ranges.append(RangeMapper(self.destination_start+offset, self.source_start+offset, self.length-offset))

        elif self.overlaps(other_range):
            ranges.append(RangeMapper(self.destination_start+other_adjustment, self.source_start, self.length))

        else:
            ranges.append(self)

        return ranges

    def rev_contains(self, dest_id):
        return dest_id >= self.destination_start and dest_id < self.destination_start+self.length

    def rev_map(self, dest_id):
        if self.rev_contains(dest_id):
            return dest_id - (self.destination_start-self.source_start)
        else:
            return dest_id
    
    def __str__(self) -> str:
        return f'({self.destination_start},{self.source_start},{self.length})'


class Mapper:
    def __init__(self, from_class, to_class) -> None:
        self.from_class = from_class
        self.to_class = to_class
        self.ranges = []
    
    def add_range(self, destination_start, source_start, length):
        self.ranges.append(RangeMapper(destination_start, source_start, length))

    def replace_range(self, range, new_ranges):
        self.ranges.remove(range)
        self.ranges.extend(new_ranges)

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

    def rev_contains(self, dest_id):
        return any(r.rev_contains(dest_id) for r in self.ranges)
    
    def rev_map(self, dest_id):
        for r in self.ranges:
            if r.rev_contains(dest_id):
                return r.rev_map(dest_id)
        return dest_id

    def source_boundaries(self):
        rs = sorted(self.ranges, key=lambda x: x.source_start)
        boundaries = set()
        for r in rs:
            boundaries.add(r.source_start)
            boundaries.add(r.source_start+r.length-1)
        sbs = sorted(boundaries)
        print(f'RM {self.from_class=} {self.to_class=} {sbs=}')
        return sbs
    
    def dest_boundaries(self):
        rs = sorted(self.ranges, key=lambda x: x.destination_start)
        boundaries = set()
        for r in rs:
            boundaries.add(r.destination_start)
            boundaries.add(r.destination_start+r.length-1)
        dbs = sorted(boundaries)
        print(f'RM {self.from_class=} {self.to_class=} {dbs=}')
        return dbs

class BoundaryMapper:
    def __init__(self, mapper_a, mapper_b) -> None:
        self.mapper_a = mapper_a
        self.mapper_b = mapper_b
        self._source_boundaries = None
        self._dest_boundaries = None
    
    @property
    def from_class(self):
        return self.mapper_a.from_class
    
    @property
    def to_class(self):
        return self.mapper_b.to_class

    def contains(self, source_id):
        return self.mapper_a.contains(source_id)
    
    def map(self, source_id):
        return self.mapper_b.map(self.mapper_a.map(source_id))

    def rev_contains(self, source_id):
        return self.mapper_a.rev_contains(source_id)
    
    def rev_map(self, source_id):
        return self.mapper_b.rev_map(self.mapper_a.rev_map(source_id))

    def _calc_source_boundaries(self):
        print(f'csb {self.from_class}=>{self.to_class} {self.mapper_a.from_class}->{self.mapper_a.to_class} {self.mapper_b.from_class}->{self.mapper_b.to_class}')
        a = self.mapper_a.dest_boundaries()
        b = self.mapper_b.source_boundaries()
        combined = set(a).union(set(b))
        sbs = list(sorted([self.mapper_a.rev_map(cid) for cid in combined if self.mapper_a.rev_contains(cid)]))
        print(f'CM {self.from_class=} {self.to_class=} {sbs=}')
        return sbs

    def _calc_dest_boundaries(self):
        print(f'cdb {self.from_class}=>{self.to_class} {self.mapper_a.from_class}->{self.mapper_a.to_class} {self.mapper_b.from_class}->{self.mapper_b.to_class}')
        a = self.mapper_a.dest_boundaries()
        b = self.mapper_b.source_boundaries()
        combined = set(a).union(set(b))
        dbs = list(sorted([self.mapper_b.map(cid) for cid in combined]))
        print(f'CM {self.from_class=} {self.to_class=} {dbs=}')
        return dbs

    def source_boundaries(self):
        if not self._source_boundaries:
            self._source_boundaries = self._calc_source_boundaries()
        return self._source_boundaries

    def dest_boundaries(self):
        if not self._dest_boundaries:
            self._dest_boundaries = self._calc_dest_boundaries()
        return self._dest_boundaries

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

def follow_location(location, rev_mappers):
    current_id = location
    current_type = 'location'
    while current_type in rev_mappers:
        next_id = rev_mappers[current_type].rev_map(current_id)
        next_type = rev_mappers[current_type].from_class
        current_id, current_type = next_id, next_type
    return current_id, current_type


def expand_seeds(seeds):
    i = 0
    while i<len(seeds):
        start = seeds[i]
        length = seeds[i+1]
        i+=2
        for j in range(start, start+length):
            yield j

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

    # part 2 - ???? -- naive, too slow
    # destinations = [follow_seed(seed, mappers) for seed in expand_seeds(seeds)]
    # print(min(dest_id for dest_id, dest_type in destinations))

    # part 2 - ???? -- start from the end, not quite right
    # rev_seeds = [follow_location(location.destination_start, rev_mappers) for location in rev_mappers['location'].ranges]
    # print(list(seed_id for seed_id, seed_type in rev_seeds))

    # part 2 - ???? -- combine map functions together
    m0 = start_seed_map(seeds)
    mappers['start'] = m0

    #cm = combined_mapper(mappers, start_type='start', end_type='humidity')
    cm = combined_mapper(mappers, start_type='start')
    print(min([m.destination_start for m in cm.ranges]))
    # m1 = m0.combine_with(mappers['seed'])
    # m2 = m1.combine_with(mappers['soil'])
    # m3 = m2.combine_with(mappers['fertilizer'])
    # m4 = m3.combine_with(mappers['water'])
    # m5 = m4.combine_with(mappers['light'])
    # m6 = m5.combine_with(mappers['temperature'])
    # m7 = m6.combine_with(mappers['humidity'])

    # val=82
    # print(f'm0 {m0.map(val)} {m0.from_class:10}-> {m0.to_class:11} {list(str(r) for r in m0.ranges)}')
    # print(f'm1 {m1.map(val)} {m1.from_class:10}-> {m1.to_class:11} {list(str(r) for r in m1.ranges)}')
    # print(f'm2 {m2.map(val)} {m2.from_class:10}-> {m2.to_class:11} {list(str(r) for r in m2.ranges)}')
    # print(f'm3 {m3.map(val)} {m3.from_class:10}-> {m3.to_class:11} {list(str(r) for r in m3.ranges)}')
    # print(f'm4 {m4.map(val)} {m4.from_class:10}-> {m4.to_class:11} {list(str(r) for r in m4.ranges)}')
    # print(f'm5 {m5.map(val)} {m5.from_class:10}-> {m5.to_class:11} {list(str(r) for r in m5.ranges)}')
    # print(f'm6 {m6.map(val)} {m6.from_class:10}-> {m6.to_class:11} {list(str(r) for r in m6.ranges)}')
    # print(f'm7 {m7.map(val)} {m7.from_class:10}-> {m7.to_class:11} {list(str(r) for r in m7.ranges)}')
    # print(f'{list(str(r) for r in cm.ranges)}')
    # print(f'{cm.from_class=} {cm.to_class=} {cm.map(82)}')

    # 79-93 -> 42-56   -- adjustment = 42-79 = -37
    # 45-50 -> 46-51   -- adjustment = 46-45 = +1
    # overlaps? 42-56 & 45-50? subset
    # new map: 79-81 -> 42-44 (-37), 82-87 -> 46-51 (-37+1), 88-93 -> 51-56 (-37)
    # rm1 = RangeMapper(42, 79, 14)
    # rm2 = RangeMapper(46, 45, 5)

    # print(f'{rm1.source_start}-{rm1.source_end} -> {rm1.destination_start}-{rm1.destination_end} -- adj = {rm1.adjustment()}')
    # print(f'{rm2.source_start}-{rm2.source_end} -> {rm2.destination_start}-{rm2.destination_end} -- adj = {rm2.adjustment()}')
    # ranges = rm1.split_overlaps(rm2)
    # print(list(str(r) for r in ranges))

