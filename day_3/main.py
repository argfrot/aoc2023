from collections import defaultdict

def get_example_input():
    with open('day_3/example.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def get_input():
    with open('day_3/input.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def parse(line):
    return line.strip()

class Cell:
    def __init__(self, row, col, val) -> None:
        self.row = row
        self.col = col
        self.val = val
        self.part_number = None
        self.part_id = None

    def __str__(self) -> str:
        #return self.val
        return self.val if not self.part_number else '@'

class Grid:
    def __init__(self) -> None:
        self.grid = defaultdict(dict)
        self.num_rows = 0
        self.num_cols = 0

    def add_cell(self, row, col, val):
        self.grid[row][col] = Cell(row, col, val)
        self.num_rows = max(self.num_rows, row+1)
        self.num_cols = max(self.num_cols, col+1)

    def get_cell(self, row, col):
        return self.grid[row][col]

    def row_slice(self, row, col_start, col_end):
        for col in range(col_start, col_end):
            yield self.get_cell(row, col)

    def clip_row(self, row):
        return min(self.num_rows, max(row, 0))

    def clip_col(self, col):
        return min(self.num_cols, max(col, 0))

    def neighbours(self, cell):
        for row in range(self.clip_row(cell.row-1), self.clip_row(cell.row+2)):
            for col in range(self.clip_col(cell.col-1), self.clip_col(cell.col+2)):
                if row != cell.row or col != cell.col:
                    yield self.get_cell(row, col)

    def draw_grid(self, highlight=[]):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if (row,col) in highlight:
                    c = '|'
                else:
                    c = self.get_cell(row, col)
                print(c, end='')
            print()


def generate_grid(data):
    grid = Grid()
    for row, row_data in enumerate(data):
        part_number = None
        for col, val in enumerate(row_data):
            grid.add_cell(row, col, val)
            if str.isdigit(val):
                if part_number is None:
                    part_number = [val]
                else:
                    part_number.append(val)
            elif part_number is not None:
                for cell in grid.row_slice(row, col-len(part_number), col):
                    cell.part_number = int(''.join(part_number))
                    cell.part_id = (row, col-len(part_number))
                part_number = None
        # number at end of row
        if part_number is not None:
            col+=1
            for cell in grid.row_slice(row, col-len(part_number), col):
                cell.part_number = int(''.join(part_number))
                cell.part_id = (row, col-len(part_number))
            part_number = None
    return grid

def search_for_parts(grid):
    parts = set()
    part_ids = set()
    count = 0
    for row in range(grid.num_rows):
        for col in range(grid.num_cols):
            cell = grid.get_cell(row, col)
            if not str.isdigit(cell.val) and cell.val != '.':
                for other_cell in grid.neighbours(cell):
                    if other_cell.part_number:
                        count += 1
                        parts.add(other_cell.part_number)
                        part_ids.add(other_cell.part_id)
    return [grid.get_cell(row, col).part_number for (row,col) in part_ids]

if __name__ == '__main__':
    data = get_input()
    grid = generate_grid(data)
    parts = search_for_parts(grid)
    # part 1 - 532445
    print(sum(parts))
    # grid.draw_grid()
    # print([(c.row, c.col) for c in grid.neighbours(grid.get_cell(0,0))])
    # grid.draw_grid(highlight=[(c.row,c.col) for c in grid.neighbours(grid.get_cell(0,0))])
    # grid.draw_grid(highlight=[(c.row,c.col) for c in grid.neighbours(grid.get_cell(grid.num_rows-1,grid.num_cols-1))])
    # grid.draw_grid(highlight=[(c.row,c.col) for c in grid.neighbours(grid.get_cell(5,5))])
