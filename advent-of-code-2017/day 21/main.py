"""Advent of Code 2017 Day 21."""

OFF = '.'
ON = '#'


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    rules = parse_rules(lines)
    start_pattern = '.#./..#/###'
    for number in (5, 18):
        pixels_on = count_pixels(enhance_n_times(rules, start_pattern, number))
        print(f'Pixels on after {number} iterations: {pixels_on}')


def enhance_n_times(rules, pattern, times):
    """Enhance pattern number of times."""
    for _ in range(times):
        pattern = enhance(rules, pattern)
    return pattern


def enhance(rules, pattern):
    """Enhance pattern using rules."""
    grid = pattern.split('/')
    if len(grid) in (2, 3):
        return rules[pattern]

    split = 3 if len(grid) % 2 == 1 else 2
    new_grid = []
    for row_index, cur_row in enumerate(grid[::split]):
        sub_grids = []
        for col_index, cur_col in enumerate(cur_row[::split]):
            sub_grid = get_sub_grid(grid, row_index, col_index, split)
            enhanced_sub_grid = enhance(rules, '/'.join(sub_grid))
            sub_grids.append(enhanced_sub_grid.split('/'))
        new_grid.extend(join_sub_grids(sub_grids))
    return '/'.join(new_grid)


def join_sub_grids(sub_grids):
    """Join sub_grids together, by corresponding rows."""
    rows = []
    sub_rows = len(sub_grids[0])
    for row in range(sub_rows):
        rows.append('')
        for index, col in enumerate(sub_grids):
            rows[row] += col[row]
    return rows


def get_sub_grid(grid, row_index, col_index, split):
    """Get sub_grid from grid containing split numbers of rows and cols."""
    return [row[col_index * split:(col_index + 1) * split]
            for row in grid[row_index * split:(row_index + 1) * split]]


def parse_rules(lines):
    """Parse lines to rules dict mapping input pattern to output pattern."""
    rules = {}
    for line in lines:
        possible_patterns, output = parse_rule(line)
        for pattern in possible_patterns:
            rules[pattern] = output
    return rules


def parse_rule(line):
    """Parse rule from line.

    Return tuple with set of unique possible input_patterns,
    and output pattern."""
    input_pattern, output = line.split(' => ')
    return get_possible_patterns(input_pattern), output


def get_possible_patterns(pattern):
    """Get possible unique patterns from pattern, by flipping and rotating."""
    patterns = set()
    cur_grid = pattern.split('/')
    for _ in range(4):
        cur_grid = rotate(cur_grid)
        patterns.add('/'.join(cur_grid))
        patterns.add('/'.join(flip(cur_grid)))
    return patterns


def rotate(pattern):
    """Rotate pattern by 90 angles to the right."""
    rotated = []
    for row_no, row in enumerate(pattern):
        rotated.append('')
        for col_no, char in enumerate(row):
            rotated[row_no] += pattern[len(pattern) - 1 - col_no][row_no]
    return rotated


def flip(pattern):
    """Flip pattern horizontally."""
    return [row[::-1] for row in pattern]


def count_pixels(pattern):
    """Count ON pixels."""
    return pattern.count(ON)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
